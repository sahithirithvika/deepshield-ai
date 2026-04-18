import cv2
import numpy as np
from PIL import Image
import io

def analyze_image(uploaded_file):
    """
    Advanced image authenticity analysis
    Returns a score between 0-100 (higher = more likely real)
    """
    # Convert uploaded file to image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    uploaded_file.seek(0)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    if img is None:
        return 50.0
    
    score = 0
    max_score = 0
    
    # 1. JPEG/Compression Analysis - Real photos have compression artifacts
    max_score += 25
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Check for DCT block artifacts (8x8 blocks in JPEG)
    block_artifacts = 0
    for i in range(0, min(gray.shape[0], 200), 8):
        for j in range(0, min(gray.shape[1], 200), 8):
            if i+8 < gray.shape[0] and j+8 < gray.shape[1]:
                block = gray[i:i+8, j:j+8].astype(float)
                block_var = np.var(block)
                if 10 < block_var < 5000:
                    block_artifacts += 1
    
    artifact_ratio = block_artifacts / max(1, (min(gray.shape[0], 200)//8) * (min(gray.shape[1], 200)//8))
    if artifact_ratio > 0.6:
        score += 25
    elif artifact_ratio > 0.4:
        score += 20
    else:
        score += 12
    
    # 2. High-frequency detail analysis - Real photos have natural high-freq content
    max_score += 25
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    laplacian_var = laplacian.var()
    
    if laplacian_var > 200:  # Strong natural texture
        score += 25
    elif laplacian_var > 100:
        score += 20
    elif laplacian_var > 50:
        score += 15
    else:
        score += 8
    
    # 3. Color channel correlation - Real photos have natural RGB correlation
    max_score += 20
    b, g, r = cv2.split(img)
    
    # Calculate correlation between channels
    rg_corr = np.corrcoef(r.flatten()[:10000], g.flatten()[:10000])[0,1]
    rb_corr = np.corrcoef(r.flatten()[:10000], b.flatten()[:10000])[0,1]
    gb_corr = np.corrcoef(g.flatten()[:10000], b.flatten()[:10000])[0,1]
    
    avg_corr = (abs(rg_corr) + abs(rb_corr) + abs(gb_corr)) / 3
    
    if 0.3 < avg_corr < 0.85:  # Natural correlation range
        score += 20
    elif 0.2 < avg_corr < 0.9:
        score += 15
    else:
        score += 10
    
    # 4. Noise pattern analysis - Real cameras have sensor noise
    max_score += 15
    # Sample small regions to check for consistent noise
    h, w = gray.shape
    noise_samples = []
    for _ in range(5):
        y = np.random.randint(0, max(1, h-50))
        x = np.random.randint(0, max(1, w-50))
        region = gray[y:y+50, x:x+50]
        if region.size > 0:
            noise_samples.append(np.std(region))
    
    if len(noise_samples) > 0:
        noise_consistency = np.std(noise_samples)
        if noise_consistency < 15:  # Consistent noise pattern
            score += 15
        else:
            score += 10
    
    # 5. Resolution and metadata check
    max_score += 15
    height, width = img.shape[:2]
    total_pixels = height * width
    aspect_ratio = width / height if height > 0 else 1
    
    # Real photos typically have standard aspect ratios and high resolution
    standard_ratios = [16/9, 4/3, 3/2, 1/1, 9/16]
    ratio_match = any(abs(aspect_ratio - ratio) < 0.1 for ratio in standard_ratios)
    
    if total_pixels > 1000000 and ratio_match:
        score += 15
    elif total_pixels > 500000:
        score += 12
    else:
        score += 8
    
    # Normalize to 0-100
    final_score = (score / max_score) * 100
    
    # Boost score for high-quality images with strong indicators
    if laplacian_var > 200 and artifact_ratio > 0.5 and total_pixels > 1000000:
        final_score = min(100, final_score + 5)
    
    final_score = np.clip(final_score, 0, 100)
    
    return final_score
