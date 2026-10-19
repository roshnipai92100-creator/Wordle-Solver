import cv2
import time

from screen_reader import capture_screen
from board_detector import detect_tiles, remove_duplicates, organize_grid
from tile_reader import read_color
from config import SCREENSHOT_PATH, DEBUG_IMAGE_PATH


def main():
    # Step 1: Capture the screen
    print("Open Wordle. Capturing in 3 seconds...")

    time.sleep(3)

    image = capture_screen()

    cv2.imwrite(SCREENSHOT_PATH, image)

    # Step 2: Detect possible tiles
    tiles = detect_tiles(image)

    print(f"Raw detections: {len(tiles)}")

    # Step 3: Remove duplicates
    tiles = remove_duplicates(tiles)

    print(f"Unique detections: {len(tiles)}")

    # Step 4: Organize tiles into rows and columns
    if len(tiles) != 30:
        print("Could not identify exactly 30 Wordle tiles.")
        return

    grid = organize_grid(tiles)

    # Step 5: Read each tile's color
    print("\nDetected Wordle Board:")

    for row_number, row in enumerate(grid):

        colors = []

        for tile in row:
            color = read_color(image, tile)
            colors.append(color)

        print(f"Row {row_number + 1}: {colors}")

    # Step 6: Save a debugging image
    debug_image = image.copy()

    for row in grid:
        for x, y, w, h in row:
            cv2.rectangle(
                debug_image,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

    for row_number, row in enumerate(grid):

        colors = []

        for tile in row:
            color = read_color(image, tile)

            x, y, w, h = tile

            sample_x = x + int(w * 0.2)
            sample_y = y + int(h * 0.2)

            bgr = image[sample_y, sample_x]
            rgb = bgr[::-1]

            print(f"Tile ({x}, {y}) RGB: {rgb}")

            colors.append(color)

        print(f"Row {row_number + 1}: {colors}")

    cv2.imwrite(DEBUG_IMAGE_PATH, debug_image)

    print("\nScreen reading complete!")


if __name__ == "__main__":
    main()