import pygame
from pygame.locals import *
from math import cos,sin,pi
import sys
import random


pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("Data/sounds/music_8bit_embience.ogg")
pygame.mixer.music.queue("Data/sounds/music_8bit_embience.ogg")
#~ pygame.mixer.music.queue("C:\\Users\\michael\\Music\\musique_jeu_spatiale.ogg")
pygame.mixer.music.set_volume(100)
pygame.mixer.music.play()
xMax = 1400
yMax = 1000

sMax = 9

window = pygame.display.set_mode((xMax,yMax))
Map = pygame.Surface((1400,1000))
clock = pygame.time.Clock()

black = pygame.Color(0,0,0)
white = pygame.Color(255,255,255)
space_blue = pygame.Color(0,155,178)#00BEBA

ACCEL_VAISSEAU = 0.2
VANG_VESSEAU = pi/60
VIT_LASER = 10
VIT_TIRS = 7


etoile_img = pygame.image.load("Data/Pictures/etoile.png")
etoile_img2 = pygame.image.load("Data/Pictures/etoile_vitesse_lumiere.png")

taille_x_vaisseau = 300
taille_y_vaisseau = 300

vaisseau_anim = pygame.transform.scale(pygame.image.load("Data/Pictures/vaisseau_anim.png"),(taille_x_vaisseau,taille_y_vaisseau))
vaisseau_anim1 = pygame.transform.scale(pygame.image.load("Data/Pictures/sprite/vaisseau_anim1.png"),(taille_x_vaisseau,taille_y_vaisseau))
vaisseau_anim2 = pygame.transform.scale(pygame.image.load("Data/Pictures/sprite/vaisseau_anim2.png"),(taille_x_vaisseau,taille_y_vaisseau))
vaisseau_anim3 = pygame.transform.scale(pygame.image.load("Data/Pictures/sprite/vaisseau_anim3.png"),(taille_x_vaisseau,taille_y_vaisseau))
vaisseau_anim4 = pygame.transform.scale(pygame.image.load("Data/Pictures/sprite/vaisseau_anim4.png"),(taille_x_vaisseau,taille_y_vaisseau))
vaisseau_anim5 = pygame.transform.scale(pygame.image.load("Data/Pictures/sprite/vaisseau_anim5.png"),(taille_x_vaisseau,taille_y_vaisseau))
#~ vaisseau_anim2 = pygame.transform.scale(pygame.image.load("C:\\Users\\michael\\Pictures\\vaisseau_anim2.png"),(300,300))
#~ vaisseau_anim3 = pygame.transform.scale(pygame.image.load("C:\\Users\\michael\\Pictures\\vaisseau_anim3.png"),(300,300))
#~ vaisseau_anim4 = pygame.transform.scale(pygame.image.load("C:\\Users\\michael\\Pictures\\vaisseau_anim4.png"),(300,300))
#~ vaisseau_anim5 = pygame.transform.scale(pygame.image.load("C:\\Users\\michael\\Pictures\\vaisseau_anim5.png"),(300,300))

munition_box = pygame.transform.scale(pygame.image.load("Data/Pictures/caisse_de_munition.png"),(100,100))
munition_box_despawn = pygame.transform.scale(pygame.image.load("Data/Pictures/caisse_de_munition_despawn.png"),(100,100))

player1 = pygame.image.load("Data/Pictures/vaisseau.png")
player1_gauche = pygame.image.load("Data/Pictures/vaisseau_gauche.png")
player1_droite = pygame.image.load("Data/Pictures/vaisseau_droite.png")
asteoride = pygame.image.load("Data/Pictures/Asteroid.png")
laser = pygame.image.load("Data/Pictures/laser.png")
logo_munition = pygame.image.load("Data/Pictures/logo_munition.png")

son_reacteur = pygame.mixer.Sound("Data/sounds/son_vaisseau_terminer.wav")
son_tire_laser = pygame.mixer.Sound("Data/sounds/tire_laser.ogg")
son_explosion = pygame.mixer.Sound("Data/sounds/explosion_vaisseau.ogg")
son_explosion2 = pygame.mixer.Sound("Data/sounds/explosion2_arcade.wav")
son_game_over = pygame.mixer.Sound("Data/sounds/Gameover_arcade.wav")
level_up = pygame.mixer.Sound("Data/sounds/levelup.wav")
speed_vaisseau = pygame.mixer.Sound("Data/sounds/speed_vaisseau.OGG")
son_caisse_munition = pygame.mixer.Sound("Data/sounds/munition_reload.OGG")


explosion1 = pygame.transform.scale(pygame.image.load("Data/Pictures/sprite/explosion1.png"),(150,150))
explosion2 = pygame.transform.scale(pygame.image.load("Data/Pictures/sprite/explosion2.png"),(150,150))
explosion3 = pygame.transform.scale(pygame.image.load("Data/Pictures/sprite/explosion3.png"),(150,150))
explosion4 = pygame.transform.scale(pygame.image.load("Data/Pictures/sprite/explosion4.png"),(150,150))
explosion5 = pygame.transform.scale(pygame.image.load("Data/Pictures/sprite/explosion5.png"),(150,150))
explosion6 = pygame.transform.scale(pygame.image.load("Data/Pictures/sprite/explosion6.png"),(150,150))
explosion7 = pygame.transform.scale(pygame.image.load("Data/Pictures/sprite/explosion7.png"),(150,150))
explosion8 = pygame.transform.scale(pygame.image.load("Data/Pictures/sprite/explosion8.png"),(150,150))


