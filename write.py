import re
import prepare_image
import pyautogui
import pytesseract
from PIL import Image
import os

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'


if __name__ == "__main__":

    images, keys = prepare_image.prepare_image('IMG_2369.jpg')
    # images_r = prepare_image.resize(images, keys, target_size=(100, 170), borders=(10, 10))
    image = prepare_image.resize_and_concatenate(
        images, keys, target_size=(100, 100), borders=(15, 10))
    custom_config = r'--oem 3 --psm 6'
    custom_config_d = r'--oem 3 --psm 6 outputbase digits'
    text = pytesseract.image_to_boxes(image, config=custom_config)
    result = ""
    for line in text.split("\n"):
        if line != "":
        
            [L, X1, Y1, X2, Y2, _] = line.split(" ")
            if L == "O":
                
                w, h = image.size
                p = 10
                image_c = image.crop((int(X1)-p, int(Y1)-p, int(X2)+p, int(Y2)+p))
                
                L = pytesseract.image_to_string(image_c, config=custom_config_d)
                L = re.findall(r'\d+', L)[0]
            result += L
    print(result)

