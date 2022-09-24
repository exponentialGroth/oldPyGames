import pygame
import random
from pygame import draw
import time
from pygame import rect
import math
from pygame import mixer


mixer.init()
pygame.init()

WIDTH, HEIGHT = 1925, 1020

WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Jump and Run")

BLACK=(0,0,0)
WHITE=(255,255,255)
PINK=(235,0,255)
BLUE = pygame.Color('lightskyblue3')
BLUE2 = (0, 99, 117)
ANAKIWA = (128, 243, 255)
RED = (255, 98, 0)
BROWN = (163, 85, 13)


# game variables

FPS = 50
size = 50
vel_of_moving_ground = 0


distance_pos = (100, 50)
distance_font = pygame.font.Font(None, 50)

bullet_width = 17
bullet_height = 12

number_of_collided_obstacle = 0

dying_enemy_sound = mixer.Sound("sounds\dyingenemy4.wav")
dying_player_sound = mixer.Sound("sounds\\and-then-i-kissed-him.wav")
shooting_sound = mixer.Sound("sounds\shot2.wav")
background_sound = mixer.Sound("sounds\pearl-harbor-war2.wav")



# menu variables

play_button_font = pygame.font.SysFont('microsofthimalaya', 150)
play_button_text = play_button_font.render("PLAY", True, RED)
play_button_rect = pygame.Rect(WIDTH/2 - play_button_text.get_width()/2, HEIGHT/2 - play_button_text.get_height()/2, play_button_text.get_width(), play_button_text.get_height() -40)
highscore_font = pygame.font.SysFont('microsofthimalaya', 100)

controls_img = pygame.transform.scale(pygame.image.load("pictures\controls.png"), (311, 300))

new_distance = 0


#pictures

BLACK_STAR_IMAGE = pygame.image.load("pictures\\black_star_844x728.png")
YELLOW_BUTTON_IMAGE = pygame.image.load("pictures\yellow_button_269x269.png")
YELLOW_BUTTON_ACTIVATED_IMAGE = pygame.image.load("pictures\yellow_button_activated.png")




class Background:
    def __init__(self, height, color) -> None:
        self.height = height
        self.color = color
        self.rect = pygame.Rect(0, 0, WIDTH, self.height)



class Ground:
    def __init__(self, colors, pos_list) -> None:
        self.colors = colors
        self.number_of_rects = len(pos_list)
        self.pos_list = pos_list
        self.rects = []
        for index in range(self.number_of_rects):
            if index < self.number_of_rects - 1:
                self.rects.append(pygame.Rect(pos_list[index][0], pos_list[index][1], pos_list[index + 1][0] - pos_list[index][0], HEIGHT - pos_list[index][1] ))
            else:
                self.rects.append(pygame.Rect(pos_list[index][0], pos_list[index][1], 10000, HEIGHT - pos_list[index][1] ))

        self.hitboxes = []

        for i in self.rects:
            self.hitboxes.append((i.x, i.y, i.w, i.h))




    def collision(self, player_rect, player_vel, other_player):
        touched = []
        number_of_collided_rect = 0
        for rect in self.rects:
            if player_rect.x < rect.x + rect.w and player_rect.x + player_rect.w >= rect.x:
                #return player_rect.y + size + player_vel[1] >= rect.y
                if player_rect.y + size >= rect.y:   
                    if player_rect.x + size - player_vel[0] < rect.x + vel_of_ground:
                        touched.append("right")
                    
                    if player_rect.x - player_vel[0] > rect.x + rect.w:
                        touched.append("left")
                        
                    if player_rect.y + size + player_vel[1] >= rect.y:
                        touched.append("bottom")
                        if self.colors[number_of_collided_rect] == RED:
                            other_player.die()
                        

                    if player_rect.y - player_vel[1] > rect.y + rect.h:
                        touched.append("top")
            
            number_of_collided_rect += 1
        return touched             

    def pos_after_collision(self, player_rect, player_vel):

        for rect in self.rects:
            if player_rect.x + player_vel[0] < rect.x + rect.w and player_rect.x + player_rect.w + player_vel[0] > rect.x:
                #return player_rect.y + size + player_vel[1] >= rect.y
                if player_rect.y + size + player_vel[1] >= rect.y and player_rect.y <= rect.y + rect.h:   
                    if player_rect.x + size - player_vel[0] < rect.x + vel_of_ground:
                        pass
                    if player_rect.y + size + player_vel[1] >= rect.y:

                        return rect.y - size
                    if player_rect.y - player_vel[1] > rect.y + rect.h:
                        pass


    def move_ground(self, vel):
        self.rects = []
        for i in range(self.number_of_rects):
            self.pos_list[i] = (self.pos_list[i][0] - vel, self.pos_list[i][1] )

        for index in range(self.number_of_rects):
            if index < self.number_of_rects - 1:
                self.rects.append(pygame.Rect(self.pos_list[index][0], self.pos_list[index][1], self.pos_list[index + 1][0] - self.pos_list[index][0], HEIGHT - self.pos_list[index][1] ))
            else:
                self.rects.append(pygame.Rect(self.pos_list[index][0], self.pos_list[index][1], 10000, HEIGHT - self.pos_list[index][1] ))

        self.hitboxes = []
        for i in self.rects:
            
            self.hitboxes.append((i.x, i.y, i.w, i.h))



