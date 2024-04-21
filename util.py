import os, json, pygame

def load_existing_save(savefile):
	with open(os.path.join(savefile), 'r+') as file:
		controls = json.load(file)
	return controls

def write_save(data):
	with open(os.path.join(os.getcwd(),'save.json'), 'w') as file:
		json.dump(data, file)

def load_save():
	try:# Se um save ja foi carregado 
		save = load_existing_save('save.json')
	except:# cria um savefile 
		save = create_save()
		write_save(save)
	return save


def create_save():
	new_save = {
	"resolution":{"W": 1366, "H": 768},
	"controls":{"Left": pygame.K_a, "Right": pygame.K_d, "Up": pygame.K_w, "Down": pygame.K_s, "Confirm": pygame.K_SPACE,
		"Soft_Drop": pygame.K_s, "Hard_Drop": pygame.K_SPACE, "Rotate_Right": pygame.K_w, "Rotate_Left": pygame.K_z,
		"Hold": pygame.K_c},
	"colors":{"I": list(pygame.Color("aqua")), "J": list(pygame.Color("blue3")), "L": list(pygame.Color("coral")),
		"O": list(pygame.Color("gold1")), "S": list(pygame.Color("limegreen")), "Z": list(pygame.Color("red2")),
		"T": list(pygame.Color("orchid3"))},
	"language":"EN"}

	return new_save

def reset_keys(actions):
	for action in actions:
		actions[action] = False
	return actions