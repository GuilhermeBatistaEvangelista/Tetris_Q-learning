from tetromino import Tetromino
import copy

class Greedy():
	def __init__(self, tetris):
		self.tetris = tetris
		self.matrix = self.tetris.matrix
	
	def update(self):
		self.values=[]
		#print("piece:"+str([self.tetris.tetromino.pos,self.tetris.tetromino.facing]))
		tetromino = Tetromino(self.tetris, self.tetris.tetromino.shape, [3,20])
		tetromino.rotation(self.tetris.tetromino.facing)
		tetromino.move([0,-1])
		tetromino.move([self.tetris.tetromino.pos[0]-tetromino.pos[0],self.tetris.tetromino.pos[1]-tetromino.pos[1]])
		#tetromino.move([0,-1])
		#print("new:"+str([tetromino.pos,tetromino.facing]))
		#print(tetromino.shape)
		#for i in range(68):
		self.search(tetromino)
		
		return self.values
	
	def search(self, tetromino):
		#print(' ')
		#print(tetromino.shape)
		rotations=3
		if tetromino.shape=='O':
			rotations=0
		elif tetromino.shape=='I' or tetromino.shape=='S' or tetromino.shape=='Z':
			rotations=1
		
		#print(f'Facing:{tetromino.facing}')
		self.get_moves(tetromino)
		while rotations!=0:
			tetromino.rotation(1)
			#print(f'Facing:{tetromino.facing}')
			self.get_moves(tetromino)
			rotations-=1
	
	def get_moves(self, tetromino):#movimenta a peça por todas as colunas
		#print('move_x')
		count=0
		while tetromino.move([-1,0]):#move para a esquerda até onde é possivel 
			pass
		self.drop(tetromino)#movimento de queda
		count=0
		#print(f'	{tetromino.pos}')
		while tetromino.move([1,0]):#move para a direita até onde é possivel 
			count-=1
			#print(tetromino.pos)
			self.drop(tetromino)#movimento de queda
		tetromino.move([count,0])#retorna a peça para o centro
	
	def drop(self, tetromino):
		count=0
		while tetromino.move([0,-1]):#drop piece
			count+=1
		blocks_pos=[]
		for block in tetromino.blocks:
			blocks_pos.append(block.pos)
		num_lines = self.full_line(blocks_pos)
		self.save_move(tetromino, self.patters(num_lines, tetromino ), self.get_parameters(blocks_pos, num_lines) )
		tetromino.move([0,count])#retorna a peça para a linha inicial
		
	def save_move(self, tetromino, scores, parameters):
		if tetromino.pos[1]<=self.tetris.tetromino.pos[1]:
			pos=[tetromino.pos[0], tetromino.pos[1], tetromino.facing]
			self.values.append([pos, scores[0], scores[1], scores[2], scores[3], parameters[0], sum(parameters[1]), parameters[1]])
			#					pos, num_lines, awarded_lines,   score, attack,					holes, soma das alturas, alturas
			#					0,			1,				2, 		3, 		4,						5,				6,		7
		
	def full_line(self, blocks_pos):#conta linhas completas
		lines=[]
		matrix=self.matrix
		for y in range(40):
			column=0
			for x in range(10):
				if matrix[x][y]!=0 or (blocks_pos[0][0]==x and blocks_pos[0][1]==y) or (blocks_pos[1][0]==x and blocks_pos[1][1]==y) or (blocks_pos[2][0]==x and blocks_pos[2][1]==y) or (blocks_pos[3][0]==x and blocks_pos[3][1]==y):
					column+=1
			if column== 10:#se todas as colunas da linha estiverem ocupadas
				lines.append(y)
		return len(lines)		#retorna o numero de linhas completas
	
	def get_parameters(self, blocks_pos, num_lines):
		holes=0
		heights=[]
		matrix=self.matrix
		count=0
		for x in range(10):
			for y in range(20):
				if matrix[x][y]!=0 or (blocks_pos[0][0]==x and blocks_pos[0][1]==y) or (blocks_pos[1][0]==x and blocks_pos[1][1]==y) or (blocks_pos[2][0]==x and blocks_pos[2][1]==y) or (blocks_pos[3][0]==x and blocks_pos[3][1]==y):
					count = y
			for y in range(count):
				if matrix[x][y]==0 and (blocks_pos[0][0]!=x or blocks_pos[0][1]!=y) and (blocks_pos[1][0]!=x or blocks_pos[1][1]!=y) and (blocks_pos[2][0]!=x or blocks_pos[2][1]!=y) and (blocks_pos[3][0]!=x or blocks_pos[3][1]!=y):
					holes+=1
			heights.append(count-num_lines)
			count=0
		return [holes, heights]
	
	def patters(self, num_lines, tetromino):
		T_spin=False
		mini_T_spin=False
		#testar para t-spin e mini t-spin
		if tetromino.shape=='T':
			A,B,C,D = tetromino.get_ABCD()		#Pega os pontos A,B,C e D
			if (C[0]<=-1 or C[0]>=10 or C[1]<=-1):#se C(e consequentemente D) estiverem encostado no chão ou parede da matriz
				if(self.matrix[A[0]][A[1]]!=0 and self.matrix[B[0]][B[1]]!=0):
					#se A e B estiverem ocupados
					T_spin=True
				elif(self.matrix[A[0]][A[1]]!=0 or self.matrix[B[0]][B[1]]!=0):
					#se A ou B  estiverem ocupados
					mini_T_spin=True
			else:#se C(e consequentemente D) NÃO estiverem encostados no chão ou parede
				#T-spin
				if (self.matrix[A[0]][A[1]]!=0 and self.matrix[B[0]][B[1]]!=0 and(self.matrix[C[0]][C[1]]!=0 or self.matrix[D[0]][D[1]]!=0)):
					#se A e B e (C ou D) estiverem ocupados
					T_spin=True
				elif (self.matrix[C[0]][C[1]]!=0 and self.matrix[D[0]][D[1]]!=0 and(self.matrix[A[0]][A[1]]!=0 or self.matrix[B[0]][B[1]]!=0)):
					#se C e D e (A ou B) estiverem ocupados
					mini_T_spin=True
		
		#Moves:
		awarded_lines=0
		score=0
		attack=0
		if num_lines==0:#Sem Line clear
			if T_spin:			#T-Spin
				score+=400*self.tetris.level+(400*self.tetris.level*0.5*self.tetris.Back_to_Back)
				awarded_lines=4+(4*0.5*self.tetris.Back_to_Back)
				attack=0+(1*self.tetris.Back_to_Back)
				self.tetris.Back_to_Back=True
			elif mini_T_spin:		#Mini T-Spin
				score+=100*self.tetris.level+(100*self.tetris.level*0.5*self.tetris.Back_to_Back)
				awarded_lines=1+(1*0.5*self.tetris.Back_to_Back)
				attack=0+(1*self.tetris.Back_to_Back)
				self.tetris.Back_to_Back=True
		elif num_lines==1:#1 line clear
			if T_spin:			#T-Spin Single
				score+=800*self.tetris.level+(800*self.tetris.level*0.5*self.tetris.Back_to_Back)
				awarded_lines=8+(8*0.5*self.tetris.Back_to_Back)
				attack=2+(1*self.tetris.Back_to_Back)
				self.tetris.Back_to_Back=True
			elif mini_T_spin:		#Mini T-Spin Single
				score+=200*self.tetris.level+(200*self.tetris.level*0.5*self.tetris.Back_to_Back)
				awarded_lines=2+(2*0.5*self.tetris.Back_to_Back)
				attack=0+(1*self.tetris.Back_to_Back)
				self.tetris.Back_to_Back=True
			else:					#Single
				score+=100*self.tetris.level
				awarded_lines=1
				attack=0
				self.tetris.Back_to_Back=False
		elif num_lines==2:#2 line clear
			if T_spin:			#T-Spin Double
				score+=1200*self.tetris.level+(1200*self.tetris.level*0.5*self.tetris.Back_to_Back)
				awarded_lines=12+(12*0.5*self.tetris.Back_to_Back)
				attack=4+(1*self.tetris.Back_to_Back)
				self.tetris.Back_to_Back=True
			else:					#Double
				score+=300*self.tetris.level
				awarded_lines=3
				attack=1
				self.tetris.Back_to_Back=False
		elif num_lines==3:#3 line clear
			if T_spin:			#T-Spin Triple
				score+=1600*self.tetris.level+(1600*self.tetris.level*0.5*self.tetris.Back_to_Back)
				awarded_lines=16+(16*0.5*self.tetris.Back_to_Back)
				attack=6+(1*self.tetris.Back_to_Back)
				self.tetris.Back_to_Back=True
			else:					#Triple
				score+=500*self.tetris.level
				awarded_lines=5
				attack=2
				self.tetris.Back_to_Back=False
		elif num_lines==4:#Tetris
			score+=800*self.tetris.level+(800*self.tetris.level*0.5*self.tetris.Back_to_Back)
			awarded_lines=8+(8*0.5*self.tetris.Back_to_Back)
			attack=4+(1*self.tetris.Back_to_Back)
			self.tetris.Back_to_Back=True
		return [num_lines, awarded_lines, score, attack]
