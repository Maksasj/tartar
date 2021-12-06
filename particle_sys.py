import pygame
import random
import math

from obj import Player

def Draw_Particles(distplay_surface, Particle_Gen, Player):
    for particle in Particle_Gen.particles:
        particle.render(distplay_surface, Player)
        if particle.life_time <= 0:
            Particle_Gen.particles.remove(particle)
    
def Update_Particles(Particle_Gen):
    for x in range(random.randint(Particle_Gen.particle_min_amount, Particle_Gen.particle_max_amount)):
        particle_colors = Particle_Gen.particle_colors
        particle = Particle(random.randint(Particle_Gen.x[0],Particle_Gen.x[1]) , random.randint(Particle_Gen.y[0],Particle_Gen.y[1]), random.randint(Particle_Gen.particle_xVel[0],Particle_Gen.particle_xVel[1])/10, random.randint(Particle_Gen.particle_yVel[0], Particle_Gen.particle_yVel[1]), Particle_Gen.particle_radius, random.choice(particle_colors), Particle_Gen.particle_life_time)
        Particle_Gen.particles.append(particle)

class Particle():
    def __init__(self, x, y, xvel, yvel, radius, color, life_time):
        self.x = x
        self.y = y
        
        self.xvel = xvel
        self.yvel = yvel
        
        self.radius = radius
        self.color = color

        self.life_time = life_time

    def render(self, win, Player):
        self.x += self.xvel
        self.y += self.yvel

        self.radius -= 0.1 * (1/self.life_time)
        self.life_time -= 1

        pygame.draw.circle(win, self.color, (self.x - Player.x, self.y - Player.y), self.radius)

class Particle_Spawner():
    def __init__(self, x, y, colors , amount , radius , xVel, yVel, life_time):
        self.x = x
        self.y = y

        self.particles = []
        self.particle_colors = colors
        self.particle_radius = radius
        self.particle_xVel = xVel
        self.particle_yVel = yVel
        self.particle_min_amount = amount[0]
        self.particle_max_amount = amount[1]
        self.particle_life_time = life_time

    def Move(self, x , y, Player):
        self.x = [int(x[0] + Player.x), int(x[1] + Player.x)]
        self.y = [int(y[0] + ((Player.hight/2) + Player.y)), int(y[1] +  ((Player.hight/2) + Player.y))]
