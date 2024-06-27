import pygame as pg

# Initialize Pygame
pg.init()

# Set up the screen
WIDTH, HEIGHT = 400, 400
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Move Points and Connect with Line")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Points initialization
NUM_POINTS = 3
points = [(WIDTH // 4 * i + WIDTH // 8, HEIGHT // 2) for i in range(1, NUM_POINTS + 1)]
labels = ["Attack", "Decay", "Sustain"]

# Function to draw points
def draw_points(screen, points):
    for point in points:
        pg.draw.circle(screen, BLACK, point, 5)

# Function to draw connecting line
def draw_line(screen, points):
    pg.draw.lines(screen, BLACK, False, [(0, HEIGHT)] + points + [(WIDTH, HEIGHT)], 2)

# Function to fill areas under the line
def fill_areas(screen, points):
    # Define the areas with corresponding colors
    areas = [
        ([ (0, HEIGHT), points[0], (points[0][0], HEIGHT) ], RED),
        ([ points[0], points[1], (points[1][0], HEIGHT), (points[0][0], HEIGHT) ], ORANGE),
        ([ points[1], points[2], (points[2][0], HEIGHT), (points[1][0], HEIGHT) ], YELLOW),
        ([ points[2], (WIDTH, HEIGHT), (points[2][0], HEIGHT) ], GREEN),
    ]
    
    for area, color in areas:
        pg.draw.polygon(screen, color, area)

# Function to print point coordinates with labels
def print_point_coordinates(points, labels):
    for i, (point, label) in enumerate(zip(points, labels)):
        print(f"{label} x, y: ({point[0]}, {point[1]})")

# Main event loop
running = True
dragging_point = None
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            for i, point in enumerate(points):
                if (point[0] - event.pos[0]) * 2 + (point[1] - event.pos[1]) * 2 < 25:
                    dragging_point = i
        elif event.type == pg.MOUSEBUTTONUP:
            dragging_point = None
        elif event.type == pg.MOUSEMOTION:
            if dragging_point is not None:
                points[dragging_point] = (event.pos[0], event.pos[1])

    # Clear the screen
    screen.fill(WHITE)

    # Fill the areas under the line
    fill_areas(screen, points)

    # Draw the line
    draw_line(screen, points)

    # Draw the points
    draw_points(screen, points)

    # Print the coordinates of each point
    print_point_coordinates(points, labels)

    # Update the display
    pg.display.flip()

# Quit Pygame
pg.quit()