class Obstacles:
    def __init__(self, pos_list, type_list, size_width_height_list) -> None:
        self.xpos_list = []
        self.ypos_list = []
        for i in pos_list:
            self.xpos_list.append(i[0])
            self.ypos_list.append(i[1])
        
        self.type_list = type_list
        self.images_list = []
        for i in range(len(type_list)):
            if self.type_list[i] == "blackstar":
                self.images_list.append(pygame.transform.scale(BLACK_STAR_IMAGE, size_width_height_list[i]))
            if self.type_list[i] == "brownblock":
                self.images_list.append(pygame.Rect(self.xpos_list[i], self.ypos_list[i], size_width_height_list[i][0], size_width_height_list[i][1]))
    

        self.hitboxes = []
        for i in range(len(self.type_list)):
            if self.type_list[i] == "blackstar":
                self.hitboxes.append((self.xpos_list[i], self.ypos_list[i], self.images_list[i].get_width(), self.images_list[i].get_height()))
            elif self.type_list[i] == "brownbox":
                self.hitboxes.append((self.xpos_list[i], self.ypos_list[i], self.images_list[i].w, self.images_list[i].h))
    


    def draw_obstacles(self):
        for i in range(len(self.type_list)):
            if self.type_list[i] == "blackstar":
                WIN.blit(self.images_list[i], (self.xpos_list[i], self.ypos_list[i]))
            elif self.type_list[i] == "brownblock":
                draw.rect(WIN, BROWN, self.images_list[i], border_radius = 1)



    def move(self):
        for i in range(len(self.xpos_list)):
            self.xpos_list[i] -= vel_of_ground
            if self.type_list[i] == "brownblock":
                self.images_list[i].x -= vel_of_ground

        self.hitboxes = []
        for i in range(len(self.type_list)):
            if self.type_list[i] == "blackstar":
                self.hitboxes.append((self.xpos_list[i], self.ypos_list[i], self.images_list[i].get_width(), self.images_list[i].get_height()))
            elif self.type_list[i] == "brownblock":
                self.hitboxes.append((self.xpos_list[i], self.ypos_list[i], self.images_list[i].w, self.images_list[i].h))


    
    def collision(self, player_rect, player_vel, other_player):
        global number_of_collided_obstacle
        touched = []
        number_of_checked_hitbox = -1
        for hitbox in self.hitboxes:
            number_of_checked_hitbox += 1

            if player_rect.x + player_rect.w >= hitbox[0] and player_rect.x <= hitbox[0] + hitbox[2]:
                if player_rect.y + size >= hitbox[1] and player_rect.y <= hitbox[1] + hitbox[3]:

                    if player_rect.x + size - player_vel[0] < hitbox[0] + vel_of_ground:
                       touched.append("right")
                       if self.type_list[number_of_checked_hitbox] == "blackstar":
                           other_player.die()
                    if player_rect.y + size - player_vel[1] <= hitbox[1]:
                       touched.append("bottom")
                       if self.type_list[number_of_checked_hitbox] == "blackstar":
                           other_player.die()
                        
                    if player_rect.y - player_vel[1] > hitbox[1] + hitbox[3]:
                        touched.append("top")
                        if self.type_list[number_of_checked_hitbox] == "blackstar":
                            other_player.die()
            
            
        
        return touched


    def pos_after_collision(self, player_rect, player_vel):
        for hitbox in self.hitboxes:

            if player_rect.x + player_rect.w >= hitbox[0] and player_rect.x <= hitbox[0] + hitbox[2]:
                if player_rect.y + size >= hitbox[1] and player_rect.y <= hitbox[1] + hitbox[3]:
                    if player_rect.x + size - player_vel[0] < hitbox[0] + vel_of_ground:
                        pass
                    if player_rect.y + size - player_vel[1] <= hitbox[1]:
                        return hitbox[1] - size
                    if player_rect.y - player_vel[1] > hitbox[1] + hitbox[3]:
                        return hitbox[1] + hitbox[3]
        
        return False

        




