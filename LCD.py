from machine import Pin,freq,PWM
import rp2
import time
from chars import charpts,zhcharpts

munpts=[[0x00, 0x00, 0x00, 0x18, 0x24, 0x42, 0x42, 0x42, 0x42, 0x42, 0x42, 0x42, 0x24, 0x18, 0x00, 0x00], #0
[0x00, 0x00, 0x00, 0x08, 0x38, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x3e, 0x00, 0x00],         #1
[0x00, 0x00, 0x00, 0x3c, 0x42, 0x42, 0x42, 0x02, 0x04, 0x08, 0x10, 0x20, 0x42, 0x7e, 0x00, 0x00],         #2
[0x00, 0x00, 0x00, 0x3c, 0x42, 0x42, 0x02, 0x04, 0x18, 0x04, 0x02, 0x42, 0x42, 0x3c, 0x00, 0x00],         #3
[0x00, 0x00, 0x00, 0x04, 0x0c, 0x0c, 0x14, 0x24, 0x24, 0x44, 0x7f, 0x04, 0x04, 0x1f, 0x00, 0x00],         #4
[0x00, 0x00, 0x00, 0x7e, 0x40, 0x40, 0x40, 0x78, 0x44, 0x02, 0x02, 0x42, 0x44, 0x38, 0x00, 0x00],         #5
[0x00, 0x00, 0x00, 0x18, 0x24, 0x40, 0x40, 0x5c, 0x62, 0x42, 0x42, 0x42, 0x22, 0x1c, 0x00, 0x00],         #6
[0x00, 0x00, 0x00, 0x7e, 0x42, 0x04, 0x04, 0x08, 0x08, 0x10, 0x10, 0x10, 0x10, 0x10, 0x00, 0x00],         #7
[0x00, 0x00, 0x00, 0x3c, 0x42, 0x42, 0x42, 0x24, 0x18, 0x24, 0x42, 0x42, 0x42, 0x3c, 0x00, 0x00],         #8
[0x00, 0x00, 0x00, 0x38, 0x44, 0x42, 0x42, 0x42, 0x46, 0x3a, 0x02, 0x02, 0x24, 0x18, 0x00, 0x00]]         #9

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW,
             out_init=(rp2.PIO.OUT_LOW,),
             out_shiftdir=rp2.PIO.SHIFT_LEFT,
             autopull=True,
             pull_thresh=8
             )
def pinwrite():
    wrap_target()
    out(x,1)                .side(0)        [1]
    mov(pins,x)             .side(0)        [2]
    nop()                   .side(1)        [2]
    irq(0)
    wrap()
    pass

