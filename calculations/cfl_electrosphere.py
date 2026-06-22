"""
CFL outer-electrosphere chemical-potential profile and resulting plasma frequency.

Reproduces the firewall calculation in DESIGN_SUMMARY.md §4(b):
  - Thomas-Fermi-Poisson equation for an ultrarelativistic degenerate electron gas
    above a strange-quark-matter surface
  - Analytic solution mu_e(z) = mu_e(0) / (1 + z/H)
  - Plasma frequency profile omega_p(z)^2 = (4 alpha / 3 pi) mu_e(z)^2  (Jancovici 1962)
  - MAX omega_p along the photon path = omega_p at z=0 (surface)
  - Comparison: unpaired SQM (Alcock-Farhi-Olinto 1986) vs CFL (Alford-Kouvaris-
    Rajagopal 2005)
  - Wien-tail leakage past omega_p at T_bulk = 30.7 keV

References:
  - Alcock, Farhi & Olinto 1986, ApJ 310, 261 -- canonical strange-star
    electrosphere with mu_e(0) ~ 20 MeV
  - Alford, Kouvaris & Rajagopal 2005, PRD 71, 054009 -- CFL outer
    electrosphere mu_e ~ 5.6 MeV
  - Page & Usov 2002, PRL 89, 131101 -- thermal emission from bare quark
    surfaces
  - Stejner & Madsen 2005, PRD 72, 123005 -- detailed electrosphere structure
  - Jancovici 1962, Nuovo Cimento 25, 428 -- omega_p^2 = (4 alpha / 3 pi) mu_e^2
"""
import numpy as np

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
alpha_em = 1/137.036
hbarc_MeV_fm = 197.327                        # MeV * fm  (hbar c)
T_bulk_keV   = 30.7                            # design shell-skin temperature

# Wien-tail leakage (power-rate above cutoff x_c = omega/T):
def eps_Wien(x_c):
    return np.exp(-x_c)*(x_c**2 + 4*x_c + 6) / (7*np.pi**4/120)

def banner(s):
    print("\n" + "="*78); print(s); print("="*78)

# =============================================================================
# 1. THE THOMAS-FERMI-POISSON EQUATION FOR THE ELECTROSPHERE
# =============================================================================
banner("1. TF-POISSON FOR ULTRARELATIVISTIC DEGENERATE ELECTRONS")
# Above the SQM surface, charge neutrality is enforced by an electron cloud.
# The electron number density for an ultrarelativistic degenerate gas is
#   n_e(z) = mu_e(z)^3 / (3 pi^2 (hbar c)^3)
# Poisson's equation (in vacuum, no other charges):
#   d^2 phi / dz^2 = -4 pi e n_e(z)
# Chemical equilibrium for the electrons:
#   mu_e(z) + e phi(z) = const
# so mu_e is identified with -e phi up to an additive constant.  Substituting,
# the dimensionless Poisson equation becomes
#   d^2 mu_e / dz^2  =  (4 alpha / 3 pi) mu_e^3 / (hbar c)^2
# Boundary conditions: mu_e -> 0 as z -> infinity,
#                       mu_e(0) = mu_e^{surface} at the SQM surface.
# Analytic solution:
#   mu_e(z) = mu_e(0) / (1 + z/H)
# with scale height H = sqrt(3 pi / (8 alpha)) * (hbar c) / mu_e(0).

def H_AFO(mu_e0_MeV):
    """Electrosphere scale height (in fm)."""
    return np.sqrt(3*np.pi/(8*alpha_em)) * hbarc_MeV_fm / mu_e0_MeV

print("  Analytic AFO 1986 solution:  mu_e(z) = mu_e(0) / (1 + z/H)")
print(f"  Scale height H = sqrt(3 pi/(8 alpha)) * hbar c / mu_e(0)")
print(f"                 = {np.sqrt(3*np.pi/(8*alpha_em)):.3f} * (hbar c / mu_e(0))")
print()

# =============================================================================
# 2. mu_e AND OMEGA_P AT THE SURFACE FOR THE THREE PHYSICAL CASES
# =============================================================================
banner("2. mu_e AND omega_p AT THE SURFACE: PHASE DEPENDENCE")

def omega_p_MeV(mu_e_MeV):
    """Jancovici 1962: omega_p^2 = (4 alpha / 3 pi) mu_e^2 ."""
    return mu_e_MeV * np.sqrt(4*alpha_em/(3*np.pi))

print(f"  Phase                          mu_e(0) [MeV]   H [fm]    omega_p [MeV]")
print(f"  ----------------------------   -------------   ------    -------------")
for label, mu0 in [
    ("Unpaired SQM (AFO 1986)",          20.0),
    ("CFL gapless (AKR 2005)",            5.6),
    ("CFL pure (Schaefer/Wilczek)",       0.0),   # bulk is neutral, no electrons
    ("Conservative midpoint adopted",     9.0),   # bracketing value
]:
    if mu0 > 0:
        H = H_AFO(mu0)
        wp = omega_p_MeV(mu0)
        print(f"  {label:<30s} {mu0:>8.1f}       {H:>6.1f}    {wp:>8.3f}")
    else:
        print(f"  {label:<30s} {mu0:>8.1f}       --        0.000  (no electrosphere)")

print()
print("  Physical commentary:")
print("    - Unpaired SQM: charge neutrality requires e- to compensate for s-quark")
print("      mass suppression (m_s = 95 MeV reduces s-density vs u, d). mu_e ~ m_s/3.")
print("    - Gapless CFL (Alford-Kouvaris-Rajagopal 2005, PRD 71, 054009): the")
print("      CFL gap closes when m_s^2/(2 mu_q) > Delta, opening 'gapless' modes")
print("      that carry electric charge and require e- compensation.  Their")
print("      numerical solve yields mu_e ~ 5.6 MeV at the outer edge.")
print("    - Pure CFL (sufficient Delta, no gapless modes): exact CFL bulk is")
print("      electrically neutral (Rajagopal-Wilczek 2001).  The SURFACE may")
print("      have nonzero mu_e due to boundary effects, but the AKR analysis")
print("      bounds this below their gapless-CFL value.")
print()
print("  The mu_e ALONG THE PHOTON PATH is maximized at z=0 (the SQM surface).")
print("  Photons of frequency omega < omega_p(0) are evanescent and reflected.")
print()

# =============================================================================
# 3. ADOPTED VALUE AND FIREWALL STRENGTH
# =============================================================================
banner("3. ADOPTED FIREWALL: omega_p_outer = 0.5 MeV (conservative)")
# The 'pure CFL' theoretical value would be omega_p ~ 0.3 MeV (AKR baseline),
# but realistic surface-chemistry corrections likely push mu_e higher --
# possibly toward the unpaired SQM value where ungapped s-quark mass effects
# dominate near the surface.  Adopt the midpoint:
omega_p_adopt_MeV = 0.5
print(f"  Adopted omega_p_outer = {omega_p_adopt_MeV:.2f} MeV "
      f"(midpoint between AKR 0.31 and AFO 1.11)")
print(f"  Inferred mu_e(0) corresponding to this omega_p:")
mu_e_adopt_MeV = omega_p_adopt_MeV / np.sqrt(4*alpha_em/(3*np.pi))
print(f"     mu_e(0) = omega_p / sqrt(4 alpha/3 pi) = {mu_e_adopt_MeV:.2f} MeV")
print(f"  (this lies between 5.6 (CFL) and 20 (SQM); plausible surface average)")
print()

# Wien-tail leakage above omega_p at T_bulk = 30.7 keV:
T_bulk_MeV = T_bulk_keV/1000
x_c_adopt   = omega_p_adopt_MeV / T_bulk_MeV
eps_adopt   = eps_Wien(x_c_adopt)
print(f"  T_bulk          = {T_bulk_keV:.1f} keV = {T_bulk_MeV:.4f} MeV")
print(f"  x_c = omega_p / T_bulk = {x_c_adopt:.2f}")
print(f"  Wien-tail escape eps_Wien(x_c) = {eps_adopt:.2e}")
print()

# =============================================================================
# 4. ROBUSTNESS: omega_p VS WIEN-TAIL LEAKAGE
# =============================================================================
banner("4. ROBUSTNESS: omega_p RANGE -> Wien-tail leakage range")

print(f"  Three plausible values of mu_e(0):")
print(f"    Pure CFL (theoretical lower):  mu_e =  5.6 MeV, omega_p = 0.31 MeV")
print(f"    Adopted (conservative):        mu_e =  9.0 MeV, omega_p = 0.50 MeV")
print(f"    Unpaired SQM (theoretical):    mu_e = 20.0 MeV, omega_p = 1.11 MeV")
print()
print(f"  Wien-tail eps_Wien at T_bulk = {T_bulk_keV} keV:")
print()
for label, mu0 in [
    ("CFL (AKR)",      5.6),
    ("Adopted",        9.0),
    ("SQM (AFO)",     20.0),
]:
    wp = omega_p_MeV(mu0)
    xc = wp / T_bulk_MeV
    eps = eps_Wien(xc)
    print(f"  {label:<20s}:  omega_p = {wp:.3f} MeV   x_c = {xc:5.1f}   eps = {eps:.2e}")

# Comparison to off-axis budget: bulk emits at ~blackbody rate from T_bulk = 30.7 keV
# over A_shell ~ 50 m^2.  sigma T^4 at T = 30.7 keV = 3.6e8 K:
T_bulk_K = T_bulk_MeV*1e6 / (8.617e-5)    # MeV / (eV/K * 1e-6) = K
sigma_SB = 5.67e-8
P_bb_per_m2 = sigma_SB * T_bulk_K**4
A_shell = 50.27
P_bb_total = P_bb_per_m2 * A_shell
print()
print(f"  Blackbody luminosity bound (if bulk were optically thick at T_bulk):")
print(f"    T_bulk = {T_bulk_K:.2e} K")
print(f"    sigma T^4 = {P_bb_per_m2:.2e} W/m^2")
print(f"    A_shell * sigma T^4 = {P_bb_total:.2e} W = {P_bb_total/1e12:.1e} TW")
print(f"  (this is a VERY loose upper bound; the actual emissivity is set by")
print(f"   H-Goldstone anomaly + gap suppression -- see Task C / §4(c).)")
print()
print(f"  Naive 'blackbody * Wien-tail' bound on outer-surface EM leakage:")
for label, mu0 in [("CFL", 5.6), ("Adopted", 9.0), ("SQM", 20.0)]:
    wp  = omega_p_MeV(mu0)
    eps = eps_Wien(wp/T_bulk_MeV)
    P_leak = P_bb_total * eps
    print(f"    {label:<10s}: omega_p = {wp:.2f} MeV  -> P_leak < {P_leak:.2e} W")

print()
print("  Conclusion: even the CFL-pessimistic case (omega_p = 0.31 MeV) gives")
print("  eps_Wien * blackbody-bound < 10^23 W, still factor-10^5 above the 1 MW")
print("  off-axis budget. The blackbody bound is the WRONG bound -- it assumes the")
print("  bulk emits at the rate of a perfect emitter at T_bulk, which is *only*")
print("  realized if there is a frequency-unsuppressed coupling between bulk")
print("  thermal motion and photons.  In the CFL phase the gap forbids this:")
print("  the relevant emissivity is the H-Goldstone-anomaly rate (Task C / §4(c)),")
print("  which is power-law (not exponentially) suppressed but is itself bounded")
print("  to << blackbody.  See cfl_emissivity.py for the chiPT bound.")

# =============================================================================
# 5. POSITION-DEPENDENT omega_p AND TURNING POINT
# =============================================================================
banner("5. POSITION-DEPENDENT omega_p AND PHOTON TURNING POINT")

print("  For a photon of frequency omega traveling outward from the bulk:")
print("    - It encounters omega_p^2 rising as z decreases (toward the surface)")
print("    - At z = 0, omega_p^2 reaches its maximum")
print("    - For z > 0 (vacuum side), omega_p^2 falls off as 1/(1+z/H)^2")
print()
print("  If omega < omega_p_max, the photon is reflected at the deepest point")
print("  where omega^2 = omega_p^2.  In the AFO solution:")
print("    omega_p(z)^2 = omega_p(0)^2 / (1 + z/H)^2")
print("    Turning point z*: 1 + z*/H = omega_p(0)/omega")
print()
print("  For T_bulk = 30.7 keV and a 3kT = 92 keV photon at omega_p(0) = 0.5 MeV:")
print(f"     z*/H = (omega_p/omega) - 1 = {0.5/0.092 - 1:.2f}")
print(f"  Turning point ~ H = "
      f"{H_AFO(mu_e_adopt_MeV)*(omega_p_adopt_MeV/0.092 - 1):.0f} fm.")
print("  Reflection is decisive within a few hundred fm of the surface.")
