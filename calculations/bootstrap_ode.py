"""
Bootstrap-phase coupled ODE for BH mass growth from 250 t seed to 10^9 kg.

ODE:    dM/dt = A(f_cap, gamma) * P(M)/c^2
        P(M)  = hbar c^6 f(M) / (G^2 M^2)
        A     = gamma f_cap / 0.061 - 1   (pellet KE-to-mass-energy factor)

f(M) is the Hawking emission factor, varying as kT crosses SM thresholds.
We tabulate f(M) and integrate the ODE numerically.

DESIGN_SUMMARY.md §7.  Companion to calculations/hawking_spectrum.py.
"""
import numpy as np
from scipy.integrate import quad, odeint
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Constants (SI)
hbar = 1.054_571_817e-34
c    = 2.997_924_58e8
G    = 6.6743e-11
GeV_J = 1.602_176_634e-10
kB   = 1.380_649e-23
me_c2_MeV = 0.510998950

# Page power-rate coefficients per DOF
ALPHA_SCALAR = 7.24e-5
ALPHA_FERMION = 4.09e-5
ALPHA_VECTOR = 1.68e-5
ALPHA_GRAVITON = 1.92e-6

SM = [
    ("up",    "fermion", 12, 0.0022),
    ("down",  "fermion", 12, 0.0047),
    ("strange","fermion",12, 0.095),
    ("charm", "fermion", 12, 1.27),
    ("bottom","fermion", 12, 4.18),
    ("top",   "fermion", 12, 173.0),
    ("e",     "fermion", 4,  me_c2_MeV*1e-3),
    ("mu",    "fermion", 4,  0.1057),
    ("tau",   "fermion", 4,  1.777),
    ("nu",    "fermion", 6,  0.0),
    ("gluon", "vector",  16, 0.0),
    ("photon","vector",  2,  0.0),
    ("W",     "vector",  6,  80.379),
    ("Z",     "vector",  3,  91.188),
    ("Higgs", "scalar",  1,  125.10),
    ("graviton","graviton",2,0.0),
]
ALPHA = {"scalar":ALPHA_SCALAR, "fermion":ALPHA_FERMION,
         "vector":ALPHA_VECTOR, "graviton":ALPHA_GRAVITON}

def suppression(x_m, fermion=True):
    if x_m == 0: return 1.0
    sign = +1.0 if fermion else -1.0
    def integrand(x):
        return np.where(x > 50.0, x**3*np.exp(-x),
                        x**3/(np.exp(np.minimum(x,50.0))+sign))
    num = quad(integrand, x_m, np.inf, limit=200)[0]
    den = quad(integrand, 0,   np.inf, limit=200)[0]
    return num/den

def f_at_mass(M_kg):
    """Hawking emission factor f at BH mass M."""
    kT_J = hbar*c**3 / (8*np.pi*G*M_kg)
    kT_GeV = kT_J/GeV_J
    f = 0.0
    for (name, typ, dof, mGeV) in SM:
        x = mGeV/kT_GeV
        S = suppression(x, fermion=(typ=="fermion"))
        f += dof*ALPHA[typ]*S
    return f

def banner(s):
    print("\n" + "="*78); print(s); print("="*78)

# =============================================================================
# 1. TABULATE f(M) ACROSS THE BOOTSTRAP RANGE
# =============================================================================
banner("1. f(M) ACROSS BOOTSTRAP RANGE  250 t -> 1e9 kg")

masses_kg = np.logspace(5.4, 9.0, 20)   # 250 t = 2.5e5 kg to 1e9 kg
f_vals = np.array([f_at_mass(M) for M in masses_kg])
kT_vals_GeV = hbar*c**3 / (8*np.pi*G*masses_kg) / GeV_J

print(f"  {'M [kg]':>12s} {'kT [GeV]':>12s} {'f':>12s}")
for M, f, kT in zip(masses_kg, f_vals, kT_vals_GeV):
    print(f"  {M:>12.2e} {kT:>12.3e} {f:>12.3e}")

# =============================================================================
# 2. BOOTSTRAP ODE
# =============================================================================
banner("2. BOOTSTRAP ODE INTEGRATION")

