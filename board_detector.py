import cv2

def detect_tiles(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    tiles = []

    for contour in contours:

        perimeter = cv2.arcLength(contour, True)

        polygon = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

        if len(polygon) != 4:
            continue

        x, y, w, h = cv2.boundingRect(polygon)

        if w < 25 or h < 25:
            continue

        aspect_ratio = w / h

        if not 0.9 <= aspect_ratio <= 1.1:
            continue

        tiles.append((x, y, w, h))

    return tiles

def remove_duplicates(tiles, tolerance=5):
    unique_tiles = []

    for tile in tiles:
        x, y, w, h = tile

        center_x = x + w / 2
        center_y = y + h / 2

        duplicate = False

        for existing in unique_tiles:
            ex, ey, ew, eh = existing

            existing_center_x = ex + ew / 2
            existing_center_y = ey + eh / 2

            if (
                abs(center_x - existing_center_x) <= tolerance
                and abs(center_y - existing_center_y) <= tolerance
            ):
                duplicate = True
                break

        if not duplicate:
            unique_tiles.append(tile)

    return unique_tiles

def organize_grid(tiles):
    # Sort tiles top -> bottom
    tiles = sorted(tiles, key=lambda tile: tile[1])

    grid = []

    for row in range(6):

        # Take five tiles per row
        start = row * 5
        end = start + 5

        row_tiles = tiles[start:end]

        # Sort each row left -> right
        row_tiles.sort(key=lambda tile: tile[0])

        grid.append(row_tiles)

    return grid

if __name__ == "__main__":
    image = cv2.imread("wordle_screenshot.png")

    if image is None:
        raise FileNotFoundError("Screenshot not found.")

    tiles = detect_tiles(image)

    print(f"Raw detections: {len(tiles)}")

    tiles = remove_duplicates(tiles)

    print(f"Unique detections: {len(tiles)}\n")

    grid = organize_grid(tiles)

    for row_number, row in enumerate(grid):
        print(f"Row {row_number + 1}:")

        for tile in row:
            print(f"    {tile}")

    for x, y, w, h in tiles:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imwrite("detected_tiles.png", image)

    print("\nDetection image saved!")