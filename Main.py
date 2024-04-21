import pygame
import time
import random
from Class import *
from util import load_save
from states.menu import Menu

class Game():
	def __init__(self):
		###########			LOAD SAVE			###########
		self.save = load_save()
		###########			INICIA JOGO			###########
		pygame.init()
		self.window_w, self.window_h = self.save["resolution"]["W"],self.save["resolution"]["H"] #recebe a resolução da janela salva
		self.window = pygame.display.set_mode((self.window_w,self.window_h))
		self.canvas_w, self.canvas_h = 1366, 768
		self.canvas = pygame.Surface((self.canvas_w,self.canvas_h)) # Canvas 16:9
		pygame.display.set_caption('Tretis Vs AI')  # Titulo da janela
		self.runGame = True	# Se esta sendo executado
		self.playGame = False	# se esta sendo jogado
		self.dtime, self.ptime = 0,0 # variaveis para independência da taxa de quadros
		self.actions = {"Left": False, "Right": False, "Up": False, "Down": False, "Scape": False, "Confirm": False,
			"Soft_Drop": False,"Hard_Drop": False, "Rotate_Right": False, "Rotate_Left": False,
			"Hold": False } # dicionario com os comandos
		self.state_stack=[] #pilha de estados
		self.load_state()
		self.mouse=False
		self.mouse_pos=(0,0)
		self.font = pygame.font.Font('arial.ttf', 150)
		self.font20 = pygame.font.Font('arial.ttf', 20)
		self.font24 = pygame.font.Font('arial.ttf', 24)
		self.font36 = pygame.font.Font('arial.ttf', 36)

	def loop(self):
		self.deltatime()
		self.eventos()
		self.update()
		self.draw()

	def deltatime(self): # calcula o deltatime para independencia de frames
		now = time.time()
		self.dtime = now-self.ptime
		self.ptime = now

	def eventos(self):###########			Eventos			###########
		self.mouse=False#reseta o click do mouse
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.runGame, self.playGame = False, False
			if event.type == pygame.MOUSEBUTTONDOWN:#registra o clique e sua posição
				if event.button==1:#se for o botão esquerdo
					self.mouse=True
					pos = pygame.mouse.get_pos()#pega posição do mouse
					self.mouse_pos=(int(pos[0]*(self.canvas_w/self.window_w)),int(pos[1]*(self.canvas_h/self.window_h)))
				if event.button==3:#se for o botão direito
					self.actions["Scape"] = True
			if event.type == pygame.KEYDOWN:#		TECLA PRESSIONADA
				self.last_key=event.key#guarda a ultima tecla pressionada
				#print(pygame.key.name(event.key))
				if event.key == pygame.K_ESCAPE:
					self.actions["Scape"] = True
				if event.key == self.save["controls"]["Left"]:
					self.actions["Left"] = True
					#self.window_w, self.window_h= 1366, 768
					#self.window = pygame.display.set_mode((self.window_w,self.window_h))
				if event.key == self.save["controls"]["Right"]:
					self.actions["Right"] = True
					#self.window_w, self.window_h= 480, 270
					#self.window = pygame.display.set_mode((self.window_w,self.window_h))
				if event.key == self.save["controls"]["Up"]:
					self.actions["Up"] = True
				if event.key == self.save["controls"]["Down"]:
					self.actions["Down"] = True
				if event.key == self.save["controls"]["Confirm"] or event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
					self.actions["Confirm"] = True
				if event.key == self.save["controls"]["Soft_Drop"]:
					self.actions["Soft_Drop"] = True
				if event.key == self.save["controls"]["Hard_Drop"]:
					self.actions["Hard_Drop"] = True
				if event.key == self.save["controls"]["Rotate_Right"]:
					self.actions["Rotate_Right"] = True
				if event.key == self.save["controls"]["Rotate_Left"]:
					self.actions["Rotate_Left"] = True
				if event.key == self.save["controls"]["Hold"]:
					self.save["language"]="BR"
					self.actions["Hold"] = True
			
			if event.type == pygame.KEYUP:#		TECLA SOLTA
				if event.key == pygame.K_ESCAPE:
					self.actions["Scape"] = False
				if event.key == self.save["controls"]["Left"]:
					self.actions["Left"] = False
				if event.key == self.save["controls"]["Right"]:
					self.actions["Right"] = False
				if event.key == self.save["controls"]["Up"]:
					self.actions["Up"] = False
				if event.key == self.save["controls"]["Down"]:
					self.actions["Down"] = False
				if event.key == self.save["controls"]["Confirm"] or event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
					self.actions["Confirm"] = False
				if event.key == self.save["controls"]["Soft_Drop"]:
					self.actions["Soft_Drop"] = False
				if event.key == self.save["controls"]["Hard_Drop"]:
					self.actions["Hard_Drop"] = False
				if event.key == self.save["controls"]["Rotate_Right"]:
					self.actions["Rotate_Right"] = False
				if event.key == self.save["controls"]["Rotate_Left"]:
					self.actions["Rotate_Left"] = False
				if event.key == self.save["controls"]["Hold"]:
					self.save["language"]="EN"
					self.actions["Hold"] = False

	def update(self):
		self.state_stack[-1].update(self.dtime, self.actions) #passa deltatime e o dicionario de comandos para o estado no topo da pilha
		
		
	def draw(self):
		self.state_stack[-1].draw(self.canvas) #passa a superficie o estado no topo da pilha
		self.window.blit(pygame.transform.scale(self.canvas,(self.window_w,self.window_h)),(0,0))
		pygame.display.flip()
	
	def text(self, canvas, text, size, color,x,y):
		if size==20:
			text_canvas = self.font20.render(text, True, color) # gera o texto
		elif size==24:
			text_canvas = self.font24.render(text, True, color) # gera o texto
		elif size==36:
			text_canvas = self.font36.render(text, True, color) # gera o texto
		else:
			text_canvas = self.font.render(text, True, color) # gera o texto
			text_canvas = pygame.transform.smoothscale_by(text_canvas, size/150)
		text_retan = text_canvas.get_rect() # recebe o retangulo do texto
		text_retan.center = (x,y) # posiçiona o texto
		canvas.blit(text_canvas,text_retan)

	def load_state(self):
		self.menu = Menu(self)
		self.state_stack.append(self.menu)

	def reset_actions(self):# redefine todas as ações
            for action in self.actions:
                self.actions[action] = False


g= Game()
while g.runGame:
	g.loop()
	
#print(pygame.font.get_fonts())