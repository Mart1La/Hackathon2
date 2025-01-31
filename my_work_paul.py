import arcade

class Goo(arcade.Sprite):

    def __init__(self, x, y):
        super().__init__(GOO)
        self.center_x, self.center_y = (x, x), (y, y) # selon le clic
        self.angle = 0
    
    def on_update(self, delta_time):
        
        # Rajouter une variation très faible au centre du goo
        # NOISE_POSITION = 5
        # self.center_x[1] += (1 - 2*random.random()) * NOISE_POSITION
        # self.center_y[1] += (1 - 2*random.random()) * NOISE_POSITION

        # # Pour rester dans la fenêtre ; à voir...
        # self.center_x %= HEIGHT
        # self.center_y %= WIDTH

class Window(arcade.Window):

    def __init__(self):
        self.Goos = []
        self.Goos_adj = {}

    # Code du clic
    def on_update(self, delta_time):
        for goo in self.Goos:
    pass


     


# Syntaxe

# Goos = [Goo() for k in range(20)]

# Goos_adj = {3: [], 5: [(3, l0_3x5)], 17: [(3,l0_3x17), (5, l0_5x17)]}

# Goos[17] # goo "numéro" 17
# Goos[17].center_x[0] # position à t - dt du goo "numéro" 17
# Goos[17].center_x[1] # position à t du goo "numéro" 17

# Goos[Goos_adj[17][0][0]] # numéro du premier voisin du goo "numéro" 17
# Goos[Goos_adj[17][0][1]] # l0 entre le goo "numéro" 17 et son premier voisin