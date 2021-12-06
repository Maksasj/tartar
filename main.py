import pygame, sys
import math
import random
import time
import json

from pygame.locals import *

from obj import *
from particle_sys import *

settings_f = open('data/settings.json')
settings = json.load(settings_f)

width = settings['Graphic_Settings']['width']
hight = settings['Graphic_Settings']['hight']
render_distance = settings['Graphic_Settings']['render_distance']

pygame.init()

logo = pygame.image.load("data/textures/icon_background/icon64x64.png")
pygame.display.set_icon(logo)

distplay_surface = pygame.display.set_mode((width, hight), pygame.FULLSCREEN)

background = Image("data/textures/icon_background/background.png", width, hight)
tartar = Image("data/textures/icon_background/tartar.png", int(width/2), hight)
tartar.move(width/2.2, (hight/20) - 2.5*(hight/20))

play_button = Button("data/textures/icon_background/play_button.png", int(width/4),  int(width/16))
play_button.move((width/1.7), (hight/3))

#settings_button = Button("data/textures/icon_background/settings_button.png", int(width/4),  int(width/16))
#settings_button.move((width/1.7), (hight/3) + int(width/12))

about_button = Button("data/textures/icon_background/about_button.png", int(width/4),  int(width/16))
about_button.move((width/1.7), (hight/3) + int(width/12))

exit_button = Button("data/textures/icon_background/exit_button.png", int(width/8),  int(width/16))
exit_button.move((width - width*0.12), (hight - hight*0.1))

pause_button = Button("data/textures/icon_background/pause.png", int(width/12),  int(width/12))
pause_button.move((width - width*0.08), 0*(hight - hight*0.1))


pygame.display.set_caption('Tartar')
Player = Player(0, 0, 'data/textures/player/player.png', width, hight, distplay_surface)
HandItem = HandItem(0, 200,'data/textures/handitems/0.png' , Player)

clock = pygame.time.Clock()
Wall_List = [ [], [], [], [], []]

Wall_List[0] = ([ 
    [16,    13,     9,     13,     13,     13,      9,     13,     13,     13,     13,     13,     13,     13,     9,     13,     17], 
    [12,    100,    12,     0,      0,      1000,   12,     0,      0,      0,     0,      0,      0,      0,      12,      200,      12], 
    [12,    200,    12,     0,      0,      0,      12,     0,      0,      0,     1,      0,      0,      0,      11,      0,      12], 
    [12,    0,      12,     0,      100,    2,      14,     0,      1,      0,     0,      0,      0,      0,      0,      0,      12], 
    [12,    0,      12,     0,      0,      0,      0,      0,      0,      0,     0,      0,     10,      0,      0,      0,      12], 
    [12,    0,      11,     100,    0,      0,      0,      0,      0,      0,     0,      0,     12,      0,      2,      13,      9], 
    [12,    0,      0,      0,      100,    0,      0,      1,      0,      0,     0,      0,     12,      0,      0,      0,      12], 
    [12,    0,      0,      0,      0,      0,      0,      0,      0,      0,     0,      0,     12,      0,      0,      0,      12], 
    [9,    13,      13,     13,    13,      3,      0,      0,      0,      0,     0,      0,     12,      0,      0,      0,      12], 
    [12,    0,      0,      0,      0,      0,      0,      1,      0,      0,     0,      0,     12,      0,      0,      0,      12], 
    [12,    0,      0,      0,      0,      0,      0,      0,      0,      0,     0,      0,     12,      0,      0,      0,      12],  
    [12,    0,      0,      2,      17,     0,      0,      0,      0,      0,     0,      0,     12,      0,      0,      0,      12], 
    [12,    0,      0,      0,      12,     0,      0,      0,      0,      0,     0,      0,     12,      0,      0,      100,      12], 
    [12,    0,      0,      100,    12,     0,      0,      0,      0,      0,     0,      0,     12,      0,      100,      100,      12], 
    [12,    0,      100,    0,      12,     0,      7,      6,      0,      0,     0,      0,     12,      0,      100,      100,      12], 
    [12,    0,      0,      0,      12,     0,      5,      4,      0,      0,     1,      0,     12,      0,      100,      100,      12], 
    [12,    100,    0,      0,      12,     100,    0,      0,      0,      0,     0,      0,     12,      0,      100,      200,      12], 
    [12,    0,      0,      200,    12,     200,    100,    0,      0,      0,     0,      0,     12,      0,      200,      200,      12],  
    [15,    13,     13,     13,     8,      13,     13,     13,     13,     13,    13,     13,     8,      13,     13,     13,     14], 
    ])

