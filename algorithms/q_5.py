import numpy as np
from algorithms.greedy import Greedy

TETROMINO = {'T':0, 'O':1, 'J':2, 'L':3, 'I':4, 'S':5, 'Z':6}

class Q_learning():
	def __init__(self, tetris):
		self.tetris = tetris
		self.actions = {"Left": False, "Right": False, "Soft_Drop": False,"Hard_Drop": False,
			"Rotate_Right": False, "Rotate_Left": False, "Hold": False } # dicionario com as ações do jogo
		self.field = np.zeros(( 10, 40))
		#				Q(Tallest column(height, position), Shortest column(height, position), piece, 3 actions)
		self.q_values = np.zeros((20, 10, 20, 10, 7, 3))
		#parametros de treinamento
		self.epsilon = 0.1 #the percentage of time when we should take the best action (instead of a random action)
		self.discount_factor = 0.9 #discount factor for future rewards
		self.learning_rate = 0.9 #the rate at which the AI agent should learn
		
		self.g=Greedy(self.tetris)#greedy search
		
		#Q-table variables
		self.tallest_h=0
		self.tallest_p=0
		self.shortest_h=0
		self.shortest_p=0
		self.current_piece = TETROMINO[self.tetris.tetromino.shape]
		
		self.old_garbage=0
		self.total_lines_cleared=0
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
		if np.random.random() < self.epsilon:
			#return np.argmax(self.q_values[self.heights[0], self.heights[1], self.heights[2], self.heights[3], self.heights[4], self.heights[5], self.heights[6], self.heights[7], self.heights[8], self.heights[9], self.current_piece])
			action = np.argmax(self.q_values[self.tallest_h, self.tallest_p, self.shortest_h, self.shortest_p, self.current_piece])
		else: #choose a random action
			action = np.random.randint(3)
		
		#print("got_action")
		self.get_pos(action)
		return action

	def get_pos(self, action):
		lista=self.g.update()
		#print(lista)
		nplist=np.array(lista, dtype=list)
		#print(nplist)
		if action==0:#Minimizar  buracos
			#print("holes")#holes
			#print(nplist[:,5])#holes list
			#print(nplist[:,5].argmin())#Minimizar  buracos
			self.position=lista[nplist[:,5].argmin()][0]
		elif action==1:#Minimizar altura
			#print("heigths")#altura
			#print(nplist[:,6])#altura list
			#print(nplist[:,6].argmin())#Minimizar  altura
			self.position=lista[nplist[:,6].argmin()][0]
		else:#Maximizar linhas
			#print("full lines")#altura
			#print(nplist[:,1])#altura list
			#print(nplist[:,1].argmax())#Maximizar linhas completadas
			#print("awarded lines")#altura
			#print(nplist[:,2])#altura list
			#print(nplist[:,2].argmax())#Maximizar linhas recompensadas
			self.position=lista[nplist[:,2].argmax()][0]
		#print("got_pos:")
		#print(self.position)
		self.tetris.wait_time=0.000000001

	def execute_action(self):
		if self.tetris.wait_time==0:#se a peça for posicionada
			self.actions["Left"]=False
			self.actions["Right"]=False
			return True
		#print(str(self.tetris.tetromino.pos)+"<"+str(self.position)+"?")
		if self.tetris.tetromino.facing!=self.position[2]:
			self.actions["Rotate_Right"]=True
			#print("rotato")
		elif self.tetris.tetromino.pos[1]<self.position[1]:
			#print("retry")
			#print(str(self.tetris.tetromino.pos)+"<"+str(self.position))
			self.get_pos(self.current_action)
		elif self.tetris.tetromino.pos[0]==self.position[0] and self.tetris.tetromino.facing==self.position[2]:
			self.actions["Hard_Drop"]=True
			self.actions["Left"]=False
			self.actions["Right"]=False
		elif self.tetris.tetromino.pos[0]>self.position[0]:
			self.actions["Right"]=False
			if self.actions["Left"]:
				self.actions["Left"]=False
			else:
				self.actions["Left"]=True
		elif self.tetris.tetromino.pos[0]<self.position[0]:
			self.actions["Left"]=False
			if self.actions["Right"]:
				self.actions["Right"]=False
			else:
				self.actions["Right"]=True
		
		#print("now:"+str([self.tetris.tetromino.pos,self.tetris.tetromino.facing]))
		return False
	
	def update_q_value(self):
		#h =[self.heights[0], self.heights[1], self.heights[2], self.heights[3], self.heights[4], self.heights[5], self.heights[6], self.heights[7], self.heights[8], self.heights[9]]
		old_t_h = self.tallest_h
		old_t_p = self.tallest_p
		old_s_h = self.shortest_h
		old_s_p = self.shortest_p
		old_tetromino = self.current_piece
		self.current_piece = TETROMINO[self.tetris.tetromino.shape]
		reward = self.get_reward()
		
		#print(f"h: {old_h_mean}")
		#print(f"heights: {self.height_mean}")
		
		#old_q_value=self.q_values[self.heights[0], self.heights[1], self.heights[2], self.heights[3], self.heights[4], self.heights[5], self.heights[6], self.heights[7], self.heights[8], self.heights[9], TETROMINO[self.tetromino.shape],self.current_action]
		old_q_value=self.q_values[old_t_h, old_t_p, old_s_h, old_s_p, old_tetromino, self.old_action]
		
		#temporal_difference = reward + (discount_factor * np.max(self.q_values[self.heights[0], self.heights[1], self.heights[2], self.heights[3], self.heights[4], self.heights[5], self.heights[6], self.heights[7], self.heights[8], self.heights[9], self.current_piece])) - old_q_value
		temporal_difference = reward +(self.discount_factor * np.max(self.q_values[self.tallest_h, self.tallest_p, self.shortest_h, self.shortest_p, self.current_piece])) - old_q_value
		new_q_value = old_q_value + (self.learning_rate * temporal_difference)
		#self.q_values[h[0], h[1], h[2], h[3], h[4], h[5], h[6], h[7], h[8], h[9], self.current_piece,self.old_action] = new_q_value
		self.q_values[old_t_h, old_t_p, old_s_h, old_s_p, old_tetromino, self.old_action] = new_q_value
		#print(f"old {old_q_value}	new {new_q_value}")
	
	def get_reward(self):
		over_10, holes = self.update_parameters()
		reward=0
		if self.old_garbage>self.tetris.garbage:
			reward = 100*(self.old_garbage-self.tetris.garbage)
			self.old_garbage=0
		reward += 1000*self.tetris.attack+(1000*self.tetris.Back_to_Back)
		reward += 100*(self.tetris.total_lines_cleared-self.total_lines_cleared) - 100*over_10 - 10*holes
		self.total_lines_cleared=self.tetris.total_lines_cleared
		return reward
		
	
	def update_parameters(self):
		h=[]
		count=0
		over_10 =0
		holes=0
		for x in range(10):
			for y in range(20):#conta a altura das linhas
				if self.tetris.matrix[x][y]!=0:
					count = y
			h.append(count)#alturas
			for y in range(count):
				if self.tetris.matrix[x][y]==0:
					holes+=1
			if count>10:
				over_10+=1
			count=0
		
		self.tallest_h=max(h)
		self.tallest_p=h.index(max(h))
		self.shortest_h=min(h)
		self.shortest_p=h.index(min(h))
		
		return over_10, holes
		
	