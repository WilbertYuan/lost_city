import pyautogui
class Settings:
    """存储游戏《失落之城》中所有设置的类"""
    def __init__(self):
        #初始化游戏的设置
        #获取屏幕分辨率
        self.width,self.height = pyautogui.size()

# ############################测试缩小
#         self.width/=3
#         self.height/=3
# ############################  

        self.ratio_playerscreen = self.width/self.height
        self.ratio_mapcreen = 2300/1350

        if(self.ratio_playerscreen > self.ratio_mapcreen):
            self.height_game_screen = self.height
            self.width_game_screen = self.ratio_mapcreen * self.height_game_screen
            self.width_game_screen -= 80*self.ratio_mapcreen
            self.height_game_screen -= 80
        else:
            self.width_game_screen = self.width
            self.height_game_screen = self.width_game_screen / self.ratio_mapcreen

        self.RATIO_ALL = self.height_game_screen/1350
        

        self.turn_money = 100
        self.money_color = (234,192,38)# 金钱 ： R234 G192 B38
        self.black_color = (0,0,0)# 黑色 ： R 0 G 0 B 0
        self.text_color = (255,250,211)# 字体 ： R255 G250 B211
        self.bg_color = (255,235,158)




