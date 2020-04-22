import random
import pygame

# 定义屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 刷新帧率
FRAME_PER_SEC = 60
# 创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprint(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""

    def __init__(self, image_name, speed=1):
        # 调用父类的初始化方法
        super().__init__()
        # 定义对象的属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        # 在屏幕的垂直方向上移动
        self.rect.y += self.speed


class Background(GameSprint):
    """游戏背景精灵"""
    def __init__(self, is_alt=False):
        # 调用父类方法实现精灵的创建（image/rect/speed）
        super().__init__("../素材包/背景图片.png")
        # 判断是否是交替图像，如果是，需要设置初始位置
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        # 调用父类的方法实现
        super().update()
        # 判断是否移出屏幕,如果是，将图像移到屏幕上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprint):
    """敌人飞机精灵"""
    def __init__(self):
        # 调用父类方法，创建敌人飞机精灵，同时指定敌机图片
        super().__init__("../素材包/敌人飞机.png")
        # 指定敌人飞机的初始随即速度
        self.speed = random.randint(1, 3)
        # 指定敌人飞机的初始随即位置
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

    def update(self):
        # 调用父类方法，保持垂直方向的飞行
        super().update()
        # 判断是否飞出屏幕，如果是，需要从精灵组删除敌人飞机
        if self.rect.y >= SCREEN_RECT.height:
            self.kill()

    def __del__(self):
        pass


class Hero(GameSprint):
    """英雄精灵"""
    def __init__(self):
        # 调用父类方法，设置image 和 speed
        super().__init__("../素材包/我方飞机.png", 0)
        # 设置英雄的初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120
        # 创建子弹的精灵组
        self.bullets = pygame.sprite.Group()

    def update(self):
        # 飞机在水平方向移动
        self.rect.x += self.speed
        # 控制飞机在屏幕内移动
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        for i in (0, 1, 2):
            # 创建子弹精灵
            bullet = Bullet()
            # 设置精灵的位置
            bullet.rect.bottom = self.rect.y - i * 20
            bullet.rect.centerx = self.rect.centerx
            # 将精灵添加到精灵组
            self.bullets.add(bullet)


class Bullet(GameSprint):
    """子弹精灵"""
    def __init__(self):
        # 调用父类方法，设置子弹图片，子弹速度
        super().__init__("../素材包/子弹.png", -2)

    def update(self):
        # 调用父类方法，让子弹言垂直方向飞行
        super().update()
        # 判断子弹是否飞出屏幕
        if self.rect.bottom < 0:
            self.kill()
