''' Simulación de una bola de bolos que empieza deslizando hasta alcanzar
la rodadura pura, comparando los resultados con la teoría.'''

import pymunk
import pymunk.pygame_util
import pygame
import sys

# --- PARÁMETROS FÍSICOS ---
MASA = 7.0
RADIO = 0.20
V_INICIAL = 6.5           
MU_D = 0.2
GRAVEDAD = 9.81

# Fórmulas teóricas del apartado 1
TIEMPO_TEORICO = (2 * V_INICIAL) / (7 * MU_D * GRAVEDAD)
VEL_FINAL_TEORICA = (5 * V_INICIAL) / 7

# Parámetros visuales
PIXELS_PER_METER = 100
FPS = 60
DT = (1.0 / FPS)*0.5

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 400))
    pygame.display.set_caption("Bolos: Deslizamiento a Rodadura")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)
    
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    space = pymunk.Space()
    space.gravity = (0, GRAVEDAD * PIXELS_PER_METER)

    # --- SUELO ---
    floor_y = 300
    floor = pymunk.Segment(space.static_body, (0, floor_y), (1000, floor_y), 3)
    floor.friction = MU_D
    space.add(floor)

    # --- BOLA ---
    radio_px = RADIO * PIXELS_PER_METER
    
    momento_inercia = (2/5) * MASA * (radio_px ** 2)
    bola = pymunk.Body(MASA, momento_inercia)
    bola.position = (50, floor_y - radio_px)
    bola.velocity = (V_INICIAL * PIXELS_PER_METER, 0)
    
    forma_bola = pymunk.Circle(bola, radio_px)
    
    forma_bola.friction = 1.0 
    space.add(bola, forma_bola)

    # --- VARIABLES DE CONTROL ---
    tiempo = 0.0
    rodadura_pura = False
    t_rodadura = 0.0
    v_rodadura = 0.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if bola.position.x < 950:
            space.step(DT)
            tiempo += DT

        v_lineal = bola.velocity.x / PIXELS_PER_METER
        w_angular = abs(bola.angular_velocity)
        v_rotacion = w_angular * RADIO

        # Condición de rodadura pura: Vcm = W*R
        diferencia = abs(v_lineal - v_rotacion)
        
        if not rodadura_pura and diferencia < 0.05 and tiempo > 0.05:
            rodadura_pura = True
            t_rodadura = tiempo
            v_rodadura = v_lineal

        # --- RENDERIZADO ---
        screen.fill((240, 240, 240))
        
        # Dibujamos todo el espacio automáticamente
        space.debug_draw(draw_options)

        # Textos informativos
        estado = "RODADURA PURA" if rodadura_pura else "DESLIZANDO"
        color_estado = (0, 150, 0) if rodadura_pura else (200, 0, 0)
        
        screen.blit(font.render(f"Estado: {estado}", True, color_estado), (20, 20))
        screen.blit(font.render(f"Tiempo: {tiempo:.3f} s", True, (0, 0, 0)), (20, 45))
        screen.blit(font.render(f"V. Lineal: {v_lineal:.3f} m/s", True, (0, 0, 0)), (20, 70))
        screen.blit(font.render(f"V. Rotación (w*R): {v_rotacion:.3f} m/s", True, (0, 0, 0)), (20, 95))
        
        if rodadura_pura:
            screen.blit(font.render(f"Tiempo Simulado: {t_rodadura:.3f} s (Teoría: {TIEMPO_TEORICO:.3f} s)", True, (0, 100, 0)), (450, 20))
            screen.blit(font.render(f"V. Simulada: {v_rodadura:.3f} m/s (Teoría: {VEL_FINAL_TEORICA:.3f} m/s)", True, (0, 100, 0)), (450, 45))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()