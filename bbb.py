from random import random
import random as rd
import pyautogui
import classify
import pymouse
import numpy
import time
import PIL
import os

x = 865  # x do [ ] no captcha do participante
y = 780  # y do participante
yc = 790 # y do [ ] no captcha do participante
yr = 400 # y do botão de votar novamente

captcha_pos = (900, 600)   # (x, y) do primeiro pixel do 1º bloco do captcha
captcha_block = (962, 657) # (x, y) do centro do 1º bloco do captcha
next_button = (1217, 1041) # (x, y) do botão de confirmar captcha

pixelPos = (1015, 524)      # (x, y) de um pixel com 3 RGBs diferentes (bike, barco, outro/nenhum): exemplo pixel aleatório da letra b de barco no hCaptcha
bicicleta = (200, 228, 231) # RGB do pixel no captcha qnd aparece p escolher bicicleta
barco = (0, 131, 143)       # RGB do pixel no captcha qnd aparece p escolher barco

mouse = pymouse.PyMouse()
keepImages = False # ligue caso queira salvar imagens aleatórias do captcha para o ./runtime/ (classificar manualmente em ./data/)
				   # Após a classificação, definir `train` como = True em classify.py para treinar o modelo

# log pos. mouse
# print(mouse.position())

# Não alterar - Constante
s = 380 # tamanho do captcha (só os 9 blocos)
m = 10  # margem entre os blocos

time.sleep(1)

def scrollDownWait():
	timeout = 1.1 + random()
	time.sleep(timeout/2)
	pyautogui.scroll(-20)
	time.sleep(timeout/2)

def captchaType():
	s = pyautogui.screenshot()
	pixel = s.getpixel(pixelPos) # posição onde pixel pode ser 3 cores diferentes (bike, barco, nada)
	# log cor pixel
	# print(pixel)
	if pixel == bicicleta: return 'bicicleta'
	elif pixel == barco: return 'barco'
	else: return False

def captchaSolve(solve_for):
	for y in range(3):
		for x in range(3):
			crop_s = int( (s - m*2)/3 )
			crop_x = int( x*m + x*crop_s )
			crop_y = int( y*m + y*crop_s )
			im = pyautogui.screenshot(region=(captcha_pos[0], captcha_pos[1], s, s))
			sl = im.crop([crop_x, crop_y, crop_x+crop_s, crop_y+crop_s]) # slice em cada bloco do captcha
			hash = rd.getrandbits(128)
			file = './runtime/%032x.jpg' % hash
			sl.save(file)
			classified = classify(file) # classificar bloco pela rede neural
			if not keepImages: os.remove(file)

			if solve_for == classified[0]:
				o = (int) (random()*80-40) # rnd offset
				block_x = captcha_block[0] + crop_x + o
				block_y = captcha_block[1] + crop_y + o
				mouse.click(block_x, block_y) # clica no bloco
				time.sleep(random())
	mouse.click(next_button[0], next_button[1]) # clica pra terminar


# Main
votos = 0
while True:
	votos += 1
	print('votos: ' + str(votos))
	o = (int) (random()*26-13) # rnd offset
	scrollDownWait()

	mouse.click(x+o, y+o) # clica candidato
	scrollDownWait()

	mouse.click(x+o, yc+o) # clica captcha
	scrollDownWait()

	c_type = captchaType()
	while c_type is not False:
		captchaSolve(c_type)
		time.sleep(1+random()*2)
		c_type = captchaType()

	scrollDownWait()
	mouse.click(x+o, yr) # clica votar novamente