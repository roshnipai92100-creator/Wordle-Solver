# Tesseract installation path
TESSERACT_PATH = (
    r"C:\Users\Aditya\AppData\Local\Tesseract-OCR\tesseract.exe"
)

# Standard NYT Wordle tile colors (RGB)
COLORS = {
    "green": [
        (106, 170, 100),  # Light theme
        (83, 141, 78),    # Dark theme
        (245, 121, 58)    # High contrast (orange)
    ],

    "yellow": [
        (201, 180, 88),   # Light theme
        (181, 159, 59),   # Dark theme
        (133, 192, 249)   # High contrast (blue)
    ],

    "gray": [
        (120, 124, 126),  # Light theme
        (58, 58, 60)      # Dark theme
    ],

    "empty": [
        (255, 255, 255),  # Light theme
        (18, 18, 19)      # Dark theme
    ]
}

# Color detection settings
COLOR_TOLERANCE = 45
SAMPLE_POSITION = 0.2

# Board dimensions
ROWS = 6
COLUMNS = 5

# Screenshot settings
SCREENSHOT_PATH = "wordle_screenshot.png"
DEBUG_IMAGE_PATH = "detected_tiles.png"

# Detection settings
MIN_TILE_SIZE = 25
ASPECT_RATIO_MIN = 0.9
ASPECT_RATIO_MAX = 1.1
DUPLICATE_TOLERANCE = 5