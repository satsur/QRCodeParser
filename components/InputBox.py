import pygame

pygame.font.init()

COLOR_INCOMPLETE = pygame.Color((255, 0, 0))
COLOR_ACTIVE = pygame.Color('dodgerblue2')
COLOR_COMPLETED = pygame.Color((0, 255, 0))
DEFAULT_FONT = pygame.font.Font("fonts/Diavlo_BOLD_II_37.otf", 22)
FONT_COLOR = pygame.Color("white")

class InputBox:
    def __init__(self, x, y, width, height, text='', font = DEFAULT_FONT):
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
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
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
            
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + self.rect.width / 2 - self.txt_surface.get_width() / 2,
                                       self.rect.y + self.rect.height / 2 - self.txt_surface.get_height() / 2))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
