import pygame
from states.state import State
from util import load_save, write_save

class Menu_Opt(State):
	def __init__(self, game):
		State.__init__(self, game)
		self.language()
		self.positiony = 0
		self.positionx = 0
		self.rec_reso = pygame.Rect((self.game.canvas_w/2,self.game.canvas_h/2), (self.game.canvas_w*0.9,self.game.canvas_h/8))#retangulo que encapsula o menu de resolução
		#retangulos que encapsulam as opções do menu de resolução
		self.rec_reso_opts= [pygame.Rect((self.game.canvas_w/2,self.game.canvas_h/2), (self.game.canvas_w/6,self.game.canvas_h/10)) for i in range(4)]#retangulos que encapsulam as opções do menu de resolução
		for i in range(len(self.rec_reso_opts)):
			self.rec_reso_opts[i].center=(self.game.canvas_w*(0.3+0.18*i),self.game.canvas_h*0.1)
		###########retangulos que encapsulam as opções do menu de controles
		self.recs= [pygame.Rect((self.game.canvas_w/2,self.game.canvas_h/2), (self.game.canvas_w*0.26,self.game.canvas_h/10)) for i in range(10)]#retangulos que encapsulam as opções do menu de resolução
		for i in range(5):#coluna da esquerda
			self.recs[i].center=(self.game.canvas_w*0.25,self.game.canvas_h*(0.25+i*0.13))
		for i in range(5,10):#coluna da direita
			self.recs[i].center=(self.game.canvas_w*0.75,self.game.canvas_h*(0.25+(i-5)*0.13))
		#retangulos que encapsulam as opções do menu de linguagem
		self.rec_langs= [pygame.Rect((self.game.canvas_w/2,self.game.canvas_h/2), (self.game.canvas_w/25,self.game.canvas_h/12)) for i in range(2)]
		self.rec_langs[0].center=(self.game.canvas_w*0.255,self.game.canvas_h*0.9)
		self.rec_langs[1].center=(self.game.canvas_w*0.3,self.game.canvas_h*0.9)
		#retangulos que encapsulam as opções do menu de reset e save
		self.rec_savres= [pygame.Rect((self.game.canvas_w/2,self.game.canvas_h/2), (self.game.canvas_w/5,self.game.canvas_h/10)) for i in range(2)]
		self.rec_savres[0].center=(self.game.canvas_w*0.6,self.game.canvas_h*0.9)
		self.rec_savres[1].center=(self.game.canvas_w*0.85,self.game.canvas_h*0.9)
		
		self.waiting_key=False
		self.temp_key=None
		
	def update(self, deltatime, actions):
		if self.waiting_key and self.game.last_key!=6666:
			self.waiting_key=False
			self.swap_key()
		#	Controla o movimento pelo menu
		movex = actions["Down"] - actions["Up"] #recebe o valor do movimento vertical
		movey = actions["Right"] - actions["Left"] #recebe o valor do movimento horizontal
		if movex !=0 and (self.positiony==0 or self.positiony==6):
			self.positionx=0
		self.positiony = ((self.positiony + movex) % 7) # realiza o movimento vertical dentre as opções
		if self.positiony==0 or self.positiony==6:
			self.positionx = ((self.positionx + movey) % 4) # realiza o movimento horizontal dentre as opções
		else:
			self.positionx = ((self.positionx + movey) % 2) # realiza o movimento horizontal dentre as opções
		
		if self.game.mouse:#se clicar
			#resoluções
			if self.rec_reso_opts[0].collidepoint(self.game.mouse_pos):#480X270
				actions["Confirm"]=True
				self.positionx, self.positiony=0,0
			if self.rec_reso_opts[1].collidepoint(self.game.mouse_pos):#640X360
				actions["Confirm"]=True
				self.positionx, self.positiony=1,0
			if self.rec_reso_opts[2].collidepoint(self.game.mouse_pos):#1366X768
				actions["Confirm"]=True
				self.positionx, self.positiony=2,0
			if self.rec_reso_opts[3].collidepoint(self.game.mouse_pos):#1920X1080
				actions["Confirm"]=True
				self.positionx, self.positiony=3,0
			#linguagem
			if self.rec_langs[0].collidepoint(self.game.mouse_pos):#EN
				actions["Confirm"]=True
				self.positionx, self.positiony=0,6
			if self.rec_langs[1].collidepoint(self.game.mouse_pos):#PT
				actions["Confirm"]=True
				self.positionx, self.positiony=1,6
			#Reset
			if self.rec_savres[0].collidepoint(self.game.mouse_pos):
				actions["Confirm"]=True
				self.positionx, self.positiony=2,6
			#Save
			if self.rec_savres[1].collidepoint(self.game.mouse_pos):
				actions["Confirm"]=True
				self.positionx, self.positiony=3,6
			#tecla de controle
			if self.recs[0].collidepoint(self.game.mouse_pos):#Left
				actions["Confirm"]=True
				self.positionx, self.positiony=0,1
			if self.recs[1].collidepoint(self.game.mouse_pos):#Right
				actions["Confirm"]=True
				self.positionx, self.positiony=0,2
			if self.recs[2].collidepoint(self.game.mouse_pos):#Up
				actions["Confirm"]=True
				self.positionx, self.positiony=0,3
			if self.recs[3].collidepoint(self.game.mouse_pos):#Down
				actions["Confirm"]=True
				self.positionx, self.positiony=0,4
			if self.recs[4].collidepoint(self.game.mouse_pos):#Confirm
				actions["Confirm"]=True
				self.positionx, self.positiony=0,5
			if self.recs[5].collidepoint(self.game.mouse_pos):#Soft Drop
				actions["Confirm"]=True
				self.positionx, self.positiony=1,1
			if self.recs[6].collidepoint(self.game.mouse_pos):#Hard Drop
				actions["Confirm"]=True
				self.positionx, self.positiony=1,2
			if self.recs[7].collidepoint(self.game.mouse_pos):#Rotate Right
				actions["Confirm"]=True
				self.positionx, self.positiony=1,3
			if self.recs[8].collidepoint(self.game.mouse_pos):#Rotate Left
				actions["Confirm"]=True
				self.positionx, self.positiony=1,4
			if self.recs[9].collidepoint(self.game.mouse_pos):#Hold
				actions["Confirm"]=True
				self.positionx, self.positiony=1,5
			
		if actions["Confirm"]:# caso selecione uma opção do menu
			if self.positiony==0 and self.res[self.positionx][0]!=self.game.window_w:#caso seja resolução diferente da atual
				self.game.window_w, self.game.window_h = self.res[self.positionx][0], self.res[self.positionx][1]
				self.game.save["resolution"]["W"], self.game.save["resolution"]["H"] = self.game.window_w, self.game.window_h
				self.game.window = pygame.display.set_mode((self.game.window_w,self.game.window_h))
				write_save(self.game.save)#salva anova resolução
			elif self.positiony==6:#caso seja a ultima coluna de opções
				if self.positionx==0:# EN
					self.game.save["language"] = "EN"
					self.language()
					write_save(self.game.save)
				if self.positionx==1:# PT
					self.game.save["language"] = "PT"
					self.language()
					write_save(self.game.save)
				if self.positionx==2:# Reset
					self.game.save["controls"]={"Left": pygame.K_a, "Right": pygame.K_d, "Up": pygame.K_w, "Down": pygame.K_s, "Confirm": pygame.K_SPACE,
						"Soft_Drop": pygame.K_s, "Hard_Drop": pygame.K_SPACE, "Rotate_Right": pygame.K_w, "Rotate_Left": pygame.K_z,
						"Hold": pygame.K_c}
				if self.positionx==3:# save
					write_save(self.game.save)
					self.state_out()			#retorna depois de salvar
					self.game.save=load_save()
			elif self.positiony!=0:#caso seja uma tecla de controle
				if self.positionx==1:
					x=self.positiony+4
				else:
					x=self.positiony-1
				#desenha a tela e espera a entrada de uma tecla
				self.temp_key=self.game.save["controls"][self.con[x]]
				self.game.save["controls"][self.con[x]]=6666
				self.game.last_key=6666
				self.waiting_key=True
		if actions["Scape"]:# retorna
			self.state_out()
			self.game.save=load_save()
		self.game.reset_actions()
	
	
	def draw(self, canvas):
		w,h = self.game.canvas_w, self.game.canvas_h
		canvas.fill(pygame.Color("aquamarine3"))
		#desenha o menu de resolução da tela
		self.rec_reso.center=(w/2,h*0.1)
		self.game.text(canvas, self.option[0], int(h/15), pygame.Color("black"), w*0.13, h/10)
		pygame.draw.rect(canvas, pygame.Color("white"), self.rec_reso,  int(h/150), int(h/50))
		for i in range(len(self.res)):
			if self.positiony==0 and self.positionx==i:
				pygame.draw.rect(canvas, pygame.Color("aliceblue"), self.rec_reso_opts[i],  0, int(h/50))
			if self.res[i][0]==self.game.save["resolution"]["W"]:
				pygame.draw.rect(canvas, pygame.Color("red"), self.rec_reso_opts[i],  int(h/150), int(h/50))
			else:
				pygame.draw.rect(canvas, pygame.Color("white"), self.rec_reso_opts[i],  int(h/150), int(h/50))
			self.game.text(canvas, str(self.res[i][0])+"X"+str(self.res[i][1]), int(h/15), pygame.Color("black"), w*(0.3+0.18*i), h*0.1)
		
		#desenha o menu de seleção de teclas
		if self.positiony>0 and self.positiony<6:
			if self.positionx==0:#coluna da esquerda
				pygame.draw.rect(canvas, pygame.Color("aliceblue"), self.recs[self.positiony-1],  0, int(h/50))
			else:#coluna da direita
				pygame.draw.rect(canvas, pygame.Color("aliceblue"), self.recs[self.positiony-1+5],  0, int(h/50))
		for i in range(10):#coluna da esquerda
			pygame.draw.rect(canvas, pygame.Color("white"), self.recs[i],  int(h/150), int(h/50))
			if i<5:#coluna da esquerda
				self.game.text(canvas, self.menucon[i]+":"+pygame.key.name(self.game.save["controls"][self.con[i]]), int(h/17), pygame.Color("black"), w*0.25, h*(0.25+i*0.13))
			else:#coluna da direita
				self.game.text(canvas, self.menucon[i]+":"+pygame.key.name(self.game.save["controls"][self.con[i]]), int(h/17), pygame.Color("black"), w*0.75, h*(0.25+(i-5)*0.13))
		
		#desenha as opções de linguagem
		rec = pygame.Rect((w/2,h/2), (w*0.26,h/10))
		rec.center=(w*0.2,h*0.9)
		self.game.text(canvas, self.option[2], int(h/16), pygame.Color("black"), w*0.16, h*0.9)
		pygame.draw.rect(canvas, pygame.Color("white"), rec,  int(h/150), int(h/50))
		#		EN
		if self.positiony==6 and self.positionx==0:
			pygame.draw.rect(canvas, pygame.Color("white"), self.rec_langs[0],  0, int(h/50))
		self.game.text(canvas, "EN", int(h/20), pygame.Color("black"), w*0.255, h*0.9)
		if self.game.save["language"]=="EN":
			pygame.draw.rect(canvas, pygame.Color("red"), self.rec_langs[0],  int(h/200), int(h/50))
		else:
			pygame.draw.rect(canvas, pygame.Color("white"), self.rec_langs[0],  int(h/200), int(h/50))
		#			PT
		if self.positiony==6 and self.positionx==1:
			pygame.draw.rect(canvas, pygame.Color("white"), self.rec_langs[1],  0, int(h/50))
		self.game.text(canvas, "PT", int(h/20), pygame.Color("black"), w*0.3, h*0.9)
		if self.game.save["language"]=="PT":
			pygame.draw.rect(canvas, pygame.Color("red"), self.rec_langs[1],  int(h/200), int(h/50))
		else:
			pygame.draw.rect(canvas, pygame.Color("white"), self.rec_langs[1],  int(h/200), int(h/50))
		
		#desenha o botão de reset
		if self.positiony==6 and self.positionx==2:
			pygame.draw.rect(canvas, pygame.Color("aliceblue"), self.rec_savres[0],  0, int(h/50))
		self.game.text(canvas, self.option[3], int(h/10), pygame.Color("black"), w*0.6, h*0.9)
		pygame.draw.rect(canvas, pygame.Color("white"), self.rec_savres[0],  int(h/150), int(h/50))
		#desenha o botão de salvar
		if self.positiony==6 and self.positionx==3:
			pygame.draw.rect(canvas, pygame.Color("aliceblue"), self.rec_savres[1],  0, int(h/50))
		self.game.text(canvas, self.option[4], int(h/10), pygame.Color("black"), w*0.85, h*0.9)
		pygame.draw.rect(canvas, pygame.Color("white"), self.rec_savres[1],  int(h/150), int(h/50))
		
		#self.game.text(canvas, "x"+str(self.positionx)+" y:"+str(self.positiony), int(self.game.canvas_h/10), [200,100,255], self.game.canvas_w*0.5, self.game.canvas_h/2) #print posição
		
	
	def swap_key(self):# espera até uma tecla ser pressionada e retorna ela
		if self.positionx==1:
			x=self.positiony+4
		else:
			x=self.positiony-1
		key=self.game.last_key
		if key!=pygame.K_ESCAPE and key!=pygame.K_RETURN:# se a tecla a ser atribuida não esc ou enter
			self.game.save["controls"][self.con[x]]=key
			for i in range(10):
				if i!=x and self.game.save["controls"][self.con[i]]==key: # caso a tecla ja esteja associada a outro comando
					if x<2 or i<2: #se um dos comandos conflitantes for left ou right, troca as teclas conflitantes
						self.game.save["controls"][self.con[i]]=self.temp_key
					elif x<5 and i<5: #se dois comando de navegação conflitarem, troca as teclas conflitantes
						self.game.save["controls"][self.con[i]]=self.temp_key
					elif x>4 and i>4: #se dois comando do jogo conflitarem, troca as teclas conflitantes
						self.game.save["controls"][self.con[i]]=self.temp_key
		else:
			self.game.save["controls"][self.con[x]]=self.temp_key
		self.game.reset_actions()
	
	def language(self):
		self.con = ["Left", "Right", "Up", "Down", "Confirm", "Soft_Drop", "Hard_Drop", "Rotate_Right", "Rotate_Left", "Hold"]
		if self.game.save["language"] == "EN":
			self.option = ["Resolution","Keybinds","Language","Reset","Save"]
			self.menucon = ["Left", "Right", "Up", "Down", "Confirm", "Soft Drop", "Hard Drop", "Rotate Right", "Rotate Left", "Hold"]
		
		elif self.game.save["language"] == "PT":
			self.option = ["Resolução","Teclas","Linguagem","Resetar","Salvar"]
			self.menucon = ["Esquerda", "Direita", "Cima", "Baixo", "Confirmar", "Queda Suave", "Queda Brusca", "Girar p/Direita", "Girar p/Esquerda", "Segurar"]
		self.res = [(480, 270), (640, 360), (1366, 768), (1920, 1080)]
		