class Button:
    def __init__(self, pos, width, height, reversed = False) -> None:
        self.xpos = pos[0]
        self.ypos = pos[1]
        self.active = False
        self.size = (width, height)
        self.reversed = reversed
        self.picture = pygame.transform.scale(YELLOW_BUTTON_IMAGE, self.size)
        self.picture_activated = pygame.transform.scale(YELLOW_BUTTON_ACTIVATED_IMAGE, (self.size[0], round(self.size[0] * 84/269)))
        

    def draw_button(self):
        if not self.active:
            WIN.blit(self.picture, (self.xpos, self.ypos))
        else:
            WIN.blit(self.picture_activated, (self.xpos, self.ypos - self.size[1] * 84/269 + self.size[1]))

    def check_for_player(self, other):
        self.rect = pygame.Rect(self.xpos, self.ypos, self.size[0], self.size[1])
        if not self.reversed:
            if other.rect.colliderect(self.rect):       #eig darf er nur von oben activated werden
                self.active = True

    def move(self):
        self.xpos -= vel_of_ground



class Elevator:
    def __init__(self, x, y, width, height, color, vel_list, active = False) -> None:


        self.x = x
        self.y = y
        #self.speed = speed
        self.active = active
        self.width = width
        self.height = height
        self.color = color
        self.vel_list = vel_list
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hitboxes = [(self.x, self.y, self.width, self.height)]
        self.absolute_position = 0







    def collision(self, other_pos, other_vel):
        if other_pos[0] + size > self.x and other_pos[0] < self.x + self.width:
            if (self.y <= other_pos[1] + size + other_vel[1]) and other_vel[1] >= 0 and self.y >= other_pos[1] + size - other_vel[1]:
                return True

        return False


    def return_vel(self):
        pass


    def draw(self):
        pygame.draw.rect(WIN, self.color, self.rect)


    def move(self, distance):

        self.x -= vel_of_ground
            
        #if distance > 100:
            #self.speed[1] += 0.25

        if self.active:
            #self.x += self.speed[0]
            #self.y += self.speed[1]
            self.x += self.vel_list[self.absolute_position][0]
            self.y += self.vel_list[self.absolute_position][1]
            

            self.absolute_position += vel_of_ground






        self.hitboxes = [(self.x, self.y, self.width, self.height)]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    

class Bullet:

    BULLET_IMAGE = pygame.image.load("pictures\\bullet_17x12.png")
    BULLET_IMAGE_REVERSED = pygame.image.load("pictures\\bullet_17x12_reversed.png")
    
    def __init__(self, pos, speed = 5) -> None:
        self.x = pos[0]
        self.y = pos[1]
        self.speed = speed

    def move(self):
        self.x += self.speed

    def draw(self):
        if self.speed > 0:
            WIN.blit(self.BULLET_IMAGE, (self.x, self.y))
        else:
            WIN.blit(self.BULLET_IMAGE_REVERSED, (self.x, self.y))

    def collision(self, other_hitbox):

        if other_hitbox[0] <= self.x <= other_hitbox[0] + other_hitbox[2]:
            if other_hitbox[1] <= self.y + bullet_height/2 <= other_hitbox[1] + other_hitbox[3]:
                return True



