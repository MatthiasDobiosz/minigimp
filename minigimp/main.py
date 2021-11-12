import sys
import tkinter

import PIL.Image
import PIL.ImageTk
from PIL.ImageOps import scale, posterize, grayscale, invert, pad, crop
import argparse

from tkinter import *

# i = PIL.Image.open(sys.argv[1])
# parser = argparse.ArgumentParser(description="Process image")
# parser.add_argument('-i', "--image",required=True, help="path to image file")
# args = vars(parser.parse_args())
# i = PIL.Image.open(args["image"])
i = PIL.Image.open("googly_kugel_64x64.png")


blurkernel = [[1, 1, 1],
              [1, 1, 1],
              [1, 1, 1]]


def is_grey_scale(imgtocheck):
    imgtocheck = imgtocheck.convert('RGB')
    w, h = imgtocheck.size
    for i in range(w):
        for j in range(h):
            r, g, b = imgtocheck.getpixel((i, j))
            if r != g != b:
                return False
    return True


isGrey = is_grey_scale(i)


def applyBlurGrey(kernel, image):
    w, h = image.size
    div = sum(kernel[0]) + sum(kernel[1]) + sum(kernel[2])
    img1 = image.copy()
    for x in range(1, w - 1):
        for y in range(1, h - 1):
            new_val = 0
            for z in range(3):
                for j in range(3):
                    print(image.getpixel((x - 1 + z, y - 1 + j)))
                    new_val += int(image.getpixel((x - 1 + z, y - 1 + j)) * kernel[z][j] / (div + 0.1))
            img1.putpixel((x, y), new_val)
    return crop(img1, 1)


def applyBlurColor(kernel, image):
    w, h = image.size
    div = sum(kernel[0]) + sum(kernel[1]) + sum(kernel[2])
    img1 = image.copy()
    for x in range(1, w - 1):
        for y in range(1, h - 1):
            new_val = 0
            new_val1 = 0
            new_val2 = 0
            new_val3 = 0
            for z in range(3):
                for j in range(3):
                    new_val += int(image.getpixel((x - 1 + z, y - 1 + j))[0] * kernel[z][j] / (div + 0.1))
                    new_val1 += int(image.getpixel((x - 1 + z, y - 1 + j))[1] * kernel[z][j] / (div + 0.1))
                    new_val2 += int(image.getpixel((x - 1 + z, y - 1 + j))[2] * kernel[z][j] / (div + 0.1))
                    new_val3 += int(image.getpixel((x - 1 + z, y - 1 + j))[3] * kernel[z][j] / (div + 0.1))
            img1.putpixel((x, y), (new_val, new_val1, new_val, new_val3))
    return crop(img1, 1)


def blurButtonListener():
    if is_grey_scale(i):
        blurimg = applyBlurGrey(blurkernel, i)
        img2 = PIL.ImageTk.PhotoImage(blurimg)
        labelimage.configure(image=img2)
        labelimage.image = img2
    else:
        blurimg = applyBlurColor(blurkernel, i)
        img2 = PIL.ImageTk.PhotoImage(blurimg)
        labelimage.configure(image=img2)
        labelimage.image = img2


root = Tk()
root.title("try")
root.geometry("900x600")

img = PIL.ImageTk.PhotoImage(i)
labelimage = Label(root, image=img)

btn1 = tkinter.Button(root, text="BlurButton", command=blurButtonListener)
btn1.grid(column=0, row=0)

btn2 = tkinter.Button(root, text="BlurButton")
btn2.grid(column=0, row=1)

btn3 = tkinter.Button(root, text="BlurButton", width=10, height=2)
btn3.grid(column=0, row=2)
labelimage.grid(column=1, row=1)

root.mainloop()
