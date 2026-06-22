"""
Seed monopole production: option-by-option rate calculation.

Phase-2 breeding (§7.5) requires a single seed monopole-antimonopole pair.
The design's PRIMARY path for producing that first pair is Option B below
(Ambjorn-Olesen accelerator).  Option A (primordial-flux capture) is retained
as a passive fallback.  The other options are deprecated.

PRIMARY (Option B): ~2000 km ring at 1000 T sustained dipoles, Pb-Pb at
25 PeV/nucleon (gamma ~ 1.4e7) producing Cho-Maison electroweak monopoles
at the W-condensate instability threshold.  See DESIGN_SUMMARY.md §7.5.1.

FALLBACK (Option A): passive 1 km^2 superconducting sail at L1, 30 yr, with
Meissner-trap detection.  Useful only if primordial flux Phi is at or near
the current MACRO upper bound; the empirical trajectory is steadily ruling
this out.

Mechanisms evaluated:
  A. Passive capture from primordial cosmic monopole flux (Kibble mechanism
     residue) with a magnetic-flux concentrator sail. [FALLBACK]
  B. Lab production via the Ambjorn-Olesen W-condensate instability at
     B > B_AO ~ 1e20 T. [PRIMARY]
  C. Heavy-ion collisions via the Schwinger mechanism (current LHC/MoEDAL
     and future-collider extrapolations). [DEPRECATED - subsumed by B]
  D. Primordial micrograms-scale BH Hawking-emission of monopoles. [DEPRECATED]
  E. Astrophysical harvesting from a magnetar that has accumulated
     primordial monopoles over Myr. [DEPRECATED]

Observational anchors:
  - Parker bound: F < 1e-15 /cm^2/s/sr (galactic field decay; Parker 1970)
  - MACRO direct (slow GUT): F < 1.4e-16 /cm^2/s/sr at 90% CL
    (Ambrosio et al., hep-ex/0207020)
  - IceCube relativistic: F < 2e-19 /cm^2/s/sr (Aartsen et al., 2110.04527)
  - MoEDAL Schwinger heavy-ion 2024: m_M > 80 GeV for charge 2-45 g_D
    (PRL 133, 071803; arXiv:2402.15682)

DESIGN_SUMMARY.md §7.5.1.
"""
import numpy as np

def banner(s):
    print("\n" + "="*78); print(s); print("="*78)

# Constants
hbar = 1.054_571_817e-34
c    = 2.997_924_58e8
G    = 6.6743e-11
mu0  = 4*np.pi*1e-7
e_q  = 1.602_176_634e-19
me   = 9.109_383_7e-31
GeV_J = 1.602_176_634e-10

# Reference monopole mass (BPS at GUT)
m_M_GeV = 1.77e17
m_M_kg = m_M_GeV * GeV_J / c**2

# Required: 1 monopole-antimonopole pair to seed Phase-2 breeding
N_seed_target = 1   # pairs

# =============================================================================
# OPTION A: PASSIVE CAPTURE FROM PRIMORDIAL FLUX
# =============================================================================
banner("OPTION A: PRIMORDIAL-FLUX CAPTURE (MAGNETIC-FLUX-CONCENTRATOR SAIL)")

# Strongest direct limit for slow GUT monopoles (MACRO 2002):
F_MACRO = 1.4e-16   # /cm^2/s/sr at 90% CL
F_Parker = 1e-15    # /cm^2/s/sr (galactic-field-decay theory limit)

print(f"  Reference fluxes:")
print(f"    Parker theoretical:           F < {F_Parker:.1e} /cm^2/s/sr")
print(f"    MACRO direct (90% CL):        F < {F_MACRO:.1e} /cm^2/s/sr")
print()

# Galactic monopole velocity (gravitational acceleration through galactic
# potential): v ~ 10^-3 c (300 km/s, similar to dark-matter velocity)
beta_gal = 1e-3