class FlyingEnemy:
    picture = pygame.image.load("pictures\enemy1.png")

    def __init__(self, pos, shooting_intervall, bullet_speed, flying_intervall, vel_y, size) -> None:
        self.x = pos[0]
        self.y = pos[1]
        self.max_y = pos[1] + flying_intervall
        self.min_y = pos[1] - flying_intervall
        self.vel_y = vel_y
        self.shooting_intervall = shooting_intervall
        self.bullet_speed = bullet_speed
        self.image = pygame.transform.scale(self.picture, size)
        self.last_shot = time.time()
        self.size = size
        

    def draw(self):
        WIN.blit(self.image, (self.x, self.y))

    def move(self):
        self.x -= vel_of_ground
        self.y += self.vel_y
        if self.y < self.min_y or self.y > self.max_y:
            self.vel_y *= -1

    def shoot(self, other_player_pos):
        if self.last_shot + 0.75 <= time.time() and 1 == random.randint(0, self.shooting_intervall):
        #if 1 == random.randint(0, 120 * self.shooting_intervall ** -1):
            self.last_shot = time.time()
            if other_player_pos[0] > self.x and -100 < self.x < 2200:
                return ((self.x + self.image.get_width(), self.y + self.image.get_height()/2 - bullet_height / 2), self.bullet_speed)
            if other_player_pos[0] < self.x and -100 < self.x < 2200:
                return ((self.x, self.y + self.image.get_height()/2 - bullet_height / 2), -1 * self.bullet_speed - vel_of_ground)
        return None


    def collision(self, other_player_pos):
        if other_player_pos[0] + size > self.x and other_player_pos[0] < self.x + self.size[0]:
            if other_player_pos[1] + size > self.y and other_player_pos[1] < self.y + self.size[1]:
                return True

    