Wall_List[1] = ([ 
    [16,    13,     13,     9,      13,     13,     13,      9,     13,     13,     9,      13,     13,     13,     13,     13,     17], 
    [12,    200,    0,      12,     0,      0,      0,      12,     0,      200,    12,      0,      0,      0,      100,      0,      12], 
    [12,    100,    0,      12,     0,      0,      0,      12,     0,      0,      12,      0,      1,      0,      100,      0,      12], 
    [12,    100,    0,      12,     0,      0,      0,      12,     100,  100,      12,      0,      0,      0,      100,      0,      12], 
    [12,    0,      0,      12,     0,      0,      0,      12,     0,      0,      12,      0,      1,      0,      100,      0,      12], 
    [12,    0,      2,      8,      3,     100,    16,      14,     0,      0,      12,      0,      0,      0,      100,      0,      12], 
    [12,    0,      0,      0,      0,      0,      12,     0,      0,      0,      12,      0,      1,      0,      100,      0,      12], 
    [12,    0,      1,      0,      0,      0,      12,     0,      0,      0,      11,      0,      0,      0,      100,      0,      12], 
    [12,    0,      0,      0,      0,      0,      12,     0,      0,      0,      0,      0,      1,      0,      100,      0,      12],  
    [12,    0,      100,    2,     13,      13,      9,     0,      100,    0,      0,      0,      0,      0,      100,      0,      12], 
    [12,    0,      0,      0,      0,      0,      12,     0,      0,      0,      0,      0,      1,      0,      100,      0,      12], 
    [12,    0,      0,      0,      0,      0,      12,     0,      0,      0,      10,      0,      0,      0,      100,      0,      12], 
    [12,    0,      1,      0,      1,      0,      12,     0,      0,      0,      12,      0,      1,      0,      100,      0,      12], 
    [12,    0,      0,      100,    0,      0,      11,     0,    100,      0,      12,      0,      0,      0,      100,      0,      12], 
    [12,    0,      0,      0,      0,      0,      0,      0,      0,      0,      12,      0,      1,      0,      100,      0,      12], 
    [12,    0,      1,      0,      0,      0,      0,      0,      0,      0,      12,      0,      0,      0,      100,      0,      12], 
    [12,    100,    0,      0,      16,     13,     13,     13,     13,     13,     8,     13,     13,     3,      0,      0,      12], 
    [12,    200,    100,    0,      12,     1000,   0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      12], 
    [15,    13,     13,     13,     8,      13,     13,     13,     13,     13,     13,     13,     13,     13,     13,     13,     14], 
    ])

Wall_List[2] = ([ 
    [16,    13,     13,     9,      13,     13,     13,     13,     13,     13,     13,     13,     13,     13,     13,     13,     17], 
    [12,    200,    100,    12,     100,    100,    100,    100,    100,    12,     0,      0,      0,      0,      0,      0,      12], 
    [12,    100,    0,      12,     100,    100,    1000,   100,    100,    12,     0,      1,      0,      0,      0,      0,      12], 
    [12,    0,      0,      12,     100,    0,      0,      0,      0,      12,     0,      0,      0,      10,     0,      0,      12],  
    [12,    0,      0,      12,     0,      0,      100,    0,      0,      12,     0,      1,      0,      12,     0,      0,      12],  
    [12,    0,      200,    12,     200,    0,      0,      0,      0,      12,     0,      100,    0,      12,     0,      0,      12], 
    [12,    0,      2,      8,      13,     3,      0,      2,      13,     9,      3,      0,      0,      12,     0,      0,      12], 
    [12,    0,      0,      0,      0,      0,      0,      0,      0,      12,     0,      0,      0,      12,     100,    100,    12],  
    [12,    0,      0,      100,    0,      0,      100,    0,      0,      12,     0,      0,      0,      12,     100,    100,      12],  
    [12,    0,      0,      0,      0,      0,      1,      0,      0,      12,     0,      1,      0,      12,     100,    100,      12],  
    [12,    100,    1,      0,      100,    0,      0,      0,      0,      12,     0,      0,      100,    12,     100,    100,      12],  
    [12,    0,      0,      100,    0,      0,      0,      0,      0,      12,     0,      0,      0,      12,     100,    100,      12],  
    [12,    100,    0,      0,      0,      0,      0,      0,      0,      12,     0,      100,    0,      12,     0,      0,      12], 
    [12,    0,      1,      0,      0,      0,      0,      0,      0,      11,     0,      1,      0,      12,     0,      0,      12],  
    [12,    100,    0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      12,     0,      0,      12], 
    [12,    0,      0,      100,    0,      0,      0,      0,      0,      0,      100,    0,      0,      12,     0,      0,      12], 
    [12,    100,    1,      0,      16,      13,      13,     13,     13,     13,     13,     13,     13,     14,     0,      0,      12], 
    [12,    200,    0,      0,      12,      0,      0,     0,      0,      0,      0,      0,      0,      0,      0,      0,      12], 
    [15,    13,     13,     13,     13,     13,     8,      13,     13,     13,     13,     13,     13,     13,     13,     13,     14], 
    ])

