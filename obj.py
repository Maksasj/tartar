import pygame
import random
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, img , width , hight, distplay_surface):
        self.x = x
        self.y = y

        self.health = 100
        self.max_health = 100

        self.width = width
        self.hight = hight

        self.invulnerability = 0

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.velX = 0
        self.velY = 0

        self.angle = 30

        self.speed = 0.1
        self.slip = 0.05

        self.distplay_surface = distplay_surface

        self.Dealing_Damage = True
        self.damage_screen = 0
        self.powerup_screen = 0
        self.regen_screen = 0
        self.portal_screen = 0
        self.DamageSound_Cd = 20
        self.Damage = 1

        self.img = pygame.image.load(img)

        self.weapon = 'hand'

        self.won = False

        self.dt = 0
        self.sweep_angle = 0
        self.rect = self.img.get_rect(center = ( (self.width/2), (self.hight/2)))

    def draw(self, distplay_surface):
        rotated_image = pygame.transform.rotate(self.img, self.angle)

        self.rect = rotated_image.get_rect(center = ((self.width/2), (self.hight/2)))
        distplay_surface.blit(rotated_image, self.rect)

        if self.damage_screen > 0:
            draw_rect_alpha(self.distplay_surface, (255, 50, 50 , 70*(self.damage_screen/100)), pygame.Rect(0, 0, self.width, self.hight))
            self.damage_screen -= 1

        if self.powerup_screen > 0:
            draw_rect_alpha(self.distplay_surface, (100, 100, 255 , 70*(self.powerup_screen/100)), pygame.Rect(0, 0, self.width, self.hight))
            self.powerup_screen -= 1
        
        if self.regen_screen > 0:
            draw_rect_alpha(self.distplay_surface, (100, 255, 100 , 70*(self.regen_screen/100)), pygame.Rect(0, 0, self.width, self.hight))
            self.regen_screen -= 1

        if self.portal_screen > 0:
            draw_rect_alpha(self.distplay_surface, (0, 0, 0 , 70*(self.portal_screen/100)), pygame.Rect(0, 0, self.width, self.hight))
            self.portal_screen -= 0.5

    def portal_col(self, portal):
        portal.rect = portal.img.get_rect(center = (portal.x - self.x, portal.y - self.y))
        col = pygame.sprite.collide_rect(self, portal)
        if col == True:
            return True

    def update_col(self, wall, id, Sound, item_id):
        wall.rect = wall.img.get_rect(center = (wall.x - self.x, wall.y - self.y))
        col = pygame.sprite.collide_rect(self, wall)
        if col == True:
            if self.DamageSound_Cd <= 10:
                Sound.play()
                self.DamageSound_Cd = 40
            if id == 'item':
                if item_id == 0: # Chainmail
                    self.img = pygame.image.load('data/textures/player/player_in_chainmail.png')
                    self.max_health = 150
                    self.powerup_screen = 100

                if item_id == 1: #Gilded Armor
                    self.img = pygame.image.load('data/textures/player/player_gilded_armor.png')
                    self.max_health = 200
                    self.powerup_screen = 100

                if item_id == 2: #Iron Armor
                    self.img = pygame.image.load('data/textures/player/player_iron_armor.png')
                    self.max_health = 250
                    self.powerup_screen = 100

                if item_id == 3: #Healt
                    if (self.health + 50) < self.max_health:
                        self.regen_screen += 100
                        self.health += 50
                    else:
                        self.health = self.max_health

                if item_id == 4:
                    self.Damage = 2
                    self.weapon = 'rusty_sword'
                    self.powerup_screen = 100

                if item_id == 5:
                    self.Damage = 3
                    self.weapon = 'steel_sword'
                    self.powerup_screen = 100

                if item_id == 6:
                    self.Damage = 4
                    self.weapon = 'battle_axe'
                    self.powerup_screen = 100

                wall.x = 10000
                
            else:
                if self.invulnerability <= 0:
                    self.damage_screen = 100
                    if wall.invulnerability_gives <= 10:
                        self.velX = 0
                        self.velY = 0
                    self.health -= wall.damage
                    self.invulnerability = wall.invulnerability_gives
                self.invulnerability -= 1

    def wall_col(self, walls, dt):
        for wall in walls:
            wall.rect = wall.img.get_rect(center = (wall.x - self.x, wall.y - self.y))

        self.rect.x += self.velX*(100*dt)
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for wall in block_hit_list:
            if (self.velX*(100*dt)) > 0:
                self.rect.right = wall.rect.left
            else:
                self.rect.left = wall.rect.right

        self.rect.y += self.velY*(100*dt)
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for wall in block_hit_list:
            if (self.velX*(100*dt)) > 0:
                self.rect.bottom = wall.rect.top
            else:
                self.rect.top = wall.rect.bottom


    def update(self, dt, wall_array):

        if self.left_pressed and not self.right_pressed:
            self.velX -= 0.1 * self.speed
        if self.right_pressed and not self.left_pressed:
            self.velX += 0.1 * self.speed
        if self.up_pressed and not self.down_pressed:
            self.velY -= 0.1 * self.speed
        if self.down_pressed and not self.up_pressed:
            self.velY += 0.1 * self.speed

        self.rect = pygame.Rect(-10 + (self.width/2), -10 + (self.hight/2), 20, 20)

        for wall in wall_array:
            wall.rect = wall.img.get_rect(center = (wall.x - self.x, wall.y - self.y))

        self.rect.x += self.velX*(100*dt)
        block_hit_list = pygame.sprite.spritecollide(self, wall_array, False)
        for wall in block_hit_list:
            if (self.velX*(100*dt)) > 0:
                self.velX = 0
            else:
                self.velX = 0

        self.rect.y += self.velY*(100*dt)
        block_hit_list = pygame.sprite.spritecollide(self, wall_array, False)
        for wall in block_hit_list:
            if (self.velY*(100*dt)) > 0:
                self.velY = 0
            else:
                self.velY = 0

        self.x += self.velX*(100*dt)
        self.y += self.velY*(100*dt)

        self.velX -= self.slip*self.velX
        self.velY -= self.slip*self.velY

    def reset(self, weapon):
        self.invulnerability = 0

        self.health = 100
        self.img = pygame.image.load('data/textures/player/player.png')
        self.weapon = 'hand'
        weapon.img = pygame.image.load('data/textures/handitems/0.png')
        self.Damage = 2
        