# Capture sail: a superconducting magnetic-flux concentrator funnels incoming
# monopoles to a central Meissner trap.  For a monopole with magnetic charge
# g_D entering a converging field, the magnetic force radial component
# accelerates it to the trap.  Capture efficiency ~ 1 for any monopole
# entering the funnel mouth.
# Effective face area = projected area; integrate over upper hemisphere.

def capture_count(F_flux, A_face_m2, T_year):
    """Expected captures from isotropic flux F (in /cm^2/s/sr)."""
    A_face_cm2 = A_face_m2 * 1e4
    T_s = T_year * 365.25*86400
    # Effective solid angle: monopoles come from a hemisphere (above sail);
    # geometry factor = pi sr (face normal direction averaging)
    sr_effective = np.pi
    return F_flux * A_face_cm2 * T_s * sr_effective

print(f"  Capture rate examples (effective solid angle pi sr):")
print(f"  {'Face area':>12s} {'Time':>8s} {'F=Parker':>12s} {'F=MACRO':>12s}"
      f" {'F=1e-3 MACRO':>16s}")
for A_m2 in [10, 100, 1000, 10000, 100000]:
    for T_yr in [10, 30, 100]:
        N_park = capture_count(F_Parker, A_m2, T_yr)
        N_macro = capture_count(F_MACRO, A_m2, T_yr)
        N_low = capture_count(F_MACRO*1e-3, A_m2, T_yr)
        print(f"  {A_m2:>10d} m^2 {T_yr:>6d} yr {N_park:>12.2e}"
              f" {N_macro:>12.2e} {N_low:>16.2e}")

print()
print("  Conclusion:")
print("    - At Parker-bound flux: a 100 m^2 sail catches ~ 1 pair / 10 yr.")
print("    - At MACRO-bound flux (1.4e-16): a 1000 m^2 sail catches ~1 pair / 10 yr.")
print("    - At 1000x sub-MACRO flux: need ~10^5 m^2 sail or centuries.")
print("    - The actual primordial flux is UNKNOWN below MACRO; could be zero.")
print("    - For an active mission, ~1 km^2 sail for 30 yr is a baseline that")
print("      gives ~100 expected pairs at the MACRO limit, ~0.1 at 10^-3 of MACRO.")

# Sail mass cost: superconducting flux concentrator at ~kg/m^2 areal density
# (cf. solar sail concepts) -> 1 km^2 ~ 10^6 kg = 1000 tonnes.  Roughly the
# mass of the drive's own shell.  Engineering tractable.
print(f"\n  Sail mass cost (1 km^2 at 1 kg/m^2 superconductor): ~1000 t")

# =============================================================================
# OPTION B (PRIMARY): AMBJORN-OLESEN ACCELERATOR
# =============================================================================
banner("OPTION B (PRIMARY): ~2000 km RING at 1000 T -> AO-THRESHOLD COLLISIONS")

# B_AO threshold: B_AO = m_W^2 c^2 / (e hbar)  (magnetic dual-Schwinger)
m_W_GeV = 80.379
m_W_kg = m_W_GeV*GeV_J/c**2
B_AO = m_W_kg**2 * c**2 / (e_q*hbar)
print(f"  B_AO = m_W^2 c^2 / (e hbar) = {B_AO:.2e} T")
print(f"        (cross-check from B_Schwinger_e * (m_W/m_e)^2 = "
      f"{4.41e9 * (m_W_GeV*1e9/0.511e6)**2:.2e} T)")

# Accelerator parameters to reach B_AO at Pb-Pb collision point
print()
print("  ACCELERATOR SPECIFICATION (to produce Cho-Maison monopole pairs):")
eps0 = 8.854e-12
Z_Pb = 82
A_Pb = 208
m_u_kg = 1.66054e-27
m_Pb_kg = A_Pb * m_u_kg
r_nuclear_m = 7e-15

