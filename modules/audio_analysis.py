import cv2
import numpy as np

def detect_ai_generated(uploaded_file):
    """
    Advanced AI-generated content detection
    Returns a score between 0-100 (higher = more likely real/authentic)
    """
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    uploaded_file.seek(0)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    if img is None:
        return 50.0
    
    score = 0
    max_score = 0
    
    # 1. Frequency Domain Analysis - AI images have distinct frequency signatures
    max_score += 30
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Resize for consistent analysis
    analysis_size = min(512, min(gray.shape[0], gray.shape[1]))
    if gray.shape[0] > analysis_size or gray.shape[1] > analysis_size:
        gray_resized = cv2.resize(gray, (analysis_size, analysis_size))
    else:
        gray_resized = gray
    
    # FFT analysis
    f_transform = np.fft.fft2(gray_resized)
    f_shift = np.fft.fftshift(f_transform)
    magnitude = np.abs(f_shift)
    magnitude = np.log(magnitude + 1)
    
    # Real photos have more uniform frequency distribution
    h, w = magnitude.shape
    center_h, center_w = h//2, w//2
    
    # Check radial frequency distribution
    y, x = np.ogrid[:h, :w]
    distances = np.sqrt((x - center_w)**2 + (y - center_h)**2)
    
    # Sample different frequency bands
    low_freq = magnitude[distances < h//8].mean()
    mid_freq = magnitude[(distances >= h//8) & (distances < h//4)].mean()
    high_freq = magnitude[distances >= h//4].mean()
    
    # Real photos have balanced frequency content
    freq_balance = (mid_freq + high_freq) / (low_freq + 1e-10)
    
    if 0.4 < freq_balance < 1.2:  # Natural frequency distribution
        score += 30
    elif 0.3 < freq_balance < 1.5:
        score += 22
    else:
        score += 15
    
    # 2. Chromatic Aberration - Real lenses have chromatic aberration
    max_score += 20
    b, g, r = cv2.split(img)
    
    # Check for slight channel misalignment at edges (natural in real photos)
    edges_r = cv2.Canny(r, 50, 150)
    edges_g = cv2.Canny(g, 50, 150)
    edges_b = cv2.Canny(b, 50, 150)
    
    # Real photos have slight edge misalignment between channels
    edge_diff_rg = np.sum(np.abs(edges_r.astype(int) - edges_g.astype(int)))
    edge_diff_rb = np.sum(np.abs(edges_r.astype(int) - edges_b.astype(int)))
    
    total_edges = np.sum(edges_r > 0) + 1
    misalignment_ratio = (edge_diff_rg + edge_diff_rb) / (2 * total_edges)
    
    if 0.1 < misalignment_ratio < 0.4:  # Natural chromatic aberration
        score += 20
    elif 0.05 < misalignment_ratio < 0.5:
        score += 15
    else:
        score += 10
    
    # 3. Local Binary Patterns - Texture analysis
    max_score += 20
    # Sample texture patterns
    h, w = gray.shape
    texture_scores = []
    
    for _ in range(10):
        y = np.random.randint(0, max(1, h-32))
        x = np.random.randint(0, max(1, w-32))
        patch = gray[y:y+32, x:x+32]
        
        if patch.size > 0:
            # Calculate local variance
            local_var = np.var(patch)
            texture_scores.append(local_var)
    
    if len(texture_scores) > 0:
        texture_consistency = np.std(texture_scores)
        avg_texture = np.mean(texture_scores)
        
        # Real photos have consistent, natural texture
        if avg_texture > 100 and texture_consistency < 500:
            score += 20
        elif avg_texture > 50:
            score += 15
        else:
            score += 10
    
    # 4. EXIF and metadata indicators (simulated - checking image properties)
    max_score += 15
    height, width = img.shape[:2]
    
    # Check for realistic image dimensions
    realistic_dims = (
        (width >= 800 and height >= 600) and
        (width % 2 == 0 or height % 2 == 0)  # Camera sensors typically even dimensions
    )
    
    if realistic_dims:
        score += 15
    else:
        score += 10
    
    # 5. Gradient consistency - AI images sometimes have unnatural gradients
    max_score += 15
    grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    
    gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
    gradient_std = np.std(gradient_magnitude)
    
    # Real photos have natural gradient distribution
    if 20 < gradient_std < 80:
        score += 15
    elif 10 < gradient_std < 100:
        score += 12
    else:
        score += 8
    
    # Normalize to 0-100
    final_score = (score / max_score) * 100
    
    # Boost for strong real photo indicators
    if freq_balance > 0.5 and misalignment_ratio > 0.1 and avg_texture > 100:
        final_score = min(100, final_score + 5)
    
    final_score = np.clip(final_score, 0, 100)
    
    return final_score
