import tkinter as tk
import cv2, time
from threading import Thread


class GUI:
    def __init__(self, camera, recognizer):
        self.win = tk.Tk()
        self.win.config(padx=5, pady=5)
        self.recognizer = recognizer
        self.camera = camera
        self.stop_btn = tk.Button(self.win, text="STOP", command=self.stop_camera, font=("Arial", 18, 'bold'), fg='red')
        self.stop_btn.grid(row=0, column=0)
        self.start_btn = tk.Button(self.win, text="START", command=self.start_camera, font=("Arial", 18, 'bold'), fg='red')
        self.start_btn.grid(row=1, column=0)
        self.win.mainloop()

    def start_camera(self):
        # print('start_camera')
        Thread(target=self.recognizer.start, args=(self.camera,)).start()
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='active')

    def stop_camera(self):
        # print('stop_camera')
        Thread(target=self.recognizer.stop).start()
        time.sleep(0.5)
        self.start_btn.config(state='active')
        self.stop_btn.config(state='disabled')
        cv2.destroyAllWindows()
