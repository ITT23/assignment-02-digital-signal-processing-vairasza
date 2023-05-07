from enum import Enum

from pyglet import media
from pyglet.media import Player
from pyglet.shapes import Rectangle, Circle
from pyglet.clock import schedule_once
import numpy as np

from Audio import AudioInput
import Config as C

class EvaluationState(Enum):
   IDLE = 1
   CORRECT = 2
   WRONG = 3

class TonePalette:

  def __init__(self, audio_input: AudioInput, sound_info: tuple[C.Tone, str, int, int], x: int) -> None:
    self.audio_input = audio_input
    self.sound_info = sound_info
    self.player = Player()
    self.player.queue(media.load(self.sound_info[1]))
    self.listening = False
    self.current_freqs = []
    self.evaluation_state = EvaluationState.IDLE

    self.rect_computer = Rectangle(x=x, y=C.Game.RECT_Y_COMPUTER, width=C.Game.RECT_WIDTH, height=C.Game.RECT_WIDTH, color=C.Color.GREY)
    x_circle_computer = self.rect_computer.x + (self.rect_computer.width / 2)
    self.helper_computer = Circle(x=x_circle_computer, y=self.rect_computer.y - C.Game.CIRCLE_OFFSET, radius=C.Game.CIRCLE_RADIUS, color=C.Color.WHITE)
    self.helper_computer.visible = False

    self.rect_player = Rectangle(x=x, y=C.Game.RECT_Y_PLAYER, width=C.Game.RECT_WIDTH, height=C.Game.RECT_WIDTH, color=C.Color.GREY)
    x_circle_player = self.rect_player.x + (self.rect_player.width / 2)
    self.helper_player = Circle(x=x_circle_player, y=self.rect_player.y - C.Game.CIRCLE_OFFSET, radius=C.Game.CIRCLE_RADIUS, color=C.Color.WHITE)
    self.helper_player.visible = False

  def delete(self) -> None:
    self.rect_computer.delete()
    self.rect_player.delete()
    self.player.delete()

  def _stop_playing(self, _) -> None:
    self.rect_computer.color = C.Color.GREY
    self.helper_computer.visible = False

  def play_sound(self) -> None:
    self.player.play()
    self.helper_computer.visible = True
    self.rect_computer.color = C.Color.WHITE
    schedule_once(func=self._stop_playing, delay=C.Game.DELAY_COMPUTER)
  
  def _evaluate_freq(self) -> bool:
    if len(self.current_freqs) == 0:
      self.evaluation_state = EvaluationState.WRONG
      return False

    #get mode: https://stackoverflow.com/a/46366383/13620136
    frequencies, counts = np.unique(self.current_freqs, return_counts=True)
    index = counts.argmax()

    if frequencies[index] >= self.sound_info[2] and frequencies[index] <= self.sound_info[3]:
      self.evaluation_state = EvaluationState.CORRECT
      return True
    else:
      self.evaluation_state = EvaluationState.WRONG
      return False
    
  def _stop_listening(self, _) -> None:
    self.listening = False
    self.helper_player.visible = False
    
    if self._evaluate_freq():
      self.evaluation_state = EvaluationState.CORRECT
      self.rect_player.color = C.Color.GREEN
    else:
      self.evaluation_state = EvaluationState.WRONG
      self.rect_player.color = C.Color.RED

  def listen_to_sound(self) -> None:
    print(f"listen {self.sound_info[0]}")
    self.current_freqs = []
    self.listening = True
    self.helper_player.visible = True
    schedule_once(func=self._stop_listening, delay=C.Game.DELAY_PLAYER)

  def draw(self) -> None:
    if self.listening:
      self.current_freqs.append(self.audio_input.read_stream())

    self.rect_computer.draw()
    self.helper_computer.draw()

    self.rect_player.draw()
    self.helper_player.draw()