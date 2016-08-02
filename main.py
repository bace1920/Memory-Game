#!/usr/local/bin/python
import pygame, sys, time,random,os
from pygame.locals import *

#讲tilelist分为两半，随机交换
def shuffle(tileList):
	for i in range(0,8):
		int_temp=random.randint(8,15)
		tile_temp=tileList[i]
		tileList[i]=tileList[int_temp]
		tileList[int_temp]=tile_temp
		
#tile类
class Tile:
	def __init__(self,image,imageIndex):
		#Initializes the instance attributes with the given parameters
		self.image=image#图片的surface object
		self.imageIndex=imageIndex#图片在inagelist的序号
		self.x=0#图片在输出屏幕时使用的横坐标
		self.y=0#图片在输出屏幕时使用的纵坐标
		self.image0=pygame.image.load("image/image0.jpg").convert()#cover
		self.showOrNot=False#记录该tile的状态，false表是hidden
	def setPosition(self,x,y):
		self.x=x
		self.y=y
	def show(self,window):#显示图片
		self.showOrNot=True
		window.blit(self.image,(self.x,self.y))
		#pygame.display.update()
	def hide(self,window):
		self.showOrNot=False
		window.blit(self.image0,(self.x,self.y))
		#pygame.display.update()

#Game类
class Memory():
	def __init__(self):
		self.score=0#得分
		self.showCount=0#记录已翻开的牌的数量，为16时游戏结束
		self.tempShowCount=0#记录临时翻开的数量，最大为2
		self.tempShowRecord=[-1,-1]#记录临时翻的两张牌的序数
		self.screen =pygame.display.set_mode((524,420),0,32)
		self.imageList = [0,0,0,0,0,0,0,0,0]#图片列表（第一位是问号图）
		self.tileList=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]#tile类列表
		
		#读取图片
		for i in range(0,9):
			source="image\\image"+str(i)+".jpg"
			self.imageList[i]=pygame.image.load(source).convert()		

		#从图片list调用surface生成16个tile并添加到tilelist中，每个图片用两次
		int_temp=1
		for q in range(0,16,2):
			#print(int_temp)
			self.tileList[q]=Tile(self.imageList[int_temp],int_temp)
			self.tileList[q+1]=Tile(self.imageList[int_temp],int_temp)
			int_temp+=1
			
		#tilelist乱序排列
		shuffle(self.tileList)
		
		#给tile的显示坐标赋值
		int_temp=0
		for i in range(0,4):
			for q in range(0,4):
				self.tileList[int_temp].setPosition(i*104+4,q*104+4)
				int_temp+=1

		#隐藏所有图片
		for i in range(0,16):
			self.tileList[i].hide(self.screen)

	#check if two images is qequal
	def equal(self,image1,image2): 
		if image1.imageIndex==image2.imageIndex:
			return True
		else:
			return False

	#接受鼠标点击事件显示图片
	def showControl(self,x,y):
		for i in range(0,4):
			for q in range(0,4):
				#确认图片在那个tile范围内
				if x>i*104+4 and y>q*104+4 and x<(i+1)*104+4 and y<(q+1)*104+4:
					if self.tempShowCount==0 and self.tileList[i*4+q].showOrNot==False:
						self.tempShowRecord[0]=i*4+q
						self.tempShowCount=1
						self.tileList[i*4+q].show(self.screen)
					elif self.tempShowCount==1 and self.tileList[i*4+q].showOrNot==False:
						self.tempShowRecord[1]=i*4+q
						self.tempShowCount=2
						self.tileList[i*4+q].show(self.screen)

	#显示分数
	def drawScore(self):
		time=pygame.time.get_ticks()//1000
		scoreString=str(time)
		fontSize=40
		fgColor=pygame.Color('white')
		bgColor=pygame.Color('black')
		font=pygame.font.SysFont(None,fontSize,True)
		textSurface=font.render(scoreString,True,fgColor,bgColor)
		self.screen.blit(textSurface,(484,5))
  
	#游戏主进程
	def start(self):
		while 1:
			self.drawScore()
			pygame.display.update()
			#如果历史翻开的牌达到两张，确认他们是否相同
			if self.showCount==16:
				os.system("pause")
				return
			if self.tempShowCount==2:
				self.tempShowCount=0		
				#不相同，隐藏他它们
				if self.equal(self.tileList[self.tempShowRecord[0]],self.tileList[self.tempShowRecord[1]])==False:
					time.sleep(1)
					self.tileList[self.tempShowRecord[0]].hide(self.screen)
					self.tileList[self.tempShowRecord[1]].hide(self.screen)
				#相同，继续游戏
				else:
					self.showCount+=2
			#if self.showCount==16:
			for event in pygame.event.get():
				if event.type == MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					#print(pos)
					self.showControl(pos[0],pos[1])
				if event.type == QUIT:
					exit()

pygame.init()
test=Memory()
test.start()