continuer = True
continuer_interface = True
espace_mode_mort = False
cpt_mort = 100

score = 0
	
x_Map = 0
y_Map = 0
cpt_tremblement = 15

taille_texte_niveau = 35
cpt_grossicement = 10

x_boutton_play = 1150
x_boutton_shop = 1150
x_boutton_quit = 1150
y_boutton_play = 520
y_boutton_shop = 620
y_boutton_quit = 720

class Etoile(pygame.sprite.Sprite):
	
	def __init__(self):
		self.x = random.randint(0,1400)
		self.y = random.randint(0,1000)
		self.xs = +50
		self.image = etoile_img
		if continuer_interface:
			self.image = etoile_img2
		pygame.sprite.Sprite.__init__(self)
		self.update()
	
	def update(self):
		self.rect = (int(self.x),int(self.y),5,5)
		self.x += self.xs

nb_etoile = []
para_etoile = Etoile()
nb_etoile.append(Etoile())


difficulter_max = 100
difficulter_min = 80
cpt_difficulter = 0
difficulter = 1
cpt_difficulter_tirs = 0
DIFFICULTER_TOTAL = 1

NB_LASER_PAR_TIRS = 1
MAX_ASTEROIDE = 4
NB_ASTEROIDE = 0
triche = False
MAX_ETOILE = random.randint(80,150)
nb_etoiles = 0
temps_etoile = random.randint(100,300)
etoile_detruite = []

arial3 = pygame.font.SysFont("arial",taille_texte_niveau)
continuer_grossir = True
continuer_retressir = False
cpt_retressir = 10
continuer_animation_text = False
cpt_animation = 200
continuer_animation_boutton = False
x_vaisseau_anim = 1000
y_vaisseau_anim = 150


def mort():
	global continuer
	global espace_mode_mort
	global cpt_mort
	continuer_mort = True
	
	police = pygame.font.SysFont("arial",200)
	arial2 = pygame.font.SysFont("arial",55)
	affiche = police.render("GAME OVER",True,white)
	affiche2 = arial2.render("PRESS RETURN TO RETRY",True,white)
	
	cpt_mort -= 1
	
	Map.blit(affiche,(70,200))
	Map.blit(affiche2,(300,450))
	espace_mode_mort = True



def rad2deg(a):
	return 180*a/pi-90
	

def rtd(x):
	return random.randint(1,x)
	

def tremblement():
	global x_Map
	global y_Map
	
	x_Map = random.randint(0,1)
	y_Map = random.randint(0,1)

def tremblement2():
	global x_Map
	global y_Map
	
	x_Map = random.randint(-10,10)
	y_Map = random.randint(-10,10)

class J1(pygame.sprite.Sprite):
	
	tourner_gauche = False
	tourner_droite = False
	cpt = 0
	MUNITION = 500
	
	def __init__(self):
		self.x, self.y = 0,500
		self.vx, self.vy = -15,0
		self.angle = 0
		self.tirs = []
		self.tourner_gauche = False
		self.tourner_droite = False
		
		pygame.sprite.Sprite.__init__(self)
		self.update()
	
	def update(self):
		self.x = (self.x + self.vx)%1400
		self.y = (self.y + self.vy)%1000
		
		if self.tourner_droite:
			self.image = pygame.transform.rotate(player1_droite,rad2deg(self.angle))
		if self.tourner_gauche:
			self.image = pygame.transform.rotate(player1_gauche,rad2deg(self.angle))
			
		if self.tourner_droite == False and self.tourner_gauche == False:
			self.image = pygame.transform.rotate(player1,rad2deg(self.angle))
		
		self.rect = (int(self.x),int(self.y),self.image.get_width(),self.image.get_height())
		self.mask = pygame.mask.from_surface(self.image)
		
		if self.vx > sMax:
			self.vx = sMax
		if self.vy > sMax:
			self.vy = sMax 
		
	def accelerer(self):
		self.vx -= ACCEL_VAISSEAU*cos(self.angle)
		self.vy += ACCEL_VAISSEAU*sin(self.angle)
	
	def reculer(self):
		self.vx += ACCEL_VAISSEAU*cos(self.angle)
		self.vy -= ACCEL_VAISSEAU*sin(self.angle)
	
	def ralentir(self):
		if self.vx < 0:
			self.vx += 0.03
		if self.vx > 0:
			self.vx -= 0.03
		if self.vy < 0:
			self.vy += 0.03
		if self.vy > 0:
			self.vy -= 0.03
		
	
	def tourner(self,direction):
		if direction == "gauche":
			self.angle += VANG_VESSEAU
			
		if direction == "droite":
			self.angle -= VANG_VESSEAU
	
	def tirer(self):
		self.cpt += 1
		tremblement()
		if self.cpt > VIT_TIRS:
			self.tirs.append(Laser(self))
			self.cpt = 0
			self.MUNITION -= 1
		
			
		
		


joueur = J1()

sxMax = 50
syMax = 50


