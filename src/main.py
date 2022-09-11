from tkinter import SCROLL
from tkinter.tix import MAX, WINDOW
import pygame

# Color paints
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (142, 145, 145)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PINK = (255, 0, 255)
PURPLE = (115, 0, 255)
ORANGE = (255, 115, 0)
COLORS = [BLACK, WHITE, GREY, GREEN, RED, BLUE, CYAN, YELLOW, PINK, PURPLE, ORANGE]
 
# Constants
WINDOW_SIZE = (800, 600)
PANEL_SIZE = 51
CANVAS_SIZE = WINDOW_SIZE[1] - PANEL_SIZE
COLOR_ICON_START = (25, 25)
COLOR_ICON_RADIUS = 15
COLOR_ICON_SPACING = 20
MIN_BRUSH_SIZE = 1
MAX_BRUSH_SIZE = 30
SCROLL_SIZE_MODIF = 30
SAVE_LOC = "my_drawing.png"

# Color icon class
class ColorIcon:
    # Initialise the icon
    def __init__(self, location, radius, color):
        self.location = location
        self.radius = radius
        self.color = color
    # Draw the icon into the given surface
    def draw(self, surface):
        if (self.color == WHITE):
            pygame.draw.circle(surface, GREY, self.location, self.radius + 2)
        pygame.draw.circle(surface, self.color, self.location, self.radius)
    # Returns True if point in cirlce
    def is_clicked(self, mpos):
        if ( (mpos[0] - self.location[0]) ** 2 + (mpos[1] - self.location[1]) ** 2 < self.radius ** 2):
            return True
        return False



# Draw panel class
class DrawPanel:
    def __init__(self):
        self.surface = pygame.Surface((WINDOW_SIZE[0], PANEL_SIZE))
        self.icon_array = []
        self.selected_color = BLACK # Default color
        x = 0
        for color in COLORS:
            self.icon_array.append(ColorIcon((COLOR_ICON_START[0] + (COLOR_ICON_RADIUS + COLOR_ICON_SPACING) * x, COLOR_ICON_START[1]) 
            ,COLOR_ICON_RADIUS , color))
            x += 1
        
    # Draw the panel
    def draw(self):
        # First clear it
        self.surface.fill(WHITE)

        # Draw icons
        for icon in self.icon_array:
            icon.draw(self.surface)

        # Draw border line
        pygame.draw.line(self.surface, GREY, (0, 50), (800, 50))

    # Check if a color icon was pressed
    def check_color_pressed(self):
        mouse_pos = pygame.mouse.get_pos()
        for icon in self.icon_array:
            if icon.is_clicked(mouse_pos):
                self.selected_color = icon.color


# Paintbrush class
class PaintBrush:
    def __init__(self):
        self.color = None  
        self.size = 5 # Default brush size
        self.brush_down = False
    
    def paint(self, canvas):
        # First get current mouse position
        if (self.brush_down):
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.circle(canvas, self.color, (mouse_pos[0], mouse_pos[1] - PANEL_SIZE), self.size)



def run_paint():
    # Initialise 
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("My Game")
    run_game = False
    clock = pygame.time.Clock()

    # Create draw panel 
    draw_panel = DrawPanel()

    # Create the canvas
    canvas = pygame.Surface((WINDOW_SIZE[0], CANVAS_SIZE))
    canvas.fill(WHITE)

    # And paintbrush
    paintbrush = PaintBrush()
    paintbrush.color = draw_panel.selected_color

    # Main loop
    while not run_game:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = True
            # Resize brush
            if event.type == pygame.MOUSEWHEEL:
                nsize = paintbrush.size + event.y/SCROLL_SIZE_MODIF
                if (event.y < 0):
                    if (nsize > MIN_BRUSH_SIZE):
                        paintbrush.size = nsize
                    else:
                        paintbrush.size = MIN_BRUSH_SIZE
                elif (event.y > 0):
                    if (nsize < MAX_BRUSH_SIZE):
                        paintbrush.size = nsize
                    else:
                        paintbrush.size = MAX_BRUSH_SIZE
            # Paint with the brush
            if event.type == pygame.MOUSEBUTTONDOWN:
                draw_panel.check_color_pressed()
                paintbrush.brush_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                paintbrush.brush_down = False

            if event.type == pygame.KEYDOWN:
                # Check if the canvas should be cleared 
                if event.key == pygame.K_c:
                    canvas.fill(WHITE)
                # Check if the canvas should be saved
                if event.key == pygame.K_s:
                    pygame.image.save(canvas, SAVE_LOC)

        # Set paintbrush color to selected color
        paintbrush.color = draw_panel.selected_color
        # Draw loop
        screen.fill(WHITE)
        # Draw the panel
        draw_panel.draw()
        screen.blit(draw_panel.surface, (0, 0))
        # Draw the canvas
        paintbrush.paint(canvas)
        screen.blit(canvas, (0, PANEL_SIZE))

        # Update display
        pygame.display.flip()

        # Framerate capping
        clock.tick(60)


if (__name__ == "__main__"):
    run_paint()