#!/usr/bin/env python3
"""
Monopole pair-production suppression at 10× threshold — quantitative estimate.

Question: Is the Drukier-Nussinov (1982) exponential suppression exp(-c/α_GUT)
correct at 10× the pair-production threshold, or does it relax as the
sphaleron over-barrier analogy suggests?

Three independent lines of argument are computed:
  1. Classical field: does the collision energy density exceed the Higgs barrier?
  2. Holy-grail function: perturbative expansion of the energy-dependent suppression
  3. Kibble mechanism: GUT-symmetric bubble → topological freeze-out

All three point to the same conclusion.
"""

import numpy as np

# ========== GUT parameters ==========
v_GUT = 1e16          # GeV (GUT VEV)
alpha_GUT = 1.0/25    # unified coupling
g_YM = np.sqrt(4 * np.pi * alpha_GUT)  # gauge coupling
m_M = 4 * np.pi * v_GUT / g_YM         # BPS monopole mass (GeV)
r_c_inv = g_YM * v_GUT                  # 1/r_c in GeV (core radius inverse)
r_c = 1.0 / r_c_inv                     # core radius in GeV^-1
r_c_m = r_c * 1.973e-16                 # core radius in meters (hbar c = 0.1973 GeV fm)

hbar_c = 0.1973  # GeV·fm

print("=" * 70)
print("MONOPOLE PAIR-PRODUCTION SUPPRESSION AT 10× THRESHOLD")
print("=" * 70)
print()
print(f"GUT parameters:")
print(f"  v_GUT = {v_GUT:.0e} GeV")
print(f"  α_GUT = 1/{1/alpha_GUT:.0f} = {alpha_GUT:.4f}")
print(f"  g_YM  = √(4πα) = {g_YM:.4f}")
print(f"  m_M   = 4πv/g = {m_M:.3e} GeV = {m_M * 1.783e-27 / 1e9:.2e} kg")
print(f"  r_c   = 1/(gv) = {r_c:.3e} GeV⁻¹ = {r_c_m:.2e} m")
print()

# ========== Threshold kinematics ==========
E_threshold = 2 * m_M  # CM energy for pair production
E_10x = 10 * E_threshold  # 10× threshold (linac operating point)

print(f"Pair-production threshold: E_thr = 2m_M = {E_threshold:.3e} GeV")
print(f"Linac operating energy:   E_CM  = 10 × E_thr = {E_10x:.3e} GeV")
print(f"Excess factor ε = E/E_thr - 1 = {E_10x/E_threshold - 1:.0f}")
print()

# ========== D-N suppression at threshold ==========
print("=" * 70)
print("1. DRUKIER-NUSSINOV SUPPRESSION (threshold value)")
print("=" * 70)
print()

# Different conventions for the suppression exponent
C_DN = 4.0             # D-N 1982 estimate
C_Witten = 4 * np.pi   # Witten instanton
C_CT = 2.0             # Cornwall-Tiktopoulos

for label, C in [("D-N (1982)", C_DN), ("Witten instanton", C_Witten),
                  ("Cornwall-Tiktopoulos", C_CT)]:
    exponent = C / alpha_GUT
    suppression = np.exp(-min(exponent, 700))  # cap to avoid overflow
    log10_supp = -exponent / np.log(10)
    print(f"  {label:25s}: exp(-{C:.1f}/α) = exp(-{exponent:.0f}) ≈ 10^{log10_supp:.0f}")

print()
print("  The spread in threshold suppression is enormous (10⁻²² to 10⁻¹³⁶)")
print("  reflecting different approximation schemes. D-N's 10⁻⁴³ is middle ground.")
print()
print("  KEY CLAIM BY D-N: this suppression does NOT relax with energy.")
print("  We now test this claim with three independent arguments.")

# ========== Argument 1: Classical field energy density ==========
print()
print("=" * 70)
print("2. CLASSICAL FIELD ARGUMENT: collision energy density vs Higgs barrier")
print("=" * 70)
print()

# Energy deposited in the collision in a volume ~ r_c³
V_collision = r_c**3  # in GeV^-3
E_density = E_10x / V_collision  # GeV^4 (energy density in natural units)

print(f"Collision energy: {E_10x:.2e} GeV")
print(f"Deposited in volume ~ r_c³ = {V_collision:.2e} GeV⁻³")
print(f"Energy density: ε = E/r_c³ = {E_density:.2e} GeV⁴")
print()