class Explosion(pygame.sprite.Sprite):
	
	cpt = 0
	
	def __init__(self, group):
		self.x = joueur.x - 20
		self.y = joueur.y -20
		self.image = explosion1
		pygame.sprite.Sprite.__init__(self, group)
		self.update()
	
	def update(self):
		self.x = joueur.x - 20
		self.y = joueur.y - 20
		self.rect = (int(self.x),int(self.y),self.image.get_width(),self.image.get_height())
	
	def animation(self):
		self.cpt += 1
		if self.cpt == 4:
			self.image = explosion1
		if self.cpt == 8:
			self.image = explosion2
		if self.cpt == 12:
			self.image = explosion3
		if self.cpt == 15:
			self.image = explosion4
		if self.cpt == 18:
			self.image = explosion5
		if self.cpt == 21:
			self.image = explosion6
		if self.cpt == 24:
			self.image = explosion7
		if self.cpt == 27:
			self.image = explosion8

explosion = Explosion([])
grp_e = pygame.sprite.Group([explosion])

class Asteroide(pygame.sprite.Sprite):
	
	
	
	def __init__(self):
		self.x, self.y = 0,2
		self.vx = rtd(10)-5
		self.vy = rtd(10)-5
		self.angle = 0
		self.va = pi/80
		
		self.taille_x = random.random()+0.6
		self.taille_y = self.taille_x
		
		
		pygame.sprite.Sprite.__init__(self)
		self.update()
	
	def update(self):
		self.x = (self.x + self.vx)%1400
		self.y = (self.y + self.vy)%1000
		self.angle = (self.angle + self.va)
		
		#~ self.taille_x = random.randint(0,2)
		#~ self.taille_y = self.taille_x
		
		self.image = pygame.transform.rotozoom(asteoride,rad2deg(self.angle),self.taille_x)
		
		self.rect = (int(self.x),int(self.y),self.image.get_width(),self.image.get_height())
		self.mask = pygame.mask.from_surface(self.image)

asteroide = Asteroide()
asteroides = []



class Laser ( pygame.sprite.Sprite ):
	
	def __init__(self,tireur):
		self.x, self.y = tireur.x + 8, tireur.y-10
		self.vx = VIT_LASER*cos(tireur.angle)
		self.vy = VIT_LASER*sin(tireur.angle)
		
		pygame.sprite.Sprite.__init__(self)
		
		self.image = pygame.transform.rotate(laser, rad2deg(tireur.angle))
		self.mask = pygame.mask.from_surface(self.image)
		self.update()
	
	def update(self):
		self.x -= self.vx
		self.y += self.vy
		
		self.rect = (int(self.x),int(self.y),self.image.get_width(),self.image.get_height())

cpt_appa_aste = random.randint(20,100)

class Caisse_munition(pygame.sprite.Sprite):
	
	cpt_despawn_box_munition = 800
	cpt = 0
	
	def __init__(self):
		self.x = random.randint(0,1400)
		self.y = random.randint(0,1000)
		self.vx = random.randint(-1,1)
		self.vy = random.randint(-1,1)
		self.image = munition_box
		self.mask = pygame.mask.from_surface(self.image)
		pygame.sprite.Sprite.__init__(self)
		self.update()
		
	
	def update(self):
		self.x = (self.x + self.vx)%1400
		self.y = (self.y + self.vy)%1000
		self.rect = (int(self.x),int(self.y),self.image.get_width(),self.image.get_height())
	
	def animation_despawn(self):
		self.cpt += 1
		if self.cpt == 10:
			self.image = munition_box_despawn
		if self.cpt == 15:
			self.image = munition_box
			self.cpt = 0

tableau_box_munition = []
#~ tableau_box_munition.append(Caisse_munition())


cpt_spawn_box_munition = 1600

cpt_anim_vaisseau = 0
continuer_anim_vaisseau = True

police_tire_jeu = pygame.font.SysFont("",160)
Titre_jeu_blanc = police_tire_jeu.render("Space Games ",True,white)
Titre_jeu_noir = police_tire_jeu.render("Space Games ",True,black)
titre_x_change = 1
titre_y_change = -1
titre_x = 100
titre_y = 200
cpt_titre_x = 0
cpt_titre_y = 0

def animation_texte_difficulter():
	global cpt_grossicement
	global arial3
	global taille_texte_niveau
	global continuer_retressir
	global continuer_grossir
	global cpt_retressir
	global continuer_animation_text
	global level_up
	
	cpt_grossicement -= 1
	level_up.play()
	
	if cpt_grossicement == 100 or cpt_grossicement < 100 and cpt_grossicement > 1:
		if continuer_grossir:
			continuer_grossir = True
			continuer_retressir = False
			
	else:
		continuer_grossir = False
		cpt_grossicement = 0
	
	if cpt_grossicement < 1 and cpt_retressir > 0:
		cpt_retressir -= 1
		continuer_retressir = True
	
	if cpt_retressir < 11 and cpt_retressir > 0:
		if continuer_retressir:
			continuer_grossir = False
			continuer_retressir = True
	else:
		continuer_retressir = False
		continuer_animation_text = False
		continuer_grossir = True
		taille_texte_niveau = 35
		cpt_grossicement = 10
		cpt_retressir = 10
	
	if continuer_grossir:
		taille_texte_niveau += 1
	
	if continuer_retressir:
		taille_texte_niveau -= 1
		
		
	
		

