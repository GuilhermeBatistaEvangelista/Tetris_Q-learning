import pygame

DIRECTION=["North", "East", "South", "West"]
TETROMINOS={
	'O':{"North":[(1,0), (2,0), (1,-1), (2,-1)],
		"East":[(1,0), (2,0), (1,-1), (2,-1)],
		"South":[(1,0), (2,0), (1,-1), (2,-1)],
		"West":[(1,0), (2,0), (1,-1), (2,-1)]},
	'T':{"North":[(1,0), (0,-1), (1,-1), (2,-1)],
		"East":[(1,0), (1,-1), (2,-1), (1,-2)],
		"South":[(1,-2), (0,-1), (1,-1), (2,-1)],
		"West":[(0,-1), (1,0), (1,-1), (1,-2)]},
	'J':{"North":[(0,0), (0,-1), (1,-1), (2,-1)],
		"East":[(1,0), (2,0), (1,-1), (1,-2)],
		"South":[(0,-1), (1,-1), (2,-1), (2,-2)],
		"West":[(0,-2), (1,0), (1,-1), (1,-2)]},
	'L':{"North":[(2,0), (0,-1), (1,-1), (2,-1)],
		"East":[(1,0), (1,-1), (1,-2), (2,-2)],
		"South":[(0,-1), (1,-1), (2,-1), (0,-2)],
		"West":[(0,0), (1,0), (1,-1), (1,-2)]},
	'I':{"North":[(0,-1), (1,-1), (2,-1), (3,-1)],
		"East":[(2,0), (2,-1), (2,-2), (2,-3)],
		"South":[(0,-2), (1,-2), (2,-2), (3,-2)],
		"West":[(1,0), (1,-1), (1,-2), (1,-3)]},
	'S':{"North":[(0,-1), (1,-1), (1,0), (2,0)],
		"East":[(1,0), (1,-1), (2,-1), (2,-2)],
		"South":[(0,-2), (1,-1), (1,-2), (2,-1)],
		"West":[(0,0), (0,-1), (1,-1), (1,-2)]},
	'Z':{"North":[(0,0), (1,0), (1,-1), (2,-1)],
		"East":[(2,0), (1,-1), (2,-1), (1,-2)],
		"South":[(0,-1), (1,-1), (1,-2), (2,-2)],
		"West":[(1,0), (0,-1), (1,-1), (0,-2)]},}
TPOINTS={
	"North":[(0,0), (2,0), (0,-2), (2,-2)],
	"East":[(2,0), (2,-2), (0,0), (0,-2)],
	"South":[(2,-2), (0,-2), (2,0), (0,0)],
	"West":[(0,-2), (0,0), (2,-2), (2,0)]}

class Block:
	def __init__(self, tetromino, start_pos, pos, color):
		self.tetromino = tetromino
		self.pos=[start_pos[0]+pos[0], start_pos[1]+pos[1]]		#posição do bloco
		self.color=color					#cor do bloco
		self.size = tetromino.tetris.block_size
		self.grid_start_pos_x = tetromino.tetris.grid_left
		self.grid_start_pos_y = tetromino.tetris.grid_y

	def draw(self, canvas):
		if self.pos[1]<20:
			rect = pygame.Rect(self.grid_start_pos_x+self.pos[0]*self.size, self.grid_start_pos_y-(self.pos[1]*self.size), self.size, self.size)
			pygame.draw.rect(canvas, pygame.Color(self.color), rect, 0)
		