class Player:

    def __init__(self, xpos, ypos, size, color, shape, distance = 0, xvel = 0, yvel = 0) -> None:
        self.x = xpos
        self.y = ypos
        self.x_vel = xvel
        self.y_vel = yvel
        self.color = color
        self.shape = shape
        self.rect = pygame.Rect(self.x, self.y, size, size)
        self.distance = distance
        self.gravitation = 1
        self.standing_on_moving_ground = False
    


    def __add__(self, o):
        self.distance += o


    def draw_player(self):
        self.rect = pygame.Rect(self.x, self.y, size, size)
        draw.rect(WIN, self.color, self.rect)
        #WIN.blit(self.picture, (self.x, self.y))


    def shoot(self):
        shooting_sound.play()
        return (self.x + size, self.y + size/2 - bullet_height / 2)


    def right_side_is_free(self, o):
        for i in o.hitboxes:
            if self.x + size >= i[0] and self.x + size < i[0] + i[2]:
                if self.y + size > i[1] or self.y > i[1]:
                    #print(i, self.y + size)
                    return False
                else:
                    return True

    def left_side_is_free(self, o):
        for i in o.hitboxes:
            if self.x > i[0] and self.x < i[0] + i[2]:
                if self.y + size > i[1]:
                    return False
                else:
                    return True     


    def bottom_is_free(self, o):
        left_bottom_is_free = True
        right_bottom_is_free = True

        for i in o.hitboxes:
            if self.x > i[0] and self.x < i[0] + i[2]:
                if self.y + size > i[1] and self.y + size < i[1] + i[3]:
                    left_bottom_is_free = False
            
            if self.x + size > i[0] and self.x + size < i[0] + i[2]:
                if self.y + size > i[1] and self.y + size < i[1] + i[3]:
                    right_bottom_is_free = False

        if left_bottom_is_free and right_bottom_is_free:
            return True
        else:
            return False

    def height_after_jump(self, other):
        left_height, right_height = 1000, 1000
        for i in other.hitboxes:
            if self.x > i[0] and self.x < i[0] + i[2]:
                left_height = i[1]

            if self.x + size > i[0] and self.x + size < i[0] + i[2]:
                right_height = i[1]


        if left_height <= right_height:
            return left_height- size
        else:
            return right_height - size


    def change_vel(self, keys_pressed):
        if keys_pressed[pygame.K_a] and self.x > 2:
            self.x_vel -= 2
            #self.distance -= 2/100

            #if keys_pressed[pygame.K_RSHIFT]:
               # self.x_vel -= 3
                #self.distance -= 3/100


        if keys_pressed[pygame.K_d] and self.x + size < WIDTH - 2:
            self.x_vel += 3
            #self.distance += 3/100
            if keys_pressed[pygame.K_RSHIFT]:
                self.x_vel += 3
                #self.distance += 3/100

        

        if keys_pressed[pygame.K_SPACE] and self.y_vel <= -1:
            self.y_vel -= 0.5

        
        if self.standing_on_moving_ground:
           self.x_vel += vel_of_moving_ground

        
        self.x_vel -= vel_of_ground



    def fall(self):

        self.y_vel += self.gravitation


    def jump(self):
        self.y -= 1
        self.y_vel -= 15
        #print("jump")



    def move(self, other_ground, other_elevators, other_obstacle):

        global vel_of_moving_ground

        self.x += self.x_vel
        self.distance += self.x_vel / 100
        self.y += self.y_vel
        self.rect = pygame.Rect(self.x, self.y, size, size)


        other_ground_collision = other_ground.collision(self.rect, (self.x_vel, self.y_vel), self)
        #if not self.right_side_is_free(other_ground):
        if "right" in other_ground_collision:
            self.x -= self.x_vel
            self.x -= vel_of_ground

        if "left" in other_ground_collision:
            self.x -= self.x_vel
            self.x -= vel_of_ground



        self.rect = pygame.Rect(self.x, self.y, size, size)

        obstacles_collision = other_obstacle.collision(self.rect, (self.x_vel, self.y_vel), self)
        if "right" in obstacles_collision:
            self.x -= self.x_vel
            self.x -= vel_of_ground

        if "bottom" in obstacles_collision:
            self.y = other_obstacle.pos_after_collision(self.rect, (self.x_vel, self.y_vel))
            self.standing_on_moving_ground = False

        if "top" in obstacles_collision:
            self.y = other_obstacle.pos_after_collision(self.rect, (self.x_vel, self.y_vel))
            self.y_vel *= -1

        self.rect = pygame.Rect(self.x, self.y, size, size)        


        if "bottom" in other_ground.collision(self.rect, (0, 0), self) and self.y_vel > 0:
            self.y = other_ground.pos_after_collision(self.rect, (0, 0))
            if self.standing_on_moving_ground:
                self.standing_on_moving_ground = False


        for el in other_elevators:
            if el.collision((self.x, self.y), (self.x_vel, self.y_vel)):
                self.y = el.y - size
                 
                if el.active:
                    vel_of_moving_ground = el.vel_list[el.absolute_position][0]
                    self.standing_on_moving_ground = True


        if self.x + size < 0:
            self.die()



        
        self.x_vel = 0


    def show_distance(self):
        text = distance_font.render(f"Distance: {self.distance:.1f} ", 1, BLACK)
        WIN.blit(text, distance_pos)

    def die(self):
        global new_distance
        new_distance = self.distance
        
        background_sound.fadeout(1000)
        dying_player_sound.play(loops = -1, fade_ms=2000)

        circle_center = (self.x + round(size / 2), self.y)
        circle_radius = 1500


        
        shrinking_steps = 20

        clock = pygame.time.Clock()

        while circle_radius > size / 2:
            clock.tick(60)

            for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()

            rects_around_circle = []

            for i in range(circle_center[0] - circle_radius, circle_center[0] + 1, 1):
                    
                    #oben links
                rects_around_circle.append(pygame.Rect(0, 0, i, circle_center[1] - math.sqrt(circle_radius ** 2 - (circle_center[0] - i) ** 2)))
                    #oben rechts
                rects_around_circle.append(pygame.Rect(i + circle_radius, 0, WIDTH - i - circle_radius,  circle_center[1] - math.sqrt(circle_radius ** 2 - (i - circle_center[0] + circle_radius) ** 2)))
                    #unten links
                rects_around_circle.append(pygame.Rect(0, circle_center[1] + math.sqrt(circle_radius ** 2 - (circle_center[0] - i) ** 2), i, HEIGHT - circle_center[1] + math.sqrt(circle_radius ** 2 - (circle_center[0] - i) ** 2)))
                    #unten rechts
                rects_around_circle.append(pygame.Rect(i + circle_radius, circle_center[1] + math.sqrt(circle_radius ** 2 - (i - circle_center[0] + circle_radius) ** 2), WIDTH - i - size/2, HEIGHT - circle_center[1] + math.sqrt(circle_radius ** 2 - (i - circle_center[0] + circle_radius) ** 2)))

                    
            for e in rects_around_circle:
                #WIN.fill(BROWN, e)
                pygame.draw.rect(WIN, BROWN, e)
                
            pygame.display.update()

            circle_radius -= shrinking_steps



        main()



        



