from pyglet.shapes import Rectangle
from pyglet.graphics import Batch

import Config as C

class Stack:

  #the lowest rect has index 0
  def __init__(self) -> None:
    self.rects = []
    self.batch = Batch()
    self.pointer = C.Stack.POINTER_START
    self._init_rects()

  def _init_rects(self) -> None:
    for i in range(C.Stack.NUM_RECTS):
      rect = Rectangle(x=C.Stack.RECTS_X, y=C.Stack.RECTS_Y + i * (C.Stack.RECT_HEIGHT + C.Stack.RECTS_OFFSET), width=C.Stack.RECT_WIDTH, height=C.Stack.RECT_HEIGHT, color=C.Color.WHITE, batch=self.batch)
    
      if self.pointer == i:
        rect.color = C.Color.GREEN

      self.rects.append(rect)

  def _move_selection(self) -> None:
    for key, rect in enumerate(self.rects):
      if key == self.pointer:
        rect.color = C.Color.GREEN

      else:
        rect.color = C.Color.WHITE

  def update(self, direction: int) -> None:
    '''
      direction: -1 -> down; 1 -> up; 0 -> no change
    '''
    if direction == -1 and self.pointer != 0:
      self.pointer -= 1
      
    elif direction == 1 and self.pointer != C.Stack.NUM_RECTS - 1:
      self.pointer += 1

    else:
      self.pointer += 0

    self._move_selection()

  def draw(self) -> None:
    self.batch.draw()