class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        self.x = x
        self.y = y

        self.damage = 0.01
        self.invulnerability_gives = 1

        self.img = pygame.image.load(img).convert_alpha()

    def draw(self, distplay_surface, player):
        self.rec = self.img.get_rect(center = (self.x - player.x, self.y - player.y))
        distplay_surface.blit(self.img, self.rec)

class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        self.x = x
        self.y = y

        self.img = pygame.image.load(img).convert_alpha()
        self.rec = self.img.get_rect(center = (self.x, self.y))

    def draw(self, distplay_surface, player):
        self.rec = self.img.get_rect(center = (self.x - player.x, self.y - player.y))
        distplay_surface.blit(self.img, self.rec)

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        self.x = x
        self.y = y

        self.img = pygame.image.load(img).convert_alpha()
        self.rec = self.img.get_rect(center = (self.x, self.y))

    def draw(self, distplay_surface, player):
        self.rec = self.img.get_rect(center = (self.x - player.x, self.y - player.y))
        distplay_surface.blit(self.img, self.rec)

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        
        self.x_ofset = random.randint(3, 15)
        self.y_ofset = random.randint(3, 15)

        self.velX = random.randint(-10, 10)
        self.velY = random.randint(-10, 10)


        self.healt = 50
        self.max_healt = 50
        self.show_healt = False

        self.damage = random.randint(10, 40)
        self.invulnerability_gives = 60

        self.angle = 10
        self.speed = 0.015
        self.slip = 0.02
        self.img = pygame.image.load(img)

        
    def draw(self, distplay_surface, player):
        if self.show_healt == True:
            pygame.draw.rect(distplay_surface, (50,50,50), 
            pygame.Rect(
                self.x - player.x - 27 * (self.healt/self.max_healt), 
                self.y - player.y - 44, 
                70 * (self.healt/self.max_healt), 
                18))
            
            pygame.draw.rect(distplay_surface, (255,0,0), 
            pygame.Rect(
                self.x - player.x - 24 * (self.healt/self.max_healt), 
                self.y - player.y - 40, 
                64 * (self.healt/self.max_healt), 
                10))

        
        
        rotated_image = pygame.transform.rotate(self.img, self.angle + 90)
        self.rec = rotated_image.get_rect(center = (self.x - player.x + self.x_ofset, self.y - player.y + self.y_ofset))

        distplay_surface.blit(rotated_image, self.rec)

    def update(self, player):
        if self.healt <= 0:
            self.x = 10000
        if math.sqrt( ( (self.x - ((player.width/2) + player.x))**2) + ( (self.y - ((player.hight/2) + player.y))**2) ) < 300:
            rel_x, rel_y = ((player.width/2)+ player.x) - self.x, ((player.hight/2)+ player.y) - self.y
            self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
            
            self.x -= (self.x - ((player.width/2) + player.x)) * self.speed
            self.y -= (self.y - ((player.hight/2) + player.y)) * self.speed
            self.show_healt = True
            if player.Dealing_Damage and (math.sqrt( ( (self.x - ((player.width/2) + player.x))**2) + ( (self.y - ((player.hight/2) + player.y))**2) ) < 150):
                self.healt -= player.Damage
        else:
            self.show_healt = False

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        
        self.x_ofset = random.randint(3, 15)
        self.y_ofset = random.randint(3, 15)

        self.velX = random.randint(-10, 10)
        self.velY = random.randint(-10, 10)

        healt = random.randint(400, 900)
        self.healt = healt
        self.max_healt = healt
        self.show_healt = False

        self.damage = 10
        self.invulnerability_gives = 60

        self.angle = 10
        self.speed = 0.005
        self.slip = 0.02
        self.img = pygame.image.load(img)

        
    def draw(self, distplay_surface, player):
        if self.show_healt == True:
            pygame.draw.rect(distplay_surface, (50,50,50), 
            pygame.Rect(
                self.x - player.x - 27 * (self.healt/self.max_healt), 
                self.y - player.y - 44, 
                70 * (self.healt/self.max_healt), 
                18))
            
            pygame.draw.rect(distplay_surface, (255,0,0), 
            pygame.Rect(
                self.x - player.x - 24 * (self.healt/self.max_healt), 
                self.y - player.y - 40, 
                64 * (self.healt/self.max_healt), 
                10))

        rotated_image = pygame.transform.rotate(self.img, self.angle)
        self.rec = rotated_image.get_rect(center = (self.x - player.x + self.x_ofset, self.y - player.y + self.y_ofset))

        #self.rec = self.img.get_rect(center = (self.x - player.x + self.x_ofset, self.y - player.y + self.y_ofset))
        distplay_surface.blit(rotated_image, self.rec)

    def update(self, player):
        if self.healt <= 0:
            self.x = 10000
        if math.sqrt( ( (self.x - ((player.width/2) + player.x))**2) + ( (self.y - ((player.hight/2) + player.y))**2) ) < 300:
            self.x -= (self.x - ((player.width/2) + player.x)) * self.speed
            self.y -= (self.y - ((player.hight/2) + player.y)) * self.speed
            self.show_healt = True
            if player.Dealing_Damage and (math.sqrt( ( (self.x - ((player.width/2) + player.x))**2) + ( (self.y - ((player.hight/2) + player.y))**2) ) < 150):
                self.healt -= player.Damage
        else:
            self.x -= self.speed * self.velX
            self.y -= self.speed * self.velY
            self.show_healt = False

