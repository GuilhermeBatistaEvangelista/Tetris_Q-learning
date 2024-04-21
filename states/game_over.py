import pygame
from states.state import State

class Game_Over(State):
	def __init__(self, game, win):
		State.__init__(self, game)
		self.win=win
		self.language()
		self.rec_menu = pygame.Rect((self.game.canvas_w/2,self.game.canvas_h/2), (self.game.canvas_w/4,self.game.canvas_h/3))
		self.rec_menu.center=(self.game.canvas_w/2,self.game.canvas_h/2.2)
		self.rec_opts= [pygame.Rect((self.game.canvas_w/2,self.game.canvas_h/2), (self.game.canvas_w/5,self.game.canvas_h/10)) for i in range(2)]
		for i in range(len(self.rec_opts)):
			self.rec_opts[i].center=(self.game.canvas_w/2,self.game.canvas_h*(0.45+0.1*i))
		self.position = 0

	def update(self, deltatime, actions):
		if actions["Scape"]:# retorna
			self.game.playGame=False
			self.state_out()
		else:
			if self.game.mouse:#se clicar
				if self.rec_opts[0].collidepoint(self.game.mouse_pos):
					actions["Confirm"]=True
					self.position=0
				if self.rec_opts[1].collidepoint(self.game.mouse_pos):
					actions["Confirm"]=True
					self.position=1
			if actions["Confirm"]:
				if self.position==0:#Reiniciar
					self.state_out()
				elif self.position==1:#Sair
					self.game.playGame=False
					self.state_out()
		move = actions["Down"] - actions["Up"] #recebe o valor do movimento vertical
		self.position = (self.position + move) % len(self.option) # realiza o movimento dentre as opções
		self.game.reset_actions()

	def draw(self, canvas):
		pygame.draw.rect(canvas, pygame.Color("azure4"), self.rec_menu,  0, int(self.game.canvas_h/50))
		pygame.draw.rect(canvas, pygame.Color("azure1"), self.rec_menu,  3, int(self.game.canvas_h/50))
		self.game.text(canvas,self.result, 52, pygame.Color("Red"), self.game.canvas_w/2, self.game.canvas_h*(0.35))
		for i in self.option:
			if self.position==i:
				pygame.draw.rect(canvas, pygame.Color("aliceblue"), self.rec_opts[i],  0, int(self.game.canvas_h/50))
			pygame.draw.rect(canvas, pygame.Color("white"), self.rec_opts[i],  int(self.game.canvas_h/150), int(self.game.canvas_h/50))
			self.game.text(canvas,self.option[i], 48, pygame.Color("black"), self.game.canvas_w/2, self.game.canvas_h*(0.45+0.1*i))

	def language(self):
		if self.game.save["language"] == "EN":
			self.option = {0:"Restart", 1:"Quit"}
			if self.win:
				self.result = "WIN"
			else:
				self.result = "Defeat"
		elif self.game.save["language"] == "PT":
			self.option = {0:"Reiniciar", 1:"Sair"}
			if self.win:
				self.result = "Vitória"
			else:
				self.result = "Derrota"