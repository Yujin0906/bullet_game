'''
슈퍼마리오의 점프 흉내내기
물리엔진을 구현 ex) 가속도
'''

import pygame

screen_size = WIDTH, HEIGHT = 800, 600

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.image = pygame.Surface((50,50))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_y = 0     # (가)속도
        self.is_jumping = False # 점프 중에 점프 방지
        self.jump_power = -10   # 아래서 위로 올라가는 것은 y좌표의 마이너스 방향임
        self.gravity = 0.5      # 중력의 값
        self.spaceKeyPressed = False # 연속 점프 방지
        
    def chechkJumpOver(self, event):
        if event.type == pygame.KEYUP and self.spaceKeyPressed:
            self.spaceKeyPressed = False
            
    def update(self): # 좌표의 갱신
        # 키 입력 처리
        keys = pygame.key.get_pressed() # 눌린 키 값을 받아옴
        if keys[pygame.K_LEFT]:
            self.rect.x -= 3
        
        if keys[pygame.K_RIGHT]:
            self.rect.x += 3
        
        if keys[pygame.K_SPACE] and not self.is_jumping and not self.spaceKeyPressed:
            self.is_jumping = True
            self.spaceKeyPressed = True
            self.velocity_y = self.jump_power # y축으로 움직일 좌푯값
        
        # 중력 적용
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity_y = 0
            self.is_jumping = False
        
        # 선반이랑 충돌 체크
        hits = pygame.sprite.spritecollide(self, obstacles, False)
        if hits:
            # 일단 선반이랑 충돌은 했다...
            for hit in hits:
                if self.velocity_y > 0: # 캐릭터가 내려오는 중이면...
                    self.rect.y = hit.rect.top - self.rect.height
                    self.velocity_y = 0
                    self.is_jumping = False
                # else:
                #     self.velocity_y = 0
                    
        
        # 게임 화면에서 좌우로 못 벗어나게 함
        if self.rect.left < 0:
            self.rect.left = 0
        
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height) -> None:
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0,0,255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        
    def update(self) -> None:
        # 바닥에 붙어서 좌우로 끝까지 왔다 갔다 이동시키기, 적당한 스피드로
        self.rect.x += self.speed
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed = -self.speed 

class Obstacle(pygame.sprite.Sprite): # 장애물, 선반같은 슈퍼마리오가 올라가는 곳
    def __init__(self,x,y,width,height) -> None:
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 255,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self) -> None: pass

clock = pygame.time.Clock()
screen = pygame.display.set_mode(screen_size)

obs1 = Obstacle(300, 550, 100, 20)
obs2 = Obstacle(400, 500, 100, 20)

player = Player(100, 100)

enemy = Enemy(500, HEIGHT-50, 50, 50)
enemies = pygame.sprite.Group()
enemies.add(enemy)

all_sprites = pygame.sprite.Group()
all_sprites.add(player, obs1, obs2, enemies)

obstacles = pygame.sprite.Group()
obstacles.add(obs1, obs2)

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type ==pygame.KEYUP:
            player.chechkJumpOver(event)
    
    
    all_sprites.update()       
    
    # 충돌 체크
    if pygame.sprite.spritecollide(player, enemies, True):
        running = False 
    
    # 배경 그림
    screen.fill((255,255,255))
    all_sprites.draw(screen)
    
    pygame.display.flip()

pygame.quit()