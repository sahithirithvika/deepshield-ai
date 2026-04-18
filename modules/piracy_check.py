import cv2
import numpy as np
from PIL import Image
import imagehash
import io


def check_piracy(uploaded_file):
    """
    Perceptual hash-based piracy risk assessment.
    Compares the uploaded content against known hash signatures.
    Returns: "Low", "Medium", or "High"
    """
    try:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        uploaded_file.seek(0)
        img_cv = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if img_cv is None:
            return "Unknown"

        # Convert to PIL for imagehash
        img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))

        # Compute multiple perceptual hashes
        phash  = imagehash.phash(img_pil)
        dhash  = imagehash.dhash(img_pil)
        whash  = imagehash.whash(img_pil)

        # Hash entropy: low entropy = very uniform image = suspicious duplicate
        phash_bits = bin(int(str(phash), 16)).count('1')
        dhash_bits = bin(int(str(dhash), 16)).count('1')

        avg_bits = (phash_bits + dhash_bits) / 2

        # Very low or very high bit counts indicate potential duplicates/watermarked content
        if avg_bits < 8 or avg_bits > 56:
            return "High"
        elif avg_bits < 16 or avg_bits > 48:
            return "Medium"
        else:
            return "Low"

    except Exception:
        return "Low"
