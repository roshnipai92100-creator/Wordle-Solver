import pyautogui
import cv2
import numpy as np
import time


def capture_screen():
    screenshot = pyautogui.screenshot()

    image = np.array(screenshot)

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    return image

if __name__ == '__main__':
    print("Open Wordle. Capturing in 3 seconds...")

    time.sleep(3)

    screen = capture_screen()

    cv2.imwrite('wordle_screenshot.png', screen)

    print("Screenshot saved successfully!")