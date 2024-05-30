import logging
import os
import subprocess
import time
import warnings

import cv2
import numpy as np
import pyautogui
import pytesseract

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Установить уровень логирования TensorFlow на 3, чтобы скрыть все сообщения
import tensorflow as tf

from tests.dict_for_test import tabs

tf.get_logger().setLevel(logging.ERROR)  # Скрыть все сообщения из TensorFlow
warnings.filterwarnings("ignore")  # Скрыть все предупреждения из библиотеки Keras


class Screen:
    def __init__(self):
        logging.info("Откройте окно МФИ...")
        time.sleep(3)
        # Получите идентификатор активного окна с помощью xdotool
        self.active_window_id = int(subprocess.check_output(['xdotool', 'getactivewindow']).decode())

        # Получите информацию об активном окне с помощью xwininfo
        self.xwininfo_output = subprocess.check_output(['xwininfo', '-id', str(self.active_window_id)]).decode()

        self.name = self.xwininfo_output.splitlines()[1].strip()
        self.x = int(self.xwininfo_output.splitlines()[3].split(":")[1].strip())
        self.y = int(self.xwininfo_output.splitlines()[4].split(":")[1].strip())
        self.width = int(self.xwininfo_output.splitlines()[7].split(":")[1].strip())
        self.height = int(self.xwininfo_output.splitlines()[8].split(":")[1].strip())

        self.path_to_png = 'temp/application_screenshot'

        self.digits = [0] * 11
        for i in range(10):
            digit = cv2.imread(f"temp/reference/{i}.png", cv2.IMREAD_GRAYSCALE)
            digit_resized = cv2.resize(digit, (64, 64))
            self.digits[i] = digit_resized

        digit = cv2.imread(f"temp/reference/plus.png", cv2.IMREAD_GRAYSCALE)
        digit_resized = cv2.resize(digit, (64, 64))
        self.digits[10] = digit_resized

        self.tab = 1

    def screen(self, path: str | None = None):
        # Сделайте скриншот только для определенного окна
        screenshot = pyautogui.screenshot(region=(self.x, self.y, self.width, self.height))
        if path is None:
            # Сохраните скриншот в файл
            screenshot.save(f"{self.path_to_png}.png")
        else:
            screenshot.save(f"{path}")

    def get_pixel_color(self, x, y):
        # Откройте изображение
        image = cv2.imread(f"{self.path_to_png}.png")

        pixel_color = image[y, x]

        # Выведите RGB значения цвета
        return pixel_color[::-1]

    def img_to_digit(self, img):
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        image_to_compare = cv2.resize(gray_image, (64, 64))

        # Сравнение изображения с каждым эталонным изображением
        best_match = None
        min_diff = float('inf')

        for i, digit in enumerate(self.digits):
            result = cv2.matchTemplate(image_to_compare, digit, cv2.TM_SQDIFF_NORMED)
            min_val, _, _, _ = cv2.minMaxLoc(result)

            if min_val < min_diff:
                best_match = i
                min_diff = min_val

        if best_match == 10:
            return ""

        return str(best_match)

    def img_to_text(self, x1, x2, y1, y2, dig, colour="w", path=None):

        if path is None:
            image = cv2.imread(f"{self.path_to_png}.png")
        else:
            image = cv2.imread(path)

        image = image[y1:y2, x1:x2]

        # Преобразование изображения в черно-белое
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        if colour != "w":
            gray_image = cv2.bitwise_not(gray_image)

        # # Применение порогового фильтра
        _, binary_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY)

        # Изменение размера изображения
        resized_image = cv2.resize(binary_image, None, fx=10, fy=10, interpolation=cv2.INTER_CUBIC)

        inverted_image = cv2.bitwise_not(resized_image)

        _, binary_image = cv2.threshold(inverted_image, 127, 255, cv2.THRESH_BINARY)
        inverted_binary_image = cv2.bitwise_not(binary_image)
        rgb_image = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2RGB)


        height, width = gray_image.shape
        if len(str(dig)) != 1:
            # Распознавание текста с помощью Tesseract
            custom_config = r'--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789.'
            text = pytesseract.image_to_string(rgb_image, config=custom_config, lang='eng').strip()
            if text and abs(float(text) - float(dig)) < 0.01:
                return text

        # Нахождение контуров на изображении
        contours, _ = cv2.findContours(inverted_binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Сортировка контуров по координате x
        contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[0])
        # Получение координат боксов для каждого контура
        string_number = ""
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            # Выделение области изображения, соответствующей контуру
            contour_region = binary_image[y:y + h, x:x + w]
            # Подсчет количества белых и черных пикселей внутри контура
            white_pixels = np.sum(contour_region == 255)
            black_pixels = np.sum(contour_region == 0)

            if h > height / 1.5 and w > width / 6 and white_pixels > black_pixels:
                string_number += self.img_to_digit(rgb_image[y:y + h, x:x + w])
        return string_number

    def get_coordinates(self, path=None):
        def click_event(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                print(self.get_pixel_color(x, y))
                return x, y

        if path is None:
            image = cv2.imread(f"{self.path_to_png}.png")
        else:
            image = cv2.imread(path)

        cv2.imshow('Image', image)
        cv2.setMouseCallback('Image', click_event)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def change_tab(self, number):
        x = tabs[number][0]
        y = tabs[number][1]
        pyautogui.click(x + self.x, y + self.y, clicks=100, interval=0.01)
        self.tab = number