def remise_a_zero():
	global son_reacteur
	global son_tire_laser
	global asteroides
	global cpt_appa_aste
	global difficulter_max
	global difficulter_min
	global cpt_difficulter
	global tableau_box_munition
	global VIT_LASER
	global cpt_difficulter_tirs
	global MAX_ASTEROIDE
	global NB_ASTEROIDE
	global NB_LASER_PAR_TIRS
	global VIT_TIRS
	global difficulter
	
	son_reacteur.stop()
	son_tire_laser.stop()
	#~ son_explosion2.play()
	asteroides = []
	explosion.animation()
	joueur.angle = 0
	tableau_box_munition = []
	cpt_appa_aste = 30
	difficulter_max = 100
	difficulter_min = 80
	cpt_difficulter = 0
	VIT_LASER = 10
	cpt_difficulter_tirs = 0
	MAX_ASTEROIDE = 4
	NB_ASTEROIDE = 0
	NB_LASER_PAR_TIRS = 1
	grp_e.draw(window)
	grp_e.draw(Map)
	mort()
	VIT_TIRS = 8
	for l in joueur.tirs:
		if lasers_perdus != []:
			joueur.tirs.remove(l)



def animation_boutton():
	global cpt_animation
	global speed_vaisseau
	global x_boutton
	global continuer_animation_boutton
	global continuer_interface
	global x_vaisseau_anim
	global y_vaisseau_anim
	global son_reacteur
	global x_Map
	global y_Map
	global taille_x_vaisseau
	global taille_y_vaisseau
	global vaisseau_anim1
	global vaisseau_anim2
	global vaisseau_anim3
	global vaisseau_anim4
	global titre_y
	global vaisseau_anim5
	
	
	cpt_animation -= 1
	stop_vaisseau = False
	
	if cpt_animation < 170:
		stop_vaisseau = True
		taille_x_vaisseau -= 1
		taille_y_vaisseau -= 1
	
	if cpt_animation > 1:
		if stop_vaisseau == False:
			x_vaisseau_anim -= 25
			y_vaisseau_anim += 5
		x_boutton += 30
		titre_y -= 10
		tremblement2()
	elif cpt_animation == 1:
		cpt_animation = 200
		continuer_animation_boutton = False
		continuer_interface = False
		x_boutton = 600
		x_vaisseau_anim = 1000
		titre_y = 200
		y_vaisseau_anim = 150
		x_Map = 0
		y_Map = 0
		para_etoile.xs = 0
		para_etoile.image = etoile_img
		speed_vaisseau.stop()
	
	#~ print(taille_x_vaisseau,taille_y_vaisseau)
	

def animation_boutton():
	global cpt_animation
	global speed_vaisseau
	global x_boutton_play
	global x_boutton_quit
	global x_boutton_shop
	global continuer_animation_boutton
	global continuer_interface
	global x_vaisseau_anim
	global y_vaisseau_anim
	global son_reacteur
	global x_Map
	global y_Map
	global taille_x_vaisseau
	global taille_y_vaisseau
	global vaisseau_anim1
	global vaisseau_anim2
	global vaisseau_anim3
	global vaisseau_anim4
	global vaisseau_anim5
	
	
	cpt_animation -= 1
	stop_vaisseau = False
	
	if cpt_animation < 170:
		stop_vaisseau = True
		taille_x_vaisseau -= 1
		taille_y_vaisseau -= 1
	
	if cpt_animation > 1:
		if stop_vaisseau == False:
			x_vaisseau_anim -= 25
			y_vaisseau_anim += 5
		x_boutton_play += 30
		x_boutton_shop += 30
		x_boutton_quit += 30
		tremblement2()
	elif cpt_animation == 1:
		cpt_animation = 200
		continuer_animation_boutton = False
		continuer_interface = False
		x_boutton = 600
		x_vaisseau_anim = 1000
		y_vaisseau_anim = 150
		x_Map = 0
		y_Map = 0
		para_etoile.xs = 0
		para_etoile.image = etoile_img
		speed_vaisseau.stop()


def reset():
	global son_reacteur
	global son_tire_laser
	global asteroides
	global cpt_appa_aste
	global difficulter_max
	global difficulter_min
	global taille_x_vaisseau
	global taille_y_vaisseau
	global cpt_difficulter
	global VIT_LASER
	global cpt_difficulter_tirs
	global MAX_ASTEROIDE
	global NB_ASTEROIDE
	global NB_LASER_PAR_TIRS
	global VIT_TIRS
	global difficulter
	global asteroides
	global VIT_LASER
	global cpt_mort
	global cpt_tremblement
	global triche
	global score
	global DIFFICULTER_TOTAL
	global difficulter
	global cpt_appa_aste
	global titre_y
	global titre_y_change
	
	
	
	taille_x_vaisseau = 300
	taille_y_vaisseau = 300
	VIT_LASER = 10
	titre_y = 200
	titre_y_change = -1
	cpt_mort = 100
	explosion.cpt = 0
	joueur.x = 700
	cpt_tremblement = 15
	triche = False
	joueur.y = 500
	score = 0
	joueur.vx = -20
	DIFFICULTER_TOTAL = 1
	difficulter = 1
	joueur.vy = 0
	cpt_appa_aste = random.randint(20,100)
	joueur.MUNITION = 500
	
	son_reacteur.stop()
	son_tire_laser.stop()
	#~ son_explosion2.play()
	asteroides = []
	joueur.angle = 0
	cpt_appa_aste = random.randint(20,100)
	difficulter_max = 100
	difficulter_min = 80
	cpt_difficulter = 0
	VIT_LASER = 10
	cpt_difficulter_tirs = 0
	MAX_ASTEROIDE = 4
	NB_ASTEROIDE = 0
	NB_LASER_PAR_TIRS = 1
	grp_e.draw(window)
	grp_e.draw(Map)
	VIT_TIRS = 8
	for l in joueur.tirs:
		if lasers_perdus != []:
			joueur.tirs.remove(l)
	

