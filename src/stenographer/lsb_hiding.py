#!/opt/homebrew/bin/python3
# from PIL import Image
import PIL.Image

import argparse
from tkinter import *
from tkinter import ttk
from enum import Enum


class Stenographer():
    """
    Hiding Data LSB
    Each pixel contains a total of 3 bytes of information, from 1 byte r, g, b.
    1 byte consists of 8 bits and at least 3 pixels are required to store hiding data.

    First 2 byte(6 pixel) is signature
    After 2 byte(6 pixel) is length (3 * length = byte size)

    HEADER SIZE is include SIGNATURE and SIZE
    - SIGNATURE informs us that there is data hidden in the photo.
    - SIZE tells us how many bytes of data there are.

    SIGNATURE   0xAAAA  2 Byte
    SIZE        0x0000  2 Byte
    """

    HEADER_SIZE = 4
    SIGNATURE = 0b1010101010101010

    def lsbEncode(self, image_path: str,  data: bytes):
        new_image_path = "new_{}".format(image_path)
        # im = Image.open(image_path)
        fp = open(image_path, "rb")
        im = PIL.Image.open(fp)
        pixels = im.load()
        width, height = im.size
        total_size = width * height
        available_hiding_data_size = total_size / 3 - self.HEADER_SIZE

        print("Image size (Width,Heigth): {}".format(im.size))
        print("Total Pixel : {} ".format(total_size))
        print("Available Hiding Byte  Size : {} ".format(available_hiding_data_size))
        print("Available Hiding KByte Size : {} ".format(available_hiding_data_size // 1024))

        if len(data) > total_size:
            raise ValueError("Message is too long to be encoded in the image")

        data_idx = 0
        for x in range(width):
            for y in range(height):
                cpixel = pixels[x, y]
                r, g, b = cpixel
                encoded_rgb = (r, g, b)

                lsb = []
                lsb.append(r & 1)
                lsb.append(g & 1)
                lsb.append(b & 1)
                print(lsb)

        print("hiding data...")

    def lsbDecode(self, image_path: str):
        print("not implemented")


class Gui(Tk):
    PADX = 5
    PADY = 5
    STR_TITLE = "Stenographer"
    FOLDER_ICON_24_BYTES = b'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAQAAABKfvVzAAAAVElEQVQ4y2NgGCbgv/v/x/+RQT0hDff/owP8Wv7//f8fiRf+//d/TPD4vwcODTi1PMKpAasr/iOpoYOGfyNRw3+aa3j0nxiAlDQ80JL3fwKJb4gDAP09+NbCRr6DAAAAAElFTkSuQmCC'

    class InputType(Enum):
        TEXT = 1,
        FILE = 2

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.title(self.STR_TITLE)
        self.geometry("640x480")
        self.resizable(True, True)

        # style
        # self.style = ttk.Style(self)
        # self.style.theme_use("aqua")
        # self.style.configure('TFrame', background='blue', foreground='red', relief='sunken')

        # load icons
        self.FOLDER_ICON_24 = PhotoImage(data=self.FOLDER_ICON_24_BYTES)

        # varaibles
        self.statusvar = StringVar(self)
        self.imagePath = StringVar(self)
        self.sourcestr = StringVar(self)
        self.inputType = IntVar(self)
        self.encryptVar = BooleanVar(self)

        mainFrame = ttk.Frame(self)
        mainFrame.pack(side=TOP, fill="both", padx=self.PADX, pady=self.PADY)

        imageFrame = ttk.LabelFrame(mainFrame, text="Source Image")
        imageFrame.pack(side=TOP, fill="both", padx=self.PADX, pady=self.PADY)
        ttk.Label(imageFrame, text="Image ").pack(side=LEFT)
        ttk.Entry(imageFrame).pack(expand=True, side=LEFT, fill="x")
        ttk.Button(imageFrame, image=self.FOLDER_ICON_24).pack(side=RIGHT)

        # settings frame
        settingsFrame = ttk.LabelFrame(mainFrame, text="Encode Settings")
        settingsFrame.pack(side=TOP, fill="both", padx=self.PADX, pady=self.PADY)

        f = Frame(settingsFrame)
        f.pack(fill=BOTH)
        ttk.Radiobutton(f, text="Encode String", variable=self.inputType, value=self.InputType.TEXT).pack(side=LEFT, fill="both")
        ttk.Entry(f).pack(side=LEFT, expand=True, fill=X)

        f = Frame(settingsFrame)
        f.pack(fill=BOTH)
        ttk.Radiobutton(f, text="Encode File", variable=self.inputType, value=self.InputType.FILE).pack(side=LEFT, fill="both")
        ttk.Entry(f).pack(side=LEFT, expand=True, fill=X)
        ttk.Button(f, image=self.FOLDER_ICON_24).pack(side=RIGHT)

        f = Frame(settingsFrame)
        f.pack(fill=BOTH)
        ttk.Checkbutton(f, text="Encrypt Data", variable=self.encryptVar).pack(side=TOP, fill="both")
        ttk.Label(f, text="Secret Key").pack(side=LEFT, fill="both")
        ttk.Entry(f).pack(side=LEFT, expand=True, fill=X)

        # output frame
        outputFrame = ttk.LabelFrame(mainFrame, text="Encode")
        outputFrame.pack(side=TOP, fill="both", padx=self.PADX, pady=self.PADY)
        ttk.Button(outputFrame, text="View", command=self.onViewBtnClick).pack()
        ttk.Button(outputFrame, text="Encode", command=self.onEncodeBtnClick).pack()

        statusBar = ttk.Frame(self)
        statusBar.pack(side=BOTTOM, fill=X, padx=self.PADX, pady=self.PADY)
        ttk.Label(statusBar, textvariable=self.statusvar, anchor="w").pack(side=BOTTOM, fill=X)

        self.statusvar.set("Ready")
        self.imagePath.set('../data/test.jpg')

    def onViewBtnClick(self):
        fp = open(self.imagePath.get(), "rb")
        im = PIL.Image.open(fp)
        im.show()

    def onEncodeBtnClick(self):
        if self.inputType == self.InputType.TEXT:
            message = "Hello World"
            binary_message = bytes(message, "utf-8")
            sten = Stenographer()
            sten.lsbEncode(self.imagePath.get(), binary_message)
        else:
            print("unimplemented")
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=Gui.STR_TITLE)
    parser.add_argument('--encode', help='Encoder')
    parser.add_argument('--decode', help='Encoder')
    parser.add_argument('--gui', action='store_true', help='Graphical User Interface')
    args = parser.parse_args()

    if args.gui:
        gui = Gui()
        gui.mainloop()
    else:
        pass
