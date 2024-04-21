import numpy as np
import copy
from algorithms.greedy import Greedy

TETROMINO = {'T':0, 'O':1, 'J':2, 'L':3, 'I':4, 'S':5, 'Z':6}

class Q_learning():
	def __init__(self, tetris):
		self.tetris = tetris
		self.actions = {"Left": False, "Right": False, "Soft_Drop": False,"Hard_Drop": False,
			"Rotate_Right": False, "Rotate_Left": False, "Hold": False } # dicionario com as ações do jogo
		self.field = np.zeros(( 10, 40))
		'''
		#				20* altura da coluna, 7 tetrominos,  40 ações
		self.q_values = np.zeros((20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 7, 40))
				=	2293760 petabyte
		'''
		#				media da altura das colunas, 7 tetrominos,  40 ações
		self.q_values = np.zeros((20, 7, 40))
		print(f"Size of q_values = {round(self.q_values.nbytes / 1024 / 1024,2)}")
		#parametros de treinamento
		self.epsilon = 0.1 #the percentage of time when we should take the best action (instead of a random action)
		self.discount_factor = 0.9 #discount factor for future rewards
		self.learning_rate = 0.9 #the rate at which the AI agent should learn
		
		self.g=Greedy(self.tetris)
		
		self.old_garbage=0
		self.height_mean=0
		self.total_lines_cleared=0
		self.current_piece = TETROMINO[self.tetris.tetromino.shape]
		self.action_counter=[0,0]#variavel para guiar o progresso da execução da ação
		self.old_action =-1
		self.current_action =self.get_next_action()
		self.training=True

	def update(self):
		#while self.tetris
		if self.current_action==-1:
			if self.training:
				self.update_q_value()
			#print("new action")
			self.current_action = self.get_next_action()
		if self.execute_action():
			self.old_action = self.current_action
			self.current_action=-1
		

	def get_next_action(self):
		'''list=[]
		field = [[False for i in range(20)] for j in range(10)]
		#field = np.zeros((10, 20))
		for x in range(10):
			for y in range(20):
				if self.tetris.matrix[x][y]==0:
					field[x][y] = True
		for i in range((2*40)*40*100):
			list.append(copy.copy(field))
		print(len(list))
		for i in range(100000):
			self.tetris.tetromino.rotation(-1)
		'''
		list=self.g.update()
		print(list)
		
		
		if np.random.random() < self.epsilon:
			#return np.argmax(self.q_values[self.heights[0], self.heights[1], self.heights[2], self.heights[3], self.heights[4], self.heights[5], self.heights[6], self.heights[7], self.heights[8], self.heights[9], self.current_piece])
			action = np.argmax(self.q_values[self.height_mean, self.current_piece])
		else: #choose a random action
			action = np.random.randint(40)
		self.action_counter[0]=int(action/10)#rotações
		self.action_counter[1]=action%10#coluna
		return action

	def execute_action(self):			
		#print(f"Exe action:{self.current_action}. counter{self.action_counter}	pos{self.tetris.tetromino.pos} "+self.tetris.tetromino.shape)
		if self.action_counter[0]>0:
			self.actions["Rotate_Right"]=True
			self.action_counter[0] -= 1
		else:
			if self.action_counter[1]==5:
				self.actions["Hard_Drop"]=True
				self.actions["Left"]=False
				self.actions["Right"]=False
				return True
			else:
				if self.action_counter[1]<5:
					if self.actions["Left"]:
						self.actions["Left"]=False
					else:
						self.actions["Left"]=True
						self.action_counter[1]+=1
				else:
					if self.actions["Right"]:
						self.actions["Right"]=False
					else:
						self.actions["Right"]=True
						self.action_counter[1]-=1
		
		return False
	
	def update_q_value(self):
		#h =[self.heights[0], self.heights[1], self.heights[2], self.heights[3], self.heights[4], self.heights[5], self.heights[6], self.heights[7], self.heights[8], self.heights[9]]
		old_h_mean=self.height_mean
		old_tetromino = self.current_piece
		reward = self.get_reward(old_h_mean)
		
		#print(f"h: {old_h_mean}")
		#print(f"heights: {self.height_mean}")
		
		#old_q_value=self.q_values[self.heights[0], self.heights[1], self.heights[2], self.heights[3], self.heights[4], self.heights[5], self.heights[6], self.heights[7], self.heights[8], self.heights[9], TETROMINO[self.tetromino.shape],self.current_action]
		old_q_value=self.q_values[old_h_mean, old_tetromino, self.old_action]
		
		#temporal_difference = reward + (discount_factor * np.max(self.q_values[self.heights[0], self.heights[1], self.heights[2], self.heights[3], self.heights[4], self.heights[5], self.heights[6], self.heights[7], self.heights[8], self.heights[9], self.current_piece])) - old_q_value
		temporal_difference = reward +(self.discount_factor * np.max(self.q_values[self.height_mean, self.current_piece])) - old_q_value
		new_q_value = old_q_value + (self.learning_rate * temporal_difference)
		#self.q_values[h[0], h[1], h[2], h[3], h[4], h[5], h[6], h[7], h[8], h[9], TETROMINO[self.tetromino.shape],self.old_action] = new_q_value
		self.q_values[self.height_mean, TETROMINO[self.tetris.tetromino.shape],self.old_action] = new_q_value
		#print(f"old {old_q_value}	new {new_q_value}")
	
	def get_reward(self, old_h_mean):
		over_10=self.update_parameters()
		reward=0
		if self.old_garbage>self.tetris.garbage:
			reward = 100*(self.old_garbage-self.tetris.garbage)
			self.old_garbage=0
		reward += 100*self.tetris.attack+(100*self.tetris.Back_to_Back)
		reward += 100*(self.tetris.total_lines_cleared-self.total_lines_cleared)
		self.total_lines_cleared=self.tetris.total_lines_cleared
		reward += 50*(old_h_mean-self.height_mean)-100*over_10
		
		return reward
		
	
	def update_parameters(self):
		h=[]
		count=0
		over_10 =0
		for x in range(10):
			for y in range(20):
				if self.tetris.matrix[x][y]!=0:
					count = y
			h.append(count)
			if count>10:
				over_10+=1
			count=0
		#self.heights=h
		self.height_mean=int(sum(h)/10)
		return over_10
		
	