Wall_List[3] = ([ 
    [16,    13,     13,     9,      13,     13,     13,     13,     13,     13,     13,     13,     13,     13,     13,     13,     17], 
    [12,    0,      0,    0,     0,    0,      0,      0,      0,      0,     0,      0,    0,      0,     0,      0,      12], 
    [12,    0,      0,    0,     0,    0,      0,      0,      0,      0,     0,      0,    0,      0,     0,      0,      12], 
    [12,    0,      0,    0,     0,    0,      0,      0,      0,      0,     0,      0,    0,      0,     0,      0,      12],  
    [12,    0,      0,    0,     0,    0,      0,      0,      0,      0,     0,      0,    0,      0,     0,      0,      12], 
    [12,    0,      0,    0,     0,    0,      0,      0,      0,      0,     0,      0,    0,      0,     0,      0,      12], 
    [12,    0,      0,    0,     0,    0,      0,      0,      0,      0,     0,      0,    0,      0,     0,      0,      12], 
    [12,    0,      0,    0,     0,    0,      0,      0,      0,      0,     0,      0,    0,      0,     0,      0,      12], 
    [12,    0,      0,    0,     0,    0,      0,      0,      0,      0,     0,      0,    0,      0,     0,      0,      12], 
    [12,    0,      0,    0,     0,    0,      0,      0,      0,      0,     0,      0,    0,      0,     0,      0,      12],  
    [12,    0,      0,    0,     0,    0,      0,      0,      0,      0,     0,      0,    0,      0,     0,      0,      12], 
    [12,    0,      0,    0,     0,    0,      0,      0,      0,      0,     0,      0,    0,      0,     0,      0,      12], 
    [12,    0,      0,    0,     0,    0,      0,      0,      0,      0,     0,      0,    0,      0,     0,      0,      12], 
    [12,    0,      0,    0,     0,    0,      0,      0,      0,      0,     0,      0,    0,      0,     0,      0,      12], 
    [12,    0,      0,    0,     0,    0,      0,      0,      0,      0,     0,      0,    0,      0,     0,      0,      12],  
    [12,    0,      0,    0,     0,    0,      0,      0,      0,      0,     0,      0,    0,      0,     0,      0,      12], 
    [12,    0,      0,    0,     0,    0,      0,      0,      0,      0,     0,      0,    0,      0,     0,      0,      12], 
    [12,    0,      0,    0,     0,    0,      0,      0,      0,      0,     0,      0,    0,      0,     0,      0,      12], 
    [15,    13,     13,     13,     13,     13,     13,      13,     13,     13,     13,     13,     13,     13,     13,     13,     14], 
    ])

level = 0
max_level = 3

Tile_Array = []
Wall_Array = []
Enemy_Array = []
Item_Array = []
Portal = []

#Sounds
PowerUpSound = Sound('data/sounds/effects/powerUp.wav', settings['Sound']['sound_effects_vol'])
WallSound = Sound('data/sounds/effects/wallhit.wav', settings['Sound']['sound_effects_vol'])
EnemySound = Sound('data/sounds/effects/enemyhit.wav', settings['Sound']['sound_effects_vol'])
Swip = Sound('data/sounds/effects/swip.mp3', settings['Sound']['sound_effects_vol'])
Player_Death = Sound('data/sounds/effects/player_death.wav', settings['Sound']['sound_effects_vol'])


