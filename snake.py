from machine import Pin,freq,Timer,PWM
from LCD import LCDGMT
import time
import math
from random import randint
import _thread
from picdata import data
import gc

classs=[]

#snake game for test
#LCDPin
#BL-->GPIO5
#CS-->GPIO4
#DC-->GPIO3
#RST-->GPIO2
#SDA-->GPIO1
#SCL-->GPIO0
#controllerPin
#com=6
#UP=7
#DOWN=8
#LEFT=9
#RIGHT=10
#MID=11
#SET=12
#RESET=13


class Body():
    def __init__(self,pos):
        self.pos=pos
        self.nextbody=None
        pass

class snake():
    def __init__(self,pos,speedvector):
        self.pos=pos
        self.speedvector=speedvector
        self.nextbody=None
        pass
    
class game():
    def __init__(self,menu,lcd,scorescale=1,difftime=500,lang=0):#0~31,0~23
        self.menu=menu
        self.lcd=lcd
        self.delaytime=difftime
        self.scorescale=scorescale
        self.lang=lang

        self.head=snake([12,16],[1,0])
        self.tail=Body([11,16])
        self.head.nextbody=self.tail
        
        self.is_eat=0
        self.have_food=0
        self.pos_food=None
        self.gameover=0
        self.isconfirom=0
        self.lcd.drawrect(116,156,124,164,0x0000ff)
        self.lcd.drawrect(106,156,114,164,0xff0000)
        self.inputinit()
        
        self.score=0
        self.lcd.drawrect(234,0,240,320,0x000000)
        #self.updatetimer=Timer(period=self.delaytime,mode=Timer.PERIODIC,callback=self.ready4update)
        self.updatetimer=Timer(period=self.delaytime,mode=Timer.PERIODIC,callback=self.update)
        self.drawsocrebord()
        #输入中断初始化
    
    def inputinit(self):
        Pin(6,Pin.OUT).on()
        self.UP=Pin(7,Pin.IN,pull=Pin.PULL_DOWN)
        self.DOWN=Pin(8,Pin.IN,pull=Pin.PULL_DOWN)
        self.LEFT=Pin(9,Pin.IN,pull=Pin.PULL_DOWN)
        self.RIGHT=Pin(10,Pin.IN,pull=Pin.PULL_DOWN)
        self.CONFIROM=Pin(11,Pin.IN,pull=Pin.PULL_DOWN)
        self.SET=Pin(12,Pin.IN,pull=Pin.PULL_DOWN)
        self.RESET=Pin(13,Pin.IN,pull=Pin.PULL_DOWN)
        
        self.UP.irq(handler=self.inputinterrupt,trigger=Pin.IRQ_RISING)
        self.DOWN.irq(self.inputinterrupt,trigger=Pin.IRQ_RISING)
        self.LEFT.irq(self.inputinterrupt,trigger=Pin.IRQ_RISING)
        self.RIGHT.irq(self.inputinterrupt,trigger=Pin.IRQ_RISING)
        self.CONFIROM.irq(self.inputinterrupt,trigger=Pin.IRQ_RISING)
        self.SET.irq(self.inputinterrupt,trigger=Pin.IRQ_RISING)
        self.RESET.irq(self.inputinterrupt,trigger=Pin.IRQ_RISING)
        pass
    
    def inputinterrupt(self,UP):
        if self.UP()==1:
            if not (self.head.speedvector[0]*0+self.head.speedvector[1]*-1)<0:
                self.head.speedvector=[0,-1]
        if self.DOWN()==1:
            if not (self.head.speedvector[0]*0+self.head.speedvector[1]*1)<0:
                self.head.speedvector=[0,1]
        if self.LEFT()==1:
            if not (self.head.speedvector[0]*-1+self.head.speedvector[1]*0)<0:
                self.head.speedvector=[-1,0]
        if self.RIGHT()==1:
            if not (self.head.speedvector[0]*1+self.head.speedvector[1]*0)<0:
                self.head.speedvector=[1,0]
        if self.CONFIROM()==1:
            if self.gameover==1:
                self.isconfirom=1
                pass
        pass
    
    def drawsocrebord(self,update=None):
        if update==None:
            self.lcd.drawrect(0,294,234,320,0x66ccff)#030a72
            if self.lang==0:
                self.lcd.showenstring(0,294,0x030a72,"yourscore:{0}".format(self.score),0x66ccff)
                if self.delaytime==500:
                    self.lcd.showenstring(120,294,0x030a72,"diff:easy",0x66ccff)
                if self.delaytime==300:
                    self.lcd.showenstring(120,294,0x030a72,"diff:mid",0x66ccff)
                if self.delaytime==200:
                    self.lcd.showenstring(120,294,0x030a72,"diff:hard",0x66ccff)
                
            if self.lang==1:
                self.lcd.showzhchar(0,294,0x030a72,"得分:",0x66ccff)
                self.lcd.showenstring(48,294,0x030a72,"{0}".format(self.score),0x66ccff)
                if self.delaytime==500:
                    self.lcd.showzhchar(120,294,0x030a72,"难度:",0x66ccff)
                    self.lcd.showzhchar(168,294,0x030a72,"简单",0x66ccff)
                if self.delaytime==300:
                    self.lcd.showzhchar(120,294,0x030a72,"难度:",0x66ccff)
                    self.lcd.showzhchar(168,294,0x030a72,"中等",0x66ccff)
                if self.delaytime==200:
                    self.lcd.showzhchar(120,294,0x030a72,"难度:",0x66ccff)
                    self.lcd.showzhchar(168,294,0x030a72,"困难",0x66ccff)
            if self.lang==2:
                self.lcd.showzhchar(0,294,0x030a72,"得分:",0x66ccff)
                self.lcd.showenstring(48,294,0x030a72,"{0}".format(self.score),0x66ccff)
                if self.delaytime==500:
                    self.lcd.showzhchar(120,294,0x030a72,"难度:",0x66ccff)
                    self.lcd.showzhchar(168,294,0x030a72,"小杯",0x66ccff)
                if self.delaytime==300:
                    self.lcd.showzhchar(120,294,0x030a72,"难度:",0x66ccff)
                    self.lcd.showzhchar(168,294,0x030a72,"中杯",0x66ccff)
                if self.delaytime==200:
                    self.lcd.showzhchar(120,294,0x030a72,"难度:",0x66ccff)
                    self.lcd.showzhchar(168,294,0x030a72,"大杯",0x66ccff)
                if self.delaytime==50:
                    self.lcd.showzhchar(120,294,0x030a72,"难度:",0x66ccff)
                    self.lcd.showenstring(168,294,0xff0000,"???",0x66ccff)
                
        else:
            if self.lang==0:
                self.lcd.showenstring(80,294,0x030a72,"{0}".format(self.score),0x66ccff)
            else:
                self.lcd.showenstring(48,294,0x030a72,"{0}".format(self.score),0x66ccff)
        pass
    
    #def ready4update(self,updatetimer):
        #_thread.start_new_thread(self.update,(0,))
    
    def update(self,updatetimer):
        uppos=list(self.head.pos)
        self.head.pos[0]+=self.head.speedvector[0]
        self.head.pos[1]+=self.head.speedvector[1]
        if self.head.pos[0]==24:
            self.head.pos[0]=0
        if self.head.pos[1]==30:
            self.head.pos[1]=0
        if self.head.pos[0]==-1:
            self.head.pos[0]=23
        if self.head.pos[1]==-1:
            self.head.pos[1]=29
        if self.head.pos==self.pos_food:
            eating=1
            self.have_food=0
            self.score+=self.scorescale
            self.drawsocrebord(1)
        else:
            eating=0
        ptr=self.head.nextbody
        #temp=ptr.pos
        while ptr:
            temp=[ptr.pos[0],ptr.pos[1]]
            ptr.pos=[uppos[0],uppos[1]]
            uppos=[temp[0],temp[1]]
            
            if ptr.pos==self.head.pos:
                self.gameover=1
                self.updatetimer.deinit()
                self.gameoverfun()
                return
            ptr=ptr.nextbody
            pass
        if eating==1:
            temp=Body(uppos)
            self.tail.nextbody=temp
            self.tail=temp
            uppos=None
        else:
            pass
        self.gerfood()
        self.drawupdate(uppos)
        pass
    
    def gerfood(self):
        while not self.have_food:
            self.pos_food=[randint(1,23),randint(1,29)]
            is_ok=1
            ptr=self.head
            while ptr:
                if ptr.pos==self.pos_food:
                    is_ok=0
                    break
                else:
                    ptr=ptr.nextbody
            if is_ok==1:
                break
        self.have_food=1
    
    def drawupdate(self,erspos=None):
        ptr=self.head.nextbody
        self.lcd.drawrect(abs(self.head.pos[0]*10-4),abs(self.head.pos[1]*10-4),self.head.pos[0]*10+4,self.head.pos[1]*10+4,0x0000ff)
        self.lcd.drawrect(abs(ptr.pos[0]*10-4),abs(ptr.pos[1]*10-4),ptr.pos[0]*10+4,ptr.pos[1]*10+4,0xff0000)
        if not erspos==None:
            self.lcd.drawrect(erspos[0]*10-4,erspos[1]*10-4,erspos[0]*10+4,erspos[1]*10+4,self.lcd.bkcolor)
        if self.pos_food==None:
            pass
        else:
            self.lcd.drawrect(self.pos_food[0]*10-4,self.pos_food[1]*10-4,self.pos_food[0]*10+4,self.pos_food[1]*10+4,0x00ff00)
            
    def gameoverfun(self):
        if self.lang==0:
            self.lcd.showenstring(88,160,0x000000,"gameover")##030a72
            self.lcd.showenstring(88,176,0x000000,"yourscore:{0}".format(self.score))
        if self.lang==1:
            self.lcd.showzhchar(88,176,0x030a72,"得分:")
            self.lcd.showenstring(136,176,0x030a72,"{0}".format(self.score))
            self.lcd.showzhchar(88,160,0x030a72,"游戏结束")
        if self.lang==2:
            self.lcd.showzhchar(88,176,0x030a72,"得分:")
            self.lcd.showenstring(136,176,0x030a72,"{0}".format(self.score))
            self.lcd.showzhchar(88,160,0x030a72,"寄啦!!!")
        while self.CONFIROM()==0:
            pass
        
        self.lcd.clear(1)
        self.menu.drawpic()
        self.menu.drawmenu()
        self.menu.drawptr()
        self.initselect()
        pass
            
