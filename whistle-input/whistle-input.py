import os, argparse, time

from pyglet import app, window
from pyglet.window import key
from pynput.keyboard import Key, Controller, Listener

from Audio import AudioInput
from Stack import Stack
import Config as C

"""
#https://stackoverflow.com/a/73032937/13620136 -> chunk size of 1024 lead to a constant IOError (OSError: [Errno -9981] Input overflowed) wherefore increasing it to 4096 resolved it; 2048 also works; https://stackoverflow.com/a/35442501/13620136 -> adding exception_on_overflow=False to stream.read() drops all exceptions; https://pyquestions.com/pyaudio-input-overflowed -> use callback function also resolves this issue but with this we have too much data and
"""

class GUIApplication:
  def __init__(self, audio_input: AudioInput) -> None:
    self.window = window.Window(C.Window.WIDTH, C.Window.HEIGTH, caption=C.Window.NAME)
    self.on_draw = self.window.event(self.on_draw)
    self.on_key_press = self.window.event(self.on_key_press)

    self.audio_input = audio_input
    self.audio_input.open_stream()
    self.stack = Stack()
  
  def run(self) -> None:
    app.run()

  def on_draw(self) -> None:
    self.window.clear()

    direction = self.audio_input.get_direction()

    self.stack.update(direction)
    self.stack.draw()

  def on_key_press(self, symbol, modifier) -> None:
    if symbol == key.ESCAPE:
      self.audio_input.stop_stream()
      self.audio_input.end_stream()

      os._exit(0)


class TerminalApplication:

  #https://pypi.org/project/pynput/
  def __init__(self, audio_input: AudioInput) -> None:
    self.audio_input = audio_input
    self.audio_input.open_stream()
    self.keyboard = Controller()
    self.keyboard_listener = Listener(on_press=self.on_press)
    self.keyboard_listener.start()
    self.running = True

  def on_press(self, key) -> None:
    if key == Key.esc:
      self.running = False

  def run(self) -> None:
    while self.running:
      direction = self.audio_input.get_direction()

      #down
      if direction == -1:
        #press and release need to be used as some listeners only listen to one of these events
        print('down')
        self.keyboard.press(Key.down)
        self.keyboard.release(Key.down)
      #up
      elif direction == 1:
        print('up')
        self.keyboard.press(Key.up)
        self.keyboard.release(Key.up)
      else:
        pass

      #time.sleep(C.Terminal.SLEEP_TIME)


if __name__ == "__main__":
  #https://docs.python.org/3/library/argparse.html
  parser = argparse.ArgumentParser(prog="Whistle Input", description="helps you navigate by whistling")
  parser.add_argument("gui", type=int, help="disable gui application and use pynput controller to navigate by using 0. use 1 to use gui.")

  args = parser.parse_args()

  audio_input = AudioInput()
  audio_input.request_input_device_index()

  if args.gui:
    gui_app = GUIApplication(audio_input)
    gui_app.run()

  else:
    t_app = TerminalApplication(audio_input)
    t_app.run()
