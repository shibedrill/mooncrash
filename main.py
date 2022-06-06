#!/usr/bin/python
import sys
import pygame, time, math

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
    rot = 0
    thrust = 0.4
    fuel = 100

# Define an object to define the ground
class ground:
    # An array of points which makes up the ground
    # Each point is an (x, y) tuple which gives the offset
    # of the point from the center of the object.
    # Also having each point in the vector makes it easier to
    # get the rect of every point and calculate landings.
    points = []

# Begin defining physics variables
grav = 0.1 * (0 - 9.8) # Acceleration due to gravity, in meters/second/second

class gui:
    fuel = font.render((f"Fuel: {(math.trunc(ship.fuel))}%"), True, green, blue)

# Shamelessly stolen function to rotate the ship
def rotate(point):
    ox, oy = ship.xpos, ship.ypos
    px, py = point

    qx = ox + math.cos(math.radians(ship.rot)) * (px - ox) - math.sin(math.radians(ship.rot)) * (py - oy)
    qy = oy + math.sin(math.radians(ship.rot)) * (px - ox) + math.cos(math.radians(ship.rot)) * (py - oy)
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
    display.blit(gui.fuel, (20, 20))

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
                # REMEMBER: Implement needed math to change both
                # X and Y velocity with regards to direction.
                # math.tangent(ship.rot) is equal to the rise over the run.
                # Now comes the question: How do we find the individual rise and run?
                # We know that the change in X velocity plus the change in Y velocity
                # should be equal to the thrust...
                # DO THIS STUFF ON PAPER. FIGURE IT OUT.
                # ----------------------------------------------------------------------
                ship.yvel += ship.thrust
                ship.fuel -= 0.2

    # Let the forces of nature do their things
    ship.yvel += (grav/fps)
    ship.ypos -= ship.yvel
    clock.tick(fps)