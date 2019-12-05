#-*- coding: utf-8 -*-
import pygame
from sys import exit

pygame.init() #初始化pygame
SCREEN_SIZE = (640, 480) #存储屏幕尺寸
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
#创建窗口

my_font = pygame.font.SysFont('arial',16)
#创建字体对象
font_height = my_font.get_linesize()
#得到字体的高度值
text = []

while True:#主循环
    event = pygame.event.wait()#这里用了wait()方法
    text.append(str(event))
    #获得事件的名称
    text = text[-SCREEN_SIZE[1]/font_height:]
    #这个切片操作保证了event_text里面只保留一个屏幕的文字

    if event.type == pygame.QUIT:
        pygame.quit()
        exit()

    screen.fill((255,255,255))

    y = SCREEN_SIZE[1]-font_height
    #找一个合适的起笔位置，最下面开始但是要留一行的空
    for line in reversed(text):#倒序写满整个屏幕的文字
        screen.blit(my_font.render(line, True, (0,0,0)), (0, y))
        #显示字体
        y -= font_height
        #把笔提一行

    pygame.display.update()