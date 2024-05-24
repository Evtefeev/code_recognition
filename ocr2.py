from PIL import Image
import pytesseract
import cv2
import re

# Загрузите и обработайте изображение
image = cv2.imread('IMG_2368.jpg', cv2.IMREAD_GRAYSCALE)
_, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Сохраните предварительно обработанное изображение (по желанию)
cv2.imwrite('processed_image.png', binary_image)

# Распознайте текст с предварительно обработанного изображения
processed_image = Image.fromarray(binary_image)
custom_config = r'--oem 3 --psm 6 outputbase digits'
text = pytesseract.image_to_string(processed_image, config=custom_config)

# Используйте регулярное выражение для извлечения чисел
# numbers = re.findall(r'\d+', text)

print(text)
