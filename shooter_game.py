#Створи власний Шутер!
import pygame
pygame.init()
from time import time
from random import randint
from random import choice
FPS = 60
window = pygame.display.set_mode((700, 500))
win_width = 500
win_height = 700
clock = pygame.time.Clock()
background = pygame.image.load('space.jpg')
background = pygame.transform.scale(background, (700, 500))
score = 0

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)
        image = pygame.transform.scale(image, (w, h))
        self.image = pygame.transform.scale(image, (w, h))
        self.speed = speed
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
heart_img = pygame.image.load('pixelheart.png')
class Player(GameSprite):
    def __init__(self, x, y, w, h, image, speed, hp):
        super().__init__(x, y, w, h, image, speed)
        self.hp = hp
        hearts = []
        x = 650
        for i in range (self.hp):
            h = GameSprite(x, 0, 50, 50, heart_img, 0)
            hearts.append(h)
            x -= 25
        self.hearts = hearts
    def move(self):
        k = pygame.key.get_pressed()
        if k[pygame.K_d]:
            if self.rect.right <= 700:
                self.rect.x += self.speed
        if k[pygame.K_a]:
            if self.rect.x >= 0:
                self.rect.x -= self.speed

    def collide(self, item):
        if self.rect.colliderect(item.rect):
            return True
        else:
            return False
    def shoot(self):
        #k = pygame.key.get_pressed()
        #if k[pygame.K_SPACE]:
        fire_sound.play()
        bullet = Bullet(self.rect.centerx - 2, self.rect.y, 10, 20, bullet_img, 8)
        


#bots = []
bots_group = pygame.sprite.Group()
class Bot(GameSprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image, speed)
        #bots.append(self)
        bots_group.add(self)
    # def start(self):
    #     self.rect.y = 0
    #     self.rect.x = randint(0, 700 - self.rect.w)
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 500:
            lost += 1
            #bots.remove(self)
            bots_group.remove(self)



bullet_group = pygame.sprite.Group()

class Bullet(GameSprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image, speed)
        bullet_group.add(self)
        
    def update(self):
        
        self.rect.y -= self.speed
        if self.rect.bottom <= 0:
            bullet_group.remove(self)


bullet_img = pygame.image.load('circle.png')

enemy_wait = randint(150, 250)
lost = 0
player_img = pygame.image.load('123369.png')
player = Player(320, 420, 80, 80, player_img, 4, 3)

bot_img = pygame.image.load('asteroid2.png')
bot = Bot(320, 90, 50, 40, bot_img, 2)

sound1 = pygame.mixer.Sound("space.ogg")
fire_sound = pygame.mixer.Sound("fire.ogg")
font1 = pygame.font.SysFont('Arial', 32)


limit = 0
en_min_speed = 1
en_max_speed2 = 3
max_score = 0
score = 0
try:
    with open('hit.txt', 'r') as file:
        max_score = int(file.read())
except FileNotFoundError:
    file = open('hit.txt', 'x')
    file.close()
except ValueError:
    pass

game = True
finish = False
while game:
    if not finish:
        lost_lb = font1.render('Lost: ' + str(lost), True, (255, 255, 255))
        score_lb = font1.render('Score: ' + str(score), True, (255, 255, 255))
        max_score_lb = font1.render('Max Score: ' + str(max_score), True, (255, 255, 255))
        limit_lb = font1.render('Limit: ' + str(score), True, (255, 255, 255))
        if enemy_wait == 0:
            bot = Bot(randint(0, 650), 0, 50, 40, bot_img, randint(en_min_speed, en_max_speed2))
            enemy_wait = randint(50, 100)
        else:
            enemy_wait -= 1
        window.blit(background, (0, 0))
        window.blit(lost_lb, (0, 0))
        window.blit(score_lb, (0, 30))
        window.blit(max_score_lb, (0, 60))
        #window.blit(limit_lb, (0, 90))
        player.draw()
        player.move()
        #player.shoot()
        for h in player.hearts:
            h.draw()
        #for bot in bots:
        #    bot.draw()
        #    bot.move()
        bots_group.draw(window)
        bots_group.update()
        bullet_group.draw(window)
        bullet_group.update()

        if pygame.sprite.groupcollide(bots_group, bullet_group, True, True):
            score += 1


            if score == 5 or score == 20:
                en_min_speed +=1
                en_max_speed2 += 1

        if pygame.sprite.spritecollide(player, bots_group, True):
            player.hp -= 1
            player.hearts.pop(0)

        if player.hp <= 0 or lost >= 3:
            game_over = font1.render('Game Over', True, (200,0,0))
            window.blit(game_over, (win_width/2, win_height/2 + 100))
            new_game_lb = font1.render('Ще раз - Enter', True, (200,0,0))
            window.blit(new_game_lb, (win_width/2, win_height/2))
            #sound2.play()
            finish = True
            if score > max_score:
                max_score = score
                with open('hit.txt', 'w') as file:
                    file.write(str(max_score))
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            player.shoot()
            limit + 1


        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and finish:
            player.rect.x = 320
            player.rect.y = 420
            bots_group.empty()
            bullet_group.empty()
            
            score = 0
            lost = 0

            finish = False
    clock.tick(FPS)
    pygame.display.update()