continuer_interface_shop = True


def interface_shop():
	global continuer_interface_shop
	global affiche_pas_terminer
	global Map
	global continuer_anim_vaisseau
	global cpt_anim_vaisseau
	
	img_vaisseau = vaisseau_anim1
	
	bleu_contour = pygame.Color(34,255,250)
	
	while continuer_interface_shop:
		
		if continuer_anim_vaisseau:
			cpt_anim_vaisseau += 1
			if cpt_anim_vaisseau == 7:
				img_vaisseau = vaisseau_anim1
			if cpt_anim_vaisseau == 14:
				img_vaisseau = vaisseau_anim2
			if cpt_anim_vaisseau == 21:
				img_vaisseau = vaisseau_anim3
			if cpt_anim_vaisseau == 28:
				img_vaisseau = vaisseau_anim4
			if cpt_anim_vaisseau == 35:
				img_vaisseau = vaisseau_anim5
				cpt_anim_vaisseau = 0
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		
		Map.fill(space_blue)
		for e in nb_etoile:
			e.update()
		for e in nb_etoile:
			if e.x > 1400:
				e.x -= 1400
		for e in nb_etoile:
			Map.blit(e.image,e.rect)
		
		Map.blit(img_vaisseau,(x_vaisseau_anim,300))
		pygame.draw.rect(Map,white,(100,250, 700, 700))
		pygame.draw.rect(Map,white,(100,50, 700, 150))
		pygame.draw.rect(Map,bleu_contour,(100,50, 10, 150))
		pygame.draw.rect(Map,bleu_contour,(800,50, 10, 150))
		pygame.draw.rect(Map,bleu_contour,(800,50, 10, 150))
		pygame.draw.rect(Map,bleu_contour,(100,50, 700, 10))
		pygame.draw.rect(Map,bleu_contour,(100,250, 700, 10))
		pygame.draw.rect(Map,bleu_contour,(100,950, 700, 10))
		pygame.draw.rect(Map,bleu_contour,(100,200, 710, 10))
		window.blit(Map,(0,0))
		pygame.display.update()
		clock.tick(100)

