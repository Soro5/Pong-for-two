import pygame
pygame.init()

win_width = 640
win_height = 480
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Pong for two")
clock = pygame.time.Clock()
fps = 60

main_font = pygame.font.SysFont('Arial', 32)

class Brick(pygame.sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        super().__init__()
        # каждый спрайт должен хранить свойство image - изображение
        self.image = pygame.transform.scale(pygame.image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.score = 0
 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def move(self, key1, key2):
        keys = pygame.key.get_pressed()
        if keys[key1] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[key2] and self.rect.y < win_height - self.rect.height:
            self.rect.y += self.speed

player1 = Brick('brick.png', 35, 50, 35, 85, 4)
player2 = Brick('brick.png', win_width - 85, 50, 35, 85, 4)

class Ball(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speedx, speedy):
        super().__init__()
        # каждый спрайт должен хранить свойство image - изображение
        self.image = pygame.transform.scale(pygame.image.load(image), (30, 30))
        self.speedx = speedx
        self.speedy = speedy
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        self.rect.x += self.speedx
        self.rect.y += self.speedy
    def default(self):
        self.rect.x = win_width // 2
        self.rect.y = win_height // 2

ball = Ball('ball.png', win_width // 2 - 30, win_height // 2 + 30, 5, 5)
win1 = main_font.render('Player 1 won!', False, (255, 255, 255))
win2 = main_font.render('Player 2 won!', False, (255, 255, 255))
max = 10

finish = False
pause = False
run = True
while run:
    pygame.display.update()
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False

    window.fill((0, 0, 0))

    if finish != True:
        score1 = main_font.render(str(player1.score), False, (255, 255, 255))
        score2 = main_font.render(str(player2.score), False, (255, 255, 255))

        window.blit(score1, (10, 0))
        window.blit(score2, (win_width - 30, 0))

        player1.reset()
        player2.reset()

        ball.update()
        player1.move(pygame.K_w, pygame.K_s)
        player2.move(pygame.K_UP, pygame.K_DOWN)

        if ball.rect.y < 0 or ball.rect.y > win_height - 30:
            ball.speedy *= -1
        if ball.rect.colliderect(player1) or ball.rect.colliderect(player2):
            ball.speedx = (ball.speedx + 0.1) * -1 

        if ball.rect.x < 0:
            player2.score += 1
            ball.default()
        if ball.rect.x > win_width - 30:
            player1.score += 1
            ball.default()
        
        if player1.score > max or player2.score > max:
            finish = True
    else:
        if player1.score == 10:
            window.blit(win1, (win_width // 2 - 75, win_height // 2))
        else:
            window.blit(win2, (win_width // 2 - 75, win_height // 2))
    
    clock.tick(fps)
pygame.quit()