def set_up():
    global ground, background, player, obstacles, button_for_elevator, elevator1, bullets, enemies, enemy_bullets, vel_of_moving_ground, elevators, vel_of_ground

    #variables

    vel_of_moving_ground = 0
    vel_of_ground = 2


    # ground
    
    ground_colors = [BLACK, RED, BLACK, RED]
    grounds_pos = [(0, 0.3 * HEIGHT), (870, 0.99 * HEIGHT), (1000, 0.85 * HEIGHT), (1970, HEIGHT - 5)]

    for i in range(1, 7):
        grounds_pos.append((1800 + i * 300, HEIGHT - 200 - i * 85))
        grounds_pos.append((1950 + i * 300, HEIGHT - 5))
        ground_colors.append(BLACK)
        ground_colors.append(RED)


    for i in range(100):
        grounds_pos.append((4500 + i * 50, HEIGHT - i * 2))
        ground_colors.append(RED)

    #obstacles

    obstacles_pos = [(400, 400)]
    obstacles_types = ["blackstar"]
    obstacles_sizes = [(35, 35)]

    for i in range(16):
        obstacles_pos.append((1000 + i * 60, 580))
        obstacles_types.append("blackstar")
        obstacles_sizes.append((50, 50))

    obstacles_pos.append((4250, 520))
    obstacles_types.append("brownblock")
    obstacles_sizes.append((150, 50))

    obstacles_pos.append((4800, 360))
    obstacles_pos.append((4800, 300))
    for i in range(5):
        obstacles_types.append("blackstar")
        obstacles_sizes.append((50, 50))
    obstacles_pos.append((5050, 380))
    obstacles_pos.append((5050, 320))
    obstacles_pos.append((5050, 260))

    for i in range(3):
        obstacles_pos.append((6600 + i * 210, 380 - (i + 1) * 70))
        obstacles_sizes.append(((i + 1) * 210, (i + 1) * 70))
        obstacles_types.append("brownblock")

    for i in range(3, 25):
        
        if i < 12 or i > 13:
            obstacles_pos.append((7500 + i * 60, 400))
            obstacles_sizes.append((50, 50))
            obstacles_types.append("blackstar")

        if i > 12:
            obstacles_pos.append((7530 + i * 60, 320))
            obstacles_sizes.append((50, 50))
            obstacles_types.append("blackstar")

        if i == 12:
            obstacles_pos.append((7500 + i * 60, 700))
            obstacles_sizes.append((500, 100))
            obstacles_types.append("brownblock")
    
    for i in range(3):
        obstacles_pos.append((9150 + i * 50, 650))
        obstacles_sizes.append((50, 50))
        obstacles_types.append("blackstar")
    for i in range(3):
        obstacles_pos.append((9600 + i * 55, 470))
        obstacles_sizes.append((50, 50))
        obstacles_types.append("blackstar")
    for i in range(3):
        obstacles_pos.append((10250 + i * 55, 355))
        obstacles_sizes.append((50, 50))
        obstacles_types.append("blackstar")


    pos_list_blackstar = [600, 550, 500, 450, 400]
    for i in range(400):
        if 1 == random.randint(1, 12):
            obstacles_pos.append((12000 + i * 300, random.choice(pos_list_blackstar)))
            obstacles_sizes.append((50, 50))
            obstacles_types.append("blackstar")


    #Enemies

    enemies = []
    enemies.append(FlyingEnemy((2000, 0.64 * HEIGHT), 80, 2, 150, 1, (50, 50)))

    for i in range(2, 7):
        enemies.append(FlyingEnemy((1850 + i * 300, HEIGHT - 260 - i * 85), 128 - 2 * i, 3, 0, 0, (45, 45)))

    enemies.append(FlyingEnemy((5400, 0.3 * HEIGHT), 160, 4, 50, 1, (50, 50)))
    enemies.append(FlyingEnemy((5800, 0.25 * HEIGHT), 160, 2, 100, 2, (75, 75)))
    enemies.append(FlyingEnemy((6200, 0.36 * HEIGHT), 160, 2, 100, 3, (100, 100)))
    enemies.append(FlyingEnemy((7600, 120), 30, 1, 10, 5, (40, 40)))

    for i in range(100):
        if 1 == random.randint(0,1):
            enemy_size = random.randint(15, 500)    
            enemies.append(FlyingEnemy((11000 + i * 300, 600), random.randint(101 - i, 256 - i * 2), 1 + i, random.randint(10, 250), random.randint(1, 12), (enemy_size, enemy_size)))
            if enemy_size < 30:
                enemies.append(FlyingEnemy((11000 + i * 300 + 50, 600), random.randint(101 - i, 256 - i * 2), 1 + i, random.randint(10, 250), random.randint(1, 12), (enemy_size, enemy_size)))
            if enemy_size < 23:
                enemies.append(FlyingEnemy((11000 + i * 300 + 100, 600), random.randint(101 - i, 256 - i * 2), 1 + i, random.randint(10, 250), random.randint(1, 12), (enemy_size, enemy_size)))

    #Elevators

    vel_list_1 = []

    for i in range(4400):
        vel_list_1.append([vel_of_ground, 0])
    for i in range(900):
        vel_list_1.append([1, -2])
    for i in range(5000):
        vel_list_1.append([0, 0])

    vel_list_2 = []
    for i in range(800):
        vel_list_2.append([vel_of_ground - 1, 0])
    for i in range(800):
        vel_list_2.append([vel_of_ground - 1, 1])
    for i in range(4000):
        vel_list_2.append([0, 0])

    vel_list_3 = []
    for i in range(500):
        vel_list_3.append([vel_of_ground - 1, 0])
    for i in range(800):
        vel_list_3.append([vel_of_ground-1, 1])
    for i in range(3000):
        vel_list_3.append([0, 0])

    vel_list_4 = []
    for i in range(850):
        vel_list_4.append([vel_of_ground - 1, 0])
    for i in range(800):
        vel_list_4.append([vel_of_ground -1, -1])
    for i in range(3000):
        vel_list_4.append([0, 0])

    vel_list_5 = []
    for i in range(5000):    
        vel_list_5.append([vel_of_ground, 0]) 


    elevator1 = Elevator(4000, 380, 150, 20, BROWN, vel_list_1)
    elevator2 = Elevator(8800, 700, 80, 15, BROWN, vel_list_2)
    elevator3 = Elevator(9250, 520, 120, 15, BROWN, vel_list_3)
    elevator4 = Elevator(9750, 400, 100, 15, BROWN, vel_list_4)
    elevator5 = Elevator(10450, 666, 250, 25, BROWN, vel_list_5)
    elevators = [elevator1, elevator2, elevator3, elevator4, elevator5]



    ground = Ground(ground_colors, grounds_pos)
    background = Background(HEIGHT, BLUE2)
    player = Player(200, HEIGHT * 0.2 - size, size, ANAKIWA, 4)
    obstacles = Obstacles(obstacles_pos, obstacles_types, obstacles_sizes)
    button_for_elevator = Button((4300, 470), 50, 50)

    bullets = []

    enemy_bullets = []



