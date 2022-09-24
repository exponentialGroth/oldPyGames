import pygame
import random

from pygame import time
pygame.init()

WIDTH, HEIGHT = 720, 480
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chimpanse")

#colors

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (195, 0, 82)


FPS = 60
level = 3
lives = 3
status_choose_coords = True
active = False
clicked_numbers = []

numbers_font = pygame.font.SysFont('arial', 33)
anzeigen_font = pygame.font.SysFont('arial', 30)
looser_font = pygame.font.SysFont("arial", 55)

timer_rect = pygame.Rect(WIDTH * 0.75 - 62, 5, 200, 30)
level_rect = pygame.Rect(WIDTH * 0.5 - 53, 5, 200, 30)
lives_rect = pygame.Rect(WIDTH * 0.25 - 52, 5, 200, 30)


def choose_coordinates(number):
    possible_coordinates = []
    boxes_dict = {}
    for x in range(40, WIDTH - 40, 40):
        for y in range(80, HEIGHT - 40, 40):
            possible_coordinates.append((x, y))

    for i in range(1, number + 1):
        boxes_dict[i] = random.choice(possible_coordinates)
        possible_coordinates.remove((boxes_dict[i]))

    return boxes_dict



def produce_boxes(number_of_numbers, boxes):

    for i in range(1, number_of_numbers + 1):
        coordinates = boxes[i]
        box_rect = pygame.Rect(coordinates[0], coordinates[1], 40, 40)
        pygame.draw.rect(WIN, PINK, box_rect)
        pygame.draw.rect(WIN, BLACK, box_rect, 1)
        number_text = numbers_font.render(str(i), 1, WHITE)
        WIN.blit(number_text, (box_rect.x + 40/2 - number_text.get_width()/2, box_rect.y + 40/2 - number_text.get_height()/2))


def hide_numbers(boxes):


    for coord in coordinates_dict.values():
        box_rect = pygame.Rect(coord[0], coord[1], 40, 40)
        pygame.draw.rect(WIN, PINK, box_rect)






def timer(seconds):
    
    while seconds > 0:
        WIN.fill(BLACK, timer_rect)
        time_text = anzeigen_font.render(str(f"Time: {seconds:.1f}"), 1, PINK)

        WIN.blit(time_text, (timer_rect.x, timer_rect.y))
        pygame.display.update(timer_rect)
        seconds -= 1/10
        time.wait(100)

 

def looser():
    WIN.fill(BLACK)
    looser_text = looser_font.render(f"Du hast {level} Levels geschafft", 1, PINK)
    WIN.blit(looser_text, (WIDTH/2 - looser_text.get_width()/2, HEIGHT/2 - looser_text.get_height()/2))
    pygame.display.update()
    time.wait(3000)
    return False




def draw_window():
    global status_choose_coords
    global coordinates_dict
   
    WIN.fill(BLACK)


    if status_choose_coords:
        coordinates_dict = choose_coordinates(level)  
        status_choose_coords = False

    produce_boxes(level, coordinates_dict)

    if active:
        hide_numbers(level)

    for number in clicked_numbers:
        number_surface = numbers_font.render(str(number), 1, WHITE)
        WIN.blit(number_surface, (coordinates_dict[number][0] + 40/2 - number_surface.get_width()/2, coordinates_dict[number][1] + 40/2 - number_surface.get_height()/2))


    level_text = anzeigen_font.render("Level: " + str(level), 1, PINK)
    WIN.blit(level_text, (level_rect.x, level_rect.y))

    lives_text = anzeigen_font.render("Lives: " + str(lives), 1, PINK)
    WIN.blit(lives_text, (lives_rect.x, lives_rect.y))

    pygame.display.update()




def main():
    global level
    global active
    global status_choose_coords
    global clicked_numbers
    global lives

    clock = pygame.time.Clock()
    run = True
    while run:
        draw_window()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(1, level + 1):
                    if i not in clicked_numbers:
                        correct_rect = pygame.Rect(coordinates_dict[i][0],coordinates_dict[i][1], 40, 40 )
                        correct_number = i
                        
                        break
                
                if correct_rect.collidepoint(event.pos):
                    clicked_numbers.append(correct_number)
                
                else:
                    lives -= 1
                    if lives == 0:
                        run = looser()




        if not active:
            timer(level * 2)
            active = True
            clicked_numbers = []

        try:
            if level == clicked_numbers[-1]:
                level += 1
                status_choose_coords = True
                active = False

        except:
            pass


        

    pygame.quit()




if __name__ == '__main__':
    main()