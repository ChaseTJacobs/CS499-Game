import pygame
from pygame.locals import *
from sys import exit
pygame.init()

screen = pygame.display.set_mode((640, 480), 0, 32)

color1 = (221, 99, 20)
color2 = (96, 130, 51)
factor = 0.
# #This is the code for Blending Colors by Lerping
# def blend_color(color1, color2, blend_factor):
#     red1, green1, blue1 = color1
#     red2, green2, blue2 = color2
#     red = red1+(red2-red1)*blend_factor
#     green = green1+(green2-green1)*blend_factor
#     blue = blue1+(blue2-blue1)*blend_factor
#     return int(red), int(green), int(blue)
# while True:
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             exit()
#     screen.fill((255, 255, 255))
#     tri = [ (0,120), (639,100), (639, 140) ]
#     pygame.draw.polygon(screen, (0,255,0), tri)
#     pygame.draw.circle(screen, (0,0,0), (int(factor*639.), 120), 10)
#     x, y = pygame.mouse.get_pos()
#     if pygame.mouse.get_pressed()[0]:
#         factor = x / 639.
#         pygame.display.set_caption("PyGame Color Blend Test - %.3f"%factor)
#     color = blend_color(color1, color2, factor)
#     pygame.draw.rect(screen, color, (0, 240, 640, 240))
#     pygame.display.update()


#This is the code for the Color Sliders
#Creates images with smooth gradients
def create_scales(height):
    red_scale_surface = pygame.surface.Surface((640, height))
    green_scale_surface = pygame.surface.Surface((640, height))
    blue_scale_surface = pygame.surface.Surface((640, height))
    for x in range(640):
        c = int((x/639.)*255.)
        red = (c, 0, 0)
        green = (0, c, 0)
        blue = (0, 0, c)
        line_rect = Rect(x, 0, 1, height)
        pygame.draw.rect(red_scale_surface, red, line_rect)
        pygame.draw.rect(green_scale_surface, green, line_rect)
        pygame.draw.rect(blue_scale_surface, blue, line_rect)
    return red_scale_surface, green_scale_surface, blue_scale_surface
red_scale, green_scale, blue_scale = create_scales(80)
color = [127, 127, 127]
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    screen.fill((0, 0, 0))
    # Draw the scales to the screen
    screen.blit(red_scale, (0, 00))
    screen.blit(green_scale, (0, 80))
    screen.blit(blue_scale, (0, 160))
    x, y = pygame.mouse.get_pos()
    # If the mouse was pressed on one of the sliders, adjust the color component
    if pygame.mouse.get_pressed()[0]:
        for component in range(3):
            if y > component*80 and y < (component+1)*80:
                color[component] = int((x/639.)*255.)
        pygame.display.set_caption("PyGame Color Test - "+str(tuple(color)))

    # Draw a circle for each slider to represent the current setting
    for component in range(3):
        pos = ( int((color[component]/255.)*639), component*80+40 )
        pygame.draw.circle(screen, (255, 255, 255), pos, 20)
    pygame.draw.rect(screen, tuple(color), (0, 240, 640, 240))
    pygame.display.update()
def scale_color(color, scale):
    red, green, blue = color
    red = int(red*scale)
    green = int(green*scale)
    blue = int(blue*scale)
    return red, green, blue

fireball_orange = (221, 99, 20)
print (fireball_orange)
print (scale_color(fireball_orange, .5))
print (scale_color(fireball_orange, 2.))
def saturate_color(color):
    red, green, blue = color
    red = min(red, 255)
    green = min(green, 255)
    blue = min(blue, 255)
    return red, green, blue
