import os

from pyglet import image
from pyglet.graphics import Batch
from pyglet.sprite import Sprite
from pyglet.text import Label

import Config as C

script_dir = os.path.dirname(__file__)

class Menu:
  def __init__(self) -> None:
    path = os.path.join(script_dir, C.Asset.INTRO_IMAGE)
    intro_image = image.load(path)
    self._intro_image_sprite = Sprite(img=intro_image, x=0, y=0)

    path = os.path.join(script_dir, C.Asset.END_IMAGE)
    end_image = image.load(path)
    self._end_image_sprite = Sprite(img=end_image, x=0, y=0)

    self._end_level = Label(text=C.GameOver.TEXT, font_name=C.Font.NAME, font_size=C.Font.LARGE, bold=True, color=C.Font.COLOUR, x=C.GameOver.X, y=C.GameOver.Y)

  def show_intro(self) -> None:
    self._intro_image_sprite.draw()

  def show_game_end(self, level: int) -> None:
    self._end_image_sprite.draw()
    self._end_level.text = C.GameOver.TEXT.replace("XXX", str(level))

    self._end_level.draw()
