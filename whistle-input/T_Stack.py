from Stack import Stack
import Config as C

#checking if the if condition works...

def t_update_down():
  s = Stack()
  s.pointer = 0
  s.update(-1)
  assert s.pointer == 0, "Should be 0"

def t_update_up():
  s = Stack()
  high_pointer = C.Stack.NUM_RECTS -1
  s.pointer = high_pointer
  s.update(1)
  assert s.pointer == high_pointer, f"Should be {high_pointer}"

def t_update_normal_1():
  s = Stack()
  s.pointer = 1
  s.update(-1)
  assert s.pointer == 0, "Should be 0"

def t_update_normal_2():
  s = Stack()
  normal_pointer = C.Stack.NUM_RECTS -2
  s.pointer = normal_pointer
  s.update(1)
  assert s.pointer == normal_pointer + 1, f"Should be {normal_pointer + 1}"

def t_update_straigth():
  s = Stack()
  s.pointer = 1
  s.update(0)
  assert s.pointer == 1, f"Should be {1}"

if __name__ == "__main__":
  t_update_down()
  t_update_up()
  t_update_normal_1()
  t_update_normal_2()