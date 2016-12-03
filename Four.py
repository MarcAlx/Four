#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-
# Developed by Marc-Alexandre Blanchard

from tkinter import *
import os,tkinter.messagebox,random,time

class Application(object):
    """ Four """
    _Version,_Name=1.0,"Four"
    _TYPE,_POSX,_POSY,_NEXTPIECE,_CHECKTIME,_GRAVITYTIME,_MOVETIME,_REFRESHTIME,_WIDTH,_HEIGHT,_MATRIXWIDTH,_MATRIXHEIGHT,_BLOCKSIZE,_FREE,_canMove,_canMoveDown=0,4,0,0,25,1000,75,100,1080,720,12,22,30,0,True,True
    _MATRIX,_CURRENTPIECE,_RDV,_CANVASSTAT,_LABELSSTAT,_STAT,_Colors,_PIECES=[],[],[],[None],[None],[None],["ivory","cyan","yellow","violet","orange","blue","red","green","brown"],[[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,2,2,0],[0,2,2,0],[0,0,0,0]],[[0,0,0,0],[0,3,3,3],[0,0,3,0],[0,0,0,0]],[[0,0,0,0],[0,4,4,4],[0,4,0,0],[0,0,0,0]],[[0,0,0,0],[0,5,5,5],[0,0,0,5],[0,0,0,0]],[[0,0,0,0],[0,6,6,0],[0,0,6,6],[0,0,0,0]],[[0,0,0,0],[0,0,7,7],[0,7,7,0],[0,0,0,0]]]
    
    def __init__(self):
        self._tk = Tk()
        self._tk.protocol("WM_DELETE_WINDOW", self.onQuit)
        self._tk.title(self._Name)
        self.createMenuBar()
        self._tk.lift()
        self._tk.resizable(width=False, height=False)
        
        self.initStat()
        
        self._blockLeft=Frame(self._tk)
        self._labelStat=Label(self._blockLeft, text="Statistics",font=("Lucida", 32),width=10)
        self._labelStat.pack()
        for i in range(1,8,1):
            self._block=Frame(self._blockLeft)
            self._CANVASSTAT.append(Canvas(self._block, width=60, height=60))
            self._CANVASSTAT[i].create_rectangle(0, 0, 60, 60, fill=self._Colors[0])
            self._CANVASSTAT[i].pack(side = LEFT)
            for j in range (0,4,1):
                for k in range (0,4,1):
                    if(self._PIECES[i][j][k]!=0):
                        self._CANVASSTAT[i].create_rectangle((k*10)+10,(j*10)+10,(k*10)+20,(j*10)+20,fill=self._Colors[i])
            self._LABELSSTAT.append(Label(self._block,textvariable=self._STAT[i],font=("Lucida", 32)))
            self._LABELSSTAT[i].pack(side=RIGHT)
            self._block.pack()
        self._blockLeft.pack(side=LEFT)

        self._blockMiddle = Frame(self._tk)
        self._FRAME = Canvas(self._blockMiddle, width=self._BLOCKSIZE*self._MATRIXWIDTH, height=self._BLOCKSIZE*self._MATRIXHEIGHT, bg=self._Colors[0])
        if(sys.platform.startswith("darwin")):
            self._tk.bind_all('<Command-q>',self.quit)
            self._tk.bind_all('<Command-Q>',self.quit)
        self._FRAME.bind_all('<Key>',self.onKeyPress)
        self._FRAME.bind_all('<KeyRelease-S>',self.onDownRelease)
        self._FRAME.bind_all('<KeyRelease-s>',self.onDownRelease)
        self._FRAME.bind_all('<Left>',self.onLeftPress)
        self._FRAME.bind_all('<Right>',self.onRightPress)
        self._FRAME.bind_all('<Up>',self.onUpPress)
        self._FRAME.bind_all('<Down>',self.onDownPress)
        self._FRAME.bind_all('<KeyRelease-Down>',self.onDownRelease)
        self._FRAME.pack()
        self._blockMiddle.pack(side = LEFT)

        self._blockRight = Frame(self._tk)
        self._labelTitleScore=Label(self._blockRight, text="Score",font=("Lucida", 32),width=10)
        self._labelTitleScore.pack()
        self._Score=Label(self._blockRight, text="0",textvariable=self._SCORE,font=("Lucida", 32),width=10)
        self._Score.pack()
        self._labelNext=Label(self._blockRight, text="Next",font=("Lucida", 38),width=10,height=2)
        self._labelNext.pack()
        self._Next=Canvas(self._blockRight, width=60, height=60)
        self._Next.create_rectangle(0, 0, 60, 60, fill=self._Colors[0])
        self._Next.pack()
        self._labelTitleLines=Label(self._blockRight, text="Lines",font=("Lucida", 32),width=10)
        self._labelTitleLines.pack()
        self._labelLines=Label(self._blockRight, text="0",textvariable=self._NBLINES,font=("Lucida", 32),width=10)
        self._labelLines.pack()
        self._labelTitleLevel=Label(self._blockRight, text="Level",font=("Lucida", 32),width=10)
        self._labelTitleLevel.pack()
        self._labelLevel=Label(self._blockRight, text="0",textvariable=self._CURRENTLVL,font=("Lucida", 32),width=10)
        self._labelLevel.pack()
        self._labelTitleHighScore=Label(self._blockRight, text="High Score",font=("Lucida", 32),width=10)
        self._labelTitleHighScore.pack()
        self._HighScore=Label(self._blockRight, text="0",textvariable=self._HIGHSCORE,font=("Lucida", 32),width=10)
        self._HighScore.pack()
        self._buttonStartRestart=Button(self._blockRight,text="Start/Restart",width=10,command=self.init)
        self._buttonStartRestart.pack()
        self._labelTitleLines=Label(self._blockRight, text="Help & How-to",font=("Lucida", 20))
        self._labelTitleLines.pack()
        self._labelTitleLines=Label(self._blockRight, text="(press H)",font=("Lucida", 20))
        self._labelTitleLines.pack()
        self._blockRight.pack(side=RIGHT)

        self.init()

    def mainloop(self):
        self._tk.mainloop()
    
    def about(self):
        tkinter.messagebox.showinfo("About", "Developed by\n\nMarc-Alexandre Blanchard")
    
    def createMenuBar(self):
        self.menubar = Menu(self._tk)
        self.appmenu = Menu(self.menubar, tearoff=0)
        self.appmenu.add_command(label="Quit", command=self._tk.destroy)
        self.menubar.add_cascade(label=self._Name, menu=self.appmenu)
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About", command=self.about)
        self.helpmenu.add_command(label="Help & How-To", command=self.help)
        self.helpmenu.add_command(label="Version", command=self.version)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        self._tk.config(menu=self.menubar)
    
    def help(self):
        tkinter.messagebox.showinfo("Help & How-To", "About : A\nHelp & How-To : H\nVersion : V\n\nMove : Q S D ← ↓ →\nLeft Rotation : W L\nRight Rotation : X M ↑ Z \nSkip gravity : Spacebar\n\nRestart : R\n")
    
    def onDownPress(self,event):
        self.getdown()
    
    def onDownRelease(self,event):
        self.allowMove()
    
    def onKeyPress(self,event):
        if(event.char=="q" or event.char=="Q"):
            self.toTheLeft()
        elif(event.char=="d" or event.char=="D"):
            self.toTheRight()
        elif(event.char=="l" or event.char=="L" or event.char=="w" or event.char=="W"):
            self.rotateLeft()
        elif(event.char=="x" or event.char=="X" or event.char=="m" or event.char=="M" or event.char=="z" or event.char=="Z"):
            self.rotateRight()
        elif(event.char=="s" or event.char=="S"):
            self.getdown()
        elif(event.char==" "):
            self.quick()
        elif(event.char=="a" or event.char=="A"):
            self.about()
        elif(event.char=="h" or event.char=="H"):
            self.help()
        elif(event.char=="v" or event.char=="V"):
            self.version()
        elif(event.char=="r" or event.char=="R"):
            self.init()
    
    def onLeftPress(self,event):
        self.toTheLeft()
    
    def onRightPress(self,event):
        self.toTheRight()
    
    def onUpPress(self,event):
        self.rotateRight()
    
    def onQuit(self):
        self.cancelation()
        self._tk.destroy()

    def quit(self,event):
        self.onQuit()

    def version(self):
        tkinter.messagebox.showinfo("Version", "Version "+str(self._Version))

    def addPiece(self):
        self.cancelation()
        self._SCORE.set(self._SCORE.get()+((self._CURRENTLVL.get()+1)*4))
        self._TYPE,self._CURRENTPIECE,self._POSX,self._POSY,self._FREE,self._canMove,self._canMoveDown=self._NEXTPIECE,self._PIECES[self._NEXTPIECE],4,0,0,True,True
        self._STAT[self._NEXTPIECE].set(self._STAT[self._NEXTPIECE].get()+1)
        self._NEXTPIECE=random.randint(1,7)
        if(self._CURRENTLVL.get()<=9):
            self._GRAVITYTIME=1000-(self._CURRENTLVL.get()*100)
        if(self._CURRENTLVL.get()<9 and self._NBLINES.get()>=12):
            self._CURRENTLVL.set(int(self._NBLINES.get()/12))
        for i in range (0,self._MATRIXHEIGHT,1):
            for j in range(0,self._MATRIXWIDTH,1):
                if(self._MATRIX[i][j]==0):
                    self._FREE+=1
        self._Next.create_rectangle(0,0,60,60, fill=self._Colors[0])
        for j in range (0,4,1):
            for k in range (0,4,1):
                if(self._PIECES[self._NEXTPIECE][j][k]!=0):
                    self._Next.create_rectangle((k*10)+10,(j*10)+10,(k*10)+20,(j*10)+20, fill=self._Colors[self._NEXTPIECE])
        self.gravity()
        self.draw()
        self.check()

    def allowMove(self):
        if(self._CURRENTLVL.get()<=9):
            self._canMove,self._GRAVITYTIME=True,(1000-(self._CURRENTLVL.get()*100))
        else:
            self._canMove,self._GRAVITYTIME=True,100

    def cancelation(self):
        for i in self._RDV:
            self._FRAME.after_cancel(i)

    def check(self):
        for i in range (0,4,1):
            for j in range (0,4,1):
                if(self._CURRENTPIECE[i][j]!=0):
                    if(self._MATRIX[self._POSY+i][self._POSX+j]!=0):
                        self.init()
                    if(self._MATRIX[self._POSY+i+1][self._POSX+j]!=0):
                        self._canMoveDown=False
        if(self._canMoveDown==True):         
            self._RDV.append(self._FRAME.after(self._CHECKTIME,self.check))
        else:
            self._RDV.append(self._FRAME.after(self._GRAVITYTIME,self.validatePiece))

    def checkCompleteLines(self):
        linesToKeep,check,padding,bonus=[],True,0,0
        for i in range(1,self._MATRIXHEIGHT-1,1):
            check=True
            for j in range(1,self._MATRIXWIDTH-1,1):
                if(self._MATRIX[i][j]==0):
                    check=False
            if(check):
                padding+=1
            else:
                linesToKeep.append(self._MATRIX[i])
        if(padding>0):
            for i in range(1,self._MATRIXHEIGHT-1,1):
                if(i<padding+1):
                    self._MATRIX[i]=[8,0,0,0,0,0,0,0,0,0,0,8]
                else:
                    self._MATRIX[i]=linesToKeep[i-padding-1]
            self._NBLINES.set(self._NBLINES.get()+padding)
            if(self._FREE>=100 and self._FREE<=150):
                bonus=40
            elif(self._FREE>150):
                bonus=80
            self._SCORE.set(self._SCORE.get()+(padding*(40+40*self._CURRENTLVL.get()))+bonus)

    def draw(self):
        self._FRAME.delete(ALL)
        for i in range (0,self._MATRIXHEIGHT,1):
            for j in range(0,self._MATRIXWIDTH,1):
                    self._FRAME.create_rectangle((self._BLOCKSIZE*j),(self._BLOCKSIZE*i),((self._BLOCKSIZE*j)+self._BLOCKSIZE),((self._BLOCKSIZE*i)+self._BLOCKSIZE),fill=self._Colors[self._MATRIX[i][j]])
        for i in range (0,4,1):
            for j in range (0,4,1):
                if(self._CURRENTPIECE[i][j]!=0):
                    self._FRAME.create_rectangle((self._BLOCKSIZE*(j+self._POSX)),(self._BLOCKSIZE*(i+self._POSY),((self._BLOCKSIZE*(j+self._POSX))+self._BLOCKSIZE),((self._BLOCKSIZE*(i+self._POSY)))+self._BLOCKSIZE),fill=self._Colors[self._CURRENTPIECE[i][j]],tag=("_CURRENTPIECE"))

    def fillMatrix(self):
        for i in range (0,self._MATRIXHEIGHT+1,1):
            self._MATRIX.append([])
            for j in range(0,self._MATRIXWIDTH,1):
                if(i==0 or j==0 or i==self._MATRIXHEIGHT-1 or j==self._MATRIXWIDTH-1):
                    self._MATRIX[i].append(8)
                else:
                    self._MATRIX[i].append(0)

    def getdown(self):
        if(self._canMoveDown and self._canMove):
            self._GRAVITYTIME,self._canMove=self._MOVETIME,False

    def getLeftRotatedBar(self,a):
        if(a[2][3]==1):
            return [[0,0,1,0],[0,0,1,0],[0,0,1,0],[0,0,1,0]]
        elif(a[3][2]==1):
            return self._PIECES[1]
        elif(a[1][0]==1):
            return [[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0]]
        elif(a[0][1]==1):
            return [[0,0,0,0],[0,0,0,0],[1,1,1,1],[0,0,0,0]]

    def getLeftRotation(self,a):
        res=[]
        for i in range(0,4,1):
            if(i<3):
                res.append([0,a[0][abs(i-3)],a[1][abs(i-3)],a[2][abs(i-3)]])
            else:
                res.append([0,0,0,0])
        return res

    def getRightRotatedBar(self,a):
        if(a[1][0]==1):
            return [[0,0,1,0],[0,0,1,0],[0,0,1,0],[0,0,1,0]]
        elif(a[0][1]==1):
            return self._PIECES[1]
        elif(a[2][3]==1):
            return [[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0]]
        elif(a[3][2]==1):
            return [[0,0,0,0],[0,0,0,0],[1,1,1,1],[0,0,0,0]]

    def getRightRotation(self,a):
        res=[]
        for i in range(0,4,1):
            if(i<3):
                res.append([0,a[2][i+1],a[1][i+1],a[0][i+1]])
            else:
                res.append([0,0,0,0])
        return res

    def gravity(self):
        if(self._canMoveDown):
            self._POSY+=1
            self._FRAME.move("_CURRENTPIECE",0,self._BLOCKSIZE)
            self._RDV.append(self._FRAME.after(self._GRAVITYTIME,self.gravity))

    def init(self):
        self.cancelation()
        self.resetStat()
        self._GRAVITYTIME,self._MATRIX,_canMoveDown,_canMoveRight,_canMoveLeft,self._NEXTPIECE=1000,[],False,False,False,random.randint(1,7)
        self._CURRENTLVL.set(0)
        self.fillMatrix()
        self.addPiece()

    def initStat(self):
        self._SCORE,self._HIGHSCORE,self._CURRENTLVL,self._NBLINES=IntVar(),IntVar(),IntVar(),IntVar()
        self._HIGHSCORE.set(0)
        self._SCORE.set(0)
        for i in range(1,8,1):
            self._STAT.append(IntVar())

    def quick(self):
        tempY,down=self._POSY,True
        while(tempY<self._MATRIXHEIGHT-3 and down):
            for i in range (0,4,1):
                for j in range (0,4,1):
                    if(self._CURRENTPIECE[i][j]!=0):
                        if(self._MATRIX[tempY+i+1][self._POSX+j]!=0):
                            down=False
            if(down):
                tempY+=1
                self._FRAME.move("_CURRENTPIECE",0,self._BLOCKSIZE)
        self._POSY=tempY

    def resetStat(self):
        if(self._SCORE.get()>self._HIGHSCORE.get()):
            self._HIGHSCORE.set(self._SCORE.get())
        self._SCORE.set(0)
        self._CURRENTLVL.set(0)
        self._NBLINES.set(0)
        for i in range(1,8,1):
            self._STAT[i].set(0)

    def rotateLeft(self):
        temp,canLeftRotate=[],True
        if(self._TYPE!=2):
            if(self._TYPE>2):
                temp=self.getLeftRotation(self._CURRENTPIECE)
            elif(self._TYPE==1):
                temp=self.getLeftRotatedBar(self._CURRENTPIECE)
            for i in range (0,4,1):
                for j in range (0,4,1):
                    if(temp[i][j]!=0 and self._MATRIX[self._POSY+i][self._POSX+j]!=0):
                        canLeftRotate=False
            if(canLeftRotate):
                self._CURRENTPIECE=temp
                self.draw()

    def rotateRight(self):
        temp,canRightRotate=[],True
        if(self._TYPE!=2):
            if(self._TYPE>2):
                temp=self.getRightRotation(self._CURRENTPIECE)
            elif(self._TYPE==1):
                temp=self.getRightRotatedBar(self._CURRENTPIECE)
            for i in range (0,4,1):
                for j in range (0,4,1):
                    if(temp[i][j]!=0 and self._MATRIX[self._POSY+i][self._POSX+j]!=0):
                        canRightRotate=False
            if(canRightRotate):
                self._CURRENTPIECE=temp
                self.draw()

    def toTheLeft(self):
        MoveLeft=True
        for i in range (0,4,1):
            for j in range (0,4,1):
                if(self._CURRENTPIECE[i][j]!=0 and self._MATRIX[self._POSY+i][self._POSX+j-1]!=0):
                        MoveLeft=False
        if(MoveLeft and self._canMove):
            self._POSX,self._canMove=(self._POSX-1),False
            self._FRAME.move("_CURRENTPIECE",-self._BLOCKSIZE,0)
            self._RDV.append(self._FRAME.after(self._MOVETIME,self.allowMove))

    def toTheRight(self):
        MoveRight=True
        for i in range (0,4,1):
            for j in range (0,4,1):
                if(self._CURRENTPIECE[i][j]!=0 and self._MATRIX[self._POSY+i][self._POSX+j+1]!=0):
                        MoveRight=False
        if(MoveRight and self._canMove):
            self._POSX,self._canMove=(self._POSX+1),False
            self._FRAME.move("_CURRENTPIECE",+self._BLOCKSIZE,0)
            self._RDV.append(self._FRAME.after(self._MOVETIME,self.allowMove))

    def validatePiece(self):
        self.quick()
        self._canMove=False
        for i in range (0,4,1):
            for j in range (0,4,1):
                if(self._CURRENTPIECE[i][j]!=0):
                    self._MATRIX[self._POSY+i][self._POSX+j]=self._CURRENTPIECE[i][j]
        self.checkCompleteLines()
        self.addPiece()

if __name__ == '__main__':
    Application().mainloop()
