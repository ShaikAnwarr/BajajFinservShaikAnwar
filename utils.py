import pytesseract
import cv2
import numpy as np
from PIL import Image
import io
import re

def process_lab_report(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        open_cv_image = np.array(image)
        img = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)
    except Exception as e:
        print(f"Error opening image: {e}")
        return []

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

    text = pytesseract.image_to_string(thresh)
    print("OCR Output:\n", text)

    lines = text.split("\n")
    results = []
    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = re.match(r"([a-zA-Z \-/()]+)\s+([0-9.]+)\s+([0-9.]+)\s*[-to]*\s*([0-9.]+)", line)
        if match:
            test_name = match.group(1).strip()
            value = float(match.group(2))
            ref_low = float(match.group(3))
            ref_high = float(match.group(4))
            out_of_range = not (ref_low <= value <= ref_high)

            results.append({
                "test_name": test_name,
                "test_value": value,
                "bio_reference_range": f"{ref_low}-{ref_high}",
                "test_unit": "",
                "lab_test_out_of_range": out_of_range
            })

    print("Extracted Results:", results)
    return results