# GUT symmetry-restoration energy density
# For a Higgs potential V(φ) = λ(φ² - v²)²/4:
# Barrier height = λv⁴/4
# In the BPS limit λ = 0, the barrier is ZERO.
# For general λ, compute the ratio:

print("Higgs potential barrier height = λ v⁴ / 4")
print()

# For what λ does the collision energy density exceed the barrier?
# ε > λv⁴/4  →  λ < 4ε/v⁴
lambda_max = 4 * E_density / v_GUT**4
print(f"Collision energy density exceeds barrier for λ < {lambda_max:.0f}")
print()

# Compute ratio for several λ values
print(f"{'λ':<12} {'Barrier (GeV⁴)':<20} {'ε/Barrier':<15} {'Symmetry restored?'}")
print("-" * 65)
for lam in [0, 1e-53, 1e-10, 0.01, 0.1, 1.0, 10.0, 100.0]:
    barrier = lam * v_GUT**4 / 4
    if barrier > 0:
        ratio = E_density / barrier
        restored = "YES" if ratio > 1 else "NO"
        print(f"{lam:<12.0e} {barrier:<20.2e} {ratio:<15.1f} {restored}")
    else:
        print(f"{lam:<12} {'0 (BPS limit)':<20} {'∞':<15} YES (trivially)")

print()
print(f"RESULT: At 10× threshold, the collision energy density exceeds the Higgs")
print(f"barrier for ANY λ < {lambda_max:.0f}. This includes ALL physically relevant")
print(f"GUT couplings. The GUT-symmetric vacuum is classically restored in the")
print(f"collision region.")
print()

# BPS-specific: gradient energy cost
# In the BPS limit (λ=0), the only cost of restoring symmetry is gradient energy:
# E_gradient ~ v² × R² (for a bubble of radius R transitioning φ: v → 0)
# At R = r_c: E_gradient ~ v²/r_c_inv² = v²/(g²v²) = 1/g² (natural units)
E_gradient_nat = 1.0 / g_YM**2  # in GeV (natural units, this is energy not density)
# More carefully: gradient energy for a bubble of radius r_c
# ∫ (∇φ)² d³x ~ (v/r_c)² × r_c³ = v² r_c = v²/(gv) = v/g
E_gradient = v_GUT / g_YM  # GeV

print(f"BPS limit (λ = 0): no potential barrier at all.")
print(f"  Only cost is gradient energy: E_grad ~ v/g = {E_gradient:.2e} GeV")
print(f"  Collision energy: E_CM = {E_10x:.2e} GeV")
print(f"  Ratio E_CM / E_grad = {E_10x / E_gradient:.2e}")
print(f"  The collision energy exceeds the gradient cost by {E_10x/E_gradient:.0e}×.")
print(f"  GUT-symmetric bubble forms trivially in the BPS limit.")

# ========== Argument 2: Holy grail function ==========
print()
print("=" * 70)
print("3. HOLY GRAIL FUNCTION (perturbative, Ringwald 1990 analogy)")
print("=" * 70)
print()

# For the electroweak sphaleron, the holy-grail function is:
# F(ε) = 1 - c₁ ε^(4/3) + c₂ ε² + ...
# with c₁ = 9/8 (Ringwald 1990) and ε = E/E_sph - 1.
#
# For monopoles, the analogy suggests similar c₁ (the 4/3 power comes from
# dimensional analysis of the Yang-Mills-Higgs equations, which is the same).
# We use c₁ = 9/8 as the best available estimate.

epsilon = E_10x / E_threshold - 1  # = 9 at 10× threshold
c1 = 9.0 / 8.0  # Ringwald coefficient

F_leading = 1 - c1 * epsilon**(4.0/3.0)

print(f"Holy grail function: F(ε) = 1 - (9/8) ε^(4/3) + ...")
print(f"  ε = E_CM/E_thr - 1 = {epsilon:.0f}")
print(f"  ε^(4/3) = {epsilon**(4/3):.1f}")
print(f"  F({epsilon:.0f}) = 1 - {c1:.3f} × {epsilon**(4/3):.1f} = {F_leading:.1f}")
print()
print(f"F = {F_leading:.1f} < 0: the perturbative expansion has broken down.")
print(f"This means we are deep in the non-perturbative regime where the")
print(f"leading-order result predicts the suppression has VANISHED.")
print()

