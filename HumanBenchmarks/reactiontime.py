import pygame
import sys
import random
import time
import statistics



pygame.init()

WIDTH, HEIGHT = 1080, 720

WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Reaction Time")


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (195, 0, 82)

FPS = 75

start = False
change_color = False
played_rounds = 0
too_early = False

starting_times_list = []
real_starting_times_list = []
ending_times_list = []



def draw_text(text, pos, size, color, font_style):
    text_font = pygame.font.SysFont(font_style, size)
    surface = text_font.render(text, 1, color)

    WIN.blit(surface, pos)



def ending():
    WIN.fill(BLACK)
    averaged_time = 0
    for i in range(4):
        averaged_time += (ending_times_list[i] - real_starting_times_list[i])

    averaged_time *= 0.2

    averaged_time = statistics.mean(ending_times_list) - statistics.mean(real_starting_times_list)


    final_times = []

    for f in range(4):
        final_times.append(ending_times_list[f] - real_starting_times_list[f])
    
    final_times.sort()

    draw_text(f"Averaged time: {averaged_time:.3f} ", (200, 200), 70, PINK, 'calibri')
    draw_text(f"Fastest time: {final_times[0]:.3f}", (230, 350), 70, PINK, 'calibri')




def draw_window():
    WIN.fill(BLACK)

    if not start:
        draw_text("Click to start", (390, 300), 60, PINK, 'calibri')

        if too_early:
            draw_text("Clicked too early", (340, 230), 60, PINK, 'calibri')

        if played_rounds > 0:
            draw_text(f"{(ending_times_list[-1] - real_starting_times_list[-1]):.3f} ", (400, 150), 120, PINK, 'calibri')


    
    if start:
        draw_text("Click when color changes", (240, 300), 60, PINK, 'calibri')
        if change_color:
            WIN.fill(PINK)


    if played_rounds == 5:
        ending()



    pygame.display.update()



def main():

    global start
    global change_color
    global too_early
    global played_rounds

    clock=pygame.time.Clock()
    run=True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not start:
                    start = True
                    too_early = False
                    starting_times_list.append(time.time())
                    break

                if start:
                    if change_color:
                        ending_times_list.append(time.time())
                        change_color = False
                        start = False
                        played_rounds += 1
                        break
                    if not change_color:
                        start = False
                        too_early = True
                    
            
        if start and not change_color:
            if time.time() - starting_times_list[-1] > 1.5:
                if 1 == random.randint(1, 200):
                    real_starting_times_list.append(time.time())
                    change_color = True



        draw_window()


    pygame.quit()




if __name__ =="__main__":
    main()