# Required gamma for B(r_nuclear) = B_AO:
gamma_threshold = B_AO * 4*np.pi*eps0 * c * r_nuclear_m**2 / (Z_Pb * e_q)
print(f"    Pb-208 nucleus (Z = {Z_Pb}), r_nuclear = {r_nuclear_m*1e15:.0f} fm")
print(f"    Required gamma for B(r_nuc) = B_AO:")
print(f"      gamma_threshold = B_AO * 4 pi eps0 * c * r^2 / (Z e) = "
      f"{gamma_threshold:.2e}")
print(f"    Per-nucleon energy: gamma * m_N c^2 = "
      f"{gamma_threshold * 0.938:.2e} GeV/nucleon = "
      f"{gamma_threshold * 0.938 / 1e6:.2f} PeV/nucleon")
print(f"    Per-Pb-nucleus energy: {gamma_threshold * 0.938 * A_Pb / 1e9:.2f} EeV")

# Bending radius at B_dip = 1000 T
B_dip_T = 1000.0
p_Pb = gamma_threshold * m_Pb_kg * c    # ultrarelativistic limit
R_bend_m = p_Pb / (Z_Pb * e_q * B_dip_T)
C_bend_m = 2*np.pi * R_bend_m
C_total_m = C_bend_m / 0.7  # 70% bending fraction (LHC-like)
print(f"    Beam momentum p = gamma m c = {p_Pb:.2e} kg m/s")
print(f"    Bending radius at B_dip = {B_dip_T:.0f} T:  R = p/(ZeB) = {R_bend_m/1e3:.0f} km")
print(f"    Bending circumference 2 pi R = {C_bend_m/1e3:.0f} km")
print(f"    Total ring (~70% bending fraction): C = {C_total_m/1e3:.0f} km")

# Stored magnetic energy in dipoles
beam_pipe_A_m2 = 1e-2 * 1e-2   # 10 cm x 10 cm beam pipe (generous)
B_dip_energy_density = B_dip_T**2 / (2*mu0)
total_dipole_volume = C_bend_m * beam_pipe_A_m2
total_stored_energy = B_dip_energy_density * total_dipole_volume
print(f"    Beam-pipe cross-section: 10 cm x 10 cm = {beam_pipe_A_m2*1e4:.0f} cm^2")
print(f"    Dipole field-energy density at 1000 T: "
      f"{B_dip_energy_density:.2e} J/m^3")
print(f"    Total dipole volume: {total_dipole_volume:.2e} m^3")
print(f"    Stored magnetic energy: {total_stored_energy/1e12:.1f} TJ "
      f"= {total_stored_energy/5e10:.0f} x LHC")

# Hoop stress at 1000 T (same materials problem as drive bore throat)
hoop_stress_Pa = B_dip_T**2 / (2*mu0)
print(f"    Hoop stress at 1000 T: B^2/(2 mu0) = {hoop_stress_Pa/1e9:.0f} GPa")
print(f"    (Same materials problem as drive's own bore throat -- §9 item 12)")

# Yield rate at threshold
print()
print("  YIELD RATE:")
# Rate per (V*t) at AO threshold
inv_lambda_W_m = m_W_GeV*GeV_J / (hbar*c)
R_per_V_at_threshold = c * inv_lambda_W_m**4
print(f"    Rate per (V*t) at AO: c (m_W/hbar c)^4 = {R_per_V_at_threshold:.2e} /m^3/s")

# Volume above threshold per collision: ~ r_nuclear^2 * (r_nuclear/gamma)
# Duration: r_nuclear/(gamma c)
V_above = r_nuclear_m**2 * r_nuclear_m / gamma_threshold     # cube of nuclear scale, contracted
t_above = r_nuclear_m / (gamma_threshold * c)
Vt_above = V_above * t_above
pairs_per_collision = R_per_V_at_threshold * Vt_above
print(f"    V above threshold per collision: ~{V_above:.2e} m^3")
print(f"    Duration above threshold: ~{t_above:.2e} s")
print(f"    V*t per collision: ~{Vt_above:.2e} m^3 s")
print(f"    Expected pairs per collision near threshold: ~{pairs_per_collision:.2e}")
print(f"    (operating above threshold by factor of few gives O(1) pairs/collision)")
print()
print(f"  For 1 captured pair (sufficient to seed Phase-2 breeding):")
print(f"    Collisions needed: ~{1/pairs_per_collision:.2e}")
print(f"    At LHC heavy-ion luminosity (~10^3 events/s): ~"
      f"{1/(pairs_per_collision*1e3):.2e} s = "
      f"{1/(pairs_per_collision*1e3)/86400:.2e} days")