class Text():
    def __init__(self, font_adress, font_size):
        self.coin_font = pygame.font.Font(font_adress, font_size)
    
    def draw(self , distplay_surface, text, color, x, y):
        coin_text = self.coin_font.render(str(text),True, color)
        text_rect = coin_text.get_rect(center = pygame.display.get_surface().get_rect().center)
        text_rect.x += x
        text_rect.y += y
        distplay_surface.blit(coin_text,  text_rect)

class HandItem(pygame.sprite.Sprite):
    def __init__(self, x, y, img, player):
        self.x = x
        self.y = y

        self.item_id = 'hand'

        self.img = pygame.image.load(img)
        self.rect = self.img.get_rect(center = ( (player.width/2), (player.hight/2)))
    def update(self, Player):
        self.item_id = Player.weapon

        if self.item_id == 'rusty_sword':
            self.img = pygame.image.load('data/textures/handitems/2.png')
        if self.item_id == 'steel_sword':
            self.img = pygame.image.load('data/textures/handitems/1.png')
        if self.item_id == 'battle_axe':
            self.img = pygame.image.load('data/textures/handitems/3.png')

    def draw(self, distplay_surface, Player):
        if self.item_id != Player.weapon:
            self.update(Player)

        if self.item_id == "battle_axe":
            pivot = (-10, 60)
            origin = ((Player.width/2), (Player.hight/2))

            image_rect = self.img.get_rect(topleft = (origin[0] - pivot[0], origin[1]-pivot[1]))
            offset_center_to_pivot = pygame.math.Vector2(origin) - image_rect.center
            rotated_offset = offset_center_to_pivot.rotate(-(Player.angle + 45 + Player.sweep_angle*30))
            rotated_image_center = (origin[0] - rotated_offset.x, origin[1] - rotated_offset.y)
            rotated_image = pygame.transform.rotate(self.img, (Player.angle + 45 + Player.sweep_angle*30))
            rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
            distplay_surface.blit(rotated_image, rotated_image_rect)
        else:
            pivot = (-5, 50)
            origin = ((Player.width/2), (Player.hight/2))

            image_rect = self.img.get_rect(topleft = (origin[0] - pivot[0], origin[1]-pivot[1]))
            offset_center_to_pivot = pygame.math.Vector2(origin) - image_rect.center
            rotated_offset = offset_center_to_pivot.rotate(-(Player.angle + 45 + 25*math.sin(Player.sweep_angle*0.6)))
            rotated_image_center = (origin[0] - rotated_offset.x, origin[1] - rotated_offset.y)
            rotated_image = pygame.transform.rotate(self.img, (Player.angle + 45 + 25*math.sin(Player.sweep_angle*0.6)))
            rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
            distplay_surface.blit(rotated_image, rotated_image_rect)

