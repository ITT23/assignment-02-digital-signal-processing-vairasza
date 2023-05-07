from typing import Callable
import random, os

from pyglet import image
from pyglet.sprite import Sprite
from pyglet.clock import schedule_once
from pyglet.text import Label

from Audio import AudioInput
from TonePalette import TonePalette, EvaluationState
import Config as C

script_dir = os.path.dirname(__file__)

class Game:

  def __init__(self, audio_input: AudioInput) -> None:
    self.audio_input = audio_input

    self.level = 1
    self.current_index = 0
    self.max_level = C.Game.MAX_LEVEL
    self.tone_palette: list[TonePalette] = []

    path = os.path.join(script_dir, C.Asset.BACKGROUND)
    bg_image = image.load(path)
    self._intro_image_sprite = Sprite(img=bg_image, x=0, y=0)

    #at the start of the game, define the sequence for max_level
    #then use an index to control the number of tones per level
    self.computer_name = Label(text="Computer:", font_name=C.Font.NAME, font_size=C.Font.LARGE, bold=True, color=C.Font.COLOUR, x=C.Game.NAME_X, y=C.Game.NAMES_Y_COMPUTER)

    self.player_name = Label(text="You:", font_name=C.Font.NAME, font_size=C.Font.LARGE, bold=True, color=C.Font.COLOUR, x=C.Game.NAME_X, y=C.Game.NAME_Y_PLAYER)

  def init(self) -> None:
    self.level = self.level
    self.current_index = 0
    self.tone_palette: list[TonePalette] = []
    self._init_tones()
    self._start_tones()

  def _init_tones(self) -> None:
    for i in range(self.max_level):
      sound_info = random.choice(C.Sound.PALETTE)
      self.tone_palette.append(TonePalette(self.audio_input, sound_info, C.Game.RECT_X + i * C.Game.RECT_X_GAP))

  def _start_tones(self) -> None:
    for i in range(self.current_index + 1):
      print(i)
      self.tone_palette[i].evaluation_state = EvaluationState.IDLE

      schedule_once(lambda _: self.tone_palette[i].play_sound(), C.Game.DELAY_COMPUTER * i)

      delay = C.Game.DELAY_COMPUTER * (self.current_index + 1) + C.Game.DELAY_COMPUTER * i
      schedule_once(lambda _: self.tone_palette[i].listen_to_sound(), delay)

  def _evaluate_game_state(self) -> bool:
    for key, tone in enumerate(self.tone_palette):
      if tone.evaluation_state == EvaluationState.WRONG:
        return False

      elif tone.evaluation_state == EvaluationState.CORRECT and self.current_index == key:
        #next level
        if self.current_index == len(self.tone_palette) - 1:
          self.level += 1
          #for tone in self.tone_palette:
          #  tone.delete()
          self.init()

        #next index
        else:
          self.current_index += 1
          self._start_tones()
    
    return True

  def _draw(self) -> None:
    self._intro_image_sprite.draw()
    self.computer_name.draw()
    self.player_name.draw()
    for tone in self.tone_palette:
      tone.draw()

  def run(self, _on_game_over: Callable[[], None]) -> None:
    if not self._evaluate_game_state():
      _on_game_over()
    self._draw()