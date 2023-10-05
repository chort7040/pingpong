from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self, key_up, key_down):
        if key_up and self.rect.y > 5:
            self.rect.y -= self.speed
        if key_down and self.rect.y < win_h - 150:
            self.rect.y += self.speed
    
        
back = (200,255,255)
win_h = 500
win_w = 600
window = display.set_mode((win_w,win_h))
window.fill(back)

game = True
finish = False
clock = time.Clock()
FPS = 60

rack1 = Player('racket.png',30,200,50,150,4)
rack2 = Player('racket.png',520,200,50,150,4)
ball = GameSprite('tenis_ball.png',200,200,50,50,4)

font.init()
font = font.Font(None, 35)
lose1 = font.render('Player 1 lose!', True,(180,20,0))
lose2 = font.render('Player 2 lose!', True,(180,20,0))

speed_x = 3
speed_y = 3

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.fill(back)
        keys = key.get_pressed()
        rack1.update(keys[K_w],keys[K_s])
        rack2.update(keys[K_UP],keys[K_DOWN])
        
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        if sprite.collide_rect(rack1, ball) or sprite.collide_rect(rack2, ball):
            speed_x *= -1
            speed_y *= 1

        if ball.rect.y > win_h-50 or ball.rect.y < 0:
            speed_y *= -1

        if ball.rect.x < 0:
            finish = True
            window.blit(lose1,(200,200))

        if ball.rect.x > win_w:
            finish = True
            window.blit(lose2,(200,200))

        rack1.reset()
        rack2.reset()
        ball.reset()

        display.update()
        clock.tick(FPS)




