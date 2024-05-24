import re
import prepare_image
import pytesseract
from PIL import Image
import os

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

ocr_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
ocr_config_i = r'--oem 3 --psm 6 -c tessedit_char_whitelist=1IT'
ocr_config_d = r'--oem 3 --psm 6 outputbase digits'


def ocr_char(image, X1, Y1, X2, Y2, config, scale=1, show=False):
    L = ""
    p = 10
    image_c = image.crop(
        (int(X1), int(Y1), int(X2), int(Y2)))

    new_width = int(image_c.width*scale)
    new_height = int(image_c.height)

    image_c.resize((new_width, new_height))
    img = Image.new("L", (new_width+p, new_height+p), (255))
    img.paste(image_c, (int(p/2), int(p/2)))
    if show:
        img.show()
    L2 = pytesseract.image_to_string(
        img, config=config)
    # print(L2)
    n = re.findall(r'\d+', L2)
    if len(n) != 0:
        L = n[0]
    return L


def split_by_y_difference(array, threshold):
    sorted_array = sorted(array, key=lambda x: x[5])  # Sorting by Y-coordinate
    groups = []  # Resultant list of groups

    # Starting with the first element in the sorted array
    current_group = [sorted_array[0]]

    for i in range(1, len(sorted_array)):
        # Checking the difference between the current element and the last element in the current group
        y_difference = abs(sorted_array[i][2] - current_group[-1][2])

        # If the difference is less than or equal to the threshold, add the element to the current group
        if y_difference <= threshold:
            current_group.append(sorted_array[i])
        else:
            # Otherwise, finish the current group and start a new one
            groups.append(current_group)
            current_group = [sorted_array[i]]

    # Adding the last group
    groups.append(current_group)

    return groups


def code2text(image_path):
    images, keys = prepare_image.prepare_image(image_path)
    image = prepare_image.resize_and_concatenate(
        images, keys, target_size=(30, 30), borders=(16, 10))

    text = pytesseract.image_to_boxes(image, config=ocr_config)
    # print(text)
    data = []
    results = []
    indexes = []
    t_index = 0

    for line in text.split("\n"):
        if line != "":
            # print(line)
            [L, X1, Y1, X2, Y2, _] = line.split(" ")
            data.append([L, int(X1), int(Y1), int(X2), int(Y2), int(_)])
    codes = split_by_y_difference(data, 4)

    # for i, el in enumerate(data):
    #     [L, X1, Y1, X2, Y2, _] = el
    #     c_index = 0
    #     new = True
    #     for index in indexes:
    #         if not abs(index - int(Y1)) > 4 and Y1 in indexes:
    #             new = False
    #     if new:
    #         indexes.append(int(Y1))
    #         c_index += 1
    #         t_index +=1;
    #     data[i][5] = c_index

    # for n in range(t_index):
    #     results.append('')
    i = 0
    for data in codes:
        results.append("")
        for el in data:
            [L, X1, Y1, X2, Y2, I] = el

            if L == "O":
                L = ocr_char(image, X1, Y1, X2, Y2, ocr_config_d)
                if L == "":
                    L = "O"
            if L == "S":
                L = ocr_char(image, X1, Y1, X2, Y2, ocr_config_d)
                if L == "":
                    L = "S"
            if L == '1' or L == 'I':
                L = ocr_char(image, X1, Y1, X2, Y2, ocr_config, 1)
                if L == '':
                    L = 'I'
                if L == '4':
                    L = '1'

            results[i] += L
        i += 1
    return results


if __name__ == "__main__":
    # DIR = 'images/jpeg/'
    # for img in os.listdir(DIR):
    #     path = DIR+img
    #     print(path)
    #     Image.open(path).show()
    #     print(code2text(path))
    #     input()

    path = 'images/jpeg/photo_2024-04-16_18-49-58.jpg'
    print(code2text(path))
