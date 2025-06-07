import pygame
import time
pygame.init()

window = pygame.display.set_mode((1550, 810))
background = pygame.image.load("grass.jpg")
background = pygame.transform.scale(background, (1550, 810))

pygame.font.init()
font = pygame.font.SysFont('Arial', 50)
big_font = pygame.font.SysFont('Arial', 80)  # Збільшений шрифт для початкових і кінцевих текстів
input_font = pygame.font.SysFont('Arial', 60)  # Збільшений шрифт для вводу імені
timer_font = pygame.font.SysFont('Arial', 60)

clock = pygame.time.Clock()

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
        if keys[pygame.K_DOWN] and self.y < 810 - self.height:
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
        if keys[pygame.K_s] and self.y < 810 - self.height:
            self.y += self.step

class Enemy():
    def __init__(self, x, y, image_sprite):
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

        if self.y < 0 or self.y + self.height > 810:
            self.y_step = -self.y_step

    def reset(self):
        self.x = 735
        self.y = 0  # м'яч стартує зверху, а не по центру
        self.x_step = -5 if self.x_step > 0 else 5
        self.y_step = 7

    def check_collision(self, player):
        if (self.x < player.x + player.width and
            self.x + self.width > player.x and
            self.y < player.y + player.height and
            self.y + self.height > player.y):
            self.x_step = -self.x_step * 1.1
            self.y_step *= 1.1
            if self.x_step > 0:
                self.x = player.x + player.width
            else:
                self.x = player.x - self.width
            return True
        return False

player = Gamesprit(1410, 280, 3, "stick.png")
player2 = Gamesprit2(10, 280, 3, "stick.png")
baller = Enemy(735, 365, "ball.png")

score1 = 0
score2 = 0

game_over = False
winner_text = ""
game_started = False

input_active = True
input_stage = 1
name1 = ""
name2 = ""

music_started = False

start_ticks = 0
game_duration = 120  # 2 хвилини

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
                        time.sleep(0.5)
                        game_started = True
                        start_ticks = pygame.time.get_ticks()
                else:
                    if event.unicode.isprintable():
                        if input_stage == 1 and len(name1) < 12:
                            name1 += event.unicode
                        elif input_stage == 2 and len(name2) < 12:
                            name2 += event.unicode
        else:
            if event.type == pygame.KEYDOWN:
                if not game_started and event.key == pygame.K_SPACE:
                    game_started = True
                    start_ticks = pygame.time.get_ticks()

    if input_active:
        window.fill((13, 113, 1))

        if input_stage == 1:
            prompt_text = big_font.render("Введіть ім'я гравця 1 (до 7 символів):", True, (200, 214, 0))
            input_text = input_font.render(name1, True, (200, 214, 0))
            prompt_rect = prompt_text.get_rect(center=(1550//2, 180))  # Заголовок вище
            input_rect = input_text.get_rect(center=(1550//2, 280))    # Текст вводу нижче
        elif input_stage == 2:
            prompt_text = big_font.render("Введіть ім'я гравця 2 (до 7 символів):", True, (200, 214, 0))
            input_text = input_font.render(name2, True, (200, 214, 0))
            prompt_rect = prompt_text.get_rect(center=(1550//2, 180))
            input_rect = input_text.get_rect(center=(1550//2, 280))
        else:
            prompt_text = big_font.render("Натисніть ПРОБІЛ для початку", True, (200, 214, 0))
            input_text = input_font.render("", True, (200, 214, 0))
            prompt_rect = prompt_text.get_rect(center=(1550//2, 230))
            input_rect = input_text.get_rect(center=(1550//2, 280))

        window.blit(prompt_text, prompt_rect)
        window.blit(input_text, input_rect)

    else:
        if not music_started:
            pygame.mixer.music.load("music2.mp3")
            pygame.mixer.music.play(-1)
            music_started = True

        if not game_over:
            window.blit(background, (0, 0))
            s = pygame.Surface((1550, 810))
            s.set_alpha(150)
            s.fill((13, 113, 1))
            window.blit(s, (0, 0))

            player.draw()
            player2.draw()
            baller.draw()

            player.update()
            player2.update()
            baller.update()

            baller.check_collision(player)
            baller.check_collision(player2)

            if baller.x <= 0:
                score2 += 1
                baller.reset()

            if baller.x + baller.width >= 1550:
                score1 += 1
                baller.reset()

            seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
            time_left = max(0, int(game_duration - seconds_passed))

            minutes = time_left // 60
            seconds = time_left % 60
            timer_display = f"{minutes}:{seconds:02d}"

            if seconds_passed >= game_duration:
                game_over = True
                winner_text = "Час вийшов, гра закінчена!"

            if score1 >= 8:
                game_over = True
                winner_text = f"{name1} виграв!"
            elif score2 >= 8:
                game_over = True
                winner_text = f"{name2} виграв!"

            text1 = font.render(f"{name1} : {score1}", True, (200, 214, 0))
            text2 = font.render(f"{name2} : {score2}", True, (200, 214, 0))

            score1_rect = pygame.Rect(20, 20, 280, 60)
            score2_rect = pygame.Rect(1250, 20, 280, 60)
            pygame.draw.rect(window, (13, 113, 1), score1_rect)
            pygame.draw.rect(window, (13, 113, 1), score2_rect)

            window.blit(text1, (30, 30))
            window.blit(text2, (1260, 30))

            timer_text = timer_font.render(timer_display, True, (200, 214, 0))
            timer_bg_rect = timer_text.get_rect(center=(1550 // 2, 50))
            padding = 15
            pygame.draw.rect(window, (13, 113, 1), 
                             (timer_bg_rect.x - padding, timer_bg_rect.y - padding, 
                              timer_bg_rect.width + 2*padding, timer_bg_rect.height + 2*padding))
            window.blit(timer_text, timer_bg_rect)

        else:
            window.fill((13, 113, 1))
            text_winner = big_font.render(winner_text, True, (200, 214, 0))
            text_rect = text_winner.get_rect(center=(1550//2, 300))
            window.blit(text_winner, text_rect)

    pygame.display.update()
    clock.tick(60)
