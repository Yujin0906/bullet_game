'''
pygame
SDL : Simple DirectMedia Layer(Open Source Library)
2D 게임이나 이미지를 지원하는 라이브러리

Bouncing Ball:
'''

import pygame, sys


FR = 60
size = WIDTH, HEIGHT = 640, 480 # size에는 튜플값이 들어감
# size = (640,480)

pygame.init() # pygame 모듈 초기화

# screen : 화면 표시될 최종 Surface 객체
screen = pygame.display.set_mode(size=size)

# clock 객체 생성
clock = pygame.time.Clock()

ball = pygame.image.load('intro_ball.gif') # filepath(파일경로) 이미지가 있는 Surface객체를 반환
ballrect = ball.get_rect() # ball 객체의 위치좌표 값을 가져온다.
speed = [2,2] # 공의 움직이는 속도를 결정할 때 사용


running = True
while running:
    clock.tick(FR) # Frame Rate 설정
    events = pygame.event.get() # 리스트의 형태로 윈도우 및 기타 사용자 이벤트들을 모두 가져옴
    for event in events: # 가져온 모든 이벤트들에 대해 대하여..
        if event.type == pygame.QUIT: # 가져온 이벤트가 QUIT이면 
            running = False
            
    # for 루프를 빠져나와서
    # 이 부분에서 screen 객체위에 무언가를 그린다음, 화면에 출력한다
    
    # 개념적으로(논리적으로) 공의 위치좌표를 바꾸어준다 -> while에서 하는 거임 for 아님!!
    ballrect = ballrect.move(speed) # ballrect 값을 [2,2]만큼 상대적으로 이동시킴
    if ballrect.left < 0 or ballrect.right > WIDTH: # 공이 좌우 끝에 붙었을 경우
        speed[0] = -speed[0] # 부호를 바꾼다는 의미는 방향을 바꾼다는 의미와 같음
        
    if ballrect.top < 0 or ballrect.bottom > HEIGHT: # 공이 상하 끝에 붙었을 경우
        speed[1] = - speed[1] # 부호를 바꾼다는 의미는 방향을 바꾼다는 의미와 같음
        
    # 그려주는 작업... 
    screen.fill((0,0,0)) # 배경을 깔고 싶다? 640x480이미지(Surface)를 로드한 뒤 여기에 blit해주면 배경을 만들 수 있음 // black
    screen.blit(ball, ballrect) # Surface의 blit method는 파라미터로 전달되는 Surface를 screen Surface에 꽝하고 찍어준다(그려준다) 
    
    pygame.display.flip() # 화면을 갱신한다
    
    
    
pygame.quit()             # pygame을 나간다
sys.exit()                # 프로그램도 종료시킨다