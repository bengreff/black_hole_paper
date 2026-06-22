"""
CFL bulk emissivity via the H-Goldstone anomaly channel.

Computes the rate of eta' + eta' -> gamma + gamma (the dominant unsuppressed
photon-emission channel in the CFL phase) and the resulting outer-surface
EM leakage past the Wien-tail plasma-mirror cutoff.

Physical setup:
  - The U(1)_B Goldstone H (eta'-like) in CFL is massless at tree level.
  - The anomaly Lagrangian L = (c_anom / F_pi) H F F-tilde gives a tree-level
    H -> gamma gamma vertex with coupling alpha/F_pi.
  - For massless H the 1-particle decay is kinematically forbidden (degeneracy
    with vacuum); the leading photon-producing process is the 2->2
    annihilation H + H -> gamma + gamma via t-/u-channel H exchange.
  - The amplitude |M|^2 ~ alpha^4 T^4 / F_pi^4 (NOT alpha^2 -- the design's
    earlier dimensional estimate was off by alpha^2; the rigorous chiPT
    counting gives one alpha at each anomaly vertex of which there are TWO).
  - Volumetric power per volume P/V ~ alpha^4 T^9 / (pi^4 F_pi^4).
  - Wien-tail fraction of this above the outer plasma frequency gives the
    actual outer-surface escape rate.

References:
  - Wess & Zumino 1971 (chiral anomaly Lagrangian)
  - Son & Stephanov 2000 (CFL meson masses and decay constants)
  - Jaikumar, Rischke & Shovkovy 2003, PRC 68, 045803 (massive-Goldstone channels)
  - Anglani-Mannarelli-Ruggieri 2011 (CFL transport review)

DESIGN_SUMMARY.md §4(c) and §9 item 7 are updated to reflect the calculation.
"""
import numpy as np

# -----------------------------------------------------------------------------
# Conversion factor: power/volume in GeV^5 (natural units) to W/m^3 (SI)
# -----------------------------------------------------------------------------
# 1 GeV (energy) = 1.602e-10 J;  1 GeV^-1 (time) = hbar/GeV = 6.582e-25 s;
# 1 GeV^-3 (volume) = (hbar c / GeV)^3 = (1.9733e-16 m)^3 = 7.685e-48 m^3.
# Therefore 1 GeV^5 = (1 GeV^2) * (1 GeV^3)
#                   = (energy/time)_natural * (volume^-1)_natural
#                   = (1.602e-10 / 6.582e-25) W * (1/7.685e-48) m^-3
#                   = 2.434e14 W * 1.301e47 m^-3
#                   = 3.167e61 W/m^3
GeV5_to_W_per_m3 = 3.167e61

alpha_em = 1/137.036
T_keV    = 30.7
T_MeV    = T_keV/1000
T_GeV    = T_MeV/1000

# CFL decay constant for U(1)_B Goldstone H.  Son-Stephanov 2000:
#   f_H^2 = (3 - 2 mu_s/mu) mu^2 / (8 pi^2)  at asymptotically high density,
#   with mu = quark chemical potential (~ 400 MeV at SQM density),
#   mu_s = strange chem pot (~ 0 to leading order).
# For mu_q = 400 MeV: f_H^2 ~ 3 * 0.16 / (8 pi^2) = 6.1e-3 GeV^2 -> f_H = 78 MeV.
# We adopt F_pi^CFL = 100 MeV as a clean round number close to f_H.
F_pi_GeV  = 0.100      # 100 MeV
F_pi_MeV  = 100.0

A_shell = 50.27        # m^2 (R = 2 m)
t_shell_m = 3.0e-12    # 3 pm
V_shell   = A_shell * t_shell_m

def banner(s):
    print("\n" + "="*78); print(s); print("="*78)

# =============================================================================
# 1. ANOMALY-MEDIATED H + H -> gamma + gamma RATE
# =============================================================================
banner("1. CHIRAL-ANOMALY 2->2 RATE  H + H -> 2 gamma")

print("  Anomaly Lagrangian (Wess-Zumino):")
print("    L = (c_anom alpha / pi F_pi) H F_mu_nu F-tilde^mu_nu")
print("  with c_anom = O(1) anomaly coefficient (depends on N_c, N_f).")
print()
print("  For massless H, single-H decay H -> 2 gamma is kinematically forbidden.")
print("  Leading photon-producing process: H + H -> 2 gamma via t-/u-channel H.")
print()
print("  Amplitude scaling:")
print("    |M|^2 ~ alpha^4 T^4 / F_pi^4    (each anomaly vertex carries alpha^1,")
print("                                      two vertices in the 2->2 process)")
print("    sigma(s) ~ |M|^2 / s ~ alpha^4 T^2 / F_pi^4    (at thermal s ~ T^2)")
print("    n_H ~ T^3 / pi^2 (massless thermal boson)")
print("    n^2 sigma v ~ alpha^4 T^8 / (pi^4 F_pi^4)")
print("    P/V ~ T x rate ~ alpha^4 T^9 / (pi^4 F_pi^4)")
print()

# Numerical computation:
P_per_V_natural = alpha_em**4 * T_GeV**9 / (np.pi**4 * F_pi_GeV**4)
P_per_V_SI = P_per_V_natural * GeV5_to_W_per_m3

print(f"  Numerical (T = {T_keV} keV, F_pi = {F_pi_MeV} MeV):")
print(f"    alpha^4                         = {alpha_em**4:.2e}")
print(f"    T^9                              = {T_GeV**9:.2e} GeV^9")
print(f"    F_pi^4                           = {F_pi_GeV**4:.2e} GeV^4")
print(f"    1/pi^4                           = {1/np.pi**4:.3f}")
print(f"    P/V = alpha^4 T^9 / (pi^4 F_pi^4) = {P_per_V_natural:.2e} GeV^5")
print(f"                                       = {P_per_V_SI:.2e} W/m^3")

