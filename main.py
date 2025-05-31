import pygame
pygame.init()

# Вікно та фон
window = pygame.display.set_mode((1300, 710))
background = pygame.image.load("grass.jpg")
background = pygame.transform.scale(background, (1300, 710))

# Музика
pygame.mixer.music.load("music.mp3.mp3")
pygame.mixer.music.play(-1)

# Шрифт
pygame.font.init()
font = pygame.font.SysFont('Arial', 50)
input_font = pygame.font.SysFont('Arial', 40)

clock = pygame.time.Clock()

# Клас для гравців
class Gamesprit():
    def __init__(self, x, y, step, image_sprite):
        self.image = pygame.image.load(image_sprite)
        self.image = pygame.transform.scale(self.image, (120, 250))
        self.x = x
        self.y = y
        self.width = 120
        self.height = 250
        self.step = step

    def draw(self):
        window.blit(self.image, (self.x, self.y))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.step
        if keys[pygame.K_DOWN] and self.y < 710 - self.height:
            self.y += self.step

class Gamesprit2():
    def __init__(self, x, y, step, image_sprite):
        self.image = pygame.image.load(image_sprite)
        self.image = pygame.transform.scale(self.image, (120, 250))
        self.x = x
        self.y = y
        self.width = 120
        self.height = 250
        self.step = step

    def draw(self):
        window.blit(self.image, (self.x, self.y))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.y > 0:
            self.y -= self.step
        if keys[pygame.K_s] and self.y < 710 - self.height:
            self.y += self.step

# Клас м’яча
class Enemy():
    def __init__(self, x, y, image_sprite, speed_x=10, speed_y=7):
        self.image = pygame.image.load(image_sprite)
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.x = x
        self.y = y
        self.width = 80
        self.height = 80
        self.x_step = -5
        self.y_step = 7

    def draw(self):
        window.blit(self.image, (self.x, self.y))

    def update(self):
        self.x += self.x_step
        self.y += self.y_step

        # Відскок по вертикалі
        if self.y < 0 or self.y + self.height > 710:
            self.y_step = -self.y_step

    def reset(self):
        self.x = 650
        self.y = 280
        self.x_step = -self.x_step
        self.y_step = 7

    def check_collision(self, player):
        if (self.x < player.x + player.width and
            self.x + self.width > player.x and
            self.y < player.y + player.height and
            self.y + self.height > player.y):
            self.x_step = -self.x_step
            if self.x_step > 0:
                self.x = player.x + player.width
            else:
                self.x = player.x - self.width
            return True
        return False

# Створення об’єктів
player = Gamesprit(1180, 250, 3, "stick.png")
player2 = Gamesprit2(10, 250, 3, "stick.png")
baller = Enemy(650, 280, "ball.png")

# Рахунок
score1 = 0
score2 = 0

# Стан гри
game_over = False
winner_text = ""
game_started = False

# Змінні для вводу імен
input_active = True
input_stage = 1  # 1 - ім'я гравця1, 2 - ім'я гравця2, 3 - готово
name1 = ""
name2 = ""

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if input_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if input_stage == 1 and len(name1) > 0:
                        name1 = name1[:-1]
                    elif input_stage == 2 and len(name2) > 0:
                        name2 = name2[:-1]
                elif event.key == pygame.K_RETURN:
                    if input_stage == 1 and len(name1) > 0:
                        input_stage = 2
                    elif input_stage == 2 and len(name2) > 0:
                        input_stage = 3
                        input_active = False
                        game_started = True
                else:
                    # Додаємо лише літери, цифри та пробіли
                    if event.unicode.isprintable():
                        if input_stage == 1 and len(name1) < 12:
                            name1 += event.unicode
                        elif input_stage == 2 and len(name2) < 12:
                            name2 += event.unicode
        else:
            if event.type == pygame.KEYDOWN:
                if not game_started and event.key == pygame.K_SPACE:
                    game_started = True

    if input_active:
        window.fill((255, 255, 255))  # Білий фон

        if input_stage == 1:
            prompt_text = font.render("Введіть ім'я гравця 1:", True, (177, 2, 93))
            input_text = input_font.render(name1, True, (0, 0, 0))
        elif input_stage == 2:
            prompt_text = font.render("Введіть ім'я гравця 2:", True, (177, 2, 93))
            input_text = input_font.render(name2, True, (0, 0, 0))
        else:
            prompt_text = font.render("Натисніть ПРОБІЛ для початку", True, (177, 2, 93))
            input_text = input_font.render("", True, (0, 0, 0))

        window.blit(prompt_text, (350, 250))
        window.blit(input_text, (350, 320))

    else:
        if not game_over:
            window.blit(background, (0, 0))

            player.draw()
            player2.draw()
            baller.draw()

            player.update()
            player2.update()
            baller.update()

            baller.check_collision(player)
            baller.check_collision(player2)

            if baller.x <= 0:
                score2 += 1   # Гравець 2 набирає, м'яч пройшов ліву межу
                baller.reset()

            if baller.x + baller.width >= 1300:
                score1 += 1   # Гравець 1 набирає, м'яч пройшов праву межу
                baller.reset()

            # Перевірка переможця
            if score1 >= 12:
                game_over = True
                winner_text = f"{name1} виграв!"
            elif score2 >= 12:
                game_over = True
                winner_text = f"{name2} виграв!"

            # Вивід рахунку з іменами гравців
            text1 = font.render(f"{name1} : {score1}", True, (177, 2, 93))
            text2 = font.render(f"{name2} : {score2}", True, (177, 2, 93))
            window.blit(text1, (30, 30))
            window.blit(text2, (900, 30))

        else:
            # Екран кінця гри
            window.fill((0, 0, 0))  # Чорний фон
            text_winner = font.render(winner_text, True, (177, 2, 93))
            window.blit(text_winner, (500, 300))

    pygame.display.update()
    clock.tick(60)
