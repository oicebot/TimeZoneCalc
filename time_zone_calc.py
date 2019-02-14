#!/usr/bin/env python3
# -*- coding:utf-8 -*-

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
    
try:
    import ttk
except ImportError:
    import tk.ttk as ttk
    
try:
    import pygubu
except:
    print("Please Install pygubu before use this app.")
    exit()

"""
"""

TIME_ZONE_INFO = {
    -12 : "日界线西",
    -11 : "中途岛，萨摩亚群岛",
    -10 : "夏威夷",
    -9  : "阿拉斯加",
    -8  : "美国太平洋时间，下加利福尼亚",
    -7  : "美国山地时间，亚利桑那，拉巴斯",
    -6  : "中美洲",
    -5  : "美国东部时间，波哥大，利马",
    -4  : "大西洋时间，拉巴斯，圣地亚哥",
    -3  : "巴西利亚，布宜诺斯艾利斯，格陵兰",
    -2  : "中大西洋",
    -1  : "佛得角群岛，亚速尔群岛",
     0  : "格林威治标准时间，都柏林，伦敦",
     1  : "阿姆斯特丹，柏林，罗马，布达佩斯",
     2  : "贝鲁特，开罗，赫尔辛基，耶路撒冷",
     3  : "巴格达，莫斯科，德黑兰",
     4  : "高加索标准时间",
     5  : "伊斯兰堡，加德满都",
     6  : "阿拉木图，新西伯利亚，仰光",
     7  : "曼谷，河内，雅加达",
     8  : "北京，上海，香港，吉隆坡",
     9  : "大阪，札幌，东京，汉城",
     10 : "关岛，堪培拉，墨尔本，海参崴",
     11 : "所罗门群岛",
     12 : "斐济，惠灵顿，堪察加半岛",
    }


class Application:
    def __init__(self,master):
    
        self.cb1 = False
        self.cb2 = False
        self.master = master
        
        # 1: Create a builder
        self.builder = builder = pygubu.Builder()

        # 2: Load an ui file
        builder.add_from_file('main.ui')

        # 3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('mainwindow', master)
        
        builder.connect_callbacks(self)
        self.refreshWidgets(None)
        
    def refreshWidgets(self, event):
        global TIME_ZONE_INFO
        
        label1 = self.builder.get_object("Label_1")
        label2 = self.builder.get_object("Label_3")
        
        from_time_zone = int(self.builder.get_object("Scale_1").get())
        label1.configure(text="来源时区: %+2d %s" % (from_time_zone, TIME_ZONE_INFO[from_time_zone]))
        
        to_time_zone = int(self.builder.get_object("Scale_2").get())
        label2.configure(text="目标时区: %+2d %s" % (to_time_zone, TIME_ZONE_INFO[to_time_zone]))

    def calc_Button_clicked(self):
        from_time_zone = int(self.builder.get_object("Scale_1").get())
        to_time_zone   = int(self.builder.get_object("Scale_2").get())
        hours          = int(self.builder.get_object("Spinbox_1").get())
        mins           = int(self.builder.get_object("Spinbox_2").get())
        from_time      = "%d:%d" % (hours,mins)

        summer_time    = [0,0]
        summer_time[0] = self.cb1
        summer_time[1] = self.cb2

        result_info = timeZoneCalc(from_time_zone, to_time_zone, from_time, summer_time)
        
        self.builder.get_object("Label_5").config(text=result_info)
        
    def cb1_check(self):
        if self.cb1:
            self.cb1 = False
        else:
            self.cb1 = True
        
    def cb2_check(self):
        if self.cb2:
            self.cb2 = False
        else:
            self.cb2 = True

def timeZoneCalc(from_time_zone, to_time_zone, from_time, summer_time=[False,False]):
    global TIME_ZONE_INFO

    try:
        hours,mins=from_time.split(":")
    except ValueError:
        hours = int(from_time)
        mins  = 0
    except AttributeError:
        hours = from_time
        mins  = 0

    hours = int(hours)
    mins = int(mins)

    to_time = "%+d 时区的 %02d:%02d %s相当于: %+d 时区中" % (from_time_zone, hours, mins, summer_time[0] and "(夏令时)" or "", to_time_zone)

    if summer_time[0]:
        to_time_zone = to_time_zone - 1
    if summer_time[1]:
        from_time_zone = from_time_zone - 1
    
    hours = hours + (to_time_zone - from_time_zone)
    
    days = "当天"
    
    if hours >= 24:
        days = "后一天"
    elif hours < 0:
        days = "前一天"
        
    hours = hours % 24
    
    #print "%+02d 时区： %s" % (from_time_zone, TIME_ZONE_INFO[from_time_zone])
    #print "%+02d 时区： %s" % (to_time_zone, TIME_ZONE_INFO[to_time_zone])
       
    to_time = to_time + "%s的 %02d:%02d %s" % (days, hours , mins, summer_time[1] and "(夏令时)" or "")

    return to_time



if __name__ == "__main__":
    """
    Syntax:  (  int     from_time_zone,
                int     to_time_zone, 
                str     time_in_from_time_zone,
                boolean [summertime_From, summertime_to] 
             )

    print timeZoneCalc(-8,8,20)
    print "----------"
    print timeZoneCalc(-5,8,20,[0,0])
    print "----------"
    print timeZoneCalc(8,-5,8,[0,0])
    print "----------"
    print timeZoneCalc(8,-5,"8:19",[0,1])
    print "----------"
    print timeZoneCalc(-5,8,"20:19",[1,0])
    print "----------"
    print timeZoneCalc(-5,8,"20:19",[0,0])
    print "----------"
    print timeZoneCalc(-5,8,"23:44",[1,0])
       
    """
    root = tk.Tk()
    app = Application(root)
    app.master.title("时区转换器")
    img = tk.PhotoImage(file="internet-web-browser.png")
    root.tk.call("wm","iconphoto", root._w, img)
    root.mainloop()
    
    
    
    
    
    
    