print()
print("  SUMMARY: This is the design's PRIMARY seed-production path (§7.5.1).")
print("  Engineering category: planetary-megastructure scale; uses same 1000 T")
print("  materials problem as the drive's own bore throat.  Once built, seed")
print("  acquisition is milliseconds-to-seconds of running time.")
print()
print("  Note: Produces Cho-Maison electroweak monopoles (mass ~5 TeV), NOT")
print("  GUT 't Hooft-Polyakov monopoles (which require B ~ 10^41 T, twenty-one")
print("  OOM beyond AO threshold).  Design substitutes BPS-collapse formation")
print("  with primordial-BH-capture + magnetic-charging (DESIGN_SUMMARY.md §7).")

# Above B_AO the W condensate becomes classically unstable.  Above the related
# threshold for 't Hooft-Polyakov monopoles (which is parametrically the same),
# the rate per volume per time is essentially set by the geometry:
#   R/V ~ c (m_W c^2 / hbar c)^4   for B/B_AO ~ O(1)
inv_lambda_W_m = m_W_GeV*GeV_J / (hbar*c)
R_per_V = c * inv_lambda_W_m**4
print(f"  Rate per volume per time at B ~ B_AO: R/V ~ c (m_W/hbar c)^4 "
      f"= {R_per_V:.2e} /m^3/s")
# A tiny volume (1 fm^3) for 1 ms above B_AO produces enormous numbers
V_test = (1e-15)**3
T_test = 1e-3
N_per_cycle = R_per_V * V_test * T_test
print(f"  Test: 1 fm^3 above threshold for 1 ms -> {N_per_cycle:.2e} pairs")
print()
print("  This is the same formula that gives ~ 10^32 GUT-scale pairs per cycle if")
print("  reachable.  The challenge is ENGINEERING B > 1e20 T over ANY volume * time.")
print()
print("  Current laboratory and astrophysical anchor fields:")
print("    Sustained lab:       ~ 45 T")
print("    Pulsed lab:          ~ 1e3 T (millisecond)")
print("    Strongest neutron star (magnetar surface): ~ 1e11 T")
print("    Peak heavy-ion (Pb-Pb 2.76 TeV at LHC): ~ 1e16 T transiently")
print(f"    Required B_AO threshold: {B_AO:.0e} T")
print(f"    Gap to threshold (from LHC heavy-ion peak): ~ "
      f"{np.log10(B_AO/1e16):.0f} OOM")
print(f"    Gap to threshold (from magnetar surface):  ~ "
      f"{np.log10(B_AO/1e11):.0f} OOM")
print()
print("  Tractability: would require fundamentally new field-generation techniques,")
print("  possibly via cosmic-string-mimicking nanostructured composites or")
print("  Schwarzschild-like gravitational field-concentration.  Not currently a")
print("  research program; the existence of monopoles (assumption #2) is precisely")
print("  what would motivate such a program.")

# =============================================================================
# OPTION C: HEAVY-ION SCHWINGER PRODUCTION (LHC and beyond)
# =============================================================================
banner("OPTION C: HEAVY-ION SCHWINGER PRODUCTION AT CURRENT/FUTURE COLLIDERS")