class Tetromino:
	def __init__(self, tetris, shape, start_pos):
		self.tetris = tetris
		self.shape=shape
		self.facing=0
		self.pos=start_pos
		self.blocks=[Block(self, self.pos, pos, self.tetris.game.save["colors"][self.shape]) for pos in TETROMINOS[self.shape][DIRECTION[self.facing]]]

	def update(self, actions):
		pass
		
	def move(self, direction):
		for block in self.blocks:
			block.pos[0]+=direction[0]
			block.pos[1]+=direction[1]
		self.pos[0]+=direction[0]
		self.pos[1]+=direction[1]
		if not self.is_inside(self.blocks) or self.collision(self.blocks):
			for block in self.blocks:
				block.pos[0]-=direction[0]
				block.pos[1]-=direction[1]
			self.pos[0]-=direction[0]
			self.pos[1]-=direction[1]
			return False
		return True
		
		
	def rotation(self, rotate):
		facing = (self.facing+rotate)%4
		new_blocks=[Block(self, self.pos, pos, self.tetris.game.save["colors"][self.shape]) for pos in TETROMINOS[self.shape][DIRECTION[facing]]]
		if self.is_inside(new_blocks) and (not self.collision(new_blocks)):#Se esta dentro da matriz e não existe colisão
			self.blocks=new_blocks
			self.facing=facing
			return True
		else:#Se a rotação no ponto 1(ponto visual) falhar, usa SRS
			if self.shape=='I':	return self.SRS_I(rotate)
			if self.shape=='T':	return self.SRS_T(rotate)
			if self.shape=='L':	return self.SRS_L(rotate)
			if self.shape=='J':	return self.SRS_J(rotate)
			if self.shape=='S':	return self.SRS_S(rotate)
			if self.shape=='Z':	return self.SRS_Z(rotate)
	
	def is_inside(self, blocks):#verifica se o tetromino esta dentro da matriz
		for block in blocks:
			if (block.pos[0]<=-1) or (block.pos[0]>=10) or (block.pos[1]<=-1):
				return False
		return True
	
	def collision(self, blocks):#verifica se a posição esta vazia
		for block in blocks:
			if self.tetris.matrix[block.pos[0]][block.pos[1]] !=0:
				return True
		return False
		
	def get_ABCD(self):
		A=[self.pos[0]+TPOINTS[DIRECTION[self.facing]][0][0], self.pos[1]+TPOINTS[DIRECTION[self.facing]][0][1]]
		B=[self.pos[0]+TPOINTS[DIRECTION[self.facing]][1][0], self.pos[1]+TPOINTS[DIRECTION[self.facing]][1][1]]
		C=[self.pos[0]+TPOINTS[DIRECTION[self.facing]][2][0], self.pos[1]+TPOINTS[DIRECTION[self.facing]][2][1]]
		D=[self.pos[0]+TPOINTS[DIRECTION[self.facing]][3][0], self.pos[1]+TPOINTS[DIRECTION[self.facing]][3][1]]
		return[A,B,C,D]
	
	def draw(self, canvas):
		for i in range(4):
			self.blocks[i].draw(canvas)
			
			
			
