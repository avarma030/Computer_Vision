#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2 #OpenCV for image processing
import easygui #Opens filebox
import numpy as np
import imageio #Reads image stored at a particular path
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image


# In[2]:


top=tk.Tk()
top.geometry('400x400')
top.title('Cartoonification')
top.configure(background='black')
label=Label(top,background='#CDCDCD', font=('calibri',20,'bold'))


# In[3]:


def upload():
    ImagePath=easygui.fileopenbox()
    cartoonify(ImagePath)


# In[4]:


def cartoonify(ImagePath):
    
    # read the image
    original_img = cv2.imread(ImagePath)
    original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
    #print(image)

    # confirm if image is loaded or not
    if original_img is None:
        print("No image found.\n Choose appropriate file")
        sys.exit()

    rs1 = cv2.resize(original_img, (960, 540))
    #plt.imshow(rs1, cmap='gray')
    
    #grayscale conversion
    grayScaleImage= cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    rs2 = cv2.resize(grayScaleImage, (960, 540))
    #plt.imshow(rs2, cmap='gray')
    
    #image smoothening by applying median blur
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    rs3 = cv2.resize(smoothGrayScale, (960, 540))
    #plt.imshow(rs3, cmap='gray')

    #retrieving the edges by using thresholding technique
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 9, 9)

    rs4 = cv2.resize(getEdge, (960, 540))
    #plt.imshow(rs4, cmap='gray')

    #removing noise and keeping edge sharp usingvbilateral filter 
    colorImage = cv2.bilateralFilter(original_img, 9, 300, 300)
    rs5 = cv2.resize(colorImage, (960, 540))
    #plt.imshow(rs5, cmap='gray')


    #masking edge image with cartoonified image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
    rs6 = cv2.resize(cartoonImage, (960, 540))
    #plt.imshow(rs6, cmap='gray')

    # Plot the entire process
    images=[rs1, rs2, rs3, rs4, rs5, rs6]

    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    save1=Button(top,text="Save Image",command=lambda: save(rs6, ImagePath),padx=30,pady=5)
    save1.configure(background='white', foreground='black',font=('calibri',10,'bold'))
    save1.pack(side=TOP,pady=50)
    
    plt.show()


# In[5]:


def save(ReSized6, ImagePath):
    
    #imwrite() is used to save an image
    newName="cartoonified_Image"
    path1 = os.path.dirname(ImagePath)
    extension=os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(ReSized6, cv2.COLOR_RGB2BGR))
    I= "Image saved by name " + newName +" at "+ path
    tk.messagebox.showinfo(title=None, message=I)


# In[6]:


upload=Button(top,text="Select an Image",command=upload,padx=10,pady=5)
upload.configure(background='white', foreground='black',font=('calibri',10,'bold'))
upload.pack(side=TOP,pady=50)

top.mainloop()


# In[ ]:




