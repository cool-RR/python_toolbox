import nibmaster

import pygame, sys,os
from pygame.locals import * 
 
pygame.init() 
 
window = pygame.display.set_mode((600, 600)) 
pygame.display.set_caption('Snail Fever') 
screen = pygame.display.get_surface() 

snail_head_file_name = "snail.gif"

snail_surface = pygame.image.load(snail_head_file_name)

screen.blit(snail_surface, (100,100)) 
pygame.display.flip() 
 
def input(events): 
   for event in events: 
      if event.type == QUIT: 
         sys.exit(0) 
      else: 
         #print event 
         pass
 
while True: 
   input(pygame.event.get()) 
   pass
