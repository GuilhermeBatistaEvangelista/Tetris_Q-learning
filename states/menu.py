import pygame
from states.state import State
from states.solo import Solo
from states.menu_opt import Menu_Opt
from states.vs import Vs
from states.train_q import Train_Q
from states.choose import Choose

class Menu(State):
	def __init__(self, game):
		State.__init__(self, game)
		self.language()
		self.verifylang=False
		self.position = 0
		self.time=0
		#botoes
		self.recs= [pygame.Rect((self.game.canvas_w/2,self.game.canvas_h/2), (self.game.canvas_w/5,self.game.canvas_h/8)) for i in range(4)]
		for i in range(len(self.recs)):
			self.recs[i].center=(self.game.canvas_w/2,self.game.canvas_h*(0.4+i*0.15))
	
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
			if self.recs[0].collidepoint(self.game.mouse_pos):
				actions["Confirm"]=True
				self.position=0
			if self.recs[1].collidepoint(self.game.mouse_pos):
				actions["Confirm"]=True
				self.position=1
			if self.recs[2].collidepoint(self.game.mouse_pos):
				actions["Confirm"]=True
				self.position=2
			if self.recs[3].collidepoint(self.game.mouse_pos):
				actions["Confirm"]=True
				self.position=3
		if actions["Confirm"]:
			print(self.option[self.position])
			if self.position==0:#se 1 Jogador for selecionada
				self.game.playGame=True
				new_state = Solo(self.game)
				new_state.state_in()	#adiciona o estado ao topo da pilha
			if self.position==1:#se VS AI for selecionada
				self.game.playGame=True
				new_state = Vs(self.game)
				new_state.state_in()	#adiciona o estado ao topo da pilha
			if self.position==2:#se configuração for selecionada
				new_state = Menu_Opt(self.game)
				new_state.state_in()	#adiciona o estado do menu de opções ao topo da pilha
				self.verifylang=True
			if self.position==3:#se Training for selecionada Train_Q
				new_state = Choose(self.game)
				new_state.state_in()	#adiciona o estado ao topo da pilha
			self.game.reset_actions()
		if actions["Scape"]:
			self.game.runGame=False
			actions["Scape"]=False

	def draw(self, canvas):
		w,h = self.game.canvas_w, self.game.canvas_h
		canvas.fill(pygame.Color("aquamarine3"))
		self.game.text(canvas,"Tetris", int(h/5), pygame.Color("black"), w/2, h/5)
		for i in self.option:
			if self.position==i:
				pygame.draw.rect(canvas, pygame.Color("aliceblue"), self.recs[i],  0, int(h/50))
			pygame.draw.rect(canvas, pygame.Color("white"), self.recs[i],  int(h/150), int(h/50))
			if self.option[i]=="Configurações":
				self.game.text(canvas,self.option[i], int(h/16), pygame.Color("black"), w/2, h*(0.4+i*0.15))
			else:
				self.game.text(canvas,self.option[i], int(h/11), pygame.Color("black"), w/2, h*(0.4+i*0.15))
		
		#self.game.text(canvas,str(self.position)+"y", int(self.game.canvas_h/10), [200,100,255], self.game.canvas_w/4, self.game.canvas_h/2) #print posição


	def language(self):
		if self.game.save["language"] == "EN":
			self.option = {0:"1 Player", 1:"Vs IA", 2:"Settings", 3:"Training"}
		elif self.game.save["language"] == "PT":
			self.option = {0:"1 Jogador", 1:"Vs AI", 2:"Configurações", 3:"Treinar"}