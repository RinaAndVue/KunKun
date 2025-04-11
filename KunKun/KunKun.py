import time
import configparser
import sys
import random
import threading
import pygame
from pygame.locals import *
import moviepy.editor as mpy

import lottery

# 窗口大小
width, height = 1400, 800

# 窗口标题
caption = "坤坤抽奖机"

# 窗口图标
icon_png = pygame.image.load("assets\\image\\ico\\icon.jpg")

# 版本号
version = "v1.1"



class Main():
    # 多线程播放音频
    def audio_(self,path):
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
    # 处理文字
    def screen_text(self, text, x, y, fonts=None, RGB=(0,0,0)):
        if fonts == None:
            fonts = self.font_noto_50
        text_surface = fonts.render(str(text), True, RGB)  # 白色文字
        self.screen.blit(text_surface, (x, y))

    def quit_normal(self):
        with open("config\\config.ini",'w') as configfile:
            self.config.write(configfile)
        pygame.quit()
        sys.exit(0)

    def Under_load(self):
        # 初始化pygame
        pygame.init()
        pygame.mixer.init()
        # 设置字体
        self.font_normal = pygame.font.Font(None, 30)  # None 默认字体，30 字体大小
        self.font_noto_50 = pygame.font.Font("assets\\fonts\\noto.ttf", 50)
        self.font_noto_bold_50 = pygame.font.Font("assets\\fonts\\noto_bold.ttf", 50)
        self.font_douyu_50 = pygame.font.Font("assets\\fonts\\DouYu.otf", 50)
        self.font_douyu_100 = pygame.font.Font("assets\\fonts\\DouYu.otf", 100)

        # 初始化坤坤视频
        self.clip = mpy.VideoFileClip("assets/videos/JiNiTaiMei.mp4")
        self.clip_resized = self.clip.resize(newsize=(width / 2, height / 2))
        self.fps = self.clip.fps

        # 加载图片
        self.KunKun_image_1 = pygame.image.load('assets\\image\\KunKun1.png')
        self.KunKun_image_2 = pygame.image.load('assets\\image\\But.png')

        # 读取名字目录文件
        F = open('name\\name.txt',encoding="utf-8")
        line = F.readline().strip()
        self.name_list = []
        self.name_list.append(line)
        while line:
            line = F.readline().strip()
            self.name_list.append(line)
        F.close()
        self.name_list.pop()

        self.loaded = True

    def loading(self):
        # 读取配置文件
        self.config = configparser.ConfigParser()
        try:
            self.config.read("config\\config.ini")
            # 启动动画
            self.animation = self.config["DEFAULT"]['animation']
            # 动态概率
            self.dynamical_probability = self.config["DEFAULT"]['dynamical_probability']
            # 声音
            self.audio = self.config["DEFAULT"]['audio']
            #权重大小
            self.weight_size = int(self.config["DEFAULT"]['weight_size'])
            #权重上限
            self.weight_max = int(self.config["DEFAULT"]['weight_max'])
            #代入变量
            self.config["DEFAULT"] = {
                'animation': self.animation,
                'audio': self.audio,
                'dynamical_probability': self.dynamical_probability,
                'weight_size': self.weight_size,
                'weight_max': self.weight_max

            }
        except:
            self.config["DEFAULT"] = {
                'animation': 'True',
                'audio': 'Ture',
                'dynamical_probability': 'True',
                'weight_size': 1,
                'weight_max': 0
            }
            with open('config\\config.ini','w') as configfile:
                self.config.write(configfile)
            self.animation = "True"

        self.loaded = False
        # 创建一个时钟对象来控制帧率
        self.clock = pygame.time.Clock()
        # 窗口大小
        self.screen = pygame.display.set_mode((width, height))
        # 窗口标题
        pygame.display.set_caption(caption)
        # 窗口图标
        pygame.display.set_icon(icon_png)
        # 加载线程
        thread = threading.Thread(target=game.Under_load)
        thread.start()
        if self.animation == "True":
            # 坤神图片加载背景
            kunshen_image = pygame.image.load("assets/image/background/kunshen.png")
            kunshen = pygame.transform.scale(kunshen_image, (width,height))
            surface = pygame.Surface(kunshen.get_size())
            # 坤坤加载界面
            for i in range (0, 255, 2):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # 退出程序
                        pygame.quit()
                        sys.exit(0)
                self.screen.fill((0, 0, 0))
                surface.set_alpha(i)
                surface.blit(kunshen, (0, 0))
                self.screen.blit(surface, (0, 0))
                pygame.display.flip()
                self.clock.tick(60)
            time.sleep(3)
            for i in range (255, 0, -2):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # 退出程序
                        pygame.quit()
                        sys.exit(0)
                self.screen.fill((0, 0, 0))
                surface.set_alpha(i)
                surface.blit(kunshen, (0, 0))
                self.screen.blit(surface, (0, 0))
                pygame.display.flip()
                self.clock.tick(60)

            time.sleep(2)

        while self.loaded == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # 退出程序
                    pygame.quit()
                    sys.exit(0)
        
        game.report_page()
        
    def report_page(self):
        report = lottery.load_name_error(self.name_list)
        RGB_1 = (255, 255, 255)
        RGB_2 = (0, 0, 0)
        if report:
            runing = True
            while runing:
                for event in pygame.event.get():
                    RGB_1 = (255, 255, 255)
                    RGB_2 = (0, 0, 0)
                    if event.type == pygame.QUIT:
                        runing = False
                        # 退出pygame
                        game.quit_normal()
                    elif event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                        # 检测鼠标位置并触发颜色变化
                        x, y = event.pos
                        # 确定
                        if (width - 250) / 2 <= x <= (width - 250) / 2 +250 and height / 2 + 150 <= y <= height / 2 + 250:
                            RGB_1 = (255, 215, 0)
                            RGB_2 = (255, 255, 255)
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                time.sleep(0.2)
                                runing=False

                self.screen_text('警告：姓名序列出现变化，已重新校对。', 300, 200,RGB=(255, 255, 255))
                pygame.draw.rect(self.screen, RGB_1, ((width - 250) / 2, height / 2 + 150, 250, 100))
                game.screen_text("确定", (width - 100) / 2, height / 2 + 170, fonts=self.font_noto_bold_50, RGB=RGB_2)

                # 刷新屏幕
                pygame.display.flip()
                # 限制帧率为60帧
                self.clock.tick(60)
        game.main_loop()

    def lottery_page(self):
                #抽奖线程
        self.lottery_succeed = False
        thread = threading.Thread(target=game.lotterying)
        thread.start()

        #页面
        RGB_1 = (255, 255, 255)
        RGB_2 = (0, 0, 0)
        runing = True
        if self.animation == 'False':
            while runing:
                for event in pygame.event.get():
                    RGB_1 = (255, 255, 255)
                    RGB_2 = (0, 0, 0)
                    if event.type == pygame.QUIT:
                        runing = False
                        # 退出pygame
                        game.quit_normal()
                    elif (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN) and self.lottery_succeed:
                        # 检测鼠标位置并触发颜色变化
                        x, y = event.pos
                        # 确定
                        if (width - 250) / 2 <= x <= (width - 250) / 2 +250 and height / 2 + 150 <= y <= height / 2 + 250:
                            RGB_1 = (255, 215, 0)
                            RGB_2 = (255, 255, 255)
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                time.sleep(0.2)
                                runing=False

                # 刷新背景
                game.draw_gradient(self.screen, (255, 200, 250), (0, 0, 200))

                if self.lottery_succeed == False:                
                    self.screen_text('正在抽取中', 300, 200,RGB=(0, 0, 0))

                elif self.lottery_succeed:
                    self.screen_text('抽取成功：', 300, 200,RGB=(0, 0, 0))
                    self.screen_text(self.lottery_name, 300, 300,RGB=(255, 215, 0),fonts=self.font_douyu_100)
                    pygame.draw.rect(self.screen, RGB_1, ((width - 250) / 2, height / 2 + 150, 250, 100))
                    game.screen_text("确定", (width - 100) / 2, height / 2 + 170, fonts=self.font_noto_bold_50, RGB=RGB_2)

                # 刷新屏幕
                pygame.display.flip()
                # 限制帧率为60帧
                self.clock.tick(60)

            game.lotteryed_page()
            

        else:
            game.lottery_page_2()
        
    def lotterying(self):
        # 如果动态概率设为开启：
        if self.dynamical_probability == 'True':
            self.lottery_name = lottery.lottery(self.name_list, self.weight_size, self.weight_max)
            # 否则使用传统方法进行抽取
        else:
            self.lottery_name = self.name_list[random.randint(0, len(self.name_list)-1)]
        self.lottery_succeed = True

    def lottery_page_2(self):
            

        # --- 动画效果 --- #
        # 当正式使用时替换为字符串类型
        if self.animation:
            image = pygame.image.load("assets/image/But.png")
            But = pygame.transform.scale(image, (width,height))
            self.screen.fill((0, 0, 0))
            self.screen.blit(But, (0, 0))
            pygame.display.flip()
            if self.audio == 'True':
                thread = threading.Thread(target=game.audio_, args=("assets/audios/THEWORLD.mp3",))
                thread.start()

            for i in range(0, 30):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # 退出pygame
                        game.quit_normal()
                time.sleep(0.1)

            names = 0
            for times in range(1, 30):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # 退出pygame
                        game.quit_normal()
                self.screen.fill((0, 0, 0))
                self.screen_text('这次会是谁呢：', 300, 200,RGB=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                if names == len(self.name_list) - 1:
                    names = 0
                self.screen_text(self.name_list[names], 300, 300,RGB=(255, 215, 0),fonts=self.font_douyu_100)
                time.sleep(times * 0.01)
                pygame.display.flip()
                names += 1
                self.clock.tick(60)
            

            if self.audio == 'True':
                thread = threading.Thread(target=game.audio_, args=("assets/audios/END.wav",))
                thread.start()

            runing_2 = True
            RGB_1 = (255, 215, 0)
            RGB_2 = (255, 255, 255)
            while runing_2:
                for event in pygame.event.get():
                    RGB_1 = (255, 215, 0)
                    RGB_2 = (255, 255, 255)
                    if event.type == pygame.QUIT:
                        runing_2 = False
                        # 退出pygame
                        game.quit_normal()
                    elif event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                        # 检测鼠标位置并触发颜色变化
                        x, y = event.pos
                        # 确定
                        if (width - 250) / 2 <= x <= (width - 250) / 2 +250 and height / 2 + 150 <= y <= height / 2 + 250:
                            RGB_1 = (255, 215, 0)
                            RGB_2 = (255, 255, 255)
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                time.sleep(0.2)
                                runing_2=False
                self.screen.fill((0, 0, 0))
                self.screen_text('就是你啦！', 300, 200,RGB=(255, 255, 255))
                self.screen_text(self.lottery_name, 300, 300,RGB=(255, 215, 0),fonts=self.font_douyu_100)
                pygame.draw.rect(self.screen, RGB_1, ((width - 250) / 2, height / 2 + 150, 250, 100))
                game.screen_text("确定", (width - 100) / 2, height / 2 + 170, fonts=self.font_noto_bold_50, RGB=RGB_2)
                pygame.display.flip()
                self.clock.tick(60)
                
        game.lotteryed_page()
        

    def lotteryed_page(self):
        RGB_1 = (255, 255, 255)
        RGB_2 = (0, 0, 0)
        runing = True
        while runing:
            for event in pygame.event.get():
                RGB_1 = (255, 255, 255)
                RGB_2 = (0, 0, 0)
                if event.type == pygame.QUIT:
                    runing = False
                    # 退出pygame
                    game.quit_normal()
                elif event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                    # 检测鼠标位置并触发颜色变化
                    x, y = event.pos
                    # 确定
                    if (width - 250) / 2 <= x <= (width - 250) / 2 +250 and height / 2 + 150 <= y <= height / 2 + 250:
                        RGB_1 = (255, 215, 0)
                        RGB_2 = (255, 255, 255)
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            time.sleep(0.2)
                            runing=False
            
            game.draw_gradient(self.screen, (255, 200, 250), (0, 0, 200))

            self.screen_text('抽取结果：', 500, 200,RGB=(0, 0, 0))
            self.screen_text(self.lottery_name, 500, 300,RGB=(255, 215, 0))
            pygame.draw.rect(self.screen, RGB_1, ((width - 250) / 2, height / 2 + 150, 250, 100))
            game.screen_text("确定", (width - 100) / 2, height / 2 + 170, fonts=self.font_noto_bold_50, RGB=RGB_2)

            # 刷新屏幕
            pygame.display.flip()
            # 限制帧率为60帧
            self.clock.tick(60)
            

    def start_page(self):
        # 初始化按钮颜色
        home_text_RGB_1 = (0,0,0)
        RGB_1 = (255, 255, 255)
        RGB_2 = (0, 0, 0)
        runing = True
        while runing:
            for event in pygame.event.get():
                RGB_1 = (255, 255, 255)
                RGB_2 = (0, 0, 0)
                # 初始化按钮颜色
                home_text_RGB_1 = (0,0,0)
                if event.type == pygame.QUIT:
                    runing = False
                    # 退出pygame
                    game.quit_normal()
                elif event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                    # 检测鼠标位置并触发颜色变化
                    x, y = event.pos
                    # 返回
                    if 30 <= x <= 150 and 30 <= y <= 80:
                        home_text_RGB_1 = (255, 215, 0)
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            time.sleep(0.2)
                            home_text_RGB_1 = (100,100,100)
                            runing = False
                    # 开始抽奖
                    if (width - 250) / 2 <= x <= (width - 250) / 2 +250 and height / 2 + 150 <= y <= height / 2 + 250:
                        RGB_1 = (255, 215, 0)
                        RGB_2 = (255, 255, 255)
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            time.sleep(0.2)
                            game.lottery_page()
                            

            # 刷新背景
            game.draw_gradient(self.screen, (255, 200, 250), (0, 0, 200))

            image_width, image_height = self.KunKun_image_1.get_size()
            
            self.screen.blit(self.KunKun_image_1, ((width - image_width) / 2, (height - image_height) / 4))
            pygame.draw.rect(self.screen, RGB_1, ((width - 250) / 2, height / 2 + 150, 250, 100))
            game.screen_text("开始抽奖", (width - 200) / 2, height / 2 + 170, fonts=self.font_noto_bold_50, RGB=RGB_2)


            
            game.screen_text("返回", 30, 30, self.font_douyu_50, home_text_RGB_1)
            
            # 刷新屏幕
            pygame.display.flip()
            # 限制帧率为60帧
            self.clock.tick(60)

    # 主循环函数
    def main_loop(self):
        # 初始化按钮颜色
        home_text_RGB_1 = (0, 0, 0)
        home_text_RGB_2 = (0, 0, 0)
        home_text_RGB_3 = (0, 0, 0)
        home_text_RGB_4 = (0, 0, 0)
        home_text_RGB_5 = (255, 182, 193)

        runing = True
        while runing:
            for frame in self.clip_resized.iter_frames(fps=self.fps, dtype="uint8"):
                for event in pygame.event.get():
                    # 初始化按钮颜色
                    home_text_RGB_1 = (0, 0, 0)
                    home_text_RGB_2 = (0, 0, 0)
                    home_text_RGB_3 = (0, 0, 0)
                    home_text_RGB_4 = (0, 0, 0)
                    home_text_RGB_5 = (255, 182, 193)
                    if event.type == pygame.QUIT:
                        runing = False
                        # 退出pygame
                        game.quit_normal()
                    elif event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                        # 检测鼠标位置并触发颜色变化
                        x, y = event.pos
                        # 开始抽奖
                        if (width / 4 - 160) <= x <= (width / 4 - 160) + 250 and (height / 2 - 100) <= y <= (height / 2 - 100) + 50:
                            home_text_RGB_1 = (255, 215, 0)
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                time.sleep(0.2)
                                home_text_RGB_1 = (100,100,100)
                                game.start_page()
                        # 设置
                        elif (width / 4 - 180) <= x <= (width / 4 - 180) + 120 and (height / 2 - 0) <= y <= (height / 2 - 0) + 50:
                            home_text_RGB_2 = (255, 215, 0)
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                time.sleep(0.2)
                                home_text_RGB_2 = (100,100,100)
                                game.setting_page()
                        #  说明
                        elif (width / 4 - 200) <= x <= (width / 4 - 200) + 120 and (height / 2 + 100) <= y <= (height / 2 + 100) + 50:
                            home_text_RGB_3 = (255, 215, 0)
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                time.sleep(0.2)
                                home_text_RGB_3 = (100,100,100)
                                game.listen_page()
                        # 制作人员
                        elif (width / 4 - 220) <= x <= (width / 4 - 220) + 250 and (height / 2 + 200) <= y <= (height / 2 + 200) + 50:
                            home_text_RGB_4 = (255, 215, 0)
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                time.sleep(0.2)
                                home_text_RGB_4 = (100,100,100)
                                game.staff_page()
                        # 不要点我
                        elif (width / 4 - 240) <= x <= (width / 4 - 240) + 250 and (height / 2 + 300) <= y <= (height / 2 + 300) + 50:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if self.audio == "True":
                                    thread = threading.Thread(target=game.audio_, args=("assets/audios/NiGanMa.mp3",))
                                    thread.start()
                        # 退出
                        elif (width - 180) <= x <= (width - 180) + 120 and (height - 100) <= y <= (height - 100) + 50:
                            home_text_RGB_5 = (255, 215, 0)
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                time.sleep(0.2)
                                home_text_RGB_5 = (100,100,100)
                                game.quit_normal()
                                
                # 刷新背景
                game.draw_gradient(self.screen, (255, 200, 250), (0, 0, 200))

                # 坤坤视频
                # 转换帧为 pygame 格式的 Surface 并显示
                frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                self.screen.blit(frame_surface, (width / 2 - 50, height / 4))
    
                # 示例：
                # game.screen_text("开始抽奖", 0, 0, fonts=self.font_noto_70, RGB=(100, 100, 100))
                game.screen_text("坤坤抽奖机", width / 8 - 100, height / 8 - 20, self.font_douyu_100, RGB=(255, 215, 0))
                game.screen_text("开始抽奖", width / 4 - 160, height / 2 - 100, self.font_douyu_50, home_text_RGB_1)
                game.screen_text("设置", width / 4 - 180, height / 2 - 0, self.font_douyu_50, home_text_RGB_2)
                game.screen_text("说明", width / 4 - 200, height / 2 + 100, self.font_douyu_50, home_text_RGB_3)
                game.screen_text("制作人员", width / 4 - 220, height / 2 + 200, self.font_douyu_50, home_text_RGB_4)
                game.screen_text("不要点我", width / 4 - 240, height / 2 + 300, self.font_douyu_50, RGB=(255, 0, 0))
                game.screen_text(f"version : {version}", 0, height - 20, self.font_normal, RGB=(100, 100, 100))

                
                game.screen_text("退出", width - 180, height - 100, self.font_douyu_50, home_text_RGB_5)
            
                # 刷新屏幕
                pygame.display.flip()
                # 限制帧率为60帧
                self.clock.tick(60)

        # 退出pygame
        pygame.quit()
        sys.exit(0)

    def setting_page(self):
            # 行间距
            h = 130
            # 初始化按钮颜色
            home_text_RGB_1 = (0,0,0)
            runing = True
            while runing:
                for event in pygame.event.get():
                    # 初始化按钮颜色
                    home_text_RGB_1 = (0,0,0)
                    if event.type == pygame.QUIT:
                        time.sleep(0.2)
                        runing = False
                        # 退出pygame
                        game.quit_normal()
                        
                    elif event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                        # 检测鼠标位置并触发颜色变化
                        x, y = event.pos
                        # 返回
                        if 30 <= x <= 150 and 30 <= y <= 80:
                            home_text_RGB_1 = (255, 215, 0)
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                time.sleep(0.2)
                                home_text_RGB_1 = (100,100,100)
                                runing = False
                        # 启动动画
                        if (width / 8 + 230) <= x <= (width / 8 + 230) + 30 and (height / 8 + 15) <= y <= (height / 8 + 15) + 30:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if self.animation == "False":
                                    self.animation = "True"
                                    self.config["DEFAULT"]['animation'] = "True"
                                else:
                                    self.animation = "False"
                                    self.config["DEFAULT"]['animation'] = "False"
                        # 声音
                        if (width / 8 + 230) <= x <= (width / 8 + 230) + 30 and (height / 8 + 15 + h) <= y <= (height / 8 + 15 + h) + 30:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if self.audio == "False":
                                    self.audio = "True"
                                    self.config["DEFAULT"]['audio'] = "True"
                                else:
                                    self.audio = "False"
                                    self.config["DEFAULT"]['audio'] = "False"
                        # 动态概率
                        if (width / 8 + 230) <= x <= (width / 8 + 230) + 30 and (height / 8 + 15 + 2 * h) <= y <= (height / 8 + 15 + 2 * h) + 30:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if self.dynamical_probability == "False":
                                    self.dynamical_probability = "True"
                                    self.config["DEFAULT"]['dynamical_probability'] = "True"
                                else:
                                    self.dynamical_probability = "False"
                                    self.config["DEFAULT"]['dynamical_probability'] = "False"
                                
                                    
                # 刷新背景
                game.draw_gradient(self.screen, (255, 255, 255), (255, 255, 255))
                    
                # 文字
                game.screen_text("设置", width / 2 - 120, 20, self.font_douyu_50, RGB=(100, 100, 100))

                # 按钮
                # 启动动画
                
                game.screen_text("动画效果", width / 8, height / 8, self.font_noto_50)
                pygame.draw.rect(self.screen, (0, 0, 0), (width / 8 + 230, height / 8 + 15, 30, 30))
                pygame.draw.rect(self.screen, (255, 255, 255), (width / 8 + 235, height / 8 + 20, 20, 20))
                if self.animation == "True":
                    pygame.draw.rect(self.screen, (0, 0, 0), (width / 8 + 240, height / 8 + 25, 10, 10))
                # 介绍
                game.screen_text("注：启动动画与抽取动画", width / 8 + 50, height / 8 + 50, self.font_noto_50, RGB=(100, 100, 100))

                # 动态概率
                game.screen_text("声音", width / 8, height / 8 + h, self.font_noto_50)
                pygame.draw.rect(self.screen, (0, 0, 0), (width / 8 + 230, height / 8 + 15 + h, 30, 30))
                pygame.draw.rect(self.screen, (255, 255, 255), (width / 8 + 235, height / 8 + 20 + h, 20, 20))
                if self.audio == "True":
                    pygame.draw.rect(self.screen, (0, 0, 0), (width / 8 + 240, height / 8 + 25 + h, 10, 10))
                # 介绍
                game.screen_text("注：是否禁音", width / 8 + 50, height / 8 + 50 + h, self.font_noto_50, RGB=(100, 100, 100))

                # 动态概率
                game.screen_text("动态概率", width / 8, height / 8 + 2 * h, self.font_noto_50)
                pygame.draw.rect(self.screen, (0, 0, 0), (width / 8 + 230, height / 8 + 15 + 2 * h, 30, 30))
                pygame.draw.rect(self.screen, (255, 255, 255), (width / 8 + 235, height / 8 + 20 + 2 * h, 20, 20))
                if self.dynamical_probability == "True":
                    pygame.draw.rect(self.screen, (0, 0, 0), (width / 8 + 240, height / 8 + 25 + 2 * h, 10, 10))
                # 介绍
                game.screen_text("注：实现更公平化的抽取", width / 8 + 50, height / 8 + 50 + 2 * h, self.font_noto_50, RGB=(100, 100, 100))

                

                # 权重大小（整数）
                game.screen_text("权重大小(在配置文件中修改)", width / 8, height / 8 + 3 * h, self.font_noto_50)

                game.screen_text("注：值越高动态概率的质量越高，但性能要求更高", width / 8 + 50, height / 8 + 50 + 3 * h, self.font_noto_50, RGB=(100, 100, 100))
                

                # 权重大小（整数）
                game.screen_text("权重上限(在配置文件中修改)", width / 8, height / 8 + 4 * h, self.font_noto_50)

                game.screen_text("注：值越高对动态概率的限制更少，但性能要求更高", width / 8 + 50, height / 8 + 50 + 4 * h, self.font_noto_50, RGB=(100, 100, 100))
               

                game.screen_text("返回", 30, 30, self.font_douyu_50, home_text_RGB_1)
                
                # 刷新屏幕
                pygame.display.flip()
                # 限制帧率为60帧
                self.clock.tick(60)

    def listen_page(self):
        # 初始化按钮颜色
        home_text_RGB_1 = (0,0,0)
        runing = True
        while runing:
            for event in pygame.event.get():
                # 初始化按钮颜色
                home_text_RGB_1 = (0,0,0)
                if event.type == pygame.QUIT:
                    time.sleep(0.2)
                    runing = False
                    # 退出pygame
                    game.quit_normal()
                elif event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                    # 检测鼠标位置并触发颜色变化
                    x, y = event.pos
                    # 返回
                    if 30 <= x <= 150 and 30 <= y <= 80:
                        home_text_RGB_1 = (255, 215, 0)
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            time.sleep(0.2)
                            home_text_RGB_1 = (100,100,100)
                            runing = False

            # 刷新背景
            game.draw_gradient(self.screen, (255, 200, 250), (0, 0, 200))
                    
            # 文字
            game.screen_text("说明", width / 2 - 120, 20, self.font_douyu_50, RGB=(100, 100, 100))
            game.screen_text("    坤坤抽奖机是一款用于随机抽取人员姓名的小工具。",width / 10, height / 6, self.font_noto_50)
            game.screen_text("它特别适合在需要公平选择某人参加活动、取奖励或分",width / 10, height / 6 + 1 * 60, self.font_noto_50)
            game.screen_text("组时使用，领可以避免人工选择的主观偏差。",width / 10, height / 6 + 2 * 60, self.font_noto_50)
            game.screen_text("应用场景：",width / 10, height / 6 + 4 * 60, self.font_noto_50)
            game.screen_text("  活动抽奖",width / 10, height / 6 + 5 * 60, self.font_noto_50)
            game.screen_text("  随机分组",width / 10, height / 6 + 6 * 60, self.font_noto_50)
            game.screen_text("  值日生安排",width / 10, height / 6 + 7 * 60, self.font_noto_50)
            game.screen_text("  教学点名",width / 10, height / 6 + 8 * 60, self.font_noto_50)
                
            game.screen_text("返回", 30, 30, self.font_douyu_50, home_text_RGB_1)
            
            # 刷新屏幕
            pygame.display.flip()
            # 限制帧率为60帧
            self.clock.tick(60)

    def staff_page(self):
        # 初始化按钮颜色
        home_text_RGB_1 = (0,0,0)
        runing = True
        page_long = 0
        while runing:
            for event in pygame.event.get():
                # 初始化按钮颜色
                home_text_RGB_1 = (0,0,0)
                if event.type == pygame.QUIT:
                    time.sleep(0.2)
                    runing = False
                    # 退出pygame
                    game.quit_normal()
                elif event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                    # 检测鼠标位置并触发颜色变化
                    x, y = event.pos
                    # 返回
                    if 30 <= x <= 150 and 30 <= y <= 80:
                        home_text_RGB_1 = (255, 215, 0)
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            time.sleep(0.2)
                            home_text_RGB_1 = (100,100,100)
                            runing = False

            # 刷新背景
            game.draw_gradient(self.screen, (255, 200, 250), (0, 0, 200))
            
            if 200 + 7 * 200 - page_long <= 400:
                page_long = 0
            game.screen_text("总策划：H2Q", width / 3, 100 - page_long, self.font_noto_50)
            game.screen_text("程序设计：H2Q", width / 3, 100 + 1 * 200 - page_long, self.font_noto_50)
            game.screen_text("美术设计：H2Q", width / 3, 100 + 2 * 200 - page_long, self.font_noto_50)
            game.screen_text("场景设计：H2Q", width / 3, 100 + 3 * 200 - page_long, self.font_noto_50)
            game.screen_text("系统架构：H2Q", width / 3, 100 + 4 * 200 - page_long, self.font_noto_50)
            game.screen_text("音效设计：H2Q", width / 3, 100 + 5 * 200 - page_long, self.font_noto_50)
            game.screen_text("后期测试：H2Q", width / 3, 100 + 6 * 200 - page_long, self.font_noto_50)
            game.screen_text("技术支持：H2Q", width / 3, 100 + 7 * 200 - page_long, self.font_noto_50)

            page_long += 1
            
            game.screen_text("返回", 30, 30, self.font_douyu_50, home_text_RGB_1)
            
            # 刷新屏幕
            pygame.display.flip()
            # 限制帧率为60帧
            self.clock.tick(60)

    def draw_gradient(self, screen, color_top, color_bottom):
        for y in range(height):
            # 计算渐变的颜色
            r = color_top[0] + (color_bottom[0] - color_top[0]) * y // height
            g = color_top[1] + (color_bottom[1] - color_top[1]) * y // height
            b = color_top[2] + (color_bottom[2] - color_top[2]) * y // height
            pygame.draw.line(screen, (r, g, b), (0, y), (width, y))
    
    


if __name__ == "__main__":
    game = Main()
    game.loading()