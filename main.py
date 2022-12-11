from utils import Recognizer, Camera
from gui import GUI
import threading

event = threading.Event()
camera = Camera()
recognizer = Recognizer('310_20', event)
gui = GUI(camera, recognizer)
