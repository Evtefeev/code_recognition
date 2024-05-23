import cv2
from PIL import Image
import os

import numpy

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


def filter(cv2_image):
    # gray = get_grayscale(cv2_image)
    thresh = thresholding(cv2_image)
    return thresh

def prepare_image(input_path):
    image = cv2.imread(input_path)

    # Convert back to RGB
    image = cv2.fastNlMeansDenoisingColored(image,None,10,10,7,21)

    # Preprocess the image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(
        gray_image, 128, 255, cv2.THRESH_BINARY_INV)


    # Find contours
    contours, _ = cv2.findContours(
        binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    images = {}
    keys = []

    # Extract and save letters
    for n, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        letter = image[y:y+h, x:x+w]
        images[x] = letter
        keys.append(x)
    return images, keys


def resize_and_concatenate(images, keys, target_size=(100, 100), borders=(10, 10)):
    resized_images = {}

    # Resize images to the target size
    for key in keys:
        img = images[key]
        # color_coverted = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
        img = Image.fromarray(img) 
        img = add_borders(img, borders)
        img_resized = img.resize(target_size)
        resized_images[key] = img_resized

    # Get the total width for the concatenated image
    total_width = sum([img.width for img in resized_images.values()])

    # Create a blank image with the total width
    concat_image = Image.new('L', (total_width, target_size[1]))

    # Paste resized images side by side
    current_width = 0
    for img in sorted(resized_images.keys()):
        concat_image.paste(resized_images[img], (current_width, 0))
        current_width += resized_images[img].width

    open_cv_image = numpy.array(concat_image)
    image = filter(open_cv_image)
    image = Image.fromarray(image) 


    image.save("res.png")
    return image

def resize(images, keys, target_size=(100, 100), borders=(10, 10)):
    resized_images = {}

    # Resize images to the target size
    for key in keys:
        img = images[key]
        # color_coverted = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
        img = Image.fromarray(img) 
        img = add_borders(img, borders)
        img_resized = img.resize(target_size)
        resized_images[key] = img_resized

    res_images = []
    for img in sorted(resized_images.keys()):
         # Create a blank image with the total width
        concat_image = Image.new('L', (target_size[0]+borders[0], target_size[1]+borders[1]))
        concat_image.paste(resized_images[img], (int(borders[0]/2), int(borders[1]/2)))
        open_cv_image = numpy.array(concat_image)
        image = filter(open_cv_image)
        image = Image.fromarray(image) 
        res_images.append(image)
        image.save("res.png")
        


    return res_images

def add_borders(image, borders=(100, 100)):
    old_size = image.size
    new_size = (old_size[0]+borders[0], old_size[1]+borders[1])
    # luckily, this is already black!
    new_im = Image.new("RGB", new_size, color=(255, 255, 255))
    box = tuple((n - o) // 2 for n, o in zip(new_size, old_size))
    new_im.paste(image, box)
    return new_im
