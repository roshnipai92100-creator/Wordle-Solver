import cv2
import pytesseract

from config import TESSERACT_PATH

import numpy as np

from config import COLORS, COLOR_TOLERANCE

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def read_color(image, tile):
    x, y, w, h = tile

    # Sample a small region away from the letter
    x1 = x + int(w * 0.15)
    x2 = x + int(w * 0.30)

    y1 = y + int(h * 0.15)
    y2 = y + int(h * 0.30)

    patch = image[y1:y2, x1:x2]

    # Calculate the median color
    median_bgr = np.median(patch, axis=(0, 1))

    # Convert BGR to RGB
    median_rgb = median_bgr[::-1]

    closest_color = None
    smallest_distance = float("inf")

    # Check every possible version of every feedback color
    for name, references in COLORS.items():

        for reference in references:

            distance = np.linalg.norm(
                median_rgb - np.array(reference)
            )

            if distance < smallest_distance:
                smallest_distance = distance
                closest_color = name

    if smallest_distance > COLOR_TOLERANCE:
        return "unknown"

    return closest_color

def read_letter(image, tile, color):

    # Only submitted, colored tiles should be read by OCR.
    if color not in ("green", "yellow", "gray"):
        return ""

    x, y, w, h = tile

    # Crop the tile while excluding its border.
    margin_x = int(w * 0.12)
    margin_y = int(h * 0.12)

    crop = image[
        y + margin_y:y + h - margin_y,
        x + margin_x:x + w - margin_x
    ]

    # Estimate the tile's background color from its upper-left corner.
    background = crop[2, 2].astype("float32")

    # Measure how different each pixel is from the background.
    difference = np.abs(
        crop.astype(np.float32) - background
    )

    difference = difference.max(axis=2)

    # Turn the letter into white pixels and the background into black.
    mask = (difference > 40).astype(np.uint8) * 255

    # Enlarge the image to help Tesseract recognize small letters.
    mask = cv2.resize(
        mask,
        None,
        fx=4,
        fy=4,
        interpolation=cv2.INTER_CUBIC
    )

    # Give the character some surrounding white space.
    mask = cv2.copyMakeBorder(
        mask,
        20, 20, 20, 20,
        cv2.BORDER_CONSTANT,
        value=0
    )

    # Tesseract generally works well with dark text on a light background.
    mask = cv2.bitwise_not(mask)

    settings = (
        "--psm 10 "
        "-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    )

    letter = pytesseract.image_to_string(
        mask,
        config=settings
    ).strip().upper()

    # Retry using a different segmentation mode if OCR fails.
    if len(letter) != 1 or not letter.isalpha():
        fallback_settings = (
            "--psm 13 "
            "-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        )

        letter = pytesseract.image_to_string(
            mask,
            config=fallback_settings
        ).strip().upper()

    if len(letter) != 1 or not letter.isalpha():
        return "I"

    return letter