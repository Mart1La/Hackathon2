import arcade
#import random as rd

WIDTH = 800
HEIGHT = 800
TITLE = "Worlds of Goo"
#PLATEFORME = "\data\plateform.png"
#BACKGROUND = "\prout"


"""
class Plateform(arcade.Window):

    def __init__(self, n):
        super().__init__(PLATEFORME)
        if n == 0:
            self.center_x = (WIDTH / 4) * (1+rd.normal(-0.5, 0.5))
        else : 
            self.center_x = (3 * WIDTH / 4) * (1+rd.normal(-0.5, 0.5))
        self.center_y = (HEIGHT / 2)*(1+rd.normal(-0.5, 0.5))
"""

class Window(arcade.Window):

    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        #arcade.set_background_color(BACKGROUND)
        #self.set_location(800, 100)
        #self.plateformes = arcade.SpriteList()
    
    #def setup():
    #    for n in range(0, 1):
    #        plateforme = Plateform(n)

    def on_draw(self):
        arcade.start_render()
        #self.plateformes.draw()

def main():
    window = Window()
    arcade.run()  # Lance la boucle de jeu, elle attend les événements et affiche la fenêtre

if __name__ == "__main__":
    main()