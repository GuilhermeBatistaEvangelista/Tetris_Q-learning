import pygame
import numpy as np
import matplotlib.pyplot
from states.state import State
from tetris import Tetris
from states.menu_game import Menu_Game
from states.game_over import Game_Over
#from algorithms.q import Q_learning
import imp
#from deep_q import Deep_q

class Train_Q(State):
	def __init__(self, game, path):
		#import
		self.name=path[:-3]
		self.path="algorithms/"+path
		module = imp.load_source("Q_learning", self.path)
		self.Algorithm=module.Q_learning
		#
		State.__init__(self, game)
		self.tetris1 = Tetris(self.game,self.game.canvas_w*0.25)
		self.tetris2 = Tetris(self.game,self.game.canvas_w*0.75)
		self.Q1 = self.Algorithm(self.tetris1)
		self.Q2 = self.Algorithm(self.tetris2)
		self.score=[0,0]
		self.lines_score=[0,0]
		self.epsilon=0.1
		self.epsilon_increase_rate=0.0009
		self.total_time=0
		self.game_time=0
		#metricas de analise de resultados
		self.result_score=[]
		self.result_lines=[]
		self.attack1=0
		self.attack2=0
		self.result_attack=[]
		self.result_time=[]
	
	def update(self, deltatime, actions):
		if self.game.playGame==False:
			self.state_out()
			return
		if actions["Scape"]:# se scape fro pressionado vai para o menu de jogo
			new_state = Menu_Game(self.game)
			new_state.state_in()	#adiciona o estado ao topo da pilha
			self.game.reset_actions()
		
		
		self.Q1.update()
		t1=self.tetris1.update(deltatime, self.Q1.actions)
		self.tetris2.garbage+=self.tetris1.attack	#envia o ataque do jogador para a Ai
		self.attack1+=self.tetris1.attack
		
		self.Q2.update()
		t2=self.tetris2.update(deltatime, self.Q2.actions)
		self.tetris1.garbage+=self.tetris2.attack	#envia o ataque da AI para o jogador
		self.attack2+=self.tetris2.attack
		
		self.game_time+=deltatime
		if not t1:#Se o algoritimo1 perder
			self.result_score.append(self.tetris2.score)
			self.result_lines.append(self.tetris2.total_lines_cleared)
			self.result_attack.append(self.attack2)
			self.restart(self.Q2.q_values)
			self.score[1]+=1
			
		elif not t2:#Se o algoritimo2 perder
			self.result_score.append(self.tetris1.score)
			self.result_lines.append(self.tetris1.total_lines_cleared)
			self.result_attack.append(self.attack1)
			self.restart(self.Q1.q_values)
			self.score[0]+=1

	def draw(self, canvas):
		canvas.fill(pygame.Color("gray"))
		self.tetris1.draw(canvas)
		self.tetris2.draw(canvas)
		
		#desenhar score
		self.game.text(canvas,f"Games:{self.score[0]+self.score[1]}", 24, pygame.Color("black"), self.game.canvas_w*0.45, 20)
		self.game.text(canvas,f"\u03B5:{round(self.epsilon,3)}", 24, pygame.Color("black"), self.game.canvas_w*0.55, 20)
		self.game.text(canvas,f"Total time: {round(self.total_time)}s", 24, pygame.Color("black"), self.game.canvas_w*0.40, self.game.canvas_h-20)
		self.game.text(canvas,f"Game time: {round(self.game_time)}s", 24, pygame.Color("black"), self.game.canvas_w*0.60, self.game.canvas_h-20)
		self.game.text(canvas,f"Lines:{self.lines_score[0]}", 24, pygame.Color("black"), self.game.canvas_w*0.20, 20)
		self.game.text(canvas,f"Wins:{self.score[0]}", 24, pygame.Color("black"), self.game.canvas_w*0.30, 20)
		self.game.text(canvas,f"Lines:{self.lines_score[1]}", 24, pygame.Color("black"), self.game.canvas_w*0.70, 20)
		self.game.text(canvas,f"Wins:{self.score[1]}", 24, pygame.Color("black"), self.game.canvas_w*0.80, 20)
		
	def restart(self,q_values):
		#save scores
		self.result_time.append(self.game_time)
		self.total_time+=self.game_time
		self.game_time=0
		self.attack1=0
		self.attack2=0
		self.lines_score[0] += self.tetris1.total_lines_cleared
		self.lines_score[1] += self.tetris2.total_lines_cleared
		
		if ((self.score[0]+self.score[1])==100) or ((self.score[0]+self.score[1])==500) or ((self.score[0]+self.score[1])==1000):
			#list=[0.1*1.0023]
			#for i in range(1000):
				#list.append(list[i]*1.0023)
			#	matplotlib.pyplot.title(self.name+" "+str(self.score[0]+self.score[1]))
			#grafico de pontuação
			data=np.array(self.result_score)
			matplotlib.pyplot.plot(data)
			matplotlib.pyplot.xlabel("Jogos")
			matplotlib.pyplot.ylabel("Pontuação")
			#matplotlib.pyplot.show()
			matplotlib.pyplot.savefig("results/"+self.name+"_"+str(self.score[0]+self.score[1])+"_score.png", format="png")
			matplotlib.pyplot.clf()
			#grafico de linhas completas
			data=np.array(self.result_lines)
			matplotlib.pyplot.plot(data)
			matplotlib.pyplot.xlabel("Jogos")
			matplotlib.pyplot.ylabel("linhas")
			#matplotlib.pyplot.show()
			matplotlib.pyplot.savefig("results/"+self.name+"_"+str(self.score[0]+self.score[1])+"_lines.png", format="png")
			matplotlib.pyplot.clf()
			#grafico de linhas de ataque enviada
			data=np.array(self.result_attack)
			matplotlib.pyplot.plot(data)
			matplotlib.pyplot.xlabel("Jogos")
			matplotlib.pyplot.ylabel("linhas de ataque")
			#matplotlib.pyplot.show()
			matplotlib.pyplot.savefig("results/"+self.name+"_"+str(self.score[0]+self.score[1])+"_attack.png", format="png")
			matplotlib.pyplot.clf()
			#grafico de tempo de jogo
			data=np.array(self.result_time)
			matplotlib.pyplot.plot(data)
			matplotlib.pyplot.xlabel("Jogos")
			matplotlib.pyplot.ylabel("Tempo(s)")
			#matplotlib.pyplot.show()
			matplotlib.pyplot.savefig("results/"+self.name+"_"+str(self.score[0]+self.score[1])+"_time.png", format="png")
			matplotlib.pyplot.clf()
			np.savez("algorithms/"+self.name+"_"+str(self.score[0]+self.score[1]), q_values)
			
		if ((self.score[0]+self.score[1])==1000):
			self.game.playGame=False
		#restart
		self.tetris1 = Tetris(self.game,self.game.canvas_w*0.25)
		self.tetris2 = Tetris(self.game,self.game.canvas_w*0.75)
		self.Q1 = self.Algorithm(self.tetris1)
		self.Q2 = self.Algorithm(self.tetris2)
		self.Q1.q_values,self.Q2.q_values = q_values,q_values
		
		#increase epsilon
		self.epsilon +=self.epsilon_increase_rate
		self.Q1.epsilon, self.Q2.epsilon = self.epsilon, self.epsilon
		