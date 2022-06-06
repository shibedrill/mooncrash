#!/usr/bin/python
import pygame, time, math, sys

# Define screen dimensions
screenx = 500
screeny = 500
screensize = (screenx, screeny)
pygame.display.set_mode(size = (screensize))
display = pygame.display.get_surface()
pygame.key.set_repeat(100, 100)
pygame.display.set_caption("Mooncrash!")
pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 32)

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

# Function to update screen
def drawscreen():
    display.fill(black)
    drawship()
    drawgui()

# Define an object to use as our Ship
class ship:
    xpos = 250
    ypos = 250
    xvel = 0
    yvel = 0
    rot = 90
    unitcircle = 0
    thrust = 5
    fuel = 100

# Define an object to define the ground
class ground:
    # An array of points which makes up the ground
    # Each point is an (x, y) tuple which gives the offset
    # of the point from the center of the object.
    # Also having each point in the vector makes it easier to
    # get the rect of every line and calculate landings.
    points = []

# Begin defining physics variables
grav = (0 - 9.8) # Acceleration due to gravity, in meters/second/second

class gui:
    fuel = font.render((f"Fuel: {(math.trunc(ship.fuel))}%"), True, white, white)

# Shamelessly stolen function to rotate the ship
def rotate(point):
    ox, oy = ship.xpos, ship.ypos
    px, py = point

    qx = ox + math.cos(math.radians(ship.rot-90)) * (px - ox) - math.sin(math.radians(ship.rot-90)) * (py - oy)
    qy = oy + math.sin(math.radians(ship.rot-90)) * (px - ox) + math.cos(math.radians(ship.rot-90)) * (py - oy)
    return qx, qy

# Draw the ship!
def drawship():
    # Make 3 points to draw the VISUAL representation of the ship.
    # This involves rotating these points about the origin (the ship's true position)
    # by the amount specified in ship.rot .
    shipbow = rotate((ship.xpos, (ship.ypos - 20)))
    shipport = rotate(((ship.xpos - 6), ship.ypos))
    shipstarboard = rotate(((ship.xpos + 6), ship.ypos))
    pygame.draw.aalines(display, white, True, (shipbow, shipport, shipstarboard), blend=1)
    pygame.display.flip()

def drawgui():
    # This doesn't show up for some godforsaken reason
    display.blit(gui.fuel, (250, 250))

# Main loop
while True:
    # Update screen
    drawscreen()
    # Pump events from queue
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                ship.rot -= 5
            if keys[pygame.K_RIGHT]:
                ship.rot += 5
            if keys[pygame.K_UP] and ship.fuel > 0:
                # TO DO: Somewhere in here, something is not working.
                # I don't think value signs are being respected.

                # What we wanna do first is get a reference angle.
                ship.unitcircle = ship.rot%180
                if ship.unitcircle > 90 :
                    ship.unitcircle = 180 - ship.unitcircle
                # Now we have a reference angle!! Woo!! The most difficult part is done.
                # ship.unitcircle is now our reference angle, so:
                # sin(ship.unitcircle) = (Increase in vel (Y)) / Thrust
                # cos(ship.unitcircle) = (Increase in vel (X)) / Thrust
                # Which means if we simply multiply these results by the Thrust value,
                # we get our vector components!!

                # I think the bug is here.
                # The ship seemingly chooses a random direction in the X axis
                # and refuses to go the other way.
                ship.yvel -= ((math.cos((ship.unitcircle))) * ship.thrust)
                ship.xvel -= ((math.sin((ship.unitcircle-90))) * ship.thrust)
                print(ship.rot, ship.xvel, ship.yvel)
                ship.fuel -= 0.2

    # Let the forces of nature do their things
    ship.yvel += (grav/fps)
    ship.ypos -= (ship.yvel/fps)
    ship.xpos += (ship.xvel/fps)
    #print("X: ", ship.xvel)
    clock.tick(fps)