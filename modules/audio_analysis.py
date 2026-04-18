import cv2
import numpy as np

def detect_ai_generated(uploaded_file):
    """
    Advanced AI-generated content detection with weighted multi-factor analysis
    Returns a score between 0-100 (higher = more likely real/authentic)
    """
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    uploaded_file.seek(0)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    if img is None:
        return 50.0
    
    scores = []
    weights = []
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    
    # 1. Frequency Domain Analysis (Weight: 35%) - MOST CRITICAL
    # AI images have distinct frequency signatures
    analysis_size = min(512, min(h, w))
    if h > analysis_size or w > analysis_size:
        gray_resized = cv2.resize(gray, (analysis_size, analysis_size))
    else:
        gray_resized = gray
    
    # FFT analysis
    f_transform = np.fft.fft2(gray_resized)
    f_shift = np.fft.fftshift(f_transform)
    magnitude = np.abs(f_shift)
    magnitude = np.log(magnitude + 1)
    
    # Analyze frequency distribution
    center_h, center_w = analysis_size//2, analysis_size//2
    y, x = np.ogrid[:analysis_size, :analysis_size]
    distances = np.sqrt((x - center_w)**2 + (y - center_h)**2)
    
    # Real photos have balanced frequency across bands
    low_freq = magnitude[distances < analysis_size//8].mean()
    mid_freq = magnitude[(distances >= analysis_size//8) & (distances < analysis_size//4)].mean()
    high_freq = magnitude[distances >= analysis_size//4].mean()
    
    freq_balance = (mid_freq + high_freq) / (low_freq + 1e-10)
    
    # Real photos: 0.5-1.0, AI often: <0.3 or >1.3
    if 0.55 < freq_balance < 0.95:
        scores.append(95)
    elif 0.45 < freq_balance < 1.1:
        scores.append(82)
    elif 0.35 < freq_balance < 1.3:
        scores.append(65)
    else:
        scores.append(35)  # Likely AI
    weights.append(35)
    
    # 2. Edge Consistency & Chromatic Aberration (Weight: 25%)
    b, g, r = cv2.split(img)
    
    # Real lenses have slight chromatic aberration (color fringing)
    edges_r = cv2.Canny(r, 100, 200)
    edges_g = cv2.Canny(g, 100, 200)
    edges_b = cv2.Canny(b, 100, 200)
    
    # Calculate edge misalignment
    total_edges = np.sum(edges_r > 0) + 1
    edge_diff_rg = np.sum(np.abs(edges_r.astype(int) - edges_g.astype(int)))
    edge_diff_rb = np.sum(np.abs(edges_r.astype(int) - edges_b.astype(int)))
    
    misalignment_ratio = (edge_diff_rg + edge_diff_rb) / (2 * total_edges)
    
    # Real photos: 0.15-0.35, AI: <0.1 or >0.45
    if 0.18 < misalignment_ratio < 0.32:
        scores.append(92)
    elif 0.12 < misalignment_ratio < 0.4:
        scores.append(78)
    elif 0.08 < misalignment_ratio < 0.5:
        scores.append(60)
    else:
        scores.append(38)  # Too perfect or too chaotic
    weights.append(25)
    
    # 3. Local Texture Patterns (Weight: 20%)
    texture_scores = []
    gradient_scores = []
    
    # Sample 15 random patches
    for _ in range(15):
        y_pos = np.random.randint(5, max(6, h-37))
        x_pos = np.random.randint(5, max(6, w-37))
        patch = gray[y_pos:y_pos+32, x_pos:x_pos+32]
        
        if patch.size > 0:
            # Texture variance
            local_var = np.var(patch)
            texture_scores.append(local_var)
            
            # Gradient analysis
            gx = cv2.Sobel(patch, cv2.CV_64F, 1, 0, ksize=3)
            gy = cv2.Sobel(patch, cv2.CV_64F, 0, 1, ksize=3)
            grad_mag = np.sqrt(gx**2 + gy**2)
            gradient_scores.append(np.mean(grad_mag))
    
    if len(texture_scores) > 0:
        avg_texture = np.mean(texture_scores)
        texture_std = np.std(texture_scores)
        avg_gradient = np.mean(gradient_scores)
        
        # Real photos have consistent, natural texture
        if avg_texture > 150 and texture_std < 400 and avg_gradient > 8:
            scores.append(93)
        elif avg_texture > 80 and texture_std < 600 and avg_gradient > 5:
            scores.append(80)
        elif avg_texture > 40:
            scores.append(65)
        else:
            scores.append(40)  # Too smooth = AI
        weights.append(20)
    
    # 4. Color Distribution & Naturalness (Weight: 12%)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h_channel, s_channel, v_channel = cv2.split(hsv)
    
    # Real photos have natural color distribution
    h_entropy = -np.sum((np.histogram(h_channel, bins=180)[0] / h_channel.size + 1e-10) * 
                        np.log(np.histogram(h_channel, bins=180)[0] / h_channel.size + 1e-10))
    s_std = np.std(s_channel)
    v_std = np.std(v_channel)
    
    if h_entropy > 4.5 and 25 < s_std < 80 and 30 < v_std < 90:
        scores.append(90)
    elif h_entropy > 3.5 and 15 < s_std < 100:
        scores.append(75)
    else:
        scores.append(55)
    weights.append(12)
    
    # 5. Image Dimensions & Properties (Weight: 8%)
    total_pixels = h * w
    aspect_ratio = w / h if h > 0 else 1
    
    # Real camera dimensions
    realistic_dims = (
        (w >= 800 and h >= 600) and
        (total_pixels > 500000) and
        (0.5 < aspect_ratio < 2.5)
    )
    
    if realistic_dims and total_pixels > 2000000:
        scores.append(92)
    elif realistic_dims:
        scores.append(80)
    elif total_pixels > 500000:
        scores.append(65)
    else:
        scores.append(50)
    weights.append(8)
    
    # Calculate weighted average
    if len(scores) > 0 and len(weights) > 0:
        final_score = np.average(scores, weights=weights)
    else:
        final_score = 50.0
    
    # Apply confidence boost for strong real photo indicators
    if freq_balance > 0.6 and misalignment_ratio > 0.15 and avg_texture > 150:
        final_score = min(100, final_score + 4)
    
    # Apply penalty for AI indicators
    if freq_balance < 0.35 and misalignment_ratio < 0.1:
        final_score = max(0, final_score - 12)
    
    final_score = np.clip(final_score, 0, 100)
    
    return final_score
