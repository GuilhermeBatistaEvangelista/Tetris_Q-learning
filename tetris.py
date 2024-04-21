import pygame
from tetromino import Tetromino
import random

class Tetris():
	def __init__(self, game, center):
		self.game = game
		self.language()
		self.block_size=30
		self.center=center # o centro horizontal do jogo
		self.grid_left=center+(self.block_size*-5)#posição X do inicio da grid
		self.grid_y=self.block_size*(3+19)#posição Y do inicio da grid
		self.matrix = [[0 for y in range(40)] for x in range(10)]# 10x20 são o campo jogavel e 10X20 são zona de buffer
		self.bag=['T', 'O', 'J', 'L', 'I', 'S', 'Z']
		random.shuffle(self.bag)	
		self.bagpos=0
		self.next_tetromino()#pega o primeiro tetromino
		self.wait_time=0			#timer de espera entre peças
		self.time=0			#timer para queda
		self.hold_time=0 # tempo segundando um botão de movimento vertical
		self.hold = None
		self.can_hold=True		#se pode-se usar a função hold
		self.falling=True		#se o tetromino esta caindo ou em lock down
		self.moves_while_lockdown=0		#quantidade de vazes que o contador foi reiniciado
		self.locking_timer=0
		self.lowest_falling_height=40
		#GAME OVER conditions:
		self.TOP_OUT=False		#Se o ataque de um oponente força os blocos axistentes acima da zona de buffer
		self.LOCK_OUT=False		#Se o player posiciona ym tetromino completamente acima do topo da matrix
		self.BLOCK_OUT=False	#Se o proximo tetromino esta bloqueado por um bloco existente
		#Scoring and, etc...
		self.level=1
		self.total_lines_cleared=0
		self.lines_until_next=self.level*5
		self.score=0
		self.Back_to_Back=False
		self.T_spin=False		#se o quinto ponto de rotação de um tetromino T for usado toda rotação subsequente sera T-spin
		self.last_move_rotation=False#marca se o ultimo movimento foi rotação, usado para verificar T-spins e Mini T-spins
		self.garbage=0
		self.garbage_gap_count=0
		self.garbage_gap_pos=random.randint(0, 9) #numero aleatoria entre 0 e 9
		self.attack=0
		self.move_rec=[]
	
	def update(self, deltatime, actions):
		if self.BLOCK_OUT or self.LOCK_OUT or self.BLOCK_OUT:#			if GAME OVER
			return False
		self.attack=0	#limpa o ataque
		if self.wait_time<0.2:
			self.wait_time+=deltatime
			return True
		
		temp_moves=self.moves_while_lockdown # guarda a de quantidade movimentos realizados quando em lock down
		#Movimento vertical
		move_x = actions["Right"] - actions["Left"] #recebe o valor do movimento horizontal
		if move_x==0:self.hold_time=0
		if move_x!=0:
			if self.hold_time==0 or self.hold_time>0.1:
				moved=self.tetromino.move([move_x,0]) # realiza o movimento vertical do tetromino
				self.hold_time=0
				if not self.falling and moved:
					self.moves_while_lockdown+=1
			self.hold_time += deltatime
		#Rotação
		rotation = actions["Rotate_Right"] - actions["Rotate_Left"] #recebe o valor de rotação
		if rotation!=0:
			if self.tetromino.rotation(rotation): # realiza a rotação do tetromino
				self.last_move_rotation=True
				if not self.falling:
					self.moves_while_lockdown+=1
			actions["Rotate_Right"], actions["Rotate_Left"]=False, False
		#Hold
		if actions["Hold"] and self.can_hold:
			shape=self.tetromino.shape
			if self.hold is not None:
				self.tetromino = Tetromino(self, self.hold.shape, [3,20])
				self.BLOCK_OUT=self.tetromino.collision(self.tetromino.blocks)#testar BLOCK OUT
				self.falling = self.tetromino.move([0,-1])
			else:
				self.next_tetromino()
			self.hold= Tetromino(self, shape, [-5,15])
			self.lowest_falling_height=40
			self.moves_while_lockdown=0
			self.last_move_rotation=False
			self.locking_timer=0
			self.time=0				#reseta o timer de queda
			self.can_hold=False		#trava o uso da função hold até uma peça ser colocada
			actions["Hold"]=False
		#Hard Fall
		if actions["Hard_Drop"]:
			while self.tetromino.move([0,-1]):
				self.score+=2		#2 pontos para cada linha percorrida em um Hard_Drop
			self.lock_tetromino()
			actions["Hard_Drop"]=False
		
		#Fall
		if self.tetromino.move([0,-1]):#se existe espaço para cair
			self.tetromino.move([0,1])
			self.falling = True
			if self.tetromino.pos[1]<self.lowest_falling_height:
				self.lowest_falling_height=self.tetromino.pos[1]
				self.moves_while_lockdown=0
				self.locking_timer=0
			self.last_move_rotation=False
		else:	self.falling = False
		
		if self.falling:#Falling phase
			self.time+=deltatime
			if self.time>(((0.8-((self.level - 1)*0.007))**(self.level - 1))/(1+19*actions["Soft_Drop"])):
				self.time=0
				self.tetromino.move([0,-1])
				self.score+=1*actions["Soft_Drop"]		#1 pontos para cada linha percorrida em um Soft_Drop
		else:#Lock phase
			if self.moves_while_lockdown<15 and temp_moves!=self.moves_while_lockdown:#se o timer de lock down for reiniciado
				self.locking_timer=0
			else:
				self.locking_timer+=deltatime
				if self.locking_timer>=0.5:#se o timer atingir o limite
					self.lock_tetromino()
		return True

	def draw(self, canvas):
		rect = pygame.Rect(self.grid_left-self.block_size*6, 1.5*self.block_size, self.block_size*22, self.block_size*23)
		pygame.draw.rect(canvas, pygame.Color("gold3"), rect, 0, 15)
		pygame.draw.rect(canvas, pygame.Color("gold"), rect, 3, 15)
		#desenhar score
		self.game.text(canvas,self.words[0], 24, pygame.Color("black"), self.grid_left+self.block_size*1.5, self.block_size*2.5)
		self.game.text(canvas,str(int(self.score)), 24, pygame.Color("black"), self.grid_left+self.block_size*5, 2.5*self.block_size)
		#desenha Hold
		self.game.text(canvas,self.words[1], 24, pygame.Color("black"), self.grid_left-self.block_size*3, self.block_size*5.5)
		rect = pygame.Rect(self.grid_left-self.block_size*5.5, 6*self.block_size, self.block_size*5, self.block_size*4)
		pygame.draw.rect(canvas, pygame.Color("black"), rect, 0, 10)
		pygame.draw.rect(canvas, pygame.Color("gold"), rect, 3, 10)
		if self.hold is not None:
			self.hold.draw(canvas)
		for y in range(2):
			for x in range(4):
				rect = pygame.Rect(self.grid_left-self.block_size*5+x*self.block_size, 8*self.block_size-(y*self.block_size), self.block_size, self.block_size)
				pygame.draw.rect(canvas, pygame.Color("black"), rect, 1)
		#desenha Next
		self.game.text(canvas,self.words[2], 24, pygame.Color("black"), self.grid_left+self.block_size*13, self.block_size*5.5)
		rect = pygame.Rect(self.grid_left+self.block_size*10.5, 6*self.block_size, self.block_size*5, self.block_size*4)
		pygame.draw.rect(canvas, pygame.Color("black"), rect, 0, 10)
		pygame.draw.rect(canvas, pygame.Color("gold"), rect, 3, 10)
		self.next.draw(canvas)
		for y in range(2):
			for x in range(4):
				rect = pygame.Rect(self.grid_left+self.block_size*11+x*self.block_size, 8*self.block_size-(y*self.block_size), self.block_size, self.block_size)
				pygame.draw.rect(canvas, pygame.Color("black"), rect, 1)
		self.game.text(canvas,"Garbage  "+str(self.garbage), 24, pygame.Color("black"), self.grid_left+self.block_size*13, self.block_size*10.5)
		#desenhar level
		self.game.text(canvas,self.words[3], 24, pygame.Color("black"), self.grid_left+self.block_size*1, self.block_size*23.5)
		self.game.text(canvas,str(int(self.level)), 24, pygame.Color("black"), self.grid_left+self.block_size*3, 23.5*self.block_size)
		#desenhar lines clears
		self.game.text(canvas,self.words[4], 24, pygame.Color("black"), self.grid_left+self.block_size*7, self.block_size*23.5)
		self.game.text(canvas,str(int(self.total_lines_cleared)), 24, pygame.Color("black"), self.grid_left+self.block_size*9, 23.5*self.block_size)
		#desenha o fundo da matriz
		rect = pygame.Rect(self.grid_left, 3*self.block_size, self.block_size*10, self.block_size*20)
		pygame.draw.rect(canvas, pygame.Color("black"), rect, 0)
		#desenha os blocos da matriz
		for x in range(10):
			for y in range(20):
				if self.matrix[x][y] !=0:
					if self.matrix[x][y] !=-1:
						self.matrix[x][y].draw(canvas)
					else:
						rect = pygame.Rect(self.grid_left+x*self.block_size, self.grid_y-(y*self.block_size), self.block_size, self.block_size)
						pygame.draw.rect(canvas, pygame.Color("gray55"), rect, 0)
		#desenha o tetromino
		if self.tetromino!=0 and self.wait_time>=0.2:
			self.tetromino.draw(canvas)
			'''if self.tetromino.shape=='T':#	show T-points
				A,B,C,D = self.tetromino.get_ABCD()
				rect = pygame.Rect(self.grid_left+A[0]*self.block_size, self.grid_y-(A[1]*self.block_size), self.block_size, self.block_size)
				pygame.draw.rect(canvas, pygame.Color("red"), rect, 0)
				rect = pygame.Rect(self.grid_left+B[0]*self.block_size, self.grid_y-(B[1]*self.block_size), self.block_size, self.block_size)
				pygame.draw.rect(canvas, pygame.Color("yellow"), rect, 0)
				rect = pygame.Rect(self.grid_left+C[0]*self.block_size, self.grid_y-(C[1]*self.block_size), self.block_size, self.block_size)
				pygame.draw.rect(canvas, pygame.Color("gray55"), rect, 0)
				rect = pygame.Rect(self.grid_left+D[0]*self.block_size, self.grid_y-(D[1]*self.block_size), self.block_size, self.block_size)
				pygame.draw.rect(canvas, pygame.Color("blue"), rect, 0)'''
		#desenha a matriz
		for y in range(20):
			for x in range(10):
				rect = pygame.Rect(self.grid_left+x*self.block_size, self.grid_y-(y*self.block_size), self.block_size, self.block_size)
				pygame.draw.rect(canvas, pygame.Color("gray"), rect, 1)
		rect = pygame.Rect(self.grid_left, self.grid_y-19*self.block_size, self.block_size*10, self.block_size*20)
		pygame.draw.rect(canvas, pygame.Color("gray"), rect, 2, 3)
		#desenha os movimentos realizados
		for x in range(len(self.move_rec)):
			self.game.text(canvas,self.move_rec[x], 16, pygame.Color("gray"+str(round(x*7))), self.grid_left-self.block_size*3, self.block_size*(11.5+x))
	
	
	def next_tetromino(self):
		self.tetromino = Tetromino(self, self.bag[self.bagpos], [3,20])
		if self.tetromino.collision(self.tetromino.blocks): #testar BLOCK OUT
			self.BLOCK_OUT=True
			return False
		self.falling = self.tetromino.move([0,-1])
		self.bagpos+=1
		if self.bagpos==7:
			self.bagpos=0
			random.shuffle(self.bag)
		self.next= Tetromino(self, self.bag[self.bagpos], [11,15])
		self.can_hold=True
		
		
		self.lowest_falling_height=40
		self.moves_while_lockdown=0
		self.locking_timer=0
		self.time=0
		return True

	def lock_tetromino(self):
		self.LOCK_OUT=True
		for block in self.tetromino.blocks:
			self.matrix[block.pos[0]][block.pos[1]] = block	#guarda o bloco na matriz
			if block.pos[1]<20:#testar Lock Out
				self.LOCK_OUT=False		#se algum bloco do tetromino estiver dentro da matriz não sera Lock Out
		if self.LOCK_OUT:
			return False
		self.pattern_recognition()
		self.next_tetromino()
		self.wait_time=0
	
	def pattern_recognition(self):#r
		lines=self.full_line()
		num_lines=len(lines)
		mini_T_spin=False
		#testar para t-spin e mini t-spin, se for T e o 5 ponto de rotação não tenha sido usado
		if self.tetromino.shape=='T' and (not self.T_spin) and self.last_move_rotation:
			A,B,C,D = self.tetromino.get_ABCD()		#Pega os pontos A,B,C e D
			if (C[0]<=-1 or C[0]>=10 or C[1]<=-1):#se C(e consequentemente D) estiverem encostado no chão ou parede da matriz
				if(self.matrix[A[0]][A[1]]!=0 and self.matrix[B[0]][B[1]]!=0):
					#se A e B estiverem ocupados
					self.T_spin=True
				elif(self.matrix[A[0]][A[1]]!=0 or self.matrix[B[0]][B[1]]!=0):
					#se A ou B  estiverem ocupados
					mini_T_spin=True
			else:#se C(e consequentemente D) NÃO estiverem encostados no chão ou parede
				#T-spin
				if (self.matrix[A[0]][A[1]]!=0 and self.matrix[B[0]][B[1]]!=0 and(self.matrix[C[0]][C[1]]!=0 or self.matrix[D[0]][D[1]]!=0)):
					#se A e B e (C ou D) estiverem ocupados
					self.T_spin=True
				elif (self.matrix[C[0]][C[1]]!=0 and self.matrix[D[0]][D[1]]!=0 and(self.matrix[A[0]][A[1]]!=0 or self.matrix[B[0]][B[1]]!=0)):
					#se C e D e (A ou B) estiverem ocupados
					mini_T_spin=True
		#Moves:
		awarded_lines=0
		if num_lines==0:#Sem Line clear
			if self.T_spin:			#T-Spin
				self.score+=400*self.level+(400*self.level*0.5*self.Back_to_Back)
				awarded_lines=4+(4*0.5*self.Back_to_Back)
				self.attack=0+(1*self.Back_to_Back)
				self.Back_to_Back=True
				self.move_rec.insert(0,"T_spin")
			elif mini_T_spin:		#Mini T-Spin
				self.score+=100*self.level+(100*self.level*0.5*self.Back_to_Back)
				awarded_lines=1+(1*0.5*self.Back_to_Back)
				self.attack=0+(1*self.Back_to_Back)
				self.Back_to_Back=True
				self.move_rec.insert(0,"Mini T_spin")
		elif num_lines==1:#1 line clear
			if self.T_spin:			#T-Spin Single
				self.score+=800*self.level+(800*self.level*0.5*self.Back_to_Back)
				awarded_lines=8+(8*0.5*self.Back_to_Back)
				self.attack=2+(1*self.Back_to_Back)
				self.Back_to_Back=True
				self.move_rec.insert(0,"T_spin Single")
			elif mini_T_spin:		#Mini T-Spin Single
				self.score+=200*self.level+(200*self.level*0.5*self.Back_to_Back)
				awarded_lines=2+(2*0.5*self.Back_to_Back)
				self.attack=0+(1*self.Back_to_Back)
				self.Back_to_Back=True
				self.move_rec.insert(0,"Mini T_spin Single")
			else:					#Single
				self.score+=100*self.level
				awarded_lines=1
				self.attack=0
				self.Back_to_Back=False
				self.move_rec.insert(0,"Single")
		elif num_lines==2:#2 line clear
			if self.T_spin:			#T-Spin Double
				self.score+=1200*self.level+(1200*self.level*0.5*self.Back_to_Back)
				awarded_lines=12+(12*0.5*self.Back_to_Back)
				self.attack=4+(1*self.Back_to_Back)
				self.Back_to_Back=True
				self.move_rec.insert(0,"T_spin Double")
			else:					#Double
				self.score+=300*self.level
				awarded_lines=3
				self.attack=1
				self.Back_to_Back=False
				self.move_rec.insert(0,"Double")
		elif num_lines==3:#3 line clear
			if self.T_spin:			#T-Spin Triple
				self.score+=1600*self.level+(1600*self.level*0.5*self.Back_to_Back)
				awarded_lines=16+(16*0.5*self.Back_to_Back)
				self.attack=6+(1*self.Back_to_Back)
				self.Back_to_Back=True
				self.move_rec.insert(0,"T_spin Triple")
			else:					#Triple
				self.score+=500*self.level
				awarded_lines=5
				self.attack=2
				self.Back_to_Back=False
				self.move_rec.insert(0,"Triple")
		elif num_lines==4:#Tetris
			self.score+=800*self.level+(800*self.level*0.5*self.Back_to_Back)
			awarded_lines=8+(8*0.5*self.Back_to_Back)
			self.attack=4+(1*self.Back_to_Back)
			self.Back_to_Back=True
			self.move_rec.insert(0,"Tetris")
		self.T_spin=False	#reseta o marcador de T-Spin
		if len(self.move_rec)>10:
			self.move_rec.pop()
		#Atualiza o level, linhas até o proximo level e o total de linhas
		if self.level<15:#15 é o level maximo
			self.lines_until_next-=awarded_lines
			while self.lines_until_next<=0:
				self.level+=1
				self.lines_until_next+=self.level*5
		self.total_lines_cleared+=awarded_lines
		#Ataque e contra-ataque
		self.attack_and_counter()
		if len(lines)!=0:#se alguma linha tiver sido completa, Line clear
			self.clear_lines(lines)#Apaga as linhas completadas
		self.add_garbage()
	
	def full_line(self):#indentifica as linhas completas 
		lines=[]
		for y in range(40):
			column=0
			for x in range(10):
				if self.matrix[x][y] !=0:
					column+=1
			if column== 10:#se todas as colunas da linha estiverem ocupadas
				lines.append(y)
		return lines		#retorna uma lista com as linhas completas
	
	def attack_and_counter(self):
		if self.garbage!=0 and self.attack!=0:#Calcula o resultado do ataque e do garbage, se ambos existirem
			if self.garbage>self.attack:
				self.garbage -= self.attack
				self.attack=0
			elif self.garbage<self.attack:
				self.attack -= self.garbage
				self.garbage=0
			else:
				self.attack, self.garbage = 0, 0
		

	def clear_lines(self, lines):#Apaga as linhas completas
		for i in range(len(lines)):
			for x in range(10):
				for y in range(lines[i]+1,40):
					self.matrix[x][y-1] = self.matrix[x][y]
					if self.matrix[x][y-1]!=0 and self.matrix[x][y-1]!= -1:
						self.matrix[x][y-1].pos[1]-=1
			for j in range(i,len(lines)):
				lines[j]-=1
		for x in range(10):
			self.matrix[x][39]=0
	
	def add_garbage(self):#Adicionar as linhas de garbage
		for x in range(10):#checa top out
			if self.matrix[x][39-self.garbage]!=0:
			#se exitir um bloco na linha que saira do topo da matriz com a adição de garbage, resultara em TOP_OUT
				self.TOP_OUT=True
				return
		while self.garbage>0:#se existir garbage
			#todos os blocos da matriz 1 linha
			for x in range(10):
				for y in range(38, -1, -1):#de 38 até 0
					self.matrix[x][y+1] = self.matrix[x][y]
					if self.matrix[x][y+1]!=0 and self.matrix[x][y+1]!= -1:
						self.matrix[x][y+1].pos[1]+=1
			#adicionar linha no fundo da matriz
			for x in range(10):
				self.matrix[x][0] = -1
			self.matrix[self.garbage_gap_pos][0]=0
			self.garbage_gap_count+=1
			if self.garbage_gap_count==8:#muda a posição do espaço vazio nas linhas de garbage a cada 8 linhas
				self.garbage_gap_count=0
				self.garbage_gap_pos=random.randint(0, 9)
			self.garbage-=1
	
	def language(self):
		if self.game.save["language"] == "EN":
			self.words = ["Score","Hold","Next","Level","Lines"]
			
		elif self.game.save["language"] == "PT":
			self.words = ["Pontuação","Hold","Proxima","Nível","Linhas"]
			