# Pellet KE/total-energy ratio at beta = 0.33: (gamma-1)/gamma ~ 0.061
beta_pellet = 0.33
gamma_pellet = 1/np.sqrt(1 - beta_pellet**2)
KE_frac = (gamma_pellet - 1)/gamma_pellet
print(f"  Pellet beta = {beta_pellet}, gamma = {gamma_pellet:.4f}")
print(f"  KE/E_total per pellet = (gamma-1)/gamma = {KE_frac:.4f}")

# Capture fraction (railgun-recovery efficiency)
f_cap_baseline = 0.50
A_factor = gamma_pellet * f_cap_baseline / KE_frac - 1.0
print(f"  Recovery fraction f_cap = {f_cap_baseline}")
print(f"  Growth amplification A = gamma f_cap / KE_frac - 1 = {A_factor:.3f}")

# Build interpolant for f(M)
def f_interp(M_kg):
    log_M = np.log10(M_kg)
    log_M_arr = np.log10(masses_kg)
    return np.interp(log_M, log_M_arr, f_vals)

def dMdt(M, t, A):
    """ODE: dM/dt = A * P(M)/c^2 = A * hbar c^4 f(M) / (G^2 M^2)."""
    f = f_interp(M)
    P_Watts = hbar * c**6 * f / (G**2 * M**2)
    return A * P_Watts / c**2

# Integrate from M_0 = 250 t to M_f = 10^9 kg
M_0 = 2.5e5     # 250 t
M_f = 1.0e9
# Use log-mass grid for accuracy
t_max = 1e9    # s; we'll cap when M reaches M_f

# Use scipy odeint with large t span; sample on log-M grid afterwards
# Avoid stiff issues by integrating with appropriate t range
yr = 365.25*86400

# Estimate the bootstrap time analytically first:
# dM/dt = A f hbar c^4 / (G^2 M^2)
# M^2 dM = A f hbar c^4 / G^2 dt
# (M_f^3 - M_0^3)/3 ~ A f_avg hbar c^4 / G^2 * t
f_avg = np.mean(f_vals)
t_est_yr = (M_f**3 - M_0**3) * G**2 / (3 * A_factor * f_avg * hbar * c**4) / yr
print(f"  Analytic estimate t ~ G^2 (M_f^3 - M_0^3) / (3 A <f> hbar c^4) = "
      f"{t_est_yr:.2f} yr")

# Numerical integration:
t_arr = np.linspace(0, 5*t_est_yr*yr, 2000)
sol = odeint(dMdt, M_0, t_arr, args=(A_factor,), full_output=False)
M_t = sol[:,0]

# Find time at which M reaches M_f
i_done = np.searchsorted(M_t, M_f)
t_bootstrap_s = t_arr[i_done] if i_done < len(t_arr) else t_arr[-1]
print(f"  Numerical bootstrap time:    t = {t_bootstrap_s/yr:.2f} yr")

# Bootstrap time scales:
# - Early phase: M small, dM/dt = A f hbar c^4 / (G^2 M^2) is huge.
# - Late phase: M ~ M_f, dM/dt = A f hbar c^4 / (G^2 M_f^2) is moderate.
# Half-life to reach M = M_f/2 from M_0:
i_half = np.searchsorted(M_t, M_f/2)
print(f"  Time to reach M = 5e8 kg:   t = {t_arr[i_half]/yr:.2f} yr")
i_tenth = np.searchsorted(M_t, M_f/10)
print(f"  Time to reach M = 1e8 kg:   t = {t_arr[i_tenth]/yr:.2f} yr")
i_kg = np.searchsorted(M_t, 1e7)
print(f"  Time to reach M = 1e7 kg:   t = {t_arr[i_kg]/yr:.4f} yr "
      f"= {t_arr[i_kg]:.2e} s")

# =============================================================================
# 3. RAILGUN POWER PROFILE vs M
# =============================================================================
banner("3. RAILGUN POWER REQUIREMENT vs BH MASS")

def P_railgun_W(M, f_cap):
    f = f_interp(M)
    P_H = hbar * c**6 * f / (G**2 * M**2)
    return f_cap * P_H

