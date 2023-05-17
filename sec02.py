'''
pygame을 이용하여 간단한 슈팅 게임 만들기
'''

import pygame
import random

FR = 60

screen_size = WIDTH, HEIGHT = 800, 600

PLAYER_SIZE = 30, 30
BULLET_SIZE = 5, 5

black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
blue = 0, 0, 255

BULLET_SPEED = -20

class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.image = pygame.Surface(BULLET_SIZE)
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.speed = BULLET_SPEED
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()
        

class Player(pygame.sprite.Sprite): # pygame.sprite : 모듈, Sprite : 게임 내의 캐릭터를 구현하기 위해 만들어진 클래스임
    def __init__(self, all_sp_group, bullet_sp_group) -> None:
        super().__init__()
        
        self.image = pygame.Surface(PLAYER_SIZE)
        self.image.fill(white) # 게임 캐릭터를 흰색으로 만듦
        self.rect = self.image.get_rect() # 게임 캐릭터의 위치
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT - PLAYER_SIZE[0]
        self.speed = 5
        self.all_sps = all_sp_group    # 모든 스프라이트들을 담는 그룹 
        self.bullets = bullet_sp_group # 총알만 담는 스프라이트 그룹
        
    def update(self):
        keys = pygame.key.get_pressed() # 현재 눌려진 키 값을 얻어옴
        if keys[pygame.K_LEFT]: # 왼쪽 방향키가 눌렸으면 
            self.rect.x -= self.speed # Player 객체의 좌표를 왼쪽으로 speed만큼 이동시킴
        elif keys[pygame.K_RIGHT]: # 오른쪽 방향키가 눌렸으면 
            self.rect.x += self.speed # Player 객체의 좌표를 오른쪽으로 speed만큼 이동시킴
        elif keys[pygame.K_UP]: # 위쪽 방향키가 눌렸으면 
            self.rect.y -= self.speed # Player 객체의 좌표가 위쪽으로 speed만큼 이동시킴 
        elif keys[pygame.K_DOWN]: # 아래쪽 방향키가 눌렸으면
            self.rect.y += self.speed  # Player 객체의 좌표가 아래쪽으로 speed만큼 이동시킴
        
        if keys[pygame.K_SPACE]: # 스페이스가 눌렸으면
            bullet = Bullets(self.rect.centerx, self.rect.top)
            self.all_sps.add(bullet) # 드로잉 + 위치 변경(update)
            self.bullets.add(bullet) # 충돌 체크용
        
        # 경계 체크
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH :
            self.rect.right = WIDTH
        elif self.rect.top < 0 :
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT :
            self.rect.bottom = HEIGHT
 
class Enemy(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.Surface(PLAYER_SIZE)
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH-50)
        self.rect.y = 0
        self.speed = random.randint(3, 6)
        
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()





pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode(screen_size)

all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()

player = Player(all_sprites, bullet_sprites)
all_sprites.add(player)

running = True
while running:
    clock.tick(FR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    if random.randint(1, 100) <= 20:
        enemy = Enemy()
        all_sprites.add(enemy) # 드로잉 목적 + 위치 이동(update) 목적
        enemy_sprites.add(enemy) # 충돌 체크용
    
    # 배경을 그려주기 전에 해야함
    all_sprites.update()
    
    # 충돌 체크
    if pygame.sprite.spritecollide(player, enemy_sprites, True): # 주인공들과 적들이 충돌이 일어남
        running = False
    
    hits =  pygame.sprite.groupcollide(bullet_sprites, enemy_sprites, True, True) # 충돌을 했다면 몇 개 충돌?
    for hit in hits:
        hit.kill()
    
    screen.fill(black) # 알아서 배경을 blit함 // 아직 화면에 나온 상태는 아니고 메모리 상에만 존재함
    # screen.blit(background)
    all_sprites.draw(screen) 
    
    pygame.display.update() # mainSurface의 부분만을 화면에 다시 출력 
    pygame.display.flip()   # mainSurface 전체를 화면에 출력