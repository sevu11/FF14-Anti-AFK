from PIL import Image, ImageTk

def resize_image(filename, width, height):
    img = Image.open(filename)
    img = img.resize((width, height), resample=Image.BILINEAR)
    return ImageTk.PhotoImage(img)