P_bulk_total = P_per_V_SI * V_shell
print(f"\n  Shell volume V = A * t = {V_shell:.2e} m^3")
print(f"  Total bulk emission P = (P/V) * V  = {P_bulk_total:.2e} W")
print(f"                                     = {P_bulk_total/1e3:.1f} kW")

# =============================================================================
# 2. WIEN-TAIL ESCAPE PAST THE OUTER PLASMA-MIRROR
# =============================================================================
banner("2. WIEN-TAIL ESCAPE PAST omega_p_outer")

def eps_Wien(x_c):
    return np.exp(-x_c)*(x_c**2 + 4*x_c + 6) / (7*np.pi**4/120)

print(f"  Photons emitted at characteristic energy ~ 2 T = {2*T_keV:.1f} keV")
print(f"  T_bulk = {T_keV:.1f} keV; emission spectrum thermal-like at T.")
print()
print(f"  Outer plasma frequency cases (from cfl_electrosphere.py):")

cases = [
    ("CFL pessimistic (AKR)",  0.31),
    ("Adopted",                0.50),
    ("Unpaired SQM (AFO)",     1.11),
]
for label, omega_p_MeV in cases:
    x_c = omega_p_MeV*1000 / T_keV     # convert MeV -> keV for x_c
    eps = eps_Wien(x_c)
    P_escape = P_bulk_total * eps
    print(f"   {label:<28s}: omega_p = {omega_p_MeV:.2f} MeV   "
          f"x_c = {x_c:6.2f}   eps = {eps:.2e}   "
          f"P_escape = {P_escape:.2e} W")

# =============================================================================
# 3. COMPARISON TO OFF-AXIS BUDGET
# =============================================================================
banner("3. MARGIN AGAINST 1 MW OFF-AXIS BUDGET")

budget_W = 1.0e6
print(f"  Off-axis EM budget: {budget_W/1e6:.0f} MW")
print()
print(f"  Margin = budget / P_escape, by case:")
for label, omega_p_MeV in cases:
    x_c = omega_p_MeV*1000 / T_keV
    eps = eps_Wien(x_c)
    P_escape = P_bulk_total * eps
    margin = budget_W / P_escape if P_escape > 0 else np.inf
    print(f"   {label:<28s}: margin = {margin:.2e}x")
print()
print("  Conclusion: even in the pessimistic CFL case (omega_p_outer = 0.31 MeV),")
print("  the chiPT-bounded H-anomaly emission is within budget by a factor of 30,000")
print("  for the alpha^4 scaling.  This significantly tightens the design's prior")
print("  dimensional estimate (alpha^2 T^9/F_pi^4) which was off by two factors of")
print("  alpha and gave a marginal margin.")

# =============================================================================
# 4. UNCERTAINTY BUDGET
# =============================================================================
banner("4. UNCERTAINTY BUDGET")

print("  Sources of factor-of-N uncertainty in P/V:")
print()
print("  (a) Anomaly coefficient c_anom: for CFL with N_c = 3 colors locked to")
print("      N_f = 3 flavors, c_anom = N_c sum_f Q_f^2 / sqrt(N_f) ~ 1.  Could")
print("      easily be 0.1-3 depending on the exact CFL embedding; factor of ~10")
print("      uncertainty in P/V (it enters squared).")
print()
print("  (b) F_pi^CFL: design value 100 MeV; Son-Stephanov asymptotic value at")
print("      mu_q = 400 MeV gives 78 MeV.  Realistic value at SQM density may")
print("      differ by factor of 2; this enters as 1/F_pi^4, so factor of 16")
print("      uncertainty in P/V.")
print()
print("  (c) Phase-space prefactor: schematic 1/pi^4 may absorb factor of 10 from")
print("      proper-flux-and-integrand calculation.")
print()
print("  Net uncertainty in P/V: factor of ~100-1000.  Even with a 10^3")
print("  enhancement, P_escape stays below 1 MW for the pessimistic CFL case.")
print()
print("  The H-anomaly channel is the residual leakage channel after all other")
print("  bulk emission paths (gap suppression for quark quasiparticles, Boltzmann")
print("  suppression for massive Goldstones) are exponentially closed.  It is")
print("  comfortable below the design budget under all plausible scaling.")

# =============================================================================
# 5. WHY THE alpha^2 ESTIMATE IN THE EARLIER DRAFT WAS WRONG
# =============================================================================
banner("5. NOTE: alpha^2 vs alpha^4 IN THE PRIOR ESTIMATE")

print("  An earlier draft DESIGN_SUMMARY.md §4(c) wrote 'P/V ~ alpha^2 T^9/F_pi^4'.")
print("  This counts the anomaly coupling as a single insertion of alpha/F_pi^2,")
print("  appropriate for a 1->2 decay tree amplitude squared (alpha^2/F_pi^4).")
print("  For the 2->2 process H + H -> 2 gamma the amplitude has TWO anomaly")
print("  insertions (one at each photon vertex via t/u-channel H exchange), so")
print("  |M|^2 carries alpha^4 not alpha^2.  This is the rigorous chiPT counting.")
print()
print("  The factor-of-alpha^2 = 5e-5 favor over the prior estimate is what makes")
print("  the bulk H-Goldstone emissivity comfortably bounded.  The factor-of-pi^4")
print("  in the denominator (from the loop and thermal phase-space integrals)")
print("  contributes another factor of 100 suppression.")
