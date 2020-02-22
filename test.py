import os
import time
import numpy
from PIL import Image, ImageChops, ImageOps
import pytesseract
import cv2

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

image = Image.open('sample.png')
scale = 1
start = (187, 270)
end = (499, 310)
image_size = (end[0] - start[0], end[1] - start[1])
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image = image.crop((start[0], start[1], end[0], end[1]))
image = image.resize(size=(image_size[0] * scale, image_size[1] * scale))
print(image.info)
cv_image = numpy.array(image)
cv_image = cv_image[:, :, ::-1].copy()
cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
# blur = cv2.GaussianBlur(cv_image, (5, 5), 0)
_, cv_image = cv2.threshold(cv_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
image = Image.fromarray(cv_image)

pixels = numpy.asarray(image)

image = ImageOps.invert(image)
# image = trim(image)

print(pytesseract.image_to_string(image))
image.show()