class Drop(pygame.sprite.Sprite):
    def __init__(self, x, y, img, item_id):
        self.x = x
        self.y = y

        self.item_id = item_id

        #id
        #0 = chain armor
        #1 = gilded armor
        #2 = iron armor
        #3 = health
        #4 = rusty sword
        #5 = steel sword
        #6 = battle axe

        self.damage = 0.01
        self.img = pygame.image.load(img).convert_alpha()

    def draw(self, distplay_surface, player):
        self.rec = self.img.get_rect(center = (self.x - player.x, self.y - player.y))
        distplay_surface.blit(self.img, self.rec)

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, img, item_id):
        self.x = x
        self.y = y

        self.item_id = item_id

        #id
        #0 = chain armor
        #1 = gilded armor
        #2 = iron armor
        #3 = health
        #4 = rusty sword
        #5 = steel sword
        #6 = battle axe

        self.damage = 0.01
        self.img = pygame.image.load(img).convert_alpha()

    def draw(self, distplay_surface, player):
        self.rec = self.img.get_rect(center = (self.x - player.x, self.y - player.y))
        distplay_surface.blit(self.img, self.rec)

class Sound():
    def __init__(self, Sound_adress, volume):
        self.Sound = pygame.mixer.Sound(Sound_adress)
        self.Sound.set_volume(volume)
    def play(self):
        self.Sound.play()

class Image(pygame.sprite.Sprite):
    def __init__(self, Texture_adress, width, hight):
        self.img = pygame.image.load(Texture_adress).convert_alpha()
        self.img= pygame.transform.scale(self.img, (width, int((width*9)/16)))
        self.rect = self.img.get_rect()
    def move(self, x , y):
        self.rect = self.rect.move(x, y)
    def draw(self, distplay_surface):
        distplay_surface.blit(self.img, self.rect)

class Button(pygame.sprite.Sprite):
    def __init__(self, Texture_adress, width, hight):
        self.img = pygame.image.load(Texture_adress).convert_alpha()
        self.img= pygame.transform.scale(self.img, (width, hight))
        self.rect = self.img.get_rect()
    def move(self, x , y):
        self.rect = self.rect.move(x, y)
    def draw(self, distplay_surface):
        distplay_surface.blit(self.img, self.rect)

def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)
