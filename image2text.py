# import the necessary packages
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
import sys
import pytesseract
import urllib
import json as m_json
import cv2
import clipboard
import pyperclip
import webbrowser
from googletrans import Translator
from pyimagesearch.transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils
import os
def capture_image():
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("test")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        if k%256 == 32:
            # SPACE pressed
            cv2.imwrite("image.png", frame)
            break
    cam.release()
    cv2.destroyAllWindows()
    select_image()

def change_dropdown(*args):
    global language
    language=tkvar.get()

def texttranslat():
    translator = Translator()
    root = Tk()
    config = ('-l '+str(language)+' --oem 1 --psm 3')
    itext = pytesseract.image_to_string(warped, config=config)
    translated = translator.translate(itext)
    lbl = Label(root, text=translated , cursor="hand2")
    lbl.pack(side="bottom", fill="both")

def callback(event):
    webbrowser.open_new(event.widget.cget("text"))

def googlesearch():
    root = Tk()
    config = ('-l '+str(language)+' --oem 1 --psm 3')
    itext = pytesseract.image_to_string(warped, config=config)
    try:
        from googlesearch import search
    except ImportError:
        print("No module named 'google' found")
    for j in search(itext, tld="co.in", num=10, stop=10, pause=2):
        lbl = Label(root, text=str(j), fg="blue", cursor="hand2")
        lbl.pack(side="bottom", fill="both")
        lbl.bind("<Button-1>", callback)

def copy():
    config = ('-l '+str(language)+' --oem 1 --psm 3')
    itext = pytesseract.image_to_string(warped, config=config)
    text=str(itext)
    clipboard.copy(text)
    print("Copied to clipboard!!")

def select_image():
	global panelA, panelB ,im ,warped ,itext ,path
	path = filedialog.askopenfilename()
	print(path)
	if len(path) > 0:
		mainimage = cv2.imread(path)
		mainimage= cv2.copyMakeBorder(mainimage,10,10,10,10,cv2.BORDER_CONSTANT)
		ratio = mainimage.shape[0] / 500.0
		orig = mainimage.copy()
		mainimage = imutils.resize(mainimage, height = 500)

		# convert the mainimage to grayscale, blur it, and find edges
		# in the mainimage
		gray = cv2.cvtColor(mainimage, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (5, 5), 0)
		edged = cv2.Canny(gray, 75, 200)


		# find the contours in the edged mainimage, keeping only the
		# largest ones, and initialize the screen contour
		cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

		# loop over the contours
		for c in cnts:
			# approximate the contour
			peri = cv2.arcLength(c, True)
			approx = cv2.approxPolyDP(c, 0.02 * peri, True)

			# if our approximated contour has four points, then we
			# can assume that we have found our screen
			if len(approx) == 4:
				screenCnt = approx
				break

		# show the contour (outline) of the piece of paper

		# apply the four point transform to obtain a top-down
		# view of the original mainimage
		warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
		# convert the warped image to grayscale, then threshold it
		# to give it that 'black and white' paper effect
		warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

		mainimage = cv2.resize(mainimage, (500,800))
		mainimage = Image.fromarray(mainimage)
		mainimage = ImageTk.PhotoImage(mainimage)
		config = ('-l '+str(language)+' --oem 1 --psm 3')
		itext = pytesseract.image_to_string(warped, config=config)

		if panelA is None or panelB is None:
			panelA = Label(image=mainimage)
			panelA.image = mainimage
			panelA.pack(side="left", padx=10, pady=10)


			panelB = Label(justify=LEFT,text=itext)
			panelB.text = itext
			panelB.pack(side="right", padx=10, pady=10)

root = Tk()
mainframe = Frame(root)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(side="top", fill="both")
tkvar = StringVar(root)
choices = { 'eng','hin','fra','ara','ita','rus'}
tkvar.set('language')
popupMenu = OptionMenu(mainframe, tkvar, *choices)
popupMenu.grid(row = 2, column =1)
tkvar.trace('w', change_dropdown)
panelA = None
panelB = None
btn = Button(root, text="Select an image", command=select_image)
btn.pack(side="bottom", fill="both")
btn = Button(root, text="Copy to clipboard", command=copy)
btn.pack(side="bottom", fill="both")
btn = Button(root, text="Translate", command=texttranslat)
btn.pack(side="bottom", fill="both")
btn = Button(root, text="Detailed search", command=googlesearch)
btn.pack(side="bottom", fill="both")
btn = Button(root, text="capture an image", command=capture_image)
btn.pack(side="bottom", fill="both")
root.mainloop()
