#!/usr/bin/python
import pygame, time, math, sys, random

# Define screen dimensions
screenx = 500
screeny = 500
screensize = (screenx, screeny)
pygame.display.set_mode(size = (screensize))
display = pygame.display.get_surface()
pygame.key.set_repeat(100, 100)
pygame.display.set_caption("Mooncrash!")
pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 12)

# Define colors and stuff
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)

# Init
pygame.init()
clock = pygame.time.Clock()
fps = 60

# Define an object to use as our Ship
class ship:
    xpos = 250
    ypos = 250
    xvel = 0
    yvel = 0
    rot = 90
    unitcircle = 0
    thrust = 20
    fuel = 100
    mass = 5
    rect = ()
    engine = False
    # Draw the ship!
    def draw():
        if ship.engine == True:
            A = rotate((ship.xpos, (ship.ypos + 10)))
            B = rotate(((ship.xpos - 2), ship.ypos))
            C = rotate(((ship.xpos + 2), ship.ypos))
            pygame.draw.aalines(display, red, True, (A, B, C), blend=1)
        # Make 3 points to draw the VISUAL representation of the ship.
        # This involves rotating these points about the origin (the ship's true position)
        # by the amount specified in ship.rot .
        shipbow = rotate((ship.xpos, (ship.ypos - 20)))
        shipport = rotate(((ship.xpos - 6), ship.ypos))
        shipstarboard = rotate(((ship.xpos + 6), ship.ypos))
        ship.rect = pygame.draw.aalines(display, white, True, (shipbow, shipport, shipstarboard), blend=1)


# Define an object to define the ground
class ground:
    # An array of points which makes up the ground
    # Each point is an (x, y) tuple which gives the offset
    # of the point from the center of the object.
    # Also having each point in the vector makes it easier to
    # get the rect of every line and calculate landings.
    points = []
    rects = []
    def populate_ground_array():
        pointpos = 500
        while len(ground.points) < 20:
            point = ((random.randint(-3, 3) + pointpos), (random.randint(-15, 15) + (screeny - (screeny * 0.1))))
            ground.points.append(point)
            pointpos -= 30
    def draw():
        pointindex = 0
        while pointindex < len(ground.points) - 1:
            ground.rects.append(pygame.draw.aaline(display, blue, ground.points[pointindex], ground.points[pointindex + 1], blend = 1))
            pointindex += 1

# Begin defining physics variables
grav = (0 - 9.8) # Acceleration due to gravity, in meters/second/second

class gui:
    def draw():
        fuel = font.render((f"Fuel: {(math.trunc(ship.fuel))}%"), True, white, black)
        display.blit(fuel, (400, 250))

# Shamelessly stolen function to rotate the ship
def rotate(point):
    ox, oy = ship.xpos, ship.ypos
    px, py = point

    qx = ox + math.cos(math.radians(ship.rot-90)) * (px - ox) - math.sin(math.radians(ship.rot-90)) * (py - oy)
    qy = oy + math.sin(math.radians(ship.rot-90)) * (px - ox) + math.cos(math.radians(ship.rot-90)) * (py - oy)
    return qx, qy

# Function to update screen
def drawscreen():
    display.fill(black)
    ship.draw()
    gui.draw()
    ground.draw()
    pygame.display.flip()

ground.populate_ground_array()
for p in ground.points:
    print(p)

# Main loop
while True:
    # Update screen
    drawscreen()
    # Pump events from queue
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] == False:
                ship.engine = False
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                ship.rot -= 5
            if keys[pygame.K_RIGHT]:
                ship.rot += 5
            if keys[pygame.K_UP] and ship.fuel > 0:
                ship.engine = True
                ship.fuel -= 0.3
                ship.unitcircle = ship.rot%360
                if 360 > ship.rot > 270 or 0 > ship.rot:
                    ship.unitcircle = 360 - ship.unitcircle
                    ship.xvel -= (math.cos(math.radians(ship.unitcircle)) * ship.thrust)
                    ship.yvel -= (math.sin(math.radians(ship.unitcircle)) * ship.thrust)
                elif 270 > ship.rot > 180:
                    ship.unitcircle -= 180
                    ship.xvel += (math.cos(math.radians(ship.unitcircle)) * ship.thrust)
                    ship.yvel -= (math.sin(math.radians(ship.unitcircle)) * ship.thrust)
                elif 180 > ship.rot > 90:
                    ship.unitcircle = 180 - ship.unitcircle
                    ship.xvel += (math.cos(math.radians(ship.unitcircle)) * ship.thrust)
                    ship.yvel += (math.sin(math.radians(ship.unitcircle)) * ship.thrust) 
                elif 90 > ship.rot > 0:
                    ship.unitcircle = ship.unitcircle
                    ship.xvel -= (math.cos(math.radians(ship.unitcircle)) * ship.thrust)
                    ship.yvel += (math.sin(math.radians(ship.unitcircle)) * ship.thrust)
                elif ship.rot == 90:
                    ship.yvel += (math.sin(math.radians(ship.unitcircle)) * ship.thrust)
                #print(ship.rot, ship.unitcircle, ship.xvel, ship.yvel)
                
    # Let the forces of nature do their things
    collide = False
    # Put collision logic here. The old stuff sucked.
    if collide == False:
        ship.yvel += ((grav * ship.mass)/fps)
        ship.ypos -= (ship.yvel/fps)
        ship.xpos += (ship.xvel/fps)
    #print("X: ", ship.xvel)
    clock.tick(fps)
