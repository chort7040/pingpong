from pygame import *
from random import *
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

img_back = 'space.jpg'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
img_rock = 'asteroid.png'

font.init()
font2 = font.SysFont('arial', 40)

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
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top,15, 20, -15)
        bullet.add(bullets)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width-80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

lost = 0
score = 0
FPS = 60
win_width = 1000
win_height = 500
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))
bg = transform.scale(image.load(img_back),(win_width, win_height))

ship = Player(img_hero, 5, win_height-100, 80, 100, 18)

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy, randint(80, win_width-80), -40, 80, 50, randint(1,5))
    monsters.add(monster)

bullets = sprite.Group()
rocks = sprite.Group()
for i in range(1,3):
    rock = Enemy(img_rock, randint(80, win_width-80), -40, 80, 50, randint(1,2))
    rock.add(rocks)

win = font2.render('You Win!', True, (20,220,0))
lose = font2.render('You Lose!', True, (180,10,0))
finish = False
max_lost = 3
goal = 10
game = True
while game:
    window.blit(bg,(0,0))

    for e in event.get():
        if e.type == QUIT: 
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_w:
                fire_sound.play()
                ship.fire()

    if not finish:
        window.blit(bg,(0,0))

        text = font2.render("Счет:"+str(score),1,(255, 255, 255))
        window.blit(text,(10,20))

        text_lose = font2.render("Пропущено:"+str(lost),1,(255, 255, 255))
        window.blit(text_lose,(10,50))
        
        ship.update()
        monsters.update()
        bullets.update()
        rocks.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        rocks.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width-80), -40, 80, 50, randint(1,5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, rocks, False) or lost >= max_lost:
            window.blit(lose,(450,250))
            finish = True

        if score >= goal:
            window.blit(win,(450,250))
            finish = True

        display.update()

    time.delay(50)