#####       THIS JUST A RAW FILE GAME       #####
#####       THIS JUST A RAW FILE GAME       #####
#####       THIS JUST A RAW FILE GAME       #####



#LIBS
import pygame
import sys
import random
import numpy as np


pygame.init()
my_font = pygame.font.Font('04B_19.ttf',40)
my_screen = pygame.display.set_mode((950,500))
background = pygame.image.load('assets/background.png').convert_alpha()


#BIRDS VARIABLES
bird_mid_flap = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
bird_down_flap = pygame.image.load('assets/yellowbird-downflap.png').convert_alpha()
bird_up_flap = pygame.image.load('assets/yellowbird-upflap.png').convert_alpha()
bird_pics = [bird_down_flap, bird_mid_flap, bird_up_flap]
bird_index = 0
bird_movement = 0
bird = bird_pics[bird_index]
bird_x = 200
bird_y = 250
bird_collider = bird.get_rect(center=(bird_x,bird_y))
bird_height = bird.get_height()
bird_width = bird.get_width()



# BIRD ACTIONS
def rotate_bird(bird):
	rotated_bird = pygame.transform.rotozoom(bird,-bird_movement*3,1)
	return rotated_bird


def bird_animation():
	new_bird = bird_pics[bird_index]
	new_bird_collider = new_bird.get_rect(center = (bird_x,bird_collider.centery))
	return new_bird, new_bird_collider


def check_collision(pipes):
	for pipe in pipes:
		if bird_collider.colliderect(pipe): 
			return False
	if bird_collider.top <= -150 or bird_collider.bottom >= 450:
		return False
	return True


#PIPES VARIABLES
pipe_img = pygame.image.load('assets/pipe-red.png').convert_alpha()
top_pipe_img = pygame.transform.flip(pipe_img, False, True)
bottom_pipe_img = pipe_img
pipe_height = pipe_img.get_height()
pipe_width = pipe_img.get_width()
pipe_list = []


# PIPE ACTIONS
def get_pipe():
	gap = 175
	random_height = random.randrange(-250,-50)
	top_pipe = pipe_img.get_rect(midtop =(1200, random_height))
	bottom_pipe = pipe_img.get_rect(midbottom =(1200, 950 + random_height - gap))
	return top_pipe, bottom_pipe


def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx -= 4
	return pipes 


def draw_pipes(pipes):
	for pipe in pipes:
		if(pipe.bottom <= 500):
		#my_screen.blit(top_pipe_img,pipe)
			my_screen.blit(top_pipe_img,pipe)
		else:
			my_screen.blit(bottom_pipe_img,pipe)


def remove_pipe(pipes):
	for pipe in pipes:
		if (pipe.centerx < -100):
			pipes.remove(pipe)


#FLOOR VARIABLES
floor = pygame.image.load('assets/floor.png').convert_alpha()
floor_width = floor.get_width()
x_floor_pos = 0


# OTHER VARIABLES
clock = pygame.time.Clock()
FPS = 120
gravity = 0.2
game_active = True
score = 0 


# EVENTS
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 800)


# SCORE
def show_score():
	score_surface = my_font.render('Score: ' + str(int(score)), True, (255,255,255))
	score_rect = score_surface.get_rect(center= (475, 50))
	my_screen.blit(score_surface,score_rect)


while True:
	
	for event in pygame.event.get():

		#  QUIT GAME
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:

			# FLY WITH SPACE
			if event.key == pygame.K_SPACE:
				bird_movement = 0
				bird_movement -= 5.5

		if event.type == SPAWNPIPE:
			pipe_list.extend(get_pipe())
		if event.type == BIRDFLAP:
			if bird_index < 2:
				bird_index += 1
			else:
				bird_index = 0

			bird,bird_collider = bird_animation()



	# SET SCREEN
	my_screen.blit(background,(0,0))
	my_screen.blit(floor,(0,450))

	if game_active == False:
		score=0
		bird_x = 200
		bird_y = 250
		bird_collider.center = (bird_x,bird_y)
		pipe_list.clear()
		game_active = True
	else:
		# BIRD 
		bird_movement += gravity
		bird_collider.centery += bird_movement
		new_bird = rotate_bird(bird)
		my_screen.blit(new_bird,bird_collider)
		game_active = check_collision(pipe_list)


		# PIPES
		move_pipes(pipe_list)
		draw_pipes(pipe_list)


		# SCORES
		score+=0.01
		show_score()
		x_floor_pos -= 3
		#  MAKE FLOOR MOVE
		my_screen.blit(floor,(x_floor_pos,450))
		my_screen.blit(floor,(x_floor_pos+floor_width,450))
		if (x_floor_pos<=-950):
			x_floor_pos=0


	pygame.display.update()
	clock.tick(FPS)



pygame.quit()
