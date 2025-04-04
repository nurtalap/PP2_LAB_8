import pygame
import random
import time

pygame.init()
pygame.mixer.init() #module for working with sound

clock = pygame.time.Clock() #oblectbfor controlling fps
FPS = 60

WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
backgroud = pygame.image.load(r"AnimatedStreet.png")
player_img = pygame.image.load(r"Player.png")
enemy_img = pygame.image.load(r"Enemy.png")
coin_img = pygame.image.load(r"coin.png")
coin_img = pygame.transform.scale(coin_img, (55, 55))
#backgroud_music = pygame.mixer.music.load(r"C:\Users\Acer\Desktop\Python\background.wav")
#crash_sound = pygame.mixer.Sound(r"C:\Users\Acer\Desktop\Python\crash.wav")

font = pygame.font.SysFont("Verdana", 60)#creates shrifts , verdana 60 fjr text game over
game_over = font.render("Game Over", True, "red") #сщздает изоьражения гейм овер

coin_count_font = pygame.font.SysFont("Verdana", 20)#verdana 20 for счет монет
coin_count = 0  #храним количество монеты 

pygame.mixer.music.play(-1)  #воспроизводит музыку бесконечно (-1)

PLAYER_SPEED = 5
ENEMY_SPEED = 4

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - self.rect.w // 2
        self.rect.y = HEIGHT - self.rect.h                                  #places player to the bottom
        
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-PLAYER_SPEED, 0) #moves the rectangle, in place
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(PLAYER_SPEED, 0)
        if self.rect.left < 0:
            self.rect.left = 0                         #moves player right and left
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.generate_random_rect()
        
    def move(self):
        self.rect.move_ip(0, ENEMY_SPEED)  #move_ip() двигает врага на заданное количество пиксеоей
        if self.rect.top > HEIGHT:
            self.generate_random_rect()#сбрасывает врага рандомную верхную часть окна если враг выходит за линию
            
    def generate_random_rect(self): 
        self.rect.x = random.randint(0, WIDTH - self.rect.w) #random position from horizontally
        self.rect.y = 0 # initial position from сверху
        
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.generate_random_rect()
        
    def move(self):
        self.rect.move_ip(0, ENEMY_SPEED // 2)
        if self.rect.top > HEIGHT:
            self.generate_random_rect()
            
    def generate_random_rect(self):
        self.rect.x = random.randint(0, WIDTH - self.rect.w )
        self.rect.y = -self.rect.h    #Спавн за пределами экрана

        
player = Player()
enemy = Enemy()
coin = Coin()

all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
coin_sprites = pygame.sprite.Group()

all_sprites.add(player, enemy, coin)
enemy_sprites.add(enemy)
coin_sprites.add(coin)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.blit(backgroud, (0, 0))

    player.move()
    enemy.move()
    coin.move()
    
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
    
    #Проверяем столкновение игрока с монетой
    if pygame.sprite.spritecollideany(player, coin_sprites):
        coin_count += 1
        coin.generate_random_rect()
    
    #Проверяем столкновение игрока и врага
    if pygame.sprite.spritecollideany(player, enemy_sprites):
        crash_sound.play()
        time.sleep(1)

        screen.fill("black") # заливка поверхности
        center_rect = game_over.get_rect(center = (WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over, center_rect)

        pygame.display.flip()

        time.sleep(1)
        running = False
    
    #Отображение счёта
    # Отображение счёта в правом верхнем углу
    counting = coin_count_font.render(f"Coins: {coin_count}", True, "black")
    counting_rect = counting.get_rect(topright=(WIDTH - 10, 10))
    screen.blit(counting, counting_rect)#зисует фон и все спрайты

    pygame.display.flip() 
    clock.tick(FPS)
pygame.quit()