import pygame
from states.state import State
from tetris import Tetris
from states.menu_game import Menu_Game
from states.game_over import Game_Over
import numpy as np
from algorithms.q_4 import Q_learning
#from deep_q import Deep_q

class Vs(State):
	def __init__(self, game):
		State.__init__(self, game)
		self.tetris1 = Tetris(self.game,self.game.canvas_w*0.25)
		self.tetris2 = Tetris(self.game,self.game.canvas_w*0.75)
		self.Q = Q_learning(self.tetris2)
		self.Q.training=False
		self.q_values = np.load("algorithms/q_4_1000.npz")['arr_0']
		self.Q.q_values = self.q_values
		self.score=[0,0]
		self.lines_score=[0,0]
	
	def update(self, deltatime, actions):
		if self.game.playGame==False:
			self.state_out()
			return
		if actions["Scape"]:# se scape fro pressionado vai para o menu de jogo
			new_state = Menu_Game(self.game)
			new_state.state_in()	#adiciona o estado ao topo da pilha
			self.game.reset_actions()
		t1=self.tetris1.update(deltatime, actions)
		self.tetris2.garbage+=self.tetris1.attack	#envia o ataque do jogador para a Ai
		
		self.Q.update()
		
		t2=self.tetris2.update(deltatime, self.Q.actions)
		self.tetris1.garbage+=self.tetris2.attack	#envia o ataque da AI para o jogador
		
		
		if not t1:#Se o jogador perder
			new_state = Game_Over(self.game, False)
			new_state.state_in()	#adiciona o estado ao topo da pilha
			self.lines_score[0] += self.tetris1.total_lines_cleared
			self.lines_score[1] += self.tetris2.total_lines_cleared
			self.tetris1 = Tetris(self.game,self.game.canvas_w*0.25)
			self.tetris2 = Tetris(self.game,self.game.canvas_w*0.75)
			self.Q = Q_learning(self.tetris2)
			self.Q.training=False
			self.Q.q_values = self.q_values
			self.score[1]+=1
		elif not t2:#Se o algoritimo perder
			new_state = Game_Over(self.game, True)
			new_state.state_in()	#adiciona o estado ao topo da pilha
			self.lines_score[0] += self.tetris1.total_lines_cleared
			self.lines_score[1] += self.tetris2.total_lines_cleared
			self.tetris1 = Tetris(self.game,self.game.canvas_w*0.25)
			self.tetris2 = Tetris(self.game,self.game.canvas_w*0.75)
			self.Q = Q_learning(self.tetris2)
			self.Q.training=False
			self.Q.q_values = self.q_values
			self.score[0]+=1

	def draw(self, canvas):
		canvas.fill(pygame.Color("gray"))
		self.tetris1.draw(canvas)
		self.tetris2.draw(canvas)
		
		#desenhar score
		self.game.text(canvas,f"Games:{self.score[0]+self.score[1]}", 24, pygame.Color("black"), self.game.canvas_w*0.50, 20)
		self.game.text(canvas,f"Lines:{self.lines_score[0]}", 24, pygame.Color("black"), self.game.canvas_w*0.20, 20)
		self.game.text(canvas,f"Wins:{self.score[0]}", 24, pygame.Color("black"), self.game.canvas_w*0.30, 20)
		self.game.text(canvas,f"Lines:{self.lines_score[1]}", 24, pygame.Color("black"), self.game.canvas_w*0.70, 20)
		self.game.text(canvas,f"Wins:{self.score[1]}", 24, pygame.Color("black"), self.game.canvas_w*0.80, 20)
		
		