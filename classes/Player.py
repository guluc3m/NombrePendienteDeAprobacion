# -*- coding: utf-8 -*-

from pygame import sprite
from Functions import *

class Player(sprite.Sprite):
	"""Representa cada personaje del juego durante la partida.

	El objeto Player contiene todos los datos comunes a todos
	los personajes y que se inicializan según el personaje
	escogido, como la vida, la lista de animaciones o el banco
	de sonidos.

	Este objeto se debe inicializar después de terminar la
	selección de personajes con los datos del personaje escogido."""

	def __init__(self, jsonObject):
		sprite.Sprite.__init__(self)
		self.name = jsonObject['nombre']
		self.sprites = self.load_sprites(jsonObject['sprites'], 200, 420)
		self.avatar = load_image(jsonObject['avatar'], False)
		self.state = "idle"
		self.health = 100
		# Hacia donde mira (0 -> derecha, 4 -> izquierda)
		self.current_hframe = 0 # Lo necesitaremos para hacer el ciclo de animación
		self.orientacion = 0
		self.x = 75
		self.y = 250
		self.vulnerable = True
		self.golpeando = False
		# Tanto el salto como cualquier acción dura varias iteraciones, por lo que se debe de tener en cuenta
		# para mantener el flujo correctamente y evitar solapamiento.
		self.cdSalto = 0
		self.cdAction = 0

	# Actions

	def avanzar(self):
		"""El avance del personaje está definido por su orientación y límitado por su posición o estado.
		No podrá salirse de los límites del escenario.
		No podrá avanzar si está ejecutando otra acción que no sea salto.
		"""

		self.state = "avanzar"
		self.vulnerable = True
		if self.orientacion == 0: # Avanzamos hacia la derecha
			if self.x <= 800: # No estamos en los límites del escenario
				self.x += 25
		else:
			if self.x >= 25: # No estamos en los límites del escenario
				self.x -= 25

	def defender(self):
		"""Durante la defensa el personaje será invulnerable a cualquier ataque y además avanzará hacia atrás.
		No podrá salirse de los límites del escenario.
		No podrá avanzar si está ejecutando otra acción que no sea salto.		
		"""
		
		self.state = "defender"
		self.vulnerable = False
		if self.orientacion == 0: # Avanzamos hacia la derecha
			if self.x >= 25: # No estamos en los límites del escenario
				self.x -= 25
		else:
			if self.x <= 800: # No estamos en los límites del escenario
				self.x += 25

	def defenderSalto(self):
		"""El personaje podrá saltar hacia atrás manteniendo su defensa.
		No podrá salirse de los límites del escenario.
		Estará saltando.
		Sólo mantendrá su defensa si se desplaza hacia atrás durante el salto.
		"""
		self.state = "defenderSalto"
		self.vulnerable = False


	def ataqueDebil(self):
		"""El ataque débil se caracteriza por ser más flojo pero más rápido. Esto en nuestro juego se traduce
		en que el daño será menor pero la cd del golpe también.
		Durante el ataque no se podrá efectuar ninguna acción.
		"""

		self.state = "ataqueDebil"
		self.vulnerable = True
		self.golpeando = True
		self.cdAction = 10

	def ataqueFuerte(self):
		"""El ataque fuerte se caracteriza por inflingir mayor daño pero requerir más tiempo de ejecución.
		Durante el ataque no se podrá efectuar ninguna acción.
		"""

		self.state = "ataqueFuerte"
		self.vulnerable = True
		self.golpeando = True
		self.cdAction = 20

	def saltar(self):
		"""El personaje podrá saltar, la altura del salto viene determinada por la altura de los personajes,
		todos los personajes deben poder saltar 1,3 veces su altura, de forma que sea posible superar al
		otro personaje y caer en el lado opuesto del escenario, obligando a cambiar la orientación de los
		sprites.
		Mientras se está en el aire las maniobras son reducidas, por lo que durante esta acción la función
		actualizar devuelve un entero que representa la duración del salto. Mientras este número sea positivo,
		el personaje estará en el aire, pudiendo sólo realizar las acciones "defenderSalto", "avanzarSalto"
		y "pegarSalto".
		Cuando el valor devuelto sea 0, el personaje habrá vuelto al suelo y en la función principal se
		recalculará la orientación de ambos personajes ya que existe la posibilidad de que hayan cambiado
		su ubicación relativa en el escenario.
		Durante un salto la dirección de avanzar o retroceder (orientación) será la misma hasta que el
		personaje termine el salto.
		El movimiento vertical descrito utiliza la fórmula del MRUA (Falta definir la altitud del salto y
		la duración para poder definir la función)
		"""

		self.state = "saltar"
		self.vulnerable = True
		self.cdSalto = 1 # Hay que apañar la formula de movimiento en salto
	def pegarSalto(self):
		""""""

	def golpeBajo(self):
		""""""

	def getHurt(self, dmg):
		""""""

		self.health -= dmg
		if self.health < 1:
			self.health = 0
			return 0	# El personaje ha sido debilitado
		else:
			return 1	# El personaje sigue vivo

	def update(self):
		# Actualizamos frames
		self.current_hframe += 1
		if self.current_hframe == 4:
			self.current_hframe = 0

		# Actualizamos posición si estamos en un salto
#		self.cdSalto = ActualizarSaltoYALOHARÉ()
		return self.cdSalto	

	def load_sprites(self, filename, width, height):
		"""Los sprites de los personajes se cargan desde una imagen donde están todos contenidos y
		después se genera una lista de listas ordenada con cada imagen de la animación"""

		# En una primera instancia vamos a definir que cada frame tiene 420 de alto y 200 de ancho

		ficha = {}

		sprite_ficha = load_image(filename)
		#Descomentar la siguiente linea para probar
		#sprite_ficha = load_image("assets/images/sprites/Sprite_chachiWachi_ficha.png")
		framePorLinea = 8
		ficha["idle"] = []
		ficha["avanzar"] = []
		ficha["defender"] = []
		ficha["defenderSalto"] = []
		ficha["ataqueDebil"] = []
		ficha["ataqueFuerte"] = []
		ficha["saltar"] = []
		ficha["pegarSalto"] = []
		ficha["golpeBajo"] = []
		ficha["recibir"] = []
		ficha["Morir"] = []
		for i in range(framePorLinea):
			ficha["idle"].append(sprite_ficha.subsurface((i*200, height*0, width, height)))
			ficha["avanzar"].append(sprite_ficha.subsurface((i*200, height*1, width, height)))
			ficha["defender"].append(sprite_ficha.subsurface((i*200, height*2, width, height)))
			ficha["defenderSalto"].append(sprite_ficha.subsurface((i*200, height*3, width, height)))
			ficha["ataqueDebil"].append(sprite_ficha.subsurface((i*200, height*4, width, height)))
			ficha["ataqueFuerte"].append(sprite_ficha.subsurface((i*200, height*5, width, height)))
			ficha["saltar"].append(sprite_ficha.subsurface((i*200, height*6, width, height)))
			ficha["pegarSalto"].append(sprite_ficha.subsurface((i*200, height*7, width, height)))
			ficha["golpeBajo"].append(sprite_ficha.subsurface((i*200, height*8, width, height)))
			ficha["recibir"].append(sprite_ficha.subsurface((i*200, height*9, width, height)))
			ficha["Morir"].append(sprite_ficha.subsurface((i*200, height*10, width, height)))

		return ficha