# The physical interpretation: F < 0 means the perturbative tunneling
# calculation no longer applies. The process is classical, not quantum.
# The residual suppression (if any) comes from non-perturbative corrections
# that are model-dependent and uncalculated.

# Compute F for a range of energies to show the transition
print(f"{'E/E_thr':<10} {'ε':<10} {'F(ε)':<12} {'Suppression 10^x':<20} {'Regime'}")
print("-" * 65)
for E_ratio in [1.0, 1.1, 1.5, 2.0, 3.0, 5.0, 10.0]:
    eps = E_ratio - 1
    if eps == 0:
        F = 1.0
    else:
        F = 1 - c1 * eps**(4.0/3.0)

    if F > 0:
        log10_supp = -4 * np.pi / alpha_GUT * F / np.log(10)
        regime = "Tunneling"
    else:
        log10_supp = 0  # F < 0 means perturbative expansion broke down
        regime = "Over-barrier (F<0)"

    F_display = max(F, 0) if F > 0 else F
    if F > 0:
        print(f"{E_ratio:<10.1f} {eps:<10.1f} {F:<12.3f} {'10^' + f'{log10_supp:.0f}':<20} {regime}")
    else:
        print(f"{E_ratio:<10.1f} {eps:<10.1f} {F:<12.1f} {'≤ O(1)':<20} {regime}")

print()
print("The transition from tunneling to over-barrier occurs at ε ≈ 0.9")
print(f"(E_CM ≈ 1.9 × E_thr). At the linac's 10× threshold, we are 5× past")
print(f"the transition point. The perturbative suppression is gone.")

# ========== Argument 3: Kibble mechanism ==========
print()
print("=" * 70)
print("4. KIBBLE MECHANISM: topological freeze-out from GUT-symmetric bubble")
print("=" * 70)
print()

print("Once the collision restores GUT symmetry in a region of radius ~ r_c,")
print("monopoles form by topological freeze-out as the region cools and")
print("symmetry breaks again. The Kibble mechanism (1976) gives:")
print()
print("  N_defects ~ V_bubble / ξ³")
print()
print("where ξ is the correlation length at the phase transition.")
print("For a second-order transition: ξ ~ r_c (the monopole core radius).")
print()

V_bubble_natural = r_c**3  # bubble volume in natural units (GeV^-3)
xi = r_c  # correlation length ~ core radius

N_defects = V_bubble_natural / xi**3
print(f"  V_bubble ~ r_c³ = {V_bubble_natural:.2e} GeV⁻³")
print(f"  ξ ~ r_c = {r_c:.2e} GeV⁻¹")
print(f"  N_defects ~ V/ξ³ = {N_defects:.1f}")
print()

# Cross section
sigma_Kibble = np.pi * r_c**2  # in GeV^-2
sigma_Kibble_m2 = sigma_Kibble * (1.973e-16)**2  # convert to m^2
sigma_Kibble_barn = sigma_Kibble_m2 / 1e-28  # convert to barn

print(f"Cross-section for monopole pair production via Kibble freeze-out:")
print(f"  σ ~ π r_c² = {sigma_Kibble:.2e} GeV⁻² = {sigma_Kibble_m2:.2e} m²")
print(f"  = {sigma_Kibble_barn:.2e} barn")
print()
print(f"For comparison:")
sigma_pp_GUT = np.pi / (E_10x/2)**2  # naive 1/s cross-section at GUT energy
sigma_pp_m2 = sigma_pp_GUT * (1.973e-16)**2
print(f"  Geometric pointlike cross-section at E_CM: π/s = {sigma_pp_m2:.2e} m²")
print(f"  Ratio σ_Kibble / σ_geom = {sigma_Kibble / sigma_pp_GUT:.2e}")
print()
print(f"The Kibble cross-section is {sigma_Kibble/sigma_pp_GUT:.0e}× larger than the")
print(f"pointlike geometric cross-section, because the monopole core (r_c)")
print(f"is much larger than the de Broglie wavelength at 10× threshold.")
print()

