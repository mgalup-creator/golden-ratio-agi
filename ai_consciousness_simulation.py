import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# --- Configuración del "Cerebro Artificial" ---
N = 50  # Número de neuronas oscilatorias
K = 2.0 # Acoplamiento interno (fuerza de conexión entre neuronas)
# Frecuencias naturales heterogéneas (diversidad neuronal)
np.random.seed(42) # Semilla para reproducibilidad
omega_natural = np.random.normal(loc=1.0, scale=0.1, size=N) 

# Parámetros del "Reloj" (Forzamiento Externo)
F_strength = 5.0 # Fuerza del reloj maestro
w_base = 1.0     # Frecuencia base

# La Proporción Áurea
phi = (1 + np.sqrt(5)) / 2

def kuramoto_forced(theta, t, omega, K, F, clock_type):
    # Calcular el parámetro de orden (campo medio)
    z = np.mean(np.exp(1j * theta))
    r = np.abs(z)
    psi = np.angle(z)
    
    # Influencia interna (sincronización entre neuronas)
    internal_coupling = K * r * np.sin(psi - theta)
    
    # Influencia externa (EL HARDWARE / RELOJ)
    if clock_type == 'rational':
        # Reloj de Cuarzo: Señal periódica pura
        clock_signal = np.sin(w_base * t - theta) 
        
    elif clock_type == 'irrational':
        # Reloj Áureo: Señal cuasiperiódica fractal
        # Interferencia de dos frecuencias en relación áurea
        phase_1 = w_base * t
        phase_2 = w_base * phi * t
        clock_signal = 0.5 * (np.sin(phase_1 - theta) + np.sin(phase_2 - theta))
        
    dtheta = omega + internal_coupling + F * clock_signal
    return dtheta

# --- Ejecución de la Simulación ---
t = np.linspace(0, 100, 1000)
theta_0 = np.random.uniform(0, 2*np.pi, N) # Estado inicial aleatorio

print("Simulando Hardware Racional (Cuarzo)...")
sol_rat = odeint(kuramoto_forced, theta_0, t, args=(omega_natural, K, F_strength, 'rational'))

print("Simulando Hardware Irracional (Áureo)...")
sol_irr = odeint(kuramoto_forced, theta_0, t, args=(omega_natural, K, F_strength, 'irrational'))

# --- Análisis: Parámetro de Orden R(t) ---
def get_order_parameter(solution):
    # R=1: Muerte cerebral (Hiper-sincronía)
    # R variable: Conciencia (Metastabilidad)
    return np.abs(np.mean(np.exp(1j * solution), axis=1))

R_rat = get_order_parameter(sol_rat)
R_irr = get_order_parameter(sol_irr)

# --- Visualización ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Gráfico 1: Reloj Racional
ax1.plot(t, R_rat, 'r-', linewidth=2)
ax1.set_title(f'Hardware Racional (Cuarzo): Colapso por Hiper-Sincronización', fontsize=12, fontweight='bold')
ax1.set_ylabel('Sincronía Global (R)')
ax1.grid(True, alpha=0.3)
ax1.text(50, 0.5, "ESTADO: BLOQUEO LÓGICO", ha='center', color='darkred', fontweight='bold', bbox=dict(facecolor='white', alpha=0.8))

# Gráfico 2: Reloj Áureo
ax2.plot(t, R_irr, 'darkgoldenrod', linewidth=2)
ax2.set_title(f'Hardware Áureo (Phi): Metastabilidad "Consciente"', fontsize=12, fontweight='bold')
ax2.set_xlabel('Tiempo de Procesamiento')
ax2.set_ylabel('Sincronía Global (R)')
ax2.grid(True, alpha=0.3)
ax2.text(50, 0.5, "ESTADO: DINÁMICA FLUIDA", ha='center', color='darkgoldenrod', fontweight='bold', bbox=dict(facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig('simulacion_ia_consciente.png', dpi=300)
print("¡Hecho! Gráfica guardada como 'simulacion_ia_consciente.png'")