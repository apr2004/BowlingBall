''' Simulación Realista de Bolos
Incluye zonas de fricción variable (aceite y seco), momento de inercia de núcleo asimétrico,
giro inicial impartido por el jugador y rozamiento por rodadura.'''

import pymunk
import pymunk.pygame_util
import pygame
import sys

# --- PARÁMETROS FÍSICOS ---
MASA = 7.0         
RADIO = 0.20      
V0 = 6.5           # Vel. lineal inicial impartida (m/s)
W0 = 10.0          # Vel. angular inicial (rad/s) simulando el giro del jugador
GRAVEDAD = 9.81

# Zonas de fricción
MU_ACEITE = 0.04   
MU_SECA = 0.2     
MU_RODADURA = 0.01 

# Visualización
PIXELS_PER_METER = 50 
FPS = 60
DT = 1.0 / FPS
ANCHO = 1000
ALTO = 400

def setup_simulation():
    space = pymunk.Space()
    space.gravity = (0, GRAVEDAD * PIXELS_PER_METER)

    floor_y = 300
    zona_aceite_px = 12 * PIXELS_PER_METER
    
    # --- PISTA ---
    floor = pymunk.Segment(space.static_body, (0, floor_y), (ANCHO + 100, floor_y), 3)
    floor.friction = MU_ACEITE # Empieza con la fricción del aceite
    space.add(floor)

    # --- BOLA (CENTRO ASIMÉTRICO) ---
    radio_px = RADIO * PIXELS_PER_METER
    momento_inercia = 0.35 * MASA * (radio_px ** 2)
    bola = pymunk.Body(MASA, momento_inercia)
    
    bola.position = (20, floor_y - (RADIO * PIXELS_PER_METER))
    bola.velocity = (V0 * PIXELS_PER_METER, 0)
    bola.angular_velocity = W0 
    
    forma_bola = pymunk.Circle(bola, RADIO * PIXELS_PER_METER)
    forma_bola.friction = 1.0 
    space.add(bola, forma_bola)

    return space, bola, floor, zona_aceite_px, momento_inercia

def main():
    pygame.init()
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Bolos: Simulación Realista")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)
    font_bold = pygame.font.SysFont("Arial", 16, bold=True)
    
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    space, bola, floor, zona_aceite_px, momento_inercia = setup_simulation()

    tiempo = 0.0
    rodadura_pura = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if bola.position.x < ANCHO:
            space.step(DT)
            tiempo += DT

        # --- CAMBIO DINÁMICO DE FRICCIÓN ---
        if bola.position.x >= zona_aceite_px:
            floor.friction = MU_SECA
        else:
            floor.friction = MU_ACEITE

        v_lineal = bola.velocity.x / PIXELS_PER_METER
        w_angular = abs(bola.angular_velocity)
        v_rotacion = w_angular * RADIO

        # Comprobación de rodadura pura
        diferencia = abs(v_lineal - v_rotacion)
        
        if diferencia < 0.1 and tiempo > 0.1:
            rodadura_pura = True
            
            # Fricción por rodadura: debe frenar tanto la traslación como la rotación
            f_rodadura = MU_RODADURA * MASA * GRAVEDAD * PIXELS_PER_METER
            bola.apply_force_at_world_point((-f_rodadura, 0), bola.position)
            
            # Calculamos el torque necesario para frenar la rotación y mantener v = w*R
            # Fórmula teórica: Torque = I * (aceleracion_lineal / radio)
            aceleracion_lineal = f_rodadura / MASA
            aceleracion_angular = aceleracion_lineal / (RADIO * PIXELS_PER_METER)
            torque_frenado = momento_inercia * aceleracion_angular
            
            # Aplicamos el torque en sentido contrario al giro
            direccion_giro = 1 if bola.angular_velocity > 0 else -1
            bola.torque = -torque_frenado * direccion_giro
        else:
            rodadura_pura = False

        # --- RENDERIZADO ---
        screen.fill((240, 240, 240)) # Fondo unificado más claro
        
        # Pymunk dibuja la bola y los segmentos del suelo automáticamente
        space.debug_draw(draw_options)

        # Textos e interfaz
        estado_txt = "RODANDO" if rodadura_pura else "DESLIZANDO"
        color_estado = (0, 150, 0) if rodadura_pura else (200, 0, 0)
        
        zona_actual = "ACEITADA (Baja Fricción)" if bola.position.x < zona_aceite_px else "SECA (Alta Fricción)"
        color_zona = (0, 100, 200) if bola.position.x < zona_aceite_px else (200, 100, 0)

        # Información en pantalla
        screen.blit(font_bold.render(f"Estado: {estado_txt}", True, color_estado), (20, 20))
        screen.blit(font_bold.render(f"Zona Pista: {zona_actual}", True, color_zona), (20, 45))
        
        screen.blit(font.render(f"Tiempo: {tiempo:.3f} s", True, (0, 0, 0)), (20, 75))
        screen.blit(font.render(f"V. Lineal: {v_lineal:.2f} m/s", True, (0, 0, 0)), (20, 95))
        screen.blit(font.render(f"V. Rotación (w*R): {v_rotacion:.2f} m/s", True, (0, 0, 0)), (20, 115))
        screen.blit(font.render(f"Giro actual (w): {w_angular:.2f} rad/s", True, (0, 0, 0)), (20, 135))

        # Indicador visual simple en la parte inferior para marcar el cambio de zona
        pygame.draw.rect(screen, (0, 100, 200), (0, ALTO - 10, zona_aceite_px, 10))
        pygame.draw.rect(screen, (200, 100, 0), (zona_aceite_px, ALTO - 10, ANCHO - zona_aceite_px, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()