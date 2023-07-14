import pygame

class Mixer():
  
    def __init__(self):
        self.explode_s = pygame.mixer.Sound("music/explode.ogg")
        self.explode_s.set_volume(0.01)

        self.gunshot_s = pygame.mixer.Sound("music/gunshot_1.ogg")
        self.gunshot_s.set_volume(0.008)   

        self.hit_s = pygame.mixer.Sound("music/hit.ogg")
        self.hit_s.set_volume(0.01)

        self.lose_s = pygame.mixer.Sound("music/lose.wav")
        self.lose_s.set_volume(0.01)

        self.level_s = pygame.mixer.Sound("music/level.ogg")
        self.level_s.set_volume(0.2)   

        self.score_s = pygame.mixer.Sound("music/score.wav")
        self.score_s.set_volume(0.008)   