# MoEDAL 2024 (arXiv:2402.15682) excluded Schwinger monopoles up to 80 GeV
# with charges 2-45 g_D in Pb-Pb at 2.76 TeV.  The peak transient B ~ 1e16 T
# in Pb-Pb gives Schwinger pair production rate ~ exp(-pi m_M^2/(g_D B)).
B_LHC_HI = 1e16    # T peak transient in Pb-Pb at LHC
g_D_SI = 6.626e-34/(2*mu0*e_q)
def schwinger_exponent_GeV(m_M_GeV_local, B_T):
    """Affleck-Manton dual-Schwinger exponent pi m^2 c^3/(g_D B hbar), m_M in GeV, B in T.

    Derivation: in natural units, S_inst = pi m^2/(g_M B).  Restoring c and hbar
    such that the result is dimensionless: S = pi (m c^2)^2 / (g_M B hbar c).
    With m_M c^2 = m_J [J], that's pi m_J^2 / (g_D B hbar c).
    Cross-check: at m_M = m_e and B = B_Schwinger = m_e^2 c^3/(e hbar) = 4.41e9 T,
    the exponent should equal pi.
    """
    m_J = m_M_GeV_local * GeV_J
    return np.pi * m_J**2 / (g_D_SI * B_T * hbar * c)

print(f"  Schwinger suppression exp(-pi m_M^2/(g_D B)) at B = {B_LHC_HI:.0e} T:")
print(f"  {'m_M [GeV]':>12s} {'exponent':>15s} {'suppression':>15s}")
for mass in [80, 1000, 10000, 1e6, 1e9, 1e12, 1e15, m_M_GeV]:
    exp_val = schwinger_exponent_GeV(mass, B_LHC_HI)
    sup = np.exp(-exp_val) if exp_val < 700 else 0
    print(f"  {mass:>12.1e} {exp_val:>15.2e} "
          f"{sup if sup > 0 else f'<{np.exp(-700):.0e}':>15}")

print()
print("  Conclusion:")
print("    - LHC heavy-ion: only m_M < ~100 GeV potentially within Schwinger reach.")
print("    - Future colliders (FCC at 100 TeV) push peak B by factor ~10-30, but")
print("      still need m_M << TeV for unsuppressed production.")
print("    - GUT-scale monopoles (m_M ~ 1e17 GeV) cannot be Schwinger-produced at")
print("      any current or proposed collider; the dual-Schwinger exponent is ~10^29.")
print()
print("  Alternative: Cho-Maison electroweak monopoles at ~TeV mass (NOT GUT-scale,")
print("  but they carry magnetic charge and could in principle play the BH-charging")
print("  role IF the design's BPS-collapse mechanism is replaced by primordial-BH")
print("  capture.  See note below.")

# =============================================================================
# OPTION D: μg PRIMORDIAL BH HAWKING-EMIT MONOPOLES
# =============================================================================
banner("OPTION D: PRIMORDIAL μg BH HAWKING-EMIT MONOPOLES")

# A BH at temperature kT > m_M c^2 / e_thermal would thermally emit monopoles.
# kT > m_M c^2 / 3 for non-Boltzmann-suppressed emission.
# Required mass:
M_for_kT = hbar * c**3 / (8*np.pi * G * m_M_GeV*GeV_J/3)
print(f"  For kT ~ m_M c^2 / 3, required BH mass = {M_for_kT:.2e} kg = "
      f"{M_for_kT*1e9:.2e} ug = {M_for_kT*1e6:.2e} mg")
# Hawking lifetime at this mass:
tau_BH = M_for_kT**3 * G**2 / (3 * hbar * c**4 * 4e-3)   # rough f ~ 4e-3 at very high T
print(f"  Hawking lifetime: tau ~ {tau_BH:.2e} s")

print()
print("  Conclusion:")
print(f"    - Such ultra-light BHs would have evaporated within {tau_BH*1e30:.1e} ys")
print(f"      of formation in the early universe.")
print("    - Not present in the observable universe today.")
print("    - Engineering creation requires Planck-scale energy concentration,")
print("      which is itself extreme tech.")

# =============================================================================
# OPTION E: ASTROPHYSICAL HARVESTING (MAGNETAR)
# =============================================================================
banner("OPTION E: HARVESTING FROM ACCUMULATED-MONOPOLE NEUTRON STAR (MAGNETAR)")

