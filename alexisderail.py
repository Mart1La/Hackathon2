
import arcade
import random as rd

BACKGROUND = arcade.color.ALMOND
WIDTH = 800
HEIGHT = 600
TITLE = "Worlds of Goo"
PLATEFORME = "data/plateforme3.png"
Spread = 0.1
START = "data/start.png"
FINISH = "data/finish.png"

class Plateform(arcade.Sprite):

    def __init__(self, n):
        super().__init__(PLATEFORME)
        if n == 0:
            self.center_x = (WIDTH / 4) * (1+rd.uniform(-Spread, Spread))
        else : 
            self.center_x = (3 * WIDTH / 4) * (1+rd.uniform(-Spread, Spread))
        self.center_y = (HEIGHT / 2)*(1+rd.uniform(-Spread, Spread))

class StartOrFinish(arcade.Sprite):
    def __init__(self, n, x, y):
        if n == 0:
            super().__init__(START)
        else :
            super().__init__(FINISH)
        self.center_x = x
        self.center_y = y

class Window(arcade.Window):

    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        arcade.set_background_color(BACKGROUND)
        #arcade.set_background_color(BACKGROUND)
        self.set_location(800, 100)
        self.plateforms = arcade.SpriteList()
    
    def setup(self):
        for n in range(0, 2):
            plateform = Plateform(n)
            startorfinish = StartOrFinish(n, plateform.center_x, plateform.center_y-40)
            self.plateforms.append(plateform)
            self.plateforms.append(startorfinish)

    def on_update(self, delta_time):
        pass
    
    def on_mouse_press(self, x, y, button, modifiers):
        print(int(x), int(y))
        return super().on_mouse_press(int(x), int(y), button, modifiers)

    def on_draw(self):
        #arcade.start_render()
        self.plateforms.draw()

window = Window()
window.setup()
arcade.run()

