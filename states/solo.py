import pygame
from states.state import State
from tetris import Tetris
from states.menu_game import Menu_Game
from states.game_over import Game_Over

####
import numpy as np
from algorithms.q_4 import Q_learning
####

class Solo(State):
	def __init__(self, game):
		State.__init__(self, game)
		self.tetris = Tetris(self.game,self.game.canvas_w/2)
		
		###
		self.Q = Q_learning(self.tetris)
		self.Q.training=False
		self.q_values = np.load("algorithms/q_4_1000.npz")['arr_0']
		self.Q.q_values = self.q_values
	
	def update(self, deltatime, actions):
		if self.game.playGame==False:
			self.state_out()
			return
		if actions["Scape"]:# se scape fro pressionado vai para o menu de jogo
			new_state = Menu_Game(self.game)
			new_state.state_in()	#adiciona o estado ao topo da pilha
			self.game.reset_actions()
		
		self.Q.update()
		print(self.tetris.tetromino.shape,end="	")
		print("pos:	",end="")
		print([self.tetris.tetromino.pos, self.tetris.tetromino.facing],end="		")
		print("target:	",end="")
		print(self.Q.position)
		#print(self.Q.actions)
		if not self.tetris.update(deltatime, self.Q.actions):
			#new_state = Game_Over(self.game, False)
			#new_state.state_in()	#adiciona o estado ao topo da pilha
			self.tetris = Tetris(self.game,self.game.canvas_w/2)
			self.Q = Q_learning(self.tetris)
			self.Q.training=False
			self.Q.q_values = self.q_values

	def draw(self, canvas):
		canvas.fill(pygame.Color("antiquewhite3"))
		self.tetris.draw(canvas)