import pygame
from states.state import State
from states.vs import Vs
from states.train_q import Train_Q

class Choose(State):
	def __init__(self, game):
		State.__init__(self, game)
		self.language()
		self.verifylang=False
		self.position = 0
		self.time = 0
		
		#botoes
		self.recs= [pygame.Rect((self.game.canvas_w/2,self.game.canvas_h/2), (self.game.canvas_w/3,self.game.canvas_h/8)) for i in range(6)]
		for i in range(len(self.recs)):
			self.recs[i].center=(self.game.canvas_w/2,self.game.canvas_h*(0.25+i*0.13))
	
	def update(self, deltatime, actions):
		if self.verifylang:#se retornar do menu de configur verifica a linguagem atual
			self.language()
			self.verifylang=False
		move = actions["Down"] - actions["Up"] #recebe o valor do movimento vertical
		if self.time==0:
			self.position = (self.position + move) % len(self.option) # realiza o movimento dentre as opções
		if move==0 or self.time>0.333:
			self.time=0
		else:
			self.time += deltatime
		if self.game.mouse:#se clicar
			for i in range(len(self.recs)):
				if self.recs[i].collidepoint(self.game.mouse_pos):
					actions["Confirm"]=True
					self.position=i
		if actions["Confirm"]:
			print(self.option[self.position])
			if self.position==0:#
				self.game.playGame=True
				new_state = Train_Q(self.game,"q_1.py")
				new_state.state_in()
			if self.position==1:#
				self.game.playGame=True
				new_state = Train_Q(self.game,"q_2.py")
				new_state.state_in()
			if self.position==2:#
				self.game.playGame=True
				new_state = Train_Q(self.game,"q_3.py")
				new_state.state_in()
			if self.position==3:#
				self.game.playGame=True
				new_state = Train_Q(self.game,"q_4.py")
				new_state.state_in()
			self.game.reset_actions()
			if self.position==4:#
				self.game.playGame=True
				new_state = Train_Q(self.game,"q_5.py")
				new_state.state_in()
			self.game.reset_actions()
			if self.position==5:#
				self.game.playGame=True
				new_state = Train_Q(self.game,"q_6.py")
				new_state.state_in()
			self.game.reset_actions()
		if actions["Scape"]:# retorna
			self.state_out()
			self.game.reset_actions()
	
	def draw(self, canvas):
		w,h = self.game.canvas_w, self.game.canvas_h
		canvas.fill(pygame.Color("aquamarine3"))
		self.game.text(canvas,"Algorithm", int(h/6), pygame.Color("black"), w/2, h/12)
		for i in self.option:
			if self.position==i:
				pygame.draw.rect(canvas, pygame.Color("aliceblue"), self.recs[i],  0, int(h/50))
			pygame.draw.rect(canvas, pygame.Color("white"), self.recs[i],  int(h/150), int(h/50))
			self.game.text(canvas,self.option[i], int(h/(len(self.option[i])*0.7)), pygame.Color("black"), w/2, h*(0.25+i*0.13))
		
		#self.game.text(canvas,str(self.position)+"y", int(self.game.canvas_h/10), [200,100,255], self.game.canvas_w/4, self.game.canvas_h/2) #print posição


	def language(self):
		if self.game.save["language"] == "EN":
			self.title="Algorithms"
			self.option = {0:"1 - Q(Height mean, piece, 40 actions)",
							1:"2 - Q(Tallest column(height, position), Shortest column(height, position), piece, 40 actions)",
							2:"3 - Q(10 x Column(Heigth/5), piece, 40 actions)",
							3:"4 - Q(Height mean, piece, 3 actions)",
							4:"5 - Q(Tallest column(height, position), Shortest column(height, position), piece, 3 actions)",
							5:"6 - Q(10 x Column(Heigth/5), piece, 3 actions)"}
		elif self.game.save["language"] == "PT":
			self.title="Algoritmos"
			self.option = {0:"1 - Q()",
							1:"2 - Q()",
							2:"3 - Q()",
							3:"4 - Q()",
							4:"5 - Q()",
							5:"6 - Q()"}
			