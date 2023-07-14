import pygame.font


class Button():
    def __init__(self, screen, msg):
        """Initializes the button attributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Assignment of sizes and properties of buttons
        self.width, self.height = 150, 50
        self.button_color = (250, 200, 150)
        self.text_color = (95, 95, 95)
        self.font = pygame.font.SysFont(None, 48)

        # Сonstructing the rect object of the button and
        # Aligning it to the center of the screen
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message is created only once
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Converts msg to a rectangle and aligns the text to the center"""

        self.msg_image = self.font.render(
            msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Displaying an empty button and displaying a message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