def draw_window():
    

    pygame.draw.rect(WIN, background.color, background.rect)
    

    for i in range(ground.number_of_rects):
        pygame.draw.rect(WIN, ground.colors[i], ground.rects[i])
    
    player.draw_player()

    player.show_distance()

    obstacles.draw_obstacles()

    button_for_elevator.draw_button()

    for el in elevators:
        el.draw()

    for b in bullets:
        b.draw()

    for e in enemies:
        e.draw()

    for eb in enemy_bullets:
        eb.draw()

    pygame.display.update()




def read_highscore():
    d = open("highscore.txt")
    highscore = d.readlines()
    d.close()
    return highscore[0]
    

def write_highscore(distance):
    d = open("highscore.txt", "w")
    d.write(str(distance))
    d.close()



def menu():
    start_game = False
    clock = pygame.time.Clock()
    
    old_highscore = read_highscore()
    if new_distance > int(old_highscore):
        highscore_text = highscore_font.render(f"Best Distance: {new_distance:.0f} ", True, RED)
        write_highscore(f"{new_distance:.0f}")
    else:
        highscore_text = highscore_font.render("Best Distance: " + str(old_highscore), True, RED)

    distance_text = highscore_font.render(f"Distance: {new_distance:.0f} ", True, RED)

    while not start_game:
        clock.tick(FPS)
        
        WIN.fill(BROWN)
        WIN.blit(play_button_text, (play_button_rect.x, play_button_rect.y))
        draw.rect(WIN, RED, play_button_rect, 3)
        WIN.blit(controls_img, (100, 150))
        WIN.blit(highscore_text, (WIDTH - 600, 100))
        if new_distance > 0:
            WIN.blit(distance_text, (WIDTH / 2 - distance_text.get_width()/2, 275))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    dying_player_sound.fadeout(3000)
                    start_game = True




