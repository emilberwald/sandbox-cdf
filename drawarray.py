import argparse
import itertools
import pathlib
import tkinter as tk
from tkinter import filedialog

import numpy
import PIL.Image
import PIL.ImageDraw


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


class myGUI:
    def __init__(self, root, args):
        self.root = root

        self.canvas = tk.Canvas(self.root, borderwidth=1, relief="sunken", width=640, height=480, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.helpmenu = tk.Menu(self.menu)

        self.filemenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Open Min...", command=self.openmin)
        self.filemenu.add_command(label="Open Max...", command=self.openmax)
        self.filemenu.add_command(label="Save As...", command=self.save)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=root.destroy)

        self.image = PIL.Image.new("RGB", (args.width, args.height), (255, 255, 255))
        self.draw = PIL.ImageDraw.Draw(self.image)
        self.canvas.bind("<B1-Motion>", self.pen_down)
        self.canvas.bind("<ButtonRelease-1>", self.pen_up)
        self.latest = None
        self.args = args

    def openmin(self):
        if (
            file := tk.filedialog.askopenfile(
                mode="r",
                initialdir=pathlib.Path.cwd() / pathlib.Path("data"),
                initialfile=self.args.min,
                defaultextension=".txt",
                filetypes=(("TXT", "*.txt"), ("All Files", "*.*")),
            )
        ) :
            try:
                path = pathlib.Path(file.name)
                mins = numpy.loadtxt(str(path))
                for i, (v, vn) in enumerate(pairwise(mins)):
                    self.draw.line(
                        [i, self.args.height - 1 - v, i + 1, self.args.height - 1 - vn], fill="black", width=1
                    )
                    self.canvas.create_line(
                        i, self.args.height - 1 - v, i + 1, self.args.height - 1 - vn, fill="black", width=1
                    )
            finally:
                file.close()

    def openmax(self):
        if (
            file := tk.filedialog.askopenfile(
                mode="r",
                initialdir=pathlib.Path.cwd() / pathlib.Path("data"),
                initialfile=self.args.max,
                defaultextension=".txt",
                filetypes=(("TXT", "*.txt"), ("All Files", "*.*")),
            )
        ) :
            try:
                path = pathlib.Path(file.name)
                maxs = numpy.loadtxt(str(path))
                for i, (v, vn) in enumerate(pairwise(maxs)):
                    self.draw.line(
                        [i, self.args.height - 1 - v, i + 1, self.args.height - 1 - vn], fill="blue", width=1
                    )
                    self.canvas.create_line(
                        i, self.args.height - 1 - v, i + 1, self.args.height - 1 - vn, fill="blue", width=1
                    )
            finally:
                file.close()

    def getlimits(self):
        data = numpy.array(self.image)
        maxs = numpy.zeros(data.shape[1])
        for j in range(0, data.shape[1]):
            for i in range(0, data.shape[0]):
                if all(data[i, j] == (0, 0, 0)):
                    maxs[j] = max(maxs[j], i)
        mins = numpy.copy(maxs)
        for j in range(0, data.shape[1]):
            for i in range(0, data.shape[0]):
                if all(data[i, j] == (0, 0, 0)):
                    mins[j] = min(mins[j], i)
        return (mins, maxs)

    def savearray(self):
        mins, maxs = self.getlimits()
        numpy.savetxt(pathlib.Path.cwd() / pathlib.Path("data") / (self.args.min), mins)
        numpy.savetxt(pathlib.Path.cwd() / pathlib.Path("data") / (self.args.max), maxs)

    def save(self):
        if (
            file := tk.filedialog.asksaveasfile(
                mode="w",
                initialdir=pathlib.Path.cwd() / pathlib.Path("data"),
                initialfile=self.args.image,
                defaultextension=".png",
                filetypes=(("PNG", "*.png"), ("All Files", "*.*")),
            )
        ) :
            try:
                path = pathlib.Path(file.name)
                self.image.save(path)
                self.savearray()
            finally:
                file.close()

    def pen_up(self, event):
        self.latest = None

    def pen_down(self, event):
        if self.latest:
            self.draw.line([self.latest.x, self.latest.y, event.x, event.y], fill="black", width=1)
            self.canvas.create_line(self.latest.x, self.latest.y, event.x, event.y, fill="black", width=1)
        self.latest = event


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Draw numpy array.")
    parser.add_argument("--width", default=640, help="width of canvas")
    parser.add_argument("--height", default=480, help="width of canvas")
    parser.add_argument("--image", default="image.png", help="Default filename for image.")
    parser.add_argument("--min", default="min.txt", help="Default filename for min array.")
    parser.add_argument("--max", default="max.txt", help="Default filename for max array.")

    args = parser.parse_args()

    root = tk.Tk()
    root.title("DrawInput")
    myGUI(root, args)
    root.mainloop()
