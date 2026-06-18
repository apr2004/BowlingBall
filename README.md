# 🎳 Simulación de Lanzamientos de Bolas de Bolos

Este proyecto consiste en una simulación en 2D del lanzamiento de una bola de bolos. El objetivo principal es analizar el comportamiento dinámico del objeto, estudiando su transición desde el deslizamiento hasta alcanzar la rodadura pura. 

---

### 💻 Tecnologías Utilizadas
*   El lenguaje principal utilizado es Python.
*   La simulación física en 2D se implementa utilizando el motor PyMunk.
*   El renderizado visual en tiempo real y la interfaz gráfica se gestionan con PyGame.

---

### ⚙️ Estructura de las Simulaciones

El proyecto está dividido en el análisis de dos modelos distintos para comparar la teoría con la realidad física[cite: 3].

#### 1. Modelo Físico Ideal (`simulacion_ideal.py`)
Esta primera aproximación recrea el modelo teórico paso a paso mediante integración numérica.
*   Asume que la bola es una esfera sólida, rígida y de densidad perfectamente uniforme.
*   Considera que la superficie de la pista es completamente horizontal y que el coeficiente de fricción dinámica se mantiene constante en todo el trayecto.
*   Parte de la premisa de que la bola se lanza sin efecto, es decir, con una velocidad angular inicial nula ($\omega_{0} = 0$).
*   Desprecia la resistencia aerodinámica y la fricción por rodadura una vez alcanzado el estado de rodadura pura.
*   Demuestra empíricamente la fórmula teórica del tiempo necesario para alcanzar la rodadura pura: $t = \frac{2V_{0}}{7\mu_{d}g}$.
*   Verifica que la velocidad lineal final en el momento de la transición es siempre $v_{f} = \frac{5V_{0}}{7}$.

#### 2. Modelo Físico Realista (`simulacion_real.py`)
El modelo ideal es una simplificación, por lo que esta segunda simulación introduce variables empíricas complejas presentes en las pistas profesionales.
*   Ajusta el momento de inercia a $I_{real} \approx 0.35mR^{2}$ para simular la distribución asimétrica de la masa producida por el núcleo denso (core) de las bolas reales.
*   Implementa variaciones dinámicas en el coeficiente de fricción de la pista. 
*   Simula una zona inicial aceitada con un coeficiente extremadamente bajo ($\mu_{d} \approx 0.04$) donde la bola resbala conservando energía.
*   Simula una zona seca final con mayor fricción ($\mu_{d} = 0.2$) que fuerza la tracción y la rodadura.
*   Permite un lanzamiento inicial con giro impartido por el jugador, estableciendo una velocidad angular inicial mayor a cero ($\omega_{0} \ne 0$).
*   Aplica un coeficiente de resistencia a la rodadura ($\mu_{r} = 0.01$) que frena progresivamente la bola y su rotación una vez finalizado el deslizamiento.
