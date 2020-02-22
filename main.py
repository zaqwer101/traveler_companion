import os
import time
import numpy
from PIL import Image
import pytesseract
import cv2

import pyscreenshot
start = (187, 273)
end = (499, 308)
image_size = (end[0] - start[0], end[1] - start[1])
scale = 4
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

for file in os.listdir("."):
    if file.split('.').__contains__("jpg"):
        os.remove(file)
iteration = 0

time.sleep(5)
while True:
    iteration += 1
    screenshot = pyscreenshot.grab(
        bbox=(187, 273, 499, 308), backend='pil'
    )
    screenshot = screenshot.resize(size=(image_size[0] * scale, image_size[1] * scale))

    cv_image = numpy.array(screenshot)
    cv_image = cv_image[:, :, ::-1].copy()
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(cv_image, (5, 5), 0)
    _, cv_image = cv2.threshold(cv_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    image = Image.fromarray(cv_image)

    # раскомментировать для сохранения дебажных изображений
    # image.save("image"+str(iteration) + ".jpg")

    try:
        coordinates = pytesseract.image_to_string(image, lang="rus")
        print(coordinates)
        coordinates = coordinates.split(",")
        print(coordinates)
    except:
        print("Something went wrong")
        time.sleep(1)
