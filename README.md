BTW I no longer code in Python. C++ FOREVER!

# Portraiterator
Python OpenCV program that creates a mosaic image using many other images.

For every 25x25 square in the original image, this program will replace it with the closest image in the loaded set of images. The original image's width and height must be divisible by 25px or it won't work.

# Usage
First, you must have Python and install the required libraries for this program.
```
$ pip install -r requirements.txt
```
You will need to specify the directories for the images it will be using and the output image.

Example:
```
$ python portraiterator.py
Original image: originalimg.png
Directory containing images for portrait: inputimages/
Output image file: outputimg.png
```