#SUPER ROTATION SYSTEM
	def rotation_offset(self, facing, offset):#rotação com offset
		position=[self.pos[0]+offset[0], self.pos[1]+offset[1]]
		new_blocks=[Block(self, position, pos, self.tetris.game.save["colors"][self.shape]) for pos in TETROMINOS[self.shape][DIRECTION[facing]]]
		if self.is_inside(new_blocks) and (not self.collision(new_blocks)):#Se esta dentro da matriz e não existe colisão
			self.blocks=new_blocks
			self.facing=facing
			self.pos=position
			return True
		return False
		

	def SRS_I(self, direction):
		#Ponto 2
		if self.facing==0:#Se a direção atual for North
			if direction==-1:#North to West
				if self.rotation_offset(((self.facing+direction)%4), (-1,0)): return True
			else:#North to East
				if self.rotation_offset(((self.facing+direction)%4), (-2,0)): return True
		elif self.facing==1:#Se a direção atual for East
			if direction==-1:#East to North
				if self.rotation_offset(((self.facing+direction)%4), (2,0)): return True
			else:#East to South
				if self.rotation_offset(((self.facing+direction)%4), (-1,0)): return True
		elif self.facing==2:#Se a direção atual for South
			if direction==-1:#South to East
				if self.rotation_offset(((self.facing+direction)%4), (1,0)): return True
			else:#South to West
				if self.rotation_offset(((self.facing+direction)%4), (2,0)): return True
		elif self.facing==3:#Se a direção atual for West
			if direction==-1:#West to South
				if self.rotation_offset(((self.facing+direction)%4), (-2,0)): return True
			else:#West to North
				if self.rotation_offset(((self.facing+direction)%4), (1,0)): return True
		#Ponto 3
		if self.facing==0:#Se a direção atual for North
			if direction==-1:#North to West
				if self.rotation_offset(((self.facing+direction)%4), (2,0)): return True
			else:#North to East
				if self.rotation_offset(((self.facing+direction)%4), (1,0)): return True
		elif self.facing==1:#Se a direção atual for East
			if direction==-1:#East to North
				if self.rotation_offset(((self.facing+direction)%4), (-1,0)): return True
			else:#East to South
				if self.rotation_offset(((self.facing+direction)%4), (2,0)): return True
		elif self.facing==2:#Se a direção atual for South
			if direction==-1:#South to East
				if self.rotation_offset(((self.facing+direction)%4), (-2,0)): return True
			else:#South to West
				if self.rotation_offset(((self.facing+direction)%4), (-1,0)): return True
		elif self.facing==3:#Se a direção atual for West
			if direction==-1:#West to South
				if self.rotation_offset(((self.facing+direction)%4), (1,0)): return True
			else:#West to North
				if self.rotation_offset(((self.facing+direction)%4), (-2,0)): return True
		#Ponto 4
		if self.facing==0:#Se a direção atual for North
			if direction==-1:#North to West
				if self.rotation_offset(((self.facing+direction)%4), (-1,2)): return True
			else:#North to East
				if self.rotation_offset(((self.facing+direction)%4), (-2,-1)): return True
		elif self.facing==1:#Se a direção atual for East
			if direction==-1:#East to North
				if self.rotation_offset(((self.facing+direction)%4), (2,1)): return True
			else:#East to South
				if self.rotation_offset(((self.facing+direction)%4), (-1,2)): return True
		elif self.facing==2:#Se a direção atual for South
			if direction==-1:#South to East
				if self.rotation_offset(((self.facing+direction)%4), (1,-2)): return True
			else:#South to West
				if self.rotation_offset(((self.facing+direction)%4), (2,1)): return True
		elif self.facing==3:#Se a direção atual for West
			if direction==-1:#West to South
				if self.rotation_offset(((self.facing+direction)%4), (-2,-1)): return True
			else:#West to North
				if self.rotation_offset(((self.facing+direction)%4), (1,-2)): return True
		#Ponto 5
		if self.facing==0:#Se a direção atual for North
			if direction==-1:#North to West
				if self.rotation_offset(((self.facing+direction)%4), (2,-1)): return True
			else:#North to East
				if self.rotation_offset(((self.facing+direction)%4), (1,2)): return True
		elif self.facing==1:#Se a direção atual for East
			if direction==-1:#East to North
				if self.rotation_offset(((self.facing+direction)%4), (-1,-2)): return True
			else:#East to South
				if self.rotation_offset(((self.facing+direction)%4), (2,-1)): return True
		elif self.facing==2:#Se a direção atual for South
			if direction==-1:#South to East
				if self.rotation_offset(((self.facing+direction)%4), (-2,1)): return True
			else:#South to West
				if self.rotation_offset(((self.facing+direction)%4), (-1,-2)): return True
		elif self.facing==3:#Se a direção atual for West
			if direction==-1:#West to South
				if self.rotation_offset(((self.facing+direction)%4), (1,2)): return True
			else:#West to North
				if self.rotation_offset(((self.facing+direction)%4), (-2,1)): return True
		return False

	def SRS_T(self, direction):
		#Ponto 2
		if self.facing==0:#Se a direção atual for North
			if direction==-1:#North to West
				if self.rotation_offset(((self.facing+direction)%4), (1,0)): return True
			else:#North to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,0)): return True
		elif self.facing==1:#Se a direção atual for East
			if direction==-1:#East to North
				if self.rotation_offset(((self.facing+direction)%4), (1,0)): return True
			else:#East to South
				if self.rotation_offset(((self.facing+direction)%4), (1,0)): return True
		elif self.facing==2:#Se a direção atual for South
			if direction==-1:#South to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,0)): return True
			else:#South to West
				if self.rotation_offset(((self.facing+direction)%4), (1,0)): return True
		elif self.facing==3:#Se a direção atual for West
			if direction==-1:#West to South
				if self.rotation_offset(((self.facing+direction)%4), (-1,0)): return True
			else:#West to North
				if self.rotation_offset(((self.facing+direction)%4), (-1,0)): return True
		#Ponto 3
		if self.facing==0:#Se a direção atual for North
			if direction==-1:#North to West
				if self.rotation_offset(((self.facing+direction)%4), (1,1)): return True
			else:#North to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,1)): return True
		elif self.facing==1:#Se a direção atual for East
			if direction==-1:#East to North
				if self.rotation_offset(((self.facing+direction)%4), (1,-1)): return True
			else:#East to South
				if self.rotation_offset(((self.facing+direction)%4), (1,-1)): return True
		elif self.facing==2:#Se a direção atual for South
			pass		#não é usado
		elif self.facing==3:#Se a direção atual for West
			if direction==-1:#West to South
				if self.rotation_offset(((self.facing+direction)%4), (-1,-1)): return True
			else:#West to North
				if self.rotation_offset(((self.facing+direction)%4), (-1,-1)): return True
		#Ponto 4
		if self.facing==0:#Se a direção atual for North
			pass		#não é usado
		elif self.facing==1:#Se a direção atual for East
			if direction==-1:#East to North
				if self.rotation_offset(((self.facing+direction)%4), (0,2)): return True
			else:#East to South
				if self.rotation_offset(((self.facing+direction)%4), (0,2)): return True
		elif self.facing==2:#Se a direção atual for South
			if direction==-1:#South to East
				if self.rotation_offset(((self.facing+direction)%4), (0,-2)): return True
			else:#South to West
				if self.rotation_offset(((self.facing+direction)%4), (0,-2)): return True
		elif self.facing==3:#Se a direção atual for West
			if direction==-1:#West to South
				if self.rotation_offset(((self.facing+direction)%4), (0,2)): return True
			else:#West to North
				if self.rotation_offset(((self.facing+direction)%4), (0,2)): return True
		#Ponto 5
		if self.facing==0:#Se a direção atual for North
			if direction==-1:#North to West
				if self.rotation_offset(((self.facing+direction)%4), (1,-2)): return True
			else:#North to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,-2)): return True
		elif self.facing==1:#Se a direção atual for East
			if direction==-1:#East to North
				if self.rotation_offset(((self.facing+direction)%4), (1,2)): return True
			else:#East to South
				if self.rotation_offset(((self.facing+direction)%4), (1,2)): return True
		elif self.facing==2:#Se a direção atual for South
			if direction==-1:#South to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,-2)): return True
			else:#South to West
				if self.rotation_offset(((self.facing+direction)%4), (1,-2)): return True
		elif self.facing==3:#Se a direção atual for West
			if direction==-1:#West to South
				if self.rotation_offset(((self.facing+direction)%4), (-1,2)): return True
			else:#West to North
				if self.rotation_offset(((self.facing+direction)%4), (-1,2)): return True
		return False

	def SRS_L(self, direction):
		#Ponto 2
		if self.facing==0:#Se a direção atual for North
			if direction==-1:#North to West
				if self.rotation_offset(((self.facing+direction)%4), (1,0)): return True
			else:#North to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,0)): return True
		elif self.facing==1:#Se a direção atual for East
			if direction==-1:#East to North
				if self.rotation_offset(((self.facing+direction)%4), (1,0)): return True
			else:#East to South
				if self.rotation_offset(((self.facing+direction)%4), (1,0)): return True
		elif self.facing==2:#Se a direção atual for South
			if direction==-1:#South to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,0)): return True
			else:#South to West
				if self.rotation_offset(((self.facing+direction)%4), (1,0)): return True
		elif self.facing==3:#Se a direção atual for West
			if direction==-1:#West to South
				if self.rotation_offset(((self.facing+direction)%4), (-1,0)): return True
			else:#West to North
				if self.rotation_offset(((self.facing+direction)%4), (-1,0)): return True
		#Ponto 3
		if self.facing==0:#Se a direção atual for North
			if direction==-1:#North to West
				if self.rotation_offset(((self.facing+direction)%4), (1,1)): return True
			else:#North to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,1)): return True
		elif self.facing==1:#Se a direção atual for East
			if direction==-1:#East to North
				if self.rotation_offset(((self.facing+direction)%4), (1,-1)): return True
			else:#East to South
				if self.rotation_offset(((self.facing+direction)%4), (1,-1)): return True
		elif self.facing==2:#Se a direção atual for South
			if direction==-1:#South to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,1)): return True
			else:#South to West
				if self.rotation_offset(((self.facing+direction)%4), (1,1)): return True
		elif self.facing==3:#Se a direção atual for West
			if direction==-1:#West to South
				if self.rotation_offset(((self.facing+direction)%4), (-1,-1)): return True
			else:#West to North
				if self.rotation_offset(((self.facing+direction)%4), (-1,-1)): return True
		#Ponto 4
		if self.facing==0:#Se a direção atual for North
			if direction==-1:#North to West
				if self.rotation_offset(((self.facing+direction)%4), (0,-2)): return True
			else:#North to East
				if self.rotation_offset(((self.facing+direction)%4), (0,-2)): return True
		elif self.facing==1:#Se a direção atual for East
			if direction==-1:#East to North
				if self.rotation_offset(((self.facing+direction)%4), (0,2)): return True
			else:#East to South
				if self.rotation_offset(((self.facing+direction)%4), (0,2)): return True
		elif self.facing==2:#Se a direção atual for South
			if direction==-1:#South to East
				if self.rotation_offset(((self.facing+direction)%4), (0,-2)): return True
			else:#South to West
				if self.rotation_offset(((self.facing+direction)%4), (0,-2)): return True
		elif self.facing==3:#Se a direção atual for West
			if direction==-1:#West to South
				if self.rotation_offset(((self.facing+direction)%4), (0,2)): return True
			else:#West to North
				if self.rotation_offset(((self.facing+direction)%4), (0,2)): return True
		#Ponto 5
		if self.facing==0:#Se a direção atual for North
			if direction==-1:#North to West
				if self.rotation_offset(((self.facing+direction)%4), (1,-2)): return True
			else:#North to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,-2)): return True
		elif self.facing==1:#Se a direção atual for East
			if direction==-1:#East to North
				if self.rotation_offset(((self.facing+direction)%4), (1,2)): return True
			else:#East to South
				if self.rotation_offset(((self.facing+direction)%4), (1,2)): return True
		elif self.facing==2:#Se a direção atual for South
			if direction==-1:#South to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,-2)): return True
			else:#South to West
				if self.rotation_offset(((self.facing+direction)%4), (1,-2)): return True
		elif self.facing==3:#Se a direção atual for West
			if direction==-1:#West to South
				if self.rotation_offset(((self.facing+direction)%4), (-1,2)): return True
			else:#West to North
				if self.rotation_offset(((self.facing+direction)%4), (-1,2)): return True
		return False

	def SRS_J(self, direction):
		#Ponto 2
		if self.facing==0:#Se a direção atual for North
			if direction==-1:#North to West
				if self.rotation_offset(((self.facing+direction)%4), (1,0)): return True
			else:#North to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,0)): return True
		elif self.facing==1:#Se a direção atual for East
			if direction==-1:#East to North
				if self.rotation_offset(((self.facing+direction)%4), (1,0)): return True
			else:#East to South
				if self.rotation_offset(((self.facing+direction)%4), (1,0)): return True
		elif self.facing==2:#Se a direção atual for South
			if direction==-1:#South to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,0)): return True
			else:#South to West
				if self.rotation_offset(((self.facing+direction)%4), (1,0)): return True
		elif self.facing==3:#Se a direção atual for West
			if direction==-1:#West to South
				if self.rotation_offset(((self.facing+direction)%4), (-1,0)): return True
			else:#West to North
				if self.rotation_offset(((self.facing+direction)%4), (-1,0)): return True
		#Ponto 3
		if self.facing==0:#Se a direção atual for North
			if direction==-1:#North to West
				if self.rotation_offset(((self.facing+direction)%4), (1,1)): return True
			else:#North to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,1)): return True
		elif self.facing==1:#Se a direção atual for East
			if direction==-1:#East to North
				if self.rotation_offset(((self.facing+direction)%4), (1,-1)): return True
			else:#East to South
				if self.rotation_offset(((self.facing+direction)%4), (1,-1)): return True
		elif self.facing==2:#Se a direção atual for South
			if direction==-1:#South to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,1)): return True
			else:#South to West
				if self.rotation_offset(((self.facing+direction)%4), (1,1)): return True
		elif self.facing==3:#Se a direção atual for West
			if direction==-1:#West to South
				if self.rotation_offset(((self.facing+direction)%4), (-1,-1)): return True
			else:#West to North
				if self.rotation_offset(((self.facing+direction)%4), (-1,-1)): return True
		#Ponto 4
		if self.facing==0:#Se a direção atual for North
			if direction==-1:#North to West
				if self.rotation_offset(((self.facing+direction)%4), (0,-2)): return True
			else:#North to East
				if self.rotation_offset(((self.facing+direction)%4), (0,-2)): return True
		elif self.facing==1:#Se a direção atual for East
			if direction==-1:#East to North
				if self.rotation_offset(((self.facing+direction)%4), (0,2)): return True
			else:#East to South
				if self.rotation_offset(((self.facing+direction)%4), (0,2)): return True
		elif self.facing==2:#Se a direção atual for South
			if direction==-1:#South to East
				if self.rotation_offset(((self.facing+direction)%4), (0,-2)): return True
			else:#South to West
				if self.rotation_offset(((self.facing+direction)%4), (0,-2)): return True
		elif self.facing==3:#Se a direção atual for West
			if direction==-1:#West to South
				if self.rotation_offset(((self.facing+direction)%4), (0,2)): return True
			else:#West to North
				if self.rotation_offset(((self.facing+direction)%4), (0,2)): return True
		#Ponto 5
		if self.facing==0:#Se a direção atual for North
			if direction==-1:#North to West
				if self.rotation_offset(((self.facing+direction)%4), (1,-2)): return True
			else:#North to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,-2)): return True
		elif self.facing==1:#Se a direção atual for East
			if direction==-1:#East to North
				if self.rotation_offset(((self.facing+direction)%4), (1,2)): return True
			else:#East to South
				if self.rotation_offset(((self.facing+direction)%4), (1,2)): return True
		elif self.facing==2:#Se a direção atual for South
			if direction==-1:#South to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,-2)): return True
			else:#South to West
				if self.rotation_offset(((self.facing+direction)%4), (1,-2)): return True
		elif self.facing==3:#Se a direção atual for West
			if direction==-1:#West to South
				if self.rotation_offset(((self.facing+direction)%4), (-1,2)): return True
			else:#West to North
				if self.rotation_offset(((self.facing+direction)%4), (-1,2)): return True
		return False

	def SRS_S(self, direction):
		#Ponto 2
		if self.facing==0:#Se a direção atual for North
			if direction==-1:#North to West
				if self.rotation_offset(((self.facing+direction)%4), (1,0)): return True
			else:#North to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,0)): return True
		elif self.facing==1:#Se a direção atual for East
			if direction==-1:#East to North
				if self.rotation_offset(((self.facing+direction)%4), (1,0)): return True
			else:#East to South
				if self.rotation_offset(((self.facing+direction)%4), (1,0)): return True
		elif self.facing==2:#Se a direção atual for South
			if direction==-1:#South to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,0)): return True
			else:#South to West
				if self.rotation_offset(((self.facing+direction)%4), (1,0)): return True
		elif self.facing==3:#Se a direção atual for West
			if direction==-1:#West to South
				if self.rotation_offset(((self.facing+direction)%4), (-1,0)): return True
			else:#West to North
				if self.rotation_offset(((self.facing+direction)%4), (-1,0)): return True
		#Ponto 3
		if self.facing==0:#Se a direção atual for North
			if direction==-1:#North to West
				if self.rotation_offset(((self.facing+direction)%4), (1,1)): return True
			else:#North to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,1)): return True
		elif self.facing==1:#Se a direção atual for East
			if direction==-1:#East to North
				if self.rotation_offset(((self.facing+direction)%4), (1,-1)): return True
			else:#East to South
				if self.rotation_offset(((self.facing+direction)%4), (1,-1)): return True
		elif self.facing==2:#Se a direção atual for South
			if direction==-1:#South to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,1)): return True
			else:#South to West
				if self.rotation_offset(((self.facing+direction)%4), (1,1)): return True
		elif self.facing==3:#Se a direção atual for West
			if direction==-1:#West to South
				if self.rotation_offset(((self.facing+direction)%4), (-1,-1)): return True
			else:#West to North
				if self.rotation_offset(((self.facing+direction)%4), (-1,-1)): return True
		#Ponto 4
		if self.facing==0:#Se a direção atual for North
			if direction==-1:#North to West
				if self.rotation_offset(((self.facing+direction)%4), (0,-2)): return True
			else:#North to East
				if self.rotation_offset(((self.facing+direction)%4), (0,-2)): return True
		elif self.facing==1:#Se a direção atual for East
			if direction==-1:#East to North
				if self.rotation_offset(((self.facing+direction)%4), (0,2)): return True
			else:#East to South
				if self.rotation_offset(((self.facing+direction)%4), (0,2)): return True
		elif self.facing==2:#Se a direção atual for South
			if direction==-1:#South to East
				if self.rotation_offset(((self.facing+direction)%4), (0,-2)): return True
			else:#South to West
				if self.rotation_offset(((self.facing+direction)%4), (0,-2)): return True
		elif self.facing==3:#Se a direção atual for West
			if direction==-1:#West to South
				if self.rotation_offset(((self.facing+direction)%4), (0,2)): return True
			else:#West to North
				if self.rotation_offset(((self.facing+direction)%4), (0,2)): return True
		#Ponto 5
		if self.facing==0:#Se a direção atual for North
			if direction==-1:#North to West
				if self.rotation_offset(((self.facing+direction)%4), (1,-2)): return True
			else:#North to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,-2)): return True
		elif self.facing==1:#Se a direção atual for East
			if direction==-1:#East to North
				if self.rotation_offset(((self.facing+direction)%4), (1,2)): return True
			else:#East to South
				if self.rotation_offset(((self.facing+direction)%4), (1,2)): return True
		elif self.facing==2:#Se a direção atual for South
			if direction==-1:#South to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,2)): return True
			else:#South to West
				if self.rotation_offset(((self.facing+direction)%4), (1,-2)): return True
		elif self.facing==3:#Se a direção atual for West
			if direction==-1:#West to South
				if self.rotation_offset(((self.facing+direction)%4), (-1,2)): return True
			else:#West to North
				if self.rotation_offset(((self.facing+direction)%4), (-1,2)): return True
		return False

	def SRS_Z(self, direction):
		#Ponto 2
		if self.facing==0:#Se a direção atual for North
			if direction==-1:#North to West
				if self.rotation_offset(((self.facing+direction)%4), (1,0)): return True
			else:#North to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,0)): return True
		elif self.facing==1:#Se a direção atual for East
			if direction==-1:#East to North
				if self.rotation_offset(((self.facing+direction)%4), (1,0)): return True
			else:#East to South
				if self.rotation_offset(((self.facing+direction)%4), (1,0)): return True
		elif self.facing==2:#Se a direção atual for South
			if direction==-1:#South to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,0)): return True
			else:#South to West
				if self.rotation_offset(((self.facing+direction)%4), (1,0)): return True
		elif self.facing==3:#Se a direção atual for West
			if direction==-1:#West to South
				if self.rotation_offset(((self.facing+direction)%4), (-1,0)): return True
			else:#West to North
				if self.rotation_offset(((self.facing+direction)%4), (-1,0)): return True
		#Ponto 3
		if self.facing==0:#Se a direção atual for North
			if direction==-1:#North to West
				if self.rotation_offset(((self.facing+direction)%4), (1,1)): return True
			else:#North to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,1)): return True
		elif self.facing==1:#Se a direção atual for East
			if direction==-1:#East to North
				if self.rotation_offset(((self.facing+direction)%4), (1,-1)): return True
			else:#East to South
				if self.rotation_offset(((self.facing+direction)%4), (1,-1)): return True
		elif self.facing==2:#Se a direção atual for South
			if direction==-1:#South to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,1)): return True
			else:#South to West
				if self.rotation_offset(((self.facing+direction)%4), (1,1)): return True
		elif self.facing==3:#Se a direção atual for West
			if direction==-1:#West to South
				if self.rotation_offset(((self.facing+direction)%4), (-1,1)): return True
			else:#West to North
				if self.rotation_offset(((self.facing+direction)%4), (-1,-1)): return True
		#Ponto 4
		if self.facing==0:#Se a direção atual for North
			if direction==-1:#North to West
				if self.rotation_offset(((self.facing+direction)%4), (0,-2)): return True
			else:#North to East
				if self.rotation_offset(((self.facing+direction)%4), (0,-2)): return True
		elif self.facing==1:#Se a direção atual for East
			if direction==-1:#East to North
				if self.rotation_offset(((self.facing+direction)%4), (0,2)): return True
			else:#East to South
				if self.rotation_offset(((self.facing+direction)%4), (0,2)): return True
		elif self.facing==2:#Se a direção atual for South
			if direction==-1:#South to East
				if self.rotation_offset(((self.facing+direction)%4), (0,-2)): return True
			else:#South to West
				if self.rotation_offset(((self.facing+direction)%4), (0,-2)): return True
		elif self.facing==3:#Se a direção atual for West
			if direction==-1:#West to South
				if self.rotation_offset(((self.facing+direction)%4), (0,2)): return True
			else:#West to North
				if self.rotation_offset(((self.facing+direction)%4), (0,2)): return True
		#Ponto 5
		if self.facing==0:#Se a direção atual for North
			if direction==-1:#North to West
				if self.rotation_offset(((self.facing+direction)%4), (1,-2)): return True
			else:#North to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,-2)): return True
		elif self.facing==1:#Se a direção atual for East
			if direction==-1:#East to North
				if self.rotation_offset(((self.facing+direction)%4), (1,2)): return True
			else:#East to South
				if self.rotation_offset(((self.facing+direction)%4), (1,2)): return True
		elif self.facing==2:#Se a direção atual for South
			if direction==-1:#South to East
				if self.rotation_offset(((self.facing+direction)%4), (-1,-2)): return True
			else:#South to West
				if self.rotation_offset(((self.facing+direction)%4), (1,-2)): return True
		elif self.facing==3:#Se a direção atual for West
			if direction==-1:#West to South
				if self.rotation_offset(((self.facing+direction)%4), (-1,2)): return True
			else:#West to North
				if self.rotation_offset(((self.facing+direction)%4), (-1,2)): return True
		return False
