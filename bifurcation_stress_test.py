import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# --- Configuración ---
F_values = np.linspace(0, 5.0, 200)  # Rango de fuerza de 0 a 5
mu = 1.0
omega_0 = 1.0

# Configuración temporal para diagrama de bifurcación
t_transient = 500  # Tiempo para eliminar transitorios
t_sampling = 100   # Ventana de muestreo
steps_per_cycle = 50 

def van_der_pol(state, t, mu, w0, F, w_ext):
    x, v = state
    dxdt = v
    dvdt = mu * (1 - x**2) * v - (w0**2) * x + F * np.cos(w_ext * t)
    return [dxdt, dvdt]

def get_bifurcation_points(w_ext_type):
    if w_ext_type == 'rational':
        w_ext = 1.0 
        print("Calculando Racional (1:1)...")
    else:
        phi = (1 + np.sqrt(5)) / 2
        w_ext = phi
        print("Calculando Áureo (Phi)...")
        
    period = 2 * np.pi / w_ext
    dt = period / steps_per_cycle
    bif_F = []
    bif_x = []
    state = [0.1, 0.1]
    
    for F in F_values:
        # Estabilizar
        t_trans = np.arange(0, t_transient, dt)
        sol = odeint(van_der_pol, state, t_trans, args=(mu, omega_0, F, w_ext))
        state = sol[-1]
        
        # Muestrear (Estroboscópico)
        t_samp = np.arange(0, t_sampling, dt)
        sol_samp = odeint(van_der_pol, state, t_samp, args=(mu, omega_0, F, w_ext))
        
        # Tomar puntos solo al final de cada ciclo
        indices = np.arange(0, len(sol_samp), steps_per_cycle)
        points_x = sol_samp[indices, 0]
        
        bif_F.extend([F] * len(points_x))
        bif_x.extend(points_x)
        
    return bif_F, bif_x

# --- Ejecución ---
F_rat, x_rat = get_bifurcation_points('rational')
F_gold, x_gold = get_bifurcation_points('golden')

# --- Graficar ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

# Racional
ax1.scatter(F_rat, x_rat, s=0.5, c='red', alpha=0.5)
ax1.set_title("Trayectoria Racional: Ruta Rápida al Caos", fontweight='bold')
ax1.set_ylabel("Posición Estroboscópica x(nT)")
ax1.set_ylim(-3, 3)
ax1.grid(True, alpha=0.3)

# Áureo
ax2.scatter(F_gold, x_gold, s=0.5, c='darkgoldenrod', alpha=0.5)
ax2.set_title("Trayectoria Áurea: Robustez Estructural (Frontera Resonante)", fontweight='bold')
ax2.set_xlabel("Amplitud de Fuerza F")
ax2.set_ylabel("Posición Estroboscópica x(nT)")
ax2.set_ylim(-3, 3)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("figura5_bifurcacion.png", dpi=300)
print("¡Hecho! Gráfica guardada como 'figura5_bifurcacion.png'")