def main():
    global vel_of_ground

    menu()
    set_up()
    clock = pygame.time.Clock()
    run = True
    background_sound.play(-1, fade_ms=1000)
    while run:
        clock.tick(FPS)

        elevators_collision = False
        for el in elevators:
            if el.collision((player.x, player.y), (player.x_vel, player.y_vel)):
                elevators_collision = True
                break
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE and ("bottom" in ground.collision(player.rect, (player.x_vel, player.y_vel), player) or "bottom" in obstacles.collision(player.rect, (player.x_vel, 0), player) or elevators_collision):
                    player.jump()

                if event.key == pygame.K_w:
                    bullets.append(Bullet(player.shoot()))



        keys_pressed = pygame.key.get_pressed()
        player.change_vel(keys_pressed)

        elevators_collision = False
        for el in elevators:
            if el.collision((player.x, player.y), (player.x_vel, player.y_vel)):
                elevators_collision = True
                break

        if "bottom" not in ground.collision(player.rect, (player.x_vel, player.y_vel), player) and not elevators_collision and not obstacles.collision(player.rect, (player.x_vel, player.y_vel), player):
            player.fall()
        else:
            player.y_vel = 0

        ground.move_ground(vel_of_ground)
        obstacles.move()
        button_for_elevator.move()
        button_for_elevator.check_for_player(player)
        
        if button_for_elevator.active:
            elevators[0].active = True
            #vel_of_moving_ground = 2
        else:
            elevators[0].active = False

        if player.distance >= 83:
            elevators[1].active = True
        else:
            elevators[1].active = False

        if player.distance > 89.5:
            elevators[2].active = True
        
        if player.distance > 95:
            elevators[3].active = True
        
        if player.distance > 103.5:
            elevators[4].active = True

        if player.distance > 120 and len(elevators) > 4:
            for i in range(4):
                del elevators[i]
        
        if player.distance == 444:
            player.die()



        for b in bullets:
            b.move()

            for e in enemies:
                if b.collision((e.x, e.y, e.size[0], e.size[1])):
                    dying_enemy_sound.play()
                    enemies.remove(e)
                    bullets.remove(b)
                    
        for b in bullets:
            if b.x > WIDTH:
                bullets.remove(b)

        for eb in enemy_bullets:
            eb.move()

            if eb.collision((player.x, player.y, size, size)):
                player.die()
        
        for e in enemies:
            if e.collision((player.x, player.y)):
                player.die()

        for el in elevators:
            el.move(player.distance)

        #print(f"x: {player.x}, y: {player.y}, vel({player.x_vel}, {player.y_vel} ) ")
        player.move(ground, elevators, obstacles)
        player.distance += vel_of_ground/100

        for enemy in enemies:
            enemy.move()
            shot = enemy.shoot((player.x, player.y))
            if shot:
                enemy_bullets.append(Bullet(shot[0], shot[1]))

        draw_window()



    pygame.quit()


if __name__ == '__main__':
    main()