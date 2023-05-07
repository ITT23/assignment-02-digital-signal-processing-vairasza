from enum import Enum

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
  NAME = "Tonepalette"

class Asset:
  INTRO_IMAGE = "assets/start_bg.png"
  BACKGROUND = "assets/game_bg.jpg"
  END_IMAGE = "assets/end_bg.png"

class Tone(Enum):
  C4 = 1
  E4 = 2
  G4 = 3
  A4 = 4

class Sound:
  #https://de.wikipedia.org/wiki/Frequenzen_der_gleichstufigen_Stimmung
  #(file location, lower boundry, upper boundry)
  C4 = (Tone.C4, "assets/c4_1s.mp3", 251, 277)
  E4 = (Tone.E4, "assets/e4_1s.mp3", 319, 339)
  G4 = (Tone.G4, "assets/g4_1s.mp3", 381, 401)
  A4 = (Tone.A4, "assets/a4_1s.mp3", 430, 450)
  PALETTE = [C4, E4, G4, A4]

class GameOver:
  TEXT = "Sequence level: XXX. YEAH!"
  X = 730
  Y = 350

class Game:
  MAX_LEVEL = 4
  
  RECT_X = 100
  RECT_X_GAP = 50
  RECT_Y_COMPUTER = 450
  RECT_Y_PLAYER = 300
  RECT_WIDTH = 40

  CIRCLE_RADIUS = 10
  CIRCLE_OFFSET = 25
  
  NAME_X = 100
  NAMES_Y_COMPUTER = 500
  NAME_Y_PLAYER = 350

  DELAY_COMPUTER = 1
  DELAY_PLAYER = 1.5

  TONE_LENGTH = 1

class Color:
  RED = (255,0,0,255)
  GREEN = (0,168,107,255)
  GREY = (122,122,122,255)
  WHITE = (255,255,255,255)
