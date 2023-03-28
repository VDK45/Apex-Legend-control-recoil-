import cv2
import numpy as np
from PIL import Image, ImageGrab
from win32api import GetSystemMetrics


def load_image_from_file(image_filename):
    img = Image.open(image_filename)
    img = np.array(img)
    img = img[:, :, ::-1].copy()
    return img


def get_screen_area_as_image(area=(0, 0, GetSystemMetrics(0), GetSystemMetrics(1))):
    screen_width = GetSystemMetrics(0)
    screen_height = GetSystemMetrics(1)

    # h, w = image.shape[:-1]  # height and width of searched image

    x1 = min(int(area[0]), screen_width)
    y1 = min(int(area[1]), screen_height)
    x2 = min(int(area[2]), screen_width)
    y2 = min(int(area[3]), screen_height)

    search_area = (x1, y1, x2, y2)

    img_rgb = ImageGrab.grab().crop(search_area).convert("RGB")
    img_rgb = np.array(img_rgb)  # convert to cv2 readable format (and to BGR)
    img_rgb = img_rgb[:, :, ::-1].copy()  # convert back to RGB

    return img_rgb


def search_image_in_image(small_image, large_image, precision=0.95):
    template = small_image.astype(np.float32)
    img_rgb = large_image.astype(np.float32)

    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = precision
    loc = np.where(res >= threshold)

    found_positions = list(zip(*loc[::-1]))

    # print("FOUND: {}".format(found_positions))
    return found_positions