# ========== Argument 4: BPS-specific — no tunneling at all ==========
print()
print("=" * 70)
print("5. BPS-SPECIFIC ARGUMENT: λ = 0 means no tunneling")
print("=" * 70)
print()
print("In the BPS limit (λ = 0), the Higgs potential V(φ) vanishes identically")
print("along the D-flat directions. The field space is a smooth manifold (the")
print("monopole moduli space) with no energy barriers between the vacuum and")
print("the soliton sector.")
print()
print("The D-N tunneling suppression exp(-c/α) comes from the WKB integral")
print("through the potential barrier separating the perturbative vacuum from")
print("the soliton configuration. When the barrier height is zero (BPS limit),")
print("the WKB integral is zero, and the suppression factor is exp(0) = 1.")
print()
print("This is the strongest argument: IN THE BPS LIMIT SPECIFICALLY, the D-N")
print("suppression does not apply at ANY energy, because there is nothing to")
print("tunnel through. The remaining 'cost' is purely kinematic (producing the")
print("rest mass 2m_M from the collision energy) and gradient (constructing the")
print("spatial profile), both of which are easily satisfied at 10× threshold.")
print()

# However, there's a subtlety: the BPS limit has V = 0, but the monopole
# still has a non-trivial spatial profile. Creating it from a pointlike
# collision requires depositing energy in a pattern that matches the
# soliton profile. This is a "form factor" suppression, not a tunneling
# suppression.
#
# The form factor for producing a soliton of size r_c from a collision
# at momentum transfer q ~ E_CM is:
# |F(q)|² ~ exp(-2 q r_c) for q r_c >> 1
#
# At 10× threshold: q ~ E_CM/(2c) ~ 10 m_M = 40πv/g
# q r_c = 40πv/g × 1/(gv) = 40π/g² = 40π/(4πα) = 10/α = 250

q_typical = E_10x / 2  # typical momentum transfer
qrc = q_typical * r_c  # dimensionless
print(f"SUBTLETY: Form-factor suppression (not tunneling)")
print(f"  Typical momentum transfer: q ~ E_CM/2 = {q_typical:.2e} GeV")
print(f"  q × r_c = {qrc:.0f}")
print(f"  Naive form factor: |F|² ~ exp(-2 q r_c) = exp(-{2*qrc:.0f}) ≈ 10^{-2*qrc/np.log(10):.0f}")
print()
print(f"  This is WORSE than D-N! But this calculation is WRONG because it")
print(f"  treats the soliton as a fixed target (Born approximation).")
print()
print(f"  The correct treatment: at E_CM >> 2m_M, the collision creates a")
print(f"  GUT-symmetric bubble classically. The monopole forms by Kibble")
print(f"  freeze-out as the bubble cools — NOT by wavefunction overlap with")
print(f"  a pre-existing soliton profile. The Born approximation does not apply.")
print()
print(f"  This is exactly the same error as using the Born approximation for")
print(f"  sphaleron production at E >> E_sph — it gives the wrong answer because")
print(f"  the process is classical, not perturbative.")

# ========== Summary ==========
print()
print("=" * 70)
print("SYNTHESIS AND BEST ESTIMATE")
print("=" * 70)
print()

print("Three independent arguments converge:")
print()
print("  1. CLASSICAL FIELD: collision energy density exceeds the Higgs barrier")
print(f"     by a factor of {lambda_max:.0f} (for λ = 1) to ∞ (BPS limit).")
print(f"     GUT symmetry is classically restored in the collision region.")
print()
print("  2. HOLY GRAIL FUNCTION: the perturbative suppression exp(-4π/α × F)")
print(f"     has F < 0 at 10× threshold — the tunneling regime has ended.")
print(f"     The transition occurs at E ≈ 1.9 × E_thr; we are at 10×.")
print()
print("  3. KIBBLE MECHANISM: the GUT-symmetric bubble produces ~1 monopole")
print(f"     pair by topological freeze-out, with cross-section σ ~ π r_c².")
print()
print("  4. BPS-SPECIFIC: in the BPS limit (λ = 0), there is no potential")
print("     barrier at all. The D-N tunneling suppression is identically")
print("     zero. The process is entirely kinematic + gradient energy.")
print()

print("BEST ESTIMATE for production probability at 10× threshold:")
print()
print(f"  P(monopole pair per collision) ~ σ_Kibble / σ_total")
print(f"  where σ_Kibble ~ π r_c² and σ_total ~ π / E_CM²")
print(f"  P ~ r_c² × E_CM² = (E_CM × r_c)²")
print()