class button():
    def __init__(self,top,bottom,color,iszh,fcolor=None,text=None):
        self.top=top
        self.bottom=bottom
        self.color=color
        self.fcolor=fcolor
        self.text=text
        self.center=[(top[0]+bottom[0])/2,(top[1]+bottom[1])/2]
        self.funcptr=None
        self.iszh=iszh
    
    def bind(self,funcptr):
        self.funcptr=funcptr
    
    def __call__(self,argvs):
        self.funcptr(argvs)
            #raise:"plz bind func first"
        pass
    def draw(self,lcd,color=None):
        
        if color:
            color=color
            fcolor=color
        else:
            color=self.color
            fcolor=self.fcolor
        lcd.drawrect(self.top[0],self.top[1],self.bottom[0],self.bottom[1],color)
        if self.iszh==1:
            lcd.showzhchar(self.top[0]+int((abs(self.bottom[0]-self.top[0])-len(self.text)*16)/2),self.top[1]+int((abs(self.top[1]-self.bottom[1])-16)/2),fcolor,self.text,color)#文字居中显示
            
        else:
            lcd.showenstring(self.top[0]+int((abs(self.bottom[0]-self.top[0])-len(self.text)*8)/2),self.top[1]+int((abs(self.top[1]-self.bottom[1])-16)/2),fcolor,self.text,color)#文字居中显示    
            
        
        
        
        pass

