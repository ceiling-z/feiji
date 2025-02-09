from random import *
import random
from time import *
import pygame
from pygame.constants import *

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


#玩家类
class HeroPlane(object):
    def __init__(self,screen):

        # 添加玩家飞机
        self.player = pygame.image.load("./hero1.jpg")

        self.x=240-50
        self.y=600

        # 飞机速度
        self.speed = 10

        #记录当前的窗口对象
        self.screen=screen

        #装子弹的列表
        self.bullets=[]

    def key_control(self):
        # 监听键盘事件
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_w] or key_pressed[K_UP]:
            self.y -= self.speed
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            self.y += self.speed
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            self.x -= self.speed
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            self.x += self.speed
        if key_pressed[K_SPACE]:
            #按下空格发射子弹
            bullet=Bullet(self.screen,self.x,self.y)
            #把子弹放进列表
            self.bullets.append(bullet)


    def display(self):
        # 将玩家飞机贴到窗口上
        self.screen.blit(self.player,(self.x, self.y))
        #遍历所有子弹
        for bullet in self.bullets:
            #让子弹飞控制子弹的y坐标
            bullet.auto_move()
            #让子弹显示在窗口
            bullet.display()


#敌方类
class EnemyPlane(object):
    def __init__(self,screen):

        # 添加玩家飞机
        self.player = pygame.image.load("./enemy.jpg")

        self.x=0
        self.y=0

        # 飞机速度
        self.speed = 10

        # 记录当前的窗口对象
        self.screen = screen

        # 装子弹的列表
        self.bullets = pygame.sprite.Group

        #装子弹的列表
        self.bullets=[]

        #敌机移动方向
        self.direction='right'

    def display(self):
        # 将玩家飞机贴到窗口上
        self.screen.blit(self.player,(self.x, self.y))
        # 遍历所有子弹
        for bullet in self.bullets:
            # 让子弹飞控制子弹的y坐标
            bullet.auto_move()
            # 让子弹显示在窗口
            bullet.display()

    def update(self):
        self.auto_move()
        self.auto_fire()
        self.display()

    def auto_move(self):
        if self.direction=='right':
            self.x+=self.speed
        elif self.direction=='left':
            self.x -= self.speed

        if self.x>480-51:
            self.direction='left'
        elif self.x<0:
            self.direction='right'

    def auto_fire(self):
        """自动开火，创建子弹对象，添加到列表里"""
        random_num=random.randint(1,20)
        if random_num==1:
            bullet=EnemyBullet(self.screen,self.x,self.y)
            self.bullets.append(bullet)


#子弹类
#属性
class Bullet(object):
    def __init__(self,screen,x,y):
        #创建图片
        self.image=pygame.image.load("./bullet.png")

        #坐标
        self.x=x+50-15/2
        self.y=y-15

        #窗口
        self.screen=screen
        #子弹速度
        self.speed=10

    def display(self):
        #显示子弹到窗口
        self.screen.blit(self.image,(self.x,self.y))

    def auto_move(self):
        """让子弹飞 修改子弹的y坐标"""
        self.y-=self.speed


#敌方子弹类
#属性
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        # 创建图片
        self.image = pygame.image.load("./bullet1.png")

        # 坐标
        self.x = x+50/2-8/2
        self.y = y+39

        # 窗口
        self.screen = screen
        # 子弹速度
        self.speed = 10


    def display(self):
        # 显示子弹到窗口
        self.screen.blit(self.image, (self.x, self.y))

    def auto_move(self):
        """让子弹飞 修改子弹的y坐标"""
        self.y += self.speed

#背景音乐类
class GameSound(object):
    def __init__(self):
        pygame.mixer.init()     #初始化背景音乐
        pygame.mixer.music.load("./yinyue.mp3")
        pygame.mixer.music.set_volume(0.5)     #音乐大小

    def playBackgroundMusic(self):
        pygame.mixer.music.play(-1)     #无限循环



def main():
    """完成整个程序的控制"""
    sound=GameSound()
    sound.playBackgroundMusic()

    #创建一个窗口
    screen=pygame.display.set_mode((480,852),0,32)
    #添加背景
    background=pygame.image.load("./th.png")

    #创建一个飞机的对象（窗口）
    player=HeroPlane(screen)
    # 创建一个敌方飞机的对象（窗口）
    enemyplane = EnemyPlane(screen)

    while True:
        # 将背景贴到窗口上
        screen.blit(background, (0, 0))

        #获取事件
        for event in pygame.event.get():
            #判断事件类型
            if event.type==pygame.QUIT:
                #执行推出
                pygame.quit()
                #python程序退出
                exit()

        #执行飞机按键监听
        player.key_control()
        #飞机的显示
        player.display()
        #敌方飞机的显示
        enemyplane.display()
        #敌机自动移动
        enemyplane.auto_move()
        #敌机自动开火
        enemyplane.auto_fire()

        #显示窗口中的内容
        pygame.display.update()
        sleep(0.01)


if __name__=='__main__':
   main()

