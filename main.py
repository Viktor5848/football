import pygame
pygame.init()
# window .;)
window = pygame.display.set_mode((1400, 715))
background = pygame.image.load("grass.jpg")
background = pygame.transform.scale(background, (1400, 715))
pygame.mixer.music.load("Epic Sport Rock - AShamaluevMusic.mp3.crdownload")
pygame.mixer.music.play(-1)
clock = pygame.time.Clock()
class Gamesprit():
    def __init__(self,x=0,y=0,height=0,width=0,step=0,image_sprite=""):
        self.image = pygame.image.load(image_sprite)
        self.image = pygame.transform.scale(self.image, (120, 290))
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.step = step
    def draw(self,x,y,):
        window.blit(self.image, (self.x, self.y))
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]and self.y>0:
            self.y-=self.step
        if keys[pygame.K_DOWN]and self.y<715-100:
            self.y+=self.step

class Gamesprit2():
    def __init__(self,x=0,y=0,height=0,width=0,step=0,image_sprite=""):
        self.image = pygame.image.load(image_sprite)
        self.image = pygame.transform.scale(self.image, (120, 290))
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.step = step
    def draw(self,x,y,):
        window.blit(self.image, (self.x, self.y))
    def update2(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]and self.y>0:
            self.y-=self.step
        if keys[pygame.K_s]and self.y<715-100:
            self.y+=self.step


class Enemy():
    def __init__(self,x=0,y=0,height=0,width=0,step=0,radius=0,image_sprite=""):
        self.image = pygame.image.load(image_sprite)
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.step = step
        self.radius = radius
    def draw(self,x,y,):
        window.blit(self.image, (self.x, self.y))
    def move(self):
        self.x += self.step
        self.y += self.step
        if self.x <= self.radius or self.x >= 1700 - self.radius:
            self.step *= -1
        if self.y <= self.radius or self.y >= 715 - self.radius:
            self.step *= -1


ball = Enemy(650, 280, 20, 50, 5, "ball.png")
player = Gamesprit(1250, 250, 20, 50, 5, "stick.png")
player2 = Gamesprit2(50, 250, 20, 50, 5, "stick.png")

game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    window.blit(background, (0, 0))
    player.draw(player.x, player.y)
    ball.draw(ball.x, ball.y)
    player2.draw(player2.x, player2.y)
    player.update()
    player2.update2()
    ball.move()
    pygame.display.update()

    clock.tick(40)
pygame.quit()
