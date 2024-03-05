import pygame

pygame.font.init()

COLOR_INCOMPLETE = pygame.Color((255, 0, 0))
COLOR_ACTIVE = pygame.Color('dodgerblue2')
COLOR_COMPLETED = pygame.Color((0, 255, 0))
DEFAULT_FONT = pygame.font.Font("fonts/Diavlo_BOLD_II_37.otf", 22)
FONT_COLOR = pygame.Color("black")
OUTLINE_WIDTH = 3

class InputBox:
    def __init__(self, x, y, width, height, text='', font = DEFAULT_FONT):
        self.default_width = width
        self.default_height = height
        self.background = pygame.Surface((width-2*OUTLINE_WIDTH, height-2*OUTLINE_WIDTH))
        self.rect = pygame.Rect(x, y, width, height)
        self.color = COLOR_INCOMPLETE
        self.text = text
        self.font = font
        self.txt_surface = self.font.render(text, True, FONT_COLOR)
        self.active = False
        self.completed = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
    
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, FONT_COLOR)

    def update(self):
        # Change the current color of the input box.
        if self.active:
            self.color = COLOR_ACTIVE
        elif not self.active and self.completed:
            self.color = COLOR_COMPLETED
        else:
            self.color = COLOR_INCOMPLETE
        
        # Update text
        self.txt_surface = self.font.render(self.text, True, FONT_COLOR)
            
        # Resize the box if the text is too long.
        width = max(self.default_width, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Set input box background
        self.background.fill((255,255,255))
        screen.blit(self.background, (self.rect.x + OUTLINE_WIDTH, self.rect.y + OUTLINE_WIDTH))
        # Blit rectangle (outline) onto input box
        pygame.draw.rect(screen, self.color, self.rect, OUTLINE_WIDTH)
        # Blit text onto input box
        screen.blit(self.txt_surface, (self.rect.x + self.rect.width / 2 - self.txt_surface.get_width() / 2,
                                                self.rect.y + self.rect.height / 2 - self.txt_surface.get_height() / 2))