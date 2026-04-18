import cv2
import numpy as np
import tempfile
import os

# ─────────────────────────────────────────────
# IMAGE ANALYSIS  (used for images)
# ─────────────────────────────────────────────
def analyze_image(uploaded_file):
    """
    Weighted authenticity analysis for a single image.
    Returns 0-100 (higher = more likely real).
    """
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    uploaded_file.seek(0)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if img is None:
        return 50.0
    return _score_frame(img)


# ─────────────────────────────────────────────
# VIDEO ANALYSIS  (used for videos)
# ─────────────────────────────────────────────
def analyze_video(uploaded_file):
    """
    Extracts multiple frames from a video and runs real detection on each.
    Returns (video_score, ai_score) both 0-100.
    """
    # Write to a temp file so OpenCV can read it
    suffix = os.path.splitext(uploaded_file.name)[-1] if hasattr(uploaded_file, 'name') else '.mp4'
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    uploaded_file.seek(0)

    try:
        cap = cv2.VideoCapture(tmp_path)
        if not cap.isOpened():
            return 50.0, 50.0

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps         = cap.get(cv2.CAP_PROP_FPS) or 25
        duration    = total_frames / fps

        # Sample up to 12 frames spread across the video
        num_samples = min(12, max(4, total_frames // 30))
        sample_positions = np.linspace(0, max(1, total_frames - 1), num_samples, dtype=int)

        frame_scores   = []
        ai_scores      = []
        temporal_diffs = []
        prev_gray      = None

        for pos in sample_positions:
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(pos))
            ret, frame = cap.read()
            if not ret or frame is None:
                continue

            # Per-frame authenticity
            frame_scores.append(_score_frame(frame))
            ai_scores.append(_ai_score_frame(frame))

            # Temporal consistency (real videos have natural motion)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if prev_gray is not None:
                diff = cv2.absdiff(gray, prev_gray)
                temporal_diffs.append(np.mean(diff))
            prev_gray = gray

        cap.release()
    finally:
        os.unlink(tmp_path)

    if not frame_scores:
        return 50.0, 50.0

    base_video = float(np.mean(frame_scores))
    base_ai    = float(np.mean(ai_scores))

    # ── Temporal consistency check ──────────────────────────────────────
    # Real videos have natural, varied motion between frames.
    # AI-generated / deepfake videos often have unnaturally uniform diffs.
    if temporal_diffs:
        td_mean = np.mean(temporal_diffs)
        td_std  = np.std(temporal_diffs)

        # Natural motion: moderate mean diff AND some variance
        if 3 < td_mean < 40 and td_std > 1.5:
            temporal_bonus = 5
        elif td_mean < 1.0 or td_std < 0.5:
            # Nearly static or perfectly uniform → suspicious
            temporal_bonus = -15
        elif td_mean > 60:
            # Extreme flickering → suspicious
            temporal_bonus = -10
        else:
            temporal_bonus = 0

        base_video = np.clip(base_video + temporal_bonus, 0, 100)
        base_ai    = np.clip(base_ai    + temporal_bonus, 0, 100)

    # ── Frame consistency check ─────────────────────────────────────────
    # Real videos have some natural variance across frames.
    # AI videos often have suspiciously consistent per-frame scores.
    score_variance = np.std(frame_scores)
    if score_variance < 3:
        # All frames score almost identically → AI-generated flag
        base_video = np.clip(base_video - 12, 0, 100)
        base_ai    = np.clip(base_ai    - 12, 0, 100)
    elif score_variance > 5:
        # Healthy variance → slight boost
        base_video = np.clip(base_video + 3, 0, 100)

    return float(base_video), float(base_ai)


# ─────────────────────────────────────────────
# INTERNAL HELPERS
# ─────────────────────────────────────────────
def _score_frame(img):
    """Weighted authenticity score for one BGR frame/image."""
    scores, weights = [], []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 1. JPEG / compression artifacts (weight 30)
    block_score, block_count = 0, 0
    for i in range(0, min(gray.shape[0] - 8, 400), 8):
        for j in range(0, min(gray.shape[1] - 8, 400), 8):
            bv = np.var(gray[i:i+8, j:j+8].astype(float))
            if 50 < bv < 3000:
                block_score += 1
            block_count += 1
    compression_ratio = block_score / max(1, block_count)
    if   compression_ratio > 0.70: scores.append(95)
    elif compression_ratio > 0.50: scores.append(85)
    elif compression_ratio > 0.30: scores.append(70)
    else:                          scores.append(35)
    weights.append(30)

    # 2. High-frequency detail (weight 25)
    lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    if   lap_var > 300: scores.append(95)
    elif lap_var > 150: scores.append(85)
    elif lap_var > 80:  scores.append(70)
    elif lap_var > 40:  scores.append(55)
    else:               scores.append(28)
    weights.append(25)

    # 3. Sensor noise (weight 20)
    h, w = gray.shape
    noise_levels = []
    for _ in range(8):
        y = np.random.randint(10, max(11, h - 60))
        x = np.random.randint(10, max(11, w - 60))
        region = gray[y:y+50, x:x+50].astype(float)
        blurred = cv2.GaussianBlur(region, (5, 5), 0)
        noise_levels.append(np.std(region - blurred))
    avg_noise = np.mean(noise_levels)
    noise_std = np.std(noise_levels)
    if   2 < avg_noise < 8  and noise_std < 2: scores.append(95)
    elif 1 < avg_noise < 10 and noise_std < 3: scores.append(80)
    elif avg_noise > 0.5:                       scores.append(60)
    else:                                       scores.append(30)
    weights.append(20)

    # 4. Color channel correlation (weight 15)
    b, g, r = cv2.split(img)
    n = min(20000, b.size)
    idx = np.random.choice(b.size, n, replace=False)
    rg = abs(np.corrcoef(r.flatten()[idx], g.flatten()[idx])[0, 1])
    rb = abs(np.corrcoef(r.flatten()[idx], b.flatten()[idx])[0, 1])
    avg_corr = (rg + rb) / 2
    if   0.45 < avg_corr < 0.75: scores.append(90)
    elif 0.35 < avg_corr < 0.85: scores.append(75)
    elif 0.25 < avg_corr < 0.90: scores.append(60)
    else:                         scores.append(38)
    weights.append(15)

    # 5. Resolution / aspect ratio (weight 10)
    total_px = h * w
    ar = w / h if h else 1
    std_ratios = [16/9, 4/3, 3/2, 1.0, 9/16, 3/4, 2/3]
    ratio_ok = any(abs(ar - r) < 0.15 for r in std_ratios)
    if   total_px > 2_000_000 and ratio_ok: scores.append(95)
    elif total_px > 1_000_000 and ratio_ok: scores.append(85)
    elif total_px > 500_000:                scores.append(70)
    else:                                   scores.append(55)
    weights.append(10)

    final = float(np.average(scores, weights=weights))
    # Boost / penalty
    if compression_ratio > 0.7 and lap_var > 200 and avg_noise > 2:
        final = min(100, final + 3)
    if compression_ratio < 0.3 and lap_var < 50:
        final = max(0,   final - 10)
    return float(np.clip(final, 0, 100))


def _ai_score_frame(img):
    """AI-generation detection score for one BGR frame/image."""
    scores, weights = [], []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    # 1. Frequency domain (weight 35)
    sz = min(512, min(h, w))
    gr = cv2.resize(gray, (sz, sz)) if (h > sz or w > sz) else gray
    mag = np.log(np.abs(np.fft.fftshift(np.fft.fft2(gr))) + 1)
    cy, cx = sz // 2, sz // 2
    Y, X = np.ogrid[:sz, :sz]
    dist = np.sqrt((X - cx)**2 + (Y - cy)**2)
    lf = mag[dist < sz//8].mean()
    mf = mag[(dist >= sz//8) & (dist < sz//4)].mean()
    hf = mag[dist >= sz//4].mean()
    fb = (mf + hf) / (lf + 1e-10)
    if   0.55 < fb < 0.95: scores.append(95)
    elif 0.45 < fb < 1.10: scores.append(82)
    elif 0.35 < fb < 1.30: scores.append(65)
    else:                   scores.append(32)
    weights.append(35)

    # 2. Chromatic aberration (weight 25)
    b, g, r = cv2.split(img)
    er = cv2.Canny(r, 100, 200)
    eg = cv2.Canny(g, 100, 200)
    eb = cv2.Canny(b, 100, 200)
    te = np.sum(er > 0) + 1
    mr = (np.sum(np.abs(er.astype(int) - eg.astype(int))) +
          np.sum(np.abs(er.astype(int) - eb.astype(int)))) / (2 * te)
    if   0.18 < mr < 0.32: scores.append(92)
    elif 0.12 < mr < 0.40: scores.append(78)
    elif 0.08 < mr < 0.50: scores.append(60)
    else:                   scores.append(35)
    weights.append(25)

    # 3. Texture (weight 20)
    tvars, gvals = [], []
    for _ in range(15):
        yp = np.random.randint(5, max(6, h - 37))
        xp = np.random.randint(5, max(6, w - 37))
        patch = gray[yp:yp+32, xp:xp+32]
        tvars.append(np.var(patch))
        gx = cv2.Sobel(patch, cv2.CV_64F, 1, 0, ksize=3)
        gy = cv2.Sobel(patch, cv2.CV_64F, 0, 1, ksize=3)
        gvals.append(np.mean(np.sqrt(gx**2 + gy**2)))
    at, ts, ag = np.mean(tvars), np.std(tvars), np.mean(gvals)
    if   at > 150 and ts < 400 and ag > 8: scores.append(93)
    elif at > 80  and ts < 600 and ag > 5: scores.append(80)
    elif at > 40:                           scores.append(62)
    else:                                   scores.append(35)
    weights.append(20)

    # 4. Color naturalness (weight 12)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hc, sc, vc = cv2.split(hsv)
    hist = np.histogram(hc, bins=180)[0] / hc.size
    he = -np.sum((hist + 1e-10) * np.log(hist + 1e-10))
    ss, vs = np.std(sc), np.std(vc)
    if   he > 4.5 and 25 < ss < 80 and 30 < vs < 90: scores.append(90)
    elif he > 3.5 and 15 < ss < 100:                  scores.append(75)
    else:                                              scores.append(52)
    weights.append(12)

    # 5. Dimensions (weight 8)
    tp = h * w
    ar = w / h if h else 1
    ok = tp > 500_000 and 0.5 < ar < 2.5
    if   ok and tp > 2_000_000: scores.append(92)
    elif ok:                     scores.append(80)
    elif tp > 500_000:           scores.append(65)
    else:                        scores.append(50)
    weights.append(8)

    final = float(np.average(scores, weights=weights))
    if fb > 0.6 and mr > 0.15 and at > 150:
        final = min(100, final + 4)
    if fb < 0.35 and mr < 0.1:
        final = max(0,   final - 12)
    return float(np.clip(final, 0, 100))
