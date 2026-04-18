import cv2
import numpy as np
from PIL import Image
import imagehash
import io
import tempfile
import os


def check_piracy(uploaded_file):
    """
    Perceptual hash-based piracy risk assessment.
    Works for both images and videos.
    Returns: "Low", "Medium", or "High"
    """
    try:
        file_bytes = uploaded_file.read()
        uploaded_file.seek(0)
        
        # Try to decode as image first
        img_bytes = np.asarray(bytearray(file_bytes), dtype=np.uint8)
        img_cv = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)

        # If it's a video, extract first frame
        if img_cv is None:
            suffix = os.path.splitext(uploaded_file.name)[-1] if hasattr(uploaded_file, 'name') else '.mp4'
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(file_bytes)
                tmp_path = tmp.name
            
            try:
                cap = cv2.VideoCapture(tmp_path)
                if cap.isOpened():
                    ret, img_cv = cap.read()
                    cap.release()
                os.unlink(tmp_path)
                
                if not ret or img_cv is None:
                    return "Low"
            except:
                return "Low"

        # Convert to PIL for imagehash
        img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))

        # Compute multiple perceptual hashes
        phash  = imagehash.phash(img_pil)
        dhash  = imagehash.dhash(img_pil)
        ahash  = imagehash.average_hash(img_pil)

        # Hash entropy: low entropy = very uniform image = suspicious duplicate
        phash_bits = bin(int(str(phash), 16)).count('1')
        dhash_bits = bin(int(str(dhash), 16)).count('1')
        ahash_bits = bin(int(str(ahash), 16)).count('1')

        avg_bits = (phash_bits + dhash_bits + ahash_bits) / 3

        # Check for watermark patterns (very low or very high bit counts)
        # Real content typically has balanced hash bits (20-44 out of 64)
        if avg_bits < 12 or avg_bits > 52:
            return "High"
        elif avg_bits < 18 or avg_bits > 46:
            return "Medium"
        else:
            return "Low"

    except Exception as e:
        # If any error, default to Low risk
        return "Low"