# A magnetar of radius 10 km with surface B ~ 1e11 T attracts incoming
# primordial monopoles.  Over Myr, accumulated count:
F_assumed = 1e-17    # /cm^2/s/sr (a few orders below MACRO -- "realistic")
A_NS_cm2 = 4*np.pi*(1e6)**2   # 10 km radius, total surface area
T_acc_s = 1e6 * 365.25*86400   # 1 Myr
N_acc = F_assumed * A_NS_cm2 * T_acc_s * 4*np.pi   # isotropic accumulation
print(f"  Magnetar parameters:")
print(f"    surface B          ~ 1e11 T")
print(f"    surface area       = 4 pi (10 km)^2 = {A_NS_cm2:.2e} cm^2")
print(f"    accumulation time  ~ 1 Myr = {T_acc_s:.2e} s")
print(f"    assumed flux       = {F_assumed:.0e} /cm^2/s/sr (3 OOM below MACRO)")
print(f"  Accumulated monopole count: {N_acc:.2e}")
print()
print(f"  This is ~ 10^9 x our design requirement (one pair).  Magnetars store far")
print(f"  more monopoles than we need IF the primordial flux is at the level assumed.")
print()
print("  Engineering tractability:")
print(f"    - Distance to nearest known magnetar (SGR 1806-20): ~50,000 ly")
print(f"    - Tidal forces near magnetar: ~10^11 g at 100 km altitude (lethal)")
print(f"    - Radiation environment: 10^11 T B-field plus X-ray flares")
print(f"    - Extraction mechanism: speculative; would require superconducting")
print(f"      'fishing rod' immersed in the NS magnetosphere to electromagnetically")
print(f"      pull off accumulated monopoles. No literature on extraction methods.")
print(f"    - This is a Type-III-civilization option, not near-term feasible.")

# =============================================================================
# SUMMARY TABLE
# =============================================================================
banner("SUMMARY: COMPARISON OF SEED-PRODUCTION OPTIONS")

print(f"  Option            Mechanism                         Tractability   "
      f"Time to first pair")
print(f"  --------------    ------------------------------    -----------    "
      f"-------------------")
print(f"  A. Capture sail   Primordial flux + mag funnel      Engineering    "
      f"10-1000 yr (flux-dep.)")
print(f"  B. Ambjorn-Olesen Lab B > 1e20 T classical          Future tech    "
      f"~ ms once threshold reached")
print(f"  C. Schwinger HI   Heavy-ion peak B at LHC/FCC       Now (lower-m)  "
      f"~ runs (TeV-mass only)")
print(f"  D. μg PBH         Hawking emission near GUT-T        Not feasible   "
      f"Need to MAKE the BH first")
print(f"  E. Magnetar       Harvest accumulated monopoles      Type III civ   "
      f"~ century just to reach")
print()
print("  PRIMARY PATH (DESIGN COMMITTED):  Option B (Ambjorn-Olesen accelerator).")
print("    - ~2000 km ring with 1000 T sustained dipoles (same materials problem as")
print("      drive's own bore throat).")
print("    - Pb-Pb at 25 PeV/nucleon (gamma ~ 1.4e7) reaches B_AO at the collision")
print("      point; W-condensate instability produces Cho-Maison electroweak")
print("      monopole pairs classically (no exponential suppression).")
print("    - Once built, ~1 captured pair per ~ms of running.")
print("    - Substitutes: GUT 't Hooft-Polyakov -> Cho-Maison; BPS-collapse formation")
print("      -> primordial-BH capture and magnetic charging.")
print()
print("  FALLBACK PATH:  Option A (passive primordial-flux capture) as backup.")
print("    - 1 km^2 superconducting sail at L1, 30 yr, Meissner-trap detection.")
print("    - Yield is uncertain (empirical bound on flux is tightening; could be 0).")
print("    - Useful as a low-cost parallel mission while AO accelerator is built.")
print()
print("  DEPRECATED PATHS: Options C (LHC Schwinger is sub-AO), D (ug PBH cannot")
print("    exist), E (magnetar harvesting requires the drive itself).")
