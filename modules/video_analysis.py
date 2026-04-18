import cv2
import numpy as np
from PIL import Image
import io

def analyze_image(uploaded_file):
    """
    Advanced image authenticity analysis with weighted scoring
    Returns a score between 0-100 (higher = more likely real)
    """
    # Convert uploaded file to image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    uploaded_file.seek(0)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    if img is None:
        return 50.0
    
    scores = []
    weights = []
    
    # 1. JPEG Compression Artifacts (Weight: 30%) - CRITICAL for real photos
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Check for 8x8 DCT block boundaries (JPEG compression signature)
    block_score = 0
    block_count = 0
    for i in range(0, min(gray.shape[0]-8, 400), 8):
        for j in range(0, min(gray.shape[1]-8, 400), 8):
            block = gray[i:i+8, j:j+8].astype(float)
            # Real JPEG has variance in blocks
            block_var = np.var(block)
            if 50 < block_var < 3000:  # Natural JPEG block variance
                block_score += 1
            block_count += 1
    
    if block_count > 0:
        compression_ratio = block_score / block_count
        if compression_ratio > 0.7:  # Strong JPEG artifacts
            scores.append(95)
        elif compression_ratio > 0.5:
            scores.append(85)
        elif compression_ratio > 0.3:
            scores.append(70)
        else:
            scores.append(40)  # Likely AI-generated (no compression)
        weights.append(30)
    
    # 2. High-Frequency Detail (Weight: 25%) - Real photos have natural texture
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    laplacian_var = laplacian.var()
    
    if laplacian_var > 300:  # Very sharp, natural detail
        scores.append(95)
    elif laplacian_var > 150:
        scores.append(85)
    elif laplacian_var > 80:
        scores.append(70)
    elif laplacian_var > 40:
        scores.append(55)
    else:
        scores.append(30)  # Too smooth, likely AI
    weights.append(25)
    
    # 3. Sensor Noise Pattern (Weight: 20%) - Real cameras have noise
    # Sample multiple regions for noise consistency
    h, w = gray.shape
    noise_levels = []
    
    for _ in range(8):
        y = np.random.randint(10, max(11, h-60))
        x = np.random.randint(10, max(11, w-60))
        region = gray[y:y+50, x:x+50].astype(float)
        
        if region.size > 0:
            # High-pass filter to isolate noise
            blurred = cv2.GaussianBlur(region, (5, 5), 0)
            noise = region - blurred
            noise_levels.append(np.std(noise))
    
    if len(noise_levels) > 0:
        avg_noise = np.mean(noise_levels)
        noise_consistency = np.std(noise_levels)
        
        # Real photos have consistent, moderate noise
        if 2 < avg_noise < 8 and noise_consistency < 2:
            scores.append(95)
        elif 1 < avg_noise < 10 and noise_consistency < 3:
            scores.append(80)
        elif avg_noise > 0.5:
            scores.append(65)
        else:
            scores.append(35)  # No noise = likely AI
        weights.append(20)
    
    # 4. Color Channel Correlation (Weight: 15%)
    b, g, r = cv2.split(img)
    
    # Sample pixels for correlation (faster)
    sample_size = min(20000, b.size)
    indices = np.random.choice(b.size, sample_size, replace=False)
    
    r_flat = r.flatten()[indices]
    g_flat = g.flatten()[indices]
    b_flat = b.flatten()[indices]
    
    rg_corr = np.corrcoef(r_flat, g_flat)[0,1]
    rb_corr = np.corrcoef(r_flat, b_flat)[0,1]
    
    avg_corr = (abs(rg_corr) + abs(rb_corr)) / 2
    
    # Real photos have moderate correlation (0.4-0.8)
    if 0.45 < avg_corr < 0.75:
        scores.append(90)
    elif 0.35 < avg_corr < 0.85:
        scores.append(75)
    elif 0.25 < avg_corr < 0.9:
        scores.append(60)
    else:
        scores.append(40)  # Unusual correlation
    weights.append(15)
    
    # 5. Resolution & Metadata (Weight: 10%)
    height, width = img.shape[:2]
    total_pixels = height * width
    aspect_ratio = width / height if height > 0 else 1
    
    # Real photos typically have standard ratios and high resolution
    standard_ratios = [16/9, 4/3, 3/2, 1.5, 1/1, 9/16, 3/4, 2/3]
    ratio_match = any(abs(aspect_ratio - ratio) < 0.15 for ratio in standard_ratios)
    
    if total_pixels > 2000000 and ratio_match:  # High-res with standard ratio
        scores.append(95)
    elif total_pixels > 1000000 and ratio_match:
        scores.append(85)
    elif total_pixels > 500000:
        scores.append(70)
    else:
        scores.append(60)
    weights.append(10)
    
    # Calculate weighted average
    if len(scores) > 0 and len(weights) > 0:
        final_score = np.average(scores, weights=weights)
    else:
        final_score = 50.0
    
    # Apply confidence boost for strong indicators
    if compression_ratio > 0.7 and laplacian_var > 200 and avg_noise > 2:
        final_score = min(100, final_score + 3)
    
    # Apply penalty for weak indicators
    if compression_ratio < 0.3 and laplacian_var < 50:
        final_score = max(0, final_score - 10)
    
    final_score = np.clip(final_score, 0, 100)
    
    return final_score