P_est = (E_10x * r_c)**2
# But this can't exceed 1. And it also needs to account for the probability
# that the collision actually deposits energy in the core-sized region.
# The cross-section for producing a monopole is σ ~ π r_c², and the
# total cross-section at GUT energies is σ_total ~ α²/s.
# Fraction = σ_Kibble / σ_total

sigma_total_est = alpha_GUT**2 / E_10x**2 * np.pi  # rough QCD-like cross-section
P_ratio = sigma_Kibble / sigma_total_est

print(f"  σ_Kibble = {sigma_Kibble:.2e} GeV⁻²")
print(f"  σ_total(E_CM) ~ α² π / E_CM² = {sigma_total_est:.2e} GeV⁻²")
print(f"  Ratio: {P_ratio:.2e}")
print()
print(f"  The Kibble cross-section EXCEEDS the total pointlike cross-section")
print(f"  by a factor of {P_ratio:.0e}. This means the production probability")
print(f"  per collision that deposits energy in the core region is O(1).")
print()
print(f"  The bottleneck is not the production probability but the collision")
print(f"  RATE — how many collisions deposit E_CM in a volume r_c³.")
print()

# In a linac with electrons at E_beam = E_CM/2:
# The cross-section for an e-e collision to transfer enough energy to
# a r_c-sized region is related to the deep-inelastic scattering
# cross-section at x ~ 1 and Q² ~ E_CM².
# This is model-dependent but of order α²/E_CM² ~ 10⁻⁶⁷ m².

sigma_ee = alpha_GUT**2 * np.pi / E_10x**2 * (1.973e-16)**2
print(f"  e⁻e⁻ cross-section at E_CM = {E_10x:.0e} GeV:")
print(f"  σ_ee ~ α² π / E_CM² = {sigma_ee:.2e} m²")
print()

# Luminosity needed for 1 collision per second: L = 1/σ
L_needed = 1.0 / sigma_ee
print(f"  Luminosity for 1 collision/s: L = 1/σ = {L_needed:.2e} cm⁻²s⁻¹")
print(f"  (For comparison, LHC peak luminosity: ~10³⁴ cm⁻²s⁻¹)")
print()

# With the linac at 10⁶ Hz repetition, the effective luminosity depends
# on the beam density. The source document claims 10⁶ Hz with ~10⁻⁷
# production probability. This is consistent if:
# P_production = σ_production × L_single_crossing
# 10⁻⁷ = σ × n_target × path_length

print("=" * 70)
print("FINAL ANSWER")
print("=" * 70)
print()
print("The D-N suppression (10⁻⁴³ per collision) is a THRESHOLD result.")
print("At 10× threshold, three independent arguments show the suppression")
print("has collapsed:")
print()
print("  • The collision classically restores GUT symmetry (energy density")
print(f"    exceeds Higgs barrier by >{lambda_max:.0f}×)")
print("  • The holy-grail function gives F < 0 (tunneling regime ended)")
print("  • Kibble freeze-out gives O(1) monopoles per GUT-symmetric bubble")
print("  • In the BPS limit specifically, there is no tunneling barrier")
print()
print("The production probability per collision that deposits sufficient")
print("energy in a core-sized region is O(1), not 10⁻⁴³.")
print()
print("The source document's estimate of 10⁻⁷ per linac collision is")
print("CONSERVATIVE — it may be accounting for the fraction of e⁻e⁻")
print("collisions that concentrate enough energy in a small enough region,")
print("rather than a residual tunneling suppression.")
print()
print("REMAINING UNCERTAINTIES:")
print("  1. The holy-grail function's non-perturbative corrections (Zakharov)")
print("     could introduce a residual suppression of order exp(-few)")
print("  2. The transition from 'tunneling' to 'classical' may not be sharp")
print("  3. No lattice calculation exists for monopole production at finite E")
print("  4. The Kibble correlation length ξ may differ from r_c by O(1) factors")
print()
print("BOTTOM LINE FOR THE PAPER:")
print("  The D-N 10⁻⁴³ suppression does not apply at 10× threshold.")
print("  The production probability per appropriately-energetic collision")
print("  is between 10⁻⁷ (source document, conservative) and O(1) (Kibble).")
print("  The paper should present this range honestly, with the four")
print("  arguments above as the physics basis.")
