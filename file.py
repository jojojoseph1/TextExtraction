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

def change_dropdown(*args):
    global language
    language=tkvar.get()
    print(language)
    print( tkvar.get() )

def texttranslat():
    translator = Translator()
    root = Tk()
    config = ('-l '+str(language)+' --oem 1 --psm 3')
    itext = pytesseract.image_to_string(im, config=config)
    translated = translator.translate(itext)
    lbl = Label(root, text=translated , cursor="hand2")
    lbl.pack(side="bottom", fill="both")

def callback(event):
    webbrowser.open_new(event.widget.cget("text"))

def googlesearch():
    root = Tk()
    config = ('-l '+str(language)+' --oem 1 --psm 3')
    itext = pytesseract.image_to_string(im, config=config)
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
    itext = pytesseract.image_to_string(im, config=config)
    text=str(itext)
    clipboard.copy(text)
    print("Copied to clipboard!!")

def select_image():
	global panelA, panelB ,im
	path = filedialog.askopenfilename()
	if len(path) > 0:
		mainimage = cv2.imread(path)
		mainimage = cv2.cvtColor(mainimage, cv2.COLOR_BGR2RGB)
		im = cv2.cvtColor(mainimage, cv2.COLOR_BGR2RGB)
		im = cv2.cvtColor(mainimage, cv2.COLOR_BGR2RGB)
		mainimage = cv2.resize(mainimage, (500,800))
		mainimage = Image.fromarray(mainimage)
		mainimage = ImageTk.PhotoImage(mainimage)
		config = ('-l '+str(language)+' --oem 1 --psm 3')
		itext = pytesseract.image_to_string(im, config=config)

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
root.mainloop()
