# -*- coding: utf-8 -*-

from Director import Director
from Functions import *
import pygame, sys
from pygame.locals import *
#import Personajes

HEIGHT = 768
WIDTH = 1024

class Scene:
    """Representa un escena abstracta del videojuego.
 
    Una escena es una parte visible del juego, como una pantalla
    de presentación o menú de opciones. Tiene que crear un objeto
    derivado de esta clase para crear una escena utilizable."""
 
    def __init__(self, director):
        self.director = director
 
    def on_update(self):
        "Actualización lógica que se llama automáticamente desde el director."
        raise NotImplemented("Tiene que implementar el método on_update.")
 
    def on_event(self, event):
        "Se llama cuando llega un evento especifico al bucle."
        raise NotImplemented("Tiene que implementar el método on_event.")
 
    def on_draw(self, screen):
        "Se llama cuando se quiere dibujar la pantalla."
        raise NotImplemented("Tiene que implementar el método on_draw.")



class SceneHome(Scene):
    """Escena inicial del juego, esta es la primera que se carga cuando inicia"""

    def __init__(self, director):
        Scene.__init__(self, director)

        #Altura: Segundo cuarto
        self.iniciar, self.iniciar_rect = texto('Seleccion de personajes', WIDTH/2, HEIGHT/2, 40)
        self.titulo, self.titulo_rect = texto('Titulo o imagen o yuqse', WIDTH/2, HEIGHT/4, 75, (255,255,255))

        self.flecha = load_image("assets/images/flecha.png")
        #self.flecha = pygame.transform.scale(self.flecha, (self.iniciar.get_width()/2,self.iniciar.get_height()/2+10))
        self.flecha_rect = self.flecha.get_rect()
        self.flecha_rect.centerx = WIDTH/2 - self.iniciar.get_width()/2 - 50
        self.flecha_rect.centery = HEIGHT/2

        #Carga la musica
        #pygame.mixer.music.load("assets/music/title_theme.mp3")
        #Pone la música a funcionar
        # loop = -1 -> Loop infinito
        #pygame.mixer.music.play(-1)

    def on_update(self, time):
        pass

    def on_event(self, time, event):
        #Al pulsar una tecla...
        keys = pygame.key.get_pressed()
        if pygame.KEYDOWN:
            if keys[K_RETURN]:
                scene = ScenePanel(self.director)
                self.director.change_scene(scene)

    def on_draw(self, screen):
        screen.fill((0,0,0))
        screen.blit(self.titulo, self.titulo_rect)
        screen.blit(self.flecha, self.flecha_rect)
        screen.blit(self.iniciar, self.iniciar_rect)

class ScenePanel(Scene):
       """Escena de selección de personajes"""

    def __init__(self, director):
        Scene.__init__(self, director)

        self.selected = 0
        self.charac1, self.charac2, self.prev1, self.prev2 = None
        self.select1, self.select2 = 0
        #Lista de objetos personajes (siendo cada posición un tipo de personaje)
        #self.panel = Personaje.getPanel()
        
        #El panel se sitúa en el medio de la pantalla y
        # a los lados la vista previa del pj

        #Altura: Segundo cuarto
        self.iniciar, self.iniciar_rect = texto('Seleccion de personajes', WIDTH/2, HEIGHT/2, 40)
        self.titulo, self.titulo_rect = texto('Titulo o imagen o yuqse', WIDTH/2, HEIGHT/4, 75, (255,255,255))

        self.flecha = load_image("assets/images/flecha.png")
        #self.flecha = pygame.transform.scale(self.flecha, (self.iniciar.get_width()/2,self.iniciar.get_height()/2+10))
        self.flecha_rect = self.flecha.get_rect()
        self.flecha_rect.centerx = WIDTH/2 - self.iniciar.get_width()/2 - 50
        self.flecha_rect.centery = HEIGHT/2

        #Carga la musica
        #pygame.mixer.music.load("assets/music/title_theme.mp3")
        #Pone la música a funcionar
        # loop = -1 -> Loop infinito
        #pygame.mixer.music.play(-1)

    def on_update(self, time):
        #O algo asi
        #self.prev1.idle()
        #self.prev2.idle()

    def on_event(self, time, event):
        #Al pulsar una tecla...
        keys = pygame.key.get_pressed()
        if pygame.KEYDOWN:
            if keys[K_RETURN] or keys[K_SPACE]:
                #Se selecciona atrás
                if self.selected == 0:
                    scene = SceneHome(self.director)
                    self.director.change_scene(scene)
                #Se selecciona luchar
                if self.selected == 2:
                    scene = SceneFight(self.director, self.charac1, self.charac2)
                    self.director.change_scene(scene)
                #Se selecciona un luchador
                if self.selected == 1:
                    if keys[K_RETURN]:
                        #Se guarda el pj seleccionado y se actualiza la vista previa
                        self.charac1 = self.panel[self.select1]
                        self.prev1 = self.panel[self.select1]
                    if keys[K_SPACE]:
                        #Se guarda el pj seleccionado y se actualiza la vista previa
                        self.charac2 = self.panel[self.select2]
                        self.prev2 = self.panel[self.select2]

    def on_draw(self, screen):
        screen.fill((0,0,0))

class SceneFight(Scene):
    pass