import pyaudio

class Audio:
  CHUNK_SIZE = 2048 #this increases the resolution of frequencies
  FORMAT = pyaudio.paInt16
  CHANNELS = 1
  RATE = 44100

class Font:
  NAME = "Verdana"
  SMALL = 15
  LARGE = 24
  XLARGE = 56
  COLOUR = (255,255,255,255)

class Window:
  WIDTH = 1280
  HEIGTH = 720
  NAME = "Whistler"

class Stack:
  NUM_RECTS = 5
  POINTER_START = 2
  RECT_WIDTH = 150
  RECT_HEIGHT = 100
  RECTS_OFFSET = 20
  RECTS_X = Window.WIDTH / 2 - RECT_WIDTH / 2
  #so that all rects are vertically centered
  RECTS_Y = ((Window.HEIGTH - ((RECT_HEIGHT * NUM_RECTS) + (RECTS_OFFSET * (NUM_RECTS - 1)))) / 2)

class Color:
  RED = (255,0,0,255)
  GREEN = (0,168,107,255)
  GREY = (122,122,122,255)
  WHITE = (255,255,255,255)

class Terminal:
  SLEEP_TIME = 0.2

'''
Nilsson, M., Bartunek, J. S., Nordberg, J., & Claesson, I. (2008, May). Human whistle detection and frequency estimation. In 2008 Congress on Image and Signal Processing (Vol. 5, pp. 737-741). IEEE.
according to this paper, the human whistle range is from 500 to 5000 Hz
'''
class Frequency:
  LOWER = 90 #lower boudry of 500 did not work at all. idk
  UPPER = 5000
  KERNEL_SIZE = 5
  KERNEL_SIG = 1
  MIN_LENGTH = 4
  WHISTLE_UP_THRESHOLD = 2
  WHISTLE_DOWN_THRESHOLD = -2