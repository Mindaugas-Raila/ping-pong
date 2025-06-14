from pygame import *
from random import randint

init()
window = display.set_mode((700, 500))
background = transform.scale(image.load('ping_pong_background.jpg'), (700, 500))
clock = time.Clock()
block_image = transform.scale(image.load('black.jpg'), (20, 50))
ball_image = image.load('test2.jpg')
font1 = font.Font('freesansbold.ttf', 32)

# Score tracking
player_score = 0
enemy_score = 0
win_score = 5

game = True
finish = False
ball_reset = False
start_time = time.get_ticks()
class Sprite:
    def __init__(self, img, x, y, width, height, direction=1):
        self.image = transform.scale(img, (width, height))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.direction = direction

    def draw(self):
        window.blit(self.image, (self.x, self.y))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def get_rect(self):
        return Rect(self.x, self.y, self.width, self.height)

    def collides_with(self, other, change=False):
        return self.get_rect().colliderect(other.get_rect())       

player = Sprite(block_image, 50, 225, 20, 50)
enemy = Sprite(block_image, 650, 225, 20, 50)
ball = Sprite(ball_image, 350 - 15, 250 - 15, 30, 30)

change = True
x_speed = -1
y_speed = -1

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        if change:
            x_speed = randint(4, 7) * (x_speed / abs(x_speed))
            y_speed = randint(2, 5) * (y_speed / abs(y_speed))
            change = False

        keys = key.get_pressed()
        if keys[K_UP] and player.y > 0:
            player.move(0, -5)
        if keys[K_DOWN] and player.y < 450:
            player.move(0, 5)

        if ball.y <= 0 or ball.y >= 470:
            y_speed *= -1
        ball.move(x_speed, y_speed)

        if ball.x <= 0:
            enemy_score += 1
            ball_reset = True
        elif ball.x >= 670:
            player_score += 1
            ball_reset = True

        if ball_reset:
            ball.x = 350 - 15
            ball.y = 250 - 15
            x_speed *= -1
            change = True
            ball_reset = False

        if player_score >= win_score:
            end = 'won'
            finish = True
        elif enemy_score >= win_score:
            end = 'lost'
            finish = True

        if (ball.collides_with(player) or ball.collides_with(enemy)) and (time.get_ticks() - start_time) // 100 >= 5:
            start_time = time.get_ticks()
            x_speed *= -1
            change = True

        dy = ball.y - enemy.y - enemy.height // 2
        if abs(dy) > 5:
            dy = 5 if dy > 0 else -5
        enemy.move(0, dy)

        window.blit(background, (0, 0))
        player.draw()
        enemy.draw()
        ball.draw()

        score_text = font1.render(f"{player_score} : {enemy_score}", True, (255, 255, 255))
        window.blit(score_text, (310, 20))

    else:
        white = (255, 255, 255)
        green = (0, 255, 0)
        blue = (0, 0, 128)
        end_text = font1.render(f'You {end}! Press W to play again', True, green, blue)
        textRect = end_text.get_rect(center=(350, 250))
        window.blit(end_text, textRect)

        keys = key.get_pressed()
        if keys[K_w]:
            finish = False
            player_score = 0
            enemy_score = 0
            ball.x = 350 - 15
            ball.y = 250 - 15
            change = True
            x_speed *= -1

    display.update()
    clock.tick(60)
