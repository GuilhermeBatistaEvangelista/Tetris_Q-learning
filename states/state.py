
class State():###########			Classe abstrata para outras classes	de estados do jogo		###########
	def __init__(self, game):
		self.game = game
		self.pstate = None # Ponteiro que registra o estado anterior

	def update(self, deltfatime, actions):#controls é o dicionario com os comandos
		pass

	def draw(self, canvas):
		pass

	def state_in(self):
		if len(self.game.state_stack)>1:
			self.pstate = self.game.state_stack[-1]
		self.game.state_stack.append(self)

	def state_out(self):
		self.game.state_stack.pop()