class LCDGMT():
    def __init__(self,BL,CS,DC,RST,SDA,SCL,height,wide):
        self.H=height
        self.W=wide
        self.BL=PWM(Pin(BL,Pin.OUT))
        self.CS=Pin(CS,Pin.OUT)
        self.DC=Pin(DC,Pin.OUT)
        self.RST=Pin(RST,Pin.OUT)
        self.SDA=Pin(SDA,Pin.OUT)
        self.SCL=Pin(SCL,Pin.OUT)
        self.bkcolor=0x00
        self.lightlevel=100
        self.BL.freq(10000)
        self.BL.duty_u16(65536)
        
        self.LCDPIN=rp2.StateMachine(0,prog=pinwrite,freq=200000000,sideset_base=self.SCL,out_base=self.SDA)
        self.LCDPIN.active(1)
        
    def changelight(self,percent):
        self.lightlevel=percent
        self.BL.duty_u16(int((percent/100)*65536))
        
    def writecmd(self,data):
        self.DC.off()
        self.CS.off()
        self.SCL.off()
        self.LCDPIN.put(data<<24)

    def writedata(self,data):
        self.DC.on()
        self.CS.off()
        self.SCL.off()
        self.LCDPIN.put(data<<24)
        
    def writeRGB(self,data):
        self.DC.on()
        self.CS.off()
        self.SCL.off()
        self.LCDPIN.put(data<<8)
        self.LCDPIN.put(data<<16)
        self.LCDPIN.put(data<<24)

    def openBL(self):
        self.CS.off()
        self.changelight(self.lightlevel)
        self.CS.on()
        
    
    def closeBL(self):
        self.CS.off()
        self.changelight(0)
        self.CS.on()

    def LCD_init(self):
        self.CS.off()
        self.RST.off()
        self.RST.on()
        self.CS.on()
        self.writecmd(0x11)
        
        time.sleep(0.12)
        self.writecmd(0x2a)
        self.writedata(0x00)
        self.writedata(0x00)
        self.writedata(0x00)
        self.writedata(0xef)

        self.writecmd(0x2b)
        self.writedata(0x00)
        self.writedata(0x28)
        self.writedata(0x01)
        self.writedata(0x17)

        self.writecmd(0xb2)
        self.writedata(0x0c)
        self.writedata(0x0c)
        self.writedata(0x00)
        self.writedata(0x33)
        self.writedata(0x33)

        self.writecmd(0x20)

        self.writecmd(0xb7)
        self.writedata(0x56)

        self.writecmd(0xbb)
        self.writedata(0x18)

        self.writecmd(0xc0)
        self.writedata(0x2c)

        self.writecmd(0xc2)
        self.writedata(0x01)

        self.writecmd(0xc3)
        self.writedata(0x1f)

        self.writecmd(0xc4)
        self.writedata(0x20)

        self.writecmd(0xc6)
        self.writedata(0x0f)

        self.writecmd(0xd0)
        self.writedata(0xa6)
        self.writedata(0xa1)


        self.writecmd(0xe0)
        self.writedata(0xd0)
        self.writedata(0x0d)
        self.writedata(0x14)
        self.writedata(0x0b)
        self.writedata(0x0b)
        self.writedata(0x07)
        self.writedata(0x3d)
        self.writedata(0x44)
        self.writedata(0x50)
        self.writedata(0x08)
        self.writedata(0x13)
        self.writedata(0x13)
        self.writedata(0x2d)
        self.writedata(0x32)

        self.writecmd(0xe1)
        self.writedata(0xd0)
        self.writedata(0x0d)
        self.writedata(0x14)
        self.writedata(0x0b)
        self.writedata(0x0b)
        self.writedata(0x07)
        self.writedata(0x3d)
        self.writedata(0x44)
        self.writedata(0x50)
        self.writedata(0x08)
        self.writedata(0x13)
        self.writedata(0x13)
        self.writedata(0x2d)
        self.writedata(0x32)

        self.writecmd(0x36)
        self.writedata(0x00)
        self.writecmd(0x3a)
        self.writedata(0x66)
        self.writecmd(0xe7)
        self.writedata(0x00)
        self.writecmd(0x21)
        self.writecmd(0x29)
        self.writecmd(0x2c)
        pass

    def clear(self,BOW=0):
        self.writecmd(0x2a)
        self.writedata(0x00)
        self.writedata(0x00)
        self.writedata(0x00)
        self.writedata(0xef)

        self.writecmd(0x2b)
        self.writedata(0x00)
        self.writedata(0x00)
        self.writedata(0x01)
        self.writedata(0x3f)
        self.writecmd(0x2c)
        
        self.DC.on()
        self.CS.off()
        self.SCL.off()
        
        self.SDA.value(BOW)
        if BOW==1:
            self.bkcolor=0xffffff
            BOW=0xff
        else :
            self.bkcolor=0x000000
            BOW=0x00
        
        for i in range(self.H):
            for j in range(self.W):
                self.LCDPIN.put(BOW<<24)
                self.LCDPIN.put(BOW<<24)
                self.LCDPIN.put(BOW<<24)
        self.CS.on()
    
    def drawtest(self):
        self.writecmd(0x2a)
        self.writedata(0x00)
        self.writedata(0x00)
        self.writedata(0x00)
        self.writedata(0x0a)

        self.writecmd(0x2b)
        self.writedata(0x00)
        self.writedata(0x00)
        self.writedata(0x00)
        self.writedata(0x0a)
        self.writecmd(0x2c)
        for i in range(10):
            for j in range(10):
                self.writeRGB(0xffffff)
    #--------------------------------------------------------devide
    def drawpixel(self,x,y,color):
        self.writecmd(0x2a)
        self.writedata(0x00)
        self.writedata(x)
        self.writedata(0x00)
        self.writedata(x+1)

        self.writecmd(0x2b)
        self.writedata(y>>8)
        self.writedata(y&0xff)
        y=y+1
        self.writedata(y>>8)
        self.writedata(y&0xff)
        self.writecmd(0x2c)
        self.writeRGB(color)
        pass

    def drawrect(self,sx,sy,ex,ey,color):
        self.writecmd(0x2a)
        self.writedata(0x00)
        self.writedata(sx)
        self.writedata(0x00)
        self.writedata((ex-1))

        self.writecmd(0x2b)
        self.writedata(sy>>8)
        self.writedata(sy&0xff)
        self.writedata((ey-1)>>8)
        self.writedata((ey-1)&0xff)
        self.writecmd(0x2c)
        for i in range(ey-sy):
            for j in range(ex-sx):
                self.writeRGB(color)

    def drawline(self,sx,sy,ex,ey,color):
        vector=[abs(ey-sy),abs(ex-sx)]
        if vector[0]==0:
            vector=[0,0]
            pass
        else:
            vector[1]/=vector[0]
            vector[0]=1
        for i in range(ex-sx):
            self.drawpixel(i+sx,int(sy+(i*vector[1])),color)
    
    def drawcricl(self,x,y,r,color):
        for i in range(2*r):
            for j in range(2*r):
                if (abs(((r-j)*(r-j))+((r-i)*(r-i))-(r*r)))**(0.5)<10:
                    self.drawpixel(j+r,i+r,color)
                pass

        pass 
    
    def showmun(self,x,y,color,data):
        p=0
        for j in munpts[data]:
            for i in range(8):
                if (j<<i)&0x80:
                    self.drawpixel(x+i,y+p,color)
                else:
                    self.drawpixel(x+i,y+p,self.bkcolor)
            p+=1
    def showzhchar(self,x,y,color,data,bkcolor=None):
        if bkcolor:
            bkcolor=bkcolor
        else:
            bkcolor=self.bkcolor
        self.writecmd(0x2a)
        self.writedata(0x00)
        self.writedata(x)
        self.writedata(0x00)
        self.writedata((x-1)+len(data)*16)#(ex-1))
        
        self.writecmd(0x2b)
        self.writedata(y>>8)
        self.writedata(y&0xff)
        self.writedata((y+15)>>8)
        self.writedata((y+15)&0xff)
        self.writecmd(0x2c)
        for i in zhcharpts.get(data):
            for j in range(8):
                if ((i<<j)&0x80)==0x80:
                    self.writeRGB(color)
                else:
                    self.writeRGB(bkcolor)
                pass
            
        pass
        
    def showenchar(self,x,y,color,data,bkcolor=None):
        if bkcolor:
            bkcolor=bkcolor
        else:
            bkcolor=self.bkcolor
        p=0
        for i in charpts.get(data):
            for j in range(8):
                if (i<<j)&0x80:
                    self.drawpixel(x+j,y+p,color)
                else:
                    self.drawpixel(x+j,y+p,bkcolor)
            p+=1

    def showenstring(self,x,y,color,data,bkcolor=None):
        if bkcolor:
            bkcolor=bkcolor
        else:
            bkcolor=self.bkcolor
        for i in range(len(data)):
            self.showenchar(x+i*8,y,color,data[i],bkcolor)


if __name__=="__main__":
    freq(200000000)
    lcd=LCDGMT(5,4,3,2,1,0,320,240)
    lcd.LCD_init()
    lcd.openBL()
    lcd.clear(1)
