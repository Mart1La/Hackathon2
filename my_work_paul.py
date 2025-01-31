import arcade

class Goo(arcade.Sprite):

    def __init__(self, x, y):
        super().__init__(GOO)
        self.index = index
        self.center_x, self.center_y = (x, x), (y, y) # selon le clic
        self.angle = 0
    
    def on_update(self, delta_time):
        
        # Rajouter une variation très faible du centre
        # self.angle += (1 - 2*random.random()) * NOISE_ANGLE

        self.center_x += self.speed * delta_time * math.cos(math.radians(self.angle))
        self.center_y += self.speed * delta_time * math.sin(math.radians(self.angle))

        # On ne teste que les quatre étoiles les plus proches
        delta_x, delta_y = 0, 0

        x_lim = STEP // 2 + ((self.center_x - STEP // 2)//STEP) * STEP
        y_lim = STEP // 2 + ((self.center_y - STEP // 2)//STEP) * STEP
        obstacles_set_reduced = {(x_lim + j*STEP, y_lim + i*STEP) for i in range(2) for j in range(2)}
        obstacle_bool = False
        for obstacle in obstacles_set_reduced:
            gap_x = self.center_x - obstacle[0]
            gap_y = self.center_y - obstacle[1]
            square_distance = (gap_x)**2 + (gap_y)**2
            if square_distance <= CRITICAL_DISTANCE**2:
                obstacle_bool = True
                self.alpha = LEAST_ALPHA + (255 - LEAST_ALPHA) * square_distance**(1/2) / CRITICAL_DISTANCE
                # Décalage par rapport aux obstacles
                delta_factor = 1/2 * (1 - (square_distance)**(1/2)/CRITICAL_DISTANCE)
                delta_x = delta_factor * gap_x
                delta_y = delta_factor * gap_y
        
        # Décalage par rapport aux boids
        for other_boid in window.boids:
            gap_x = self.center_x - other_boid.center_x
            gap_y = self.center_y - other_boid.center_y
            square_distance = (gap_x)**2 + (gap_y)**2
            if square_distance > 0 and square_distance <= (CRITICAL_DISTANCE/5)**2:
                delta_factor = 1/2 * (1 - square_distance**(1/2) / CRITICAL_DISTANCE/5)
                delta_x = delta_factor * gap_x
                delta_y = delta_factor * gap_y

        # Décalage
        self.center_x += delta_x
        self.center_y += delta_y

        # Orientation
        if obstacle_bool:
            var_x = self.center_x - previous_center_x
            var_y = self.center_y - previous_center_y
            if (var_x, var_y) != (0, 0):
                self.angle = math.atan2(var_y, var_x)

        # # Pour rester dans la fenêtre ; à voir...
        # self.center_x %= HEIGHT
        # self.center_y %= WIDTH


    # Voisins dans un dico

    Goos = [Goo() for k in range(20)]

    Goos_adj = {1: [(2,l0_2), (7, l0_7)], 2: [(3, l0_3)], 3: []}

    Goos[0] # premier goo de la liste
    Goos[0].center_x[1] # position à t du premier goo de la liste

    Goos[Goos_adj[1][0][0]] # premier voisin du premier sommet
    Goos[Goos_adj[1][0][1]] # l0 entre le premier sommet et son premier voisin