def interface():
	global window
	global continuer_interface
	global Map
	global space_blue
	global nb_etoile
	global nb_etoiles
	global MAX_ETOILE
	global continuer_animation_boutton
	global x_boutton_play
	global x_boutton_quit
	global x_vaisseau_anim
	global continuer_anim_vaisseau
	global cpt_anim_vaisseau
	global vaisseau_anim1
	global vaisseau_anim2
	global vaisseau_anim3
	global vaisseau_anim4
	global vaisseau_anim5
	global vaisseau_anim1
	global vaisseau_anim2
	global vaisseau_anim3
	global vaisseau_anim4
	global vaisseau_anim5
	global taille_x_vaisseau
	global y_boutton_play
	global y_boutton_quit
	global y_boutton_shop
	global x_boutton_shop
	global speed_vaisseau
	global taille_y_vaisseau
	global police_tire_jeu
	global Titre_jeu_blanc
	global Titre_jeu_noir
	global titre_x_change 
	global titre_x
	global titre_y
	global titre_y_change
	global cpt_titre_x
	global cpt_titre_y
	boutton_quitter2 = pygame.image.load("Data/Pictures/Bouttons/boutton_quitter_swagg.png")
	boutton_quitter = boutton_quitter2
	boutton_quitter_select = pygame.image.load("Data/Pictures/Bouttons/boutton_quitter_swagg_select.png")
	boutton_quitter_apuyer = pygame.image.load("Data/Pictures/Bouttons/boutton_quitter_apuyer.png")
	
	
	img_vaisseau = vaisseau_anim1
	
	boutton_play2 = pygame.image.load("Data/Pictures/Bouttons/boutton_play_swagg.png")
	boutton_play = boutton_play2
	boutton_play_apuyer = pygame.image.load("Data/Pictures/Bouttons/boutton_play_apuyer.png")
	boutton_play_select = pygame.image.load("Data/Pictures/Bouttons/boutton_play_swagg_select.png")
	
	boutton_anim_play = pygame.image.load("Data/Pictures/Bouttons/boutton_play_swagg.png")
	boutton_anim_play_select = pygame.image.load("Data/Pictures/Bouttons/boutton_play_swagg_select.png")
	
	boutton_shop_img = pygame.image.load("Data/Pictures/Bouttons/boutton_shop_swagg.png")
	boutton_shop_select = pygame.image.load("Data/Pictures/Bouttons/boutton_shop_swagg_select.png")
	boutton_shop = boutton_shop_img
	
	bloc_select_play = False
	bloc_select_quitter = False
	
	def button_shop(x,y):
		if x < 1400 and x > 1150:
			if y < 670 and y > 620:
				return True
		return False
	
	def button_shop_select(x,y):
		if x < 1400 and x > 1000:
			if y < 670 and y > 620:
				return True
		return False
	
	def button_play(x,y):
		if x < 1400 and x > 1150:
			if y < 570 and y > 520:
				return True
		return False
	
	def button_play_select(x,y):
		if x < 1400 and x > 1000:
			if y < 570 and y > 520:
				return True
		return False
	
	def button_quitter(x,y):
		if x < 1400 and x > 1150:
			if y < 770 and y > 720:
				return True
		return False
	
	def button_quitter_select(x,y):
		if x < 1400 and x > 1000:
			if y < 770 and y > 720:
				return True
		return False
	
	while continuer_interface:
		
		for e in nb_etoile:
			e.image = etoile_img2
			e.xs = 30
		
		if continuer_anim_vaisseau:
			cpt_anim_vaisseau += 1
			if cpt_anim_vaisseau == 7:
				img_vaisseau = vaisseau_anim1
			if cpt_anim_vaisseau == 14:
				img_vaisseau = vaisseau_anim2
			if cpt_anim_vaisseau == 21:
				img_vaisseau = vaisseau_anim3
			if cpt_anim_vaisseau == 28:
				img_vaisseau = vaisseau_anim4
			if cpt_anim_vaisseau == 35:
				img_vaisseau = vaisseau_anim5
				cpt_anim_vaisseau = 0
		
		if nb_etoiles < 50:
			nb_etoile.append(Etoile())
			nb_etoiles += 1
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					x,y = pygame.mouse.get_pos()
					
					if button_play(x,y):
						continuer_animation_boutton = True
						speed_vaisseau.play()
						continuer_anim_vaisseau = True
						joueur.x = 500
					
					if button_quitter(x,y):
						pygame.quit()
						sys.exit()
					
					if button_shop(x,y):
						interface_shop()
						
			
			elif event.type == MOUSEMOTION:
				
				x,y = pygame.mouse.get_pos()
				
				
				
				if boutton_play == boutton_play2:
					if button_play(x,y):
						if bloc_select_play == False:
							boutton_play = boutton_play_select
					else:
						if bloc_select_play == False:
							boutton_play = boutton_play2
				
				if boutton_play == boutton_play_select:
					if button_play_select(x,y):
						if bloc_select_play == False:
							boutton_play = boutton_play_select
					else:
						if bloc_select_play == False:
							boutton_play = boutton_play2
				
				if boutton_quitter == boutton_quitter2:
					if button_quitter(x,y):
						if bloc_select_quitter == False:
							boutton_quitter = boutton_quitter_select
					else:
						if bloc_select_quitter == False:
							boutton_quitter = boutton_quitter2
				
				if boutton_quitter == boutton_quitter_select:
					if button_quitter_select(x,y):
						if bloc_select_quitter == False:
							boutton_quitter = boutton_quitter_select
					else:
						if bloc_select_quitter == False:
							boutton_quitter = boutton_quitter2
				
				if boutton_shop == boutton_shop_img:
					if button_shop_select(x,y):
						boutton_shop = boutton_shop_select
					else:
						boutton_shop = boutton_shop_img
				
				if boutton_shop == boutton_shop_select:
					if button_shop_select(x,y):
						boutton_shop = boutton_shop_select
					else:
						boutton_shop = boutton_shop_img
		
		if continuer_animation_boutton:
			animation_boutton()
		else:
			joueur.x = 1400
		
		
		cpt_titre_x += 1
		cpt_titre_y += 1
		
		if titre_x_change == 1:
			if cpt_titre_x > 100:
				titre_x_change = -1
				cpt_titre_x = 0
		if titre_x_change == -1:
			if cpt_titre_x > 100:
				titre_x_change = 1
				cpt_titre_x = 0
		if titre_y_change == 1:
			if cpt_titre_y > 110:
				titre_y_change = -1
				cpt_titre_y = 0
		if titre_y_change == -1:
			if cpt_titre_y > 110:
				titre_y_change = 1
				cpt_titre_y = 0
		
		
		if continuer_animation_boutton:
			titre_y_change = 0
			titre_y -= 20
		
		titre_x += titre_x_change
		titre_y += titre_y_change
		
		Map.fill(space_blue)
		for e in nb_etoile:
			e.update()
		for e in nb_etoile:
			if e.x > 1400:
				e.x -= 1400
		for e in nb_etoile:
			Map.blit(e.image,e.rect)
		
		if continuer_animation_boutton == False:
			if boutton_play == boutton_play2:
				x_boutton_play = 1150
				y_boutton_play = 520
			if boutton_play == boutton_play_select:
				x_boutton_play = 900
				y_boutton_play = 500
			if boutton_quitter == boutton_quitter2:
				x_boutton_quit = 1150
				y_boutton_quit = 720
			if boutton_quitter == boutton_quitter_select:
				x_boutton_quit = 900
				y_boutton_quit = 700
			if boutton_shop == boutton_shop_img:
				x_boutton_shop = 1150
				y_boutton_shop = 620
			if boutton_shop == boutton_shop_select:
				x_boutton_shop = 900
				y_boutton_shop = 600
		
		Map.blit(boutton_play,(x_boutton_play,y_boutton_play))
		Map.blit(boutton_quitter,(x_boutton_quit,y_boutton_quit))
		Map.blit(boutton_shop,(x_boutton_shop,y_boutton_shop))
		Map.blit(Titre_jeu_noir,(titre_x-7,titre_y))
		Map.blit(Titre_jeu_blanc,(titre_x,titre_y))
		Map.blit(img_vaisseau,(x_vaisseau_anim,y_vaisseau_anim))
		#~ window.blit(vaisseau_anim,(x_vaisseau_anim,300))
		window.blit(Map,(x_Map,y_Map))
		pygame.display.update()
		joueur.update()
		clock.tick(70)
				
				
interface()






cpt_music = 7200
continuer_triche = False
cpt_triche = 50

tableau_box_munition.append(Caisse_munition())