FootStepSounds = []
FootStepSounds.append(Sound('data/sounds/effects/footstep1.mp3', settings['Sound']['ambient']) )
FootStepSounds.append(Sound('data/sounds/effects/footstep2.mp3', settings['Sound']['ambient']) )
FootStepSounds.append(Sound('data/sounds/effects/footstep3.mp3', settings['Sound']['ambient']) )

#Theme music
pygame.mixer.music.load('data/sounds/music/theme.mp3')
pygame.mixer.music.play(-1)
FootStepSounds_Cd = 20

pygame.mixer.music.set_volume(settings['Sound']['music_vol'])

def load_level(level):
    Wall_Init_X = 0
    Wall_Init_Y = 0

    Tile_Array.clear()
    Wall_Array.clear()
    Enemy_Array.clear()
    Item_Array.clear()
    Portal.clear()
    
    for Row in Wall_List[level]:
        Wall_Init_Y += 1
        for Collum in Row:           
            if Collum == 0:
                Wall_Random = random.randint(1, 11)
                Tile_Array.append(Floor(Wall_Init_X*64, Wall_Init_Y*64, "data/textures/floor/floortile"+str(Wall_Random)+".png"))
            if Collum == 100:
                Wall_Random = random.randint(1, 3)
                Enemy_Random = random.randint(1, 3)
                Enemy_Array.append(Mob(Wall_Init_X*64, Wall_Init_Y*64, "data/textures/enemy/"+str(Enemy_Random)+".png"))
                Tile_Array.append(Floor(Wall_Init_X*64, Wall_Init_Y*64, "data/textures/floor/floortile"+str(Wall_Random)+".png"))
            if Collum == 200:
                Wall_Random = random.randint(1, 3)
                Item_ID = random.randint(1, 6)
                Tile_Array.append(Floor(Wall_Init_X*64, Wall_Init_Y*64, "data/textures/floor/floortile"+str(Wall_Random)+".png"))
                Item_Array.append(Drop(Wall_Init_X*64, Wall_Init_Y*64, "data/textures/items/item"+str(Item_ID)+".png", Item_ID))
            if Collum == 1000:
                Wall_Random = random.randint(1, 3)
                Portal.append(Floor(Wall_Init_X*64, Wall_Init_Y*64, "data/textures/floor/portal.png"))
                Tile_Array.append(Floor(Wall_Init_X*64, Wall_Init_Y*64, "data/textures/floor/floortile"+str(Wall_Random)+".png"))
            if Collum != 0 and Collum != 100 and Collum != 200 and Collum != 1000:
                Wall_Array.append(Barrier(Wall_Init_X*64, Wall_Init_Y*64, "data/textures/wall/new_wall"+str(Collum)+".png"))
            
            Player.portal_screen = 360

            Wall_Init_X += 1
        Wall_Init_X = 0
Particle_Generators = []
#Void \/
Particle_Generators.append(Particle_Spawner([0, 64*17], [-50, 50], [(0, 0, 0), (10, 10, 10), (5,5,5)] , [1, 1] , 20, [-10, 10] , [-1, 0], 200))
Particle_Generators.append(Particle_Spawner([0, 64*17], [1250, 1350], [(0, 0, 0), (10, 10, 10), (5,5,5)] , [1, 1] , 20, [-10, 10] , [0, 1], 200))
Particle_Generators.append(Particle_Spawner([-100, 0], [0, 1250], [(0, 0, 0), (10, 10, 10), (5,5,5)] , [1, 1] , 20, [-10, 0] , [0, 0], 200))
Particle_Generators.append(Particle_Spawner([1000, 1100], [0, 1250], [(0, 0, 0), (10, 10, 10), (5,5,5)] , [1, 1] , 20, [0, 10] , [0, 0], 200))

Wall_Trace = False #Стены хуярит

In_Game_Timer_Start = time.time()
In_Game_Timer = 0

text = Text('data/fonts/VCR_OSD_MONO.ttf', 30)

game_state = 0
# 1 = Menu
# 0 = Levels
# 2 = Settings
# 3 = about

prev_time = time.time()

load_level(0)

