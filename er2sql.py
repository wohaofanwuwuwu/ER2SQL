#导入所需的模块
import sys

from turtle import width
import pygame

pygame.init()

SIZE = (1000,600)
back_ground_color = (187,212,212)
seperate_line_color = (255,255,255)
f = pygame.font.Font('C:/Windows/Fonts/simhei.ttf',50)
substance_color = (86,108,111)

screen = pygame.display.set_mode(SIZE)

pygame.display.set_caption('From er diagram to sql phrase')

screen.fill(back_ground_color)
pygame.display.flip()

pygame.draw.line(screen,seperate_line_color,(200,0),(200,600),width=3)
pygame.draw.rect(screen,substance_color , pygame.Rect(30, 30, 140, 60))
points = [(30, 240), (100, 190), (170, 240), (100, 290)]
pygame.draw.polygon(screen,substance_color,points)
pygame.draw.ellipse(screen,substance_color,pygame.Rect(30, 380, 150, 70))


# 固定代码段，实现点击"X"号退出界面的功能，几乎所有的pygame都会使用该段代码
while True:
    # 循环获取事件，监听事件状态
    for event in pygame.event.get():
        # 判断用户是否点了"X"关闭按钮,并执行if代码段
        if event.type == pygame.QUIT:
            #卸载所有模块
            pygame.quit()
            #终止程序，确保退出程序
            sys.exit()
    pygame.display.flip() 