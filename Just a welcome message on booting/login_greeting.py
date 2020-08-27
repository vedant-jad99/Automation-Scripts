from tkinter import *
from tkinter import font
from datetime import datetime as dt
from PIL import Image, ImageTk

if __name__ == "__main__":
    string = ""
    time_str = str(dt.now().time())[:8]
    if time_str < "17:00:00":
        string = "Welcome back Vedant! Have a pleasant day!"
    else:
        string = "Welcome back Vedant! Hope you are having a good day!"

    window = Tk()
    frame2 = Frame(window, padx=10, pady=10)
    text = Label(frame2, text=string, padx=10, pady=10, font=font.Font(size=13), foreground="blue")
    frame1 = Frame(window, padx=10, pady=10)
    close = Button(frame2, text="Close", width=10, padx=10, pady=10, relief=RAISED, borderwidth=5, command=window.destroy)
    image = Image.open('/home/thedarkcoder/Desktop/Projects/Basic_study_prompt_generator/welcome_back.png')
    size_tuple = (image.size[0]//2, image.size[1]//2)
    image = image.resize(size_tuple)
    gif = ImageTk.PhotoImage(image)
    gif_label = Label(frame1, image=gif, padx=10, pady=10)
    gif_label.image = gif

    text.grid(row=0, column=0)
    close.grid(row=0, column=1)
    gif_label.pack()
    frame2.grid(row=1, column=0)
    frame1.grid(row=0, column=0)

    window.update()
    width = window.winfo_width()
    height = window.winfo_height()
    x_ = (window.winfo_screenwidth() - width)//2
    y_ = (window.winfo_screenheight() - height)//2
    window.geometry("%dx%d+%d+%d" % (width, height, x_, y_))
    window.mainloop()