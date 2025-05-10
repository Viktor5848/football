import pygame
pygame.init()
# window .;)
window = pygame.display.set_mode((1400, 715))
background = pygame.image.load("grass.jpg")
background = pygame.transform.scale(background, (1400, 715))
clock = pygame.time.Clock()
class Gamesprit():
    def __init__(self,x=0,y=0,height=0,width=0,step=0,image_sprite=""):
        self.image = pygame.image.load(image_sprite)
        self.image = pygame.transform.scale(self.image, (120, 230))
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.step = step
    def draw(self,x,y,):
        window.blit(self.image, (self.x, self.y))
    def update(self):
        keys = pygame.key.get_pressed()
        if event.keys == pygame.K_UP:
            self.y -= self.step
        if event.keys == pygame.K_DOWN:
            self.y += self.step


player = Gamesprit(1250, 250, 20, 50, 5, "stick.png")

game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    window.blit(background, (0, 0))
    player.draw(player.x, player.y)
    pygame.display.update()
    clock.tick(40)
pygame.quit()