import threading
from tkinter import *
from main_window import *


class SettingsWindow(Tk):
    def __init__(self):
        super().__init__()

        greet_button = Button(self, text="Run drawing window", command=self.run_drawing_window)
        greet_button.pack()

        self.drawing_window = None

    def run_drawing_window(self):
        self.drawing_window = MainWindow()

        t1 = threading.Thread(target=self.drawing_window_main_loop)
        t1.start()

    def drawing_window_main_loop(self):
        while self.drawing_window.running:
            self.drawing_window.update()
            pygame.time.Clock().tick(60)