Exit = True
while True: # main game loop
    In_Game_Timer = int(time.time() - In_Game_Timer_Start)
    if In_Game_Timer > 150:
        Wall_Trace = True
    if In_Game_Timer > 60:
        rand = random.randint(1, 50)
        if rand == 50:
            random.choice(Tile_Array).y = random.randint(-Player.hight, 2*Player.hight)
            random.choice(Tile_Array).y = random.randint(-Player.hight, 2*Player.hight)
        
        rand = random.randint(1, 50)
        if rand == 50:
            random.choice(Enemy_Array).y = random.randint(-Player.hight, 2*Player.hight)
            random.choice(Enemy_Array).y = random.randint(-Player.hight, 2*Player.hight)
            
    now = time.time()
    dt = now - prev_time
    prev_time = now
    Player.dt = dt
    if game_state == 1:
        distplay_surface.fill((0, 0, 0))

        for Tile in Tile_Array:
            if math.sqrt( ( (Tile.x - ((Player.width/2) + Player.x))**2) + ( (Tile.y - ((Player.hight/2) + Player.y))**2) ) < render_distance:
                Tile.draw(distplay_surface, Player)
        
        if math.sqrt( ( (Portal[0].x - ((Player.width/2) + Player.x))**2) + ( (Portal[0].y - ((Player.hight/2) + Player.y))**2) ) < render_distance:
            Portal[0].draw(distplay_surface, Player)
        
        for Item in Item_Array:
            if math.sqrt( ( (Item.x - ((Player.width/2) + Player.x))**2) + ( (Item.y - ((Player.hight/2) + Player.y))**2) ) < render_distance:
                Item.draw(distplay_surface, Player)
                Player.update_col(Item, 'item', PowerUpSound, Item.item_id)

        if Wall_Trace == True:
            Player.update(dt, Wall_Array)

        for Wall in Wall_Array:
            if math.sqrt( ( (Wall.x - ((Player.width/2) + Player.x))**2) + ( (Wall.y - ((Player.hight/2) + Player.y))**2) ) < render_distance:
                Wall.draw(distplay_surface, Player)

        for Enemy in Enemy_Array:
            if math.sqrt( ( (Enemy.x - ((Player.width/2) + Player.x))**2) + ( (Enemy.y - ((Player.hight/2) + Player.y))**2) ) < render_distance:
                Enemy.update(Player)
                Enemy.draw(distplay_surface, Player)
                Player.update_col(Enemy, 'enemy', EnemySound, 0)

        #if Wall_Trace == False:
        if Wall_Trace == False:
            Player.update(dt, Wall_Array)
            
        for Particle_Generator in Particle_Generators:
            Update_Particles(Particle_Generator)
            Draw_Particles(distplay_surface, Particle_Generator, Player)
        
        pos = pygame.mouse.get_pos()
        HandItem.draw(distplay_surface, Player)
        Player.wall_col(Wall_Array, dt)
        Player.draw(distplay_surface)

        Player.DamageSound_Cd -= 1
        
        #Gui
        if Player.won == True:
            text.draw(distplay_surface , "You won !!!", (255, 255, 0) , 0 , 0)
        Player_Healt_Prop = str(int(Player.health))+'/'+str(Player.max_health)
        text.draw(distplay_surface , "Healt: "+Player_Healt_Prop, (255, 0, 0) , -(width/2) + (width/9), (hight/2) - (hight/20))
        text.draw(distplay_surface , "Level: "+str(level+1)+"/"+(str(max_level+1)), (255, 255, 255) , -(width/2) + (width/12), -(hight/2) + (hight/20))

        clock.tick()
        Player.speed = 1/int(clock.get_fps() + 1) + 0.5

        mause_left, mause_middle, mause_right = pygame.mouse.get_pressed()
    
        #Damage Detection
        if mause_left:
            Player.Dealing_Damage = True
            if Player.DamageSound_Cd < 10:
                Swip.play()
                Player.DamageSound_Cd = 40
            Player.sweep_angle += 40*dt
        else:
            Player.Dealing_Damage = False
        
        FootStepSounds_Cd -= 1
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if FootStepSounds_Cd < 10:
                    FootStepSounds[random.randint(0,2)].play()
                    FootStepSounds_Cd = 80
                if event.key == pygame.K_a:
                    Player.left_pressed = True
                if event.key == pygame.K_d:
                    Player.right_pressed = True
                if event.key == pygame.K_w:
                    Player.up_pressed = True
                if event.key == pygame.K_s:
                    Player.down_pressed = True

            if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        Player.left_pressed = False
                    if event.key == pygame.K_d:
                        Player.right_pressed = False
                    if event.key == pygame.K_w:
                        Player.up_pressed = False
                    if event.key == pygame.K_s:
                        Player.down_pressed = False
            if event.type == pygame.MOUSEBUTTONDOWN:           
                if pause_button.rect.collidepoint(pygame.mouse.get_pos()):
                    game_state = 0
            
        mause_pos = pygame.mouse.get_pos()
        mause_distance_x = ((width/2) -mause_pos[0])
        mause_distance_y = ((hight/2) -mause_pos[1])

        if mause_distance_x == 0: mause_distance_x = 1
        distance = math.degrees(math.atan(mause_distance_y/mause_distance_x))

        if (mause_distance_x > 0) and (mause_distance_y > 0):
            Player.angle = 90+(-distance)
        if (mause_distance_x < 0) and (mause_distance_y < 0):
            Player.angle = 270+(-distance)
        if (mause_distance_x > 0) and (mause_distance_y < 0):
            Player.angle = 90+(-distance)
        if (mause_distance_x < 0) and (mause_distance_y > 0):
            Player.angle = 270+(-distance)

        if Player.portal_col(Portal[0]) == True:
            level += 1
            if level >= max_level:
                Player.won = True
                Portal[0].x = 10000
            else:
                Tile_Array.clear()
                Wall_Array.clear()
                Enemy_Array.clear()
                Item_Array.clear()
                Portal.clear() 
                load_level(level)

        

        if Player.health <= 0:
            Player_Death.play()
            game_state = 0

            Player.reset(HandItem)

        pause_button.draw(distplay_surface)
        
        pygame.display.update()
    elif game_state == 0:
        distplay_surface.fill((0, 0, 0))

        background.draw(distplay_surface)
        tartar.draw(distplay_surface)
        
        play_button.draw(distplay_surface)
        #settings_button.draw(distplay_surface)
        about_button.draw(distplay_surface)
        exit_button.draw(distplay_surface)

        mause_left, mause_middle, mause_right = pygame.mouse.get_pressed()

        clock.tick()
        pygame.display.set_caption('Tartar Fps: '+ str(int(clock.get_fps())))
    
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:           
                if play_button.rect.collidepoint(pygame.mouse.get_pos()):
                    game_state = 1
                #if settings_button.rect.collidepoint(pygame.mouse.get_pos()):
                #    game_state = 2
                if about_button.rect.collidepoint(pygame.mouse.get_pos()):
                    game_state = 3
                if exit_button.rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()    
        pygame.display.update()       
    elif game_state == 2:
        distplay_surface.fill((0, 0, 0))

        background.draw(distplay_surface)
        exit_button.draw(distplay_surface)

        mause_left, mause_middle, mause_right = pygame.mouse.get_pressed()

        clock.tick()
        pygame.display.set_caption('Tartar Fps: '+ str(int(clock.get_fps())))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:           
                if exit_button.rect.collidepoint(pygame.mouse.get_pos()):
                    game_state = 0
        pygame.display.update()
    elif game_state == 3:
        distplay_surface.fill((0, 0, 0))

        background.draw(distplay_surface)
        exit_button.draw(distplay_surface)

        mause_left, mause_middle, mause_right = pygame.mouse.get_pressed()

        text.draw(distplay_surface , "Dark fantasy with elements of satire", (255, 255, 255)                                        , -(width/2) + (width/2), -(hight/2) + (hight/20) + (hight/3))
        text.draw(distplay_surface , "for the production of 2D games in 2000.", (255, 255, 255)                                     , -(width/2) + (width/2), -(hight/2) + 2*(hight/20) + (hight/3))
        text.draw(distplay_surface , "Made by one person, in pure python with ", (255, 255, 255)                                    , -(width/2) + (width/2), -(hight/2) + 3*(hight/20) + (hight/3))
        text.draw(distplay_surface , "popular pygame library, for Backtrace GameJam #3", (255, 255, 255)                            , -(width/2) + (width/2), -(hight/2) + 4*(hight/20) + + (hight/3))


        clock.tick()
        pygame.display.set_caption('Tartar Fps: '+ str(int(clock.get_fps())))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:           
                if exit_button.rect.collidepoint(pygame.mouse.get_pos()):
                    game_state = 0
        
        pygame.display.update()