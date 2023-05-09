## Bierschneider (11.5/15P)

### 1 Karaoke Game (5/6P)

 * frequency detection
   * detection seems to work pretty well (+3)
 * game
   * Had to do a bit of fiddling around to get everything to run. Problem was that the audio device was initialized in a loop so it crashed on startup. (-1)
   * seems to work after the fix (+1)
 * latency
   * looks good (+1)

### 2 Whistle Input (6/8P)

 * whiste detection
   * in rare cases, the direction is detected wrong (-0.5)
   * works great otherwise (+2.5)
 * robust against noise
   * almost passed my sophisticated background noise test, good enough (+2)
 * latency
   * very fast for pyglet program (+0.5), very slow with key presses (-0.5)
 * pyglet test program
   * works (+1)
 * triggered key events
   * had to fix a number of things to get it working (-1)
     * 'up' was in an else block, so it got triggered during silence
     * no key release in 'up' condition
     * sleeping for 200 ms adds a lot of latency and is not required when there is a neutral condition

## Bonus Point: (0.5/1P)

Code looks really good but I had to fix things in both programs (-0.5)
