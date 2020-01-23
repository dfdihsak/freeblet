import tkinter as tk  
import tkinter.filedialog
import pyautogui    # pip3 install PyAutoGUI
import cv2          # pip3 install opencv-python
import numpy as np  # pip3 install numpy
from thinning import guo_hall_thinning  # pip3 install thinning_py3

points = []

class Application(tk.Frame):
    def __init__(self, master=None):
        print("Welcome to Freeblet Beta! This is window for testing purposes. If something goes wrong, copy paste what appears here and contact https://www.freeblet.com/")
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.threshold_label = tk.Label(self, text="To stop, move\nmouse to any\nCORNER of screen")
        self.threshold_label.pack(side="top")

        self.adjustment = tk.Scale(self, from_=0, to=255, orient="horizontal", variable=threshold)
        self.adjustment.set(127)
        self.adjustment.pack(side="top")

        self.threshold_label = tk.Label(self, text="Tolerance")
        self.threshold_label.pack(side="top")

        self.speed_toggle = tk.Scale(self, from_=0, to=10, orient="horizontal", variable=speed)
        self.speed_toggle.set(2)
        self.speed_toggle.pack(side="top")

        self.speed_label = tk.Label(self, text="Delay")
        self.speed_label.pack(side="top")

        self.previewer = tk.Button(self)
        self.previewer["text"] = "Preview"
        self.previewer["command"] = self.getFilePreview
        self.previewer.pack(side="top")

        self.draw = tk.Button(self)
        self.draw["text"] = "Draw"
        self.draw["command"] = self.drawFile
        self.draw.pack(side="top")

        # self.speed = tk.Scale(self, from_=0, to=255, orient="horizontal", variable=threshold)
        # self.speed.set(127)
        # self.speed.pack(side="top")

    def getFilePreview(self):
        print("previewing...")
        # file select
        self.filename = tk.filedialog.askopenfilename(
            initialdir = "/",title = "Select file",
            filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        image = cv2.imread(self.filename, 0)
        print(self.filename)
        self.getPoints(image, True)  # sets points to last thing previewed
        print("done")

    def drawFile(self):
        # sets speed
        pyautogui.PAUSE = 0.0005 * speed.get()
        screenWidth, screenHeight = pyautogui.size() 
        x, y = pyautogui.position()
        print("drawing...")
        # file select
        self.filename = tk.filedialog.askopenfilename(
            initialdir = "/",title = "Select file",
            filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        image = cv2.imread(self.filename, 0)
        print(self.filename)
        global points
        points = self.getPoints(image, False)  # sets points to last thing previewed
        print("got points")
        print(x)
        print(y)
        pyautogui.moveTo(x + 150, y) 
        print("moved")
        x_diff = x - points[0][0] + 150
        y_diff = y - points[0][1]
        pyautogui.moveTo(points[0][0] + x_diff, points[0][1] + y_diff) 
        print(pyautogui.position())         
        # clicks a few times to ensure window is selected
        pyautogui.click()
        pyautogui.click()
        pyautogui.click()        
        pyautogui.mouseDown()
        pyautogui.mouseUp()
        pyautogui.mouseDown()
        print("moved broh")
        while (points):
            self.getStroke(points[0], 0, x_diff, y_diff)

    # converts the picture to an array of points
    def getPoints(self, image, show):
        window = image[0:3000,0:3000] # crops image pixels to desired window size
        # sets threshold
        _, filtered = cv2.threshold(window, threshold.get(), 255, cv2.THRESH_BINARY_INV)
        window = guo_hall_thinning(filtered)
        if show:
            cv2.imshow("test", window)
        # plt.imshow(window)
        # plt.show()
        
        points = []

        # add to array
        for pt in np.argwhere(window.T != 0):
            point = []
            point.append(pt[0]) # add x coordinate
            point.append(pt[1]) # add y
            points.append(point)

        return points

    # connects the points in a stroke from starting point
    def getStroke(self, point, stack, x_diff, y_diff):
        print(stack)
        if (stack > 900):
            pyautogui.click()
            pyautogui.mouseUp()
            pyautogui.mouseUp()
            pyautogui.mouseUp()
            return
        pyautogui.moveTo(point[0] + x_diff, point[1] + y_diff)
        pyautogui.mouseDown()
        pyautogui.mouseDown()
        pyautogui.mouseDown()
        continued = False
        # adds point to stroke
        # stroke.append(point)
        # removes points that have been added
        points.remove(point)
        # surrounding pixels are all potential neighbors
        potentialNeighbors =    [[point[0] - 1, point[1] - 1], [point[0], point[1] - 1], [point[0] + 1, point[1] - 1], 
                                [point[0] - 1, point[1]], [point[0] + 1, point[1]], 
                                [point[0] - 1, point[1] + 1], [point[0], point[1] + 1], [point[0] + 1, point[1] + 1]]

        # recursive step
        for potentialNeighbor in potentialNeighbors:
            if potentialNeighbor in points:
                result = potentialNeighbor
                continued = True
                self.getStroke(potentialNeighbor, stack + 1, x_diff, y_diff)
        if (not continued):
            pyautogui.click()
            pyautogui.mouseUp()
            pyautogui.mouseUp()
            pyautogui.mouseUp()

root = tk.Tk()
threshold = tk.IntVar()
speed = tk.IntVar()
root.geometry("100x250")
root.title('Freeblet (BETA)')
app = Application(master=root)
app.mainloop()