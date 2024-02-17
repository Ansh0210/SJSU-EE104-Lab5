# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 21:54:08 2022

@author: chris.pham
@modified: Shivansh Shukla
"""

# Import necessary libraries
import pgzrun
import pygame
import pgzero
import random
from pgzero.builtins import Actor
from random import randint

#Declare constants
FONT_COLOR = (255, 255, 255)
WIDTH = 800 # width of window
HEIGHT = 600 # height of window
CENTER_X = WIDTH / 2 # x-cord of the center of screen
CENTER_Y = HEIGHT / 2 # y-cord of the center of screen
CENTER = (CENTER_X, CENTER_Y) # center point of the screen
FINAL_LEVEL = 6 # final level of the game
START_SPEED = 8 # initial speed for the stars 
COLORS = ["green", "blue"] # possible color of stars

#Declare global variables
game_over = False # track if game is over
game_complete = False # track if game is won
game_intro = True # track if on intro screen
current_level = 1 # track the level

#Keep track of the stars on the screen
stars = []
animations = []

#Draw the stars
def draw():
    global stars, current_level, game_over, game_complete, game_intro
    screen.clear()
    screen.blit("space", (0,0)) #add a background image to the game window
    if game_over:
        display_message("GAME OVER!", "Press 'Space' to Try Again!")
    elif game_complete:
        display_message("YOU WON!", "Well done!", "Press 'Space' to Play Again!")
    elif game_intro:
        display_message("Welcome to Red Alerts!", "Press 'Space' to Start the Game")
    else:
        for star in stars: # draw stars on screen
            star.draw()

#update the game state
def update():
    global stars
    global game_over, game_complete, current_level, game_intro
    
    if game_intro: 
        if keyboard.space:
            game_intro = False
            stars = make_stars(current_level) #starts the game when spacebar is pressed
    else:
        if len(stars) == 0:
            stars = make_stars(current_level) #generate stars for curr level if none left
            
        if (game_complete or game_over) and keyboard.space:
            stars = [] # clear stars 
            current_level = 1 # reset level
            game_complete = False # reset game state
            game_over = False # reset game state

# create stars for the curr level
def make_stars(number_of_extra_stars):
    colors_to_create = get_colors_to_create(number_of_extra_stars) # determine color of stars
    new_stars = create_stars(colors_to_create) # create star actor objects
    layout_stars(new_stars) # position stars on screen
    animate_stars(new_stars) # animates the stars
    return new_stars

# determine colors of stars to create for the level
def get_colors_to_create(number_of_extra_stars):
    colors_to_create = ["red"] #start with red star
    for i in range(0, number_of_extra_stars):
        random_color = random.choice(COLORS) # choose a random color for options
        colors_to_create.append(random_color) # add the color to list
    return colors_to_create

# create star actors with specified colors
def create_stars(colors_to_create):
    new_stars = [] # stores created stars
    for color in colors_to_create: 
        star = Actor("snowflake-" + color) # create star actor with specified image 
        new_stars.append(star) # add star to the list
    return new_stars

# layout the stars on screen
def layout_stars(stars_to_layout):
    number_of_gaps = len(stars_to_layout) + 1 # calc num of gaps between stars
    gap_size = WIDTH / number_of_gaps # calc size of each gap
    random.shuffle(stars_to_layout) # shuffle the list 
    for index, star in enumerate(stars_to_layout):
        new_x_pos = (index + 1) * gap_size # new x pos each star
        star.x = new_x_pos # set x cord
        if index%2 == 0:
            star.y = 0 # place stars on top of screen 
        else:
            star.y = HEIGHT # place stars on bottom of screen 

# animate the stars movement
def animate_stars(stars_to_animate):    
    for star in stars_to_animate:
        rand_speed_adj = randint(0, 2) # random speed adjustment for each star
        duration = START_SPEED - current_level + rand_speed_adj # animation duration
        
        if star.y == 0:
            star.anchor = ("center", "bottom")
            rand_dir = HEIGHT # set y cord where the star will move to
        elif star.y == HEIGHT:
            star.anchor = ("center", "top") # anchor point for stars on bottom
            rand_dir = 0 # set y cord where the star will move to

        #star.anchor = ("center", "bottom")
        #rand_dir = random.choice((0, HEIGHT))
        animation = animate(star, duration=duration, on_finished=handle_game_over, y=rand_dir)
        animations.append(animation) # start animation and add to list

# handle the game over state    
def handle_game_over():
    global game_over 
    game_over = True  
    
# handle mouse click events on screen
def on_mouse_down(pos):
    global stars, current_level
    for star in stars:
        if star.collidepoint(pos):
            if "red" in star.image: # if red star is clicked, handle that event
                red_star_click()
            else:
                handle_game_over() # otherwise handle game over when clicked on other stars

# handle click on red stars
def red_star_click():
    global current_level, stars, animations, game_complete 
    stop_animations(animations) # stops animations 
    if current_level == FINAL_LEVEL:
        game_complete = True # if the final level is reached, game is completed
    else:
        current_level = current_level + 1 #move to next level
        stars = [] # clear the stars for new level
        animations = [] # clear animations for new level

# stop star animations     
def stop_animations(animations_to_stop):
    for animation in animations_to_stop:
        if animation.running:
            animation.stop()
            
# display game messages
def display_message(heading_text, sub_heading_text, third_text=''):
    screen.draw.text(heading_text, fontsize=60, center=CENTER, color=FONT_COLOR) # display large heading
    screen.draw.text(sub_heading_text,fontsize=30, center=(CENTER_X, CENTER_Y+30), color=FONT_COLOR) # sub heading
    screen.draw.text(third_text, fontsize=25, center=(CENTER_X, CENTER_Y+60), color=FONT_COLOR) #third heading

# shuffle the stars position peridically
def shuffle():
    global stars
    if stars:
        x_values = [star.x for star in stars] # get x cord of all stars
        random.shuffle(x_values) # shuffle the x cords
        for index, star in enumerate(stars):
            new_x = x_values[index] # get new x cord for each star
            animation = animate(star, duration=0.2, x=new_x) # animate stars to new pos
            animations.append(animation)
            
# schedule the shuffle function every 1 sec
clock.schedule_interval(shuffle, 1)
        
pgzrun.go()