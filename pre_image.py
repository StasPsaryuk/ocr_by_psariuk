# --*-- coding=utf-8 --*--
# Імпорт модулів необхідних для попередньої обробки фото
from PIL import Image, ImageFilter, ImageChops
import cv2

# Функція фільтрації зображення з використанням модулів бібліотеки СV
def get_image(filename:str):
    image = cv2.imread(filename)
    gray = cv2.threshold(image,127,255,cv2.THRESH_TOZERO)[1]
    filename = "{}.jpg".format('123')
    cv2.imwrite('tmp/'+filename, gray)
    tmp_image = Image.open('tmp/'+filename)
    tmp_image = tmp_image.crop(tmp_image.getbbox())
    tmp_image.save('tmp/321.png')
    return tmp_image
