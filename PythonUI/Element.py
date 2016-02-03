import sys
import string
import itertools
import tkinter
from tkinter import *
from tkinter import font
from tkinter import simpledialog
from tkinter import messagebox

class Element():   
    def __init__(self):
        self.createElementList()        #根据avikt.txt创建元素符号、值得列表
        self.constructUI()              #创建UI
        
    def constructUI(self):
        self.root = Tk()                #创建顶层界面
        self.root.geometry('360x220')   #设定UI界面大小
        self.root.title("Chemistry Crossword Specifications")#设置标题栏
        self.root.resizable(0,0)        #UI界面大小不可调

        # 创建一个Label用来提示用户输入
        # 指定字体名称、大小、样式
        tipFont = font.Font(family = 'Fixdsys',size = 10,weight = font.NORMAL)
        tipLabel = Label(self.root,text = 'Please input 4 letters in the square',font = tipFont)
        tipLabel.pack(pady=5)

        #创建4个输入文本框的父控件
        inputEntryFrame = Frame(self.root)
        inputEntryFrame.pack()

        #声明输入控件存放列表，已经输入文本存放列表
        self.inputEntryList = []
        self.inputStrList = []

        #输入文本框字体大小、样式
        self.inputFont = font.Font(family = 'Fixdsys',size = 20,weight = font.BOLD)
        for i in (0,1,2,3):
             self.inputStrList.append(StringVar())

        #创建输入文本框，以及布局为十字交叉网格
        for i in (0,1,2,3):
             inputEnter = self.creatEntry(inputEntryFrame,self.inputStrList[i]);
             inputEnter.grid(row = (int)(i/2) ,column = (int)(i%2),padx=10,pady=10)
             self.inputEntryList.append(inputEnter)
        self.inputEntrySetFocus()
        
        #创建Play,Quit按钮的父控件
        buttonFrame = Frame(self.root)
        buttonFrame.pack()

        #创建按钮，及绑定按钮左键按下事件的回调函数             
        self.playButton = Button(buttonFrame,text = 'Play',width=8)
        self.playButton.bind("<Button-1>",self.palyAction)
        self.playButton.grid(row = 0,column =0,padx=10,pady=10)

        quitButton = Button(buttonFrame,text = 'Quit',width=8)
        quitButton.bind("<Button-1>",self.quitAction)
        quitButton.grid(row = 0,column =1,padx=10,pady=10)

    def inputEntrySetFocus(self):
        self.inputEntryList[0].focus_set()
        
    def createElementList(self):
        self.elementsSign = []
        self.elementsValue = []
        fd = open("avikt.txt")          #打开存放信息文件
        for line in fd.readlines():     #读取文件每行中的信息，即每个元素的信息
            line = line.strip()
            elementSign = line.split(' ')
            self.elementsSign.append(elementSign[0])    #存放元素表符号
            self.elementsValue.append(elementSign[len(elementSign)-1])#存放元素表符号对应的原子量
        fd.close()
        
#################调式打印信息，查看数据是否正确#################
##        print(self.elementsSign)
##        print(self.elementsValue)
        
    def newElement(self):
        self.inputLettersCombination()
        self.elementLookup()
##        print(self.existElementSignList)
##        print(self.existElementValueList)
    def inputLettersCombination(self):
        inputList = []
        for inputStr in self.inputStrList:  #获取输入文本内容
            inputList.append(inputStr.get())
        #将inputList 列表中的元素排列组合
        self.combination = []
        combinationTemp = []
        combinationTemp = list(itertools.permutations(inputList,2)) #排列算法

        for comb in combinationTemp:    #排列后数据格式是元组性的，重新组合成期望类型                
            self.combination.append(comb[0] + comb[1])

        #去除排列组合中重复的元素   
        self.combination = set(self.combination)

##        print(self.combination)

    def elementLookup(self):
        self.existElementSignList = []
        self.existElementValueList = []
        self.cnt = 0
        #遍历排列组合中的元素是否存在
        for index,sign in enumerate(self.elementsSign):
            for comb in self.combination:
                if(comb.lower() == sign.lower() and len(sign) == 2):   #不区分大小写,并且只有匹配的元素是两个字符才加入得到显示队列中
                    self.cnt+=1
##                    print(comb ,"is a element", "and value is",self.elementsValue[index])
##                    self.existElementSignList.append(comb)  #将匹配的元素存放到，成功匹配列表中，后续显示使用
                    self.existElementSignList.append(sign)  #将文本中保存的标准元素作为输出 
                    self.existElementValueList.append(self.elementsValue[index])#将文本中保存的标准原子量作为输出

    def entryLimit(self,inputStr):
        if(len(inputStr.get()) > 1):
            s = inputStr.get()
            inputStr.set(s[0])

            
    def creatEntry(self,root,inputStr):
##        entry = Entry(root,textvariable = inputStr,width = 4,font = self.inputFont,validate='key',validatecommand = lambda inputStr=inputStr:len(inputStr.get()) < 1)
        
        entry = Entry(root,textvariable = inputStr,width = 4,font = self.inputFont)
        inputStr.trace("w", lambda nm, idx, mode,inputStr = inputStr:self.entryLimit(inputStr))
        
        return entry;

    def inputStrInit(self):
        for inputStr in self.inputEntryList: 
            inputStr.delete(0, END)
            
    def palyAction(self,event): #按下Play调用的回调函数
        self.newElement()
        self.showResult()
        self.inputStrInit()
        self.continueOrNot()
        
    def quitAction(self,event): #按下Quit调用的回调函数
        self.root.destroy()
        
    def continueOrNot(self):    #根据模态对话框的返回值，判断是否继续
        if(self.respond == "no"):
            self.root.destroy()
        else:
            self.inputEntrySetFocus()
            self.root.mainloop()#没有这句话，Play按钮一直弹不起来，不知道原因?
    def showResult(self):
        if(self.cnt <= 0):
            showMsg = "Sorry! You can not construct a new element with those 4 letters"    
        elif(self.cnt == 1):
            showMsg = "Congratulations! You constructed a new element \n"
            for index,sign in enumerate(self.existElementSignList):
                  showMsg = showMsg + "(%s , %s)  " % (sign, self.existElementValueList[index])
        else:
            showMsg = "Congratulations! You constructed  new elements \n"
            for index,sign in enumerate(self.existElementSignList):
                  showMsg = showMsg + "(%s , %s)  " % (sign, self.existElementValueList[index])
                  
        showMsg = showMsg + "\n\nWould you like to Continue or Not?"    
        self.respond = messagebox.askquestion(title="Result", message=showMsg, parent = self.root)
        
    def mainloop(self):
         self.root.mainloop();
    
if __name__ == '__main__':  #程序开始        
    element=Element();      #创建元素对象，会调用构造函数__init__
    element.mainloop()      #事件循环  
