#!/opt/homebrew/bin/python3
import os
import PIL.Image
from Crypto.Cipher import AES

import argparse
from tkinter import *
from tkinter import ttk
from enum import Enum
from enum import IntEnum


class Stenographer():
    """
    Hiding Data LSB
    Each pixel contains a total of 3 bytes of information, from 1 byte r, g, b.
    1 byte consists of 8 bits and at least 3 pixels are required to store hiding data.

    First 1 byte(3 pixel) is signature
    After 1 byte(3 pixel) is settings
    After 2 byte(6 pixel) is length (3 * length = byte size)

    HEADER SIZE is include SIGNATURE and SIZE
    - SIGNATURE informs us that there is data hidden in the photo.
    - DATATYPE  text, binary, base64, image
    - SIZE tells us how many bytes of data there are.

    SIGNATURE   0xAA    1 Byte
    SETTINGS    0xFF    1 Byte
    SIZE        0xFFFF  2 Byte
    """

    HEADER_SIZE = 4
    SIGNATURE_SIZE = 1
    SETTINGS_SIZE = 1
    SIGNATURE = 0b10101010

    class DataType(IntEnum):
        NONE = 0,
        TEXT = 1,
        BINARY = 2,
        BASE64 = 3,
        IMAGE = 4

    class Settings():
        def __init__(self):
            self.dataType = Stenographer.DataType.BINARY

    def encrypt(data: str, secretkey: str) -> str:
        pass
        # cipher = AES.new(secretkey, AES.MODE_CBC, iv)

    def lsbEncode(self, image_path: str,  data: bytes, settings: Settings):
        new_image_path = "new_{}".format(image_path)
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

        # write signature top of byte array
        # write settings top of byte array
        data = self.SIGNATURE.to_bytes() + bytes(settings.dataType) + data

        print("SIGNATURE: {0} : 0X{0:02X}".format(self.SIGNATURE))
        print(bytes(self.SIGNATURE))
        print(bytes(settings.dataType.value))
        print(data)

        if len(data) > total_size:
            raise ValueError("Message is too long to be encoded in the image")

        data_idx = 0
        data_bit_idx = 0
        pixel_counter = 0
        active_idx = 0
        debugging = False

        for y in range(height):
            for x in range(width):
                if data_idx == len(data):
                    # encoding ended
                    break

                if debugging:
                    active_idx += 1
                    if active_idx < 5:
                        print("idx {0} putpixel in x:{1} y:{2}".format(active_idx, x, y))
                        im.putpixel((x, y), (0xAA, 0xAA, 0xAA))
                        continue
                    break

                # every 3 pixel is 1 byte
                # get current pixel r,g,b color and clear lsb
                r, g, b = pixels[x, y]
                r = r ^ (r & 1)
                g = g ^ (g & 1)
                b = b ^ (b & 1)

                data_bit_idx += 1
                b1 = (data[data_idx] >> data_bit_idx) & 1

                data_bit_idx += 1
                b2 = (data[data_idx] >> data_bit_idx) & 1
                r |= b1
                g |= b2

                pixel_counter += 1
                if pixel_counter < 3:
                    data_bit_idx += 1
                    b3 = (data[data_idx] >> data_bit_idx) & 1
                    b |= b3

                # set encoded color
                encoded_rgb = (r, g, b)
                im.putpixel((x, y), encoded_rgb)

                # reset idx
                # and increment data pointer
                if pixel_counter == 3:
                    pixel_counter = 0
                    data_bit_idx = 0
                    data_idx += 1

        # save as with new name
        im.save(os.path.basename(new_image_path))

    def lsbDecode(self, image_path: str):
        print("not implemented")


class Gui(Tk):
    PADX = 5
    PADY = 5
    STR_TITLE = "Stenographer"
    FOLDER_ICON_24_BYTES = b'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAQAAABKfvVzAAAAVElEQVQ4y2NgGCbgv/v/x/+RQT0hDff/owP8Wv7//f8fiRf+//d/TPD4vwcODTi1PMKpAasr/iOpoYOGfyNRw3+aa3j0nxiAlDQ80JL3fwKJb4gDAP09+NbCRr6DAAAAAElFTkSuQmCC'

    class InputType(IntEnum):
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
        ttk.Radiobutton(f, text="Encode String", variable=self.inputType, value=self.InputType.TEXT.value).pack(side=LEFT, fill="both")
        self.sourceEntry = ttk.Entry(f)
        self.sourceEntry.pack(side=LEFT, expand=True, fill=X)

        f = Frame(settingsFrame)
        f.pack(fill=BOTH)
        ttk.Radiobutton(f, text="Encode File", variable=self.inputType, value=self.InputType.FILE.value).pack(side=LEFT, fill="both")
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
        if self.inputType.get() == self.InputType.TEXT:
            message = self.sourceEntry.get()
            binary_message = bytes(message, "utf-8")
            settings = Stenographer.Settings()
            settings.dataType = Stenographer.DataType.TEXT
            sten = Stenographer()
            sten.lsbEncode(self.imagePath.get(), binary_message, settings)
            self.statusvar.set("Encoded!")
        else:
            self.statusvar.set("Unimplemented")
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
