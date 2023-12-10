from tkinter import Tk, Canvas
import threading, json
root = Tk()

from game import Game

try:
    settings = json.load(open("settings.json", 'r'))
    botOn = settings.get("botOn", True)
except:
    botOn = True

root.title("CHESS")
canvas = Canvas(root, width=800, height=800, bg="gray")
canvas.pack()
restart = True
def main():
    global restart
    while True:
        if restart:
            newG = Game(root, canvas, botOn)
            restart = False
mainThread = threading.Thread(target=main)
mainThread.start()
root.mainloop()
