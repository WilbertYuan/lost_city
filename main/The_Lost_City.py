from http import client
from pickle import TRUE
from re import T
import sys
from xml.etree.ElementTree import TreeBuilder
import pygame
from settings import Settings
from pygame import locals
from PIL import Image
import json
import socket
import tkinter as tk
import select
import socketserver
import time
import threading
import screen_adjust
from unittest.mock import NonCallableMagicMock
import pygame.font
import random

class LostCity:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        screen_adjust.screen_adjust()
        pygame.init()
        pygame.font.init()

        with open('json/surface_3.json',"r",encoding='utf8') as f:
            self.surface_json:dict = json.load(f)
        with open('json/surface_point_3.json',"r",encoding='utf8') as g:
            self.surface_point_json:dict = json.load(g)
        with open('json/number_3.json',"r",encoding='utf8') as h:
            self.number_json:dict = json.load(h)
        with open('json/point.json',"r",encoding='utf8') as p:
            self.point_json:dict = json.load(p)
        with open('json/surface_point_player_3.json',"r",encoding='utf8') as q:
            self.surface_point_player_json:dict = json.load(q)
        self.clock = pygame.time.Clock()
        self.settings=Settings()

        self.icon = pygame.image.load('images/lost_city.png') 
        pygame.display.set_icon(self.icon)

        self.screen = pygame.display.set_mode(
            (self.settings.width_game_screen,self.settings.height_game_screen))
        self.settings.width =  self.screen.get_rect().width
        self.settings.height = self.screen.get_rect().height
        self._image_events()
        self.active()
        self.mouse_click_pos = (-1,-1)
        self.mouse_pos = (-1,-1)
        self.player=''
        pygame.display.set_caption("Lost City")

        self.font=pygame.font.Font('TTF/COOPBL.TTF',36)
        self.font_2=pygame.font.Font('TTF/COOPBL.TTF',66)
        self.font_3=pygame.font.Font('TTF/COOPBL.TTF',36)



        #------------------------------------------自我认定变量
        self.i_am = 0
        #------------------------------------------是否已自我认定
        self.i_have_known_myself = False
        #------------------------------------------客户总数
        self.client_number = 0
        #------------------------------------------客户端决定是否发送命令
        self.CLIENT_whether_command = False
        # #------------------------------------------客户端传送命令--字典：{“str”：[int,int]}
        self.have_calculated_number = 0
        #------------------------------------------已清算的回合数
        self.limit = False
        self.i_think = 0

        self.flush = False
        self.co = {"class1":"round&client_number&time",
                   "data1":[3,0],
                   "class2":"round&client_number&time",
                   "data2":[3,0],
                   "class3":"round&client_number&time",
                   "data3":[3,0],
                   "class4":"round&client_number&time",
                   "data4":[3,0],
                   "class5":"round&client_number&time",
                   "data5":[3,0]}#---------------------------客户端命令初始化

        self.click_point = 0

        self.x = 0
        # # 跳动字符状态
        # self.word_1=True
        # self.word_2=False
        # self.word_3=False
        self.ipv4 = ''
        self.ipv4_entry:tk.Entry
        self.window = tk.Tk()

        self.total_info = {
            "1":[0,4,0,0,0,0,0,0,0,0],
            "2":[0,4,0,0,0,0,0,0,0,0],
            "3":[0,4,0,0,0,0,0,0,0,0],
            "4":[0,4,0,0,0,0,0,0,0,0],
            "5":[0,4,0,0,0,0,0,0,4,0],
            "6":[0,4,0,0,0,0,0,0,0,0],
            "7":[0,4,0,0,0,0,0,0,0,0],
            "8":[0,4,0,0,0,0,0,0,0,0],
            "9":[0,4,0,0,0,0,0,0,0,0],
            "10":[0,4,0,0,0,0,0,0,0,0],
            "11":[0,4,0,0,0,0,0,0,0,0],
            "12":[0,4,0,0,0,0,0,0,0,0],
            "13":[0,4,0,0,0,0,0,0,0,0],
            "14":[0,4,0,0,0,0,0,0,0,0],
            "15":[0,4,0,0,0,0,0,0,0,0],
            "16":[0,4,0,0,0,0,0,0,0,0],
            "17":[0,4,0,0,0,0,0,0,0,0],
            "18":[0,4,0,0,0,0,0,0,0,0],
            "19":[0,4,0,0,0,0,0,0,0,0],
            "20":[0,4,0,0,0,0,0,0,0,0],
            "21":[0,4,0,0,0,0,0,0,0,0],
            "22":[0,4,0,0,0,0,0,0,0,0],
            "23":[0,4,0,0,0,0,0,0,0,0],
            "24":[0,4,0,0,0,0,0,0,0,0],
            "25":[0,4,0,0,0,0,0,0,0,0],
            "26":[0,4,0,0,0,0,0,0,0,0],
            "27":[0,4,0,0,0,0,0,0,0,0],
            "28":[0,4,0,0,0,0,0,0,0,0],
            "29":[0,4,0,0,0,0,0,0,0,0],
            "30":[0,4,0,0,0,0,0,0,0,0],
            "31":[0,4,0,0,0,0,0,0,0,0],
            "32":[0,4,0,0,0,0,0,0,0,0],
            "33":[0,4,0,0,0,0,0,0,0,0],
            "34":[0,4,0,0,0,0,0,0,0,0],
            "35":[0,4,0,0,0,0,0,0,0,0],
            "36":[0,4,0,0,0,0,0,0,0,0],
            "37":[0,4,0,0,0,0,0,0,0,0],
            "38":[0,4,0,0,0,0,0,0,0,0],
            "39":[0,4,0,0,0,0,0,0,0,0],
            "40":[0,4,0,0,0,0,0,0,0,0],
            "41":[0,4,0,0,0,0,0,0,0,0],
            "42":[0,4,0,0,0,0,0,0,0,0],
            "43":[0,4,0,0,0,0,0,0,0,0],
            "44":[0,4,0,0,0,0,0,0,0,0],
            "45":[0,4,0,0,0,0,0,0,0,0],
            "46":[0,4,0,0,0,0,0,0,0,0],
            "player1":[200, 0,0,0, 0,0,0,0, 0,0,0,0,0, 0,1, 0],
            "player2":[200, 0,0,0, 0,0,0,0, 0,0,0,0,0, 0,1, 0],
            "player3":[200, 0,0,0, 0,0,0,0, 0,0,0,0,0, 0,1, 0],
            "player4":[200, 0,0,0, 0,0,0,0, 0,0,0,0,0, 0,1, 0],
            "round&client_number&time":[1,0,0,0,0]
        }
        self.send_msg_pre = self.total_info



#在1到45个点中
#第一个参数，0表示空，1，2，3，4表示玩家，5表示战争点，6表示陷阱点，7表示玩家在陷阱中，8表示玩家在隐藏中
#第二个参数，点处于war状态触发，0表示无法设置战争点，3表示战争状态还剩3回合，4表示可放置战争点
#第三个参数，点处于trap状态触发，0表示该点没有trap
#第4，5，6，7个参数，表示是玩家1，2，3，4设置
#第8个参数，表示玩家1,2,3,4被trap
#第9个参数，表示玩家1,2,3,4于此点隐藏
#第10个参数，表示玩家是否hide，无敌状态

#player里面，数字依次表示money[0],ship_card[1],railway_card[2],road_card[3],war_card[4]
#trap_card[5],hide_card[6],skip_card[7],被trap时间[8],使用trap次数[9],使用war次数[10],使用hide次数[11]
#使用skip次数[12],玩家所在点[13],终点[14],玩家起点[15]  ] = 2 >=


        #音乐初始化
        self.music_file = "music/1698916501000_67tool_01.mp3"
        pygame.mixer.music.load(self.music_file)
        pygame.mixer.music.play(loops=-1)
        self.real = 0 
        self.time_end = 0.0
        self.time_start = 0.0

        self.client = {}

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            #侦听鼠标和键盘事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_click_pos = pygame.mouse.get_pos()
                # if event.type == pygame.K_SPACE:
            if self.button_finish_dark_new_rect.collidepoint(self.mouse_click_pos) and self.game_active_6 == True:
                self.mouse_click_pos = (-1,-1)
                #self._msg_space()
                if self.i_am == 1 and self.total_info['round&client_number&time'][0]%4 == 1:
                    self.mouse_click_pos = (-1,-1)
                    self.flush = True
                    self.mouse_click_pos = (-1,-1)

                if self.i_am == 2 and self.total_info['round&client_number&time'][0]%4 == 2:
                    self.alter_1('round&client_number&time',0,self.total_info['round&client_number&time'][0] + 1)
                    self.flush = True
                    self.mouse_click_pos = (-1,-1)
                if self.i_am == 3 and self.total_info['round&client_number&time'][0]%4 == 3:
                    self.alter_1('round&client_number&time',0,self.total_info['round&client_number&time'][0] + 1)
                    self.flush = True
                    self.mouse_click_pos = (-1,-1)
                if self.i_am == 4 and self.total_info['round&client_number&time'][0]%4 == 0:
                    self.alter_1('round&client_number&time',0,self.total_info['round&client_number&time'][0] + 1)
                    self.flush = True
                    self.mouse_click_pos = (-1,-1)
                self.mouse_click_pos = (-1,-1)


            self._check_button()
            self._blit_events()
            self._highlight_button()
            self._blit_hightlight()
            self.shop_button()
            

            if self.game_active_5 == False:
                self.time_start = time.time()
            if self.game_active_1 == False and self.game_active_2 == False and self.game_active_3 == False and self.game_active_4 == False and self.game_active_5 == False and self.game_active_6 == False:
                self.time_end = time.time()


            if self.game_active_6 or self.game_active_7:
                self.dazhan_shuju()
                if self.i_am == 1:
                    self.calculate()
                self.reset()

            if self.game_active_6 and self.total_info['round&client_number&time'][0]%4 == self.i_am%4 and self.total_info[str(self.total_info[str(self.player)][13])][2] == 0:
                self.click_point_number()
                self._trap_card()
                self._war_card()
                self._hide_card()
                self._skip_card()
                self.reset()
                if self.limit:
                    self._ship_card()
                    self._road_card()
                    self._railway_card()
                    
            
            if self.i_think < self.total_info['round&client_number&time'][0]/4:
                self.i_think += 1
                self.limit = True



            # #print(self.i_think)
            # #print(self.limit)
            #test
            ##print(self.total_info)


            if self.game_active_8:
                self.total_time=int((self.time_start - self.time_end)/60)
                self.jiesuan_shuju()
            self.x += 1
            self.mouse_pos = pygame.mouse.get_pos()
            if(self.game_active_audio == False):
                pygame.mixer.music.stop()
                self.real = 1 
 
            if(self.game_active_audio and self.real):
                self.real = 0
                pygame.mixer.music.play(loops=-1) 
            
            #创建服务器
            if self.game_active_4 and self.game_active_12:#点击创建房间
                list_start = [1,2,3,4]
                list_1=[1,2,3,4,8]
                list_2=[39,41,42,43,44,45,46]
                players=['player1','player2','player3','player4']
                for player in players:
                    right_left=random.randint(0,len(list_start)-1)
                    
                    if list_start[right_left] % 2 == 0:
                        right_left=list_start[right_left]
                        list_start.remove(right_left)

                        start = random.randint(0,len(list_1)-1)
                        start=list_1[start]
                        self.total_info[f'{player}'][13] = start
                        self.total_info[f'{player}'][15] = start
                        if player == 'player1':
                            self.total_info[f'{start}'][0] = 1
                        if player == 'player2':
                            self.total_info[f'{start}'][0] = 2
                        if player == 'player3':
                            self.total_info[f'{start}'][0] = 3
                        if player == 'player4':
                            self.total_info[f'{start}'][0] = 4
                        list_1.remove(start)

                        end = random.randint(0,len(list_2)-1)
                        end=list_2[end]
                        self.total_info[f'{player}'][14] = end
                        list_2.remove(end)                        
                    
                    elif list_start[right_left] % 2 == 1:
                        right_left=list_start[right_left]
                        list_start.remove(right_left)

                        start = random.randint(0,len(list_2)-1)
                        start=list_2[start]
                        self.total_info[f'{player}'][13] = start
                        self.total_info[f'{player}'][15] = start
                        if player == 'player1':
                            self.total_info[f'{start}'][0] = 1
                        if player == 'player2':
                            self.total_info[f'{start}'][0] = 2
                        if player == 'player3':
                            self.total_info[f'{start}'][0] = 3
                        if player == 'player4':
                            self.total_info[f'{start}'][0] = 4
                        list_2.remove(start)

                        end = random.randint(0,len(list_1)-1)
                        end=list_1[end]
                        self.total_info[f'{player}'][14] = end
                        list_1.remove(end)
                self.send_msg_pre = self.total_info        
                #print(self.total_info)        
                self.ipv4 = socket.gethostbyname_ex(socket.gethostname())[2][0]
                #print(self.ipv4)


                self.screen.blit(self.window_matching_new, self.surface_json['window']['window_matching'])

                self.screen.blit(self.words_matching_1_new, self.surface_json['words']['words_matching_1'])

                self.screen.blit(self.button_out_static_new, self.surface_json['button']['button_out_static'])
                HOST = self.ipv4
                PORT = 8000
                BUFSIZE = 1024
                ADDR=(HOST,PORT)
                self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server.bind(ADDR)
                self.data = {'client':{}}
                self.addresses = {}
                threading.Thread(target=run_server, args=(self,)).start()

                self.i_am = 1 #转为player1
                self.i_have_known_myself = True
                self.game_active_12 = False
            if self.game_active_4:
                #绘制ipv4图
                self.ipv4 = socket.gethostbyname_ex(socket.gethostname())[2][0]
                share_ipv4 = self.ipv4
                self.share_ipv4_image = self.font_2.render(share_ipv4,True,
                                                         (255,0,0))
                self.share_ipv4_image_rect = self.share_ipv4_image.get_rect()
                self.share_ipv4_image_rect.x +=int(1227.5*self.settings.RATIO_ALL)
                self.share_ipv4_image_rect.y +=int(270.5*self.settings.RATIO_ALL)
                self.screen.blit(self.share_ipv4_image,self.share_ipv4_image_rect)

                
                        #输入你房间地址高光按钮
            
            #客户端加入
            if self.button_enter_your_room_address_highlight_new_rect.collidepoint(self.mouse_click_pos)  and self.game_active_5 == True: #matching界面        
                self.enter_room()
                self.mouse_click_pos = (-1,-1)
            

            # #print(self.i_am)


            if self.total_info["round&client_number&time"][1] == 2:
                if self.i_have_known_myself == False:
                    self.i_am = 2
                    self.i_have_known_myself = True

            if self.total_info["round&client_number&time"][1] == 3:
                if self.i_have_known_myself == False:
                    self.i_am = 3
                    self.i_have_known_myself = True

            if self.total_info["round&client_number&time"][1] == 4:
                if self.i_have_known_myself == False:
                    self.i_am = 4
                    self.i_have_known_myself = True
            if self.i_am == 2:
                self.player = 'player2'
            elif self.i_am == 3:
                self.player = 'player3'
            elif self.i_am == 4:
                self.player = 'player4'
            elif self.i_am == 1:
                self.player = 'player1'


            if self.i_have_known_myself == True:

                if (self.total_info["round&client_number&time"][1] == 4):    #--------该数字根据玩家数量来更改
        
                    if self.game_active_13:
         
                        self.game_active_4 = False
                        self.game_active_5 = False
                        self.game_active_6 = True
                        self.game_active_13 = False

            self.finale()


            pygame.display.flip()
            self.clock.tick(60)
  
    def active(self):
        self.game_active_1 = True           #封面
        self.game_active_1_1 = False
        self.game_active_1_2 = False
        self.game_active_1_3 = False
        self.game_active_2 = False           #进入界面
        self.game_active_3 = False           #房间选择（建立or加入）界面
        self.game_active_4 = False           #创建房间
        self.game_active_5 = False           #matching界面
        self.game_active_6 = False         #大战界面
        self.game_active_7 = False           #商店界面
        self.game_active_8 = False           #结算界面
        self.game_active_audio = True
        self.game_active_10 = False          #About us
        self.game_active_11= False           #Rules
        self.game_active_12 = True           #只能定义一次服务器
        self.game_active_13 = True           #分界位置过度变量

        self.highlight_active_1 = False
        self.highlight_active_2 = False
        self.highlight_active_3 = False      #button_About_us_static
        self.highlight_active_4 = False      #创建房间高光按钮
        self.highlight_active_5 = False      #加入房间高光按钮
        self.highlight_active_6 = False      #button_open_audio_highlight
        self.highlight_active_7 = False      #button_close_audio_highlight
        self.highlight_active_8 = False
        self.highlight_active_9 = False
        self.highlight_active_10 = False
        self.highlight_active_11= False    
        self.highlight_active_12 = False
        self.highlight_active_13 = False
        self.highlight_active_14 = False
        self.highlight_active_15 = False
        self.highlight_active_16 = False
        self.highlight_active_17 = False
        self.highlight_active_18 = False
        self.highlight_active_19 = False    
        self.highlight_active_20 = False  

        self.railway_active = False
        self.ship_active = False
        self.road_active = False
        self.war_active = False
        self.trap_active = False
        self.hide_active = False
        self.skip_active = False

        self.random_card = 0

    def _image_events(self):


        self.button_finish_shallow = pygame.image.load('images/button_finish_shallow.png')
        self.button_finish_shallow_2 = Image.open('images/button_finish_shallow.png')
        self.button_finish_shallow_width, self.button_finish_shallow_height = self.button_finish_shallow_2.size
        self.button_finish_shallow_new = pygame.transform.scale(surface=self.button_finish_shallow, size=(self.button_finish_shallow_width * self.settings.RATIO_ALL, self.button_finish_shallow_height * self.settings.RATIO_ALL))
        self.button_finish_shallow_new_rect = self.button_finish_shallow_new.get_rect()
        self.screen.blit(self.button_finish_shallow_new, self.surface_json['button']['button_finish_shallow'])
        self.button_finish_shallow_new_rect.x += self.surface_json['button']['button_finish_shallow'][0]
        self.button_finish_shallow_new_rect.y += self.surface_json['button']['button_finish_shallow'][1]


        self.button_finish_dark = pygame.image.load('images/button_finish_dark.png')
        self.button_finish_dark_2 = Image.open('images/button_finish_dark.png')
        self.button_finish_dark_width, self.button_finish_dark_height = self.button_finish_dark_2.size
        self.button_finish_dark_new = pygame.transform.scale(surface=self.button_finish_dark, size=(self.button_finish_dark_width * self.settings.RATIO_ALL, self.button_finish_dark_height * self.settings.RATIO_ALL))
        self.button_finish_dark_new_rect = self.button_finish_dark_new.get_rect()
        self.screen.blit(self.button_finish_dark_new, self.surface_json['button']['button_finish_dark'])
        self.button_finish_dark_new_rect.x += self.surface_json['button']['button_finish_dark'][0]
        self.button_finish_dark_new_rect.y += self.surface_json['button']['button_finish_dark'][1]


        #--------------------------------------------wjq要求的cancel键的使用

        self.button_cancel_shallow = pygame.image.load('images/button_cancel_shallow.png')
        self.button_cancel_shallow_2 = Image.open('images/button_cancel_shallow.png')
        self.button_cancel_shallow_width, self.button_cancel_shallow_height = self.button_cancel_shallow_2.size
        self.button_cancel_shallow_new = pygame.transform.scale(surface=self.button_cancel_shallow, size=(self.button_cancel_shallow_width * self.settings.RATIO_ALL, self.button_cancel_shallow_height * self.settings.RATIO_ALL))
        self.button_cancel_shallow_new_rect = self.button_cancel_shallow_new.get_rect()
        self.screen.blit(self.button_cancel_shallow_new, self.surface_json['button']['button_cancel_shallow'])
        self.button_cancel_shallow_new_rect.x += self.surface_json['button']['button_cancel_shallow'][0]
        self.button_cancel_shallow_new_rect.y += self.surface_json['button']['button_cancel_shallow'][1]


        self.button_cancel_dark = pygame.image.load('images/button_cancel_dark.png')
        self.button_cancel_dark_2 = Image.open('images/button_cancel_dark.png')
        self.button_cancel_dark_width, self.button_cancel_dark_height = self.button_cancel_dark_2.size
        self.button_cancel_dark_new = pygame.transform.scale(surface=self.button_cancel_dark, size=(self.button_cancel_dark_width * self.settings.RATIO_ALL, self.button_cancel_dark_height * self.settings.RATIO_ALL))
        self.button_cancel_dark_new_rect = self.button_cancel_dark_new.get_rect()
        self.screen.blit(self.button_cancel_dark_new, self.surface_json['button']['button_cancel_dark'])
        self.button_cancel_dark_new_rect.x += self.surface_json['button']['button_cancel_dark'][0]
        self.button_cancel_dark_new_rect.y += self.surface_json['button']['button_cancel_dark'][1]



        
        #button_About_us_highlight
        self.button_About_us_highlight = pygame.image.load('images/button_About_us_highlight.png')
        self.button_About_us_highlight_2 = Image.open('images/button_About_us_highlight.png')
        self.button_About_us_highlight_width, self.button_About_us_highlight_height = self.button_About_us_highlight_2.size
        self.button_About_us_highlight_new = pygame.transform.scale(surface=self.button_About_us_highlight, size=(self.button_About_us_highlight_width * self.settings.RATIO_ALL, self.button_About_us_highlight_height * self.settings.RATIO_ALL))
        self.button_About_us_highlight_new_rect = self.button_About_us_highlight_new.get_rect()
        self.screen.blit(self.button_About_us_highlight_new, self.surface_json['button']['button_About_us_highlight'])
        self.button_About_us_highlight_new_rect.x += self.surface_json['button']['button_About_us_highlight'][0]
        self.button_About_us_highlight_new_rect.y += self.surface_json['button']['button_About_us_highlight'][1]



        #button_About_us_static
        self.button_About_us_static = pygame.image.load('images/button_About_us_static.png')
        self.button_About_us_static_2 = Image.open('images/button_About_us_static.png')
        self.button_About_us_static_width, self.button_About_us_static_height = self.button_About_us_static_2.size
        self.button_About_us_static_new = pygame.transform.scale(surface=self.button_About_us_static, size=(self.button_About_us_static_width * self.settings.RATIO_ALL, self.button_About_us_static_height * self.settings.RATIO_ALL))
        self.button_About_us_static_new_rect = self.button_About_us_static_new.get_rect()
        self.screen.blit(self.button_About_us_static_new, self.surface_json['button']['button_About_us_static'])
        self.button_About_us_static_new_rect.x += self.surface_json['button']['button_About_us_static'][0]
        self.button_About_us_static_new_rect.y += self.surface_json['button']['button_About_us_static'][1]



        #button_buy_dark
        self.button_buy_dark = pygame.image.load('images/button_buy_dark.png')
        self.button_buy_dark_2 = Image.open('images/button_buy_dark.png')
        self.button_buy_dark_width, self.button_buy_dark_height = self.button_buy_dark_2.size
        self.button_buy_dark_new = pygame.transform.scale(surface=self.button_buy_dark, size=(self.button_buy_dark_width * self.settings.RATIO_ALL, self.button_buy_dark_height * self.settings.RATIO_ALL))
        
        
        self.button_buy_dark_ship_ticket_new_rect = self.button_buy_dark_new.get_rect()
        self.screen.blit(self.button_buy_dark_new, self.surface_json['button']['button_buy_dark']['ship_ticket'])
        self.button_buy_dark_ship_ticket_new_rect.x += self.surface_json['button']['button_buy_dark']['ship_ticket'][0]
        self.button_buy_dark_ship_ticket_new_rect.y += self.surface_json['button']['button_buy_dark']['ship_ticket'][1]

        self.button_buy_dark_railway_ticket_new_rect = self.button_buy_dark_new.get_rect()
        self.screen.blit(self.button_buy_dark_new, self.surface_json['button']['button_buy_dark']['railway_ticket'])
        self.button_buy_dark_railway_ticket_new_rect.x += self.surface_json['button']['button_buy_dark']['railway_ticket'][0]
        self.button_buy_dark_railway_ticket_new_rect.y += self.surface_json['button']['button_buy_dark']['railway_ticket'][1]

        self.button_buy_dark_road_ticket_new_rect = self.button_buy_dark_new.get_rect()
        self.screen.blit(self.button_buy_dark_new, self.surface_json['button']['button_buy_dark']['road_ticket'])
        self.button_buy_dark_road_ticket_new_rect.x += self.surface_json['button']['button_buy_dark']['road_ticket'][0]
        self.button_buy_dark_road_ticket_new_rect.y += self.surface_json['button']['button_buy_dark']['road_ticket'][1]

        self.button_buy_dark_unknown_ticket_new_rect = self.button_buy_dark_new.get_rect()
        self.screen.blit(self.button_buy_dark_new, self.surface_json['button']['button_buy_dark']['unknown_ticket'])
        self.button_buy_dark_unknown_ticket_new_rect.x += self.surface_json['button']['button_buy_dark']['unknown_ticket'][0]
        self.button_buy_dark_unknown_ticket_new_rect.y += self.surface_json['button']['button_buy_dark']['unknown_ticket'][1]

        self.button_buy_dark_trap_card_new_rect = self.button_buy_dark_new.get_rect()
        self.screen.blit(self.button_buy_dark_new, self.surface_json['button']['button_buy_dark']['trap_card'])
        self.button_buy_dark_trap_card_new_rect.x += self.surface_json['button']['button_buy_dark']['trap_card'][0]
        self.button_buy_dark_trap_card_new_rect.y += self.surface_json['button']['button_buy_dark']['trap_card'][1]

        self.button_buy_dark_skip_card_new_rect = self.button_buy_dark_new.get_rect()
        self.screen.blit(self.button_buy_dark_new, self.surface_json['button']['button_buy_dark']['skip_card'])
        self.button_buy_dark_skip_card_new_rect.x += self.surface_json['button']['button_buy_dark']['skip_card'][0]
        self.button_buy_dark_skip_card_new_rect.y += self.surface_json['button']['button_buy_dark']['skip_card'][1]

        self.button_buy_dark_hide_card_new_rect = self.button_buy_dark_new.get_rect()
        self.screen.blit(self.button_buy_dark_new, self.surface_json['button']['button_buy_dark']['hide_card'])
        self.button_buy_dark_hide_card_new_rect.x += self.surface_json['button']['button_buy_dark']['hide_card'][0]
        self.button_buy_dark_hide_card_new_rect.y += self.surface_json['button']['button_buy_dark']['hide_card'][1]

        self.button_buy_dark_war_card_new_rect = self.button_buy_dark_new.get_rect()
        self.screen.blit(self.button_buy_dark_new, self.surface_json['button']['button_buy_dark']['war_card'])
        self.button_buy_dark_war_card_new_rect.x += self.surface_json['button']['button_buy_dark']['war_card'][0]
        self.button_buy_dark_war_card_new_rect.y += self.surface_json['button']['button_buy_dark']['war_card'][1]





        #button_buy_shallow
        self.button_buy_shallow = pygame.image.load('images/button_buy_shallow.png')
        self.button_buy_shallow_2 = Image.open('images/button_buy_shallow.png')
        self.button_buy_shallow_width, self.button_buy_shallow_height = self.button_buy_shallow_2.size
        self.button_buy_shallow_new = pygame.transform.scale(surface=self.button_buy_shallow, size=(self.button_buy_shallow_width * self.settings.RATIO_ALL, self.button_buy_shallow_height * self.settings.RATIO_ALL))
        self.button_buy_shallow_new_rect = self.button_buy_shallow_new.get_rect()
        #self.screen.blit(self.button_buy_shallow_new, self.surface_json['button']['button_buy_shallow'])
        #self.button_buy_shallow_new_rect.x += self.surface_json['button']['button_buy_shallow'][0]
        #self.button_buy_shallow_new_rect.y += self.surface_json['button']['button_buy_shallow'][1]

        self.button_buy_shallow_ship_ticket_new_rect = self.button_buy_shallow_new.get_rect()
        self.screen.blit(self.button_buy_shallow_new, self.surface_json['button']['button_buy_shallow']['ship_ticket'])
        self.button_buy_shallow_ship_ticket_new_rect.x += self.surface_json['button']['button_buy_shallow']['ship_ticket'][0]
        self.button_buy_shallow_ship_ticket_new_rect.y += self.surface_json['button']['button_buy_shallow']['ship_ticket'][1]

        self.button_buy_shallow_railway_ticket_new_rect = self.button_buy_shallow_new.get_rect()
        self.screen.blit(self.button_buy_shallow_new, self.surface_json['button']['button_buy_shallow']['railway_ticket'])
        self.button_buy_shallow_railway_ticket_new_rect.x += self.surface_json['button']['button_buy_shallow']['railway_ticket'][0]
        self.button_buy_shallow_railway_ticket_new_rect.y += self.surface_json['button']['button_buy_shallow']['railway_ticket'][1]

        self.button_buy_shallow_road_ticket_new_rect = self.button_buy_shallow_new.get_rect()
        self.screen.blit(self.button_buy_shallow_new, self.surface_json['button']['button_buy_shallow']['road_ticket'])
        self.button_buy_shallow_road_ticket_new_rect.x += self.surface_json['button']['button_buy_shallow']['road_ticket'][0]
        self.button_buy_shallow_road_ticket_new_rect.y += self.surface_json['button']['button_buy_shallow']['road_ticket'][1]

        self.button_buy_shallow_unknown_ticket_new_rect = self.button_buy_shallow_new.get_rect()
        self.screen.blit(self.button_buy_shallow_new, self.surface_json['button']['button_buy_shallow']['unknown_ticket'])
        self.button_buy_shallow_unknown_ticket_new_rect.x += self.surface_json['button']['button_buy_shallow']['unknown_ticket'][0]
        self.button_buy_shallow_unknown_ticket_new_rect.y += self.surface_json['button']['button_buy_shallow']['unknown_ticket'][1]

        self.button_buy_shallow_trap_card_new_rect = self.button_buy_shallow_new.get_rect()
        self.screen.blit(self.button_buy_shallow_new, self.surface_json['button']['button_buy_shallow']['trap_card'])
        self.button_buy_shallow_trap_card_new_rect.x += self.surface_json['button']['button_buy_shallow']['trap_card'][0]
        self.button_buy_shallow_trap_card_new_rect.y += self.surface_json['button']['button_buy_shallow']['trap_card'][1]

        self.button_buy_shallow_skip_card_new_rect = self.button_buy_shallow_new.get_rect()
        self.screen.blit(self.button_buy_shallow_new, self.surface_json['button']['button_buy_shallow']['skip_card'])
        self.button_buy_shallow_skip_card_new_rect.x += self.surface_json['button']['button_buy_shallow']['skip_card'][0]
        self.button_buy_shallow_skip_card_new_rect.y += self.surface_json['button']['button_buy_shallow']['skip_card'][1]

        self.button_buy_shallow_hide_card_new_rect = self.button_buy_shallow_new.get_rect()
        self.screen.blit(self.button_buy_shallow_new, self.surface_json['button']['button_buy_shallow']['hide_card'])
        self.button_buy_shallow_hide_card_new_rect.x += self.surface_json['button']['button_buy_shallow']['hide_card'][0]
        self.button_buy_shallow_hide_card_new_rect.y += self.surface_json['button']['button_buy_shallow']['hide_card'][1]

        self.button_buy_shallow_war_card_new_rect = self.button_buy_shallow_new.get_rect()
        self.screen.blit(self.button_buy_shallow_new, self.surface_json['button']['button_buy_shallow']['war_card'])
        self.button_buy_shallow_war_card_new_rect.x += self.surface_json['button']['button_buy_shallow']['war_card'][0]
        self.button_buy_shallow_war_card_new_rect.y += self.surface_json['button']['button_buy_shallow']['war_card'][1]



        #button_close_audio_highlight
        self.button_close_audio_highlight = pygame.image.load('images/button_close_audio_highlight.png')
        self.button_close_audio_highlight_2 = Image.open('images/button_close_audio_highlight.png')
        self.button_close_audio_highlight_width, self.button_close_audio_highlight_height = self.button_close_audio_highlight_2.size
        self.button_close_audio_highlight_new = pygame.transform.scale(surface=self.button_close_audio_highlight, size=(self.button_close_audio_highlight_width * self.settings.RATIO_ALL, self.button_close_audio_highlight_height * self.settings.RATIO_ALL))
        self.button_close_audio_highlight_new_rect = self.button_close_audio_highlight_new.get_rect()
        self.screen.blit(self.button_close_audio_highlight_new, self.surface_json['button']['button_close_audio_highlight'])
        self.button_close_audio_highlight_new_rect.x += self.surface_json['button']['button_close_audio_highlight'][0]
        self.button_close_audio_highlight_new_rect.y += self.surface_json['button']['button_close_audio_highlight'][1]



        #button_close_audio_static
        self.button_close_audio_static = pygame.image.load('images/button_close_audio_static.png')
        self.button_close_audio_static_2 = Image.open('images/button_close_audio_static.png')
        self.button_close_audio_static_width, self.button_close_audio_static_height = self.button_close_audio_static_2.size
        self.button_close_audio_static_new = pygame.transform.scale(surface=self.button_close_audio_static, size=(self.button_close_audio_static_width * self.settings.RATIO_ALL, self.button_close_audio_static_height * self.settings.RATIO_ALL))
        self.button_close_audio_static_new_rect = self.button_close_audio_static_new.get_rect()
        self.screen.blit(self.button_close_audio_static_new, self.surface_json['button']['button_close_audio_static'])
        self.button_close_audio_static_new_rect.x += self.surface_json['button']['button_close_audio_static'][0]
        self.button_close_audio_static_new_rect.y += self.surface_json['button']['button_close_audio_static'][1]



        #创建房间高光按钮
        self.button_create_a_room_highlight = pygame.image.load('images/button_create_a_room_highlight.png')
        self.button_create_a_room_highlight_2 = Image.open('images/button_create_a_room_highlight.png')
        self.button_create_a_room_highlight_width, self.button_create_a_room_highlight_height = self.button_create_a_room_highlight_2.size
        self.button_create_a_room_highlight_new = pygame.transform.scale(surface=self.button_create_a_room_highlight, size=(self.button_create_a_room_highlight_width * self.settings.RATIO_ALL, self.button_create_a_room_highlight_height * self.settings.RATIO_ALL))
        self.button_create_a_room_highlight_new_rect = self.button_create_a_room_highlight_new.get_rect()
        self.screen.blit(self.button_create_a_room_highlight_new, self.surface_json['button']['button_create_a_room_highlight'])
        self.button_create_a_room_highlight_new_rect.x += self.surface_json['button']['button_create_a_room_highlight'][0]
        self.button_create_a_room_highlight_new_rect.y += self.surface_json['button']['button_create_a_room_highlight'][1]



        #button_create_a_room_static
        self.button_create_a_room_static = pygame.image.load('images/button_create_a_room_static.png')
        self.button_create_a_room_static_2 = Image.open('images/button_create_a_room_static.png')
        self.button_create_a_room_static_width, self.button_create_a_room_static_height = self.button_create_a_room_static_2.size
        self.button_create_a_room_static_new = pygame.transform.scale(surface=self.button_create_a_room_static, size=(self.button_create_a_room_static_width * self.settings.RATIO_ALL, self.button_create_a_room_static_height * self.settings.RATIO_ALL))
        self.button_create_a_room_static_new_rect = self.button_create_a_room_static_new.get_rect()
        self.screen.blit(self.button_create_a_room_static_new, self.surface_json['button']['button_create_a_room_static'])
        self.button_create_a_room_static_new_rect.x += self.surface_json['button']['button_create_a_room_static'][0]
        self.button_create_a_room_static_new_rect.y += self.surface_json['button']['button_create_a_room_static'][1]



        #button_enter_your_room_address_highlight
        self.button_enter_your_room_address_highlight = pygame.image.load('images/button_enter_your_room_address_highlight.png')
        self.button_enter_your_room_address_highlight_2 = Image.open('images/button_enter_your_room_address_highlight.png')
        self.button_enter_your_room_address_highlight_width, self.button_enter_your_room_address_highlight_height = self.button_enter_your_room_address_highlight_2.size
        self.button_enter_your_room_address_highlight_new = pygame.transform.scale(surface=self.button_enter_your_room_address_highlight, size=(self.button_enter_your_room_address_highlight_width * self.settings.RATIO_ALL, self.button_enter_your_room_address_highlight_height * self.settings.RATIO_ALL))
        self.button_enter_your_room_address_highlight_new_rect = self.button_enter_your_room_address_highlight_new.get_rect()
        self.screen.blit(self.button_enter_your_room_address_highlight_new, self.surface_json['button']['button_enter_your_room_address_highlight'])
        self.button_enter_your_room_address_highlight_new_rect.x += self.surface_json['button']['button_enter_your_room_address_highlight'][0]
        self.button_enter_your_room_address_highlight_new_rect.y += self.surface_json['button']['button_enter_your_room_address_highlight'][1]



        #button_enter_your_room_address_static
        self.button_enter_your_room_address_static = pygame.image.load('images/button_enter_your_room_address_static.png')
        self.button_enter_your_room_address_static_2 = Image.open('images/button_enter_your_room_address_static.png')
        self.button_enter_your_room_address_static_width, self.button_enter_your_room_address_static_height = self.button_enter_your_room_address_static_2.size
        self.button_enter_your_room_address_static_new = pygame.transform.scale(surface=self.button_enter_your_room_address_static, size=(self.button_enter_your_room_address_static_width * self.settings.RATIO_ALL, self.button_enter_your_room_address_static_height * self.settings.RATIO_ALL))
        self.button_enter_your_room_address_static_new_rect = self.button_enter_your_room_address_static_new.get_rect()
        self.screen.blit(self.button_enter_your_room_address_static_new, self.surface_json['button']['button_enter_your_room_address_static'])
        self.button_enter_your_room_address_static_new_rect.x += self.surface_json['button']['button_enter_your_room_address_static'][0]
        self.button_enter_your_room_address_static_new_rect.y += self.surface_json['button']['button_enter_your_room_address_static'][1]



        #button_exit_dark
        self.button_exit_dark = pygame.image.load('images/button_exit_dark.png')
        self.button_exit_dark_2 = Image.open('images/button_exit_dark.png')
        self.button_exit_dark_width, self.button_exit_dark_height = self.button_exit_dark_2.size
        self.button_exit_dark_new = pygame.transform.scale(surface=self.button_exit_dark, size=(self.button_exit_dark_width * self.settings.RATIO_ALL, self.button_exit_dark_height * self.settings.RATIO_ALL))
        self.button_exit_dark_new_rect = self.button_exit_dark_new.get_rect()
        self.screen.blit(self.button_exit_dark_new, self.surface_json['button']['button_exit_dark'])
        self.button_exit_dark_new_rect.x += self.surface_json['button']['button_exit_dark'][0]
        self.button_exit_dark_new_rect.y += self.surface_json['button']['button_exit_dark'][1]



        #button_exit_shallow
        self.button_exit_shallow = pygame.image.load('images/button_exit_shallow.png')
        self.button_exit_shallow_2 = Image.open('images/button_exit_shallow.png')
        self.button_exit_shallow_width, self.button_exit_shallow_height = self.button_exit_shallow_2.size
        self.button_exit_shallow_new = pygame.transform.scale(surface=self.button_exit_shallow, size=(self.button_exit_shallow_width * self.settings.RATIO_ALL, self.button_exit_shallow_height * self.settings.RATIO_ALL))
        self.button_exit_shallow_new_rect = self.button_exit_shallow_new.get_rect()
        self.screen.blit(self.button_exit_shallow_new, self.surface_json['button']['button_exit_shallow'])
        self.button_exit_shallow_new_rect.x += self.surface_json['button']['button_exit_shallow'][0]
        self.button_exit_shallow_new_rect.y += self.surface_json['button']['button_exit_shallow'][1]



        #button_hide_dark
        self.button_hide_dark = pygame.image.load('images/button_hide_dark.png')
        self.button_hide_dark_2 = Image.open('images/button_hide_dark.png')
        self.button_hide_dark_width, self.button_hide_dark_height = self.button_hide_dark_2.size
        self.button_hide_dark_new = pygame.transform.scale(surface=self.button_hide_dark, size=(self.button_hide_dark_width * self.settings.RATIO_ALL, self.button_hide_dark_height * self.settings.RATIO_ALL))
        self.button_hide_dark_new_rect = self.button_hide_dark_new.get_rect()
        self.screen.blit(self.button_hide_dark_new, self.surface_json['button']['button_hide_dark'])
        self.button_hide_dark_new_rect.x += self.surface_json['button']['button_hide_dark'][0]
        self.button_hide_dark_new_rect.y += self.surface_json['button']['button_hide_dark'][1]



        #button_hide_shallow
        self.button_hide_shallow = pygame.image.load('images/button_hide_shallow.png')
        self.button_hide_shallow_2 = Image.open('images/button_hide_shallow.png')
        self.button_hide_shallow_width, self.button_hide_shallow_height = self.button_hide_shallow_2.size
        self.button_hide_shallow_new = pygame.transform.scale(surface=self.button_hide_shallow, size=(self.button_hide_shallow_width * self.settings.RATIO_ALL, self.button_hide_shallow_height * self.settings.RATIO_ALL))
        self.button_hide_shallow_new_rect = self.button_hide_shallow_new.get_rect()
        self.screen.blit(self.button_hide_shallow_new, self.surface_json['button']['button_hide_shallow'])
        self.button_hide_shallow_new_rect.x += self.surface_json['button']['button_hide_shallow'][0]
        self.button_hide_shallow_new_rect.y += self.surface_json['button']['button_hide_shallow'][1]



        #button_join_in_a_room_highlight
        self.button_join_in_a_room_highlight = pygame.image.load('images/button_join_in_a_room_highlight.png')
        self.button_join_in_a_room_highlight_2 = Image.open('images/button_join_in_a_room_highlight.png')
        self.button_join_in_a_room_highlight_width, self.button_join_in_a_room_highlight_height = self.button_join_in_a_room_highlight_2.size
        self.button_join_in_a_room_highlight_new = pygame.transform.scale(surface=self.button_join_in_a_room_highlight, size=(self.button_join_in_a_room_highlight_width * self.settings.RATIO_ALL, self.button_join_in_a_room_highlight_height * self.settings.RATIO_ALL))
        self.button_join_in_a_room_highlight_new_rect = self.button_join_in_a_room_highlight_new.get_rect()
        self.screen.blit(self.button_join_in_a_room_highlight_new, self.surface_json['button']['button_join_in_a_room_highlight'])
        self.button_join_in_a_room_highlight_new_rect.x += self.surface_json['button']['button_join_in_a_room_highlight'][0]
        self.button_join_in_a_room_highlight_new_rect.y += self.surface_json['button']['button_join_in_a_room_highlight'][1]



        #button_join_in_a_room_static
        self.button_join_in_a_room_static = pygame.image.load('images/button_join_in_a_room_static.png')
        self.button_join_in_a_room_static_2 = Image.open('images/button_join_in_a_room_static.png')
        self.button_join_in_a_room_static_width, self.button_join_in_a_room_static_height = self.button_join_in_a_room_static_2.size
        self.button_join_in_a_room_static_new = pygame.transform.scale(surface=self.button_join_in_a_room_static, size=(self.button_join_in_a_room_static_width * self.settings.RATIO_ALL, self.button_join_in_a_room_static_height * self.settings.RATIO_ALL))
        self.button_join_in_a_room_static_new_rect = self.button_join_in_a_room_static_new.get_rect()
        self.screen.blit(self.button_join_in_a_room_static_new, self.surface_json['button']['button_join_in_a_room_static'])
        self.button_join_in_a_room_static_new_rect.x += self.surface_json['button']['button_join_in_a_room_static'][0]
        self.button_join_in_a_room_static_new_rect.y += self.surface_json['button']['button_join_in_a_room_static'][1]



        #button_Multi_player_highlight
        self.button_Multi_player_highlight = pygame.image.load('images/button_Multi_player_highlight.png')
        self.button_Multi_player_highlight_2 = Image.open('images/button_Multi_player_highlight.png')
        self.button_Multi_player_highlight_width, self.button_Multi_player_highlight_height = self.button_Multi_player_highlight_2.size
        self.button_Multi_player_highlight_new = pygame.transform.scale(surface=self.button_Multi_player_highlight, size=(self.button_Multi_player_highlight_width * self.settings.RATIO_ALL, self.button_Multi_player_highlight_height * self.settings.RATIO_ALL))
        self.button_Multi_player_highlight_new_rect = self.button_Multi_player_highlight_new.get_rect()
        self.screen.blit(self.button_Multi_player_highlight_new, self.surface_json['button']['button_Multi_player_highlight'])
        self.button_Multi_player_highlight_new_rect.x += self.surface_json['button']['button_Multi_player_highlight'][0]
        self.button_Multi_player_highlight_new_rect.y += self.surface_json['button']['button_Multi_player_highlight'][1]



        #button_Multi_player_static
        self.button_Multi_player_static = pygame.image.load('images/button_Multi_player_static.png')
        self.button_Multi_player_static_2 = Image.open('images/button_Multi_player_static.png')
        self.button_Multi_player_static_width, self.button_Multi_player_static_height = self.button_Multi_player_static_2.size
        self.button_Multi_player_static_new = pygame.transform.scale(surface=self.button_Multi_player_static, size=(self.button_Multi_player_static_width * self.settings.RATIO_ALL, self.button_Multi_player_static_height * self.settings.RATIO_ALL))
        self.button_Multi_player_static_new_rect = self.button_Multi_player_static_new.get_rect()
        self.screen.blit(self.button_Multi_player_static_new, self.surface_json['button']['button_Multi_player_static'])
        self.button_Multi_player_static_new_rect.x += self.surface_json['button']['button_Multi_player_static'][0]
        self.button_Multi_player_static_new_rect.y += self.surface_json['button']['button_Multi_player_static'][1]



        #button_open_audio_highlight
        self.button_open_audio_highlight = pygame.image.load('images/button_open_audio_highlight.png')
        self.button_open_audio_highlight_2 = Image.open('images/button_open_audio_highlight.png')
        self.button_open_audio_highlight_width, self.button_open_audio_highlight_height = self.button_open_audio_highlight_2.size
        self.button_open_audio_highlight_new = pygame.transform.scale(surface=self.button_open_audio_highlight, size=(self.button_open_audio_highlight_width * self.settings.RATIO_ALL, self.button_open_audio_highlight_height * self.settings.RATIO_ALL))
        self.button_open_audio_highlight_new_rect = self.button_open_audio_highlight_new.get_rect()
        self.screen.blit(self.button_open_audio_highlight_new, self.surface_json['button']['button_open_audio_highlight'])
        self.button_open_audio_highlight_new_rect.x += self.surface_json['button']['button_open_audio_highlight'][0]
        self.button_open_audio_highlight_new_rect.y += self.surface_json['button']['button_open_audio_highlight'][1]



        #button_open_audio_static
        self.button_open_audio_static = pygame.image.load('images/button_open_audio_static.png')
        self.button_open_audio_static_2 = Image.open('images/button_open_audio_static.png')
        self.button_open_audio_static_width, self.button_open_audio_static_height = self.button_open_audio_static_2.size
        self.button_open_audio_static_new = pygame.transform.scale(surface=self.button_open_audio_static, size=(self.button_open_audio_static_width * self.settings.RATIO_ALL, self.button_open_audio_static_height * self.settings.RATIO_ALL))
        self.button_open_audio_static_new_rect = self.button_open_audio_static_new.get_rect()
        self.screen.blit(self.button_open_audio_static_new, self.surface_json['button']['button_open_audio_static'])
        self.button_open_audio_static_new_rect.x += self.surface_json['button']['button_open_audio_static'][0]
        self.button_open_audio_static_new_rect.y += self.surface_json['button']['button_open_audio_static'][1]



        #button_out_highlight
        self.button_out_highlight = pygame.image.load('images/button_out_highlight.png')
        self.button_out_highlight_2 = Image.open('images/button_out_highlight.png')
        self.button_out_highlight_width, self.button_out_highlight_height = self.button_out_highlight_2.size
        self.button_out_highlight_new = pygame.transform.scale(surface=self.button_out_highlight, size=(self.button_out_highlight_width * self.settings.RATIO_ALL, self.button_out_highlight_height * self.settings.RATIO_ALL))
        self.button_out_highlight_new_rect = self.button_out_highlight_new.get_rect()
        self.screen.blit(self.button_out_highlight_new, self.surface_json['button']['button_out_highlight'])
        self.button_out_highlight_new_rect.x += self.surface_json['button']['button_out_highlight'][0]
        self.button_out_highlight_new_rect.y += self.surface_json['button']['button_out_highlight'][1]



        #button_out_static
        self.button_out_static = pygame.image.load('images/button_out_static.png')
        self.button_out_static_2 = Image.open('images/button_out_static.png')
        self.button_out_static_width, self.button_out_static_height = self.button_out_static_2.size
        self.button_out_static_new = pygame.transform.scale(surface=self.button_out_static, size=(self.button_out_static_width * self.settings.RATIO_ALL, self.button_out_static_height * self.settings.RATIO_ALL))
        self.button_out_static_new_rect = self.button_out_static_new.get_rect()
        self.screen.blit(self.button_out_static_new, self.surface_json['button']['button_out_static'])
        self.button_out_static_new_rect.x += self.surface_json['button']['button_out_static'][0]
        self.button_out_static_new_rect.y += self.surface_json['button']['button_out_static'][1]



        #button_Rules_highlight
        self.button_Rules_highlight = pygame.image.load('images/button_Rules_highlight.png')
        self.button_Rules_highlight_2 = Image.open('images/button_Rules_highlight.png')
        self.button_Rules_highlight_width, self.button_Rules_highlight_height = self.button_Rules_highlight_2.size
        self.button_Rules_highlight_new = pygame.transform.scale(surface=self.button_Rules_highlight, size=(self.button_Rules_highlight_width * self.settings.RATIO_ALL, self.button_Rules_highlight_height * self.settings.RATIO_ALL))
        self.button_Rules_highlight_new_rect = self.button_Rules_highlight_new.get_rect()
        self.screen.blit(self.button_Rules_highlight_new, self.surface_json['button']['button_Rules_highlight'])
        self.button_Rules_highlight_new_rect.x += self.surface_json['button']['button_Rules_highlight'][0]
        self.button_Rules_highlight_new_rect.y += self.surface_json['button']['button_Rules_highlight'][1]



        #button_Rules_static
        self.button_Rules_static = pygame.image.load('images/button_Rules_static.png')
        self.button_Rules_static_2 = Image.open('images/button_Rules_static.png')
        self.button_Rules_static_width, self.button_Rules_static_height = self.button_Rules_static_2.size
        self.button_Rules_static_new = pygame.transform.scale(surface=self.button_Rules_static, size=(self.button_Rules_static_width * self.settings.RATIO_ALL, self.button_Rules_static_height * self.settings.RATIO_ALL))
        self.button_Rules_static_new_rect = self.button_Rules_static_new.get_rect()
        self.screen.blit(self.button_Rules_static_new, self.surface_json['button']['button_Rules_static'])
        self.button_Rules_static_new_rect.x += self.surface_json['button']['button_Rules_static'][0]
        self.button_Rules_static_new_rect.y += self.surface_json['button']['button_Rules_static'][1]



        #button_shop_dark
        self.button_shop_dark = pygame.image.load('images/button_shop_dark.png')
        self.button_shop_dark_2 = Image.open('images/button_shop_dark.png')
        self.button_shop_dark_width, self.button_shop_dark_height = self.button_shop_dark_2.size
        self.button_shop_dark_new = pygame.transform.scale(surface=self.button_shop_dark, size=(self.button_shop_dark_width * self.settings.RATIO_ALL, self.button_shop_dark_height * self.settings.RATIO_ALL))
        self.button_shop_dark_new_rect = self.button_shop_dark_new.get_rect()
        self.screen.blit(self.button_shop_dark_new, self.surface_json['button']['button_shop_dark'])
        self.button_shop_dark_new_rect.x += self.surface_json['button']['button_shop_dark'][0]
        self.button_shop_dark_new_rect.y += self.surface_json['button']['button_shop_dark'][1]



        #button_shop_shallow
        self.button_shop_shallow = pygame.image.load('images/button_shop_shallow.png')
        self.button_shop_shallow_2 = Image.open('images/button_shop_shallow.png')
        self.button_shop_shallow_width, self.button_shop_shallow_height = self.button_shop_shallow_2.size
        self.button_shop_shallow_new = pygame.transform.scale(surface=self.button_shop_shallow, size=(self.button_shop_shallow_width * self.settings.RATIO_ALL, self.button_shop_shallow_height * self.settings.RATIO_ALL))
        self.button_shop_shallow_new_rect = self.button_shop_shallow_new.get_rect()
        self.screen.blit(self.button_shop_shallow_new, self.surface_json['button']['button_shop_shallow'])
        self.button_shop_shallow_new_rect.x += self.surface_json['button']['button_shop_shallow'][0]
        self.button_shop_shallow_new_rect.y += self.surface_json['button']['button_shop_shallow'][1]



        #button_skip_dark
        self.button_skip_dark = pygame.image.load('images/button_skip_dark.png')
        self.button_skip_dark_2 = Image.open('images/button_skip_dark.png')
        self.button_skip_dark_width, self.button_skip_dark_height = self.button_skip_dark_2.size
        self.button_skip_dark_new = pygame.transform.scale(surface=self.button_skip_dark, size=(self.button_skip_dark_width * self.settings.RATIO_ALL, self.button_skip_dark_height * self.settings.RATIO_ALL))
        self.button_skip_dark_new_rect = self.button_skip_dark_new.get_rect()
        self.screen.blit(self.button_skip_dark_new, self.surface_json['button']['button_skip_dark'])
        self.button_skip_dark_new_rect.x += self.surface_json['button']['button_skip_dark'][0]
        self.button_skip_dark_new_rect.y += self.surface_json['button']['button_skip_dark'][1]



        #button_skip_shallow
        self.button_skip_shallow = pygame.image.load('images/button_skip_shallow.png')
        self.button_skip_shallow_2 = Image.open('images/button_skip_shallow.png')
        self.button_skip_shallow_width, self.button_skip_shallow_height = self.button_skip_shallow_2.size
        self.button_skip_shallow_new = pygame.transform.scale(surface=self.button_skip_shallow, size=(self.button_skip_shallow_width * self.settings.RATIO_ALL, self.button_skip_shallow_height * self.settings.RATIO_ALL))
        self.button_skip_shallow_new_rect = self.button_skip_shallow_new.get_rect()
        self.screen.blit(self.button_skip_shallow_new, self.surface_json['button']['button_skip_shallow'])
        self.button_skip_shallow_new_rect.x += self.surface_json['button']['button_skip_shallow'][0]
        self.button_skip_shallow_new_rect.y += self.surface_json['button']['button_skip_shallow'][1]



        #button_trap_dark
        self.button_trap_dark = pygame.image.load('images/button_trap_dark.png')
        self.button_trap_dark_2 = Image.open('images/button_trap_dark.png')
        self.button_trap_dark_width, self.button_trap_dark_height = self.button_trap_dark_2.size
        self.button_trap_dark_new = pygame.transform.scale(surface=self.button_trap_dark, size=(self.button_trap_dark_width * self.settings.RATIO_ALL, self.button_trap_dark_height * self.settings.RATIO_ALL))
        self.button_trap_dark_new_rect = self.button_trap_dark_new.get_rect()
        self.screen.blit(self.button_trap_dark_new, self.surface_json['button']['button_trap_dark'])
        self.button_trap_dark_new_rect.x += self.surface_json['button']['button_trap_dark'][0]
        self.button_trap_dark_new_rect.y += self.surface_json['button']['button_trap_dark'][1]



        #button_trap_shallow
        self.button_trap_shallow = pygame.image.load('images/button_trap_shallow.png')
        self.button_trap_shallow_2 = Image.open('images/button_trap_shallow.png')
        self.button_trap_shallow_width, self.button_trap_shallow_height = self.button_trap_shallow_2.size
        self.button_trap_shallow_new = pygame.transform.scale(surface=self.button_trap_shallow, size=(self.button_trap_shallow_width * self.settings.RATIO_ALL, self.button_trap_shallow_height * self.settings.RATIO_ALL))
        self.button_trap_shallow_new_rect = self.button_trap_shallow_new.get_rect()
        self.screen.blit(self.button_trap_shallow_new, self.surface_json['button']['button_trap_shallow'])
        self.button_trap_shallow_new_rect.x += self.surface_json['button']['button_trap_shallow'][0]
        self.button_trap_shallow_new_rect.y += self.surface_json['button']['button_trap_shallow'][1]



        #button_war_dark
        self.button_war_dark = pygame.image.load('images/button_war_dark.png')
        self.button_war_dark_2 = Image.open('images/button_war_dark.png')
        self.button_war_dark_width, self.button_war_dark_height = self.button_war_dark_2.size
        self.button_war_dark_new = pygame.transform.scale(surface=self.button_war_dark, size=(self.button_war_dark_width * self.settings.RATIO_ALL, self.button_war_dark_height * self.settings.RATIO_ALL))
        self.button_war_dark_new_rect = self.button_war_dark_new.get_rect()
        self.screen.blit(self.button_war_dark_new, self.surface_json['button']['button_war_dark'])
        self.button_war_dark_new_rect.x += self.surface_json['button']['button_war_dark'][0]
        self.button_war_dark_new_rect.y += self.surface_json['button']['button_war_dark'][1]



        #button_war_shallow
        self.button_war_shallow = pygame.image.load('images/button_war_shallow.png')
        self.button_war_shallow_2 = Image.open('images/button_war_shallow.png')
        self.button_war_shallow_width, self.button_war_shallow_height = self.button_war_shallow_2.size
        self.button_war_shallow_new = pygame.transform.scale(surface=self.button_war_shallow, size=(self.button_war_shallow_width * self.settings.RATIO_ALL, self.button_war_shallow_height * self.settings.RATIO_ALL))
        self.button_war_shallow_new_rect = self.button_war_shallow_new.get_rect()
        self.screen.blit(self.button_war_shallow_new, self.surface_json['button']['button_war_shallow'])
        self.button_war_shallow_new_rect.x += self.surface_json['button']['button_war_shallow'][0]
        self.button_war_shallow_new_rect.y += self.surface_json['button']['button_war_shallow'][1]


        #button_ship_dark
        self.button_ship_dark = pygame.image.load('images/button_ship_dark.png')
        self.button_ship_dark_2 = Image.open('images/button_ship_dark.png')
        self.button_ship_dark_width, self.button_ship_dark_height = self.button_ship_dark_2.size
        self.button_ship_dark_new = pygame.transform.scale(surface=self.button_ship_dark, size=(self.button_ship_dark_width * self.settings.RATIO_ALL, self.button_ship_dark_height * self.settings.RATIO_ALL))
        self.button_ship_dark_new_rect = self.button_ship_dark_new.get_rect()
        self.screen.blit(self.button_ship_dark_new, self.surface_json['button']['button_ship_dark'])
        self.button_ship_dark_new_rect.x += self.surface_json['button']['button_ship_dark'][0]
        self.button_ship_dark_new_rect.y += self.surface_json['button']['button_ship_dark'][1]



        #button_ship_shallow
        self.button_ship_shallow = pygame.image.load('images/button_ship_shallow.png')
        self.button_ship_shallow_2 = Image.open('images/button_ship_shallow.png')
        self.button_ship_shallow_width, self.button_ship_shallow_height = self.button_ship_shallow_2.size
        self.button_ship_shallow_new = pygame.transform.scale(surface=self.button_ship_shallow, size=(self.button_ship_shallow_width * self.settings.RATIO_ALL, self.button_ship_shallow_height * self.settings.RATIO_ALL))
        self.button_ship_shallow_new_rect = self.button_ship_shallow_new.get_rect()
        self.screen.blit(self.button_ship_shallow_new, self.surface_json['button']['button_ship_shallow'])
        self.button_ship_shallow_new_rect.x += self.surface_json['button']['button_ship_shallow'][0]
        self.button_ship_shallow_new_rect.y += self.surface_json['button']['button_ship_shallow'][1]




        #button_railway_dark
        self.button_railway_dark = pygame.image.load('images/button_railway_dark.png')
        self.button_railway_dark_2 = Image.open('images/button_railway_dark.png')
        self.button_railway_dark_width, self.button_railway_dark_height = self.button_railway_dark_2.size
        self.button_railway_dark_new = pygame.transform.scale(surface=self.button_railway_dark, size=(self.button_railway_dark_width * self.settings.RATIO_ALL, self.button_railway_dark_height * self.settings.RATIO_ALL))
        self.button_railway_dark_new_rect = self.button_railway_dark_new.get_rect()
        self.screen.blit(self.button_railway_dark_new, self.surface_json['button']['button_railway_dark'])
        self.button_railway_dark_new_rect.x += self.surface_json['button']['button_railway_dark'][0]
        self.button_railway_dark_new_rect.y += self.surface_json['button']['button_railway_dark'][1]



        #button_railway_shallow
        self.button_railway_shallow = pygame.image.load('images/button_railway_shallow.png')
        self.button_railway_shallow_2 = Image.open('images/button_railway_shallow.png')
        self.button_railway_shallow_width, self.button_railway_shallow_height = self.button_railway_shallow_2.size
        self.button_railway_shallow_new = pygame.transform.scale(surface=self.button_railway_shallow, size=(self.button_railway_shallow_width * self.settings.RATIO_ALL, self.button_railway_shallow_height * self.settings.RATIO_ALL))
        self.button_railway_shallow_new_rect = self.button_railway_shallow_new.get_rect()
        self.screen.blit(self.button_railway_shallow_new, self.surface_json['button']['button_railway_shallow'])
        self.button_railway_shallow_new_rect.x += self.surface_json['button']['button_railway_shallow'][0]
        self.button_railway_shallow_new_rect.y += self.surface_json['button']['button_railway_shallow'][1]



        #button_road_dark
        self.button_road_dark = pygame.image.load('images/button_road_dark.png')
        self.button_road_dark_2 = Image.open('images/button_road_dark.png')
        self.button_road_dark_width, self.button_road_dark_height = self.button_road_dark_2.size
        self.button_road_dark_new = pygame.transform.scale(surface=self.button_road_dark, size=(self.button_road_dark_width * self.settings.RATIO_ALL, self.button_road_dark_height * self.settings.RATIO_ALL))
        self.button_road_dark_new_rect = self.button_road_dark_new.get_rect()
        self.screen.blit(self.button_road_dark_new, self.surface_json['button']['button_road_dark'])
        self.button_road_dark_new_rect.x += self.surface_json['button']['button_road_dark'][0]
        self.button_road_dark_new_rect.y += self.surface_json['button']['button_road_dark'][1]



        #button_road_shallow
        self.button_road_shallow = pygame.image.load('images/button_road_shallow.png')
        self.button_road_shallow_2 = Image.open('images/button_road_shallow.png')
        self.button_road_shallow_width, self.button_road_shallow_height = self.button_road_shallow_2.size
        self.button_road_shallow_new = pygame.transform.scale(surface=self.button_road_shallow, size=(self.button_road_shallow_width * self.settings.RATIO_ALL, self.button_road_shallow_height * self.settings.RATIO_ALL))
        self.button_road_shallow_new_rect = self.button_road_shallow_new.get_rect()
        self.screen.blit(self.button_road_shallow_new, self.surface_json['button']['button_road_shallow'])
        self.button_road_shallow_new_rect.x += self.surface_json['button']['button_road_shallow'][0]
        self.button_road_shallow_new_rect.y += self.surface_json['button']['button_road_shallow'][1]



        #figure_player1_others
        self.figure_player1_others = pygame.image.load('images/figure_player1_others.png')
        self.figure_player1_others_2 = Image.open('images/figure_player1_others.png')
        self.figure_player1_others_width, self.figure_player1_others_height = self.figure_player1_others_2.size
        self.figure_player1_others_new = pygame.transform.scale(surface=self.figure_player1_others, size=(self.figure_player1_others_width * self.settings.RATIO_ALL, self.figure_player1_others_height * self.settings.RATIO_ALL))
        self.figure_player1_others_new_rect = self.figure_player1_others_new.get_rect()
        self.screen.blit(self.figure_player1_others_new, self.surface_json['figure']['figure_player1_others'])
        self.figure_player1_others_new_rect.x += self.surface_json['figure']['figure_player1_others'][0]
        self.figure_player1_others_new_rect.y += self.surface_json['figure']['figure_player1_others'][1]



        #figure_player1_you
        self.figure_player1_you = pygame.image.load('images/figure_player1_you.png')
        self.figure_player1_you_2 = Image.open('images/figure_player1_you.png')
        self.figure_player1_you_width, self.figure_player1_you_height = self.figure_player1_you_2.size
        self.figure_player1_you_new = pygame.transform.scale(surface=self.figure_player1_you, size=(self.figure_player1_you_width * self.settings.RATIO_ALL, self.figure_player1_you_height * self.settings.RATIO_ALL))
        self.figure_player1_you_new_rect = self.figure_player1_you_new.get_rect()
        self.screen.blit(self.figure_player1_you_new, self.surface_json['figure']['figure_player1_you'])
        self.figure_player1_you_new_rect.x += self.surface_json['figure']['figure_player1_you'][0]
        self.figure_player1_you_new_rect.y += self.surface_json['figure']['figure_player1_you'][1]



        #figure_player2_others
        self.figure_player2_others = pygame.image.load('images/figure_player2_others.png')
        self.figure_player2_others_2 = Image.open('images/figure_player2_others.png')
        self.figure_player2_others_width, self.figure_player2_others_height = self.figure_player2_others_2.size
        self.figure_player2_others_new = pygame.transform.scale(surface=self.figure_player2_others, size=(self.figure_player2_others_width * self.settings.RATIO_ALL, self.figure_player2_others_height * self.settings.RATIO_ALL))
        self.figure_player2_others_new_rect = self.figure_player2_others_new.get_rect()
        self.screen.blit(self.figure_player2_others_new, self.surface_json['figure']['figure_player2_others'])
        self.figure_player2_others_new_rect.x += self.surface_json['figure']['figure_player2_others'][0]
        self.figure_player2_others_new_rect.y += self.surface_json['figure']['figure_player2_others'][1]



        #figure_player2_you
        self.figure_player2_you = pygame.image.load('images/figure_player2_you.png')
        self.figure_player2_you_2 = Image.open('images/figure_player2_you.png')
        self.figure_player2_you_width, self.figure_player2_you_height = self.figure_player2_you_2.size
        self.figure_player2_you_new = pygame.transform.scale(surface=self.figure_player2_you, size=(self.figure_player2_you_width * self.settings.RATIO_ALL, self.figure_player2_you_height * self.settings.RATIO_ALL))
        self.figure_player2_you_new_rect = self.figure_player2_you_new.get_rect()
        self.screen.blit(self.figure_player2_you_new, self.surface_json['figure']['figure_player2_you'])
        self.figure_player2_you_new_rect.x += self.surface_json['figure']['figure_player2_you'][0]
        self.figure_player2_you_new_rect.y += self.surface_json['figure']['figure_player2_you'][1]



        #figure_player3_others
        self.figure_player3_others = pygame.image.load('images/figure_player3_others.png')
        self.figure_player3_others_2 = Image.open('images/figure_player3_others.png')
        self.figure_player3_others_width, self.figure_player3_others_height = self.figure_player3_others_2.size
        self.figure_player3_others_new = pygame.transform.scale(surface=self.figure_player3_others, size=(self.figure_player3_others_width * self.settings.RATIO_ALL, self.figure_player3_others_height * self.settings.RATIO_ALL))
        self.figure_player3_others_new_rect = self.figure_player3_others_new.get_rect()
        self.screen.blit(self.figure_player3_others_new, self.surface_json['figure']['figure_player3_others'])
        self.figure_player3_others_new_rect.x += self.surface_json['figure']['figure_player3_others'][0]
        self.figure_player3_others_new_rect.y += self.surface_json['figure']['figure_player3_others'][1]



        #figure_player3_you
        self.figure_player3_you = pygame.image.load('images/figure_player3_you.png')
        self.figure_player3_you_2 = Image.open('images/figure_player3_you.png')
        self.figure_player3_you_width, self.figure_player3_you_height = self.figure_player3_you_2.size
        self.figure_player3_you_new = pygame.transform.scale(surface=self.figure_player3_you, size=(self.figure_player3_you_width * self.settings.RATIO_ALL, self.figure_player3_you_height * self.settings.RATIO_ALL))
        self.figure_player3_you_new_rect = self.figure_player3_you_new.get_rect()
        self.screen.blit(self.figure_player3_you_new, self.surface_json['figure']['figure_player3_you'])
        self.figure_player3_you_new_rect.x += self.surface_json['figure']['figure_player3_you'][0]
        self.figure_player3_you_new_rect.y += self.surface_json['figure']['figure_player3_you'][1]



        #figure_player4_others
        self.figure_player4_others = pygame.image.load('images/figure_player4_others.png')
        self.figure_player4_others_2 = Image.open('images/figure_player4_others.png')
        self.figure_player4_others_width, self.figure_player4_others_height = self.figure_player4_others_2.size
        self.figure_player4_others_new = pygame.transform.scale(surface=self.figure_player4_others, size=(self.figure_player4_others_width * self.settings.RATIO_ALL, self.figure_player4_others_height * self.settings.RATIO_ALL))
        self.figure_player4_others_new_rect = self.figure_player4_others_new.get_rect()
        self.screen.blit(self.figure_player4_others_new, self.surface_json['figure']['figure_player4_others'])
        self.figure_player4_others_new_rect.x += self.surface_json['figure']['figure_player4_others'][0]
        self.figure_player4_others_new_rect.y += self.surface_json['figure']['figure_player4_others'][1]



        #figure_player4_you
        self.figure_player4_you = pygame.image.load('images/figure_player4_you.png')
        self.figure_player4_you_2 = Image.open('images/figure_player4_you.png')
        self.figure_player4_you_width, self.figure_player4_you_height = self.figure_player4_you_2.size
        self.figure_player4_you_new = pygame.transform.scale(surface=self.figure_player4_you, size=(self.figure_player4_you_width * self.settings.RATIO_ALL, self.figure_player4_you_height * self.settings.RATIO_ALL))
        self.figure_player4_you_new_rect = self.figure_player4_you_new.get_rect()
        self.screen.blit(self.figure_player4_you_new, self.surface_json['figure']['figure_player4_you'])
        self.figure_player4_you_new_rect.x += self.surface_json['figure']['figure_player4_you'][0]
        self.figure_player4_you_new_rect.y += self.surface_json['figure']['figure_player4_you'][1]



        #label_hiding_all
        self.label_hiding_all = pygame.image.load('images/label_hiding_all.png')
        self.label_hiding_all_2 = Image.open('images/label_hiding_all.png')
        self.label_hiding_all_width, self.label_hiding_all_height = self.label_hiding_all_2.size
        self.label_hiding_all_new = pygame.transform.scale(surface=self.label_hiding_all, size=(self.label_hiding_all_width * self.settings.RATIO_ALL, self.label_hiding_all_height * self.settings.RATIO_ALL))
        self.label_hiding_all_new_rect = self.label_hiding_all_new.get_rect()
        #self.screen.blit(self.label_hiding_all_new, self.surface_json['label']['label_hiding_all'])
        #self.label_hiding_all_new_rect.x += self.surface_json['label']['label_hiding_all'][0]
        #self.label_hiding_all_new_rect.y += self.surface_json['label']['label_hiding_all'][1]



        #label_trapped_all
        self.label_trapped_all = pygame.image.load('images/label_trapped_all.png')
        self.label_trapped_all_2 = Image.open('images/label_trapped_all.png')
        self.label_trapped_all_width, self.label_trapped_all_height = self.label_trapped_all_2.size
        self.label_trapped_all_new = pygame.transform.scale(surface=self.label_trapped_all, size=(self.label_trapped_all_width * self.settings.RATIO_ALL, self.label_trapped_all_height * self.settings.RATIO_ALL))
        self.label_trapped_all_new_rect = self.label_trapped_all_new.get_rect()
        #self.screen.blit(self.label_trapped_all_new, self.surface_json['label']['label_trapped_all'])
        #self.label_trapped_all_new_rect.x += self.surface_json['label']['label_trapped_all'][0]
       # self.label_trapped_all_new_rect.y += self.surface_json['label']['label_trapped_all'][1]



        #label_turn_player1
        self.label_turn_player1 = pygame.image.load('images/label_turn_player1.png')
        self.label_turn_player1_2 = Image.open('images/label_turn_player1.png')
        self.label_turn_player1_width, self.label_turn_player1_height = self.label_turn_player1_2.size
        self.label_turn_player1_new = pygame.transform.scale(surface=self.label_turn_player1, size=(self.label_turn_player1_width * self.settings.RATIO_ALL, self.label_turn_player1_height * self.settings.RATIO_ALL))
        self.label_turn_player1_new_rect = self.label_turn_player1_new.get_rect()
        self.screen.blit(self.label_turn_player1_new, self.surface_json['label']['label_turn_player1'])
        self.label_turn_player1_new_rect.x += self.surface_json['label']['label_turn_player1'][0]
        self.label_turn_player1_new_rect.y += self.surface_json['label']['label_turn_player1'][1]



        #label_turn_player2
        self.label_turn_player2 = pygame.image.load('images/label_turn_player2.png')
        self.label_turn_player2_2 = Image.open('images/label_turn_player2.png')
        self.label_turn_player2_width, self.label_turn_player2_height = self.label_turn_player2_2.size
        self.label_turn_player2_new = pygame.transform.scale(surface=self.label_turn_player2, size=(self.label_turn_player2_width * self.settings.RATIO_ALL, self.label_turn_player2_height * self.settings.RATIO_ALL))
        self.label_turn_player2_new_rect = self.label_turn_player2_new.get_rect()
        self.screen.blit(self.label_turn_player2_new, self.surface_json['label']['label_turn_player2'])
        self.label_turn_player2_new_rect.x += self.surface_json['label']['label_turn_player2'][0]
        self.label_turn_player2_new_rect.y += self.surface_json['label']['label_turn_player2'][1]



        #label_turn_player3
        self.label_turn_player3 = pygame.image.load('images/label_turn_player3.png')
        self.label_turn_player3_2 = Image.open('images/label_turn_player3.png')
        self.label_turn_player3_width, self.label_turn_player3_height = self.label_turn_player3_2.size
        self.label_turn_player3_new = pygame.transform.scale(surface=self.label_turn_player3, size=(self.label_turn_player3_width * self.settings.RATIO_ALL, self.label_turn_player3_height * self.settings.RATIO_ALL))
        self.label_turn_player3_new_rect = self.label_turn_player3_new.get_rect()
        self.screen.blit(self.label_turn_player3_new, self.surface_json['label']['label_turn_player3'])
        self.label_turn_player3_new_rect.x += self.surface_json['label']['label_turn_player3'][0]
        self.label_turn_player3_new_rect.y += self.surface_json['label']['label_turn_player3'][1]



        #label_turn_player4
        self.label_turn_player4 = pygame.image.load('images/label_turn_player4.png')
        self.label_turn_player4_2 = Image.open('images/label_turn_player4.png')
        self.label_turn_player4_width, self.label_turn_player4_height = self.label_turn_player4_2.size
        self.label_turn_player4_new = pygame.transform.scale(surface=self.label_turn_player4, size=(self.label_turn_player4_width * self.settings.RATIO_ALL, self.label_turn_player4_height * self.settings.RATIO_ALL))
        self.label_turn_player4_new_rect = self.label_turn_player4_new.get_rect()
        self.screen.blit(self.label_turn_player4_new, self.surface_json['label']['label_turn_player4'])
        self.label_turn_player4_new_rect.x += self.surface_json['label']['label_turn_player4'][0]
        self.label_turn_player4_new_rect.y += self.surface_json['label']['label_turn_player4'][1]



        #lost_city
        # self.lost_city = pygame.image.load('images/lost_city.png')
        # self.lost_city_2 = Image.open('images/lost_city.png')
        # self.lost_city_width, self.lost_city_height = self.lost_city_2.size
        # self.lost_city_new = pygame.transform.scale(surface=self.lost_city, size=(self.lost_city_width * self.settings.RATIO_ALL, self.lost_city_height * self.settings.RATIO_ALL))
        # self.lost_city_new_rect = self.lost_city_new.get_rect()
        # self.screen.blit(self.lost_city_new, self.surface_json['lost']['lost_city'])
        # self.lost_city_new_rect.x += self.surface_json['lost']['lost_city'][0]
        # self.lost_city_new_rect.y += self.surface_json['lost']['lost_city'][1]

#-------11_4_point初始化设置----------------------------------------------------------------------------------------------------------------------------------------

        #point_end
        #end图片初始化，用于46个按钮的调用
        self.point_end = pygame.image.load('images/point_end.png')
        self.point_end_2 = Image.open('images/point_end.png')
        self.point_end_width, self.point_end_height = self.point_end_2.size
        self.point_end_new = pygame.transform.scale(surface=self.point_end, size=(self.point_end_width * self.settings.RATIO_ALL, self.point_end_height * self.settings.RATIO_ALL))
        
        # 对46个点进行外接矩形的构建，同时定位矩形的位置。

        self.point_1_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['1'])
        self.point_1_end_new_rect.x += self.surface_point_json['1'][0]
        self.point_1_end_new_rect.y += self.surface_point_json['1'][1]


        self.point_2_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['2'])
        self.point_2_end_new_rect.x += self.surface_point_json['2'][0]
        self.point_2_end_new_rect.y += self.surface_point_json['2'][1]


        self.point_3_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['3'])
        self.point_3_end_new_rect.x += self.surface_point_json['3'][0]
        self.point_3_end_new_rect.y += self.surface_point_json['3'][1]


        self.point_4_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['4'])
        self.point_4_end_new_rect.x += self.surface_point_json['4'][0]
        self.point_4_end_new_rect.y += self.surface_point_json['4'][1]


        self.point_5_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['5'])
        self.point_5_end_new_rect.x += self.surface_point_json['5'][0]
        self.point_5_end_new_rect.y += self.surface_point_json['5'][1]


        self.point_6_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['6'])
        self.point_6_end_new_rect.x += self.surface_point_json['6'][0]
        self.point_6_end_new_rect.y += self.surface_point_json['6'][1]


        self.point_7_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['7'])
        self.point_7_end_new_rect.x += self.surface_point_json['7'][0]
        self.point_7_end_new_rect.y += self.surface_point_json['7'][1]


        self.point_8_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['8'])
        self.point_8_end_new_rect.x += self.surface_point_json['8'][0]
        self.point_8_end_new_rect.y += self.surface_point_json['8'][1]


        self.point_9_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['9'])
        self.point_9_end_new_rect.x += self.surface_point_json['9'][0]
        self.point_9_end_new_rect.y += self.surface_point_json['9'][1]


        self.point_10_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['10'])
        self.point_10_end_new_rect.x += self.surface_point_json['10'][0]
        self.point_10_end_new_rect.y += self.surface_point_json['10'][1]


        self.point_11_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['11'])
        self.point_11_end_new_rect.x += self.surface_point_json['11'][0]
        self.point_11_end_new_rect.y += self.surface_point_json['11'][1]


        self.point_12_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['12'])
        self.point_12_end_new_rect.x += self.surface_point_json['12'][0]
        self.point_12_end_new_rect.y += self.surface_point_json['12'][1]


        self.point_13_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['13'])
        self.point_13_end_new_rect.x += self.surface_point_json['13'][0]
        self.point_13_end_new_rect.y += self.surface_point_json['13'][1]


        self.point_14_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['14'])
        self.point_14_end_new_rect.x += self.surface_point_json['14'][0]
        self.point_14_end_new_rect.y += self.surface_point_json['14'][1]


        self.point_15_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['15'])
        self.point_15_end_new_rect.x += self.surface_point_json['15'][0]
        self.point_15_end_new_rect.y += self.surface_point_json['15'][1]


        self.point_16_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['16'])
        self.point_16_end_new_rect.x += self.surface_point_json['16'][0]
        self.point_16_end_new_rect.y += self.surface_point_json['16'][1]


        self.point_17_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['17'])
        self.point_17_end_new_rect.x += self.surface_point_json['17'][0]
        self.point_17_end_new_rect.y += self.surface_point_json['17'][1]


        self.point_18_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['18'])
        self.point_18_end_new_rect.x += self.surface_point_json['18'][0]
        self.point_18_end_new_rect.y += self.surface_point_json['18'][1]


        self.point_19_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['19'])
        self.point_19_end_new_rect.x += self.surface_point_json['19'][0]
        self.point_19_end_new_rect.y += self.surface_point_json['19'][1]


        self.point_20_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['20'])
        self.point_20_end_new_rect.x += self.surface_point_json['20'][0]
        self.point_20_end_new_rect.y += self.surface_point_json['20'][1]


        self.point_21_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['21'])
        self.point_21_end_new_rect.x += self.surface_point_json['21'][0]
        self.point_21_end_new_rect.y += self.surface_point_json['21'][1]


        self.point_22_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['22'])
        self.point_22_end_new_rect.x += self.surface_point_json['22'][0]
        self.point_22_end_new_rect.y += self.surface_point_json['22'][1]


        self.point_23_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['23'])
        self.point_23_end_new_rect.x += self.surface_point_json['23'][0]
        self.point_23_end_new_rect.y += self.surface_point_json['23'][1]


        self.point_24_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['24'])
        self.point_24_end_new_rect.x += self.surface_point_json['24'][0]
        self.point_24_end_new_rect.y += self.surface_point_json['24'][1]


        self.point_25_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['25'])
        self.point_25_end_new_rect.x += self.surface_point_json['25'][0]
        self.point_25_end_new_rect.y += self.surface_point_json['25'][1]


        self.point_26_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['26'])
        self.point_26_end_new_rect.x += self.surface_point_json['26'][0]
        self.point_26_end_new_rect.y += self.surface_point_json['26'][1]


        self.point_27_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['27'])
        self.point_27_end_new_rect.x += self.surface_point_json['27'][0]
        self.point_27_end_new_rect.y += self.surface_point_json['27'][1]


        self.point_28_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['28'])
        self.point_28_end_new_rect.x += self.surface_point_json['28'][0]
        self.point_28_end_new_rect.y += self.surface_point_json['28'][1]


        self.point_29_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['29'])
        self.point_29_end_new_rect.x += self.surface_point_json['29'][0]
        self.point_29_end_new_rect.y += self.surface_point_json['29'][1]


        self.point_30_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['30'])
        self.point_30_end_new_rect.x += self.surface_point_json['30'][0]
        self.point_30_end_new_rect.y += self.surface_point_json['30'][1]


        self.point_31_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['31'])
        self.point_31_end_new_rect.x += self.surface_point_json['31'][0]
        self.point_31_end_new_rect.y += self.surface_point_json['31'][1]


        self.point_32_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['32'])
        self.point_32_end_new_rect.x += self.surface_point_json['32'][0]
        self.point_32_end_new_rect.y += self.surface_point_json['32'][1]


        self.point_33_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['33'])
        self.point_33_end_new_rect.x += self.surface_point_json['33'][0]
        self.point_33_end_new_rect.y += self.surface_point_json['33'][1]


        self.point_34_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['34'])
        self.point_34_end_new_rect.x += self.surface_point_json['34'][0]
        self.point_34_end_new_rect.y += self.surface_point_json['34'][1]


        self.point_35_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['35'])
        self.point_35_end_new_rect.x += self.surface_point_json['35'][0]
        self.point_35_end_new_rect.y += self.surface_point_json['35'][1]


        self.point_36_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['36'])
        self.point_36_end_new_rect.x += self.surface_point_json['36'][0]
        self.point_36_end_new_rect.y += self.surface_point_json['36'][1]


        self.point_37_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['37'])
        self.point_37_end_new_rect.x += self.surface_point_json['37'][0]
        self.point_37_end_new_rect.y += self.surface_point_json['37'][1]


        self.point_38_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['38'])
        self.point_38_end_new_rect.x += self.surface_point_json['38'][0]
        self.point_38_end_new_rect.y += self.surface_point_json['38'][1]


        self.point_39_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['39'])
        self.point_39_end_new_rect.x += self.surface_point_json['39'][0]
        self.point_39_end_new_rect.y += self.surface_point_json['39'][1]


        self.point_40_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['40'])
        self.point_40_end_new_rect.x += self.surface_point_json['40'][0]
        self.point_40_end_new_rect.y += self.surface_point_json['40'][1]


        self.point_41_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['41'])
        self.point_41_end_new_rect.x += self.surface_point_json['41'][0]
        self.point_41_end_new_rect.y += self.surface_point_json['41'][1]


        self.point_42_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['42'])
        self.point_42_end_new_rect.x += self.surface_point_json['42'][0]
        self.point_42_end_new_rect.y += self.surface_point_json['42'][1]


        self.point_43_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['43'])
        self.point_43_end_new_rect.x += self.surface_point_json['43'][0]
        self.point_43_end_new_rect.y += self.surface_point_json['43'][1]


        self.point_44_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['44'])
        self.point_44_end_new_rect.x += self.surface_point_json['44'][0]
        self.point_44_end_new_rect.y += self.surface_point_json['44'][1]


        self.point_45_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['45'])
        self.point_45_end_new_rect.x += self.surface_point_json['45'][0]
        self.point_45_end_new_rect.y += self.surface_point_json['45'][1]


        self.point_46_end_new_rect = self.point_end_new.get_rect()
        self.screen.blit(self.point_end_new, self.surface_point_json['46'])
        self.point_46_end_new_rect.x += self.surface_point_json['46'][0]
        self.point_46_end_new_rect.y += self.surface_point_json['46'][1]

        #point_trap
        #trap图片初始化，用于46个按钮的调用
        self.point_trap = pygame.image.load('images/point_trap.png')
        self.point_trap_2 = Image.open('images/point_trap.png')
        self.point_trap_width, self.point_trap_height = self.point_trap_2.size
        self.point_trap_new = pygame.transform.scale(surface=self.point_trap, size=(self.point_trap_width * self.settings.RATIO_ALL, self.point_trap_height * self.settings.RATIO_ALL))
        
        # 对46个点进行外接矩形的构建，同时定位矩形的位置。

        self.point_1_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['1'])
        self.point_1_trap_new_rect.x += self.surface_point_json['1'][0]
        self.point_1_trap_new_rect.y += self.surface_point_json['1'][1]


        self.point_2_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['2'])
        self.point_2_trap_new_rect.x += self.surface_point_json['2'][0]
        self.point_2_trap_new_rect.y += self.surface_point_json['2'][1]


        self.point_3_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['3'])
        self.point_3_trap_new_rect.x += self.surface_point_json['3'][0]
        self.point_3_trap_new_rect.y += self.surface_point_json['3'][1]


        self.point_4_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['4'])
        self.point_4_trap_new_rect.x += self.surface_point_json['4'][0]
        self.point_4_trap_new_rect.y += self.surface_point_json['4'][1]


        self.point_5_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['5'])
        self.point_5_trap_new_rect.x += self.surface_point_json['5'][0]
        self.point_5_trap_new_rect.y += self.surface_point_json['5'][1]


        self.point_6_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['6'])
        self.point_6_trap_new_rect.x += self.surface_point_json['6'][0]
        self.point_6_trap_new_rect.y += self.surface_point_json['6'][1]


        self.point_7_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['7'])
        self.point_7_trap_new_rect.x += self.surface_point_json['7'][0]
        self.point_7_trap_new_rect.y += self.surface_point_json['7'][1]


        self.point_8_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['8'])
        self.point_8_trap_new_rect.x += self.surface_point_json['8'][0]
        self.point_8_trap_new_rect.y += self.surface_point_json['8'][1]


        self.point_9_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['9'])
        self.point_9_trap_new_rect.x += self.surface_point_json['9'][0]
        self.point_9_trap_new_rect.y += self.surface_point_json['9'][1]


        self.point_10_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['10'])
        self.point_10_trap_new_rect.x += self.surface_point_json['10'][0]
        self.point_10_trap_new_rect.y += self.surface_point_json['10'][1]


        self.point_11_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['11'])
        self.point_11_trap_new_rect.x += self.surface_point_json['11'][0]
        self.point_11_trap_new_rect.y += self.surface_point_json['11'][1]


        self.point_12_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['12'])
        self.point_12_trap_new_rect.x += self.surface_point_json['12'][0]
        self.point_12_trap_new_rect.y += self.surface_point_json['12'][1]


        self.point_13_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['13'])
        self.point_13_trap_new_rect.x += self.surface_point_json['13'][0]
        self.point_13_trap_new_rect.y += self.surface_point_json['13'][1]


        self.point_14_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['14'])
        self.point_14_trap_new_rect.x += self.surface_point_json['14'][0]
        self.point_14_trap_new_rect.y += self.surface_point_json['14'][1]


        self.point_15_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['15'])
        self.point_15_trap_new_rect.x += self.surface_point_json['15'][0]
        self.point_15_trap_new_rect.y += self.surface_point_json['15'][1]


        self.point_16_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['16'])
        self.point_16_trap_new_rect.x += self.surface_point_json['16'][0]
        self.point_16_trap_new_rect.y += self.surface_point_json['16'][1]


        self.point_17_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['17'])
        self.point_17_trap_new_rect.x += self.surface_point_json['17'][0]
        self.point_17_trap_new_rect.y += self.surface_point_json['17'][1]


        self.point_18_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['18'])
        self.point_18_trap_new_rect.x += self.surface_point_json['18'][0]
        self.point_18_trap_new_rect.y += self.surface_point_json['18'][1]


        self.point_19_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['19'])
        self.point_19_trap_new_rect.x += self.surface_point_json['19'][0]
        self.point_19_trap_new_rect.y += self.surface_point_json['19'][1]


        self.point_20_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['20'])
        self.point_20_trap_new_rect.x += self.surface_point_json['20'][0]
        self.point_20_trap_new_rect.y += self.surface_point_json['20'][1]


        self.point_21_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['21'])
        self.point_21_trap_new_rect.x += self.surface_point_json['21'][0]
        self.point_21_trap_new_rect.y += self.surface_point_json['21'][1]


        self.point_22_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['22'])
        self.point_22_trap_new_rect.x += self.surface_point_json['22'][0]
        self.point_22_trap_new_rect.y += self.surface_point_json['22'][1]


        self.point_23_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['23'])
        self.point_23_trap_new_rect.x += self.surface_point_json['23'][0]
        self.point_23_trap_new_rect.y += self.surface_point_json['23'][1]


        self.point_24_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['24'])
        self.point_24_trap_new_rect.x += self.surface_point_json['24'][0]
        self.point_24_trap_new_rect.y += self.surface_point_json['24'][1]


        self.point_25_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['25'])
        self.point_25_trap_new_rect.x += self.surface_point_json['25'][0]
        self.point_25_trap_new_rect.y += self.surface_point_json['25'][1]


        self.point_26_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['26'])
        self.point_26_trap_new_rect.x += self.surface_point_json['26'][0]
        self.point_26_trap_new_rect.y += self.surface_point_json['26'][1]


        self.point_27_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['27'])
        self.point_27_trap_new_rect.x += self.surface_point_json['27'][0]
        self.point_27_trap_new_rect.y += self.surface_point_json['27'][1]


        self.point_28_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['28'])
        self.point_28_trap_new_rect.x += self.surface_point_json['28'][0]
        self.point_28_trap_new_rect.y += self.surface_point_json['28'][1]


        self.point_29_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['29'])
        self.point_29_trap_new_rect.x += self.surface_point_json['29'][0]
        self.point_29_trap_new_rect.y += self.surface_point_json['29'][1]


        self.point_30_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['30'])
        self.point_30_trap_new_rect.x += self.surface_point_json['30'][0]
        self.point_30_trap_new_rect.y += self.surface_point_json['30'][1]


        self.point_31_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['31'])
        self.point_31_trap_new_rect.x += self.surface_point_json['31'][0]
        self.point_31_trap_new_rect.y += self.surface_point_json['31'][1]


        self.point_32_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['32'])
        self.point_32_trap_new_rect.x += self.surface_point_json['32'][0]
        self.point_32_trap_new_rect.y += self.surface_point_json['32'][1]


        self.point_33_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['33'])
        self.point_33_trap_new_rect.x += self.surface_point_json['33'][0]
        self.point_33_trap_new_rect.y += self.surface_point_json['33'][1]


        self.point_34_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['34'])
        self.point_34_trap_new_rect.x += self.surface_point_json['34'][0]
        self.point_34_trap_new_rect.y += self.surface_point_json['34'][1]


        self.point_35_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['35'])
        self.point_35_trap_new_rect.x += self.surface_point_json['35'][0]
        self.point_35_trap_new_rect.y += self.surface_point_json['35'][1]


        self.point_36_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['36'])
        self.point_36_trap_new_rect.x += self.surface_point_json['36'][0]
        self.point_36_trap_new_rect.y += self.surface_point_json['36'][1]


        self.point_37_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['37'])
        self.point_37_trap_new_rect.x += self.surface_point_json['37'][0]
        self.point_37_trap_new_rect.y += self.surface_point_json['37'][1]


        self.point_38_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['38'])
        self.point_38_trap_new_rect.x += self.surface_point_json['38'][0]
        self.point_38_trap_new_rect.y += self.surface_point_json['38'][1]


        self.point_39_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['39'])
        self.point_39_trap_new_rect.x += self.surface_point_json['39'][0]
        self.point_39_trap_new_rect.y += self.surface_point_json['39'][1]


        self.point_40_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['40'])
        self.point_40_trap_new_rect.x += self.surface_point_json['40'][0]
        self.point_40_trap_new_rect.y += self.surface_point_json['40'][1]


        self.point_41_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['41'])
        self.point_41_trap_new_rect.x += self.surface_point_json['41'][0]
        self.point_41_trap_new_rect.y += self.surface_point_json['41'][1]


        self.point_42_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['42'])
        self.point_42_trap_new_rect.x += self.surface_point_json['42'][0]
        self.point_42_trap_new_rect.y += self.surface_point_json['42'][1]


        self.point_43_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['43'])
        self.point_43_trap_new_rect.x += self.surface_point_json['43'][0]
        self.point_43_trap_new_rect.y += self.surface_point_json['43'][1]


        self.point_44_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['44'])
        self.point_44_trap_new_rect.x += self.surface_point_json['44'][0]
        self.point_44_trap_new_rect.y += self.surface_point_json['44'][1]


        self.point_45_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['45'])
        self.point_45_trap_new_rect.x += self.surface_point_json['45'][0]
        self.point_45_trap_new_rect.y += self.surface_point_json['45'][1]


        self.point_46_trap_new_rect = self.point_trap_new.get_rect()
        self.screen.blit(self.point_trap_new, self.surface_point_json['46'])
        self.point_46_trap_new_rect.x += self.surface_point_json['46'][0]
        self.point_46_trap_new_rect.y += self.surface_point_json['46'][1]



        #point_war
        #war图片初始化，用于46个按钮的调用
        self.point_war = pygame.image.load('images/point_war.png')
        self.point_war_2 = Image.open('images/point_war.png')
        self.point_war_width, self.point_war_height = self.point_war_2.size
        self.point_war_new = pygame.transform.scale(surface=self.point_war, size=(self.point_war_width * self.settings.RATIO_ALL, self.point_war_height * self.settings.RATIO_ALL))
        
        # 对46个点进行外接矩形的构建，同时定位矩形的位置。

        self.point_1_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['1'])
        self.point_1_war_new_rect.x += self.surface_point_json['1'][0]
        self.point_1_war_new_rect.y += self.surface_point_json['1'][1]


        self.point_2_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['2'])
        self.point_2_war_new_rect.x += self.surface_point_json['2'][0]
        self.point_2_war_new_rect.y += self.surface_point_json['2'][1]


        self.point_3_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['3'])
        self.point_3_war_new_rect.x += self.surface_point_json['3'][0]
        self.point_3_war_new_rect.y += self.surface_point_json['3'][1]


        self.point_4_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['4'])
        self.point_4_war_new_rect.x += self.surface_point_json['4'][0]
        self.point_4_war_new_rect.y += self.surface_point_json['4'][1]


        self.point_5_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['5'])
        self.point_5_war_new_rect.x += self.surface_point_json['5'][0]
        self.point_5_war_new_rect.y += self.surface_point_json['5'][1]


        self.point_6_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['6'])
        self.point_6_war_new_rect.x += self.surface_point_json['6'][0]
        self.point_6_war_new_rect.y += self.surface_point_json['6'][1]


        self.point_7_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['7'])
        self.point_7_war_new_rect.x += self.surface_point_json['7'][0]
        self.point_7_war_new_rect.y += self.surface_point_json['7'][1]


        self.point_8_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['8'])
        self.point_8_war_new_rect.x += self.surface_point_json['8'][0]
        self.point_8_war_new_rect.y += self.surface_point_json['8'][1]


        self.point_9_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['9'])
        self.point_9_war_new_rect.x += self.surface_point_json['9'][0]
        self.point_9_war_new_rect.y += self.surface_point_json['9'][1]


        self.point_10_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['10'])
        self.point_10_war_new_rect.x += self.surface_point_json['10'][0]
        self.point_10_war_new_rect.y += self.surface_point_json['10'][1]


        self.point_11_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['11'])
        self.point_11_war_new_rect.x += self.surface_point_json['11'][0]
        self.point_11_war_new_rect.y += self.surface_point_json['11'][1]


        self.point_12_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['12'])
        self.point_12_war_new_rect.x += self.surface_point_json['12'][0]
        self.point_12_war_new_rect.y += self.surface_point_json['12'][1]


        self.point_13_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['13'])
        self.point_13_war_new_rect.x += self.surface_point_json['13'][0]
        self.point_13_war_new_rect.y += self.surface_point_json['13'][1]


        self.point_14_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['14'])
        self.point_14_war_new_rect.x += self.surface_point_json['14'][0]
        self.point_14_war_new_rect.y += self.surface_point_json['14'][1]


        self.point_15_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['15'])
        self.point_15_war_new_rect.x += self.surface_point_json['15'][0]
        self.point_15_war_new_rect.y += self.surface_point_json['15'][1]


        self.point_16_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['16'])
        self.point_16_war_new_rect.x += self.surface_point_json['16'][0]
        self.point_16_war_new_rect.y += self.surface_point_json['16'][1]


        self.point_17_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['17'])
        self.point_17_war_new_rect.x += self.surface_point_json['17'][0]
        self.point_17_war_new_rect.y += self.surface_point_json['17'][1]


        self.point_18_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['18'])
        self.point_18_war_new_rect.x += self.surface_point_json['18'][0]
        self.point_18_war_new_rect.y += self.surface_point_json['18'][1]


        self.point_19_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['19'])
        self.point_19_war_new_rect.x += self.surface_point_json['19'][0]
        self.point_19_war_new_rect.y += self.surface_point_json['19'][1]


        self.point_20_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['20'])
        self.point_20_war_new_rect.x += self.surface_point_json['20'][0]
        self.point_20_war_new_rect.y += self.surface_point_json['20'][1]


        self.point_21_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['21'])
        self.point_21_war_new_rect.x += self.surface_point_json['21'][0]
        self.point_21_war_new_rect.y += self.surface_point_json['21'][1]


        self.point_22_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['22'])
        self.point_22_war_new_rect.x += self.surface_point_json['22'][0]
        self.point_22_war_new_rect.y += self.surface_point_json['22'][1]


        self.point_23_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['23'])
        self.point_23_war_new_rect.x += self.surface_point_json['23'][0]
        self.point_23_war_new_rect.y += self.surface_point_json['23'][1]


        self.point_24_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['24'])
        self.point_24_war_new_rect.x += self.surface_point_json['24'][0]
        self.point_24_war_new_rect.y += self.surface_point_json['24'][1]


        self.point_25_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['25'])
        self.point_25_war_new_rect.x += self.surface_point_json['25'][0]
        self.point_25_war_new_rect.y += self.surface_point_json['25'][1]


        self.point_26_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['26'])
        self.point_26_war_new_rect.x += self.surface_point_json['26'][0]
        self.point_26_war_new_rect.y += self.surface_point_json['26'][1]


        self.point_27_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['27'])
        self.point_27_war_new_rect.x += self.surface_point_json['27'][0]
        self.point_27_war_new_rect.y += self.surface_point_json['27'][1]


        self.point_28_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['28'])
        self.point_28_war_new_rect.x += self.surface_point_json['28'][0]
        self.point_28_war_new_rect.y += self.surface_point_json['28'][1]


        self.point_29_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['29'])
        self.point_29_war_new_rect.x += self.surface_point_json['29'][0]
        self.point_29_war_new_rect.y += self.surface_point_json['29'][1]


        self.point_30_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['30'])
        self.point_30_war_new_rect.x += self.surface_point_json['30'][0]
        self.point_30_war_new_rect.y += self.surface_point_json['30'][1]


        self.point_31_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['31'])
        self.point_31_war_new_rect.x += self.surface_point_json['31'][0]
        self.point_31_war_new_rect.y += self.surface_point_json['31'][1]


        self.point_32_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['32'])
        self.point_32_war_new_rect.x += self.surface_point_json['32'][0]
        self.point_32_war_new_rect.y += self.surface_point_json['32'][1]


        self.point_33_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['33'])
        self.point_33_war_new_rect.x += self.surface_point_json['33'][0]
        self.point_33_war_new_rect.y += self.surface_point_json['33'][1]


        self.point_34_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['34'])
        self.point_34_war_new_rect.x += self.surface_point_json['34'][0]
        self.point_34_war_new_rect.y += self.surface_point_json['34'][1]


        self.point_35_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['35'])
        self.point_35_war_new_rect.x += self.surface_point_json['35'][0]
        self.point_35_war_new_rect.y += self.surface_point_json['35'][1]


        self.point_36_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['36'])
        self.point_36_war_new_rect.x += self.surface_point_json['36'][0]
        self.point_36_war_new_rect.y += self.surface_point_json['36'][1]


        self.point_37_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['37'])
        self.point_37_war_new_rect.x += self.surface_point_json['37'][0]
        self.point_37_war_new_rect.y += self.surface_point_json['37'][1]


        self.point_38_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['38'])
        self.point_38_war_new_rect.x += self.surface_point_json['38'][0]
        self.point_38_war_new_rect.y += self.surface_point_json['38'][1]


        self.point_39_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['39'])
        self.point_39_war_new_rect.x += self.surface_point_json['39'][0]
        self.point_39_war_new_rect.y += self.surface_point_json['39'][1]


        self.point_40_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['40'])
        self.point_40_war_new_rect.x += self.surface_point_json['40'][0]
        self.point_40_war_new_rect.y += self.surface_point_json['40'][1]


        self.point_41_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['41'])
        self.point_41_war_new_rect.x += self.surface_point_json['41'][0]
        self.point_41_war_new_rect.y += self.surface_point_json['41'][1]


        self.point_42_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['42'])
        self.point_42_war_new_rect.x += self.surface_point_json['42'][0]
        self.point_42_war_new_rect.y += self.surface_point_json['42'][1]


        self.point_43_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['43'])
        self.point_43_war_new_rect.x += self.surface_point_json['43'][0]
        self.point_43_war_new_rect.y += self.surface_point_json['43'][1]


        self.point_44_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['44'])
        self.point_44_war_new_rect.x += self.surface_point_json['44'][0]
        self.point_44_war_new_rect.y += self.surface_point_json['44'][1]


        self.point_45_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['45'])
        self.point_45_war_new_rect.x += self.surface_point_json['45'][0]
        self.point_45_war_new_rect.y += self.surface_point_json['45'][1]


        self.point_46_war_new_rect = self.point_war_new.get_rect()
        self.screen.blit(self.point_war_new, self.surface_point_json['46'])
        self.point_46_war_new_rect.x += self.surface_point_json['46'][0]
        self.point_46_war_new_rect.y += self.surface_point_json['46'][1]


        #point_player1
        #player1图片初始化，用于46个按钮的调用
        self.point_player1 = pygame.image.load('images/point_player1.png')
        self.point_player1_2 = Image.open('images/point_player1.png')
        self.point_player1_width, self.point_player1_height = self.point_player1_2.size
        self.point_player1_new = pygame.transform.scale(surface=self.point_player1, size=(self.point_player1_width * self.settings.RATIO_ALL, self.point_player1_height * self.settings.RATIO_ALL))
        
        # 对46个点进行外接矩形的构建，同时定位矩形的位置。

        self.point_1_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['1'])
        self.point_1_player1_new_rect.x += self.surface_point_player_json['1'][0]
        self.point_1_player1_new_rect.y += self.surface_point_player_json['1'][1]


        self.point_2_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['2'])
        self.point_2_player1_new_rect.x += self.surface_point_player_json['2'][0]
        self.point_2_player1_new_rect.y += self.surface_point_player_json['2'][1]


        self.point_3_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['3'])
        self.point_3_player1_new_rect.x += self.surface_point_player_json['3'][0]
        self.point_3_player1_new_rect.y += self.surface_point_player_json['3'][1]


        self.point_4_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['4'])
        self.point_4_player1_new_rect.x += self.surface_point_player_json['4'][0]
        self.point_4_player1_new_rect.y += self.surface_point_player_json['4'][1]


        self.point_5_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['5'])
        self.point_5_player1_new_rect.x += self.surface_point_player_json['5'][0]
        self.point_5_player1_new_rect.y += self.surface_point_player_json['5'][1]


        self.point_6_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['6'])
        self.point_6_player1_new_rect.x += self.surface_point_player_json['6'][0]
        self.point_6_player1_new_rect.y += self.surface_point_player_json['6'][1]


        self.point_7_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['7'])
        self.point_7_player1_new_rect.x += self.surface_point_player_json['7'][0]
        self.point_7_player1_new_rect.y += self.surface_point_player_json['7'][1]


        self.point_8_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['8'])
        self.point_8_player1_new_rect.x += self.surface_point_player_json['8'][0]
        self.point_8_player1_new_rect.y += self.surface_point_player_json['8'][1]


        self.point_9_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['9'])
        self.point_9_player1_new_rect.x += self.surface_point_player_json['9'][0]
        self.point_9_player1_new_rect.y += self.surface_point_player_json['9'][1]


        self.point_10_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['10'])
        self.point_10_player1_new_rect.x += self.surface_point_player_json['10'][0]
        self.point_10_player1_new_rect.y += self.surface_point_player_json['10'][1]


        self.point_11_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['11'])
        self.point_11_player1_new_rect.x += self.surface_point_player_json['11'][0]
        self.point_11_player1_new_rect.y += self.surface_point_player_json['11'][1]


        self.point_12_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['12'])
        self.point_12_player1_new_rect.x += self.surface_point_player_json['12'][0]
        self.point_12_player1_new_rect.y += self.surface_point_player_json['12'][1]


        self.point_13_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['13'])
        self.point_13_player1_new_rect.x += self.surface_point_player_json['13'][0]
        self.point_13_player1_new_rect.y += self.surface_point_player_json['13'][1]


        self.point_14_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['14'])
        self.point_14_player1_new_rect.x += self.surface_point_player_json['14'][0]
        self.point_14_player1_new_rect.y += self.surface_point_player_json['14'][1]


        self.point_15_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['15'])
        self.point_15_player1_new_rect.x += self.surface_point_player_json['15'][0]
        self.point_15_player1_new_rect.y += self.surface_point_player_json['15'][1]


        self.point_16_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['16'])
        self.point_16_player1_new_rect.x += self.surface_point_player_json['16'][0]
        self.point_16_player1_new_rect.y += self.surface_point_player_json['16'][1]


        self.point_17_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['17'])
        self.point_17_player1_new_rect.x += self.surface_point_player_json['17'][0]
        self.point_17_player1_new_rect.y += self.surface_point_player_json['17'][1]


        self.point_18_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['18'])
        self.point_18_player1_new_rect.x += self.surface_point_player_json['18'][0]
        self.point_18_player1_new_rect.y += self.surface_point_player_json['18'][1]


        self.point_19_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['19'])
        self.point_19_player1_new_rect.x += self.surface_point_player_json['19'][0]
        self.point_19_player1_new_rect.y += self.surface_point_player_json['19'][1]


        self.point_20_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['20'])
        self.point_20_player1_new_rect.x += self.surface_point_player_json['20'][0]
        self.point_20_player1_new_rect.y += self.surface_point_player_json['20'][1]


        self.point_21_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['21'])
        self.point_21_player1_new_rect.x += self.surface_point_player_json['21'][0]
        self.point_21_player1_new_rect.y += self.surface_point_player_json['21'][1]


        self.point_22_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['22'])
        self.point_22_player1_new_rect.x += self.surface_point_player_json['22'][0]
        self.point_22_player1_new_rect.y += self.surface_point_player_json['22'][1]


        self.point_23_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['23'])
        self.point_23_player1_new_rect.x += self.surface_point_player_json['23'][0]
        self.point_23_player1_new_rect.y += self.surface_point_player_json['23'][1]


        self.point_24_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['24'])
        self.point_24_player1_new_rect.x += self.surface_point_player_json['24'][0]
        self.point_24_player1_new_rect.y += self.surface_point_player_json['24'][1]


        self.point_25_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['25'])
        self.point_25_player1_new_rect.x += self.surface_point_player_json['25'][0]
        self.point_25_player1_new_rect.y += self.surface_point_player_json['25'][1]


        self.point_26_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['26'])
        self.point_26_player1_new_rect.x += self.surface_point_player_json['26'][0]
        self.point_26_player1_new_rect.y += self.surface_point_player_json['26'][1]


        self.point_27_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['27'])
        self.point_27_player1_new_rect.x += self.surface_point_player_json['27'][0]
        self.point_27_player1_new_rect.y += self.surface_point_player_json['27'][1]


        self.point_28_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['28'])
        self.point_28_player1_new_rect.x += self.surface_point_player_json['28'][0]
        self.point_28_player1_new_rect.y += self.surface_point_player_json['28'][1]


        self.point_29_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['29'])
        self.point_29_player1_new_rect.x += self.surface_point_player_json['29'][0]
        self.point_29_player1_new_rect.y += self.surface_point_player_json['29'][1]


        self.point_30_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['30'])
        self.point_30_player1_new_rect.x += self.surface_point_player_json['30'][0]
        self.point_30_player1_new_rect.y += self.surface_point_player_json['30'][1]


        self.point_31_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['31'])
        self.point_31_player1_new_rect.x += self.surface_point_player_json['31'][0]
        self.point_31_player1_new_rect.y += self.surface_point_player_json['31'][1]


        self.point_32_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['32'])
        self.point_32_player1_new_rect.x += self.surface_point_player_json['32'][0]
        self.point_32_player1_new_rect.y += self.surface_point_player_json['32'][1]


        self.point_33_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['33'])
        self.point_33_player1_new_rect.x += self.surface_point_player_json['33'][0]
        self.point_33_player1_new_rect.y += self.surface_point_player_json['33'][1]


        self.point_34_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['34'])
        self.point_34_player1_new_rect.x += self.surface_point_player_json['34'][0]
        self.point_34_player1_new_rect.y += self.surface_point_player_json['34'][1]


        self.point_35_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['35'])
        self.point_35_player1_new_rect.x += self.surface_point_player_json['35'][0]
        self.point_35_player1_new_rect.y += self.surface_point_player_json['35'][1]


        self.point_36_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['36'])
        self.point_36_player1_new_rect.x += self.surface_point_player_json['36'][0]
        self.point_36_player1_new_rect.y += self.surface_point_player_json['36'][1]


        self.point_37_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['37'])
        self.point_37_player1_new_rect.x += self.surface_point_player_json['37'][0]
        self.point_37_player1_new_rect.y += self.surface_point_player_json['37'][1]


        self.point_38_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['38'])
        self.point_38_player1_new_rect.x += self.surface_point_player_json['38'][0]
        self.point_38_player1_new_rect.y += self.surface_point_player_json['38'][1]


        self.point_39_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['39'])
        self.point_39_player1_new_rect.x += self.surface_point_player_json['39'][0]
        self.point_39_player1_new_rect.y += self.surface_point_player_json['39'][1]


        self.point_40_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['40'])
        self.point_40_player1_new_rect.x += self.surface_point_player_json['40'][0]
        self.point_40_player1_new_rect.y += self.surface_point_player_json['40'][1]


        self.point_41_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['41'])
        self.point_41_player1_new_rect.x += self.surface_point_player_json['41'][0]
        self.point_41_player1_new_rect.y += self.surface_point_player_json['41'][1]


        self.point_42_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['42'])
        self.point_42_player1_new_rect.x += self.surface_point_player_json['42'][0]
        self.point_42_player1_new_rect.y += self.surface_point_player_json['42'][1]


        self.point_43_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['43'])
        self.point_43_player1_new_rect.x += self.surface_point_player_json['43'][0]
        self.point_43_player1_new_rect.y += self.surface_point_player_json['43'][1]


        self.point_44_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['44'])
        self.point_44_player1_new_rect.x += self.surface_point_player_json['44'][0]
        self.point_44_player1_new_rect.y += self.surface_point_player_json['44'][1]


        self.point_45_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['45'])
        self.point_45_player1_new_rect.x += self.surface_point_player_json['45'][0]
        self.point_45_player1_new_rect.y += self.surface_point_player_json['45'][1]


        self.point_46_player1_new_rect = self.point_player1_new.get_rect()
        self.screen.blit(self.point_player1_new, self.surface_point_player_json['46'])
        self.point_46_player1_new_rect.x += self.surface_point_player_json['46'][0]
        self.point_46_player1_new_rect.y += self.surface_point_player_json['46'][1]




    #point_player2
        #player2图片初始化，用于46个按钮的调用
        self.point_player2 = pygame.image.load('images/point_player2.png')
        self.point_player2_2 = Image.open('images/point_player2.png')
        self.point_player2_width, self.point_player2_height = self.point_player2_2.size
        self.point_player2_new = pygame.transform.scale(surface=self.point_player2, size=(self.point_player2_width * self.settings.RATIO_ALL, self.point_player2_height * self.settings.RATIO_ALL))
        
        # 对46个点进行外接矩形的构建，同时定位矩形的位置。

        self.point_1_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['1'])
        self.point_1_player2_new_rect.x += self.surface_point_player_json['1'][0]
        self.point_1_player2_new_rect.y += self.surface_point_player_json['1'][1]


        self.point_2_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['2'])
        self.point_2_player2_new_rect.x += self.surface_point_player_json['2'][0]
        self.point_2_player2_new_rect.y += self.surface_point_player_json['2'][1]


        self.point_3_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['3'])
        self.point_3_player2_new_rect.x += self.surface_point_player_json['3'][0]
        self.point_3_player2_new_rect.y += self.surface_point_player_json['3'][1]


        self.point_4_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['4'])
        self.point_4_player2_new_rect.x += self.surface_point_player_json['4'][0]
        self.point_4_player2_new_rect.y += self.surface_point_player_json['4'][1]


        self.point_5_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['5'])
        self.point_5_player2_new_rect.x += self.surface_point_player_json['5'][0]
        self.point_5_player2_new_rect.y += self.surface_point_player_json['5'][1]


        self.point_6_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['6'])
        self.point_6_player2_new_rect.x += self.surface_point_player_json['6'][0]
        self.point_6_player2_new_rect.y += self.surface_point_player_json['6'][1]


        self.point_7_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['7'])
        self.point_7_player2_new_rect.x += self.surface_point_player_json['7'][0]
        self.point_7_player2_new_rect.y += self.surface_point_player_json['7'][1]


        self.point_8_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['8'])
        self.point_8_player2_new_rect.x += self.surface_point_player_json['8'][0]
        self.point_8_player2_new_rect.y += self.surface_point_player_json['8'][1]


        self.point_9_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['9'])
        self.point_9_player2_new_rect.x += self.surface_point_player_json['9'][0]
        self.point_9_player2_new_rect.y += self.surface_point_player_json['9'][1]


        self.point_10_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['10'])
        self.point_10_player2_new_rect.x += self.surface_point_player_json['10'][0]
        self.point_10_player2_new_rect.y += self.surface_point_player_json['10'][1]


        self.point_11_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['11'])
        self.point_11_player2_new_rect.x += self.surface_point_player_json['11'][0]
        self.point_11_player2_new_rect.y += self.surface_point_player_json['11'][1]


        self.point_12_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['12'])
        self.point_12_player2_new_rect.x += self.surface_point_player_json['12'][0]
        self.point_12_player2_new_rect.y += self.surface_point_player_json['12'][1]


        self.point_13_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['13'])
        self.point_13_player2_new_rect.x += self.surface_point_player_json['13'][0]
        self.point_13_player2_new_rect.y += self.surface_point_player_json['13'][1]


        self.point_14_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['14'])
        self.point_14_player2_new_rect.x += self.surface_point_player_json['14'][0]
        self.point_14_player2_new_rect.y += self.surface_point_player_json['14'][1]


        self.point_15_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['15'])
        self.point_15_player2_new_rect.x += self.surface_point_player_json['15'][0]
        self.point_15_player2_new_rect.y += self.surface_point_player_json['15'][1]


        self.point_16_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['16'])
        self.point_16_player2_new_rect.x += self.surface_point_player_json['16'][0]
        self.point_16_player2_new_rect.y += self.surface_point_player_json['16'][1]


        self.point_17_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['17'])
        self.point_17_player2_new_rect.x += self.surface_point_player_json['17'][0]
        self.point_17_player2_new_rect.y += self.surface_point_player_json['17'][1]


        self.point_18_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['18'])
        self.point_18_player2_new_rect.x += self.surface_point_player_json['18'][0]
        self.point_18_player2_new_rect.y += self.surface_point_player_json['18'][1]


        self.point_19_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['19'])
        self.point_19_player2_new_rect.x += self.surface_point_player_json['19'][0]
        self.point_19_player2_new_rect.y += self.surface_point_player_json['19'][1]


        self.point_20_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['20'])
        self.point_20_player2_new_rect.x += self.surface_point_player_json['20'][0]
        self.point_20_player2_new_rect.y += self.surface_point_player_json['20'][1]


        self.point_21_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['21'])
        self.point_21_player2_new_rect.x += self.surface_point_player_json['21'][0]
        self.point_21_player2_new_rect.y += self.surface_point_player_json['21'][1]


        self.point_22_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['22'])
        self.point_22_player2_new_rect.x += self.surface_point_player_json['22'][0]
        self.point_22_player2_new_rect.y += self.surface_point_player_json['22'][1]


        self.point_23_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['23'])
        self.point_23_player2_new_rect.x += self.surface_point_player_json['23'][0]
        self.point_23_player2_new_rect.y += self.surface_point_player_json['23'][1]


        self.point_24_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['24'])
        self.point_24_player2_new_rect.x += self.surface_point_player_json['24'][0]
        self.point_24_player2_new_rect.y += self.surface_point_player_json['24'][1]


        self.point_25_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['25'])
        self.point_25_player2_new_rect.x += self.surface_point_player_json['25'][0]
        self.point_25_player2_new_rect.y += self.surface_point_player_json['25'][1]


        self.point_26_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['26'])
        self.point_26_player2_new_rect.x += self.surface_point_player_json['26'][0]
        self.point_26_player2_new_rect.y += self.surface_point_player_json['26'][1]


        self.point_27_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['27'])
        self.point_27_player2_new_rect.x += self.surface_point_player_json['27'][0]
        self.point_27_player2_new_rect.y += self.surface_point_player_json['27'][1]


        self.point_28_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['28'])
        self.point_28_player2_new_rect.x += self.surface_point_player_json['28'][0]
        self.point_28_player2_new_rect.y += self.surface_point_player_json['28'][1]


        self.point_29_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['29'])
        self.point_29_player2_new_rect.x += self.surface_point_player_json['29'][0]
        self.point_29_player2_new_rect.y += self.surface_point_player_json['29'][1]


        self.point_30_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['30'])
        self.point_30_player2_new_rect.x += self.surface_point_player_json['30'][0]
        self.point_30_player2_new_rect.y += self.surface_point_player_json['30'][1]


        self.point_31_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['31'])
        self.point_31_player2_new_rect.x += self.surface_point_player_json['31'][0]
        self.point_31_player2_new_rect.y += self.surface_point_player_json['31'][1]


        self.point_32_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['32'])
        self.point_32_player2_new_rect.x += self.surface_point_player_json['32'][0]
        self.point_32_player2_new_rect.y += self.surface_point_player_json['32'][1]


        self.point_33_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['33'])
        self.point_33_player2_new_rect.x += self.surface_point_player_json['33'][0]
        self.point_33_player2_new_rect.y += self.surface_point_player_json['33'][1]


        self.point_34_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['34'])
        self.point_34_player2_new_rect.x += self.surface_point_player_json['34'][0]
        self.point_34_player2_new_rect.y += self.surface_point_player_json['34'][1]


        self.point_35_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['35'])
        self.point_35_player2_new_rect.x += self.surface_point_player_json['35'][0]
        self.point_35_player2_new_rect.y += self.surface_point_player_json['35'][1]


        self.point_36_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['36'])
        self.point_36_player2_new_rect.x += self.surface_point_player_json['36'][0]
        self.point_36_player2_new_rect.y += self.surface_point_player_json['36'][1]


        self.point_37_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['37'])
        self.point_37_player2_new_rect.x += self.surface_point_player_json['37'][0]
        self.point_37_player2_new_rect.y += self.surface_point_player_json['37'][1]


        self.point_38_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['38'])
        self.point_38_player2_new_rect.x += self.surface_point_player_json['38'][0]
        self.point_38_player2_new_rect.y += self.surface_point_player_json['38'][1]


        self.point_39_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['39'])
        self.point_39_player2_new_rect.x += self.surface_point_player_json['39'][0]
        self.point_39_player2_new_rect.y += self.surface_point_player_json['39'][1]


        self.point_40_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['40'])
        self.point_40_player2_new_rect.x += self.surface_point_player_json['40'][0]
        self.point_40_player2_new_rect.y += self.surface_point_player_json['40'][1]


        self.point_41_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['41'])
        self.point_41_player2_new_rect.x += self.surface_point_player_json['41'][0]
        self.point_41_player2_new_rect.y += self.surface_point_player_json['41'][1]


        self.point_42_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['42'])
        self.point_42_player2_new_rect.x += self.surface_point_player_json['42'][0]
        self.point_42_player2_new_rect.y += self.surface_point_player_json['42'][1]


        self.point_43_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['43'])
        self.point_43_player2_new_rect.x += self.surface_point_player_json['43'][0]
        self.point_43_player2_new_rect.y += self.surface_point_player_json['43'][1]


        self.point_44_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['44'])
        self.point_44_player2_new_rect.x += self.surface_point_player_json['44'][0]
        self.point_44_player2_new_rect.y += self.surface_point_player_json['44'][1]


        self.point_45_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['45'])
        self.point_45_player2_new_rect.x += self.surface_point_player_json['45'][0]
        self.point_45_player2_new_rect.y += self.surface_point_player_json['45'][1]


        self.point_46_player2_new_rect = self.point_player2_new.get_rect()
        self.screen.blit(self.point_player2_new, self.surface_point_player_json['46'])
        self.point_46_player2_new_rect.x += self.surface_point_player_json['46'][0]
        self.point_46_player2_new_rect.y += self.surface_point_player_json['46'][1]




        #point_player3
        #player3图片初始化，用于46个按钮的调用
        self.point_player3 = pygame.image.load('images/point_player3.png')
        self.point_player3_2 = Image.open('images/point_player3.png')
        self.point_player3_width, self.point_player3_height = self.point_player3_2.size
        self.point_player3_new = pygame.transform.scale(surface=self.point_player3, size=(self.point_player3_width * self.settings.RATIO_ALL, self.point_player3_height * self.settings.RATIO_ALL))
        
        # 对46个点进行外接矩形的构建，同时定位矩形的位置。

        self.point_1_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['1'])
        self.point_1_player3_new_rect.x += self.surface_point_player_json['1'][0]
        self.point_1_player3_new_rect.y += self.surface_point_player_json['1'][1]


        self.point_2_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['2'])
        self.point_2_player3_new_rect.x += self.surface_point_player_json['2'][0]
        self.point_2_player3_new_rect.y += self.surface_point_player_json['2'][1]


        self.point_3_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['3'])
        self.point_3_player3_new_rect.x += self.surface_point_player_json['3'][0]
        self.point_3_player3_new_rect.y += self.surface_point_player_json['3'][1]


        self.point_4_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['4'])
        self.point_4_player3_new_rect.x += self.surface_point_player_json['4'][0]
        self.point_4_player3_new_rect.y += self.surface_point_player_json['4'][1]


        self.point_5_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['5'])
        self.point_5_player3_new_rect.x += self.surface_point_player_json['5'][0]
        self.point_5_player3_new_rect.y += self.surface_point_player_json['5'][1]


        self.point_6_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['6'])
        self.point_6_player3_new_rect.x += self.surface_point_player_json['6'][0]
        self.point_6_player3_new_rect.y += self.surface_point_player_json['6'][1]


        self.point_7_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['7'])
        self.point_7_player3_new_rect.x += self.surface_point_player_json['7'][0]
        self.point_7_player3_new_rect.y += self.surface_point_player_json['7'][1]


        self.point_8_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['8'])
        self.point_8_player3_new_rect.x += self.surface_point_player_json['8'][0]
        self.point_8_player3_new_rect.y += self.surface_point_player_json['8'][1]


        self.point_9_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['9'])
        self.point_9_player3_new_rect.x += self.surface_point_player_json['9'][0]
        self.point_9_player3_new_rect.y += self.surface_point_player_json['9'][1]


        self.point_10_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['10'])
        self.point_10_player3_new_rect.x += self.surface_point_player_json['10'][0]
        self.point_10_player3_new_rect.y += self.surface_point_player_json['10'][1]


        self.point_11_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['11'])
        self.point_11_player3_new_rect.x += self.surface_point_player_json['11'][0]
        self.point_11_player3_new_rect.y += self.surface_point_player_json['11'][1]


        self.point_12_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['12'])
        self.point_12_player3_new_rect.x += self.surface_point_player_json['12'][0]
        self.point_12_player3_new_rect.y += self.surface_point_player_json['12'][1]


        self.point_13_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['13'])
        self.point_13_player3_new_rect.x += self.surface_point_player_json['13'][0]
        self.point_13_player3_new_rect.y += self.surface_point_player_json['13'][1]


        self.point_14_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['14'])
        self.point_14_player3_new_rect.x += self.surface_point_player_json['14'][0]
        self.point_14_player3_new_rect.y += self.surface_point_player_json['14'][1]


        self.point_15_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['15'])
        self.point_15_player3_new_rect.x += self.surface_point_player_json['15'][0]
        self.point_15_player3_new_rect.y += self.surface_point_player_json['15'][1]


        self.point_16_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['16'])
        self.point_16_player3_new_rect.x += self.surface_point_player_json['16'][0]
        self.point_16_player3_new_rect.y += self.surface_point_player_json['16'][1]


        self.point_17_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['17'])
        self.point_17_player3_new_rect.x += self.surface_point_player_json['17'][0]
        self.point_17_player3_new_rect.y += self.surface_point_player_json['17'][1]


        self.point_18_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['18'])
        self.point_18_player3_new_rect.x += self.surface_point_player_json['18'][0]
        self.point_18_player3_new_rect.y += self.surface_point_player_json['18'][1]


        self.point_19_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['19'])
        self.point_19_player3_new_rect.x += self.surface_point_player_json['19'][0]
        self.point_19_player3_new_rect.y += self.surface_point_player_json['19'][1]


        self.point_20_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['20'])
        self.point_20_player3_new_rect.x += self.surface_point_player_json['20'][0]
        self.point_20_player3_new_rect.y += self.surface_point_player_json['20'][1]


        self.point_21_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['21'])
        self.point_21_player3_new_rect.x += self.surface_point_player_json['21'][0]
        self.point_21_player3_new_rect.y += self.surface_point_player_json['21'][1]


        self.point_22_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['22'])
        self.point_22_player3_new_rect.x += self.surface_point_player_json['22'][0]
        self.point_22_player3_new_rect.y += self.surface_point_player_json['22'][1]


        self.point_23_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['23'])
        self.point_23_player3_new_rect.x += self.surface_point_player_json['23'][0]
        self.point_23_player3_new_rect.y += self.surface_point_player_json['23'][1]


        self.point_24_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['24'])
        self.point_24_player3_new_rect.x += self.surface_point_player_json['24'][0]
        self.point_24_player3_new_rect.y += self.surface_point_player_json['24'][1]


        self.point_25_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['25'])
        self.point_25_player3_new_rect.x += self.surface_point_player_json['25'][0]
        self.point_25_player3_new_rect.y += self.surface_point_player_json['25'][1]


        self.point_26_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['26'])
        self.point_26_player3_new_rect.x += self.surface_point_player_json['26'][0]
        self.point_26_player3_new_rect.y += self.surface_point_player_json['26'][1]


        self.point_27_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['27'])
        self.point_27_player3_new_rect.x += self.surface_point_player_json['27'][0]
        self.point_27_player3_new_rect.y += self.surface_point_player_json['27'][1]


        self.point_28_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['28'])
        self.point_28_player3_new_rect.x += self.surface_point_player_json['28'][0]
        self.point_28_player3_new_rect.y += self.surface_point_player_json['28'][1]


        self.point_29_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['29'])
        self.point_29_player3_new_rect.x += self.surface_point_player_json['29'][0]
        self.point_29_player3_new_rect.y += self.surface_point_player_json['29'][1]


        self.point_30_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['30'])
        self.point_30_player3_new_rect.x += self.surface_point_player_json['30'][0]
        self.point_30_player3_new_rect.y += self.surface_point_player_json['30'][1]


        self.point_31_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['31'])
        self.point_31_player3_new_rect.x += self.surface_point_player_json['31'][0]
        self.point_31_player3_new_rect.y += self.surface_point_player_json['31'][1]


        self.point_32_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['32'])
        self.point_32_player3_new_rect.x += self.surface_point_player_json['32'][0]
        self.point_32_player3_new_rect.y += self.surface_point_player_json['32'][1]


        self.point_33_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['33'])
        self.point_33_player3_new_rect.x += self.surface_point_player_json['33'][0]
        self.point_33_player3_new_rect.y += self.surface_point_player_json['33'][1]


        self.point_34_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['34'])
        self.point_34_player3_new_rect.x += self.surface_point_player_json['34'][0]
        self.point_34_player3_new_rect.y += self.surface_point_player_json['34'][1]


        self.point_35_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['35'])
        self.point_35_player3_new_rect.x += self.surface_point_player_json['35'][0]
        self.point_35_player3_new_rect.y += self.surface_point_player_json['35'][1]


        self.point_36_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['36'])
        self.point_36_player3_new_rect.x += self.surface_point_player_json['36'][0]
        self.point_36_player3_new_rect.y += self.surface_point_player_json['36'][1]


        self.point_37_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['37'])
        self.point_37_player3_new_rect.x += self.surface_point_player_json['37'][0]
        self.point_37_player3_new_rect.y += self.surface_point_player_json['37'][1]


        self.point_38_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['38'])
        self.point_38_player3_new_rect.x += self.surface_point_player_json['38'][0]
        self.point_38_player3_new_rect.y += self.surface_point_player_json['38'][1]


        self.point_39_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['39'])
        self.point_39_player3_new_rect.x += self.surface_point_player_json['39'][0]
        self.point_39_player3_new_rect.y += self.surface_point_player_json['39'][1]


        self.point_40_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['40'])
        self.point_40_player3_new_rect.x += self.surface_point_player_json['40'][0]
        self.point_40_player3_new_rect.y += self.surface_point_player_json['40'][1]


        self.point_41_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['41'])
        self.point_41_player3_new_rect.x += self.surface_point_player_json['41'][0]
        self.point_41_player3_new_rect.y += self.surface_point_player_json['41'][1]


        self.point_42_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['42'])
        self.point_42_player3_new_rect.x += self.surface_point_player_json['42'][0]
        self.point_42_player3_new_rect.y += self.surface_point_player_json['42'][1]


        self.point_43_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['43'])
        self.point_43_player3_new_rect.x += self.surface_point_player_json['43'][0]
        self.point_43_player3_new_rect.y += self.surface_point_player_json['43'][1]


        self.point_44_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['44'])
        self.point_44_player3_new_rect.x += self.surface_point_player_json['44'][0]
        self.point_44_player3_new_rect.y += self.surface_point_player_json['44'][1]


        self.point_45_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['45'])
        self.point_45_player3_new_rect.x += self.surface_point_player_json['45'][0]
        self.point_45_player3_new_rect.y += self.surface_point_player_json['45'][1]


        self.point_46_player3_new_rect = self.point_player3_new.get_rect()
        self.screen.blit(self.point_player3_new, self.surface_point_player_json['46'])
        self.point_46_player3_new_rect.x += self.surface_point_player_json['46'][0]
        self.point_46_player3_new_rect.y += self.surface_point_player_json['46'][1]



        #point_player4
        #player4图片初始化，用于46个按钮的调用
        self.point_player4 = pygame.image.load('images/point_player4.png')
        self.point_player4_2 = Image.open('images/point_player4.png')
        self.point_player4_width, self.point_player4_height = self.point_player4_2.size
        self.point_player4_new = pygame.transform.scale(surface=self.point_player4, size=(self.point_player4_width * self.settings.RATIO_ALL, self.point_player4_height * self.settings.RATIO_ALL))
        
        # 对46个点进行外接矩形的构建，同时定位矩形的位置。

        self.point_1_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['1'])
        self.point_1_player4_new_rect.x += self.surface_point_player_json['1'][0]
        self.point_1_player4_new_rect.y += self.surface_point_player_json['1'][1]


        self.point_2_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['2'])
        self.point_2_player4_new_rect.x += self.surface_point_player_json['2'][0]
        self.point_2_player4_new_rect.y += self.surface_point_player_json['2'][1]


        self.point_3_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['3'])
        self.point_3_player4_new_rect.x += self.surface_point_player_json['3'][0]
        self.point_3_player4_new_rect.y += self.surface_point_player_json['3'][1]


        self.point_4_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['4'])
        self.point_4_player4_new_rect.x += self.surface_point_player_json['4'][0]
        self.point_4_player4_new_rect.y += self.surface_point_player_json['4'][1]


        self.point_5_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['5'])
        self.point_5_player4_new_rect.x += self.surface_point_player_json['5'][0]
        self.point_5_player4_new_rect.y += self.surface_point_player_json['5'][1]


        self.point_6_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['6'])
        self.point_6_player4_new_rect.x += self.surface_point_player_json['6'][0]
        self.point_6_player4_new_rect.y += self.surface_point_player_json['6'][1]


        self.point_7_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['7'])
        self.point_7_player4_new_rect.x += self.surface_point_player_json['7'][0]
        self.point_7_player4_new_rect.y += self.surface_point_player_json['7'][1]


        self.point_8_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['8'])
        self.point_8_player4_new_rect.x += self.surface_point_player_json['8'][0]
        self.point_8_player4_new_rect.y += self.surface_point_player_json['8'][1]


        self.point_9_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['9'])
        self.point_9_player4_new_rect.x += self.surface_point_player_json['9'][0]
        self.point_9_player4_new_rect.y += self.surface_point_player_json['9'][1]


        self.point_10_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['10'])
        self.point_10_player4_new_rect.x += self.surface_point_player_json['10'][0]
        self.point_10_player4_new_rect.y += self.surface_point_player_json['10'][1]


        self.point_11_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['11'])
        self.point_11_player4_new_rect.x += self.surface_point_player_json['11'][0]
        self.point_11_player4_new_rect.y += self.surface_point_player_json['11'][1]


        self.point_12_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['12'])
        self.point_12_player4_new_rect.x += self.surface_point_player_json['12'][0]
        self.point_12_player4_new_rect.y += self.surface_point_player_json['12'][1]


        self.point_13_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['13'])
        self.point_13_player4_new_rect.x += self.surface_point_player_json['13'][0]
        self.point_13_player4_new_rect.y += self.surface_point_player_json['13'][1]


        self.point_14_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['14'])
        self.point_14_player4_new_rect.x += self.surface_point_player_json['14'][0]
        self.point_14_player4_new_rect.y += self.surface_point_player_json['14'][1]


        self.point_15_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['15'])
        self.point_15_player4_new_rect.x += self.surface_point_player_json['15'][0]
        self.point_15_player4_new_rect.y += self.surface_point_player_json['15'][1]


        self.point_16_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['16'])
        self.point_16_player4_new_rect.x += self.surface_point_player_json['16'][0]
        self.point_16_player4_new_rect.y += self.surface_point_player_json['16'][1]


        self.point_17_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['17'])
        self.point_17_player4_new_rect.x += self.surface_point_player_json['17'][0]
        self.point_17_player4_new_rect.y += self.surface_point_player_json['17'][1]


        self.point_18_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['18'])
        self.point_18_player4_new_rect.x += self.surface_point_player_json['18'][0]
        self.point_18_player4_new_rect.y += self.surface_point_player_json['18'][1]


        self.point_19_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['19'])
        self.point_19_player4_new_rect.x += self.surface_point_player_json['19'][0]
        self.point_19_player4_new_rect.y += self.surface_point_player_json['19'][1]


        self.point_20_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['20'])
        self.point_20_player4_new_rect.x += self.surface_point_player_json['20'][0]
        self.point_20_player4_new_rect.y += self.surface_point_player_json['20'][1]


        self.point_21_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['21'])
        self.point_21_player4_new_rect.x += self.surface_point_player_json['21'][0]
        self.point_21_player4_new_rect.y += self.surface_point_player_json['21'][1]


        self.point_22_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['22'])
        self.point_22_player4_new_rect.x += self.surface_point_player_json['22'][0]
        self.point_22_player4_new_rect.y += self.surface_point_player_json['22'][1]


        self.point_23_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['23'])
        self.point_23_player4_new_rect.x += self.surface_point_player_json['23'][0]
        self.point_23_player4_new_rect.y += self.surface_point_player_json['23'][1]


        self.point_24_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['24'])
        self.point_24_player4_new_rect.x += self.surface_point_player_json['24'][0]
        self.point_24_player4_new_rect.y += self.surface_point_player_json['24'][1]


        self.point_25_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['25'])
        self.point_25_player4_new_rect.x += self.surface_point_player_json['25'][0]
        self.point_25_player4_new_rect.y += self.surface_point_player_json['25'][1]


        self.point_26_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['26'])
        self.point_26_player4_new_rect.x += self.surface_point_player_json['26'][0]
        self.point_26_player4_new_rect.y += self.surface_point_player_json['26'][1]


        self.point_27_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['27'])
        self.point_27_player4_new_rect.x += self.surface_point_player_json['27'][0]
        self.point_27_player4_new_rect.y += self.surface_point_player_json['27'][1]


        self.point_28_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['28'])
        self.point_28_player4_new_rect.x += self.surface_point_player_json['28'][0]
        self.point_28_player4_new_rect.y += self.surface_point_player_json['28'][1]


        self.point_29_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['29'])
        self.point_29_player4_new_rect.x += self.surface_point_player_json['29'][0]
        self.point_29_player4_new_rect.y += self.surface_point_player_json['29'][1]


        self.point_30_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['30'])
        self.point_30_player4_new_rect.x += self.surface_point_player_json['30'][0]
        self.point_30_player4_new_rect.y += self.surface_point_player_json['30'][1]


        self.point_31_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['31'])
        self.point_31_player4_new_rect.x += self.surface_point_player_json['31'][0]
        self.point_31_player4_new_rect.y += self.surface_point_player_json['31'][1]


        self.point_32_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['32'])
        self.point_32_player4_new_rect.x += self.surface_point_player_json['32'][0]
        self.point_32_player4_new_rect.y += self.surface_point_player_json['32'][1]


        self.point_33_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['33'])
        self.point_33_player4_new_rect.x += self.surface_point_player_json['33'][0]
        self.point_33_player4_new_rect.y += self.surface_point_player_json['33'][1]


        self.point_34_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['34'])
        self.point_34_player4_new_rect.x += self.surface_point_player_json['34'][0]
        self.point_34_player4_new_rect.y += self.surface_point_player_json['34'][1]


        self.point_35_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['35'])
        self.point_35_player4_new_rect.x += self.surface_point_player_json['35'][0]
        self.point_35_player4_new_rect.y += self.surface_point_player_json['35'][1]


        self.point_36_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['36'])
        self.point_36_player4_new_rect.x += self.surface_point_player_json['36'][0]
        self.point_36_player4_new_rect.y += self.surface_point_player_json['36'][1]


        self.point_37_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['37'])
        self.point_37_player4_new_rect.x += self.surface_point_player_json['37'][0]
        self.point_37_player4_new_rect.y += self.surface_point_player_json['37'][1]


        self.point_38_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['38'])
        self.point_38_player4_new_rect.x += self.surface_point_player_json['38'][0]
        self.point_38_player4_new_rect.y += self.surface_point_player_json['38'][1]


        self.point_39_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['39'])
        self.point_39_player4_new_rect.x += self.surface_point_player_json['39'][0]
        self.point_39_player4_new_rect.y += self.surface_point_player_json['39'][1]


        self.point_40_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['40'])
        self.point_40_player4_new_rect.x += self.surface_point_player_json['40'][0]
        self.point_40_player4_new_rect.y += self.surface_point_player_json['40'][1]


        self.point_41_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['41'])
        self.point_41_player4_new_rect.x += self.surface_point_player_json['41'][0]
        self.point_41_player4_new_rect.y += self.surface_point_player_json['41'][1]


        self.point_42_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['42'])
        self.point_42_player4_new_rect.x += self.surface_point_player_json['42'][0]
        self.point_42_player4_new_rect.y += self.surface_point_player_json['42'][1]


        self.point_43_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['43'])
        self.point_43_player4_new_rect.x += self.surface_point_player_json['43'][0]
        self.point_43_player4_new_rect.y += self.surface_point_player_json['43'][1]


        self.point_44_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['44'])
        self.point_44_player4_new_rect.x += self.surface_point_player_json['44'][0]
        self.point_44_player4_new_rect.y += self.surface_point_player_json['44'][1]


        self.point_45_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['45'])
        self.point_45_player4_new_rect.x += self.surface_point_player_json['45'][0]
        self.point_45_player4_new_rect.y += self.surface_point_player_json['45'][1]


        self.point_46_player4_new_rect = self.point_player4_new.get_rect()
        self.screen.blit(self.point_player4_new, self.surface_point_player_json['46'])
        self.point_46_player4_new_rect.x += self.surface_point_player_json['46'][0]
        self.point_46_player4_new_rect.y += self.surface_point_player_json['46'][1]



        self.point = pygame.image.load('images/point_end.png')
        self.point_2 = Image.open('images/point_end.png')
        self.point_width, self.point_height = self.point_2.size
        self.point_new = self.point.convert_alpha()
        self.point_new.set_alpha(0)
        self.point_new = pygame.transform.scale(surface=self.point_new, size=(self.point_width * self.settings.RATIO_ALL, self.point_height * self.settings.RATIO_ALL))



        self.point_1_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['1'])
        self.point_1_new_rect.x += self.surface_point_json['1'][0]
        self.point_1_new_rect.y += self.surface_point_json['1'][1]
        self.point_2_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['2'])
        self.point_2_new_rect.x += self.surface_point_json['2'][0]
        self.point_2_new_rect.y += self.surface_point_json['2'][1]
        self.point_3_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['3'])
        self.point_3_new_rect.x += self.surface_point_json['3'][0]
        self.point_3_new_rect.y += self.surface_point_json['3'][1]
        self.point_4_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['4'])
        self.point_4_new_rect.x += self.surface_point_json['4'][0]
        self.point_4_new_rect.y += self.surface_point_json['4'][1]
        self.point_5_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['5'])
        self.point_5_new_rect.x += self.surface_point_json['5'][0]
        self.point_5_new_rect.y += self.surface_point_json['5'][1]
        self.point_6_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['6'])
        self.point_6_new_rect.x += self.surface_point_json['6'][0]
        self.point_6_new_rect.y += self.surface_point_json['6'][1]
        self.point_7_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['7'])
        self.point_7_new_rect.x += self.surface_point_json['7'][0]
        self.point_7_new_rect.y += self.surface_point_json['7'][1]
        self.point_8_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['8'])
        self.point_8_new_rect.x += self.surface_point_json['8'][0]
        self.point_8_new_rect.y += self.surface_point_json['8'][1]
        self.point_9_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['9'])
        self.point_9_new_rect.x += self.surface_point_json['9'][0]
        self.point_9_new_rect.y += self.surface_point_json['9'][1]
        self.point_10_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['10'])
        self.point_10_new_rect.x += self.surface_point_json['10'][0]
        self.point_10_new_rect.y += self.surface_point_json['10'][1]
        self.point_11_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['11'])
        self.point_11_new_rect.x += self.surface_point_json['11'][0]
        self.point_11_new_rect.y += self.surface_point_json['11'][1]
        self.point_12_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['12'])
        self.point_12_new_rect.x += self.surface_point_json['12'][0]
        self.point_12_new_rect.y += self.surface_point_json['12'][1]
        self.point_13_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['13'])
        self.point_13_new_rect.x += self.surface_point_json['13'][0]
        self.point_13_new_rect.y += self.surface_point_json['13'][1]
        self.point_14_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['14'])
        self.point_14_new_rect.x += self.surface_point_json['14'][0]
        self.point_14_new_rect.y += self.surface_point_json['14'][1]
        self.point_15_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['15'])
        self.point_15_new_rect.x += self.surface_point_json['15'][0]
        self.point_15_new_rect.y += self.surface_point_json['15'][1]
        self.point_16_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['16'])
        self.point_16_new_rect.x += self.surface_point_json['16'][0]
        self.point_16_new_rect.y += self.surface_point_json['16'][1]
        self.point_17_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['17'])
        self.point_17_new_rect.x += self.surface_point_json['17'][0]
        self.point_17_new_rect.y += self.surface_point_json['17'][1]
        self.point_18_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['18'])
        self.point_18_new_rect.x += self.surface_point_json['18'][0]
        self.point_18_new_rect.y += self.surface_point_json['18'][1]
        self.point_19_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['19'])
        self.point_19_new_rect.x += self.surface_point_json['19'][0]
        self.point_19_new_rect.y += self.surface_point_json['19'][1]
        self.point_20_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['20'])
        self.point_20_new_rect.x += self.surface_point_json['20'][0]
        self.point_20_new_rect.y += self.surface_point_json['20'][1]
        self.point_21_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['21'])
        self.point_21_new_rect.x += self.surface_point_json['21'][0]
        self.point_21_new_rect.y += self.surface_point_json['21'][1]
        self.point_22_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['22'])
        self.point_22_new_rect.x += self.surface_point_json['22'][0]
        self.point_22_new_rect.y += self.surface_point_json['22'][1]
        self.point_23_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['23'])
        self.point_23_new_rect.x += self.surface_point_json['23'][0]
        self.point_23_new_rect.y += self.surface_point_json['23'][1]
        self.point_24_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['24'])
        self.point_24_new_rect.x += self.surface_point_json['24'][0]
        self.point_24_new_rect.y += self.surface_point_json['24'][1]
        self.point_25_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['25'])
        self.point_25_new_rect.x += self.surface_point_json['25'][0]
        self.point_25_new_rect.y += self.surface_point_json['25'][1]
        self.point_26_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['26'])
        self.point_26_new_rect.x += self.surface_point_json['26'][0]
        self.point_26_new_rect.y += self.surface_point_json['26'][1]
        self.point_27_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['27'])
        self.point_27_new_rect.x += self.surface_point_json['27'][0]
        self.point_27_new_rect.y += self.surface_point_json['27'][1]
        self.point_28_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['28'])
        self.point_28_new_rect.x += self.surface_point_json['28'][0]
        self.point_28_new_rect.y += self.surface_point_json['28'][1]
        self.point_29_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['29'])
        self.point_29_new_rect.x += self.surface_point_json['29'][0]
        self.point_29_new_rect.y += self.surface_point_json['29'][1]
        self.point_30_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['30'])
        self.point_30_new_rect.x += self.surface_point_json['30'][0]
        self.point_30_new_rect.y += self.surface_point_json['30'][1]
        self.point_31_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['31'])
        self.point_31_new_rect.x += self.surface_point_json['31'][0]
        self.point_31_new_rect.y += self.surface_point_json['31'][1]
        self.point_32_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['32'])
        self.point_32_new_rect.x += self.surface_point_json['32'][0]
        self.point_32_new_rect.y += self.surface_point_json['32'][1]
        self.point_33_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['33'])
        self.point_33_new_rect.x += self.surface_point_json['33'][0]
        self.point_33_new_rect.y += self.surface_point_json['33'][1]
        self.point_34_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['34'])
        self.point_34_new_rect.x += self.surface_point_json['34'][0]
        self.point_34_new_rect.y += self.surface_point_json['34'][1]
        self.point_35_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['35'])
        self.point_35_new_rect.x += self.surface_point_json['35'][0]
        self.point_35_new_rect.y += self.surface_point_json['35'][1]
        self.point_36_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['36'])
        self.point_36_new_rect.x += self.surface_point_json['36'][0]
        self.point_36_new_rect.y += self.surface_point_json['36'][1]
        self.point_37_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['37'])
        self.point_37_new_rect.x += self.surface_point_json['37'][0]
        self.point_37_new_rect.y += self.surface_point_json['37'][1]
        self.point_38_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['38'])
        self.point_38_new_rect.x += self.surface_point_json['38'][0]
        self.point_38_new_rect.y += self.surface_point_json['38'][1]
        self.point_39_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['39'])
        self.point_39_new_rect.x += self.surface_point_json['39'][0]
        self.point_39_new_rect.y += self.surface_point_json['39'][1]
        self.point_40_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['40'])
        self.point_40_new_rect.x += self.surface_point_json['40'][0]
        self.point_40_new_rect.y += self.surface_point_json['40'][1]
        self.point_41_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['41'])
        self.point_41_new_rect.x += self.surface_point_json['41'][0]
        self.point_41_new_rect.y += self.surface_point_json['41'][1]
        self.point_42_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['42'])
        self.point_42_new_rect.x += self.surface_point_json['42'][0]
        self.point_42_new_rect.y += self.surface_point_json['42'][1]
        self.point_43_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['43'])
        self.point_43_new_rect.x += self.surface_point_json['43'][0]
        self.point_43_new_rect.y += self.surface_point_json['43'][1]
        self.point_44_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['44'])
        self.point_44_new_rect.x += self.surface_point_json['44'][0]
        self.point_44_new_rect.y += self.surface_point_json['44'][1]
        self.point_45_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['45'])
        self.point_45_new_rect.x += self.surface_point_json['45'][0]
        self.point_45_new_rect.y += self.surface_point_json['45'][1]
        self.point_46_new_rect = self.point_new.get_rect()
        self.screen.blit(self.point_new, self.surface_point_json['46'])
        self.point_46_new_rect.x += self.surface_point_json['46'][0]
        self.point_46_new_rect.y += self.surface_point_json['46'][1]





        # #point_hide
        # self.point_hide = pygame.image.load('images/point_hide.png')
        # self.point_hide_2 = Image.open('images/point_hide.png')
        # self.point_hide_width, self.point_hide_height = self.point_hide_2.size
        # self.point_hide_new = pygame.transform.scale(surface=self.point_hide, size=(self.point_hide_width * self.settings.RATIO_ALL, self.point_hide_height * self.settings.RATIO_ALL))
        # self.point_hide_new_rect = self.point_hide_new.get_rect()
        # self.screen.blit(self.point_hide_new, self.surface_json['point']['point_hide'])
        # self.point_hide_new_rect.x += self.surface_json['point']['point_hide'][0]
        # self.point_hide_new_rect.y += self.surface_json['point']['point_hide'][1]



        # #point_player1
        # self.point_player1 = pygame.image.load('images/point_player1.png')
        # self.point_player1_2 = Image.open('images/point_player1.png')
        # self.point_player1_width, self.point_player1_height = self.point_player1_2.size
        # self.point_player1_new = pygame.transform.scale(surface=self.point_player1, size=(self.point_player1_width * self.settings.RATIO_ALL, self.point_player1_height * self.settings.RATIO_ALL))
        # self.point_player1_new_rect = self.point_player1_new.get_rect()
        # self.screen.blit(self.point_player1_new, self.surface_json['point']['point_player1'])
        # self.point_player1_new_rect.x += self.surface_json['point']['point_player1'][0]
        # self.point_player1_new_rect.y += self.surface_json['point']['point_player1'][1]



        # #point_player2
        # self.point_player2 = pygame.image.load('images/point_player2.png')
        # self.point_player2_2 = Image.open('images/point_player2.png')
        # self.point_player2_width, self.point_player2_height = self.point_player2_2.size
        # self.point_player2_new = pygame.transform.scale(surface=self.point_player2, size=(self.point_player2_width * self.settings.RATIO_ALL, self.point_player2_height * self.settings.RATIO_ALL))
        # self.point_player2_new_rect = self.point_player2_new.get_rect()
        # self.screen.blit(self.point_player2_new, self.surface_json['point']['point_player2'])
        # self.point_player2_new_rect.x += self.surface_json['point']['point_player2'][0]
        # self.point_player2_new_rect.y += self.surface_json['point']['point_player2'][1]



        # #point_player3
        # self.point_player3 = pygame.image.load('images/point_player3.png')
        # self.point_player3_2 = Image.open('images/point_player3.png')
        # self.point_player3_width, self.point_player3_height = self.point_player3_2.size
        # self.point_player3_new = pygame.transform.scale(surface=self.point_player3, size=(self.point_player3_width * self.settings.RATIO_ALL, self.point_player3_height * self.settings.RATIO_ALL))
        # self.point_player3_new_rect = self.point_player3_new.get_rect()
        # self.screen.blit(self.point_player3_new, self.surface_json['point']['point_player3'])
        # self.point_player3_new_rect.x += self.surface_json['point']['point_player3'][0]
        # self.point_player3_new_rect.y += self.surface_json['point']['point_player3'][1]



        # #point_player4
        # self.point_player4 = pygame.image.load('images/point_player4.png')
        # self.point_player4_2 = Image.open('images/point_player4.png')
        # self.point_player4_width, self.point_player4_height = self.point_player4_2.size
        # self.point_player4_new = pygame.transform.scale(surface=self.point_player4, size=(self.point_player4_width * self.settings.RATIO_ALL, self.point_player4_height * self.settings.RATIO_ALL))
        # self.point_player4_new_rect = self.point_player4_new.get_rect()
        # self.screen.blit(self.point_player4_new, self.surface_json['point']['point_player4'])
        # self.point_player4_new_rect.x += self.surface_json['point']['point_player4'][0]
        # self.point_player4_new_rect.y += self.surface_json['point']['point_player4'][1]



        # #point_war
        # self.point_war = pygame.image.load('images/point_war.png')
        # self.point_war_2 = Image.open('images/point_war.png')
        # self.point_war_width, self.point_war_height = self.point_war_2.size
        # self.point_war_new = pygame.transform.scale(surface=self.point_war, size=(self.point_war_width * self.settings.RATIO_ALL, self.point_war_height * self.settings.RATIO_ALL))
        # self.point_war_new_rect = self.point_war_new.get_rect()
        # self.screen.blit(self.point_war_new, self.surface_json['point']['point_war'])
        # self.point_war_new_rect.x += self.surface_json['point']['point_war'][0]
        # self.point_war_new_rect.y += self.surface_json['point']['point_war'][1]



        #ticket_railway
        self.ticket_railway = pygame.image.load('images/ticket_railway.png')
        self.ticket_railway_2 = Image.open('images/ticket_railway.png')
        self.ticket_railway_width, self.ticket_railway_height = self.ticket_railway_2.size
        self.ticket_railway_new = pygame.transform.scale(surface=self.ticket_railway, size=(self.ticket_railway_width * self.settings.RATIO_ALL, self.ticket_railway_height * self.settings.RATIO_ALL))
        self.ticket_railway_new_rect = self.ticket_railway_new.get_rect()
        self.screen.blit(self.ticket_railway_new, self.surface_json['ticket']['ticket_railway'])
        self.ticket_railway_new_rect.x += self.surface_json['ticket']['ticket_railway'][0]
        self.ticket_railway_new_rect.y += self.surface_json['ticket']['ticket_railway'][1]



        #ticket_road
        self.ticket_road = pygame.image.load('images/ticket_road.png')
        self.ticket_road_2 = Image.open('images/ticket_road.png')
        self.ticket_road_width, self.ticket_road_height = self.ticket_road_2.size
        self.ticket_road_new = pygame.transform.scale(surface=self.ticket_road, size=(self.ticket_road_width * self.settings.RATIO_ALL, self.ticket_road_height * self.settings.RATIO_ALL))
        self.ticket_road_new_rect = self.ticket_road_new.get_rect()
        self.screen.blit(self.ticket_road_new, self.surface_json['ticket']['ticket_road'])
        self.ticket_road_new_rect.x += self.surface_json['ticket']['ticket_road'][0]
        self.ticket_road_new_rect.y += self.surface_json['ticket']['ticket_road'][1]



        #ticket_ship
        self.ticket_ship = pygame.image.load('images/ticket_ship.png')
        self.ticket_ship_2 = Image.open('images/ticket_ship.png')
        self.ticket_ship_width, self.ticket_ship_height = self.ticket_ship_2.size
        self.ticket_ship_new = pygame.transform.scale(surface=self.ticket_ship, size=(self.ticket_ship_width * self.settings.RATIO_ALL, self.ticket_ship_height * self.settings.RATIO_ALL))
        self.ticket_ship_new_rect = self.ticket_ship_new.get_rect()
        self.screen.blit(self.ticket_ship_new, self.surface_json['ticket']['ticket_ship'])
        self.ticket_ship_new_rect.x += self.surface_json['ticket']['ticket_ship'][0]
        self.ticket_ship_new_rect.y += self.surface_json['ticket']['ticket_ship'][1]



        #window_cover
        self.window_cover = pygame.image.load('images/window_cover.png')
        self.window_cover_2 = Image.open('images/window_cover.png')
        self.window_cover_width, self.window_cover_height = self.window_cover_2.size
        self.window_cover_new = pygame.transform.scale(surface=self.window_cover, size=(self.window_cover_width * self.settings.RATIO_ALL, self.window_cover_height * self.settings.RATIO_ALL))
        self.window_cover_new_rect = self.window_cover_new.get_rect()
        self.screen.blit(self.window_cover_new, self.surface_json['window']['window_cover'])
        self.window_cover_new_rect.x += self.surface_json['window']['window_cover'][0]
        self.window_cover_new_rect.y += self.surface_json['window']['window_cover'][1]


        self.window_blank = pygame.image.load('images/window_blank.png')
        self.window_blank_2 = Image.open('images/window_blank.png')
        self.window_blank_width, self.window_blank_height = self.window_blank_2.size
        self.window_blank_new = pygame.transform.scale(surface=self.window_blank, size=(self.window_blank_width * self.settings.RATIO_ALL, self.window_blank_height * self.settings.RATIO_ALL))
        self.window_blank_new_rect = self.window_blank_new.get_rect()
        self.screen.blit(self.window_blank_new, self.surface_json['window']['window_blank'])
        self.window_blank_new_rect.x += self.surface_json['window']['window_blank'][0]
        self.window_blank_new_rect.y += self.surface_json['window']['window_blank'][1]



        #window_ending
        self.window_ending = pygame.image.load('images/window_ending.png')
        self.window_ending_2 = Image.open('images/window_ending.png')
        self.window_ending_width, self.window_ending_height = self.window_ending_2.size
        self.window_ending_new = pygame.transform.scale(surface=self.window_ending, size=(self.window_ending_width * self.settings.RATIO_ALL, self.window_ending_height * self.settings.RATIO_ALL))
        self.window_ending_new_rect = self.window_ending_new.get_rect()
        self.screen.blit(self.window_ending_new, self.surface_json['window']['window_ending'])
        self.window_ending_new_rect.x += self.surface_json['window']['window_ending'][0]
        self.window_ending_new_rect.y += self.surface_json['window']['window_ending'][1]



        #window_input
        self.window_input = pygame.image.load('images/window_input.png')
        self.window_input_2 = Image.open('images/window_input.png')
        self.window_input_width, self.window_input_height = self.window_input_2.size
        self.window_input_new = pygame.transform.scale(surface=self.window_input, size=(self.window_input_width * self.settings.RATIO_ALL, self.window_input_height * self.settings.RATIO_ALL))
        self.window_input_new_rect = self.window_input_new.get_rect()
        self.screen.blit(self.window_input_new, self.surface_json['window']['window_input'])
        self.window_input_new_rect.x += self.surface_json['window']['window_input'][0]
        self.window_input_new_rect.y += self.surface_json['window']['window_input'][1]



        #window_main
        self.window_main = pygame.image.load('images/window_main.png')
        self.window_main_2 = Image.open('images/window_main.png')
        self.window_main_width, self.window_main_height = self.window_main_2.size
        self.window_main_new = pygame.transform.scale(surface=self.window_main, size=(self.window_main_width * self.settings.RATIO_ALL, self.window_main_height * self.settings.RATIO_ALL))
        self.window_main_new_rect = self.window_main_new.get_rect()
        self.screen.blit(self.window_main_new, self.surface_json['window']['window_main'])
        self.window_main_new_rect.x += self.surface_json['window']['window_main'][0]
        self.window_main_new_rect.y += self.surface_json['window']['window_main'][1]



        #window_main_map
        self.window_main_map = pygame.image.load('images/window_main_map.png')
        self.window_main_map_2 = Image.open('images/window_main_map.png')
        self.window_main_map_width, self.window_main_map_height = self.window_main_map_2.size
        self.window_main_map_new = pygame.transform.scale(surface=self.window_main_map, size=(self.window_main_map_width * self.settings.RATIO_ALL, self.window_main_map_height * self.settings.RATIO_ALL))
        self.window_main_map_new_rect = self.window_main_map_new.get_rect()
        self.screen.blit(self.window_main_map_new, self.surface_json['window']['window_main_map'])
        self.window_main_map_new_rect.x += self.surface_json['window']['window_main_map'][0]
        self.window_main_map_new_rect.y += self.surface_json['window']['window_main_map'][1]



        #window_matching
        self.window_matching = pygame.image.load('images/window_matching.png')
        self.window_matching_2 = Image.open('images/window_matching.png')
        self.window_matching_width, self.window_matching_height = self.window_matching_2.size
        self.window_matching_new = pygame.transform.scale(surface=self.window_matching, size=(self.window_matching_width * self.settings.RATIO_ALL, self.window_matching_height * self.settings.RATIO_ALL))
        self.window_matching_new_rect = self.window_matching_new.get_rect()
        self.screen.blit(self.window_matching_new, self.surface_json['window']['window_matching'])
        self.window_matching_new_rect.x += self.surface_json['window']['window_matching'][0]
        self.window_matching_new_rect.y += self.surface_json['window']['window_matching'][1]



        #window_shop
        self.window_shop = pygame.image.load('images/window_shop.png')
        self.window_shop_2 = Image.open('images/window_shop.png')
        self.window_shop_width, self.window_shop_height = self.window_shop_2.size
        self.window_shop_new = pygame.transform.scale(surface=self.window_shop, size=(self.window_shop_width * self.settings.RATIO_ALL, self.window_shop_height * self.settings.RATIO_ALL))
        self.window_shop_new_rect = self.window_shop_new.get_rect()
        self.screen.blit(self.window_shop_new, self.surface_json['window']['window_shop'])
        self.window_shop_new_rect.x += self.surface_json['window']['window_shop'][0]
        self.window_shop_new_rect.y += self.surface_json['window']['window_shop'][1]

        #window_rules
        self.window_rules = pygame.image.load('images/window_rules.png')
        self.window_rules_2 = Image.open('images/window_rules.png')
        self.window_rules_width, self.window_rules_height = self.window_rules_2.size
        self.window_rules_new = pygame.transform.scale(surface=self.window_rules, size=(self.window_rules_width * self.settings.RATIO_ALL, self.window_rules_height * self.settings.RATIO_ALL))
        self.window_rules_new_rect = self.window_rules_new.get_rect()
        self.screen.blit(self.window_rules_new,self.surface_json['window']['window_shop'])
        self.window_shop_new_rect.x += self.surface_json['window']['window_shop'][0]
        self.window_shop_new_rect.y += self.surface_json['window']['window_shop'][1]

        #window_rules
        self.window_About_us = pygame.image.load('images/window_About_us.png')
        self.window_About_us_2 = Image.open('images/window_About_us.png')
        self.window_About_us_width, self.window_About_us_height = self.window_About_us_2.size
        self.window_About_us_new = pygame.transform.scale(surface=self.window_About_us, size=(self.window_About_us_width * self.settings.RATIO_ALL, self.window_About_us_height * self.settings.RATIO_ALL))
        self.window_About_us_new_rect = self.window_About_us_new.get_rect()
        self.screen.blit(self.window_About_us_new,self.surface_json['window']['window_shop'])
        self.window_shop_new_rect.x += self.surface_json['window']['window_shop'][0]
        self.window_shop_new_rect.y += self.surface_json['window']['window_shop'][1]




        #words_matching_1
        self.words_matching_1 = pygame.image.load('images/words_matching_1.png')
        self.words_matching_1_2 = Image.open('images/words_matching_1.png')
        self.words_matching_1_width, self.words_matching_1_height = self.words_matching_1_2.size
        self.words_matching_1_new = pygame.transform.scale(surface=self.words_matching_1, size=(self.words_matching_1_width * self.settings.RATIO_ALL, self.words_matching_1_height * self.settings.RATIO_ALL))
        self.words_matching_1_new_rect = self.words_matching_1_new.get_rect()
        self.screen.blit(self.words_matching_1_new, self.surface_json['words']['words_matching_1'])
        self.words_matching_1_new_rect.x += self.surface_json['words']['words_matching_1'][0]
        self.words_matching_1_new_rect.y += self.surface_json['words']['words_matching_1'][1]



        #words_matching_2
        self.words_matching_2 = pygame.image.load('images/words_matching_2.png')
        self.words_matching_2_2 = Image.open('images/words_matching_2.png')
        self.words_matching_2_width, self.words_matching_2_height = self.words_matching_2_2.size
        self.words_matching_2_new = pygame.transform.scale(surface=self.words_matching_2, size=(self.words_matching_2_width * self.settings.RATIO_ALL, self.words_matching_2_height * self.settings.RATIO_ALL))
        self.words_matching_2_new_rect = self.words_matching_2_new.get_rect()
        self.screen.blit(self.words_matching_2_new, self.surface_json['words']['words_matching_2'])
        self.words_matching_2_new_rect.x += self.surface_json['words']['words_matching_2'][0]
        self.words_matching_2_new_rect.y += self.surface_json['words']['words_matching_2'][1]



        #words_matching_3
        self.words_matching_3 = pygame.image.load('images/words_matching_3.png')
        self.words_matching_3_2 = Image.open('images/words_matching_3.png')
        self.words_matching_3_width, self.words_matching_3_height = self.words_matching_3_2.size
        self.words_matching_3_new = pygame.transform.scale(surface=self.words_matching_3, size=(self.words_matching_3_width * self.settings.RATIO_ALL, self.words_matching_3_height * self.settings.RATIO_ALL))
        self.words_matching_3_new_rect = self.words_matching_3_new.get_rect()
        self.screen.blit(self.words_matching_3_new, self.surface_json['words']['words_matching_3'])
        self.words_matching_3_new_rect.x += self.surface_json['words']['words_matching_3'][0]
        self.words_matching_3_new_rect.y += self.surface_json['words']['words_matching_3'][1]



        #words_please_wait_1
        self.words_please_wait_1 = pygame.image.load('images/words_please_wait_1.png')
        self.words_please_wait_1_2 = Image.open('images/words_please_wait_1.png')
        self.words_please_wait_1_width, self.words_please_wait_1_height = self.words_please_wait_1_2.size
        self.words_please_wait_1_new = pygame.transform.scale(surface=self.words_please_wait_1, size=(self.words_please_wait_1_width * self.settings.RATIO_ALL, self.words_please_wait_1_height * self.settings.RATIO_ALL))
        self.words_please_wait_1_new_rect = self.words_please_wait_1_new.get_rect()
        self.screen.blit(self.words_please_wait_1_new, self.surface_json['words']['words_please_wait_1'])
        self.words_please_wait_1_new_rect.x += self.surface_json['words']['words_please_wait_1'][0]
        self.words_please_wait_1_new_rect.y += self.surface_json['words']['words_please_wait_1'][1]



        #words_please_wait_2
        self.words_please_wait_2 = pygame.image.load('images/words_please_wait_2.png')
        self.words_please_wait_2_2 = Image.open('images/words_please_wait_2.png')
        self.words_please_wait_2_width, self.words_please_wait_2_height = self.words_please_wait_2_2.size
        self.words_please_wait_2_new = pygame.transform.scale(surface=self.words_please_wait_2, size=(self.words_please_wait_2_width * self.settings.RATIO_ALL, self.words_please_wait_2_height * self.settings.RATIO_ALL))
        self.words_please_wait_2_new_rect = self.words_please_wait_2_new.get_rect()
        self.screen.blit(self.words_please_wait_2_new, self.surface_json['words']['words_please_wait_2'])
        self.words_please_wait_2_new_rect.x += self.surface_json['words']['words_please_wait_2'][0]
        self.words_please_wait_2_new_rect.y += self.surface_json['words']['words_please_wait_2'][1]



        #words_please_wait_3
        self.words_please_wait_3 = pygame.image.load('images/words_please_wait_3.png')
        self.words_please_wait_3_2 = Image.open('images/words_please_wait_3.png')
        self.words_please_wait_3_width, self.words_please_wait_3_height = self.words_please_wait_3_2.size
        self.words_please_wait_3_new = pygame.transform.scale(surface=self.words_please_wait_3, size=(self.words_please_wait_3_width * self.settings.RATIO_ALL, self.words_please_wait_3_height * self.settings.RATIO_ALL))
        self.words_please_wait_3_new_rect = self.words_please_wait_3_new.get_rect()
        self.screen.blit(self.words_please_wait_3_new, self.surface_json['words']['words_please_wait_3'])
        self.words_please_wait_3_new_rect.x += self.surface_json['words']['words_please_wait_3'][0]
        self.words_please_wait_3_new_rect.y += self.surface_json['words']['words_please_wait_3'][1]


        self.words_1 = pygame.image.load('images/words_1.png')
        self.words_1_2 = Image.open('images/words_1.png')
        self.words_1_width, self.words_1_height = self.words_1_2.size
        self.words_1_new = self.words_1.convert_alpha()
        self.words_1_new.set_alpha(0)
        self.words_1_new = pygame.transform.scale(surface=self.words_1, size=(self.words_1_width * self.settings.RATIO_ALL, self.words_1_height * self.settings.RATIO_ALL))


        self.screen.blit(self.words_1_new, self.surface_json['words']['words_1'])
        self.words_1_new.set_alpha(0)
        self.words_1_new = pygame.transform.scale(surface=self.words_1, size=(self.words_1_width * self.settings.RATIO_ALL, self.words_1_height * self.settings.RATIO_ALL))


        self.words_2 = pygame.image.load('images/words_2.png')
        self.words_2_2 = Image.open('images/words_2.png')
        self.words_2_width, self.words_2_height = self.words_2_2.size
        self.words_2_new = self.words_2.convert_alpha()
        self.words_2_new.set_alpha(0)
        self.words_2_new = pygame.transform.scale(surface=self.words_2, size=(self.words_2_width * self.settings.RATIO_ALL, self.words_2_height * self.settings.RATIO_ALL))


        self.screen.blit(self.words_2_new, self.surface_json['words']['words_2'])
        self.words_2_new.set_alpha(0)
        self.words_2_new = pygame.transform.scale(surface=self.words_2, size=(self.words_2_width * self.settings.RATIO_ALL, self.words_2_height * self.settings.RATIO_ALL))


        self.words_3 = pygame.image.load('images/words_3.png')
        self.words_3_2 = Image.open('images/words_3.png')
        self.words_3_width, self.words_3_height = self.words_3_2.size
        self.words_3_new = self.words_3.convert_alpha()
        self.words_3_new.set_alpha(0)
        self.words_3_new = pygame.transform.scale(surface=self.words_3, size=(self.words_3_width * self.settings.RATIO_ALL, self.words_3_height * self.settings.RATIO_ALL))


        self.screen.blit(self.words_3_new, self.surface_json['words']['words_3'])
        self.words_3_new.set_alpha(0)
        self.words_3_new = pygame.transform.scale(surface=self.words_3, size=(self.words_3_width * self.settings.RATIO_ALL, self.words_3_height * self.settings.RATIO_ALL))




    def _blit_events(self):
            if self.game_active_1:
                """封面"""      
                self.screen.blit(self.window_cover_new, self.surface_json['window']['window_cover'])

                if(self.x >= 20 ):
                    self.screen.blit(self.words_please_wait_1_new,self.surface_json['words']['words_please_wait_1'])
                if(self.x >= 40 and self.x < 60):
                    self.screen.blit(self.words_please_wait_2_new, self.surface_json['words']['words_please_wait_2'])
                if(self.x >= 60 and self.x < 80):    
                    self.screen.blit(self.words_please_wait_3_new, self.surface_json['words']['words_please_wait_3'])
                if(self.x >= 80 and self.x <100):
                    self.screen.blit(self.words_please_wait_1_new,self.surface_json['words']['words_please_wait_1'])
                if(self.x >= 100 and self.x < 120):
                    self.screen.blit(self.words_please_wait_2_new, self.surface_json['words']['words_please_wait_2'])
                if(self.x >= 120 and self.x < 140):    
                    self.screen.blit(self.words_please_wait_3_new, self.surface_json['words']['words_please_wait_3'])
                if(self.x >= 140 and self.x <160):
                    self.screen.blit(self.words_please_wait_1_new,self.surface_json['words']['words_please_wait_1'])
                if(self.x >= 160 and self.x < 180):
                    self.screen.blit(self.words_please_wait_2_new, self.surface_json['words']['words_please_wait_2'])
                if(self.x >= 180):    
                    self.screen.blit(self.words_please_wait_3_new, self.surface_json['words']['words_please_wait_3'])
                if(self.x >= 220):
                    self.game_active_1 = False
                    self.game_active_1_1 = True
                # #print(self.x)
                self.mouse_click_pos = (-1,-1)

            if self.game_active_1_1:
                self.screen.blit(self.window_blank_new, self.surface_json['window']['window_blank'])

                self.screen.blit(self.words_1_new, self.surface_json['words']['words_1'])
                self.words_1_new.set_alpha((self.x-220)*3)
                #self.words_1_new = pygame.transform.scale(surface=self.words_1, size=(self.words_1_width * self.settings.RATIO_ALL, self.words_1_height * self.settings.RATIO_ALL))


                if(self.x >= 720):
                    self.game_active_1_1 = False
                    self.game_active_1_2 = True
                self.mouse_click_pos = (-1,-1)
                

            if self.game_active_1_2:
                self.screen.blit(self.window_blank_new, self.surface_json['window']['window_blank'])

                self.screen.blit(self.words_2_new, self.surface_json['words']['words_2'])
                self.words_2_new.set_alpha((self.x-720)*3)

                if(self.x >= 1420):
                    self.game_active_1_2 = False
                    self.game_active_1_3 = True
                self.mouse_click_pos = (-1,-1)


            if self.game_active_1_3:
                self.screen.blit(self.window_blank_new, self.surface_json['window']['window_blank'])

                self.screen.blit(self.words_3_new, self.surface_json['words']['words_3'])
                self.words_3_new.set_alpha((self.x-1420)*3)

                if(self.x >= 2120):
                    self.game_active_1_3 = False
                    self.mouse_click_pos = (-1,-1)
                    self.game_active_2 = True
                self.mouse_click_pos = (-1,-1)



            if self.game_active_2:
                """进入界面"""
                self.mouse_click_pos = (-1,-1)
                self.screen.blit(self.window_main_new, self.surface_json['window']['window_main'])

                if self.highlight_active_1 == False:
                    self.screen.blit(self.button_Multi_player_static_new, self.surface_json['button']['button_Multi_player_static'])
                if self.highlight_active_2 == False:
                    self.screen.blit(self.button_Rules_static_new, self.surface_json['button']['button_Rules_static'])
                if self.highlight_active_3 == False:
                    self.screen.blit(self.button_About_us_static_new, self.surface_json['button']['button_About_us_static'])


                if self.game_active_audio == True:
                    self.screen.blit(self.button_open_audio_static_new, self.surface_json['button']['button_open_audio_static'])

                else:   
                    self.screen.blit(self.button_close_audio_static_new, self.surface_json['button']['button_close_audio_static'])

            if self.game_active_3:
                """房间选择（建立or加入）界面"""
                self.screen.blit(self.window_main_new, self.surface_json['window']['window_main'])


                self.screen.blit(self.button_out_static_new, self.surface_json['button']['button_out_static'])

                if self.game_active_audio == True:
                    self.screen.blit(self.button_open_audio_static_new, self.surface_json['button']['button_open_audio_static'])
                else:   
                    self.screen.blit(self.button_close_audio_static_new, self.surface_json['button']['button_close_audio_static'])


                self.screen.blit(self.button_join_in_a_room_static_new, self.surface_json['button']['button_join_in_a_room_static'])
                self.screen.blit(self.button_create_a_room_static_new, self.surface_json['button']['button_create_a_room_static'])
                
            if self.game_active_4:
                """房间拥有者界面"""
                self.screen.blit(self.window_matching_new, self.surface_json['window']['window_matching'])

                self.screen.blit(self.words_matching_1_new, self.surface_json['words']['words_matching_1'])
                # self.screen.blit(self.words_matching_2_new, self.surface_json['words']['words_matching_2'])
                # self.screen.blit(self.words_matching_3_new, self.surface_json['words']['words_matching_3'])


                self.screen.blit(self.button_out_static_new, self.surface_json['button']['button_out_static'])

                if self.game_active_audio == True:
                    self.screen.blit(self.button_open_audio_static_new, self.surface_json['button']['button_open_audio_static'])
                else:   
                    self.screen.blit(self.button_close_audio_static_new, self.surface_json['button']['button_close_audio_static'])


                # 以下为玩家图像表示（人像），需要根据玩家连入局域网顺序以及玩家身份（others 还是 you)来生成

                
                self.screen.blit(self.figure_player1_you_new, self.surface_json['figure']['figure_player1_you'])
                # 
                if self.total_info["round&client_number&time"][1] == 2 :
                    self.screen.blit(self.figure_player2_others_new, self.surface_json['figure']['figure_player2_others'])
                elif self.total_info["round&client_number&time"][1] == 3 :
                    self.screen.blit(self.figure_player3_others_new, self.surface_json['figure']['figure_player3_others'])
                    self.screen.blit(self.figure_player2_others_new, self.surface_json['figure']['figure_player2_others'])
                elif self.total_info["round&client_number&time"][1] == 4 :
                    self.screen.blit(self.figure_player3_others_new, self.surface_json['figure']['figure_player3_others'])
                    self.screen.blit(self.figure_player2_others_new, self.surface_json['figure']['figure_player2_others'])
                    self.screen.blit(self.figure_player4_others_new, self.surface_json['figure']['figure_player4_others'])
                
                
                # self.screen.blit(self.figure_player2_you_new, self.surface_json['figure']['figure_player2_you'])
                
                # self.screen.blit(self.figure_player3_you_new, self.surface_json['figure']['figure_player3_you'])
                # self.screen.blit(self.figure_player4_others_new, self.surface_json['figure']['figure_player4_others'])
                # self.screen.blit(self.figure_player4_you_new, self.surface_json['figure']['figure_player4_you'])
                # pass

            if self.game_active_5:
                """房间加入者界面"""
                self.screen.blit(self.window_matching_new, self.surface_json['window']['window_matching'])

                self.screen.blit(self.words_matching_1_new, self.surface_json['words']['words_matching_1'])
                # self.screen.blit(self.words_matching_2_new, self.surface_json['words']['words_matching_2'])
                # self.screen.blit(self.words_matching_3_new, self.surface_json['words']['words_matching_3'])

                self.screen.blit(self.button_enter_your_room_address_static_new, self.surface_json['button']['button_enter_your_room_address_static'])


                self.screen.blit(self.button_out_static_new, self.surface_json['button']['button_out_static'])

                if self.game_active_audio == True:
                    self.screen.blit(self.button_open_audio_static_new, self.surface_json['button']['button_open_audio_static'])
                else:   
                    self.screen.blit(self.button_close_audio_static_new, self.surface_json['button']['button_close_audio_static'])
                
                self.screen.blit(self.figure_player1_others_new, self.surface_json['figure']['figure_player1_others'])
                
                if(self.i_am == 2 and self.total_info["round&client_number&time"][1] == 2):
                    self.screen.blit(self.figure_player2_you_new, self.surface_json['figure']['figure_player2_you'])
                if(self.i_am == 2 and self.total_info["round&client_number&time"][1] == 3):
                    self.screen.blit(self.figure_player2_you_new, self.surface_json['figure']['figure_player2_you'])
                    self.screen.blit(self.figure_player3_others_new, self.surface_json['figure']['figure_player3_others'])
                if(self.i_am == 2 and self.total_info["round&client_number&time"][1] == 4):
                    self.screen.blit(self.figure_player2_you_new, self.surface_json['figure']['figure_player2_you'])
                    self.screen.blit(self.figure_player3_others_new, self.surface_json['figure']['figure_player3_others'])
                    self.screen.blit(self.figure_player4_others_new, self.surface_json['figure']['figure_player4_others'])
                if(self.i_am == 3 and self.total_info["round&client_number&time"][1] == 3):
                    self.screen.blit(self.figure_player2_others_new, self.surface_json['figure']['figure_player2_others'])
                    self.screen.blit(self.figure_player3_you_new, self.surface_json['figure']['figure_player3_you'])
                if(self.i_am == 3 and self.total_info["round&client_number&time"][1] == 4):
                    self.screen.blit(self.figure_player2_others_new, self.surface_json['figure']['figure_player2_others'])
                    self.screen.blit(self.figure_player3_you_new, self.surface_json['figure']['figure_player3_you'])
                    self.screen.blit(self.figure_player4_others_new, self.surface_json['figure']['figure_player4_others'])
                if(self.i_am == 4 and self.total_info["round&client_number&time"][1] == 4):
                    self.screen.blit(self.figure_player2_others_new, self.surface_json['figure']['figure_player2_others'])
                    self.screen.blit(self.figure_player3_others_new, self.surface_json['figure']['figure_player3_others'])
                    self.screen.blit(self.figure_player4_you_new, self.surface_json['figure']['figure_player4_you'])
                '''

                以下为玩家图像表示（人像），需要根据玩家连入局域网顺序以及玩家身份（others 还是 you)来生成

                self.screen.blit(self.figure_player1_others_new, self.surface_json['figure']['figure_player1_others'])
                self.screen.blit(self.figure_player1_you_new, self.surface_json['figure']['figure_player1_you'])
                self.screen.blit(self.figure_player2_others_new, self.surface_json['figure']['figure_player2_others'])
                self.screen.blit(self.figure_player2_you_new, self.surface_json['figure']['figure_player2_you'])
                self.screen.blit(self.figure_player3_others_new, self.surface_json['figure']['figure_player3_others'])
                self.screen.blit(self.figure_player3_you_new, self.surface_json['figure']['figure_player3_you'])
                self.screen.blit(self.figure_player4_others_new, self.surface_json['figure']['figure_player4_others'])
                self.screen.blit(self.figure_player4_you_new, self.surface_json['figure']['figure_player4_you'])
                pass
 
                '''

                # pass

            if self.game_active_6:
                """大战界面"""
                self.screen.blit(self.window_main_map_new, self.surface_json['window']['window_main_map'])


                self.screen.blit(self.button_shop_shallow_new, self.surface_json['button']['button_shop_shallow'])


                self.screen.blit(self.button_war_shallow_new, self.surface_json['button']['button_war_shallow'])
                self.screen.blit(self.button_trap_shallow_new, self.surface_json['button']['button_trap_shallow'])
                self.screen.blit(self.button_skip_shallow_new, self.surface_json['button']['button_skip_shallow'])
                self.screen.blit(self.button_hide_shallow_new, self.surface_json['button']['button_hide_shallow'])

                self.screen.blit(self.button_ship_shallow_new, self.surface_json['button']['button_ship_shallow'])
                # self.screen.blit(self.button_ship_dark_new, self.surface_json['button']['button_ship_dark'])
                self.screen.blit(self.button_railway_shallow_new, self.surface_json['button']['button_railway_shallow'])

                self.screen.blit(self.button_road_shallow_new, self.surface_json['button']['button_road_shallow'])

                self.screen.blit(self.button_cancel_shallow_new, self.surface_json['button']['button_cancel_shallow'])


                self.screen.blit(self.button_finish_shallow_new, self.surface_json['button']['button_finish_shallow'])
            
                
                


                if self.i_am == 1:
                    self.screen.blit(self.point_player1_new, self.surface_json['point']['point_player1'])
                    self.screen.blit(self.point_player2_new, self.surface_json['point']['point_player2'])
                    self.screen.blit(self.point_player3_new, self.surface_json['point']['point_player3'])
                    self.screen.blit(self.point_player4_new, self.surface_json['point']['point_player4'])

                if self.i_am == 2:
                    self.screen.blit(self.point_player2_new, self.surface_json['point']['point_player1'])
                    self.screen.blit(self.point_player3_new, self.surface_json['point']['point_player2'])
                    self.screen.blit(self.point_player4_new, self.surface_json['point']['point_player3'])
                    self.screen.blit(self.point_player1_new, self.surface_json['point']['point_player4'])

                if self.i_am == 3:
                    self.screen.blit(self.point_player3_new, self.surface_json['point']['point_player1'])
                    self.screen.blit(self.point_player4_new, self.surface_json['point']['point_player2'])
                    self.screen.blit(self.point_player1_new, self.surface_json['point']['point_player3'])
                    self.screen.blit(self.point_player2_new, self.surface_json['point']['point_player4'])

                if self.i_am == 4:
                    self.screen.blit(self.point_player4_new, self.surface_json['point']['point_player1'])
                    self.screen.blit(self.point_player1_new, self.surface_json['point']['point_player2'])
                    self.screen.blit(self.point_player2_new, self.surface_json['point']['point_player3'])
                    self.screen.blit(self.point_player3_new, self.surface_json['point']['point_player4'])
                


                if self.game_active_audio == True:
                    self.screen.blit(self.button_open_audio_static_new, self.surface_json['button']['button_open_audio_static'])
                else:   
                    self.screen.blit(self.button_close_audio_static_new, self.surface_json['button']['button_close_audio_static'])
                
                


                '''
                以下表示各个玩家的trap 以及hide的状态，调用两张图片，需要依次进行判断后才可以显示

                self.screen.blit(self.label_hiding_all_new, self.surface_json['label']['label_hiding_all']['player1'])
                self.screen.blit(self.label_hiding_all_new, self.surface_json['label']['label_hiding_all']['player2'])
                self.screen.blit(self.label_hiding_all_new, self.surface_json['label']['label_hiding_all']['player3'])
                self.screen.blit(self.label_hiding_all_new, self.surface_json['label']['label_hiding_all']['player4'])
                self.screen.blit(self.label_trapped_all_new, self.surface_json['label']['label_trapped_all']['player1'])
                self.screen.blit(self.label_trapped_all_new, self.surface_json['label']['label_trapped_all']['player2'])
                self.screen.blit(self.label_trapped_all_new, self.surface_json['label']['label_trapped_all']['player3'])
                self.screen.blit(self.label_trapped_all_new, self.surface_json['label']['label_trapped_all']['player4'])
                '''

                

                
                #取决于是否轮到玩家turn
                if self.i_am == 1:
                    if self.total_info["round&client_number&time"][0]%4==1:
                        self.screen.blit(self.label_turn_player1_new, self.surface_json['label']['label_turn_player1'])
                    if self.total_info["round&client_number&time"][0]%4==2:
                        self.screen.blit(self.label_turn_player2_new, self.surface_json['label']['label_turn_player2'])
                    if self.total_info["round&client_number&time"][0]%4==3:
                        self.screen.blit(self.label_turn_player3_new, self.surface_json['label']['label_turn_player3'])
                    if self.total_info["round&client_number&time"][0]%4==0:
                        self.screen.blit(self.label_turn_player4_new, self.surface_json['label']['label_turn_player4'])
                if self.i_am == 2:
                    if self.total_info["round&client_number&time"][0]%4==2:
                        self.screen.blit(self.label_turn_player1_new, self.surface_json['label']['label_turn_player1'])
                    if self.total_info["round&client_number&time"][0]%4==3:
                        self.screen.blit(self.label_turn_player2_new, self.surface_json['label']['label_turn_player2'])
                    if self.total_info["round&client_number&time"][0]%4==0:
                        self.screen.blit(self.label_turn_player3_new, self.surface_json['label']['label_turn_player3'])
                    if self.total_info["round&client_number&time"][0]%4==1:
                        self.screen.blit(self.label_turn_player4_new, self.surface_json['label']['label_turn_player4'])
                if self.i_am == 3:
                    if self.total_info["round&client_number&time"][0]%4==3:
                        self.screen.blit(self.label_turn_player1_new, self.surface_json['label']['label_turn_player1'])
                    if self.total_info["round&client_number&time"][0]%4==0:
                        self.screen.blit(self.label_turn_player2_new, self.surface_json['label']['label_turn_player2'])
                    if self.total_info["round&client_number&time"][0]%4==1:
                        self.screen.blit(self.label_turn_player3_new, self.surface_json['label']['label_turn_player3'])
                    if self.total_info["round&client_number&time"][0]%4==2:
                        self.screen.blit(self.label_turn_player4_new, self.surface_json['label']['label_turn_player4'])
                if self.i_am == 4:
                    if self.total_info["round&client_number&time"][0]%4==0:
                        self.screen.blit(self.label_turn_player1_new, self.surface_json['label']['label_turn_player1'])
                    if self.total_info["round&client_number&time"][0]%4==1:
                        self.screen.blit(self.label_turn_player2_new, self.surface_json['label']['label_turn_player2'])
                    if self.total_info["round&client_number&time"][0]%4==2:
                        self.screen.blit(self.label_turn_player3_new, self.surface_json['label']['label_turn_player3'])
                    if self.total_info["round&client_number&time"][0]%4==3:
                        self.screen.blit(self.label_turn_player4_new, self.surface_json['label']['label_turn_player4'])
                
                # pass
                self.random_card = 0

                self.screen.blit(self.point_new, self.surface_point_json['1'])
                self.screen.blit(self.point_new, self.surface_point_json['2'])
                self.screen.blit(self.point_new, self.surface_point_json['3'])
                self.screen.blit(self.point_new, self.surface_point_json['4'])
                self.screen.blit(self.point_new, self.surface_point_json['5'])
                self.screen.blit(self.point_new, self.surface_point_json['6'])
                self.screen.blit(self.point_new, self.surface_point_json['7'])
                self.screen.blit(self.point_new, self.surface_point_json['8'])
                self.screen.blit(self.point_new, self.surface_point_json['9'])
                self.screen.blit(self.point_new, self.surface_point_json['10'])
                self.screen.blit(self.point_new, self.surface_point_json['11'])
                self.screen.blit(self.point_new, self.surface_point_json['12'])
                self.screen.blit(self.point_new, self.surface_point_json['13'])
                self.screen.blit(self.point_new, self.surface_point_json['14'])
                self.screen.blit(self.point_new, self.surface_point_json['15'])
                self.screen.blit(self.point_new, self.surface_point_json['16'])
                self.screen.blit(self.point_new, self.surface_point_json['17'])
                self.screen.blit(self.point_new, self.surface_point_json['18'])
                self.screen.blit(self.point_new, self.surface_point_json['19'])
                self.screen.blit(self.point_new, self.surface_point_json['20'])
                self.screen.blit(self.point_new, self.surface_point_json['21'])
                self.screen.blit(self.point_new, self.surface_point_json['22'])
                self.screen.blit(self.point_new, self.surface_point_json['23'])
                self.screen.blit(self.point_new, self.surface_point_json['24'])
                self.screen.blit(self.point_new, self.surface_point_json['25'])
                self.screen.blit(self.point_new, self.surface_point_json['26'])
                self.screen.blit(self.point_new, self.surface_point_json['27'])
                self.screen.blit(self.point_new, self.surface_point_json['28'])
                self.screen.blit(self.point_new, self.surface_point_json['29'])
                self.screen.blit(self.point_new, self.surface_point_json['30'])
                self.screen.blit(self.point_new, self.surface_point_json['31'])
                self.screen.blit(self.point_new, self.surface_point_json['32'])
                self.screen.blit(self.point_new, self.surface_point_json['33'])
                self.screen.blit(self.point_new, self.surface_point_json['34'])
                self.screen.blit(self.point_new, self.surface_point_json['35'])
                self.screen.blit(self.point_new, self.surface_point_json['36'])
                self.screen.blit(self.point_new, self.surface_point_json['37'])
                self.screen.blit(self.point_new, self.surface_point_json['38'])
                self.screen.blit(self.point_new, self.surface_point_json['39'])
                self.screen.blit(self.point_new, self.surface_point_json['40'])
                self.screen.blit(self.point_new, self.surface_point_json['41'])
                self.screen.blit(self.point_new, self.surface_point_json['42'])
                self.screen.blit(self.point_new, self.surface_point_json['43'])
                self.screen.blit(self.point_new, self.surface_point_json['44'])
                self.screen.blit(self.point_new, self.surface_point_json['45'])
                self.screen.blit(self.point_new, self.surface_point_json['46'])



                #-----------------------------------------------------------------------------------------------------------------------


                for i in range (1,47):
                    if self.total_info[f'{i}'][0] == 1:
                        self.screen.blit(self.point_player1_new, self.surface_point_player_json[f'{i}'])
                    if self.total_info[f'{i}'][0] == 2:
                        self.screen.blit(self.point_player2_new, self.surface_point_player_json[f'{i}'])
                    if self.total_info[f'{i}'][0] == 3:
                        self.screen.blit(self.point_player3_new, self.surface_point_player_json[f'{i}'])
                    if self.total_info[f'{i}'][0] == 4:
                        self.screen.blit(self.point_player4_new, self.surface_point_player_json[f'{i}'])
                    if self.total_info[f'{i}'][0] == 5:
                        self.screen.blit(self.point_war_new, self.surface_point_json[f'{i}'])
                    if self.total_info[f'{i}'][0] == 6 and self.total_info[f'{i}'][self.i_am + 2] != 0:
                        self.screen.blit(self.point_trap_new, self.surface_point_json[f'{i}'])
                    if self.total_info[f'{i}'][0] == 7:
                        #print("trap_1")
                        if self.i_am == 1:
                            if self.total_info[f'{i}'][7] == 1:
                                #print("trap_3")
                                self.screen.blit(self.point_player1_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_trapped_all_new, self.surface_json['label']['label_trapped_all']['player1'])
                            if self.total_info[f'{i}'][7] == 2:
                                self.screen.blit(self.point_player2_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_trapped_all_new, self.surface_json['label']['label_trapped_all']['player2'])
                            if self.total_info[f'{i}'][7] == 3:
                                self.screen.blit(self.point_player3_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_trapped_all_new, self.surface_json['label']['label_trapped_all']['player3'])
                            if self.total_info[f'{i}'][7] == 4:
                                self.screen.blit(self.point_player4_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_trapped_all_new, self.surface_json['label']['label_trapped_all']['player4'])
                        if self.i_am == 2:
                            if self.total_info[f'{i}'][7] == 2:
                                self.screen.blit(self.point_player2_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_trapped_all_new, self.surface_json['label']['label_trapped_all']['player1'])
                            if self.total_info[f'{i}'][7] == 3:
                                self.screen.blit(self.point_player3_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_trapped_all_new, self.surface_json['label']['label_trapped_all']['player2'])
                            if self.total_info[f'{i}'][7] == 4:
                                self.screen.blit(self.point_player4_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_trapped_all_new, self.surface_json['label']['label_trapped_all']['player3'])
                            if self.total_info[f'{i}'][7] == 1:
                                self.screen.blit(self.point_player1_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_trapped_all_new, self.surface_json['label']['label_trapped_all']['player4'])
                        if self.i_am == 3:
                            if self.total_info[f'{i}'][7] == 3:
                                self.screen.blit(self.point_player3_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_trapped_all_new, self.surface_json['label']['label_trapped_all']['player1'])
                            if self.total_info[f'{i}'][7] == 4:
                                self.screen.blit(self.point_player4_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_trapped_all_new, self.surface_json['label']['label_trapped_all']['player2'])
                            if self.total_info[f'{i}'][7] == 1:
                                self.screen.blit(self.point_player1_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_trapped_all_new, self.surface_json['label']['label_trapped_all']['player3'])
                            if self.total_info[f'{i}'][7] == 2:
                                self.screen.blit(self.point_player2_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_trapped_all_new, self.surface_json['label']['label_trapped_all']['player4'])
                        if self.i_am == 4:
                            if self.total_info[f'{i}'][7] == 4:
                                self.screen.blit(self.point_player4_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_trapped_all_new, self.surface_json['label']['label_trapped_all']['player1'])
                            if self.total_info[f'{i}'][7] == 1:
                                self.screen.blit(self.point_player1_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_trapped_all_new, self.surface_json['label']['label_trapped_all']['player2'])
                            if self.total_info[f'{i}'][7] == 2:
                                self.screen.blit(self.point_player2_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_trapped_all_new, self.surface_json['label']['label_trapped_all']['player3'])
                            if self.total_info[f'{i}'][7] == 3:
                                self.screen.blit(self.point_player3_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_trapped_all_new, self.surface_json['label']['label_trapped_all']['player4'])

                    if self.total_info[f'{i}'][0] == 8:
                        if self.i_am == 1:
                            if self.total_info[f'{i}'][8] == 1:
                                self.screen.blit(self.point_player1_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_hiding_all_new, self.surface_json['label']['label_hiding_all']['player1'])
                            if self.total_info[f'{i}'][8] == 2:
                                #self.screen.blit(self.point_player2_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_hiding_all_new, self.surface_json['label']['label_hiding_all']['player2'])
                            if self.total_info[f'{i}'][8] == 3:
                                #self.screen.blit(self.point_player3_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_hiding_all_new, self.surface_json['label']['label_hiding_all']['player3'])
                            if self.total_info[f'{i}'][8] == 4:
                                #self.screen.blit(self.point_player4_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_hiding_all_new, self.surface_json['label']['label_hiding_all']['player4'])
                        if self.i_am == 2:
                            if self.total_info[f'{i}'][8] == 2:
                                self.screen.blit(self.point_player2_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_hiding_all_new, self.surface_json['label']['label_hiding_all']['player1'])
                            if self.total_info[f'{i}'][8] == 3:
                                #self.screen.blit(self.point_player2_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_hiding_all_new, self.surface_json['label']['label_hiding_all']['player2'])
                            if self.total_info[f'{i}'][8] == 4:
                                #self.screen.blit(self.point_player3_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_hiding_all_new, self.surface_json['label']['label_hiding_all']['player3'])
                            if self.total_info[f'{i}'][8] == 1:
                                #self.screen.blit(self.point_player4_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_hiding_all_new, self.surface_json['label']['label_hiding_all']['player4'])
                        if self.i_am == 3:
                            if self.total_info[f'{i}'][8] == 3:
                                self.screen.blit(self.point_player3_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_hiding_all_new, self.surface_json['label']['label_hiding_all']['player1'])
                            if self.total_info[f'{i}'][8] == 4:
                                #self.screen.blit(self.point_player2_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_hiding_all_new, self.surface_json['label']['label_hiding_all']['player2'])
                            if self.total_info[f'{i}'][8] == 1:
                                #self.screen.blit(self.point_player3_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_hiding_all_new, self.surface_json['label']['label_hiding_all']['player3'])
                            if self.total_info[f'{i}'][8] == 2:
                                #self.screen.blit(self.point_player4_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_hiding_all_new, self.surface_json['label']['label_hiding_all']['player4'])
                        if self.i_am == 4:
                            if self.total_info[f'{i}'][8] == 4:
                                self.screen.blit(self.point_player4_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_hiding_all_new, self.surface_json['label']['label_hiding_all']['player1'])
                            if self.total_info[f'{i}'][8] == 1:
                                #elf.screen.blit(self.point_player2_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_hiding_all_new, self.surface_json['label']['label_hiding_all']['player2'])
                            if self.total_info[f'{i}'][8] == 2:
                                #self.screen.blit(self.point_player3_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_hiding_all_new, self.surface_json['label']['label_hiding_all']['player3'])
                            if self.total_info[f'{i}'][8] == 3:
                                #self.screen.blit(self.point_player4_new, self.surface_point_player_json[f'{i}'])
                                self.screen.blit(self.label_hiding_all_new, self.surface_json['label']['label_hiding_all']['player4'])

                
                if self.i_am == 1:
                    self.screen.blit(self.point_end_new, self.surface_point_json[f'{self.total_info["player1"][14]}'])
                if self.i_am == 2:
                    self.screen.blit(self.point_end_new, self.surface_point_json[f'{self.total_info["player2"][14]}'])
                if self.i_am == 3:
                    self.screen.blit(self.point_end_new, self.surface_point_json[f'{self.total_info["player3"][14]}'])
                if self.i_am == 4:
                    self.screen.blit(self.point_end_new, self.surface_point_json[f'{self.total_info["player4"][14]}'])

                    
                    
                #-----------------------------------------------------------------------------------------------------------------------







                





            if self.game_active_7:
                """商店界面"""
                self.screen.blit(self.window_shop_new, self.surface_json['window']['window_shop'])

                self.screen.blit(self.button_exit_shallow_new, self.surface_json['button']['button_exit_shallow'])


                self.screen.blit(self.button_buy_shallow_new, self.surface_json['button']['button_buy_shallow']['ship_ticket'])
                self.screen.blit(self.button_buy_shallow_new, self.surface_json['button']['button_buy_shallow']['railway_ticket'])
                self.screen.blit(self.button_buy_shallow_new, self.surface_json['button']['button_buy_shallow']['road_ticket'])
                self.screen.blit(self.button_buy_shallow_new, self.surface_json['button']['button_buy_shallow']['unknown_ticket'])
                self.screen.blit(self.button_buy_shallow_new, self.surface_json['button']['button_buy_shallow']['trap_card'])
                self.screen.blit(self.button_buy_shallow_new, self.surface_json['button']['button_buy_shallow']['skip_card'])
                self.screen.blit(self.button_buy_shallow_new, self.surface_json['button']['button_buy_shallow']['hide_card'])
                self.screen.blit(self.button_buy_shallow_new, self.surface_json['button']['button_buy_shallow']['war_card'])


                self.screen.blit(self.button_ship_shallow_new, self.surface_json['button']['button_ship_shallow'])
                # self.screen.blit(self.button_ship_dark_new, self.surface_json['button']['button_ship_dark'])
                self.screen.blit(self.button_railway_shallow_new, self.surface_json['button']['button_railway_shallow'])

                self.screen.blit(self.button_road_shallow_new, self.surface_json['button']['button_road_shallow'])

                self.screen.blit(self.button_war_shallow_new, self.surface_json['button']['button_war_shallow'])
                self.screen.blit(self.button_trap_shallow_new, self.surface_json['button']['button_trap_shallow'])
                self.screen.blit(self.button_skip_shallow_new, self.surface_json['button']['button_skip_shallow'])
                self.screen.blit(self.button_hide_shallow_new, self.surface_json['button']['button_hide_shallow'])

                if  self.random_card == 1 :
                    self.screen.blit(self.ticket_ship_new,self.surface_json["ticket"]["ticket_ship"])
                if  self.random_card == 2 :                
                    self.screen.blit(self.ticket_railway_new,self.surface_json["ticket"]["ticket_railway"])
                if  self.random_card == 3 :
                    self.screen.blit(self.ticket_road_new,self.surface_json["ticket"]["ticket_road"])
                    


                if self.i_am == 1:
                    self.screen.blit(self.point_player1_new, self.surface_json['point']['point_player1'])

                if self.i_am == 2:
                    self.screen.blit(self.point_player2_new, self.surface_json['point']['point_player1'])

                if self.i_am == 3:
                    self.screen.blit(self.point_player3_new, self.surface_json['point']['point_player1'])

                if self.i_am == 4:
                    self.screen.blit(self.point_player4_new, self.surface_json['point']['point_player1'])

                    


                if self.game_active_audio == True:
                    self.screen.blit(self.button_open_audio_static_new, self.surface_json['button']['button_open_audio_static'])
                else:   
                    self.screen.blit(self.button_close_audio_static_new, self.surface_json['button']['button_close_audio_static'])


                '''盲盒抽出的卡，需要具体if判断
                self.screen.blit(self.ticket_railway_new, self.surface_json['ticket']['ticket_railway'])
                self.screen.blit(self.ticket_road_new, self.surface_json['ticket']['ticket_road'])
                self.screen.blit(self.ticket_ship_new, self.surface_json['ticket']['ticket_ship'])
                '''
                

                # pass

            if self.game_active_8:
                """结算界面"""

                self.screen.blit(self.window_ending_new, self.surface_json['window']['window_ending'])
                if self.game_active_audio == True:
                    self.screen.blit(self.button_open_audio_static_new, self.surface_json['button']['button_open_audio_static'])
                else:   
                    self.screen.blit(self.button_close_audio_static_new, self.surface_json['button']['button_close_audio_static'])
                
                if self.total_info["round&client_number&time"][4] == 1:
                    self.screen.blit(self.point_player1_new, self.surface_json['point']['point_winner'])
                if self.total_info["round&client_number&time"][4] == 2:
                    self.screen.blit(self.point_player2_new, self.surface_json['point']['point_winner'])
                if self.total_info["round&client_number&time"][4] == 3:
                    self.screen.blit(self.point_player3_new, self.surface_json['point']['point_winner'])
                if self.total_info["round&client_number&time"][4] == 4:
                    self.screen.blit(self.point_player4_new, self.surface_json['point']['point_winner'])

                # pass

            if self.game_active_11:
                '''rules界面'''
                self.screen.blit(self.window_rules_new, self.surface_json['window']['window_ending'])
                if self.game_active_audio == True:
                    self.screen.blit(self.button_open_audio_static_new, self.surface_json['button']['button_open_audio_static'])
                else:   
                    self.screen.blit(self.button_close_audio_static_new, self.surface_json['button']['button_close_audio_static'])

                self.screen.blit(self.button_out_static_new, self.surface_json['button']['button_out_static'])

            if self.game_active_10:
                '''rules界面'''
                self.screen.blit(self.window_About_us_new, self.surface_json['window']['window_ending'])
                if self.game_active_audio == True:
                    self.screen.blit(self.button_open_audio_static_new, self.surface_json['button']['button_open_audio_static'])
                else:   
                    self.screen.blit(self.button_close_audio_static_new, self.surface_json['button']['button_close_audio_static'])

                self.screen.blit(self.button_out_static_new, self.surface_json['button']['button_out_static'])

    def _check_button(self):     
            # if self.window_cover_new_rect.collidepoint(self.mouse_click_pos) and self.game_active_1 == True and self.x >= 200:
            #     self.game_active_1 = False
            #     self.game_active_2 = True
            #     self.mouse_click_pos = (-1,-1)
                
            if self.button_Multi_player_highlight_new_rect.collidepoint(self.mouse_click_pos) and self.game_active_2 == True and self.game_active_1 == False:
                self.game_active_2 = False
                self.game_active_3 = True
                self.mouse_click_pos = (-1,-1)

            if self.button_Rules_highlight_new_rect.collidepoint(self.mouse_click_pos) and self.game_active_2 == True and self.game_active_1 == False:
                self.game_active_2 = False
                self.game_active_11 = True
                self.mouse_click_pos = (-1,-1)

            if self.button_About_us_highlight_new_rect.collidepoint(self.mouse_click_pos) and self.game_active_2 == True and self.game_active_1 == False:
                self.game_active_2 = False
                self.game_active_10 = True
                self.mouse_click_pos = (-1,-1)
                
            if self.button_create_a_room_highlight_new_rect.collidepoint(self.mouse_click_pos) and self.game_active_1 == False and self.game_active_3 == True:   
                self.game_active_3 = False        #房间选择（建立or加入）界面
                self.game_active_4 = True
                self.mouse_click_pos = (-1,-1)


            #加入房间高光按钮
            if self.button_join_in_a_room_highlight_new_rect.collidepoint(self.mouse_click_pos) and self.game_active_1 == False and self.game_active_3 == True:           
                self.game_active_3 = False
                self.game_active_5 = True    ##matching界面
                self.mouse_click_pos = (-1,-1)

            #button_open_audio_highlight
            if self.game_active_audio == True and self.button_open_audio_highlight_new_rect.collidepoint(self.mouse_click_pos): 
                self.game_active_audio = False
                self.mouse_click_pos = (-1,-1)

            #button_close_audio_highlight
            if self.game_active_audio == False and self.button_close_audio_highlight_new_rect.collidepoint(self.mouse_click_pos):              
                self.game_active_audio = True
                self.mouse_click_pos = (-1,-1)

            #button_out_highlight
            if self.button_out_highlight_new_rect.collidepoint(self.mouse_click_pos) and self.game_active_3 == True:            
            
                self.game_active_3 = False
                self.game_active_2 = True
                ##print(1)
                self.mouse_click_pos = (-1,-1)
                

            if self.button_out_highlight_new_rect.collidepoint(self.mouse_click_pos) and self.game_active_4 == True: 
                self.game_active_4 = False
                self.game_active_3 = True
                ##print(2)
                self.mouse_click_pos = (-1,-1)
            

            if self.button_out_highlight_new_rect.collidepoint(self.mouse_click_pos) and self.game_active_5 == True: 
                self.game_active_5 = False         #matching界面
                self.game_active_3 = True
                ##print(3)
                self.mouse_click_pos = (-1,-1)

            if self.button_out_highlight_new_rect.collidepoint(self.mouse_click_pos) and self.game_active_11 == True: 
                self.game_active_11 = False
                self.game_active_2 = True
                ##print(3)
                self.mouse_click_pos = (-1,-1)

            if self.button_out_highlight_new_rect.collidepoint(self.mouse_click_pos) and self.game_active_10 == True: 
                self.game_active_10 = False
                self.game_active_2 = True
                ##print(3)
                self.mouse_click_pos = (-1,-1)

            if self.button_shop_dark_new_rect.collidepoint(self.mouse_click_pos) and self.game_active_6 == True: 
                self.game_active_6 = False
                self.game_active_7 = True
                ##print(3)
                self.mouse_click_pos = (-1,-1)            

            if self.button_exit_dark_new_rect.collidepoint(self.mouse_click_pos) and self.game_active_7 == True: 
                self.game_active_7 = False
                self.game_active_6 = True
                ##print(3)
                self.mouse_click_pos = (-1,-1)            
                        
    def _blit_hightlight(self):
            if self.highlight_active_1 and self.game_active_2:
                self.screen.blit(self.button_Multi_player_highlight_new, self.surface_json['button']['button_Multi_player_highlight'])
            if self.highlight_active_2 and self.game_active_2:
                self.screen.blit(self.button_Rules_highlight_new, self.surface_json['button']['button_Rules_highlight'])
            if self.highlight_active_3 and self.game_active_2:
                self.screen.blit(self.button_About_us_highlight_new, self.surface_json['button']['button_About_us_highlight'])
            if self.highlight_active_4 and self.game_active_3:       # 如果收到highlight标识且处于对应的界面，那么就blit highlight
                self.screen.blit(self.button_create_a_room_highlight_new, self.surface_json['button']['button_create_a_room_highlight'])
            if self.highlight_active_5 and self.game_active_3:       # 如果收到highlight标识且处于对应的界面，那么就blit highlight
                self.screen.blit(self.button_join_in_a_room_highlight_new, self.surface_json['button']['button_join_in_a_room_highlight'])

            if self.highlight_active_6 and self.game_active_1 == False:                               # 如果收到highlight标识且处于对应的界面，那么就blit highlight
                self.screen.blit(self.button_open_audio_highlight_new, self.surface_json['button']['button_open_audio_highlight'])
            if self.highlight_active_7 and self.game_active_1 == False:                               # 如果收到highlight标识且处于对应的界面，那么就blit highlight
                self.screen.blit(self.button_close_audio_highlight_new, self.surface_json['button']['button_close_audio_highlight'])

            if self.highlight_active_8 and self.game_active_5:                               # 如果收到highlight标识且处于对应的界面，那么就blit highlight
                self.screen.blit(self.button_enter_your_room_address_highlight_new, self.surface_json['button']['button_enter_your_room_address_highlight'])     # 如果收到highlight标识且处于对应的界面，那么就blit highlight
            if self.highlight_active_9 and (self.game_active_3 or self.game_active_4 or self.game_active_5 or self.game_active_11 or self.game_active_10) :         # 如果被碰到，发送highlight标识
                self.screen.blit(self.button_out_highlight_new, self.surface_json['button']['button_out_highlight'])

            if self.highlight_active_10 and (self.game_active_6) :         # 如果被碰到，发送highlight标识
                self.screen.blit(self.button_shop_dark_new, self.surface_json['button']['button_shop_dark'])

            if self.highlight_active_11 and (self.game_active_7) :         # 如果被碰到，发送highlight标识
                self.screen.blit(self.button_exit_dark_new, self.surface_json['button']['button_exit_dark'])

            if self.highlight_active_12 and (self.game_active_6) :
                self.screen.blit(self.button_hide_dark_new, self.surface_json['button']['button_hide_dark'])

            if self.highlight_active_13 and (self.game_active_6) :
                self.screen.blit(self.button_skip_dark_new, self.surface_json['button']['button_skip_dark'])

            if self.highlight_active_14 and (self.game_active_6) :
                self.screen.blit(self.button_war_dark_new, self.surface_json['button']['button_war_dark'])

            if self.highlight_active_15 and (self.game_active_6) :
                self.screen.blit(self.button_trap_dark_new, self.surface_json['button']['button_trap_dark'])

            if self.highlight_active_16 and (self.game_active_6) :
                self.screen.blit(self.button_ship_dark_new, self.surface_json['button']['button_ship_dark'])

            if self.highlight_active_17 and (self.game_active_6) :
                self.screen.blit(self.button_railway_dark_new, self.surface_json['button']['button_railway_dark'])

            if self.highlight_active_18 and (self.game_active_6) :
                self.screen.blit(self.button_road_dark_new, self.surface_json['button']['button_road_dark'])

            if self.highlight_active_19 and (self.game_active_6) :
                self.screen.blit(self.button_cancel_dark_new, self.surface_json['button']['button_cancel_dark'])

            if self.highlight_active_20 and (self.game_active_6) :
                self.screen.blit(self.button_finish_dark_new, self.surface_json['button']['button_finish_dark'])
  
    def _highlight_button(self):
            # #print(self.button_Multi_player_static_new_rect)
            if self.button_Multi_player_static_new_rect.collidepoint(self.mouse_pos)and self.game_active_2:         # 如果被碰到，发送highlight标识
                self.highlight_active_1 = True
            else:  
                self.highlight_active_1 = False
            if self.button_Rules_static_new_rect.collidepoint(self.mouse_pos)and self.game_active_2:         # 如果被碰到，发送highlight标识
                self.highlight_active_2 = True
            else:  
                self.highlight_active_2 = False
            if self.button_About_us_static_new_rect.collidepoint(self.mouse_pos)and self.game_active_2:         # 如果被碰到，发送highlight标识
                self.highlight_active_3 = True
            else:  
                self.highlight_active_3 = False
            if self.button_create_a_room_static_new_rect.collidepoint(self.mouse_pos)and self.game_active_3:         # 如果被碰到，发送highlight标识
                self.highlight_active_4 = True      #创建房间高光按钮
            else:  
                self.highlight_active_4 = False
            if self.button_join_in_a_room_static_new_rect.collidepoint(self.mouse_pos)and self.game_active_3:         # 如果被碰到，发送highlight标识
                self.highlight_active_5 = True      #加入房间高光按钮
            else:  
                self.highlight_active_5 = False


            if self.button_open_audio_static_new_rect.collidepoint(self.mouse_pos)and self.game_active_1==False and self.game_active_audio == True:         # 如果被碰到，发送highlight标识
                self.highlight_active_7 = True
            else:  
                self.highlight_active_6 = False

            if self.button_close_audio_static_new_rect.collidepoint(self.mouse_pos)and self.game_active_1==False and self.game_active_audio == False:         # 如果被碰到，发送highlight标识
                self.highlight_active_6 = True
            else:  
                self.highlight_active_7 = False


            if self.button_enter_your_room_address_static_new_rect.collidepoint(self.mouse_pos)and self.game_active_5:         # 如果被碰到，发送highlight标识
                self.highlight_active_8 = True
            else:  
                self.highlight_active_8 = False
            if self.button_out_static_new_rect.collidepoint(self.mouse_pos) and (self.game_active_3 or self.game_active_4 or self.game_active_5 or self.game_active_11 or self.game_active_10):
                self.highlight_active_9 = True
            else:  
                self.highlight_active_9 = False

            if self.button_shop_shallow_new_rect.collidepoint(self.mouse_pos) and (self.game_active_6):
                self.highlight_active_10 = True
            else:  
                self.highlight_active_10 = False

            if self.button_exit_shallow_new_rect.collidepoint(self.mouse_pos) and (self.game_active_7):
                self.highlight_active_11 = True
            else:  
                self.highlight_active_11 = False

            if self.button_hide_shallow_new_rect.collidepoint(self.mouse_pos) and (self.game_active_6):
                self.highlight_active_12 = True
            else:  
                self.highlight_active_12 = False

            if self.button_skip_shallow_new_rect.collidepoint(self.mouse_pos) and (self.game_active_6):
                self.highlight_active_13 = True
            else:  
                self.highlight_active_13 = False

            if self.button_war_shallow_new_rect.collidepoint(self.mouse_pos) and (self.game_active_6):
                self.highlight_active_14 = True
            else:  
                self.highlight_active_14 = False

            if self.button_trap_shallow_new_rect.collidepoint(self.mouse_pos) and (self.game_active_6):
                self.highlight_active_15 = True
            else:  
                self.highlight_active_15 = False

            if self.button_ship_shallow_new_rect.collidepoint(self.mouse_pos) and (self.game_active_6):
                self.highlight_active_16 = True
            else:  
                self.highlight_active_16 = False

            if self.button_railway_shallow_new_rect.collidepoint(self.mouse_pos) and (self.game_active_6):
                self.highlight_active_17 = True
            else:  
                self.highlight_active_17 = False

            if self.button_road_shallow_new_rect.collidepoint(self.mouse_pos) and (self.game_active_6):
                self.highlight_active_18 = True
            else:  
                self.highlight_active_18 = False

            if self.button_cancel_shallow_new_rect.collidepoint(self.mouse_pos) and (self.game_active_6):
                self.highlight_active_19 = True
            else:  
                self.highlight_active_19 = False

            if self.button_finish_shallow_new_rect.collidepoint(self.mouse_pos) and (self.game_active_6):
                self.highlight_active_20 = True
            else:  
                self.highlight_active_20 = False



# 服务器回合清算代码
    def calculate(self):
        if self.have_calculated_number < self.total_info["round&client_number&time"][0]:

            if self.total_info["round&client_number&time"][0] % 4 == 1:
                self.total_info['player1'][0] += 100
                self.total_info['player2'][0] += 100
                self.total_info['player3'][0] += 100
                self.total_info['player4'][0] += 100
                for i in range(1,47):
                    if self.total_info[str(f'{i}')][0] == 5:
                        self.total_info[str(f'{i}')][1] -= 1 
                        if self.total_info[str(f'{i}')][1] ==0:
                            self.total_info[str(f'{i}')][0] = 0           #天下太平
                    if self.total_info[str(f'{i}')][0] == 7:
                        self.total_info[str(f'{i}')][2] -= 0.5
                        if self.total_info[str(f'{i}')][2] == 0:
                            self.total_info[str(f'{i}')][0] = self.total_info[str(f'{i}')][7] #self.i_am   #刑满释放
                            self.total_info[str(f'{i}')][7] = 0
                            #self.total_info[str(f'{i}')][2]
                    if self.total_info[str(f'{i}')][9]>0:
                        self.total_info[str(f'{i}')][9] -= 1
                        if self.total_info[str(f'{i}')][9] ==0:
                            self.total_info[str(f'{i}')][0] = 1 #self.i_am   #原形毕露

            if self.total_info["round&client_number&time"][0] % 8 == 1:
                num1 = random.randint(1,3)
                self.total_info['player1'][num1] += 1
                num2 = random.randint(1,3)
                self.total_info['player2'][num2] += 1
                num3 = random.randint(1,3)
                self.total_info['player3'][num3] += 1
                num4 = random.randint(1,3)
                self.total_info['player4'][num4] += 1

            if self.total_info["round&client_number&time"][0] == 1:
                num1 = random.randint(1,3)
                self.total_info['player1'][num1] += 1
                num2 = random.randint(1,3)
                self.total_info['player2'][num2] += 1
                num3 = random.randint(1,3)
                self.total_info['player3'][num3] += 1
                num4 = random.randint(1,3)
                self.total_info['player4'][num4] += 1
                num1 = random.randint(1,3)
                self.total_info['player1'][num1] += 1
                num2 = random.randint(1,3)
                self.total_info['player2'][num2] += 1
                num3 = random.randint(1,3)
                self.total_info['player3'][num3] += 1
                num4 = random.randint(1,3)
                self.total_info['player4'][num4] += 1
                
            self.have_calculated_number += 4

            # elif self.total_info["round&client_number&time"][0] % 4 == 2:
            #     self.total_info['player2'][0] += 100
            #     for i in range(1,47):
            #         if self.total_info[str(f'{i}')][0] == 5:
            #             self.total_info[str(f'{i}')][1] -= 1 
            #             if self.total_info[str(f'{i}')][1] ==0:
            #                 self.total_info[str(f'{i}')][0] = 0           #天下太平
            #         if self.total_info[str(f'{i}')][0] == 7:
            #             self.total_info[str(f'{i}')][2] -= 1
            #             if self.total_info[str(f'{i}')][2] == 0:
            #                 self.total_info[str(f'{i}')][0] = 2 #self.i_am   #刑满释放
            #         if self.total_info[str(f'{i}')][10]>=0:
            #             self.total_info[str(f'{i}')][10] -= 1
            #             if self.total_info[str(f'{i}')][10] ==0:
            #                 self.total_info[str(f'{i}')][0] = 2 #self.i_am   #原形毕露

            # elif self.total_info["round&client_number&time"][0] % 4 == 3:
            #     self.total_info['player3'][0] += 100
            #     for i in range(1,47):
            #         if self.total_info[str(f'{i}')][0] == 5:
            #             self.total_info[str(f'{i}')][1] -= 1 
            #             if self.total_info[str(f'{i}')][1] ==0:
            #                 self.total_info[str(f'{i}')][0] = 0           #天下太平
            #         if self.total_info[str(f'{i}')][0] == 7:
            #             self.total_info[str(f'{i}')][2] -= 1
            #             if self.total_info[str(f'{i}')][2] == 0:
            #                 self.total_info[str(f'{i}')][0] = 3 #self.i_am   #刑满释放
            #         if self.total_info[str(f'{i}')][10]>=0:
            #             self.total_info[str(f'{i}')][10] -= 1
            #             if self.total_info[str(f'{i}')][10] ==0:
            #                 self.total_info[str(f'{i}')][0] = 3 #self.i_am   #原形毕露

            # elif self.total_info["round&client_number&time"][0] % 4 == 0:
            #     self.total_info['player4'][0] += 100
            #     for i in range(1,47):
            #         if self.total_info[str(f'{i}')][0] == 5:
            #             self.total_info[str(f'{i}')][1] -= 1 
            #             if self.total_info[str(f'{i}')][1] ==0:
            #                 self.total_info[str(f'{i}')][0] = 0           #天下太平
            #         if self.total_info[str(f'{i}')][0] == 7:
            #             self.total_info[str(f'{i}')][2] -= 1
            #             if self.total_info[str(f'{i}')][2] == 0:
            #                 self.total_info[str(f'{i}')][0] = 4 #self.i_am   #刑满释放
            #         if self.total_info[str(f'{i}')][10]>=0:
            #             self.total_info[str(f'{i}')][10] -= 1
            #             if self.total_info[str(f'{i}')][10] ==0:
            #                 self.total_info[str(f'{i}')][0] = 4 #self.i_am   #原形毕露

            

        







    #客户端专用代码
    def enter_room(self):
        self.ipv4_entry = tk.Entry(self.window)
        self.button = tk.Button(self.window, text="点击进入房間",command=self._exit_)
        #执行_exit_

        self.ipv4_label = tk.Label(self.window, text="请输入IPv4地址:")
        self.ipv4_label.pack()
        self.ipv4_entry.pack()
        self.button.pack()
        self.window.mainloop()
        threading.Thread(target=run_client, args=(self,)).start()

    def _exit_(self):
        self.ipv4 = self.ipv4_entry.get()#一个entry控件，get()方法获取控件的文本内容
        self.port = 8000  # 设置端口号
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket对象
        #print(self.ipv4)
        self.game_active_3 = False
        self.game_active_5 = True
        if self.button.winfo_exists():
            self.window.destroy()
 



    def alter_1(self,a1,b1,c1):
        self.co['class1'] = a1
        self.co['data1'][0] =b1
        self.co['data1'][1] =c1
    def alter_2(self,a2,b2,c2):
        self.co['class2'] = a2
        self.co['data2'][0] =b2
        self.co['data2'][1] =c2
    def alter_3(self,a3,b3,c3):
        self.co['class3'] = a3
        self.co['data3'][0] =b3
        self.co['data3'][1] =c3
    def alter_4(self,a4,b4,c4):
        self.co['class4'] = a4
        self.co['data4'][0] =b4
        self.co['data4'][1] =c4
    def alter_5(self,a5,b5,c5):
        self.co['class5'] = a5
        self.co['data5'][0] =b5
        self.co['data5'][1] =c5




#player里面，数字依次表示money(0),ship_card(1),railway_card(2),road_card(3),war_card(4)
#trap_card(5),hide_card(6),skip_card(7),被trap时间(8),使用trap次数(9),使用war次数(10),使用hide次数(11)
#使用skip次数(12),起点(13),终点(14)

    def shop_button(self):
        """有关商店界面的按钮"""
        #水路票
        if self.button_buy_dark_ship_ticket_new_rect.collidepoint(self.mouse_click_pos) and self.game_active_7 == True:
            if self.total_info[self.player][0] >= 150:
                if self.i_am == 1:
                    self.total_info[self.player][1] += 1
                    self.total_info[self.player][0] -= 150
                    self.mouse_click_pos = (-1,-1)
                else:
                    self.alter_1(self.player,1,self.total_info[self.player][1] + 1)
                    self.alter_2(self.player,0,self.total_info[self.player][0] - 150)
                    self.mouse_click_pos = (-1,-1)

        #铁路票
        elif self.button_buy_dark_railway_ticket_new_rect.collidepoint(self.mouse_click_pos) and self.game_active_7 == True:
            if self.total_info[self.player][0] >= 150:
                if self.i_am == 1:
                    self.total_info[self.player][2] += 1
                    self.total_info[self.player][0] -= 150
                    self.mouse_click_pos = (-1,-1)
                else:
                    self.alter_1(self.player,2,self.total_info[self.player][2] + 1)
                    self.alter_2(self.player,0,self.total_info[self.player][0] - 150)
                    self.mouse_click_pos = (-1,-1)

        #公路票
        elif self.button_buy_dark_road_ticket_new_rect.collidepoint(self.mouse_click_pos) and self.game_active_7 == True:
            if self.total_info[self.player][0] >= 150:
                if self.i_am == 1:
                    self.total_info[self.player][3] += 1
                    self.total_info[self.player][0] -= 150
                    self.mouse_click_pos = (-1,-1)
                else:
                    self.alter_1(self.player,3,self.total_info[self.player][3] + 1)
                    self.alter_2(self.player,0,self.total_info[self.player][0] - 150)
                    self.mouse_click_pos = (-1,-1)


        #随机票
        elif self.button_buy_dark_unknown_ticket_new_rect.collidepoint(self.mouse_click_pos) and self.game_active_7 == True:
            if self.total_info[self.player][0] >= 100:
                a = random.randint(1,3)
                if self.i_am==1:
                    self.total_info[self.player][0] -= 100
                    if a == 1:
                        self.total_info[self.player][1] +=1
                        self.random_card = 1
                    elif a==2:
                        self.total_info[self.player][2] +=1
                        self.random_card = 2
                    elif a==3:
                        self.total_info[self.player][3] +=1
                        self.random_card = 3
                else:
                    self.alter_1(self.player,0,self.total_info[self.player][0]-100)
                    if a == 1:
                        self.alter_2(self.player,1,self.total_info[self.player][1]+1)
                        self.random_card = 1
                    elif a==2:
                        self.alter_2(self.player,2,self.total_info[self.player][2]+1)
                        self.random_card = 2
                    elif a==3:
                        self.alter_2(self.player,3,self.total_info[self.player][3]+1)
                        self.random_card = 3
            self.mouse_click_pos = (-1,-1)            


        #战争卡
        elif self.button_buy_dark_war_card_new_rect.collidepoint(self.mouse_click_pos) and self.game_active_7 == True:
                if self.i_am == 1:
                    self.total_info[self.player][4] += 1
                    self.total_info[self.player][0] -= 200
                    self.mouse_click_pos = (-1,-1)
                else:
                    self.alter_1(self.player,4,self.total_info[self.player][4] + 1)
                    self.alter_2(self.player,0,self.total_info[self.player][0] - 200)
                    self.mouse_click_pos = (-1,-1)       
        
        #陷阱卡
        elif self.button_buy_dark_trap_card_new_rect.collidepoint(self.mouse_click_pos) and self.game_active_7 == True:
            if self.total_info[self.player][0] >= 250:
                if self.i_am == 1:
                    self.total_info[self.player][5] += 1
                    self.total_info[self.player][0] -= 250
                    self.mouse_click_pos = (-1,-1)
                else:
                    self.alter_1(self.player,5,self.total_info[self.player][5] + 1)
                    self.alter_2(self.player,0,self.total_info[self.player][0] - 250)
                    self.mouse_click_pos = (-1,-1)

        #隐身卡
        elif self.button_buy_dark_hide_card_new_rect.collidepoint(self.mouse_click_pos) and self.game_active_7 == True:
                if self.i_am == 1:
                    self.total_info[self.player][6] += 1
                    self.total_info[self.player][0] -= 300
                    self.mouse_click_pos = (-1,-1)
                else:
                    self.alter_1(self.player,6,self.total_info[self.player][6] + 1)
                    self.alter_2(self.player,0,self.total_info[self.player][0] - 300)
                    self.mouse_click_pos = (-1,-1)

        #跃迁卡
        elif self.button_buy_dark_skip_card_new_rect.collidepoint(self.mouse_click_pos) and self.game_active_7 == True:
                if self.i_am == 1:
                    self.total_info[self.player][7] += 1
                    self.total_info[self.player][0] -= 200
                    self.mouse_click_pos = (-1,-1)
                else:
                    self.alter_1(self.player,7,self.total_info[self.player][7] + 1)
                    self.alter_2(self.player,0,self.total_info[self.player][0] - 200)
                    self.mouse_click_pos = (-1,-1)



        
        if self.button_buy_shallow_ship_ticket_new_rect.collidepoint(self.mouse_pos) and self.game_active_7 == True:
            self.screen.blit(self.button_buy_dark_new, self.surface_json['button']['button_buy_dark']['ship_ticket'])
                    
        if self.button_buy_shallow_railway_ticket_new_rect.collidepoint(self.mouse_pos) and self.game_active_7 == True:
            self.screen.blit(self.button_buy_dark_new, self.surface_json['button']['button_buy_dark']['railway_ticket'])
            
        if self.button_buy_shallow_road_ticket_new_rect.collidepoint(self.mouse_pos) and self.game_active_7 == True:
            self.screen.blit(self.button_buy_dark_new, self.surface_json['button']['button_buy_dark']['road_ticket'])
        
        if self.button_buy_shallow_unknown_ticket_new_rect.collidepoint(self.mouse_pos) and self.game_active_7 == True:
            self.screen.blit(self.button_buy_dark_new, self.surface_json['button']['button_buy_dark']['unknown_ticket'])
                
        if self.button_buy_shallow_trap_card_new_rect.collidepoint(self.mouse_pos) and self.game_active_7 == True:
            self.screen.blit(self.button_buy_dark_new, self.surface_json['button']['button_buy_dark']['trap_card'])
                
        if self.button_buy_shallow_hide_card_new_rect.collidepoint(self.mouse_pos) and self.game_active_7 == True:
            self.screen.blit(self.button_buy_dark_new, self.surface_json['button']['button_buy_dark']['hide_card'])
                
        if self.button_buy_shallow_skip_card_new_rect.collidepoint(self.mouse_pos) and self.game_active_7 == True:
            self.screen.blit(self.button_buy_dark_new, self.surface_json['button']['button_buy_dark']['skip_card'])
              
        if self.button_buy_shallow_war_card_new_rect.collidepoint(self.mouse_pos) and self.game_active_7 == True:
            self.screen.blit(self.button_buy_dark_new, self.surface_json['button']['button_buy_dark']['war_card'])

#这里放一回合内玩家进行的操作
    def action(self):
        self.increase_money()

    def increase_money(self):
        """每回合增加玩家的金钱"""
        if self.total_info["round&client_number&time"][0] %4 ==1:
            self.total_info['player1'][0] += 100

        if self.total_info["round&client_number&time"][0] %4 ==2:
            self.total_info['player2'][0] += 100

        if self.total_info["round&client_number&time"][0] %4 ==3:
            self.total_info['player3'][0] += 100

        if self.total_info["round&client_number&time"][0] %4 ==0:
            self.total_info['player4'][0] += 100






#------------------------------------------------卡牌使用--------------------------------------------
    #战争卡使用
    def _war_card(self):
        if self.button_war_dark_new_rect.collidepoint(self.mouse_click_pos) and self.total_info[self.player][4]>0:
            self.click_point = 0
            self.mouse_click_pos = (-1,-1)
            #手里有战争卡且点击打开active
            self._msg_war()
            self.war_active = True
        if self.war_active:
            self._msg_cancel()
            if str(self.click_point) in self.total_info and self.total_info[str(self.click_point)][0] ==0 and self.total_info[str(self.click_point)][1] !=0 and self.click_point != 1 and self.click_point != 2 and self.click_point != 3 and self.click_point != 4 and self.click_point != 8 and self.click_point != 39 and self.click_point != 44 and self.click_point != 45 and self.click_point != 41 and self.click_point != 42 and self.click_point != 46 and self.click_point != 43:
                #点空且未设置过战争
                if self.i_am ==1:
                    self.total_info[self.player][4] -=1#玩家战争卡减少
                    self.total_info[self.player][10] +=1#玩家使用战争卡次数增多
                    self.total_info[str(self.click_point)][0] = 5#点处于战争状态
                    self.total_info[str(self.click_point)][1] = 3#点处于战争状态3回合
                else:
                    self.alter_1(self.player,4,self.total_info[self.player][4]-1)
                    self.alter_2(self.player,10,self.total_info[self.player][10]+1)
                    self.alter_3(str(self.click_point),0,5)
                    self.alter_4(str(self.click_point),1,3)
                self.war_active=False

    #陷阱卡使用
    def _trap_card(self):
        if self.button_trap_dark_new_rect.collidepoint(self.mouse_click_pos) and self.total_info[self.player][5] > 0:
            self.mouse_click_pos = (-1,-1)
            self.click_point = 0
            #有陷阱卡且点击打开active
            self.trap_active = True
        if self.trap_active:
            self._msg_cancel()
            self._msg_trap()
            if str(self.click_point) in self.total_info and self.click_point != self.total_info[self.player][13] and self.total_info[str(self.click_point)][0]!=5 and self.click_point != 1 and self.click_point != 2 and self.click_point != 3 and self.click_point != 4 and self.click_point != 8 and self.click_point != 39 and self.click_point != 44 and self.click_point != 45 and self.click_point != 41 and self.click_point != 42 and self.click_point != 46 and self.click_point != 43:
                #点击点没有玩家且没有战争
                if self.player == 'player1':
                    self.total_info[str(self.click_point)][3]+=1
                    self.total_info[str(self.click_point)][0] = 6
                    self.total_info[self.player][5] -= 1
                    self.total_info[self.player][9] += 1  
                    self.total_info[str(self.click_point)][2] = (self.total_info[str(self.click_point)][3]+self.total_info[str(self.click_point)][4]+self.total_info[str(self.click_point)][5]+self.total_info[str(self.click_point)][6])*2                  
                elif self.player == 'player2':
                    self.alter_1(str(self.click_point),4,self.total_info[str(self.click_point)][4]+1)   
                    self.alter_2(str(self.click_point),0,6)
                    self.alter_3(self.player,5,self.total_info[self.player][5]-1)
                    self.alter_4(self.player,9,self.total_info[self.player][9]+1)
                elif self.player == 'player3':
                    self.alter_1(str(self.click_point),5,self.total_info[str(self.click_point)][4]+1)   
                    self.alter_2(str(self.click_point),0,6)
                    self.alter_3(self.player,5,self.total_info[self.player][5]-1)
                    self.alter_4(self.player,9,self.total_info[self.player][9]+1)
                elif self.player == 'player4':
                    self.alter_1(str(self.click_point),6,self.total_info[str(self.click_point)][4]+1)   
                    self.alter_2(str(self.click_point),0,6)
                    self.alter_3(self.player,5,self.total_info[self.player][5]-1)
                    self.alter_4(self.player,9,self.total_info[self.player][9]+1)  
                self.alter_5(str(self.click_point),2,(self.total_info[str(self.click_point)][3]+self.total_info[str(self.click_point)][4]+self.total_info[str(self.click_point)][5]+self.total_info[str(self.click_point)][6])*2)                    
                self.trap_active = False

    #跃迁卡使用
    def _skip_card(self):
        if self.button_skip_dark_new_rect.collidepoint(self.mouse_click_pos) and self.total_info[self.player][7]>0:
            #玩家手里有跃迁卡并且点击
            self.skip_active = True
            self.mouse_click_pos = (-1,-1)
        if self.skip_active:
            self._msg_cancel()
            self._msg_skip()
            for d in self.point_json[str(self.total_info[self.player][13])]["neighbour"]:
                if self.total_info[str(d)][0] ==0:
                    self.skip_active_2 = True
                else:
                    self.skip_active_2 = False
                    break
            if self.msg_skip_image_rect.collidepoint(self.mouse_click_pos) and self.skip_active_2:
                self.mouse_click_pos = (-1,-1)
                if self.i_am ==1:
                    self.suiji_point_1()
                else:
                    self.suiji_point_2()
                self.skip_active = False

    def suiji_point_1(self):
        b= random.randint(1,6)
        for a in self.point_json[str(self.total_info[self.player][13])]["neighbour"]:#a代表玩家相邻点序号
            if self.total_info[str(a)][0] ==0 :#如果玩家相邻点河清海晏
                self.total_info[str(self.total_info[self.player][13])][0]=0
                if len(self.point_json[str(self.total_info[self.player][13])]["neighbour"])==2:#玩家相邻点的个数
                    c=b%2
                    if c==0:
                        self.total_info[self.player][13] = self.point_json[str(self.total_info[self.player][13])]['neighbour'][0]
                    elif c==1:
                        self.total_info[self.player][13] = self.point_json[str(self.total_info[self.player][13])]['neighbour'][1]
                    break
                elif len(self.point_json[str(self.total_info[self.player][13])]["neighbour"])==3:
                    c=b%3
                    if c==0:
                        self.total_info[self.player][13] = self.point_json[str(self.total_info[self.player][13])]['neighbour'][0]
                    elif c==1:
                        self.total_info[self.player][13] = self.point_json[str(self.total_info[self.player][13])]['neighbour'][1]
                    elif c==2:
                        self.total_info[self.player][13] = self.point_json[str(self.total_info[self.player][13])]['neighbour'][2]
                    break
                elif len(self.point_json[str(self.total_info[self.player][13])]["neighbour"])==4:
                    c=b%4
                    if c==0:
                        self.total_info[self.player][13] = self.point_json[str(self.total_info[self.player][13])]['neighbour'][0]
                    elif c==1:
                        self.total_info[self.player][13] = self.point_json[str(self.total_info[self.player][13])]['neighbour'][1]
                    elif c==2:
                        self.total_info[self.player][13] = self.point_json[str(self.total_info[self.player][13])]['neighbour'][2]
                    elif c==3:
                        self.total_info[self.player][13] = self.point_json[str(self.total_info[self.player][13])]['neighbour'][3]
                    break
                elif len(self.point_json[str(self.total_info[self.player][13])]["neighbour"])==5:
                    c=b%5
                    if c==0:
                        self.total_info[self.player][13] = self.point_json[str(self.total_info[self.player][13])]['neighbour'][0]
                    elif c==1:
                        self.total_info[self.player][13] = self.point_json[str(self.total_info[self.player][13])]['neighbour'][1]
                    elif c==2:
                        self.total_info[self.player][13] = self.point_json[str(self.total_info[self.player][13])]['neighbour'][2]
                    elif c==3:
                        self.total_info[self.player][13] = self.point_json[str(self.total_info[self.player][13])]['neighbour'][3]
                    elif c==4:
                        self.total_info[self.player][13] = self.point_json[str(self.total_info[self.player][13])]['neighbour'][4]
                    break
        self.total_info[str(self.total_info[self.player][13])][0]=self.i_am
        self.total_info[self.player][7] -=1
        self.total_info[self.player][12] +=1
        self.skip_active = False

    def suiji_point_2(self):
        b= random.randint(1,6)
        for a in self.point_json[str(self.total_info[self.player][13])]["neighbour"]:#玩家相邻点序号
            if self.total_info[str(a)][0] ==0 :
                self.alter_5(self.total_info[str(self.total_info[self.player][13])],0,0)
                if len(self.point_json[str(self.total_info[self.player][13])]["neighbour"])==2:
                    c=b%2
                    if c==0:
                        self.alter_1(self.player,13,self.point_json[str(self.total_info[self.player][13])]['neighbour'][0])
                    elif c==1:
                        self.alter_1(self.player,13,self.point_json[str(self.total_info[self.player][13])]['neighbour'][1])
                    break
                elif len(self.point_json[str(self.total_info[self.player][13])]["neighbour"])==3:
                    c=b%3
                    if c==0:
                        self.alter_1(self.player,13,self.point_json[str(self.total_info[self.player][13])]['neighbour'][0])
                    elif c==1:
                        self.alter_1(self.player,13,self.point_json[str(self.total_info[self.player][13])]['neighbour'][1])
                    elif c==2:
                        self.alter_1(self.player,13,self.point_json[str(self.total_info[self.player][13])]['neighbour'][2])
                    break
                elif len(self.point_json[str(self.total_info[self.player][13])]["neighbour"])==4:
                    c=b%4
                    if c==0:
                        self.alter_1(self.player,13,self.point_json[str(self.total_info[self.player][13])]['neighbour'][0])
                    elif c==1:
                        self.alter_1(self.player,13,self.point_json[str(self.total_info[self.player][13])]['neighbour'][1])
                    elif c==2:
                        self.alter_1(self.player,13,self.point_json[str(self.total_info[self.player][13])]['neighbour'][2])
                    elif c==3:
                        self.alter_1(self.player,13,self.point_json[str(self.total_info[self.player][13])]['neighbour'][3])
                    break
                elif len(self.point_json[str(self.total_info[self.player][13])]["neighbour"])==5:
                    c=b%5
                    if c==0:
                        self.alter_1(self.player,13,self.point_json[str(self.total_info[self.player][13])]['neighbour'][0])
                    elif c==1:
                        self.alter_1(self.player,13,self.point_json[str(self.total_info[self.player][13])]['neighbour'][1])
                    elif c==2:
                        self.alter_1(self.player,13,self.point_json[str(self.total_info[self.player][13])]['neighbour'][2])
                    elif c==3:
                        self.alter_1(self.player,13,self.point_json[str(self.total_info[self.player][13])]['neighbour'][3])
                    elif c==4:
                        self.alter_1(self.player,13,self.point_json[str(self.total_info[self.player][13])]['neighbour'][4])
                    break
        self.alter_2(str(self.total_info[self.player][13]),0,self.i_am)
        self.alter_4(self.player,7,self.total_info[self.player][7] -1)
        self.alter_3(self.player,12,self.total_info[self.player][12] +1)
        self.skip_active = False

 
    #隐身卡使用
    def _hide_card(self):
        if self.button_hide_dark_new_rect.collidepoint(self.mouse_click_pos) and self.total_info[self.player][6] >0:
            #玩家手里有隐身卡并且点击
            self.hide_active = True
        if self.hide_active:
            self._msg_cancel()
            self._msg_hide()
            if self.msg_hide_image_rect.collidepoint(self.mouse_click_pos):
                if self.i_am==1:
                    self.total_info[self.player][6] -=1#玩家1手卡-1
                    self.total_info[self.player][11] +=1#玩家1使用隐身卡+1
                    self.total_info[str(self.total_info[self.player][13])][0] =8#玩家1于此点隐藏
                    self.total_info[str(self.total_info[self.player][13])][8] =1#玩家1于此点隐藏
                    self.total_info[str(self.total_info[self.player][13])][9] =1#玩家1处于无敌状态
                else:
                    self.alter_1(self.player,6,self.total_info[self.player][6]-1)
                    self.alter_2(self.player,11,self.total_info[self.player][11]+1)
                    self.alter_3(str(self.total_info[self.player][13]),0,8)
                    self.alter_4(str(self.total_info[self.player][13]),8,self.i_am)
                    self.alter_5(str(self.total_info[self.player][13]),9,1)
                self.mouse_click_pos = (-1,-1)
                self.hide_active = False


    #水路卡使用
    def _ship_card(self):
        players = ['player1','player2','player3','player4']
        if self.button_ship_dark_new_rect.collidepoint(self.mouse_click_pos) and self.total_info[self.player][1]>0:
            self.mouse_click_pos = (-1,-1)
            self.click_point = 0
            self.ship_active = True
        if self.ship_active:
            self._msg_ship()
            self._msg_cancel()
            if self.check_neighbour() and self.total_info[str(self.click_point)][0] != 5 and self.total_info[str(self.click_point)][0] != 8 and self.point_json[str(self.total_info[self.player][13])][str(self.click_point)][1] != 0:
                #检查玩家点击的点是否相邻/没被设置为战争状态/没有玩家隐藏
                if  self.total_info[self.player][1] >= self.point_json[str(self.total_info[self.player][13])][str(self.click_point)][1]:
                    #检查玩家相应卡牌是否足够
                    
                    if self.i_am==1:
                        self.total_info[self.player][1] -= self.point_json[str(self.total_info[self.player][13])][str(self.click_point)][1]#玩家1相应卡牌减少
                        self.total_info[self.player][13] = self.click_point#玩家1位置信息更改
                        self.total_info[str(self.click_point)][0] = 1
                        if self.total_info[str(self.click_point)][0] == 6:
                            #如果玩家1到了一个trap
                            self.total_info[self.player][8] += 1#玩家1被trap次数加1
                            self.total_info[str(self.click_point)][0] = 7#点的第一个参数表示玩家陷阱中
                        players.remove(self.player)
                        for k in players:
                            if self.total_info[f'{k}'][13] == self.click_point:
                                #如果玩家1所到处有其他玩家，将玩家撞回原地
                                self.total_info[f'{k}'][13] = self.total_info[f'{k}'][15]
                        self.mouse_click_pos = (-1,-1)
                        self.limit = False
                        self.ship_active = False
                    else:
                        self.alter_1(self.player,1,self.total_info[self.player][1]-self.point_json[str(self.total_info[self.player][13])][str(self.click_point)][1])#玩家234相应卡牌减少
                        self.alter_2(self.player,13,self.click_point)#玩家234位置信息更改
                        self.alter_5(str(self.click_point),0,self.i_am)
                        if self.total_info[str(self.click_point)][0] == 6:
                            #如果玩家234到了一个trap
                            self.alter_3(self.player,8,self.total_info[self.player][8]+1)#玩家234被trap次数加1
                            self.alter_4(str(self.click_point),0,7)#点的第一个参数表示玩家陷阱中
                        players.remove(self.player)
                        for k in players:
                            if self.total_info[f'{k}'][13] == self.click_point:
                                #如果玩家234所到处有其他玩家，将玩家撞回原地
                                self.alter_4(f'{k}',13,self.total_info[f'{k}'][15])
                        self.mouse_click_pos = (-1,-1)
                        self.limit = False
                        self.ship_active = False
                        
    
    #铁路卡使用
    def _railway_card(self):
        players = ['player1','player2','player3','player4']
        if self.button_railway_dark_new_rect.collidepoint(self.mouse_click_pos) and self.total_info[self.player][2]>0:
            self.mouse_click_pos = (-1,-1)
            self.click_point = 0
            #print(12)
            self.railway_active = True
        if self.railway_active:
            #print(34)
            self._msg_railway()
            self._msg_cancel()
            if self.check_neighbour() and self.total_info[str(self.click_point)][0] != 5 and self.total_info[str(self.click_point)][0] != 8 and self.point_json[str(self.total_info[self.player][13])][str(self.click_point)][0] != 0:
                #print(56)
                #检查玩家点击的点是否相邻/没被设置为战争状态/没有玩家隐藏
                if  self.total_info[self.player][2] >= self.point_json[str(self.total_info[self.player][13])][str(self.click_point)][0]:
                    #print(78)
                    #检查玩家相应卡牌是否足够
                    
                    if self.i_am==1:
                        self.total_info[self.player][2] -= self.point_json[str(self.total_info[self.player][13])][str(self.click_point)][0]#玩家1相应卡牌减少
                        self.total_info[self.player][13] = self.click_point#玩家1位置信息更改
                        self.total_info[str(self.click_point)][0] = 1
                        if self.total_info[str(self.click_point)][0] == 6:
                            #如果玩家1到了一个trap
                            self.total_info[self.player][8] += 1#玩家1被trap次数加1
                            self.total_info[str(self.click_point)][0] = 7#点的第一个参数表示玩家陷阱中
                        players.remove(self.player)
                        for k in players:
                            if self.total_info[f'{k}'][13] == self.click_point:
                                #如果玩家1所到处有其他玩家，将玩家撞回原地
                                self.total_info[f'{k}'][13] = self.total_info[f'{k}'][15]
                        #print(87)
                        self.mouse_click_pos = (-1,-1)
                        self.limit = False
                        self.railway_active = False
                    else:
                        self.alter_1(self.player,2,self.total_info[self.player][2]-self.point_json[str(self.total_info[self.player][13])][str(self.click_point)][0])#玩家234相应卡牌减少
                        self.alter_2(self.player,13,self.click_point)#玩家234位置信息更改
                        self.alter_5(str(self.click_point),0,self.i_am)
                        if self.total_info[str(self.click_point)][0] == 6:
                            #如果玩家234到了一个trap
                            self.alter_3(self.player,8,self.total_info[self.player][8]+1)#玩家234被trap次数加1
                            self.alter_4(str(self.click_point),0,7)#点的第一个参数表示玩家陷阱中
                        players.remove(self.player)
                        for k in players:
                            if self.total_info[f'{k}'][13] == self.click_point:
                                #如果玩家234所到处有其他玩家，将玩家撞回原地
                                self.alter_4(f'{k}',13,self.total_info[f'{k}'][15])
                        self.mouse_click_pos = (-1,-1)
                        self.limit = False
                        self.railway_active = False
                        

    #公路卡使用
    def _road_card(self):
        players = ['player1','player2','player3','player4']
        if self.button_road_dark_new_rect.collidepoint(self.mouse_click_pos) and self.total_info[self.player][3]>0:
            self.mouse_click_pos = (-1,-1)
            self.click_point = 0
            self.road_active = True
            #print(5)
        if self.road_active:
            self._msg_road()
            self._msg_cancel()
            #print(6)
            if self.check_neighbour() and self.total_info[str(self.click_point)][0] != 5 and self.total_info[str(self.click_point)][0] != 8 and self.point_json[str(self.total_info[self.player][13])][str(self.click_point)][2] != 0:
                #print(7)
                #检查玩家点击的点是否相邻/没被设置为战争状态/没有玩家隐藏
                if  self.total_info[self.player][3] >= self.point_json[str(self.total_info[self.player][13])][str(self.click_point)][2]:
                    #检查玩家相应卡牌是否足够
                    
                    if self.i_am==1:
                        self.total_info[self.player][3] -= self.point_json[str(self.total_info[self.player][13])][str(self.click_point)][2]#玩家1相应卡牌减少
                        self.total_info[self.player][13] = self.click_point#玩家1位置信息更改
                        self.total_info[str(self.click_point)][0] = 1
                        if self.total_info[str(self.click_point)][0] == 6:
                            #如果玩家1到了一个trap
                            self.total_info[self.player][8] += 1#玩家1被trap次数加1
                            self.total_info[str(self.click_point)][0] = 7#点的第一个参数表示玩家陷阱中
                        players.remove(self.player)
                        for k in players:
                            if self.total_info[f'{k}'][13] == self.click_point:
                                #如果玩家1所到处有其他玩家，将玩家撞回原地
                                self.total_info[f'{k}'][13] = self.total_info[f'{k}'][15]
                                self.mouse_click_pos = (-1,-1)
                        self.limit = False
                        self.road_active = False
                    else:
                        self.alter_1(self.player,3,self.total_info[self.player][3]-self.point_json[str(self.total_info[self.player][13])][str(self.click_point)][2])#玩家234相应卡牌减少
                        self.alter_2(self.player,13,self.click_point)#玩家234位置信息更改
                        self.alter_5(str(self.click_point),0,self.i_am)                    
                        if self.total_info[str(self.click_point)][0] == 6:
                            #如果玩家234到了一个trap
                            self.alter_3(self.player,8,self.total_info[self.player][8]+1)#玩家234被trap次数加1
                            self.alter_4(str(self.click_point),0,7)#点的第一个参数表示玩家陷阱中
                        players.remove(self.player)
                        for k in players:
                            if self.total_info[f'{k}'][13] == self.click_point:
                                #如果玩家234所到处有其他玩家，将玩家撞回原地
                                self.alter_4(f'{k}',13,self.total_info[f'{k}'][15])
                        self.mouse_click_pos = (-1,-1)
                        self.limit = False
                        self.road_active = False
                        




#在1到45个点中
#第一个参数，0表示空，1，2，3，4表示玩家，5表示战争点，6表示陷阱点，7表示玩家在陷阱中，8表示玩家在隐藏中
#第二个参数，点处于war状态触发，0表示无法设置战争点，3表示战争状态还剩3回合，4表示可放置战争点
#第三个参数，点处于trap状态触发，0表示该点没有trap
#第4，5，6，7个参数，表示是玩家1，2，3，4设置
#第8个参数，表示玩家1,2,3,4被trap
#第9个参数，表示玩家1,2,3,4于此点隐藏
#第10个参数，表示玩家是否hide，无敌状态

#player里面，数字依次表示money(0),ship_card(1),railway_card(2),road_card(3),war_card(4)
#trap_card(5),hide_card(6),skip_card(7),被trap时间(8),使用trap次数(9),使用war次数(10),使用hide次数(11)
#使用skip次数(12),起点(13),终点(14)
#----------------------------------------------------------message------------------------------------
    #隐身卡提示信息
    def _msg_hide(self):
        msg_hide = str("Click here to confirm use.")
        self.msg_hide_image = self.font.render(msg_hide,True,
                                          (0,0,0))
        self.msg_hide_image_rect = self.msg_hide_image.get_rect()
        self.msg_hide_image_rect.x += int(367*self.settings.RATIO_ALL)
        self.msg_hide_image_rect.y += int(74.815*self.settings.RATIO_ALL)
        self.screen.blit(self.msg_hide_image,(367*self.settings.RATIO_ALL,74.815*self.settings.RATIO_ALL))
    #战争卡提示信息
    def _msg_war(self):
        msg_war = str("Please select a point ")
        self.tip_image = self.font.render(msg_war,True,
                                          (0,0,0))
        self.screen.blit(self.tip_image,(367*self.settings.RATIO_ALL,14.815*self.settings.RATIO_ALL))
        msg_war = str("as the war point.")
        self.tip_image = self.font.render(msg_war,True,
                                          (0,0,0))
        self.screen.blit(self.tip_image,(367*self.settings.RATIO_ALL,74.815*self.settings.RATIO_ALL))
    #陷阱卡提示信息       
    def _msg_trap(self):
        msg_trap_1 = str("Please select a point")
        self.msg_trap_1_image = self.font.render(msg_trap_1,True,
                                          (0,0,0))
        self.screen.blit(self.msg_trap_1_image,(367*self.settings.RATIO_ALL,14.815*self.settings.RATIO_ALL))
        msg_trap_2 = str("as the trap point.")
        self.msg_trap_2_image = self.font.render(msg_trap_2,True,
                                          (0,0,0))
        self.screen.blit(self.msg_trap_2_image,(367*self.settings.RATIO_ALL,74.815*self.settings.RATIO_ALL))
    #跃迁卡提示信息
    def _msg_skip(self):
        msg_skip = str("Click here to confirm use.")
        self.msg_skip_image = self.font.render(msg_skip,True,
                                          (0,0,0))
        self.msg_skip_image_rect = self.msg_skip_image.get_rect()
        self.msg_skip_image_rect.x += int(367*self.settings.RATIO_ALL)
        self.msg_skip_image_rect.y += int(74.815*self.settings.RATIO_ALL)
        self.screen.blit(self.msg_skip_image,(367*self.settings.RATIO_ALL,74.815*self.settings.RATIO_ALL))


    #铁路票提示信息
    def _msg_railway(self):
        msg_railway = str("Please select a point as ")
        self.msg_railway_image = self.font.render(msg_railway,True,
                                          (0,0,0))

        self.screen.blit(self.msg_railway_image,(367*self.settings.RATIO_ALL,14.815*self.settings.RATIO_ALL))
        msg_railway = str("the destination of the railway.")
        self.msg_railway_image = self.font.render(msg_railway,True,
                                          (0,0,0))

        self.screen.blit(self.msg_railway_image,(367*self.settings.RATIO_ALL,74.815*self.settings.RATIO_ALL))
    #水路票提示提示
    def _msg_ship(self):
        msg_ship = str("Please select a point as ")
        self.msg_ship_image = self.font.render(msg_ship,True,
                                          (0,0,0))

        self.screen.blit(self.msg_ship_image,(367*self.settings.RATIO_ALL,14.815*self.settings.RATIO_ALL))
        msg_ship = str("the destination of the ship.")
        self.msg_ship_image = self.font.render(msg_ship,True,
                                          (0,0,0))

        self.screen.blit(self.msg_ship_image,(367*self.settings.RATIO_ALL,74.815*self.settings.RATIO_ALL))
        #print(234567890)
    #公路票提示信息
    def _msg_road(self):
        msg_road = str("Please select a point as ")
        self.msg_road_image = self.font.render(msg_road,True,
                                          (0,0,0))

        self.screen.blit(self.msg_road_image,(367*self.settings.RATIO_ALL,14.815*self.settings.RATIO_ALL))
        msg_road = str("the destination of the road.")
        self.msg_road_image = self.font.render(msg_road,True,
                                          (0,0,0))

        self.screen.blit(self.msg_road_image,(367*self.settings.RATIO_ALL,74.815*self.settings.RATIO_ALL))

    #取消使用
    def _msg_cancel(self):
        if self.button_cancel_dark_new_rect.collidepoint(self.mouse_click_pos):
            self.war_active = False
            self.trap_active = False
            self.skip_active = False
            self.hide_active = False
            self.ship_active = False
            self.road_active = False
            self.railway_active = False
        if self.war_active:
            self.trap_active = False
            self.skip_active = False
            self.hide_active = False
            self.ship_active = False
            self.road_active = False
            self.railway_active = False
        elif self.trap_active:
            self.war_active = False
            self.skip_active = False
            self.hide_active = False
            self.ship_active = False
            self.road_active = False
            self.railway_active = False
        elif self.skip_active:
            self.war_active = False
            self.trap_active = False
            self.hide_active = False
            self.ship_active = False
            self.road_active = False
            self.railway_active = False
        elif self.hide_active:
            self.war_active = False
            self.trap_active = False
            self.skip_active = False
            self.ship_active = False
            self.road_active = False
            self.railway_active = False
        elif self.ship_active:
            self.war_active = False
            self.trap_active = False
            self.skip_active = False
            self.hide_active = False
            self.road_active = False
            self.railway_active = False
        elif self.road_active:
            self.war_active = False
            self.trap_active = False
            self.skip_active = False
            self.hide_active = False
            self.ship_active = False
            self.railway_active = False
        elif self.railway_active:
            self.war_active = False
            self.trap_active = False
            self.skip_active = False
            self.hide_active = False
            self.ship_active = False
            self.road_active = False







    def come_back(self):
        # self.total_info['round&client_number&time'][0] +=1
        self.total_info[self.player][0] += 100
        for i in range(1,47):
            if self.total_info[str(f'{i}')][0] == 5:
                self.total_info[str(f'{i}')][1] -= 1 
                if self.total_info[str(f'{i}')][1] ==0:
                    self.total_info[str(f'{i}')][0] = 0           #天下太平
            if self.total_info[str(f'{i}')][0] == 7:
                self.total_info[str(f'{i}')][2] -= 1
                if self.total_info[str(f'{i}')][2] == 0:
                    self.total_info[str(f'{i}')][0] = self.i_am   #刑满释放
            if self.total_info[str(f'{i}')][10]>=0:
                self.total_info[str(f'{i}')][10] -= 1
                if self.total_info[str(f'{i}')][10] ==0:
                    self.total_info[str(f'{i}')][0] = self.i_am   #原形毕露

#------------------------------------------------------message----------------------
    #检查点击点是否与玩家相邻
    def check_neighbour(self):
        """检查玩家所在点与玩家点击点是否相邻"""
        a = self.total_info[self.player][13]#玩家所在点
        b = self.click_point #玩家点击的点的序号
        if b in self.point_json[str(f'{a}')]['neighbour']:
            return True
        else:
            return False
        
    #玩家点击的点的序号
    def click_point_number(self):
        if self.point_1_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 1
            self.mouse_click_pos = (-1,-1)
        elif self.point_2_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 2
            self.mouse_click_pos = (-1,-1)
        elif self.point_3_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 3
            self.mouse_click_pos = (-1,-1)
        elif self.point_4_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 4
            self.mouse_click_pos = (-1,-1)
        elif self.point_5_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 5
            self.mouse_click_pos = (-1,-1)
        elif self.point_6_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 6
            self.mouse_click_pos = (-1,-1)
        elif self.point_7_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 7
            self.mouse_click_pos = (-1,-1)
        elif self.point_8_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 8
            self.mouse_click_pos = (-1,-1)
        elif self.point_9_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 9
            self.mouse_click_pos = (-1,-1)
        elif self.point_10_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 10
            self.mouse_click_pos = (-1,-1)
        elif self.point_11_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 11
            self.mouse_click_pos = (-1,-1)
        elif self.point_12_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 12
            self.mouse_click_pos = (-1,-1)
        elif self.point_13_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 13
            self.mouse_click_pos = (-1,-1)
        elif self.point_14_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 14
            self.mouse_click_pos = (-1,-1)
        elif self.point_15_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 15
            self.mouse_click_pos = (-1,-1)
        elif self.point_16_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 16
            self.mouse_click_pos = (-1,-1)
        elif self.point_17_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 17
            self.mouse_click_pos = (-1,-1)
        elif self.point_18_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 18
            self.mouse_click_pos = (-1,-1)
        elif self.point_19_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 19
            self.mouse_click_pos = (-1,-1)
        elif self.point_20_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 20
            self.mouse_click_pos = (-1,-1)
        elif self.point_21_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 21
            self.mouse_click_pos = (-1,-1)
        elif self.point_22_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 22
            self.mouse_click_pos = (-1,-1)
        elif self.point_23_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 23
            self.mouse_click_pos = (-1,-1)
        elif self.point_24_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 24
            self.mouse_click_pos = (-1,-1)
        elif self.point_25_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 25
            self.mouse_click_pos = (-1,-1)
        elif self.point_26_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 26
            self.mouse_click_pos = (-1,-1)
        elif self.point_27_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 27
            self.mouse_click_pos = (-1,-1)
        elif self.point_28_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 28
            self.mouse_click_pos = (-1,-1)
        elif self.point_29_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 29
            self.mouse_click_pos = (-1,-1)
        elif self.point_30_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 30
            self.mouse_click_pos = (-1,-1)
        elif self.point_31_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 31
            self.mouse_click_pos = (-1,-1)
        elif self.point_32_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 32
            self.mouse_click_pos = (-1,-1)
        elif self.point_33_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 33
            self.mouse_click_pos = (-1,-1)
        elif self.point_34_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 34
            self.mouse_click_pos = (-1,-1)
        elif self.point_35_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 35
            self.mouse_click_pos = (-1,-1)
        elif self.point_36_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 36
            self.mouse_click_pos = (-1,-1)
        elif self.point_37_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 37
            self.mouse_click_pos = (-1,-1)
        elif self.point_38_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 38
            self.mouse_click_pos = (-1,-1)
        elif self.point_39_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 39
            self.mouse_click_pos = (-1,-1)
        elif self.point_40_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 40
            self.mouse_click_pos = (-1,-1)
        elif self.point_41_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 41
            self.mouse_click_pos = (-1,-1)
        elif self.point_42_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 42
            self.mouse_click_pos = (-1,-1)
        elif self.point_43_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 43
            self.mouse_click_pos = (-1,-1)
        elif self.point_44_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 44
            self.mouse_click_pos = (-1,-1)
        elif self.point_45_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 45
            self.mouse_click_pos = (-1,-1)
        elif self.point_46_new_rect.collidepoint(self.mouse_click_pos):
            self.click_point = 46
            self.mouse_click_pos = (-1,-1)

    #玩家走动后原位置点的清算
    def reset(self):
        #如果玩家现在所在的点不是此点，此点第1个参数却还保留1234的属性，则此属性更改为0
        for i in range(1,47):
            if self.total_info['player1'][13] != i and self.total_info['player2'][13] != i and self.total_info['player3'][13] != i and self.total_info['player4'][13] != i:
                if self.total_info[f'{i}'][0]==1 or self.total_info[f'{i}'][0]==2 or self.total_info[f'{i}'][0]==3 or self.total_info[f'{i}'][0]==4:
                    self.total_info[f'{i}'][0] = 0
            if self.total_info[f'{i}'][3] + self.total_info[f'{i}'][4] + self.total_info[f'{i}'][5] + self.total_info[f'{i}'][6] != 0:
                #self.total_info[f'{i}'][2] = 1
                if self.total_info['player1'][13] != i and self.total_info['player2'][13] != i and self.total_info['player3'][13] != i and self.total_info['player4'][13] != i:
                    self.total_info[f'{i}'][0] = 6
                    self.total_info[f'{i}'][2] = self.total_info[f'{i}'][3] + self.total_info[f'{i}'][4] + self.total_info[f'{i}'][5] + self.total_info[f'{i}'][6]
            if self.total_info[f'{i}'][2] != 0 and (self.total_info['player1'][13] == i or self.total_info['player2'][13] == i or self.total_info['player3'][13] == i or self.total_info['player4'][13] == i) and ( self.total_info[f'{i}'][3] + self.total_info[f'{i}'][4] + self.total_info[f'{i}'][5] + self.total_info[f'{i}'][6] != 0):
                self.total_info[f'{i}'][0] = 7
            
            if self.total_info[f'{i}'][0] == 7 and self.total_info[f'{i}'][2] != 0:
                #print("trap_2")
                if self.total_info['player1'][13] == i:
                    #print("trap_3")
                    self.total_info[f'{i}'][7] = 1
                elif self.total_info['player2'][13] == i:
                    #print("trap_3")
                    self.total_info[f'{i}'][7] = 2
                elif self.total_info['player3'][13] == i:
                    #print("trap_3")
                    self.total_info[f'{i}'][7] = 3
                elif self.total_info['player4'][13] == i:
                    #print("trap_3")
                    self.total_info[f'{i}'][7] = 4

    #玩家到达目的地后结束游戏
    def finale(self):
        players = ['player1','player2','player3','player4']
        for player in players:
            if self.total_info[f'{player}'][13]==self.total_info[f'{player}'][14]:
                self.game_active_6 = False
                if player == "player1":
                    self.total_info["round&client_number&time"][4] = 1
                elif player == "player2":
                    self.total_info["round&client_number&time"][4] = 2
                elif player == "player3":
                    self.total_info["round&client_number&time"][4] = 3
                elif player == "player4":
                    self.total_info["round&client_number&time"][4] = 4
                self.game_active_8 = True

#大战界面数据
    def dazhan_shuju(self):
        if self.i_am == 1:

            dj_player_1_railway = str(self.total_info["player1"][2])
            self.dj_player_1_railway_image = self.font.render(dj_player_1_railway,True,
                                                (0,0,0))
            self.dj_player_1_railway_image_rect = self.dj_player_1_railway_image.get_rect()
            self.dj_player_1_railway_image_rect.x += self.number_json["main"]["player1_railway"][0]
            self.dj_player_1_railway_image_rect.y += self.number_json["main"]["player1_railway"][1]
            self.screen.blit(self.dj_player_1_railway_image,self.dj_player_1_railway_image_rect)

            dj_player_1_ship = str(self.total_info["player1"][1])
            self.dj_player_1_ship_image = self.font.render(dj_player_1_ship,True,
                                                (0,0,0))
            self.dj_player_1_ship_image_rect = self.dj_player_1_ship_image.get_rect()
            self.dj_player_1_ship_image_rect.x += self.number_json["main"]["player1_ship"][0]
            self.dj_player_1_ship_image_rect.y += self.number_json["main"]["player1_ship"][1]
            self.screen.blit(self.dj_player_1_ship_image,self.dj_player_1_ship_image_rect)

            dj_player_1_road = str(self.total_info["player1"][3])
            self.dj_player_1_road_image = self.font.render(dj_player_1_road,True,
                                                (0,0,0))
            self.dj_player_1_road_image_rect = self.dj_player_1_road_image.get_rect()
            self.dj_player_1_road_image_rect.x += self.number_json["main"]["player1_road"][0]
            self.dj_player_1_road_image_rect.y += self.number_json["main"]["player1_road"][1]
            self.screen.blit(self.dj_player_1_road_image,self.dj_player_1_road_image_rect)

            dj_player_1_money = str(self.total_info["player1"][0])
            self.dj_player_1_money_image = self.font.render(dj_player_1_money,True,
                                                (234,192,38))
            self.dj_player_1_money_image_rect = self.dj_player_1_money_image.get_rect()
            self.dj_player_1_money_image_rect.x += self.number_json["main"]["player1_money"][0]
            self.dj_player_1_money_image_rect.y += self.number_json["main"]["player1_money"][1]
            self.screen.blit(self.dj_player_1_money_image,self.dj_player_1_money_image_rect)

            dj_player_1_trap = str(self.total_info["player1"][5])
            self.dj_player_1_trap_image = self.font.render(dj_player_1_trap,True,
                                                (0,0,0))
            self.dj_player_1_trap_image_rect = self.dj_player_1_trap_image.get_rect()
            self.dj_player_1_trap_image_rect.x += self.number_json["main"]["player1_trap"][0]
            self.dj_player_1_trap_image_rect.y += self.number_json["main"]["player1_trap"][1]
            self.screen.blit(self.dj_player_1_trap_image,self.dj_player_1_trap_image_rect)

            dj_player_1_war = str(self.total_info["player1"][4])
            self.dj_player_1_war_image = self.font.render(dj_player_1_war,True,
                                                (0,0,0))
            self.dj_player_1_war_image_rect = self.dj_player_1_war_image.get_rect()
            self.dj_player_1_war_image_rect.x += self.number_json["main"]["player1_war"][0]
            self.dj_player_1_war_image_rect.y += self.number_json["main"]["player1_war"][1]
            self.screen.blit(self.dj_player_1_war_image,self.dj_player_1_war_image_rect)

            dj_player_1_skip = str(self.total_info["player1"][7])
            self.dj_player_1_skip_image = self.font.render(dj_player_1_skip,True,
                                                (0,0,0))
            self.dj_player_1_skip_image_rect = self.dj_player_1_skip_image.get_rect()
            self.dj_player_1_skip_image_rect.x += self.number_json["main"]["player1_skip"][0]
            self.dj_player_1_skip_image_rect.y += self.number_json["main"]["player1_skip"][1]
            self.screen.blit(self.dj_player_1_skip_image,self.dj_player_1_skip_image_rect)

            dj_player_1_hide = str(self.total_info["player1"][6])
            self.dj_player_1_hide_image = self.font.render(dj_player_1_hide,True,
                                                (0,0,0))
            self.dj_player_1_hide_image_rect = self.dj_player_1_hide_image.get_rect()
            self.dj_player_1_hide_image_rect.x += self.number_json["main"]["player1_hide"][0]
            self.dj_player_1_hide_image_rect.y += self.number_json["main"]["player1_hide"][1]
            self.screen.blit(self.dj_player_1_hide_image,self.dj_player_1_hide_image_rect)



            if self.game_active_7 == False:
                dj_player_2_railway = str(self.total_info["player2"][2])
                self.dj_player_2_railway_image = self.font.render(dj_player_2_railway,True,
                                                    (0,0,0))
                self.dj_player_2_railway_image_rect = self.dj_player_2_railway_image.get_rect()
                self.dj_player_2_railway_image_rect.x += self.number_json["main"]["player2_railway"][0]
                self.dj_player_2_railway_image_rect.y += self.number_json["main"]["player2_railway"][1]
                self.screen.blit(self.dj_player_2_railway_image,self.dj_player_2_railway_image_rect)

                dj_player_2_ship = str(self.total_info["player2"][1])
                self.dj_player_2_ship_image = self.font.render(dj_player_2_ship,True,
                                                    (0,0,0))
                self.dj_player_2_ship_image_rect = self.dj_player_2_ship_image.get_rect()
                self.dj_player_2_ship_image_rect.x += self.number_json["main"]["player2_ship"][0]
                self.dj_player_2_ship_image_rect.y += self.number_json["main"]["player2_ship"][1]
                self.screen.blit(self.dj_player_2_ship_image,self.dj_player_2_ship_image_rect)

                dj_player_2_road = str(self.total_info["player2"][3])
                self.dj_player_2_road_image = self.font.render(dj_player_2_road,True,
                                                    (0,0,0))
                self.dj_player_2_road_image_rect = self.dj_player_2_road_image.get_rect()
                self.dj_player_2_road_image_rect.x += self.number_json["main"]["player2_road"][0]
                self.dj_player_2_road_image_rect.y += self.number_json["main"]["player2_road"][1]
                self.screen.blit(self.dj_player_2_road_image,self.dj_player_2_road_image_rect)

                dj_player_2_money = str(self.total_info["player2"][0])
                self.dj_player_2_money_image = self.font_3.render(dj_player_2_money,True,
                                                    (234,192,38))
                self.dj_player_2_money_image_rect = self.dj_player_2_money_image.get_rect()
                self.dj_player_2_money_image_rect.x += self.number_json["main"]["player2_money"][0]
                self.dj_player_2_money_image_rect.y += self.number_json["main"]["player2_money"][1]
                self.screen.blit(self.dj_player_2_money_image,self.dj_player_2_money_image_rect)
                
                    
                dj_player_3_railway = str(self.total_info["player3"][2])
                self.dj_player_3_railway_image = self.font.render(dj_player_3_railway,True,
                                                    (0,0,0))
                self.dj_player_3_railway_image_rect = self.dj_player_3_railway_image.get_rect()
                self.dj_player_3_railway_image_rect.x += self.number_json["main"]["player3_railway"][0]
                self.dj_player_3_railway_image_rect.y += self.number_json["main"]["player3_railway"][1]
                self.screen.blit(self.dj_player_3_railway_image,self.dj_player_3_railway_image_rect)

                dj_player_3_ship = str(self.total_info["player3"][1])
                self.dj_player_3_ship_image = self.font.render(dj_player_3_ship,True,
                                                    (0,0,0))
                self.dj_player_3_ship_image_rect = self.dj_player_3_ship_image.get_rect()
                self.dj_player_3_ship_image_rect.x += self.number_json["main"]["player3_ship"][0]
                self.dj_player_3_ship_image_rect.y += self.number_json["main"]["player3_ship"][1]
                self.screen.blit(self.dj_player_3_ship_image,self.dj_player_3_ship_image_rect)

                dj_player_3_road = str(self.total_info["player3"][3])
                self.dj_player_3_road_image = self.font.render(dj_player_3_road,True,
                                                    (0,0,0))
                self.dj_player_3_road_image_rect = self.dj_player_3_road_image.get_rect()
                self.dj_player_3_road_image_rect.x += self.number_json["main"]["player3_road"][0]
                self.dj_player_3_road_image_rect.y += self.number_json["main"]["player3_road"][1]
                self.screen.blit(self.dj_player_3_road_image,self.dj_player_3_road_image_rect)

                dj_player_3_money = str(self.total_info["player3"][0])
                self.dj_player_3_money_image = self.font_3.render(dj_player_3_money,True,
                                                    (234,192,38))
                self.dj_player_3_money_image_rect = self.dj_player_3_money_image.get_rect()
                self.dj_player_3_money_image_rect.x += self.number_json["main"]["player3_money"][0]
                self.dj_player_3_money_image_rect.y += self.number_json["main"]["player3_money"][1]
                self.screen.blit(self.dj_player_3_money_image,self.dj_player_3_money_image_rect)

                        
                dj_player_4_railway = str(self.total_info["player4"][2])
                self.dj_player_4_railway_image = self.font.render(dj_player_4_railway,True,
                                                    (0,0,0))
                self.dj_player_4_railway_image_rect = self.dj_player_4_railway_image.get_rect()
                self.dj_player_4_railway_image_rect.x += self.number_json["main"]["player4_railway"][0]
                self.dj_player_4_railway_image_rect.y += self.number_json["main"]["player4_railway"][1]
                self.screen.blit(self.dj_player_4_railway_image,self.dj_player_4_railway_image_rect)

                dj_player_4_ship = str(self.total_info["player4"][1])
                self.dj_player_4_ship_image = self.font.render(dj_player_4_ship,True,
                                                    (0,0,0))
                self.dj_player_4_ship_image_rect = self.dj_player_4_ship_image.get_rect()
                self.dj_player_4_ship_image_rect.x += self.number_json["main"]["player4_ship"][0]
                self.dj_player_4_ship_image_rect.y += self.number_json["main"]["player4_ship"][1]
                self.screen.blit(self.dj_player_4_ship_image,self.dj_player_4_ship_image_rect)

                dj_player_4_road = str(self.total_info["player4"][3])
                self.dj_player_4_road_image = self.font.render(dj_player_4_road,True,
                                                    (0,0,0))
                self.dj_player_4_road_image_rect = self.dj_player_4_road_image.get_rect()
                self.dj_player_4_road_image_rect.x += self.number_json["main"]["player4_road"][0]
                self.dj_player_4_road_image_rect.y += self.number_json["main"]["player4_road"][1]
                self.screen.blit(self.dj_player_4_road_image,self.dj_player_4_road_image_rect)

                dj_player_4_money = str(self.total_info["player4"][0])
                self.dj_player_4_money_image = self.font_3.render(dj_player_4_money,True,
                                                    (234,192,38))
                self.dj_player_4_money_image_rect = self.dj_player_4_money_image.get_rect()
                self.dj_player_4_money_image_rect.x += self.number_json["main"]["player4_money"][0]
                self.dj_player_4_money_image_rect.y += self.number_json["main"]["player4_money"][1]
                self.screen.blit(self.dj_player_4_money_image,self.dj_player_4_money_image_rect)

        if self.i_am == 2:
            dj_player_1_railway = str(self.total_info["player2"][2])
            self.dj_player_1_railway_image = self.font.render(dj_player_1_railway,True,
                                                (0,0,0))
            self.dj_player_1_railway_image_rect = self.dj_player_1_railway_image.get_rect()
            self.dj_player_1_railway_image_rect.x += self.number_json["main"]["player1_railway"][0]
            self.dj_player_1_railway_image_rect.y += self.number_json["main"]["player1_railway"][1]
            self.screen.blit(self.dj_player_1_railway_image,self.dj_player_1_railway_image_rect)

            dj_player_1_ship = str(self.total_info["player2"][1])
            self.dj_player_1_ship_image = self.font.render(dj_player_1_ship,True,
                                                (0,0,0))
            self.dj_player_1_ship_image_rect = self.dj_player_1_ship_image.get_rect()
            self.dj_player_1_ship_image_rect.x += self.number_json["main"]["player1_ship"][0]
            self.dj_player_1_ship_image_rect.y += self.number_json["main"]["player1_ship"][1]
            self.screen.blit(self.dj_player_1_ship_image,self.dj_player_1_ship_image_rect)

            dj_player_1_road = str(self.total_info["player2"][3])
            self.dj_player_1_road_image = self.font.render(dj_player_1_road,True,
                                                (0,0,0))
            self.dj_player_1_road_image_rect = self.dj_player_1_road_image.get_rect()
            self.dj_player_1_road_image_rect.x += self.number_json["main"]["player1_road"][0]
            self.dj_player_1_road_image_rect.y += self.number_json["main"]["player1_road"][1]
            self.screen.blit(self.dj_player_1_road_image,self.dj_player_1_road_image_rect)

            dj_player_1_money = str(self.total_info["player2"][0])
            self.dj_player_1_money_image = self.font.render(dj_player_1_money,True,
                                                (234,192,38))
            self.dj_player_1_money_image_rect = self.dj_player_1_money_image.get_rect()
            self.dj_player_1_money_image_rect.x += self.number_json["main"]["player1_money"][0]
            self.dj_player_1_money_image_rect.y += self.number_json["main"]["player1_money"][1]
            self.screen.blit(self.dj_player_1_money_image,self.dj_player_1_money_image_rect)

            dj_player_1_trap = str(self.total_info["player2"][5])
            self.dj_player_1_trap_image = self.font.render(dj_player_1_trap,True,
                                                (0,0,0))
            self.dj_player_1_trap_image_rect = self.dj_player_1_trap_image.get_rect()
            self.dj_player_1_trap_image_rect.x += self.number_json["main"]["player1_trap"][0]
            self.dj_player_1_trap_image_rect.y += self.number_json["main"]["player1_trap"][1]
            self.screen.blit(self.dj_player_1_trap_image,self.dj_player_1_trap_image_rect)

            dj_player_1_war = str(self.total_info["player2"][4])
            self.dj_player_1_war_image = self.font.render(dj_player_1_war,True,
                                                (0,0,0))
            self.dj_player_1_war_image_rect = self.dj_player_1_war_image.get_rect()
            self.dj_player_1_war_image_rect.x += self.number_json["main"]["player1_war"][0]
            self.dj_player_1_war_image_rect.y += self.number_json["main"]["player1_war"][1]
            self.screen.blit(self.dj_player_1_war_image,self.dj_player_1_war_image_rect)

            dj_player_1_skip = str(self.total_info["player2"][7])
            self.dj_player_1_skip_image = self.font.render(dj_player_1_skip,True,
                                                (0,0,0))
            self.dj_player_1_skip_image_rect = self.dj_player_1_skip_image.get_rect()
            self.dj_player_1_skip_image_rect.x += self.number_json["main"]["player1_skip"][0]
            self.dj_player_1_skip_image_rect.y += self.number_json["main"]["player1_skip"][1]
            self.screen.blit(self.dj_player_1_skip_image,self.dj_player_1_skip_image_rect)

            dj_player_1_hide = str(self.total_info["player2"][6])
            self.dj_player_1_hide_image = self.font.render(dj_player_1_hide,True,
                                                (0,0,0))
            self.dj_player_1_hide_image_rect = self.dj_player_1_hide_image.get_rect()
            self.dj_player_1_hide_image_rect.x += self.number_json["main"]["player1_hide"][0]
            self.dj_player_1_hide_image_rect.y += self.number_json["main"]["player1_hide"][1]
            self.screen.blit(self.dj_player_1_hide_image,self.dj_player_1_hide_image_rect)

            if self.game_active_7 == False:
                dj_player_2_railway = str(self.total_info["player3"][2])
                self.dj_player_2_railway_image = self.font.render(dj_player_2_railway,True,
                                                    (0,0,0))
                self.dj_player_2_railway_image_rect = self.dj_player_2_railway_image.get_rect()
                self.dj_player_2_railway_image_rect.x += self.number_json["main"]["player2_railway"][0]
                self.dj_player_2_railway_image_rect.y += self.number_json["main"]["player2_railway"][1]
                self.screen.blit(self.dj_player_2_railway_image,self.dj_player_2_railway_image_rect)

                dj_player_2_ship = str(self.total_info["player3"][1])
                self.dj_player_2_ship_image = self.font.render(dj_player_2_ship,True,
                                                    (0,0,0))
                self.dj_player_2_ship_image_rect = self.dj_player_2_ship_image.get_rect()
                self.dj_player_2_ship_image_rect.x += self.number_json["main"]["player2_ship"][0]
                self.dj_player_2_ship_image_rect.y += self.number_json["main"]["player2_ship"][1]
                self.screen.blit(self.dj_player_2_ship_image,self.dj_player_2_ship_image_rect)

                dj_player_2_road = str(self.total_info["player3"][3])
                self.dj_player_2_road_image = self.font.render(dj_player_2_road,True,
                                                    (0,0,0))
                self.dj_player_2_road_image_rect = self.dj_player_2_road_image.get_rect()
                self.dj_player_2_road_image_rect.x += self.number_json["main"]["player2_road"][0]
                self.dj_player_2_road_image_rect.y += self.number_json["main"]["player2_road"][1]
                self.screen.blit(self.dj_player_2_road_image,self.dj_player_2_road_image_rect)

                dj_player_2_money = str(self.total_info["player3"][0])
                self.dj_player_2_money_image = self.font_3.render(dj_player_2_money,True,
                                                    (234,192,38))
                self.dj_player_2_money_image_rect = self.dj_player_2_money_image.get_rect()
                self.dj_player_2_money_image_rect.x += self.number_json["main"]["player2_money"][0]
                self.dj_player_2_money_image_rect.y += self.number_json["main"]["player2_money"][1]
                self.screen.blit(self.dj_player_2_money_image,self.dj_player_2_money_image_rect)

                dj_player_3_railway = str(self.total_info["player4"][2])
                self.dj_player_3_railway_image = self.font.render(dj_player_3_railway,True,
                                                    (0,0,0))
                self.dj_player_3_railway_image_rect = self.dj_player_3_railway_image.get_rect()
                self.dj_player_3_railway_image_rect.x += self.number_json["main"]["player3_railway"][0]
                self.dj_player_3_railway_image_rect.y += self.number_json["main"]["player3_railway"][1]
                self.screen.blit(self.dj_player_3_railway_image,self.dj_player_3_railway_image_rect)

                dj_player_3_ship = str(self.total_info["player4"][1])
                self.dj_player_3_ship_image = self.font.render(dj_player_3_ship,True,
                                                    (0,0,0))
                self.dj_player_3_ship_image_rect = self.dj_player_3_ship_image.get_rect()
                self.dj_player_3_ship_image_rect.x += self.number_json["main"]["player3_ship"][0]
                self.dj_player_3_ship_image_rect.y += self.number_json["main"]["player3_ship"][1]
                self.screen.blit(self.dj_player_3_ship_image,self.dj_player_3_ship_image_rect)

                dj_player_3_road = str(self.total_info["player4"][3])
                self.dj_player_3_road_image = self.font.render(dj_player_3_road,True,
                                                    (0,0,0))
                self.dj_player_3_road_image_rect = self.dj_player_3_road_image.get_rect()
                self.dj_player_3_road_image_rect.x += self.number_json["main"]["player3_road"][0]
                self.dj_player_3_road_image_rect.y += self.number_json["main"]["player3_road"][1]
                self.screen.blit(self.dj_player_3_road_image,self.dj_player_3_road_image_rect)

                dj_player_3_money = str(self.total_info["player4"][0])
                self.dj_player_3_money_image = self.font_3.render(dj_player_3_money,True,
                                                    (234,192,38))
                self.dj_player_3_money_image_rect = self.dj_player_3_money_image.get_rect()
                self.dj_player_3_money_image_rect.x += self.number_json["main"]["player3_money"][0]
                self.dj_player_3_money_image_rect.y += self.number_json["main"]["player3_money"][1]
                self.screen.blit(self.dj_player_3_money_image,self.dj_player_3_money_image_rect)

                dj_player_4_railway = str(self.total_info["player1"][2])
                self.dj_player_4_railway_image = self.font.render(dj_player_4_railway,True,
                                                    (0,0,0))
                self.dj_player_4_railway_image_rect = self.dj_player_4_railway_image.get_rect()
                self.dj_player_4_railway_image_rect.x += self.number_json["main"]["player4_railway"][0]
                self.dj_player_4_railway_image_rect.y += self.number_json["main"]["player4_railway"][1]
                self.screen.blit(self.dj_player_4_railway_image,self.dj_player_4_railway_image_rect)

                dj_player_4_ship = str(self.total_info["player1"][1])
                self.dj_player_4_ship_image = self.font.render(dj_player_4_ship,True,
                                                    (0,0,0))
                self.dj_player_4_ship_image_rect = self.dj_player_4_ship_image.get_rect()
                self.dj_player_4_ship_image_rect.x += self.number_json["main"]["player4_ship"][0]
                self.dj_player_4_ship_image_rect.y += self.number_json["main"]["player4_ship"][1]
                self.screen.blit(self.dj_player_4_ship_image,self.dj_player_4_ship_image_rect)

                dj_player_4_road = str(self.total_info["player1"][3])
                self.dj_player_4_road_image = self.font.render(dj_player_4_road,True,
                                                    (0,0,0))
                self.dj_player_4_road_image_rect = self.dj_player_4_road_image.get_rect()
                self.dj_player_4_road_image_rect.x += self.number_json["main"]["player4_road"][0]
                self.dj_player_4_road_image_rect.y += self.number_json["main"]["player4_road"][1]
                self.screen.blit(self.dj_player_4_road_image,self.dj_player_4_road_image_rect)

                dj_player_4_money = str(self.total_info["player1"][0])
                self.dj_player_4_money_image = self.font_3.render(dj_player_4_money,True,
                                                    (234,192,38))
                self.dj_player_4_money_image_rect = self.dj_player_4_money_image.get_rect()
                self.dj_player_4_money_image_rect.x += self.number_json["main"]["player4_money"][0]
                self.dj_player_4_money_image_rect.y += self.number_json["main"]["player4_money"][1]
                self.screen.blit(self.dj_player_4_money_image,self.dj_player_4_money_image_rect)


            
        if self.i_am == 3:
            dj_player_1_railway = str(self.total_info["player3"][2])
            self.dj_player_1_railway_image = self.font.render(dj_player_1_railway,True,
                                                (0,0,0))
            self.dj_player_1_railway_image_rect = self.dj_player_1_railway_image.get_rect()
            self.dj_player_1_railway_image_rect.x += self.number_json["main"]["player1_railway"][0]
            self.dj_player_1_railway_image_rect.y += self.number_json["main"]["player1_railway"][1]
            self.screen.blit(self.dj_player_1_railway_image,self.dj_player_1_railway_image_rect)

            dj_player_1_ship = str(self.total_info["player3"][1])
            self.dj_player_1_ship_image = self.font.render(dj_player_1_ship,True,
                                                (0,0,0))
            self.dj_player_1_ship_image_rect = self.dj_player_1_ship_image.get_rect()
            self.dj_player_1_ship_image_rect.x += self.number_json["main"]["player1_ship"][0]
            self.dj_player_1_ship_image_rect.y += self.number_json["main"]["player1_ship"][1]
            self.screen.blit(self.dj_player_1_ship_image,self.dj_player_1_ship_image_rect)

            dj_player_1_road = str(self.total_info["player3"][3])
            self.dj_player_1_road_image = self.font.render(dj_player_1_road,True,
                                                (0,0,0))
            self.dj_player_1_road_image_rect = self.dj_player_1_road_image.get_rect()
            self.dj_player_1_road_image_rect.x += self.number_json["main"]["player1_road"][0]
            self.dj_player_1_road_image_rect.y += self.number_json["main"]["player1_road"][1]
            self.screen.blit(self.dj_player_1_road_image,self.dj_player_1_road_image_rect)

            dj_player_1_money = str(self.total_info["player3"][0])
            self.dj_player_1_money_image = self.font.render(dj_player_1_money,True,
                                                (234,192,38))
            self.dj_player_1_money_image_rect = self.dj_player_1_money_image.get_rect()
            self.dj_player_1_money_image_rect.x += self.number_json["main"]["player1_money"][0]
            self.dj_player_1_money_image_rect.y += self.number_json["main"]["player1_money"][1]
            self.screen.blit(self.dj_player_1_money_image,self.dj_player_1_money_image_rect)

            dj_player_1_trap = str(self.total_info["player3"][5])
            self.dj_player_1_trap_image = self.font.render(dj_player_1_trap,True,
                                                (0,0,0))
            self.dj_player_1_trap_image_rect = self.dj_player_1_trap_image.get_rect()
            self.dj_player_1_trap_image_rect.x += self.number_json["main"]["player1_trap"][0]
            self.dj_player_1_trap_image_rect.y += self.number_json["main"]["player1_trap"][1]
            self.screen.blit(self.dj_player_1_trap_image,self.dj_player_1_trap_image_rect)

            dj_player_1_war = str(self.total_info["player3"][4])
            self.dj_player_1_war_image = self.font.render(dj_player_1_war,True,
                                                (0,0,0))
            self.dj_player_1_war_image_rect = self.dj_player_1_war_image.get_rect()
            self.dj_player_1_war_image_rect.x += self.number_json["main"]["player1_war"][0]
            self.dj_player_1_war_image_rect.y += self.number_json["main"]["player1_war"][1]
            self.screen.blit(self.dj_player_1_war_image,self.dj_player_1_war_image_rect)

            dj_player_1_skip = str(self.total_info["player3"][7])
            self.dj_player_1_skip_image = self.font.render(dj_player_1_skip,True,
                                                (0,0,0))
            self.dj_player_1_skip_image_rect = self.dj_player_1_skip_image.get_rect()
            self.dj_player_1_skip_image_rect.x += self.number_json["main"]["player1_skip"][0]
            self.dj_player_1_skip_image_rect.y += self.number_json["main"]["player1_skip"][1]
            self.screen.blit(self.dj_player_1_skip_image,self.dj_player_1_skip_image_rect)

            dj_player_1_hide = str(self.total_info["player3"][6])
            self.dj_player_1_hide_image = self.font.render(dj_player_1_hide,True,
                                                (0,0,0))
            self.dj_player_1_hide_image_rect = self.dj_player_1_hide_image.get_rect()
            self.dj_player_1_hide_image_rect.x += self.number_json["main"]["player1_hide"][0]
            self.dj_player_1_hide_image_rect.y += self.number_json["main"]["player1_hide"][1]
            self.screen.blit(self.dj_player_1_hide_image,self.dj_player_1_hide_image_rect)

            if self.game_active_7 == False:
                dj_player_2_railway = str(self.total_info["player4"][2])
                self.dj_player_2_railway_image = self.font.render(dj_player_2_railway,True,
                                                    (0,0,0))
                self.dj_player_2_railway_image_rect = self.dj_player_2_railway_image.get_rect()
                self.dj_player_2_railway_image_rect.x += self.number_json["main"]["player2_railway"][0]
                self.dj_player_2_railway_image_rect.y += self.number_json["main"]["player2_railway"][1]
                self.screen.blit(self.dj_player_2_railway_image,self.dj_player_2_railway_image_rect)

                dj_player_2_ship = str(self.total_info["player4"][1])
                self.dj_player_2_ship_image = self.font.render(dj_player_2_ship,True,
                                                    (0,0,0))
                self.dj_player_2_ship_image_rect = self.dj_player_2_ship_image.get_rect()
                self.dj_player_2_ship_image_rect.x += self.number_json["main"]["player2_ship"][0]
                self.dj_player_2_ship_image_rect.y += self.number_json["main"]["player2_ship"][1]
                self.screen.blit(self.dj_player_2_ship_image,self.dj_player_2_ship_image_rect)

                dj_player_2_road = str(self.total_info["player4"][3])
                self.dj_player_2_road_image = self.font.render(dj_player_2_road,True,
                                                    (0,0,0))
                self.dj_player_2_road_image_rect = self.dj_player_2_road_image.get_rect()
                self.dj_player_2_road_image_rect.x += self.number_json["main"]["player2_road"][0]
                self.dj_player_2_road_image_rect.y += self.number_json["main"]["player2_road"][1]
                self.screen.blit(self.dj_player_2_road_image,self.dj_player_2_road_image_rect)

                dj_player_2_money = str(self.total_info["player4"][0])
                self.dj_player_2_money_image = self.font_3.render(dj_player_2_money,True,
                                                    (234,192,38))
                self.dj_player_2_money_image_rect = self.dj_player_2_money_image.get_rect()
                self.dj_player_2_money_image_rect.x += self.number_json["main"]["player2_money"][0]
                self.dj_player_2_money_image_rect.y += self.number_json["main"]["player2_money"][1]
                self.screen.blit(self.dj_player_2_money_image,self.dj_player_2_money_image_rect)

                dj_player_3_railway = str(self.total_info["player1"][2])
                self.dj_player_3_railway_image = self.font.render(dj_player_3_railway,True,
                                                    (0,0,0))
                self.dj_player_3_railway_image_rect = self.dj_player_3_railway_image.get_rect()
                self.dj_player_3_railway_image_rect.x += self.number_json["main"]["player3_railway"][0]
                self.dj_player_3_railway_image_rect.y += self.number_json["main"]["player3_railway"][1]
                self.screen.blit(self.dj_player_3_railway_image,self.dj_player_3_railway_image_rect)

                dj_player_3_ship = str(self.total_info["player1"][1])
                self.dj_player_3_ship_image = self.font.render(dj_player_3_ship,True,
                                                    (0,0,0))
                self.dj_player_3_ship_image_rect = self.dj_player_3_ship_image.get_rect()
                self.dj_player_3_ship_image_rect.x += self.number_json["main"]["player3_ship"][0]
                self.dj_player_3_ship_image_rect.y += self.number_json["main"]["player3_ship"][1]
                self.screen.blit(self.dj_player_3_ship_image,self.dj_player_3_ship_image_rect)

                dj_player_3_road = str(self.total_info["player1"][3])
                self.dj_player_3_road_image = self.font.render(dj_player_3_road,True,
                                                    (0,0,0))
                self.dj_player_3_road_image_rect = self.dj_player_3_road_image.get_rect()
                self.dj_player_3_road_image_rect.x += self.number_json["main"]["player3_road"][0]
                self.dj_player_3_road_image_rect.y += self.number_json["main"]["player3_road"][1]
                self.screen.blit(self.dj_player_3_road_image,self.dj_player_3_road_image_rect)

                dj_player_3_money = str(self.total_info["player1"][0])
                self.dj_player_3_money_image = self.font_3.render(dj_player_3_money,True,
                                                    (234,192,38))
                self.dj_player_3_money_image_rect = self.dj_player_3_money_image.get_rect()
                self.dj_player_3_money_image_rect.x += self.number_json["main"]["player3_money"][0]
                self.dj_player_3_money_image_rect.y += self.number_json["main"]["player3_money"][1]
                self.screen.blit(self.dj_player_3_money_image,self.dj_player_3_money_image_rect)


                dj_player_4_railway = str(self.total_info["player2"][2])
                self.dj_player_4_railway_image = self.font.render(dj_player_4_railway,True,
                                                    (0,0,0))
                self.dj_player_4_railway_image_rect = self.dj_player_4_railway_image.get_rect()
                self.dj_player_4_railway_image_rect.x += self.number_json["main"]["player4_railway"][0]
                self.dj_player_4_railway_image_rect.y += self.number_json["main"]["player4_railway"][1]
                self.screen.blit(self.dj_player_4_railway_image,self.dj_player_4_railway_image_rect)

                dj_player_4_ship = str(self.total_info["player2"][1])
                self.dj_player_4_ship_image = self.font.render(dj_player_4_ship,True,
                                                    (0,0,0))
                self.dj_player_4_ship_image_rect = self.dj_player_4_ship_image.get_rect()
                self.dj_player_4_ship_image_rect.x += self.number_json["main"]["player4_ship"][0]
                self.dj_player_4_ship_image_rect.y += self.number_json["main"]["player4_ship"][1]
                self.screen.blit(self.dj_player_4_ship_image,self.dj_player_4_ship_image_rect)

                dj_player_4_road = str(self.total_info["player2"][3])
                self.dj_player_4_road_image = self.font.render(dj_player_4_road,True,
                                                    (0,0,0))
                self.dj_player_4_road_image_rect = self.dj_player_4_road_image.get_rect()
                self.dj_player_4_road_image_rect.x += self.number_json["main"]["player4_road"][0]
                self.dj_player_4_road_image_rect.y += self.number_json["main"]["player4_road"][1]
                self.screen.blit(self.dj_player_4_road_image,self.dj_player_4_road_image_rect)

                dj_player_4_money = str(self.total_info["player2"][0])
                self.dj_player_4_money_image = self.font_3.render(dj_player_4_money,True,
                                                    (234,192,38))
                self.dj_player_4_money_image_rect = self.dj_player_4_money_image.get_rect()
                self.dj_player_4_money_image_rect.x += self.number_json["main"]["player4_money"][0]
                self.dj_player_4_money_image_rect.y += self.number_json["main"]["player4_money"][1]
                self.screen.blit(self.dj_player_4_money_image,self.dj_player_4_money_image_rect)
            

        if self.i_am == 4:
            dj_player_1_railway = str(self.total_info["player4"][2])
            self.dj_player_1_railway_image = self.font.render(dj_player_1_railway,True,
                                                (0,0,0))
            self.dj_player_1_railway_image_rect = self.dj_player_1_railway_image.get_rect()
            self.dj_player_1_railway_image_rect.x += self.number_json["main"]["player1_railway"][0]
            self.dj_player_1_railway_image_rect.y += self.number_json["main"]["player1_railway"][1]
            self.screen.blit(self.dj_player_1_railway_image,self.dj_player_1_railway_image_rect)

            dj_player_1_ship = str(self.total_info["player4"][1])
            self.dj_player_1_ship_image = self.font.render(dj_player_1_ship,True,
                                                (0,0,0))
            self.dj_player_1_ship_image_rect = self.dj_player_1_ship_image.get_rect()
            self.dj_player_1_ship_image_rect.x += self.number_json["main"]["player1_ship"][0]
            self.dj_player_1_ship_image_rect.y += self.number_json["main"]["player1_ship"][1]
            self.screen.blit(self.dj_player_1_ship_image,self.dj_player_1_ship_image_rect)

            dj_player_1_road = str(self.total_info["player4"][3])
            self.dj_player_1_road_image = self.font.render(dj_player_1_road,True,
                                                (0,0,0))
            self.dj_player_1_road_image_rect = self.dj_player_1_road_image.get_rect()
            self.dj_player_1_road_image_rect.x += self.number_json["main"]["player1_road"][0]
            self.dj_player_1_road_image_rect.y += self.number_json["main"]["player1_road"][1]
            self.screen.blit(self.dj_player_1_road_image,self.dj_player_1_road_image_rect)

            dj_player_1_money = str(self.total_info["player4"][0])
            self.dj_player_1_money_image = self.font.render(dj_player_1_money,True,
                                                (234,192,38))
            self.dj_player_1_money_image_rect = self.dj_player_1_money_image.get_rect()
            self.dj_player_1_money_image_rect.x += self.number_json["main"]["player1_money"][0]
            self.dj_player_1_money_image_rect.y += self.number_json["main"]["player1_money"][1]
            self.screen.blit(self.dj_player_1_money_image,self.dj_player_1_money_image_rect)

            dj_player_1_trap = str(self.total_info["player4"][5])
            self.dj_player_1_trap_image = self.font.render(dj_player_1_trap,True,
                                                (0,0,0))
            self.dj_player_1_trap_image_rect = self.dj_player_1_trap_image.get_rect()
            self.dj_player_1_trap_image_rect.x += self.number_json["main"]["player1_trap"][0]
            self.dj_player_1_trap_image_rect.y += self.number_json["main"]["player1_trap"][1]
            self.screen.blit(self.dj_player_1_trap_image,self.dj_player_1_trap_image_rect)

            dj_player_1_war = str(self.total_info["player4"][4])
            self.dj_player_1_war_image = self.font.render(dj_player_1_war,True,
                                                (0,0,0))
            self.dj_player_1_war_image_rect = self.dj_player_1_war_image.get_rect()
            self.dj_player_1_war_image_rect.x += self.number_json["main"]["player1_war"][0]
            self.dj_player_1_war_image_rect.y += self.number_json["main"]["player1_war"][1]
            self.screen.blit(self.dj_player_1_war_image,self.dj_player_1_war_image_rect)

            dj_player_1_skip = str(self.total_info["player4"][7])
            self.dj_player_1_skip_image = self.font.render(dj_player_1_skip,True,
                                                (0,0,0))
            self.dj_player_1_skip_image_rect = self.dj_player_1_skip_image.get_rect()
            self.dj_player_1_skip_image_rect.x += self.number_json["main"]["player1_skip"][0]
            self.dj_player_1_skip_image_rect.y += self.number_json["main"]["player1_skip"][1]
            self.screen.blit(self.dj_player_1_skip_image,self.dj_player_1_skip_image_rect)

            dj_player_1_hide = str(self.total_info["player4"][6])
            self.dj_player_1_hide_image = self.font.render(dj_player_1_hide,True,
                                                (0,0,0))
            self.dj_player_1_hide_image_rect = self.dj_player_1_hide_image.get_rect()
            self.dj_player_1_hide_image_rect.x += self.number_json["main"]["player1_hide"][0]
            self.dj_player_1_hide_image_rect.y += self.number_json["main"]["player1_hide"][1]
            self.screen.blit(self.dj_player_1_hide_image,self.dj_player_1_hide_image_rect)

            if self.game_active_7 == False:
                dj_player_2_railway = str(self.total_info["player1"][2])
                self.dj_player_2_railway_image = self.font.render(dj_player_2_railway,True,
                                                    (0,0,0))
                self.dj_player_2_railway_image_rect = self.dj_player_2_railway_image.get_rect()
                self.dj_player_2_railway_image_rect.x += self.number_json["main"]["player2_railway"][0]
                self.dj_player_2_railway_image_rect.y += self.number_json["main"]["player2_railway"][1]
                self.screen.blit(self.dj_player_2_railway_image,self.dj_player_2_railway_image_rect)

                dj_player_2_ship = str(self.total_info["player1"][1])
                self.dj_player_2_ship_image = self.font.render(dj_player_2_ship,True,
                                                    (0,0,0))
                self.dj_player_2_ship_image_rect = self.dj_player_2_ship_image.get_rect()
                self.dj_player_2_ship_image_rect.x += self.number_json["main"]["player2_ship"][0]
                self.dj_player_2_ship_image_rect.y += self.number_json["main"]["player2_ship"][1]
                self.screen.blit(self.dj_player_2_ship_image,self.dj_player_2_ship_image_rect)

                dj_player_2_road = str(self.total_info["player1"][3])
                self.dj_player_2_road_image = self.font.render(dj_player_2_road,True,
                                                    (0,0,0))
                self.dj_player_2_road_image_rect = self.dj_player_2_road_image.get_rect()
                self.dj_player_2_road_image_rect.x += self.number_json["main"]["player2_road"][0]
                self.dj_player_2_road_image_rect.y += self.number_json["main"]["player2_road"][1]
                self.screen.blit(self.dj_player_2_road_image,self.dj_player_2_road_image_rect)

                dj_player_2_money = str(self.total_info["player1"][0])
                self.dj_player_2_money_image = self.font_3.render(dj_player_2_money,True,
                                                    (234,192,38))
                self.dj_player_2_money_image_rect = self.dj_player_2_money_image.get_rect()
                self.dj_player_2_money_image_rect.x += self.number_json["main"]["player2_money"][0]
                self.dj_player_2_money_image_rect.y += self.number_json["main"]["player2_money"][1]
                self.screen.blit(self.dj_player_2_money_image,self.dj_player_2_money_image_rect)

                dj_player_3_railway = str(self.total_info["player2"][2])
                self.dj_player_3_railway_image = self.font.render(dj_player_3_railway,True,
                                                    (0,0,0))
                self.dj_player_3_railway_image_rect = self.dj_player_3_railway_image.get_rect()
                self.dj_player_3_railway_image_rect.x += self.number_json["main"]["player3_railway"][0]
                self.dj_player_3_railway_image_rect.y += self.number_json["main"]["player3_railway"][1]
                self.screen.blit(self.dj_player_3_railway_image,self.dj_player_3_railway_image_rect)

                dj_player_3_ship = str(self.total_info["player2"][1])
                self.dj_player_3_ship_image = self.font.render(dj_player_3_ship,True,
                                                    (0,0,0))
                self.dj_player_3_ship_image_rect = self.dj_player_3_ship_image.get_rect()
                self.dj_player_3_ship_image_rect.x += self.number_json["main"]["player3_ship"][0]
                self.dj_player_3_ship_image_rect.y += self.number_json["main"]["player3_ship"][1]
                self.screen.blit(self.dj_player_3_ship_image,self.dj_player_3_ship_image_rect)

                dj_player_3_road = str(self.total_info["player2"][3])
                self.dj_player_3_road_image = self.font.render(dj_player_3_road,True,
                                                    (0,0,0))
                self.dj_player_3_road_image_rect = self.dj_player_3_road_image.get_rect()
                self.dj_player_3_road_image_rect.x += self.number_json["main"]["player3_road"][0]
                self.dj_player_3_road_image_rect.y += self.number_json["main"]["player3_road"][1]
                self.screen.blit(self.dj_player_3_road_image,self.dj_player_3_road_image_rect)

                dj_player_3_money = str(self.total_info["player2"][0])
                self.dj_player_3_money_image = self.font_3.render(dj_player_3_money,True,
                                                    (234,192,38))
                self.dj_player_3_money_image_rect = self.dj_player_3_money_image.get_rect()
                self.dj_player_3_money_image_rect.x += self.number_json["main"]["player3_money"][0]
                self.dj_player_3_money_image_rect.y += self.number_json["main"]["player3_money"][1]
                self.screen.blit(self.dj_player_3_money_image,self.dj_player_3_money_image_rect)


                dj_player_4_railway = str(self.total_info["player3"][2])
                self.dj_player_4_railway_image = self.font.render(dj_player_4_railway,True,
                                                    (0,0,0))
                self.dj_player_4_railway_image_rect = self.dj_player_4_railway_image.get_rect()
                self.dj_player_4_railway_image_rect.x += self.number_json["main"]["player4_railway"][0]
                self.dj_player_4_railway_image_rect.y += self.number_json["main"]["player4_railway"][1]
                self.screen.blit(self.dj_player_4_railway_image,self.dj_player_4_railway_image_rect)

                dj_player_4_ship = str(self.total_info["player3"][1])
                self.dj_player_4_ship_image = self.font.render(dj_player_4_ship,True,
                                                    (0,0,0))
                self.dj_player_4_ship_image_rect = self.dj_player_4_ship_image.get_rect()
                self.dj_player_4_ship_image_rect.x += self.number_json["main"]["player4_ship"][0]
                self.dj_player_4_ship_image_rect.y += self.number_json["main"]["player4_ship"][1]
                self.screen.blit(self.dj_player_4_ship_image,self.dj_player_4_ship_image_rect)

                dj_player_4_road = str(self.total_info["player3"][3])
                self.dj_player_4_road_image = self.font.render(dj_player_4_road,True,
                                                    (0,0,0))
                self.dj_player_4_road_image_rect = self.dj_player_4_road_image.get_rect()
                self.dj_player_4_road_image_rect.x += self.number_json["main"]["player4_road"][0]
                self.dj_player_4_road_image_rect.y += self.number_json["main"]["player4_road"][1]
                self.screen.blit(self.dj_player_4_road_image,self.dj_player_4_road_image_rect)

                dj_player_4_money = str(self.total_info["player3"][0])
                self.dj_player_4_money_image = self.font_3.render(dj_player_4_money,True,
                                                    (234,192,38))
                self.dj_player_4_money_image_rect = self.dj_player_4_money_image.get_rect()
                self.dj_player_4_money_image_rect.x += self.number_json["main"]["player4_money"][0]
                self.dj_player_4_money_image_rect.y += self.number_json["main"]["player4_money"][1]
                self.screen.blit(self.dj_player_4_money_image,self.dj_player_4_money_image_rect)


            
#结算界面数据
    def jiesuan_shuju(self):
        """初始化并绘制各类数据"""
        sj_player_1_money = str(self.total_info["player1"][0])
        self.sj_player_1_money_image = self.font.render(sj_player_1_money,True,
                                            (0,0,0))
        self.sj_player_1_money_image_rect = self.sj_player_1_money_image.get_rect()
        self.sj_player_1_money_image_rect.x += self.number_json["ending"]["player1_money"][0]
        self.sj_player_1_money_image_rect.y += self.number_json["ending"]["player1_money"][1]
        self.screen.blit(self.sj_player_1_money_image,self.sj_player_1_money_image_rect)

        sj_player_1_trap = str(self.total_info["player1"][5])
        self.sj_player_1_trap_image = self.font.render(sj_player_1_trap,True,
                                            (0,0,0))
        self.sj_player_1_trap_image_rect = self.sj_player_1_trap_image.get_rect()
        self.sj_player_1_trap_image_rect.x += self.number_json["ending"]["player1_trap"][0]
        self.sj_player_1_trap_image_rect.y += self.number_json["ending"]["player1_trap"][1]
        self.screen.blit(self.sj_player_1_trap_image,self.sj_player_1_trap_image_rect)

        sj_player_1_trapped = str(self.total_info["player1"][9])
        self.sj_player_1_trapped_image = self.font.render(sj_player_1_trapped,True,
                                            (0,0,0))
        self.sj_player_1_trapped_image_rect = self.sj_player_1_trapped_image.get_rect()
        self.sj_player_1_trapped_image_rect.x += self.number_json["ending"]["player1_trapped"][0]
        self.sj_player_1_trapped_image_rect.y += self.number_json["ending"]["player1_trapped"][1]
        self.screen.blit(self.sj_player_1_trapped_image,self.sj_player_1_trapped_image_rect)

        sj_player_1_war = str(self.total_info["player1"][10])
        self.sj_player_1_war_image = self.font.render(sj_player_1_war,True,
                                            (0,0,0))
        self.sj_player_1_war_image_rect = self.sj_player_1_war_image.get_rect()
        self.sj_player_1_war_image_rect.x += self.number_json["ending"]["player1_war"][0]
        self.sj_player_1_war_image_rect.y += self.number_json["ending"]["player1_war"][1]
        self.screen.blit(self.sj_player_1_war_image,self.sj_player_1_war_image_rect)

        sj_player_1_hide = str(self.total_info["player1"][11])
        self.sj_player_1_hide_image = self.font.render(sj_player_1_hide,True,
                                            (0,0,0))
        self.sj_player_1_hide_image_rect = self.sj_player_1_hide_image.get_rect()
        self.sj_player_1_hide_image_rect.x += self.number_json["ending"]["player1_hide"][0]
        self.sj_player_1_hide_image_rect.y += self.number_json["ending"]["player1_hide"][1]
        self.screen.blit(self.sj_player_1_hide_image,self.sj_player_1_hide_image_rect)

        sj_player_1_skip = str(self.total_info["player1"][12])
        self.sj_player_1_skip_image = self.font.render(sj_player_1_skip,True,
                                            (0,0,0))
        self.sj_player_1_skip_image_rect = self.sj_player_1_skip_image.get_rect()
        self.sj_player_1_skip_image_rect.x += self.number_json["ending"]["player1_skip"][0]
        self.sj_player_1_skip_image_rect.y += self.number_json["ending"]["player1_skip"][1]
        self.screen.blit(self.sj_player_1_skip_image,self.sj_player_1_skip_image_rect)



                
        sj_player_2_money = str(self.total_info["player2"][0])
        self.sj_player_2_money_image = self.font.render(sj_player_2_money,True,
                                            (0,0,0))
        self.sj_player_2_money_image_rect = self.sj_player_2_money_image.get_rect()
        self.sj_player_2_money_image_rect.x += self.number_json["ending"]["player2_money"][0]
        self.sj_player_2_money_image_rect.y += self.number_json["ending"]["player2_money"][1]
        self.screen.blit(self.sj_player_2_money_image,self.sj_player_2_money_image_rect)

        sj_player_2_trap = str(self.total_info["player2"][5])
        self.sj_player_2_trap_image = self.font.render(sj_player_2_trap,True,
                                            (0,0,0))
        self.sj_player_2_trap_image_rect = self.sj_player_2_trap_image.get_rect()
        self.sj_player_2_trap_image_rect.x += self.number_json["ending"]["player2_trap"][0]
        self.sj_player_2_trap_image_rect.y += self.number_json["ending"]["player2_trap"][1]
        self.screen.blit(self.sj_player_2_trap_image,self.sj_player_2_trap_image_rect)

        sj_player_2_trapped = str(self.total_info["player2"][9])
        self.sj_player_2_trapped_image = self.font.render(sj_player_2_trapped,True,
                                            (0,0,0))
        self.sj_player_2_trapped_image_rect = self.sj_player_2_trapped_image.get_rect()
        self.sj_player_2_trapped_image_rect.x += self.number_json["ending"]["player2_trapped"][0]
        self.sj_player_2_trapped_image_rect.y += self.number_json["ending"]["player2_trapped"][1]
        self.screen.blit(self.sj_player_2_trapped_image,self.sj_player_2_trapped_image_rect)

        sj_player_2_war = str(self.total_info["player2"][10])
        self.sj_player_2_war_image = self.font.render(sj_player_2_war,True,
                                            (0,0,0))
        self.sj_player_2_war_image_rect = self.sj_player_2_war_image.get_rect()
        self.sj_player_2_war_image_rect.x += self.number_json["ending"]["player2_war"][0]
        self.sj_player_2_war_image_rect.y += self.number_json["ending"]["player2_war"][1]
        self.screen.blit(self.sj_player_2_war_image,self.sj_player_2_war_image_rect)

        sj_player_2_hide = str(self.total_info["player2"][11])
        self.sj_player_2_hide_image = self.font.render(sj_player_2_hide,True,
                                            (0,0,0))
        self.sj_player_2_hide_image_rect = self.sj_player_2_hide_image.get_rect()
        self.sj_player_2_hide_image_rect.x += self.number_json["ending"]["player2_hide"][0]
        self.sj_player_2_hide_image_rect.y += self.number_json["ending"]["player2_hide"][1]
        self.screen.blit(self.sj_player_2_hide_image,self.sj_player_2_hide_image_rect)

        sj_player_2_skip = str(self.total_info["player2"][12])
        self.sj_player_2_skip_image = self.font.render(sj_player_2_skip,True,
                                            (0,0,0))
        self.sj_player_2_skip_image_rect = self.sj_player_2_skip_image.get_rect()
        self.sj_player_2_skip_image_rect.x += self.number_json["ending"]["player2_skip"][0]
        self.sj_player_2_skip_image_rect.y += self.number_json["ending"]["player2_skip"][1]
        self.screen.blit(self.sj_player_2_skip_image,self.sj_player_2_skip_image_rect)



                
        sj_player_3_money = str(self.total_info["player3"][0])
        self.sj_player_3_money_image = self.font.render(sj_player_3_money,True,
                                            (0,0,0))
        self.sj_player_3_money_image_rect = self.sj_player_3_money_image.get_rect()
        self.sj_player_3_money_image_rect.x += self.number_json["ending"]["player3_money"][0]
        self.sj_player_3_money_image_rect.y += self.number_json["ending"]["player3_money"][1]
        self.screen.blit(self.sj_player_3_money_image,self.sj_player_3_money_image_rect)

        sj_player_3_trap = str(self.total_info["player3"][5])
        self.sj_player_3_trap_image = self.font.render(sj_player_3_trap,True,
                                            (0,0,0))
        self.sj_player_3_trap_image_rect = self.sj_player_3_trap_image.get_rect()
        self.sj_player_3_trap_image_rect.x += self.number_json["ending"]["player3_trap"][0]
        self.sj_player_3_trap_image_rect.y += self.number_json["ending"]["player3_trap"][1]
        self.screen.blit(self.sj_player_3_trap_image,self.sj_player_3_trap_image_rect)

        sj_player_3_trapped = str(self.total_info["player3"][9])
        self.sj_player_3_trapped_image = self.font.render(sj_player_3_trapped,True,
                                            (0,0,0))
        self.sj_player_3_trapped_image_rect = self.sj_player_3_trapped_image.get_rect()
        self.sj_player_3_trapped_image_rect.x += self.number_json["ending"]["player3_trapped"][0]
        self.sj_player_3_trapped_image_rect.y += self.number_json["ending"]["player3_trapped"][1]
        self.screen.blit(self.sj_player_3_trapped_image,self.sj_player_3_trapped_image_rect)

        sj_player_3_war = str(self.total_info["player3"][10])
        self.sj_player_3_war_image = self.font.render(sj_player_3_war,True,
                                            (0,0,0))
        self.sj_player_3_war_image_rect = self.sj_player_3_war_image.get_rect()
        self.sj_player_3_war_image_rect.x += self.number_json["ending"]["player3_war"][0]
        self.sj_player_3_war_image_rect.y += self.number_json["ending"]["player3_war"][1]
        self.screen.blit(self.sj_player_3_war_image,self.sj_player_3_war_image_rect)

        sj_player_3_hide = str(self.total_info["player3"][11])
        self.sj_player_3_hide_image = self.font.render(sj_player_3_hide,True,
                                            (0,0,0))
        self.sj_player_3_hide_image_rect = self.sj_player_3_hide_image.get_rect()
        self.sj_player_3_hide_image_rect.x += self.number_json["ending"]["player3_hide"][0]
        self.sj_player_3_hide_image_rect.y += self.number_json["ending"]["player3_hide"][1]
        self.screen.blit(self.sj_player_3_hide_image,self.sj_player_3_hide_image_rect)

        sj_player_3_skip = str(self.total_info["player3"][12])
        self.sj_player_3_skip_image = self.font.render(sj_player_3_skip,True,
                                            (0,0,0))
        self.sj_player_3_skip_image_rect = self.sj_player_3_skip_image.get_rect()
        self.sj_player_3_skip_image_rect.x += self.number_json["ending"]["player3_skip"][0]
        self.sj_player_3_skip_image_rect.y += self.number_json["ending"]["player3_skip"][1]
        self.screen.blit(self.sj_player_3_skip_image,self.sj_player_3_skip_image_rect)



                
        sj_player_4_money = str(self.total_info["player4"][0])
        self.sj_player_4_money_image = self.font.render(sj_player_4_money,True,
                                            (0,0,0))
        self.sj_player_4_money_image_rect = self.sj_player_4_money_image.get_rect()
        self.sj_player_4_money_image_rect.x += self.number_json["ending"]["player4_money"][0]
        self.sj_player_4_money_image_rect.y += self.number_json["ending"]["player4_money"][1]
        self.screen.blit(self.sj_player_4_money_image,self.sj_player_4_money_image_rect)

        sj_player_4_trap = str(self.total_info["player4"][5])
        self.sj_player_4_trap_image = self.font.render(sj_player_4_trap,True,
                                            (0,0,0))
        self.sj_player_4_trap_image_rect = self.sj_player_4_trap_image.get_rect()
        self.sj_player_4_trap_image_rect.x += self.number_json["ending"]["player4_trap"][0]
        self.sj_player_4_trap_image_rect.y += self.number_json["ending"]["player4_trap"][1]
        self.screen.blit(self.sj_player_4_trap_image,self.sj_player_4_trap_image_rect)

        sj_player_4_trapped = str(self.total_info["player4"][9])
        self.sj_player_4_trapped_image = self.font.render(sj_player_4_trapped,True,
                                            (0,0,0))
        self.sj_player_4_trapped_image_rect = self.sj_player_4_trapped_image.get_rect()
        self.sj_player_4_trapped_image_rect.x += self.number_json["ending"]["player4_trapped"][0]
        self.sj_player_4_trapped_image_rect.y += self.number_json["ending"]["player4_trapped"][1]
        self.screen.blit(self.sj_player_4_trapped_image,self.sj_player_4_trapped_image_rect)

        sj_player_4_war = str(self.total_info["player4"][10])
        self.sj_player_4_war_image = self.font.render(sj_player_4_war,True,
                                            (0,0,0))
        self.sj_player_4_war_image_rect = self.sj_player_4_war_image.get_rect()
        self.sj_player_4_war_image_rect.x += self.number_json["ending"]["player4_war"][0]
        self.sj_player_4_war_image_rect.y += self.number_json["ending"]["player4_war"][1]
        self.screen.blit(self.sj_player_4_war_image,self.sj_player_4_war_image_rect)

        sj_player_4_hide = str(self.total_info["player4"][11])
        self.sj_player_4_hide_image = self.font.render(sj_player_4_hide,True,
                                            (0,0,0))
        self.sj_player_4_hide_image_rect = self.sj_player_4_hide_image.get_rect()
        self.sj_player_4_hide_image_rect.x += self.number_json["ending"]["player4_hide"][0]
        self.sj_player_4_hide_image_rect.y += self.number_json["ending"]["player4_hide"][1]
        self.screen.blit(self.sj_player_4_hide_image,self.sj_player_4_hide_image_rect)

        sj_player_4_skip = str(self.total_info["player4"][12])
        self.sj_player_4_skip_image = self.font.render(sj_player_4_skip,True,
                                            (0,0,0))
        self.sj_player_4_skip_image_rect = self.sj_player_4_skip_image.get_rect()
        self.sj_player_4_skip_image_rect.x += self.number_json["ending"]["player4_skip"][0]
        self.sj_player_4_skip_image_rect.y += self.number_json["ending"]["player4_skip"][1]
        self.screen.blit(self.sj_player_4_skip_image,self.sj_player_4_skip_image_rect)

        sj_total_time = str(self.total_time)
        self.sj_total_time_image = self.font.render(sj_total_time,True,
                                            (0,0,0))
        self.sj_total_time_image_rect = self.sj_total_time_image.get_rect()
        self.sj_total_time_image_rect.x += self.number_json["ending"]["time"][0]
        self.sj_total_time_image_rect.y += self.number_json["ending"]["time"][1]
        self.screen.blit(self.sj_total_time_image,self.sj_total_time_image_rect)

def run_server(self:LostCity):
    #print([2])
    pygame.display.flip()
    self.server.listen(10)

    while True:
        self.mouse_click_pos = (-1,-1)
        conn, address = self.server.accept()
        self.addresses[conn] = address
        threading.Thread(target=server_handle, args=(conn, address, self)).start()

def server_handle(conn,addr,self:LostCity):
    num = len(self.client) + 1
    self.client[conn] = num
    #print("test start!")
    pre_msg = self.total_info
    while True:    
        self.data['client'][str(num)] = conn
        
        try:


            msg = conn.recv(4096).decode('utf8')#------------------------------------------------------服务端接收
            #print(456)
            # #print("已收到信息为：")
            # #print(msg)
            self.co = json.loads(msg)
            #print(789)
            ##print("服务器已更改信息为：")
            ##print(msg)
            # self.total_info["1"][0] +=1

            '''这里写数据处理'''#--------------------一定要写在这里

            self.total_info['round&client_number&time'][1] = len(self.client) + 1
            #print(324)


            self.total_info[self.co['class1']][self.co['data1'][0]]=self.co['data1'][1]
            self.total_info[self.co['class2']][self.co['data2'][0]]=self.co['data2'][1]
            self.total_info[self.co['class3']][self.co['data3'][0]]=self.co['data3'][1]
            self.total_info[self.co['class4']][self.co['data4'][0]]=self.co['data4'][1]
            self.total_info[self.co['class5']][self.co['data5'][0]]=self.co['data5'][1]
            
            # self.total_info["round&client_number&time"][0] += 1
            #print(self.total_info['round&client_number&time'][0])
            #print(self.send_msg_pre['round&client_number&time'][0])
            if self.send_msg_pre['round&client_number&time'][0] != self.total_info['round&client_number&time'][0] or self.flush == True :
                #print(1345999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999)
                '''这里写回合清算数据更新'''
                #self.come_back()
                if self.flush == True:
                    self.flush = False
                    self.mouse_click_pos = (-1,-1)
                    self.total_info['round&client_number&time'][0] += 1
                    #print(37537556)
                    
                    # if self.i_am == 1:
                    #     self.come_back()

         
            #if msg != send_msg or self.total_info['round&client_number&time'][1]<4:
            send_msg = json.dumps(self.total_info)
            #print(65432)
            conn.send(bytes(send_msg, 'utf8'))#--------------------------------------------------------服务端发送
            self.send_msg_pre = self.total_info
            # #print("已发送信息为：")
            # #print(send_msg)
        
    
        except:
            conn.close()

def run_client(self:LostCity):
    self.tcp.connect((self.ipv4, self.port))  # 绑定主机和端口

    #test:
    self.client = {"wilbert":[100,100,100]}
    #print("test start! ")
    pre_msg = self.total_info
    while True:
        try:

            # if self.i_am % 4  ==  self.total_info["round&client_number&time"][0]%4 or self.total_info["round&client_number&time"][1] != 4:
            
            #print(1234567890)
            send_msg = json.dumps(self.co)#-----------------------------------------------------客户端发送
            #print(123456789765432)
            self.tcp.send(bytes(send_msg, 'utf8'))
            #print(23456786543)
            self.send_msg_pre = self.total_info

            


            try:
                recv_msg = self.tcp.recv(4096).decode('utf8')#----------------------------------------------客户端接收
                #print(3245678654324567443567655443)
                

                if pre_msg != recv_msg:
                    self.total_info = json.loads(recv_msg)
                    if self.send_msg_pre['round&client_number&time'][0] != self.total_info['round&client_number&time'][0]:
                        self.flush = False
                        self.mouse_click_pos = (-1,-1)
                        self.co = {"class1":"round&client_number&time",
                        "data1":[3,0],
                        "class2":"round&client_number&time",
                        "data2":[3,0],
                        "class3":"round&client_number&time",
                        "data3":[3,0],
                        "class4":"round&client_number&time",
                        "data4":[3,0],
                        "class5":"round&client_number&time",
                        "data5":[3,0]}
                    #print(456478657645324)
                    # #print("客户端已更改信息为：")
                    # #print(recv_msg)
                # self.total_info["1"][1] +=1

            except json.JSONDecodeError:
                print("Invalid JSON data received")
            except Exception as e:
                print(f"An error occurred: {e}")
                



                
            if self.total_info["round&client_number&time"][1] == 2:
                #print(234234)
                if self.i_have_known_myself == False:
                    self.i_am = 2
                    self.i_have_known_myself = True

            if self.total_info["round&client_number&time"][1] == 3:
                if self.i_have_known_myself == False:
                    self.i_am = 3
                    self.i_have_known_myself = True

            if self.total_info["round&client_number&time"][1] == 4:
                if self.i_have_known_myself == False:
                    self.i_am = 4
                    self.i_have_known_myself = True
            
            # send_msg = ''   #----------玩家修改数据的命令
            #self.server.send(bytes(send_msg, 'utf8'))
        except:
            #print("断开")
            break

if __name__ == '__main__':
    #创建游戏实例并运行游戏
    lc = LostCity()
    lc.run_game()