class texts():
    def __init__(self,top,content,color,iszh,bkcolor=None):
        self.top=top
        self.content=content
        self.color=color
        self.bkcolor=bkcolor
        self.upponlen=len(content)
        self.iszh=iszh
        pass
    def draw(self,lcd,color=None):
        if color:
            color=color
            fcolor=color
        else:
            color=self.bkcolor
            fcolor=self.color
        if self.iszh==1:
            
            if self.content=="eatingsnake":
                lcd.showenstring(self.top[0],self.top[1],fcolor,self.content,color)
            else:
                lcd.showzhchar(self.top[0],self.top[1],fcolor,self.content,color)
        else:
            lcd.showenstring(self.top[0],self.top[1],fcolor,self.content,color)
    
class pic():
    def __init__(self,top,bottom,data):
        self.top=top
        self.bottom=bottom
        self.picdata=[]
        
    def draw(self,lcd,color=None):
        lcd.drawpixel()
        

class menu(game):
    def __init__(self,lcd):
        self.lcd=lcd
        self.buttons=[]
        self.texts=[]
        self.pics=[]
        self.argvs=[]
        self.bkcolor=0xffffff
        self.pcolor=0x000000
        self.difftimes=500
        self.diffchscale=1
        
        self.selecptr=0
        self.initselect()
        self.langptr=0
        
        pass
    
    def menuselect(self,PIN):#interrupt
        if self.UP()==1:
            if not self.selecptr==len(self.buttons)-1:
                self.drawptr(0xffffff)
                self.selecptr+=1
                self.drawptr()
            
        if self.DOWN()==1:
            if not self.selecptr==0:
                self.drawptr(0xffffff)
                self.selecptr-=1
                self.drawptr()
                
        if self.CONFIROM()==1:
            self.buttons[self.selecptr](self.argvs[self.selecptr])
            self.drawptr(0xffffff)
            
        if self.SET()==1:
            if self.langptr==2:#必须是梗体中文才能触发
                lasttime=time.time()
                isready=1
                while not time.time()-lasttime==3:
                    if self.SET()==1:
                        pass
                    else:
                        isready=0
                if isready==1:
                    self.lcd.drawrect(40,60,200,140,0xffffff)
                    self.drawmenu(0xffffff)
                    self.drawptr(0xffffff)
                    super(menu,self).__init__(self,self.lcd,50,50,self.langptr)
                    #super(menu,self).__init__(self,self.lcd,scorescale,difftimes,self.langptr)
                

        
        
    
    def initselect(self):#初始化选择
        Pin(6,Pin.OUT).on()
        self.UP=Pin(7,Pin.IN,pull=Pin.PULL_DOWN)
        self.DOWN=Pin(8,Pin.IN,pull=Pin.PULL_DOWN)
        self.LEFT=Pin(9,Pin.IN,pull=Pin.PULL_DOWN)
        self.RIGHT=Pin(10,Pin.IN,pull=Pin.PULL_DOWN)
        self.CONFIROM=Pin(11,Pin.IN,pull=Pin.PULL_DOWN)
        self.SET=Pin(12,Pin.IN,pull=Pin.PULL_DOWN)
        self.RESET=Pin(13,Pin.IN,pull=Pin.PULL_DOWN)
        
        self.UP.irq(self.menuselect,trigger=Pin.IRQ_RISING)
        self.DOWN.irq(self.menuselect,trigger=Pin.IRQ_RISING)
        self.LEFT.irq(self.menuselect,trigger=Pin.IRQ_RISING)
        self.RIGHT.irq(self.menuselect,trigger=Pin.IRQ_RISING)
        self.CONFIROM.irq(self.menuselect,trigger=Pin.IRQ_RISING)
        self.SET.irq(self.menuselect,trigger=Pin.IRQ_RISING)
        self.RESET.irq(self.menuselect,trigger=Pin.IRQ_RISING)
        pass
    
    def createbutton(self,top,bottom,func,argv,color,fcolor=0x000000,text=None):
        if self.langptr==0:
            temp=button(top,bottom,color,0,fcolor,text)    
        else:
            temp=button(top,bottom,color,1,fcolor,text)    
        temp.bind(func) 
        self.buttons.append(temp)
        self.argvs.append(argv)
        pass
    
    def createtext(self,top,content,color,bkcolor=None):
        if not bkcolor:
            bkcolor=self.bkcolor
        if self.langptr==0:
            self.texts.append(texts(top,content,color,0,bkcolor))
        else:
            self.texts.append(texts(top,content,color,1,bkcolor))
        return self.texts[len(self.texts)-1]
        
    def createpic(self,top,bottom,data):
        self.pics.append(pic(top,bottom,data))
        
    def desbutton(self,ptr=None,text=None):
        if ptr:
            self.buttons.remove(self.buttons[ptr])
        if text:
            for i in self.buttons:
                if i.text==text:
                    self.buttons.remove(i)
    
    def drawmenu(self,color=None):#外部菜单绘图函数
        for i in self.texts:
            i.draw(self.lcd,color)
        for i in self.buttons:
            i.draw(self.lcd,color)
        for i in self.pics:
            i.draw(self.lcd,color)
    
    def drawptr(self,color=0xffff00):
        self.lcd.drawrect(self.buttons[self.selecptr].top[0],self.buttons[self.selecptr].top[1]-5,self.buttons[self.selecptr].bottom[0],self.buttons[self.selecptr].top[1],color)
        pass
    
    def start(self,scorescale=1,difftimes=500):
        super(menu,self).__init__(self,self.lcd,scorescale,difftimes,self.langptr)
        
    def drawpic(self):
        sx=75
        sy=80
        ex=165
        ey=120
        self.lcd.writecmd(0x2a)
        self.lcd.writedata(0x00)
        self.lcd.writedata(sx)
        self.lcd.writedata(0x00)
        self.lcd.writedata((ex-1))

        self.lcd.writecmd(0x2b)
        self.lcd.writedata(sy>>8)
        self.lcd.writedata(sy&0xff)
        self.lcd.writedata((ey-1)>>8)
        self.lcd.writedata((ey-1)&0xff)
        self.lcd.writecmd(0x2c)
        gc.collect()
        for i in list(data):
            self.lcd.writeRGB(i)
        pass
            