while continuer:
	
	
	for c in tableau_box_munition:
		if c.vx == 0:
			c.vx = random.randint(-1,1)
		if c.vy == 0:
			c.vy = random.randint(-1,1)
	
	speed_vaisseau.stop()
	
	cpt_spawn_box_munition -= 1
	
	if cpt_spawn_box_munition == 0:
		tableau_box_munition.append(Caisse_munition())
		cpt_spawn_box_munition = 1600
	
	for c in tableau_box_munition:
		for l in joueur.tirs:
			if pygame.sprite.collide_mask(c,l) != None:
				joueur.tirs.remove(l)
				if c in tableau_box_munition:
					tableau_box_munition.remove(c)
			
	
	for c in tableau_box_munition:
		c.cpt_despawn_box_munition -= 1
		if c.cpt_despawn_box_munition < 200:
			c.animation_despawn()
		if c.cpt_despawn_box_munition == 0:
			tableau_box_munition.remove(c)
	
	if continuer_triche:
		cpt_triche -= 1
	
	if cpt_triche < 1:
		continuer_triche = False
		cpt_triche = 50
	
	for e in nb_etoile:
		e.image = etoile_img
		e.xs = 0
	
	cpt_music -= 1
	if cpt_music == 0:
		pygame.mixer.music.play()
		cpt_music = 8000
	
	temps_etoile -= 1
	
	arial3 = pygame.font.SysFont("arial",taille_texte_niveau)
	
	for e in nb_etoile:
		if temps_etoile < 5:
			nb_etoile.remove(e)
			temps_etoile = 50
			nb_etoiles -= 1
	if nb_etoiles < MAX_ETOILE:
		nb_etoile.append(Etoile())
		nb_etoiles += 1
	 
	 
	 
	cpt_difficulter += 1
	cpt_appa_aste -= 1
	cpt_difficulter_tirs += 1
	
	if DIFFICULTER_TOTAL < 8:
		if cpt_difficulter == 1500:
			level_up.play()
			cpt_difficulter = 0
			difficulter += 1
			joueur.MUNITION += 100
			continuer_animation_text = True
	
	if continuer_animation_text:
		animation_texte_difficulter()
   	 
	if difficulter == 1:
		if triche == False:
			VIT_TIRS = 10
			DIFFICULTER_TOTAL = 1
	if difficulter == 2:
		if triche == False:
			VIT_TIRS = 5
		DIFFICULTER_TOTAL = 2
		MAX_ASTEROIDE = 3
	if difficulter == 3:
		if triche == False:
			NB_LASER_PAR_TIRS = 1
			VIT_TIRS = 15
		MAX_ASTEROIDE = 5
		DIFFICULTER_TOTAL = 3
	if difficulter == 4:
		if triche == False:
			VIT_TIRS = 7
			NB_LASER_PAR_TIRS = 1
		DIFFICULTER_TOTAL = 4
	if difficulter == 5:
		if triche == False:
			VIT_TIRS = 10
			NB_LASER_PAR_TIRS = 0
			VIT_LASER = 5
		DIFFICULTER_TOTAL = 5
		MAX_ASTEROIDE = 8
	if difficulter == 6:
		if triche == False:
			VIT_LASER = 10
			NB_LASER_PAR_TIRS = 2
			VIT_TIRS = 15
		difficulter_max = 60
		DIFFICULTER_TOTAL = 6
		difficulter_min = 40
		MAX_ASTEROIDE = 10
	if difficulter == 7:
		if triche == False:
			VIT_LASER = 10
			VIT_TIRS = 10
		difficulter_max = 50
		difficulter_min = 30
		DIFFICULTER_TOTAL = 7
	if difficulter == 8:
		if triche == False:
			VIT_TIRS = 3
			NB_LASER_PAR_TIRS = 1
		difficulter_max = 50
		DIFFICULTER_TOTAL = 8
		difficulter_min = 30
		MAX_ASTEROIDE = 12

	if cpt_appa_aste < 1:
		if NB_ASTEROIDE < MAX_ASTEROIDE:
			asteroides.append(Asteroide())
			NB_ASTEROIDE += 1
		cpt_appa_aste = random.randint(difficulter_min,difficulter_max)
	
	if joueur.vx > sMax:
		joueur.vx = sMax
	if joueur.vx < sMax -18:
		joueur.vx = sMax -18
	
	if joueur.vy > sMax:
		joueur.vy = sMax
	if joueur.vy < sMax -16:
		joueur.vy = sMax -16
	
	appui = pygame.key.get_pressed()
	if appui[K_ESCAPE]:
		if espace_mode_mort == False:
			reset()
			continuer_interface = True
			for e in nb_etoile:
				e.image = etoile_img2
				nb_etoiles -= 1
				e.xs = 30
				nb_etoile.remove(e)
			interface()
	
	if appui[K_RIGHT]:
		joueur.tourner("droite")
		joueur.tourner_gauche = False
		joueur.tourner_droite = True
	
	if appui[K_LEFT]:
		joueur.tourner("gauche")
		joueur.tourner_gauche = True
		joueur.tourner_droite = False
	
	if appui[K_UP]:
		joueur.accelerer()
		x_Map = random.randint(-1,1)
		y_Map = random.randint(-1,1)
		son_reacteur.play()
	
	if appui[K_r]:
		joueur.ralentir()
	
	if appui[K_v] and appui[K_c]:
		joueur.vx = 0
		joueur.vy = 0
	
	if appui[K_KP4] and appui[K_KP5] and[K_KP6] and [K_KP8]:
		triche = True
		VIT_TIRS = 0
		joueur.MUNITION = 999
		
	if appui[K_KP0]:
		triche = False
	
	if appui[K_SPACE]:
		if espace_mode_mort == False:
			if joueur.MUNITION > 0:
				joueur.tirer()
				if difficulter > 2:
					if joueur.cpt > VIT_TIRS-NB_LASER_PAR_TIRS:
						joueur.tirs.append(Laser(joueur))
				son_tire_laser.play()
	
	
	
	if appui[K_BACKSPACE]:
		if espace_mode_mort:
			if cpt_mort < 1:
				espace_mode_mort = False
				VIT_LASER = 10
				cpt_mort = 100
				explosion.cpt = 0
				joueur.x = 700
				cpt_tremblement = 15
				triche = False
				joueur.y = 500
				score = 0
				joueur.vx = 0
				DIFFICULTER_TOTAL = 1
				difficulter = 1
				joueur.vy = 0
				cpt_appa_aste = 30
				joueur.MUNITION = 500
				pygame.mixer.music.play()
		
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_u:
				continuer_triche = True
			if event.key == K_i:
				if continuer_triche:
					joueur.MUNITION += 99999999
					continuer_triche = False
					cpt_triche = 50
			if event.key == K_KP3:
				joueur.MUNITION = 500
				continuer_triche = False
				cpt_triche = 50
		if event.type == KEYUP:
			if event.key == K_RIGHT or event.key == K_LEFT:
				joueur.tourner_droite = False
				joueur.tourner_gauche = False
			if event.key == K_SPACE:
				if espace_mode_mort == False:
					x_Map = 0
					y_Map = 0			
			if event.key == K_UP:
				son_reacteur.stop()
				x_Map = 0
				y_Map = 0
				
	
	window.fill(black)
	Map.fill(black)
	
	
	for e in nb_etoile:
		e.update()
	for e in nb_etoile:
		if e.x < 0:
			e.x += 1400
	for e in nb_etoile:
		Map.blit(e.image,e.rect)
	
	#~ if joueur.tourner_gauche:
		#~ joueur.image = player1_gauche
	#~ if joueur.tourner_droite:
		#~ joueur.image = player1_droite
	
	
	asteroides_detruits = []
	lasers_perdus = []
	etoile_detruite = []
	
	for l in joueur.tirs:
		for a in asteroides:
			if pygame.sprite.collide_mask(a,l) != None:
				score += 1
				asteroides_detruits.append(a)
				NB_ASTEROIDE -= 1
				lasers_perdus.append(l)
		if l.x < 0 or l.x > 1400 or l.y < 0 or l.y > 1000:
			lasers_perdus.append(l)
	
	for a in asteroides_detruits:
		if a in asteroides:
			asteroides.remove(a)
	for l in lasers_perdus:
		if l in joueur.tirs:
			joueur.tirs.remove(l)
	
	#~ if not asteroides:
		#~ print("Victoire")
		#~ pygame.quit()
		#~ sys.exit()
	
	if triche:
		joueur.MUNITION += 2
		score += 1
	
	if espace_mode_mort == False:
		Map.blit(joueur.image,joueur.rect)
	
	for c in tableau_box_munition:
		c.update()
	for c in tableau_box_munition:
		Map.blit(c.image,c.rect)
	
	for a in asteroides:
		a.update()
	for l in joueur.tirs:
		l.update()
	for a in asteroides:
		Map.blit(a.image,a.rect)
	for l in joueur.tirs:
		Map.blit(l.image,l.rect)
	
	
	if espace_mode_mort == False:
		explosion.update()
	joueur.update()
	
	for c in tableau_box_munition:
		if pygame.sprite.collide_mask(c,joueur) != None:
			joueur.MUNITION += 100
			son_caisse_munition.play()
			tableau_box_munition.remove(c)
	
	if triche == False:
		if espace_mode_mort == False:
			for a in asteroides:
				if  pygame.sprite.collide_mask(a,joueur) != None:
					pygame.mixer.music.stop()
					son_tire_laser.stop()
					son_reacteur.stop()
					son_explosion2.play()
					son_game_over.play()
					espace_mode_mort = True
					asteroides_detruits.append(a)
					for a in asteroides_detruits:
						if a in asteroides:
							asteroides.remove(a)
	
	
	if espace_mode_mort:
		remise_a_zero()
		
	
	
	arial4 = pygame.font.SysFont("arial",35)
	affiche3 = arial4.render("Score: "+str(score),True,white)
	affiche4 = arial4.render("x "+str(joueur.MUNITION),True,white)
	if DIFFICULTER_TOTAL < 8:
		affiche5 = arial3.render("Difficulty Level: "+str(DIFFICULTER_TOTAL),True,white)
	if DIFFICULTER_TOTAL == 8:
		affiche5 = arial3.render("Difficulty Level: Max",True,white)
	
	Map.blit(affiche3,(10,10))
	Map.blit(logo_munition,(10,50))
	Map.blit(affiche4,(80,70))
	Map.blit(affiche5,(500,10))
	if espace_mode_mort:
		if cpt_tremblement > 1:
			x_Map = random.randint(-20,50)
			y_Map = random.randint(-20,50)
			cpt_tremblement -= 1
		else:
			x_Map = 0
			y_Map = 0
			
	
	window.blit(Map,(x_Map,y_Map))
	pygame.display.update()
	clock.tick(70)

