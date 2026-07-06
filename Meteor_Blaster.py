import pygame
import random
import math

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ANCHO = 900
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Meteor Blaster")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AMARILLO = (255, 255, 0)
# Add after the initial variables section
# Estrellas
estrellas = []
for _ in range(50):  # Create 50 stars
    x = random.randint(0, ANCHO)
    y = random.randint(0, ALTO)
    estrellas.append([x, y])

def dibujar_estrellas():
    fuente = pygame.font.Font(None, 8)  # Small font size for stars
    for estrella in estrellas:
        texto = fuente.render(".", True, BLANCO)
        pantalla.blit(texto, (estrella[0], estrella[1]))

# Jugador (nave espacial)
jugador_pos = [ANCHO // 2, ALTO - 50]
jugador_velocidad = 5.5

# Disparos
disparos = []
disparo_velocidad = 7

# Meteoros
meteoros = []
meteoro_velocidad = 1.5

# Puntuación y vidas
puntuacion = 0
vidas = 3
high_score = 0

# After pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("Meteor_Rush.mp3")
pygame.mixer.music.play(-1)  # -1 means loop indefinitely

# Add this color after the other color definitions
AZUL_CIELO = (135, 206, 235)

def dibujar_jugador():
    # Dibujar borde azul cielo
    pygame.draw.polygon(pantalla, AZUL_CIELO, [
        (jugador_pos[0], jugador_pos[1] - 22),
        (jugador_pos[0] - 17, jugador_pos[1] + 12),
        (jugador_pos[0] + 17, jugador_pos[1] + 12)
    ])
    # Dibujar triángulo principal
    pygame.draw.polygon(pantalla, BLANCO, [
        (jugador_pos[0], jugador_pos[1] - 20),
        (jugador_pos[0] - 15, jugador_pos[1] + 10),
        (jugador_pos[0] + 15, jugador_pos[1] + 10)
    ])

def dibujar_meteoros():
    for meteoro in meteoros:
        # Dibujar borde rojo
        pygame.draw.circle(pantalla, ROJO, (int(meteoro[0]), int(meteoro[1])), 22)
        # Dibujar círculo principal
        pygame.draw.circle(pantalla, AMARILLO, (int(meteoro[0]), int(meteoro[1])), 20)

def crear_meteoro():
    # Generar un meteoro dentro de un rango más centrado
    x = random.randint(150, ANCHO - 150)  # Limitar el rango para que no aparezcan cerca de los bordes
    meteoros.append([x, -20])  # Se genera un meteoro a una altura inicial fuera de la pantalla

# En el bucle principal, ajustamos la probabilidad de generar meteoros:
if random.random() < 0.01:  # Reducimos la probabilidad de generación de meteoros
    crear_meteoro()
def dibujar_disparos():
    for disparo in disparos:
        pygame.draw.rect(pantalla, ROJO, (int(disparo[0] - 2), int(disparo[1] - 10), 4, 10))

def mostrar_puntuacion():
    fuente = pygame.font.Font(None, 36)
    texto = fuente.render(f"Puntuación: {puntuacion} Vidas: {vidas}", True, BLANCO)
    pantalla.blit(texto, (10, 10))

def game_over():
    fuente = pygame.font.Font(None, 74)
    texto_game_over = fuente.render("GAME OVER", True, BLANCO)
    texto_score = fuente.render(f"High Score: {high_score}", True, BLANCO)
    texto_continuar = fuente.render("Presiona Y para Reintentar", True, BLANCO)
    texto_salir = fuente.render("N para salir", True, BLANCO)
    
    # Mostrar los textos centrados y alineados verticalmente
    pantalla.blit(texto_game_over, (ANCHO//2 - texto_game_over.get_width()//2, ALTO//2 - 100))
    pantalla.blit(texto_score, (ANCHO//2 - texto_score.get_width()//2, ALTO//2))
    pantalla.blit(texto_continuar, (ANCHO//2 - texto_continuar.get_width()//2, ALTO//2 + 50))
    pantalla.blit(texto_salir, (ANCHO//2 - texto_salir.get_width()//2, ALTO//2 + 120))

def reiniciar_juego():
    global puntuacion, vidas, meteoros, disparos, jugador_pos
    puntuacion = 0
    vidas = 3
    meteoros = []
    disparos = []
    jugador_pos = [ANCHO // 2, ALTO - 50]
    pygame.mixer.music.play(-1)  # Restart music when game restarts

# Bucle principal del juego
jugando = True
reloj = pygame.time.Clock()

while jugando:
    disparo_sonido = pygame.mixer.Sound("Blast.mp3")
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                disparos.append([jugador_pos[0], jugador_pos[1]])
                disparo_sonido.play()  # Play shooting sound
            elif vidas <= 0:
                if evento.key == pygame.K_y:
                    reiniciar_juego()
                elif evento.key == pygame.K_n:
                    jugando = False

    if vidas > 0:
        # Movimiento del jugador
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jugador_pos[0] > 15:
            jugador_pos[0] -= jugador_velocidad
        if teclas[pygame.K_RIGHT] and jugador_pos[0] < ANCHO - 15:
            jugador_pos[0] += jugador_velocidad

        # Crear meteoros
        if random.random() < 0.02:
            crear_meteoro()

        # Actualizar posición de meteoros
        for meteoro in meteoros[:]:
            meteoro[1] += meteoro_velocidad
            if meteoro[1] > ALTO:
                meteoros.remove(meteoro)
                vidas -= 1

        # Actualizar posición de disparos
        for disparo in disparos[:]:
            disparo[1] -= disparo_velocidad
            if disparo[1] < 0:
                disparos.remove(disparo)

        # Detectar colisiones
        for disparo in disparos[:]:
            for meteoro in meteoros[:]:
                distancia = math.sqrt((disparo[0] - meteoro[0])**2 + (disparo[1] - meteoro[1])**2)
                if distancia < 20:
                    if disparo in disparos:
                        disparos.remove(disparo)
                    if meteoro in meteoros:
                        meteoros.remove(meteoro)
                    puntuacion += 10

        # Actualizar high score
        if puntuacion > high_score:
            high_score = puntuacion

        # Dibujar todo
        pantalla.fill(NEGRO)
        dibujar_estrellas()  # Add this line before drawing other elements
        dibujar_jugador()
        dibujar_meteoros()
        dibujar_disparos()
        mostrar_puntuacion()
    else:
        pantalla.fill(NEGRO)
        dibujar_estrellas()  # Add this line here too for game over screen
        game_over()
        pygame.mixer.music.stop()  # Stop music when game is over

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