def easy(argv):
    argv[0].lcd.drawrect(40,60,200,140,0xffffff)
    argv[0].drawmenu(0xffffff)
    argv[0].drawptr(0xffffff)
    argv[0].start(1,500)
    pass

def mid(argv):
    argv[0].lcd.drawrect(40,60,200,140,0xffffff)
    argv[0].drawmenu(0xffffff)
    argv[0].drawptr(0xffffff)
    argv[0].start(5,300)
    pass

def hard(argv):
    argv[0].lcd.drawrect(40,60,200,140,0xffffff)
    argv[0].drawmenu(0xffffff)
    argv[0].drawptr(0xffffff)
    argv[0].start(10,200)
    pass

def shiftlang(argv):
    argv[0].langptr+=1
    if argv[0].langptr==3:
        argv[0].langptr=0
    argv[0].drawmenu(0xffffff)
    argv[0].drawptr(0xffffff)
    argv[0].buttons=[]
    argv[0].texts=[]
    initmenu(argv[0])
    argv[0].drawmenu()
    argv[0].drawptr()
    pass

def initmenu(handle):
    if handle.langptr==0:
        handle.createbutton([40,175],[80,200],easy,[handle],0x66ccff,text="easy",fcolor=0x00ff00)
        handle.createbutton([90,175],[130,200],mid,[handle],0x66ccff,text="mid",fcolor=0x000000)
        handle.createbutton([140,175],[180,200],hard,[handle],0x66ccff,text="hard",fcolor=0xff0000)
        handle.createbutton([40,210],[180,235],shiftlang,[handle],0x66ccff,text="English",fcolor=0x000000)
    if handle.langptr==1:
        handle.createbutton([40,175],[80,200],easy,[handle],0x66ccff,text="简单",fcolor=0x00ff00)
        handle.createbutton([90,175],[130,200],mid,[handle],0x66ccff,text="中等",fcolor=0x000000)
        handle.createbutton([140,175],[180,200],hard,[handle],0x66ccff,text="困难",fcolor=0xff0000)
        handle.createbutton([40,210],[180,235],shiftlang,[handle],0x66ccff,text="中文",fcolor=0x000000)
    if handle.langptr==2:
        handle.createbutton([40,175],[80,200],easy,[handle],0x66ccff,text="小杯",fcolor=0x00ff00)
        handle.createbutton([90,175],[130,200],mid,[handle],0x66ccff,text="中杯",fcolor=0x000000)
        handle.createbutton([140,175],[180,200],hard,[handle],0x66ccff,text="大杯",fcolor=0xff0000)
        handle.createbutton([40,210],[180,235],shiftlang,[handle],0x66ccff,text="梗体",fcolor=0x000000)
    
    pass


if __name__=="__main__":
    freq(270000000)
    lcd=LCDGMT(5,4,3,2,1,0,240,320)
    lcd.LCD_init()
    led=Pin(25,Pin.OUT)
    led.on()
    lcd.clear(1)
    led.off()
    
#--------------------系统初始化----------------------
    #g1=game(lcd)
    mainmenu=menu(lcd)
    initmenu(mainmenu)
    mainmenu.drawpic()
    mainmenu.drawmenu()
    mainmenu.drawptr()
    while 1:
        
        pass
    pass




    



