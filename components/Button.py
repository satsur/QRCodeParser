import pygame

pygame.font.init()

COLOR_ACTIVE = pygame.Color((255,120,0))
COLOR_HOVER = pygame.Color((255,140,0))
COLOR_DEFAULT = pygame.Color((255,150,0))
DEFAULT_FONT = pygame.font.Font("fonts/Diavlo_BOLD_II_37.otf", 22)

class Button:
    def __init__(self, x, y, width, height, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = DEFAULT_FONT
        self.color = COLOR_DEFAULT
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.txt_surface = self.font.render(self.text, True, pygame.Color("white"))
        self.hovered = False
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            # If the user is hovering on the button rect:
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.hovered = True
            else:
                self.hovered = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on button rect:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        elif event.type == pygame.MOUSEBUTTONUP:
            # If the user lets go of the mouse button
            self.active = False
            if self.rect.collidepoint(event.pos):
                self.hovered = True
            else:
                self.hovered = False

    def update(self):
        # Update color based on hover
        if self.active:
            self.color = COLOR_ACTIVE
        elif self.hovered:
            self.color = COLOR_HOVER
        else:
            self.color = COLOR_DEFAULT
            

    def draw(self, screen, outline=None):
        # Draw the button on the screen
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        
        if self.active:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width-4, self.height-4), 0)
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width-4, self.height-4), 0)
        
        if self.txt_surface != '':
            font = self.font
            self.txt_surface = font.render(self.text, 1, (0, 0, 0))
            screen.blit(self.txt_surface, 
                        (self.x + (self.width/2 - self.txt_surface.get_width()/2), self.y + (self.height/2 - self.txt_surface.get_height()/2)))