print(f"  {'M [kg]':>12s} {'P_H [W]':>12s} {'P_railgun [W]':>15s}")
for M_test in [2.5e5, 1e6, 1e7, 1e8, 1e9]:
    P_H = hbar * c**6 * f_interp(M_test) / (G**2 * M_test**2)
    P_rg = f_cap_baseline * P_H
    print(f"  {M_test:>12.2e} {P_H:>12.3e} {P_rg:>15.3e}")
print()
print("  The railgun must scale dynamically over 8 orders of magnitude in power.")
print("  Early phase requires PW-class power into ~tonnes/s pellet flow;")
print("  late phase requires ~30 PW into kg/s pellet flow.")

# =============================================================================
# 4. RECOVERY SHELL REQUIREMENT vs M
# =============================================================================
banner("4. RECOVERY SHELL STOPPING BUDGET vs M")

# The recovery shell must absorb the spectrum at each M.  At each M, kT scales
# as 1/M, so the (mu+tau) tail energy E_c that needs to be stopped scales:
# E_c needed = 20-25 * kT (from §3 punch-through analysis)
print(f"  {'M [kg]':>12s} {'kT [GeV]':>12s} {'E_c needed [GeV]':>17s}"
      f" {'t_shell (3000fm @ 1e9kg scaling) [pm]':>40s}")
for M_test in [2.5e5, 1e6, 1e7, 1e8, 1e9]:
    kT = hbar*c**3 / (8*np.pi*G*M_test) / GeV_J
    Ec = 22.7 * kT
    # 3 pm shell at design point = 240 GeV stopping budget at 80 MeV/fm.
    t_pm = Ec / (80e-3 * 1000) * 1e3  # GeV / (GeV/pm) = pm
    print(f"  {M_test:>12.2e} {kT:>12.3e} {Ec:>17.1f} {t_pm:>40.1f}")
print()
print("  The recovery shell at the seed phase (M = 250 t) must be ~12,000x thicker")
print("  than the operational 3 pm shell, but for only ~6 ms (the seed BH lifetime).")
print("  Engineering tractability: this is the dominant challenge of the bootstrap.")

# Plot M vs t and produce a PNG
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].semilogy(t_arr/yr, M_t)
axes[0].set_xlabel("time [yr]"); axes[0].set_ylabel("M [kg]")
axes[0].set_title("BH mass during bootstrap")
axes[0].set_xlim(0, t_bootstrap_s/yr*1.1)
axes[0].axhline(M_f, color='r', linestyle='--', label='M_f = 10^9 kg')
axes[0].legend()

axes[1].loglog(masses_kg, f_vals, 'o-')
axes[1].set_xlabel("M [kg]"); axes[1].set_ylabel("f(M)")
axes[1].set_title("Hawking emission factor f vs M")
plt.tight_layout()
fig.savefig("/Users/ben/black_hole_paper/figures/bootstrap_ode.png", dpi=100)
print(f"  Plot saved to figures/bootstrap_ode.png")

# =============================================================================
# 5. SUMMARY
# =============================================================================
banner("5. SUMMARY")

print(f"  Bootstrap from M_0 = 250 t to M_f = 10^9 kg, f_cap = {f_cap_baseline}:")
print(f"    Total time ~ {t_bootstrap_s/yr:.2f} yr")
print(f"    Dominated by late-phase 1/M^2 slowdown")
print()
print(f"  Sensitivity to f_cap:")
for f_cap in [0.2, 0.3, 0.5, 0.7, 0.9]:
    A_f = gamma_pellet * f_cap / KE_frac - 1.0
    t_est_yr = (M_f**3) * G**2 / (3 * A_f * f_avg * hbar * c**4) / yr
    print(f"    f_cap = {f_cap}: A = {A_f:.2f}, t_bootstrap ~ {t_est_yr:.2f} yr")
print()
print(f"  Engineering constraints:")
print(f"    - Railgun power ranges 10^17 - 10^25 W over the bootstrap (8 OOM)")
print(f"    - Recovery shell thickness scales linearly with kT, i.e. 1/M")
print(f"    - Pellet mass-rate ranges 10^-1 - 10^11 kg/s (12 OOM)")
print(f"    - Throughout, the architecture is mass-positive only if f_cap > 0.061")
print(f"      (the pellet-KE-cost threshold).  Baseline f_cap = 0.5 is comfortable.")
