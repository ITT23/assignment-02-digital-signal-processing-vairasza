[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/Itg11K3e)

remove unnessecary packages at last

## Setup

1. source ./.venv/bin/activate
2. python -m pip install -r requirements.txt

## Karaoke Game

0. `python karaoke.py` to start in the terminal
1. start game with SPACE
2. terminate game with ESC
3. the games idea comes from colour memory game: https://youtu.be/Tm6mAwrn2L8
4. the computer plays a sequence of sine sounds
5. after the sequence that builds up, you must correctly repeat it
6. the white dot under the rectangle shows where the sequence is
7. the upper row is the computer that plays the sounds
8. the lower row is where you must put in the sounds
9. the rectangles are coloured red and green after evaluating the result
10. you get to the next level with a longer sequence after beating the current level

## Whistle Input

1. start it in terminal with `python whistle-input.py [gui]`
2. if gui is 1, the application is rendered with a gui/pyglet and shows the rectangle stack that you can navigate through
3. if gui is 0, the application is terminal only and uses pynput to navigate through apps
4. Terminal application can uses whistle input to navigate: whistle up corresponds to arrow-up-key, while whistle down corresponds to arrow-down-key
5. use ESC key to quit both applications

## References

- for generating sine data: https://www.audiocheck.net/audiofrequencysignalgenerator_sinetone.php
- frequences: https://de.wikipedia.org/wiki/Frequenzen_der_gleichstufigen_Stimmung
- background image: https://unsplash.com/@othentikisra
