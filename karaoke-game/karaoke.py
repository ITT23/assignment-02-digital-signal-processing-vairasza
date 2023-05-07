import os

from pyglet import app, window
from pyglet.window import key

from Audio import AudioInput
from AppState import AppState
from Menu import Menu
from Game import Game
import Config as C

"""
#https://stackoverflow.com/a/73032937/13620136 -> chunk size of 1024 lead to a constant IOError (OSError: [Errno -9981] Input overflowed) wherefore increasing it to 4096 resolved it; 2048 also works; https://stackoverflow.com/a/35442501/13620136 -> adding exception_on_overflow=False to stream.read() drops all exceptions; https://pyquestions.com/pyaudio-input-overflowed -> use callback function also resolves this issue but with this we have too much data and
"""

class Application:
  def __init__(self, audio_input: AudioInput) -> None:
    self.app_state = AppState.START
    self.window = window.Window(C.Window.WIDTH, C.Window.HEIGTH, caption=C.Window.NAME)
    self.on_draw = self.window.event(self.on_draw)
    self.on_key_press = self.window.event(self.on_key_press)

    self.audio_input = audio_input
    self.menu = Menu()
    self.game = Game(self.audio_input)
  
  def run(self) -> None:
    app.run()

  def _on_game_over(self):
    self.app_state = AppState.END

  def on_draw(self) -> None:
    self.window.clear()

    if self.app_state == AppState.START:
      self.audio_input.open_stream()
      self.menu.show_intro()

    elif self.app_state == AppState.GAME:
      self.game.run(self._on_game_over)

    elif self.app_state == AppState.END:
      self.menu.show_game_end(self.game.level)

    elif self.app_state == AppState.EXIT:
      self.audio_input.stop_stream()
      self.audio_input.end_stream()
      os._exit(0)

  def on_key_press(self, symbol, modifier):
    if symbol == key.SPACE:
      self.game.init()
      self.audio_input.open_stream()
      self.app_state = AppState.GAME

    elif symbol == key.ESCAPE:
      self.app_state = AppState.EXIT

if __name__ == "__main__":
  audio_input = AudioInput()
  audio_input.request_input_device_index()

  application = Application(audio_input)
  application.run()
