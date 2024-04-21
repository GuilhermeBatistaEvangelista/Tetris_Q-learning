import pygame
from states.state import State
from tetris import Tetris
from states.menu_game import Menu_Game
from states.game_over import Game_Over

class Solo(State):
	def __init__(self, game):
		State.__init__(self, game)
		self.tetris = Tetris(self.game,self.game.canvas_w/2)
	
	def update(self, deltatime, actions):
		if self.game.playGame==False:
			self.state_out()
			return
		if actions["Scape"]:# se scape fro pressionado vai para o menu de jogo
			new_state = Menu_Game(self.game)
			new_state.state_in()	#adiciona o estado ao topo da pilha
			self.game.reset_actions()
		if not self.tetris.update(deltatime, actions):
			new_state = Game_Over(self.game, False)
			new_state.state_in()	#adiciona o estado ao topo da pilha
			self.tetris = Tetris(self.game,self.game.canvas_w/2)

	def draw(self, canvas):
		canvas.fill(pygame.Color("antiquewhite3"))
		self.tetris.draw(canvas)