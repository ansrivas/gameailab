""" A few global constants used everywhere in the program """

# Resolution of the screen, Screen_Width, Screen_Height
RESOLUTION = SCREEN_W, SCREEN_H = (1280, 720)

NO_VOL, LOW_VOL, MED_VOL, HIGH_VOL, FULL_VOL = 0, 0.2, 0.5, 0.8, 1

# Set number of stars to appear in background
numStars = 100

# Ring Radius
RADIUS = 320
RING_CENTER = SCREEN_W/2, SCREEN_H/2

# Initial number of balls that game starts with
TOTAL_BALLS = 50

DEFAULT_BAT_SPEED = 1
DEFAULT_BALL_SPEED = 2
# Increase Angle
DEFAULT_INCREASE_ANGLE = 2

#A few RGB color values
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 255, 255)
RED = (255, 0, 0)
SNOW = (205, 201, 201)
PALEGREEN = (152, 251, 152)

RUNNING, STOPPED, PAUSED, RESET, MANUAL, AUTO = 1, 2, 3, 4, 5, 6