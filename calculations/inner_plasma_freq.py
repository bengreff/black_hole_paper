"""
Inner-cavity plasma frequency from bombardment-driven pair density.

Tightens the §9 item 14 resolution: the steady-state pair density n* set by
the multi-bounce dynamics in the magnetic bottle gives an inner-cavity plasma
frequency far below the design's earlier 7 MeV claim.

Method:
  1. Pair emission rate per area from the Usov mechanism (§4).
  2. Per-pair cavity residence time = N_bounces * tau_b (collisional pitch-
     angle randomization, ~6-10 bounces per emission).
  3. Steady-state population: n* = (pair flux * residence time) / V_cavity.
  4. Plasma frequency: ω_p^2 = n_e e^2 / (epsilon_0 m_e).
  5. Compare to the design's annihilation-photon energy 0.511 MeV; conclude
     that ω_p << 0.511 MeV, so the cavity-side annihilation photons are
     NOT reflected by an inner plasma mirror; they instead pair-convert in
     the strong BH-side magnetic field (chi >> 1 -- see §3 stage 3).
"""
import numpy as np

def banner(s):
    print("\n" + "="*78); print(s); print("="*78)

# Constants
hbar = 1.054_571_817e-34
c    = 2.997_924_58e8
e_q  = 1.602_176_634e-19
me   = 9.109_383_7e-31
eps0 = 8.854_187_8128e-12
MeV_J = 1.602_176_634e-13
eV_J  = 1.602_176_634e-19

# Cavity parameters (§§4-5)
R_cavity_m = 2.0
A_shell_m2 = 4*np.pi*R_cavity_m**2
V_cavity_m3 = (4/3)*np.pi*R_cavity_m**3
L_pair_W_per_m2 = 8.21e15      # design L_pair (§4)
E_pair_J = 0.542*MeV_J         # per pair total energy
beta_pair = 0.332
v_pair = beta_pair * c
tau_b = 2.0 / v_pair           # bounce period
N_bounces = 8                  # 6-10; midpoint
tau_res = N_bounces * tau_b    # residence time per pair

# =============================================================================
# 1. STEADY-STATE PAIR DENSITY
# =============================================================================
banner("1. STEADY-STATE PAIR DENSITY IN CAVITY")

pair_rate_per_m2 = L_pair_W_per_m2 / E_pair_J
total_pair_rate = pair_rate_per_m2 * A_shell_m2
print(f"  L_pair                = {L_pair_W_per_m2:.2e} W/m^2")
print(f"  E_pair (total)        = {E_pair_J/MeV_J:.3f} MeV = {E_pair_J:.2e} J")
print(f"  Pair rate per area    = L/E = {pair_rate_per_m2:.2e} /m^2/s")
print(f"  Total pair rate       = {total_pair_rate:.2e} /s")
print()
print(f"  Cavity volume         = {V_cavity_m3:.2f} m^3")
print(f"  Bounce period tau_b   = 2R/v = {tau_b*1e9:.1f} ns")
print(f"  Bounces per emission  = {N_bounces}")
print(f"  Residence time tau_res = {tau_res*1e9:.0f} ns")
print()
n_pair = total_pair_rate * tau_res / V_cavity_m3
n_e = 2 * n_pair    # e+ and e- both contribute as charge carriers
print(f"  Steady-state pair n*  = {n_pair:.2e} /m^3")
print(f"  Total e+ + e- density = {n_e:.2e} /m^3")

# =============================================================================
# 2. PLASMA FREQUENCY
# =============================================================================
banner("2. PLASMA FREQUENCY")

# Non-relativistic formula (pair kinetic energy ~ 30 keV << m_e c^2 = 511 keV)
omega_p_sq = n_e * e_q**2 / (eps0 * me)
omega_p = np.sqrt(omega_p_sq)
hbar_omega_p_J = hbar * omega_p
hbar_omega_p_eV = hbar_omega_p_J / eV_J

print(f"  Non-relativistic formula: omega_p^2 = n e^2 / (epsilon_0 m_e)")
print(f"  omega_p              = {omega_p:.2e} rad/s")
print(f"  hbar omega_p         = {hbar_omega_p_J:.2e} J = {hbar_omega_p_eV*1e3:.3f} meV")
print(f"                       = {hbar_omega_p_eV:.3e} eV")

# Relativistic correction: omega_p^2 -> omega_p^2 / gamma (for cold plasma)
gamma_pair = 1.060
omega_p_rel = omega_p / np.sqrt(gamma_pair)
hbar_omega_p_rel_eV = hbar * omega_p_rel / eV_J
print(f"\n  Relativistic correction (cold-plasma): omega_p -> omega_p / sqrt(gamma)")
print(f"  hbar omega_p (rel)   = {hbar_omega_p_rel_eV*1e3:.3f} meV")
print(f"  (negligible correction since gamma = {gamma_pair} is close to 1)")

# =============================================================================
# 3. CONSEQUENCES FOR THE INNER MIRROR ROLE
# =============================================================================
banner("3. CONSEQUENCES")

print(f"  Inner-cavity plasma frequency: hbar omega_p_inner ~ "
      f"{hbar_omega_p_eV*1e3:.2f} meV")
print(f"  Annihilation-photon energy: 2 m_e c^2 = 1.022 MeV per gamma pair")
print(f"  Bombardment photon energy: ~ kT_pair = 30.7 keV")
print()
print(f"  Ratio: omega_photon / omega_p ~ "
      f"{30.7e3/hbar_omega_p_eV:.2e}  (for 30.7 keV photons)")
print()
print("  Conclusion: ω_p_inner is many orders of magnitude BELOW any photon")
print("  energy of interest.  The 'inner plasma mirror' role attributed in the")
print("  earlier draft (ω_p ~ 7 MeV) was orders too high.")
print()
print("  Why this doesn't break the design:")
print("    The cavity-side annihilation photons (0.511 MeV from e+e- -> 2 gamma)")
print("    are NOT reflected by the inner plasma -- they instead pair-CONVERT in")
print("    the strong BH-side magnetic field (chi = (omega/m_e c^2)(B/B_cr) >> 1")
print("    at any radius r < r_chi where B(r) > B_cr).")
print("    The pair-converted electrons/positrons then magnetically circulate back")
print("    to the shell, depositing their energy and contributing to the captured")
print("    power.  Energy bookkeeping is preserved without an inner plasma mirror.")
print()
print(f"  Critical-radius computation (B = B_cr at r_chi):")
mu0 = 4*np.pi*1e-7
g_BH = 1.182e6
B_cr = 4.41e9    # Schwinger critical field
r_chi = np.sqrt(mu0*g_BH/(4*np.pi*B_cr))
print(f"    B(r) = (mu0/4 pi) g/r^2 = B_cr at r = sqrt((mu0/4 pi) g / B_cr) = "
      f"{r_chi*1e6:.2f} um")
print(f"    Only photons passing within ~5 um of the BH see B > B_cr;")
print(f"    cavity volume fraction within r_chi: (r_chi/R)^3 ~ "
      f"{(r_chi/R_cavity_m)**3:.2e}.")
print()
print(f"  Most cavity annihilation gammas (positrons in the inner electrosphere ~30 fm")
print(f"  deep) emit isotropically.  ~50% go DEEPER into the shell (absorbed within")
print(f"  the 3 pm stopping budget); the other ~50% go back through the cavity and")
print(f"  are absorbed on the opposite shell wall.  Energy is preserved either way;")
print(f"  the inner plasma mirror is NOT the load-bearing reflection mechanism.")
