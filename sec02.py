'''
pygame을 이용하여 간단한 슈팅 게임 만들기
'''

import pygame # pygame module import
import random # random module import
import sys, os 

FR = 60 # 이 게임의 Frame Rate(초당 화면 갱신률)

 # 게임의 가로, 세로 화면 사이즈 정의
screen_size = (WIDTH, HEIGHT) = 800, 600 # 튜플 변수

PLAYER_SIZE = 30, 30 # 튜플 변수, 메인 캐릭터의 가로, 세로
BULLET_SIZE = 5, 5 # 튜플 변수, 총알의 가로, 세로

black = 0, 0, 0       # 튜플 변수, (r,g,b)순서
white = 255, 255, 255 # 튜플 변수
red = 255, 0, 0       # 튜플 변수
blue = 0, 0, 255      # 튜플 변수
                      # green은 0, 255, 0

BULLET_SPEED = -20 # 총알 스피드

class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.image = pygame.Surface(BULLET_SIZE)
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.speed = BULLET_SPEED
    
    # 오버라이딩
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class Player(pygame.sprite.Sprite): # pygame.sprite : 모듈, Sprite : 게임 내의 캐릭터를 구현하기 위해 만들어진 클래스임
    def __init__(self, all_sp_group, bullet_sp_group) -> None:
        super().__init__()
        
        # self.image = pygame.Surface(PLAYER_SIZE)
        self.image = pygame.image.load('shooter1.png').convert_alpha()      
        # self.image.fill(white) # 게임 캐릭터를 흰색으로 만듦
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

# 현재 디렉토리를 구함, import sys, os
current_path = os.path.dirname(sys.argv[0])

# 절대 경로로 변환
absolute_path = os.path.abspath(current_path)

# 폰트 파일의 절대 경로를 얻음
front_file_path = os.path.join(absolute_path, '나눔손글씨 무궁화.ttf')

pygame.init() # 반드시 init() 호출해야 pygame을 사용할 수 있음

clock = pygame.time.Clock() # FR를 사용하기 위해 초기화 함
screen = pygame.display.set_mode(screen_size) # 게임 화면을 메모리에 저장한 상태

# 화면에 점수를 출력하기 위해 폰트 객체 생성
font = pygame.font.Font('나눔손글씨 무궁화.ttf', 40) # 한글 출력 ttf(true type font), 나눔손글씨 무궁화 폰트

all_sprites = pygame.sprite.Group()    # Group는 sprite를 저장하는 것(리스트와 비슷), 모든 캐릭터(플레이어, 적, 총알 포함) -> (다시) 그려주기 위해
enemy_sprites = pygame.sprite.Group()  # 플레이어와 적들과의 충돌 감지위해서
bullet_sprites = pygame.sprite.Group() # 내 총알과 적들과의 충돌 감지를 위해서

player = Player(all_sprites, bullet_sprites) # 플레이어 생성
all_sprites.add(player)                      # 그리기 위해 플레이어를 all_sprites()에 저장

# 배경
background = pygame.image.load('background1.jpg') # 800 X 1200
back_y_pos = -(background.get_rect().height - HEIGHT)
scroll_speed = 1


score = 0
running = True # 플래그 변수

life = 3

# 게임 루프
while running:
    clock.tick(FR) # Frame Rate 적용, 초당 60회 flip, 2d 게임이므로 굳이 높은 값을 줄 필요 없음

    # 게임 상에서 발생하는 모든 이벤트를 모두 가져옴
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # 종료 이벤트가 발생시 
            running = False           # 게임 루프를 탈출
            
    if random.randint(1, 100) <= 20: # 적 생성 빈도수
        enemy = Enemy()
        all_sprites.add(enemy)   # 드로잉 목적 + 위치 이동(update()) 목적
        enemy_sprites.add(enemy) # 충돌 체크용
    
    text = font.render(f'점수  : {score}', # 화면에 출력할 텍스트
                       True, # anti-aliasing 사용 여부
                       white # 텍스트 컬러
                       )
    
    # 배경을 그려주기 전에 해야함
    all_sprites.update() # 논리적으로 캐릭터들의 좌표이동이 발생
    
    # 배경도 위치 업데이트를 해줌(배경 스크롤)
    back_y_pos += scroll_speed # 스크롤
    if(back_y_pos >= 0):
        back_y_pos = 0
    
    # 충돌 체크
    if pygame.sprite.spritecollide(player, enemy_sprites, True): # 주인공들과 적들이 충돌이 일어남
        for enemy in enemy_sprites:
            enemy.kill() # 화면에 있는 적들 클리어
            
        life -= 1           # 목숨 -1
        if(life == 0):      # 목숨 3개를 다 쓰면
            running = False # 게임 종료
    
    # 플레이어가 발사한 총알에 적들이 맞은 경우(적들과 총알의 충돌 감지)
    hits =  pygame.sprite.groupcollide(bullet_sprites, enemy_sprites, True, True) # 충돌을 했다면 몇 개 충돌?
    for hit in hits:
        hit.kill()
        score += 10        
    
    # screen.fill(black) # 알아서 배경을 blit함 // 아직 화면에 나온 상태는 아니고 메모리 상에만 존재함
    # 배경을 그려줌
    screen.blit(background, (0,back_y_pos))    
    
    # screen.blit(background)
    all_sprites.draw(screen) # 모든 스프라이트들을 메모리 서피스에 그려줌
    screen.blit(text, (0,0)) 

    # pygame.display.update() # mainSurface의 부분만을 화면에 다시 출력 
    pygame.display.flip()   # mainSurface 전체를 화면에 출력