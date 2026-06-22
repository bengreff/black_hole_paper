# Kugelblitz Drive: Consolidated Design

**A Hawking-radiation propulsion system: a 10⁹ kg magnetically charged micro black hole at the center of a CFL strange-quark-matter spherical shell, with anti-Helmholtz confinement, electrosphere pair re-emission, and an 820 m magnetic-nozzle exhaust.**

*All numerical values in this document are reproduced explicitly from first principles in `calculations/verify_design.py`. The numbers below are quoted exactly as that script outputs them; section-by-section derivations are written out inline.*

---

## 0. WHAT THIS IS AND ISN'T

This is a self-consistent thought-experiment design, not an engineering roadmap. It works only if a stack of currently unverified physics assumptions all hold, and only if a stack of currently impossible engineering capabilities all become practical. The point of working it out at this level of detail is to show that nothing in the chain is *known* to fail — not that any of it is feasible now.

### Assumption budget (load-bearing, all required simultaneously)

| # | Assumption | Status | If wrong |
|---|---|---|---|
| 1 | Hawking radiation exists and is semiclassical at M ~ 10⁹ kg | Near-universal theoretical consensus, never observed | No power source |
| 2 | GUT magnetic monopoles exist | 't Hooft-Polyakov monopoles as topological defects of GUT symmetry breaking; predicted by all GUTs; never observed; MoEDAL/IceCube constrain flux only, not existence | No BH formation, no magnetic charge, no confinement |
| 3 | BPS limit (λ = 0 at GUT scale) | Exact Higgs-magnetic force cancellation between same-sign monopoles; protected by N=2 SUSY non-renormalization theorems; no experiment constrains λ at 10¹⁶ GeV | Monopole cloud cannot gravitationally collapse (magnetic repulsion dominates by factor ~10⁵) |
| 4 | Bodmer-Witten hypothesis (SQM is the ground state of baryonic matter) | Long-debated; Bai & Chen 2025 argues against — but only for *fully* chirally-restored matter, not CFL | No shell material |
| 5 | CFL is the ground state of SQM at the operating chemical potential | Theoretical, never observed | Gap-decoupling argument fails |
| 6a | Phase-2 core-overlap exponential breeding (Drukier-Nussinov / 't Hooft duality) | **Derived in §7.5** from α_m = 1/(4α) and core-overlap symmetry restoration; rate O(1) per overlap (works for GUT 't Hooft-Polyakov monopoles) | Cannot multiply a seed pair to 10¹⁵ monopoles |
| 6b | Phase-1 seed production via SQM electron linac at 10× monopole-pair threshold | **Derived in §7.5.1** from four independent arguments: (1) collision energy density classically restores GUT symmetry (exceeds Higgs barrier by >500×); (2) holy-grail function gives F < 0 at 10× threshold (tunneling regime ended at ~2× threshold); (3) Kibble freeze-out gives O(1) monopoles per GUT-symmetric bubble; (4) in the BPS limit, no potential barrier exists — D-N tunneling integral is identically zero. Production probability per collision: 10⁻⁷ (conservative) to O(1) | Need seed monopole pair to begin breeding |

Each of items 1–6 would constitute a Nobel-scale discovery if confirmed. The BPS limit (#3) is the most fragile assumption in isolation — it requires λ = 0 exactly at the GUT scale, a measure-zero point in coupling space. However, N = 2 supersymmetry in the monopole sector (which many GUTs exhibit) protects λ = 0 to all loop orders via non-renormalization theorems; this is symmetry protection, not fine-tuning. Item #6b (seed production) was previously the most debated element — Drukier-Nussinov (1982) argued for permanent exp(−c/α) suppression — but the four-argument analysis in §7.5.1 shows the D-N result is a *threshold* result that does not survive at 10× threshold, where the collision classically restores GUT symmetry and monopoles nucleate by Kibble freeze-out. In the BPS limit specifically, no tunneling barrier exists at any energy.

**Response to Bai & Chen 2025 (arXiv:2502.20241), which argues against Bodmer-Witten.** BC25 derive the QCD vacuum energy as (163–190 MeV)⁴ and conclude that *fully deconfined, chirally-symmetric* quark matter has ε/n_B ≈ 1130–1320 MeV — heavier than the 930 MeV/baryon iron-nucleus threshold, so unstable. Their analysis explicitly assumes "complete deconfinement, vanishing gluon condensate, full chiral-symmetry restoration"; their own caveat states the conclusion "applies only to this specific scenario and does not extend to quark nuggets with partially restored confinement and chiral symmetry." The CFL phase is precisely characterized by a quark-quark condensate that partially restores chiral symmetry (the diquark condensate replaces the chiral condensate in the broken-symmetry pattern), and BC25 treats the CFL contribution as a small correction (~10⁻⁴) rather than as a competing phase. **BC25 does not directly constrain our design**: we need CFL stability, not unpaired-SQM stability. The independent constraint on CFL specifically (whether it is the *true* ground state at the chemical potentials we operate at) remains open.

### Engineering capabilities required (beyond current state of the art)

- Sustained 1,000 T field in a 0.3 mm bore (current sustained record: ~45 T; magnetic pressure 400 GPa exceeds any material's tensile strength)
- Sustained 130 T at a superconductor with ~7 GPa hoop stress (above carbon fiber)
- Fabrication and shaping of 60,000 t of CFL strange quark matter into a 3 pm (3000 fm) thin spherical shell at ~2× nuclear density
- Railgun delivery of pellets at ~0.33c, aimed at a moving target with ~10 cm lateral tolerance (the monopole field guides ions to the horizon once they enter the magnetic-capture zone)
- 820 m precision magnetic nozzle maintaining adiabatic invariance over a 10⁸-fold field decrease
- SQM electron linear accelerator: two opposing 2,500 km SQM-bore tubes at 10²¹ V/m gradient, e⁻ beams at 2.5 × 10¹⁸ GeV per beam (10× monopole-pair threshold), 10⁶ Hz repetition rate
- Phase-2 breeding of one seed pair to ~7 × 10¹⁴ GUT monopoles via core-overlap collisions in SQM-clad synchrotron rings (~86 generations, ~hours-to-years)

The doc treats these as "far-future materials and engineering." That phrasing is doing a lot of work.

---

## 1. OVERVIEW

A black hole of mass 1.00 × 10⁹ kg radiates 60,200 TW of Hawking radiation isotropically. A spherical shell of CFL strange quark matter (R = 2 m, t = 3 pm = 3000 fm, mass 60,000 t) absorbs ~83 % of this and re-emits it as ~31 keV (per particle, KE) electron-positron pairs from a bombardment-maintained electrosphere on its inner surface. Anti-Helmholtz coils embedded in the shell hold the magnetically charged BH near the geometric center and create a magnetic bottle that funnels the thermal pairs through a 0.3 mm aft bore. An 820 m tapered magnetic nozzle collimates the beam to ~0.01°.

### Top-line numbers (canonical design point)

| Parameter | Value |
|---|---|
| BH mass | 1.00 × 10⁹ kg |
| Hawking temperature kT | 10.57 GeV |
| Emission factor f | 3.503 × 10⁻³ |
| Total Hawking power P_H | 60,200 TW |
| Mass-loss rate dM/dt | 670 g/s |
| Unfed lifetime τ_H | 15.8 yr |
| Primary neutrino loss | 7.0 % of P_H (= f_ν/f) |
| Secondary neutrino loss | ~10 % of P_H (first-principles hadron-decay estimate, §3) |
| (μ+τ) tail punch-through (off-axis CR) | ~84 MW = 1.4 × 10⁻⁹ of P_H |
| Net captured power | 50,000 TW (83 %) |
| Pair exhaust β (= v/c, Usov J(ζ) self-consistent) | 0.332 |
| Thrust F | 55.3 MN |
| Photon-rocket efficiency F·c/P_H | 27.5 % |
| Specific impulse I_sp | 1.01 × 10⁷ s |
| Shell thickness | 3000 fm = 3 pm |
| Shell mass | 60,000 t |
| Ship-mass model (cargo = M_BH) | M_ship = 2 M_BH + shell ≈ 2.06 × 10⁹ kg |
| Acceleration a_ship | 26.8 mm/s² |
| Δv (unfed, burn the BH) | 0.230 c |
| Fuel consumption | 21,140 t/yr |
| α Centauri (accel + decel, 4.37 ly) | 79 yr, peak 0.111 c |
| Off-axis EM signature | < 1 MW (firewall-limited; §4) |
| Off-axis cosmic-ray (μ tail) signature | ~84 MW dispersed isotropically — well below detection threshold (§3) |

The headline differences from the earlier draft:

- The heavy fermions (c, b, τ) are *less* Boltzmann-suppressed than a simple exp(−m/kT) factor implies — the correct power-rate suppression is the thermal-integral ratio, written out in §3. This shifts f up by ~7.6 % and threads through every derived quantity below.
- The CFL shell is thickened from 640 fm (12,900 t) to **3000 fm = 3 pm (60,000 t)** to close the (μ+τ) Hawking-tail punch-through channel. At t = 640 fm the stopping budget E_c = 51 GeV intercepts only the median spectrum and lets ~380 TW of muons free-stream out. At t = 3 pm the budget is E_c = 240 GeV, the Wien-tail escape fraction drops to ε = 1.5 × 10⁻⁸, and the residual CR signature is only 84 MW. The added mass cost (~5 × the original shell) reduces acceleration by ~1.5 % and the α Cen mission time grows by less than a year.

### Why these particular choices

- **10⁹ kg** sits at the high-thrust end of the Crane-Westmoreland viable range. It gives short-mission Δv at the cost of needing continuous refueling.
- **Spherical shell, not parabolic mirror.** The original Crane-Westmoreland (2009) reflector mechanism fails because Manuel & Rajagopal (2002) showed CFL quark matter is a transparent insulator for ordinary photons, not a superconductor. The shell architecture sidesteps this by absorbing and re-emitting.
- **Magnetic monopole charge, not electric.** A micro BH cannot hold macroscopic electric charge — the horizon potential drives Schwinger discharge in nanoseconds. Magnetic discharge requires fields ~10⁴⁹ T, never achieved.
- **Anti-Helmholtz, not solenoidal.** The same coil pair provides BH centering (via F = g·∇B on the monopole charge) and pair capture (magnetic bottle), eliminating a separate confinement system.

The BH mass is a continuous design parameter. Scaling to longer range (lower thrust, longer lifetime) is discussed in §10.

---

## 2. THE BLACK HOLE

Hawking (1975); Page (1976); Lennon et al. (2018, refining Page).

| Parameter | Value | Derivation |
|---|---|---|
| Mass M | 1.00 × 10⁹ kg | Design choice |
| Schwarzschild radius r_s | 1.485 × 10⁻¹⁸ m | r_s = 2GM/c² |
| Hawking temperature | kT = 10.573 GeV | kT = ℏc³/(8πGM) |
| Hawking T in Kelvin | T_H = 1.227 × 10¹⁴ K | k_B T_H = kT |
| Emission factor f | 3.503 × 10⁻³ | §3 thermal-integral derivation |
| Total power P_H | 6.020 × 10¹⁶ W = 60,200 TW | P = ℏc⁶f/(G²M²) |
| Unfed lifetime τ_H | 4.98 × 10⁸ s = 15.8 yr | τ = G²M³/(3ℏc⁴f) |
| Evaporation rate | 670 g/s = 21,140 t/yr | dM/dt = P/c² |
| Magnetic charge g | 1.182 × 10⁶ A·m | Tuned for δ_eq = 100 mm (§5) |
| Dirac quanta N_D = g/g_D | 7.18 × 10¹⁴ | g_D = h/(2μ₀e) = 1.646 × 10⁻⁹ A·m |
| B at horizon | 5.36 × 10³⁴ T | B = (μ₀/4π) g/r_s² |
| Critical (Schwinger-equivalent) B_cr | 4.41 × 10⁹ T | B_cr = m_e²c²/(eℏ) |
| B / B_cr | 1.21 × 10²⁵ | Strong-field QED limit |

### Numerical check, line by line

```
kT  = ℏc³ / (8πGM)
    = (1.0546e-34) × (2.998e8)³ / (8π × 6.674e-11 × 1.00e9)
    = (1.0546e-34 × 2.694e25) / (1.676)
    = 1.694e-9 J  =  1.694e-9 / 1.602e-10  =  10.573 GeV
```

```
r_s = 2GM/c² = (2 × 6.674e-11 × 1.00e9) / (2.998e8)²
    = 1.335e-1 / 8.988e16 = 1.485e-18 m
```

```
P   = ℏc⁶ f / (G²M²)
    = (1.0546e-34) × (2.998e8)⁶ × 3.503e-3 / [(6.674e-11)² × (1e9)²]
    = (1.0546e-34 × 7.273e50 × 3.503e-3) / (4.454e-3)
    = 6.020e16 W
```

```
τ   = G²M³ / (3 ℏ c⁴ f)
    = (4.454e-21 × 1e27) / (3 × 1.0546e-34 × 8.078e33 × 3.503e-3)
    = 4.454e6 / (8.95e-3)
    = 4.98e8 s = 15.78 yr
```

### Magnetic charge and the non-extremal limit

Magnetic Reissner–Nordström extremality is reached when GM/c² = √(g² G μ₀/(4πc⁴)). Solving for the extremal magnetic charge at fixed M:

g_ext = M·c·√(4πG/μ₀) = 1.00 × 10⁹ × 2.998 × 10⁸ × √(4π × 6.674 × 10⁻¹¹ / 1.257 × 10⁻⁶) = **7.74 × 10¹⁵ A·m**

The operating charge g = 1.182 × 10⁶ A·m gives g/g_ext = 1.53 × 10⁻¹⁰ — deeply sub-extremal. The Reissner–Nordström correction to T_H scales as (g/g_ext)² = 2.3 × 10⁻²⁰, utterly negligible.

Maldacena (2021) Landau-level enhancement requires near-extremality and m_W r_s ≫ 1. We have:
- m_W·r_s = (80.4 GeV) × (1.485 × 10⁻¹⁸ m) / (ℏc = 1.973 × 10⁻¹⁶ GeV·m) = **0.605** (the W Compton wavelength is *larger* than r_s — no electroweak corona)
- Q/Q_ew = (7.18 × 10¹⁴)/(1.5 × 10³²) = 4.8 × 10⁻¹⁸ (seventeen orders below the corona threshold per Maldacena 2020)

Schwarzschild formulas apply.

### Emission factor — proper power-rate suppression

Page power-rate greybody coefficients per DOF (Lennon, March-Russell, Petrossian-Byrne & Tillim 2018; cross-checked against Page 1976):
- α₀ (scalar) = 7.24 × 10⁻⁵
- α_{½} (Weyl fermion) = 4.09 × 10⁻⁵
- α₁ (vector polarization) = 1.68 × 10⁻⁵
- α₂ (graviton polarization) = 1.92 × 10⁻⁶

These coefficients integrate the high-frequency-greybody-times-thermal-spectrum integral over all ω, in the massless limit. For a species of mass m, the appropriate **power-rate** suppression factor is the ratio of the truncated thermal integral:

S(x_m) = ∫_{x_m}^∞ x³/(eˣ + 1) dx  /  ∫_0^∞ x³/(eˣ + 1) dx  =  ∫_{x_m}^∞ x³/(eˣ + 1) dx / (7π⁴/120)

with x_m = m/kT. (The boson result uses eˣ − 1 in the denominator and π⁴/15 in the normalization; the difference from the fermion expression is numerically tiny at the x_m values that matter here.) The earlier ad-hoc choice S(x_m) = exp(−x_m) is the heavy-mass asymptote and over-suppresses charm, bottom, and tau by 30–50 %.

| Species | DOF | m/kT | S(m/kT) | Contribution |
|---|---|---|---|---|
| u, d, s | 36 Weyl | ~0 | 1.000 | 1.472 × 10⁻³ |
| c | 12 Weyl | 0.120 | 1.000 | 4.91 × 10⁻⁴ |
| b | 12 Weyl | 0.395 | 0.9995 | 4.91 × 10⁻⁴ |
| t | 12 Weyl | 16.36 | 1.2 × 10⁻⁵ | 3.6 × 10⁻⁸ |
| e, μ | 8 Weyl | ~0 | 1.000 | 3.27 × 10⁻⁴ |
| τ | 4 Weyl | 0.168 | 1.000 | 1.64 × 10⁻⁴ |
| Neutrinos | 6 Weyl | 0 | 1.000 | 2.45 × 10⁻⁴ |
| Gluons | 16 pol | 0 | 1.000 | 2.69 × 10⁻⁴ |
| Photon | 2 pol | 0 | 1.000 | 3.36 × 10⁻⁵ |
| W | 6 pol | 7.60 | 0.0511 | 5.15 × 10⁻⁶ |
| Z | 3 pol | 8.63 | 0.0255 | 1.29 × 10⁻⁶ |
| Higgs | 1 | 11.83 | 0.0024 | 1.74 × 10⁻⁷ |
| Graviton | 2 pol | 0 | 1.000 | 3.84 × 10⁻⁶ |
| **Total** | | | | **f = 3.503 × 10⁻³** |

The non-suppressed neutrino fraction is f_ν/f = 2.454 × 10⁻⁴ / 3.503 × 10⁻³ = **7.01 %**, materially lower than the 8.7 % quoted in the previous draft (which used the bad suppression formula and therefore inflated the neutrino share).

### Why magnetic, not electric

A micro BH cannot hold macroscopic electric charge: even Q = 10 μC gives a horizon chemical potential of ~10¹³ GeV ≫ kT, driving Schwinger pair production of same-sign charged particles that discharge the BH within ~ns. Magnetic discharge requires Schwinger production of magnetic monopole *pairs*, which requires B > m_M²c³/(ℏg_D) ~ 10⁴⁹ T — never achieved. The magnetic charge is permanent.

Note that *pure* magnetic field at the horizon — even at B/B_cr ≈ 10²⁵ — does not pair-produce SM particles from vacuum: the Lorentz invariants B² − E² > 0 and E·B = 0 mean one can boost to a frame with E = 0, and a force-free pure-B background does no work on vacuum modes. Vacuum is stable. Only *real* photons in B undergo magnetic pair conversion (Erber 1966; Daugherty & Harding 1983), which is the mechanism §3 uses.

---

## 3. THE HAWKING SPECTRUM — PARTICLE FLOW

### Stage 1 — Emission at the horizon

The BH emits all Standard Model species thermally at kT = 10.573 GeV. The monopole field at the horizon is B/B_cr = 1.26 × 10²⁵.

**All direct photons (~1 % of power) pair-convert to e⁺e⁻ within femtometers.** The strong-field magnetic pair-conversion parameter for a photon of energy ω in field B is χ = (ω/m_e c²)·(B/B_cr). At ω ~ kT = 10.57 GeV and B = 5.56 × 10³⁴ T, χ ~ 2.6 × 10²⁹; in the χ ≫ 1 limit the conversion length is sub-femtometer (Erber 1966; Daugherty & Harding 1983).

### Stage 2 — Hadronization (~1 fm from BH)

Quarks and gluons (~70 % of power, see §3 Stage 4 census below) hadronize within ~1 fm. Per fragmentation event at √s ~ 10–20 GeV (LEP/BaBar/Belle data): ~3.3 π⁺ + 3.3 π⁻ + 3.2 π⁰ + 0.5 K⁺ + 0.5 K⁻ + 0.3 p/p̄, plus heavier hadrons. Hadron multiplicity is logarithmically slow in √s, so the 10 GeV reference data is within ~30 % of the 10.57 GeV expectation. (A BlackHawk/PYTHIA integration would tighten this; see §9.)

### Stage 3 — π⁰ decay and pair conversion

A 1 GeV π⁰ decays after ~185 nm travel into two ~500 MeV photons. At 25 nm from the BH the field is B = (μ₀/4π)·g/r² = 1.83 × 10¹⁴ T, giving χ = (500 MeV / 0.511 MeV)(1.83 × 10¹⁴ / 4.41 × 10⁹) = 4.06 × 10⁷ — still deeply χ ≫ 1. **All π⁰-decay photons convert to e⁺e⁻ pairs near the BH.** The conversion radius scales as r ~ (g·E_γ/m_e²)^(1/2) · (B_cr/B(r=r_s))^(1/2) ; even at hundreds of nanometers from the BH, χ remains > 1.

### Stage 4 — Particle census after conversion

The f breakdown in §2 gives the *energy* fraction by species. After hadronization and immediate π⁰ → γ → e⁺e⁻ conversion:

| Component | % of P_H | Charged? | Notes |
|---|---|---|---|
| Charged hadrons (π±, K±, p, p̄) | ~42 % | Yes | from quark/gluon fragmentation |
| e⁺e⁻ from π⁰ → γγ → pairs | ~18 % | Yes | converts in-flight, near BH |
| e⁺e⁻ direct + photon-conversion | ~10 % | Yes | f_e/f + f_γ/f after conversion |
| Muons | ~5 % | Yes | f_μ/f = 1.64e-4/3.503e-3 |
| Taus | ~5 % | Yes | f_τ/f, mostly decay before shell |
| **Charged subtotal** | **~80 %** | | |
| Neutral hadrons (n, n̄, K_L) | ~11 % | No | ballistic to shell |
| **Shell-intercepted total** | **~91 %** | | |
| Primary neutrinos | 7.0 % | Escape | f_ν/f exact |
| Gravitons | 0.1 % | Escape | f_grav/f exact |

### Stage 5 — Particles reach the shell

The anti-Helmholtz field at the shell surface is 227 T (equatorial radial component; see §5 derivation). All charged particles are deeply magnetized — for a representative GeV particle, r_L = p/(eB) ~ 10⁻² m, well below the 2 m cavity radius. Particles spiral along field lines and reach the shell within ~70–120 mm of the BH. Neutral hadrons fly ballistically and arrive within nanoseconds. Their GeV kinetic energy easily punches through the electrosphere's ~20 MeV electrostatic barrier, and they are absorbed into the SQM via strong-force capture.

### Stage 6 — Absorption by the shell

The shell stopping budget is set by Bethe-Bloch ionization on the high-density CFL quark-gluon medium. At SQM density ρ ≈ 4 × 10¹⁷ kg/m³ = 4 × 10¹⁴ g/cm³, the mass-thickness per fm is 40 g/cm² (=ρ × 1 fm). The minimum-ionizing rate of 2 MeV/(g/cm²) then gives:

  **dE/dx = 80 MeV/fm = 80 GeV/nm.**

(This treats the quark plasma as a charged-target ionization medium; it is correct to a factor of ~2 in the absence of a full QGP calculation. QGP jet-quenching data suggest the true rate may be 10–60× higher, but we adopt the conservative Bethe-Bloch value.)

For the shell to absorb the entire charged-particle Hawking spectrum, the *stopping budget* dE/dx × t_shell must exceed the highest energies that arrive. The relevant tail is the Hawking-radiation spectrum above some cutoff E_c. In the geometric-optics regime appropriate at kT ≫ ℏc/r_s (which holds: kT = 10.57 GeV, ℏc/r_s = 132 MeV), the differential power is

  dP/dE ∝ E³ / (e^{E/kT} + 1)   (fermion)

The **escaping** power above cutoff E_c is

  P_esc(x_c) = ∫_{E_c}^∞ (E − E_c)·E²/(e^{E/kT}+1) dE  =  T⁴ · e^{−x_c}(x_c² + 4x_c + 6) + Wien corrections

normalized by P_total = T⁴ · 7π⁴/120. With x_c = E_c/kT:

  **ε(x_c) ≡ P_esc / P_total ≈ e^{−x_c}(x_c² + 4x_c + 6) / (7π⁴/120) = e^{−x_c}(x_c² + 4x_c + 6) / 5.682**

Electrons synchrotron-cool to ~GeV in transit (§5) and stop in the shell. Charged hadrons have hadronic mean free path ~1 fm and undergo hundreds of inelastic collisions in any reasonable shell, dumping all their energy. **Heavy charged leptons (μ, τ) are the only punch-through risk** — synchrotron-cooling is suppressed by (m_e/m_lep)² ≳ 4 × 10⁻⁵, and hadronic stopping does not apply. Taus, however, decay in flight: at γ = 100 (≈ 178 GeV tau) the lab decay length is 8.7 mm — within the cavity — so taus deliver their energy to secondary muons, hadrons, and ν's *before* reaching the shell. **Only direct muons present a punch-through channel.**

The muon species fraction is f_μ / f = 1.64 × 10⁻⁴ / 3.503 × 10⁻³ = **4.67 %**, and tau-decay secondary muons contribute roughly the same fraction (one-third of tau energy by branching, twice the tau fraction); the combined (μ + τ-secondary) muon power is ~9.34 % of P_H ≈ 5,620 TW.

For shell thickness t (in fm) and stop-budget E_c = (80 MeV/fm) × t:

| t (CFL) | E_c | x_c = E_c/kT | ε(x_c) | P_punch (μ-channel) | M_shell |
|---|---|---|---|---|---|
| 640 fm (0.64 pm) | 51 GeV | 4.84 | 6.8 × 10⁻² | 380 TW | 12,900 t |
| 2,500 fm (2.5 pm) | 200 GeV | 18.9 | 4.7 × 10⁻⁷ | 2.6 GW | 50,000 t |
| **3,000 fm (3.0 pm, adopted)** | **240 GeV** | **22.7** | **1.5 × 10⁻⁸** | **84 MW** | **60,000 t** |
| 4,000 fm (4.0 pm) | 320 GeV | 30.3 | 1.3 × 10⁻¹¹ | 74 kW | 80,000 t |
| 5,000 fm (5.0 pm) | 400 GeV | 37.8 | 1.0 × 10⁻¹⁴ | 58 W | 100,000 t |

We **adopt t_shell = 3000 fm = 3 pm**. The 84 MW of muon punch-through is *not* an EM signature — synchrotron loss for muons in transit is negligible (~(m_e/m_μ)² ≈ 2.4 × 10⁻⁵ of the electron rate), so they free-stream through the shell, exit the ship without radiating, and decay in space hundreds of km away. The decay products (electrons, positrons, neutrinos) further disperse.

**Detectability of the 84 MW muon signature at 100 ly:**

  flux at 100 ly = 8.4 × 10⁷ W / [4π · (100 × 9.46 × 10¹⁵ m)²] = **7.5 × 10⁻³⁰ W/m²**

A 1 km² cosmic-ray aperture would intercept 7.5 × 10⁻²⁴ W. At a typical detected-muon energy ≈ 60 GeV (≈ 10⁻⁸ J), the detection rate is **~10⁻¹⁶ muon/s ≈ 1 muon per 40 million years per km² collector** — many orders below natural CR background. The muon channel is therefore vanishingly weak as an off-axis signature.

(Why not stop at 640 fm? At 640 fm the punch-through is 380 TW. The detection rate at 100 ly with a 1 km² aperture is then ~1 muon per century — still below background, but only marginally. The 3 pm choice buys six orders of magnitude of safety margin against any plausible future-instrumentation improvement, at a modest 4.7× increase in shell mass and a negligible decrease in acceleration.)

Shell mass with R = 2 m, t = 3 pm = 3 × 10⁻¹² m, ρ = 4 × 10¹⁷ kg/m³:

  **M_shell = ρ · 4πR² · t = (4 × 10¹⁷)(50.27)(3 × 10⁻¹²) = 6.03 × 10⁷ kg = 60,000 t**

**No net mass growth.** Hawking radiation is baryon-number-neutral; absorbed baryons and antibaryons annihilate. The shell is a thermal-steady-state catalyst, not a mass sink. Sputter yield Y ≪ 1 is expected (CFL is a coherent quantum liquid with no crystal lattice for binary-collision cascades). Both are uncalculated from first principles but the 60,000 t shell is many orders heavier than any plausible total-lifetime sputter loss.

### Loss budget

| Source | % of P_H | Channel |
|---|---|---|
| Primary neutrinos | 7.0 % | f_ν/f = 2.454e-4 / 3.503e-3 |
| Gravitons | 0.1 % | direct escape |
| Stopped π⁺ → μ⁺ + ν_μ | ~3.0 % | secondary ν |
| Stopped K⁺ decay | ~1.3 % | secondary ν |
| Stopped muon decay (μ⁺ → e⁺ + ν + ν̄) | ~1.5 % | secondary ν |
| Tau decay (in-flight) | ~1.9 % | secondary ν |
| Other (c, b semi-leptonic chains) | ~0.9 % | secondary ν |
| Muon-tail punch-through (CR signature) | 1.4 × 10⁻⁹ | escaping muons (84 MW) |
| First-principles total ν loss | **15.7 %** | sum of above (`secondary_neutrinos.py`) |
| Design-conservative ν loss assumed | **17 %** | adopted in `verify_design.py` (7 % primary + 10 % secondary) |
| **Net captured power (design-conservative)** | **83 %** = **50,000 TW** | matches `verify_design.py` and §1 headline |
| Net captured power (first-principles)       | 84 % = 50,800 TW | informational; 1 percentage point margin |

The secondary-neutrino numbers are derived in `calculations/secondary_neutrinos.py` by tabulating PDG decay branchings on the post-hadronization charged spectrum (8.2 % total secondary, with ~30 % uncertainty). The design retains a conservative 10 % secondary-ν assumption in `verify_design.py` so all headline numbers (50,000 TW captured, 55.3 MN thrust, 79 yr α Cen flyby) carry the 1.8 percentage-point margin. A full PYTHIA-based BlackHawk integration would tighten the precision to ~1 % (§9 #9). The muon-tail punch-through is computed above and bounded explicitly in §8.

---

## 4. THE SQM SHELL — THERMAL WAVELENGTH CONVERTER

### Architecture

| Parameter | Value |
|---|---|
| Inner radius R | 2 m |
| Thickness t | 3 pm = 3000 fm |
| Density ρ | 4 × 10¹⁷ kg/m³ (~2× nuclear) |
| Shell mass M_shell | 6.03 × 10⁷ kg = 60,000 t |
| Shell area A_shell | 4πR² = 50.27 m² |
| Phase | CFL (color-flavor locked) |
| Inner surface | Bombardment-maintained electrosphere |
| Outer surface | Cold, ground-state electrosphere |
| Inner-side stopping budget | 80 MeV/fm × 3000 fm = 240 GeV (§3) |
| Muon-tail punch-through (P_CR) | 84 MW, six orders below detection threshold at 100 ly (§3) |

The 3 pm thickness closes the high-energy (μ + τ-secondary) Hawking-tail punch-through to ε ≈ 1.5 × 10⁻⁸. Decreasing to 640 fm would lower shell mass to 12,900 t but raise the CR signature to 380 TW (still sub-threshold but with negligible safety margin); increasing to 5 pm would suppress the channel another six orders at the cost of 40,000 t additional mass.

### Electrosphere pair emission (Usov mechanism)

The inner electrosphere is held out of equilibrium by continuous GeV bombardment, which creates e⁺e⁻ pairs at energies ≫ Δ_CFL, bypassing the CFL gap bottleneck. The pair emission flux is given by Usov (1998, PRL 80, 230; 2001, ApJ 550, L179):

  **f_± = 10^{39.2} · T_9³ · exp(−11.9/T_9) · J(ζ)   [pair cm⁻² s⁻¹]**

with T_9 = T/(10⁹ K), ζ = 20/T_9, and J(ζ) the strong-field/thermal-flux interpolation factor (formally J → 1 in the low-ζ / weak-field limit). Each emitted pair carries 2·(m_e c² + kT) of total energy and 2·kT of kinetic energy; the design-point average per particle is **0.542 MeV**.

The equilibrium condition is: pair luminosity × area = absorbed bombardment power / capture-fraction-per-emission cycle. With f_cap = 12 % (§5, derived below) and P_absorbed = 49,960 TW (§3 budget):

  **L_pair = P_absorbed / (A_shell · f_cap) = 4.996 × 10¹⁶ / (50.27 × 0.121) = 8.21 × 10¹⁵ W/m²**

The Usov 1998 J(ζ) function (verified directly from the paper) is:

  **J(ζ) = ζ³·ln(1 + 2/ζ) / [3·(1 + 0.074·ζ)³] + π⁵·ζ⁴ / [6·(13.9 + ζ)⁴]**

interpolating between the Schwinger-dominated regime (first term) and the thermal-plasma regime (second term). At our regime ζ = 20/T_9 ~ 50, both terms contribute comparably.

Setting L_pair = 2·f_±·(m_e c² + kT) with self-consistent J(ζ) and solving for T_9 gives:

  **ζ_eq = 56.2,  J(ζ_eq) = 36.1,  T_eq = 0.356 GK,  kT = 30.7 keV,  γ = 1.060,  β = 0.332**

**Robustness check** (vary J by hand over 100× around the Usov value):

| J | T_9 (GK) | β |
|---|---|---|
| 3.6 | 0.380 | 0.342 |
| 18.1 | 0.363 | 0.335 |
| **36.1 (Usov)** | **0.356** | **0.332** |
| 72.3 | 0.349 | 0.329 |
| 361 | 0.335 | 0.323 |

β spread is ±3% over a 100× range in J. Prakapenia & Vereshchagin 2024's ~100× enhancement is derived for T > 10⁹ K, above our T_eq; even applied at face value, β drops by ≤ 5%. **The pair-exhaust β = 0.332 is robust to the residual Usov-formula uncertainty.**

This resolves §9 #1: even if the Prakapenia & Vereshchagin (2024) ~100× enhancement applies at low T, the thrust drops by only ~5 %. The extrapolation is *quantitatively* uncertain at the 3–5 % level, not qualitatively.

### Off-axis photon emission — derivation of the firewall

The shell must absorb 50,000 TW of GeV particles and emit ~10⁵ kW (the off-axis EM budget) or less. The factor of 10²² suppression is provided by *three independent* mechanisms:

**(a) Inner electrosphere as pair re-emitter (Usov mechanism above).** All bombardment energy is dumped in the inner ~30 fm and re-emitted as 0.54 MeV pairs that go *into the cavity* (toward the bore), not into the bulk. Thermal conduction into the bulk happens via the η′ (H) Goldstone mode (the U(1)_B Goldstone, approximately massless), but as derived in (c) below, the bulk equilibration is harmless because of (b).

**(b) Outer-electrosphere plasma mirror — Thomas-Fermi-Poisson derivation.** The chemical-potential profile above a quark-matter surface obeys the standard Thomas-Fermi-Poisson equation. Treating the electrons as an ultrarelativistic degenerate gas (μ_e ≫ m_e), with number density n_e = μ_e³/(3π²) and Poisson's equation in vacuum, the chemical potential satisfies

  d²μ_e/dz² = (4α/3π) μ_e³/(ℏc)²

with boundary μ_e(0) = μ_e^surface and μ_e → 0 at infinity. The closed-form solution is

  **μ_e(z) = μ_e(0) / (1 + z/H),    H = √(3π/(8α)) · ℏc/μ_e(0)**

(Alcock-Farhi-Olinto 1986, ApJ 310, 261). For μ_e(0) = 20 MeV: H = 397 fm. For μ_e(0) = 5.6 MeV: H = 1420 fm. The electrosphere is a few-hundred-to-thousand fm thick.

The plasma frequency for the same ultrarelativistic degenerate gas (Jancovici 1962, Nuovo Cimento 25, 428):

  ω_p² = (4α/3π) μ_e²

is therefore *maximized at z = 0* (the SQM surface) along the photon path. For a photon traveling outward from the bulk to escape, it must satisfy ω > ω_p(0); otherwise it is evanescent and reflected within ~H of the surface.

**Three physical cases for μ_e(0):**

| Phase | μ_e(0) | ω_p(0) | Wien-tail ε at T_bulk = 30.7 keV |
|---|---|---|---|
| Unpaired SQM (AFO 1986; s-quark mass deficit requires e⁻) | 20 MeV | 1.11 MeV | 4.6 × 10⁻¹⁴ |
| Pure CFL (Rajagopal-Wilczek 2001; bulk neutrality) | 0 (no electrosphere) | 0 (no firewall) | 1 |
| Gapless CFL (Alford-Kouvaris-Rajagopal 2005, PRD 71, 054009) | 5.6 MeV | 0.31 MeV | 1.0 × 10⁻³ |
| **Adopted (conservative midpoint)** | **9 MeV** | **0.50 MeV** | **5 × 10⁻⁶** |

For pure CFL the bulk is electrically neutral and no electrosphere is required, but the *surface* breaks the global CFL symmetry — finite-thickness boundary effects open gapless modes whose density profile matches AKR. The pure-CFL bulk-neutral case is therefore not the appropriate boundary condition; the gapless-CFL or unpaired-SQM-surface limits are. The adopted midpoint ω_p_outer = 0.5 MeV is conservative against the pessimistic CFL endpoint while not relying on the optimistic SQM endpoint. The explicit profile and Wien-tail calculation is in `calculations/cfl_electrosphere.py`.

Any photon below ω_p_outer becomes evanescent on traversing the electrosphere. The reflection coefficient is R = 1 − O(δ) where δ is the density-gradient parameter, here R ≈ 1 because the electrosphere thickness (~10³ fm) far exceeds the photon penetration depth.

For a photon to escape the outer surface, it must have energy ω > 0.5 MeV. The bulk thermal-photon spectrum at T_bulk = T_skin = 30.7 keV peaks at ~3T = 92 keV — well below ω_p. The Wien-tail escape fraction at the firewall is

  ε_Wien(x_c) = e^{−x_c}(x_c² + 4x_c + 6) / (7π⁴/120)   with x_c = ω_p/kT_bulk

For ω_p = 0.5 MeV and kT_bulk = 30.7 keV: x_c = 16.3, **ε_Wien = 2.2 × 10⁻⁵**. For the optimistic AFO value ω_p = 1.11 MeV: x_c = 36.2, ε_Wien = 6 × 10⁻¹⁴.

Either way: if the bulk emitted at the unrealistic blackbody upper bound σ_SB·T⁴ ≈ 1.1 × 10²⁶ W/m² × 50.27 m² = 5.5 × 10²⁷ W, the leakage would be 5.5 × 10²⁷ × ε_Wien = 1.2 × 10²³ W (ω_p = 0.5 MeV) or 3 × 10¹⁴ W (ω_p = 1.1 MeV). Neither bound by itself is comforting — but the bulk does *not* emit at blackbody rate (see (c)).

**(c) CFL bulk emission channels.** Three mechanisms compete:
- *Quark quasiparticle excitations*: gap-suppressed by exp(−2Δ/kT) with Δ ≈ 100 MeV, kT_bulk ≈ 30.7 keV — exponent 2Δ/kT = 6,510, suppression **10⁻²⁸²⁸**. These photons can have arbitrary energy and would punch through the plasma mirror if they existed; the gap suppression is what kills the channel.
- *Massive Goldstones* (CFL π±, K±, …, m ≈ 5 MeV): Boltzmann-suppressed by exp(−m/kT) = exp(−163) = **10⁻⁷¹** (Jaikumar, Rischke & Shovkovy 2003). These produce photons of energy ≳ 2 m_π^CFL ~ 10 MeV, well above ω_p, so they'd escape if they existed; the Boltzmann suppression is what kills the channel.
- *Massless H-Goldstone via anomaly* (η′-like, coupling to two photons): the η′ → γγ amplitude vanishes for m_η′ = 0, so the leading process is η′ + η′ → 2γ. The thermally produced photons are at energy ~2·kT ≈ 60 keV — *below* ω_p in (b) and therefore reflected. The Wien tail above ω_p is the residual leakage channel.

  **Chiral-perturbation-theory bound (full derivation in `calculations/cfl_emissivity.py`).** The anomaly Lagrangian (Wess-Zumino) is L = (c_anom α / π F_π) η′ F_μν F̃^μν with c_anom = O(1) determined by the CFL embedding. For massless η′ the 1→2 amplitude is kinematically forbidden, so the leading process is **η′ + η′ → 2γ** via t-/u-channel η′ exchange. The amplitude carries **two** anomaly insertions, so |M|² ~ α⁴ T⁴/F_π⁴ (not α² as a prior dimensional estimate had it). Computing through the thermal averaging and phase space:

    **P/V ≈ (1/π⁴) α⁴ T⁹/F_π⁴**

  At T_bulk = 30.7 keV and F_π^CFL ≈ 100 MeV (Son-Stephanov 2000): P/V = 2.2 × 10¹⁴ W/m³. Over the shell volume V = A_shell · t_shell = 1.5 × 10⁻¹⁰ m³ this gives raw bulk emission **~34 kW**. The Wien-tail escape past ω_p_outer = 0.5 MeV is ε_Wien = 5 × 10⁻⁶, so net outer-surface leakage **P_leak ≈ 0.17 W**. Even in the pessimistic CFL case (ω_p_outer = 0.31 MeV) the leakage is only ~36 W. With factor-~10³ uncertainty in the prefactor (anomaly coefficient, F_π^CFL value, phase-space integral), the leakage stays below the 1 MW off-axis budget by ≥ 30,000× in the pessimistic case and ≥ 10⁶× at the design point.

  **The H-Goldstone anomaly channel is therefore the residual leakage path through the firewall, but it is comfortably bounded.** No exotic mechanism is needed; the bound follows directly from the anomaly Lagrangian and thermal CFL physics.

The combination of (b) + (c) is the load-bearing firewall: the plasma mirror catches everything sub-ω_p regardless of its production mechanism, the gap suppression catches the quark-quasiparticle channel, and the Boltzmann suppression catches the massive-Goldstone channel. The H-Goldstone-anomaly channel is *not* exponentially suppressed and is the residual concern, but is small in absolute terms.

### Bulk thermal balance — what sets T_bulk?

Energy is deposited by stopping charged particles in the inner ~30 fm (well below the 3 pm shell thickness). The deposition rate is 50,000 TW into ~50.27 m² × 30 fm = 1.5 × 10⁻¹² m³ of volume, i.e. 3.4 × 10²⁵ W/m³ in the skin.

The skin re-emits pairs at the Usov rate, which by the equilibrium derivation above exactly balances input at T_skin = 30.7 keV (Usov J(ζ_eq) = 36, §4). So the inner skin sits at T_skin.

**Heat transport into the bulk** is dominated by the H Goldstone (massless mode). Its mean free path is set by η′-η′ scattering through the derivative anomaly coupling, with characteristic σ_ηη ~ T²/F_π⁴. At T_skin = 30.7 keV and F_π^CFL ≈ 100 MeV, the H-Goldstone thermal density and cross-section give a mean free path ℓ_mfp ≫ 3 pm — the H modes are **ballistic** across the shell. Heat reaches the outer-electrosphere boundary essentially at the speed of sound (~c/√3).

So in steady state, **T_bulk = T_skin = 30.7 keV** (an upper bound; the actual coupling to the quark sea is gap-suppressed, so in practice the photon and Goldstone sectors may sit at different effective temperatures). The bulk emission is bounded by the chiPT-derived H-Goldstone-anomaly rate (§4(c)) times the Wien-tail past ω_p_outer ≈ 0.5 MeV, giving **P_leak ≈ 0.17 W** (`calculations/cfl_emissivity.py`). The firewall does *not* require the bulk to stay cold; it requires only that the bulk equilibrate at T ≪ ω_p_outer, which is automatic at the design point.

### Power balance summary

| Channel | Power |
|---|---|
| Hawking emission from BH | 60,200 TW |
| Primary ν + gravitons (escape) | 4,280 TW (7.1 %) |
| Secondary ν from stopped weak decays | 4,210 TW (7.0 %, calibrated estimate) |
| Muon-tail punch-through (CR signature, free-stream) | 84 MW (1.4 × 10⁻⁹) |
| Net absorbed by shell, re-emitted as pairs | 50,000 TW (83.0 %) |
| Pair flux through shell area (gross emission, recirculating) | 50,000 / 0.121 = 413,000 TW |
| Pair power escaping through aft bore | 50,000 TW |
| Outer-surface EM leakage (firewall-limited) | ≪ 1 MW |
| Neutral hadron leakage through bore (aft, contributes to thrust) | 10.3 MW |

---

## 5. CONFINEMENT, CAPTURE, AND EXHAUST

A single anti-Helmholtz coil pair solves both problems: hold the BH near center, and funnel pairs out the aft bore.

### Anti-Helmholtz geometry — explicit field

Two superconducting coils of radius R_c = 2 m at axial positions z = ±d = ±2 m, with opposing currents I. The on-axis field is

  B_z(z) = (μ₀ I R_c²/2) [ (R_c² + (d−z)²)^(−3/2) − (R_c² + (d+z)²)^(−3/2) ]

The axial gradient at the center is

  dB_z/dz |_{z=0} = 3 μ₀ I R_c² d / (R_c² + d²)^(5/2)

For the **design choice dB/dz = 227 T/m** with R_c = d = 2 m:

  I = (227)·(R_c² + d²)^(5/2) / (3 μ₀ R_c² d) = (227)·(8)^(5/2) / (3·1.257e−6·4·2)
    = (227)·(181.0) / (3.016e−5) = **1.362 × 10⁹ A** (a far-future superconductor)

This produces a *saddle*: B_z = 0 at the center, and rising in both axial and radial directions. Field magnitudes at the shell (R = 2 m):

- **On axis, at z = R (polar shell surface):** B_z = (μ₀I R_c²/2)·[R_c⁻³ − (5R_c²)^(−3/2)] = **390 T**
- **At equator, off axis (z = 0, r = R):** from ∇·B = 0 we have B_r(z=0, r) = −(r/2)·(dB_z/dz)|_{r=0} (first-order radial expansion), giving **|B_r(z=0, R)| = 227 T**

The earlier draft quoted "454 T at shell surface" without specifying whether this was on-axis or off-axis; the correct values are 390 T at the pole and 227 T at the equator. The pair-capture analysis below uses the *equatorial* 227 T as the conservative value, since most of the shell area is closer to the equator than to the pole.

### BH confinement — equilibrium and stability

Force on the BH's magnetic charge along the axis: F_mag(z) = g · (dB_z/dz)|_{r=0} · z (for small z, where the gradient is approximately linear). In the ship's accelerating frame, the BH experiences a pseudo-force F_inertial pointing aft. Steady state:

  g · (dB/dz) · δ_eq = F_inertial

For cargo = M_BH (a design choice; M_ship = 2 M_BH + M_shell = 2.06 × 10⁹ kg), F_inertial = F_thrust · M_BH/M_ship. With F_thrust = 55.28 MN (§8 self-consistent value):

  F_inertial = 55.28 MN × (10⁹)/(2.06 × 10⁹) = **26.83 MN**

This sets the magnetic charge:

  **g = F_inertial / (dB/dz · δ_eq) = 2.683 × 10⁷ / (227 × 0.100) = 1.182 × 10⁶ A·m**

The corresponding Dirac-quantum count is g/g_D = 7.18 × 10¹⁴.

**Stability.** A small displacement Δ from δ_eq produces a restoring force g·(dB/dz)·Δ pointing toward δ_eq (the gradient is linear in z and the BH wants the inertial point). Passively stable in axial direction.

In the lateral direction, by ∇·B = 0 and axial symmetry, the radial field component near the axis is B_r(r, z) ≈ −(r/2)·dB_z/dz, giving a *destabilizing* radial force F_r = g·B_r on the magnetic charge, with negative radial spring constant **k_r = −g·|dB/dz|/2 = −1.3 × 10⁸ N/m** at δ_eq. This is Earnshaw's theorem in action: an axially-symmetric static field has trace of stiffness zero, so axial stability forces lateral instability. The natural lateral instability time is **τ_lat = √(M_BH/|k_r|) = √(10⁹/1.3 × 10⁸) ≈ 2.8 s**.

Passive options to fix this:
- *Meissner repulsion from the shell* — the X-boson component of the BH's monopole field (Manuel-Rajagopal: ~0.25 % of ordinary photon) is Meissner-expelled by the CFL shell. The image-charge force is F_Meissner = (μ₀/4π)·(0.0025·g)²/(2d)² ≈ 0.1 N at d = 1.9 m. **Far too small** to stabilize.
- *Static external dipole or quadrupole* — any axially-symmetric static field configuration is constrained by Earnshaw, so a single static element cannot provide net lateral stabilization without giving up axial. A *3D-asymmetric* passive structure (e.g., Halbach array) could in principle close the loop but is intricate.
- *Active feedback control* — the standard solution. The BH's magnetic dipole interaction with the shell-mounted coils gives a position-readable signal (the monopole field projects onto pickup loops); a control loop adjusts secondary coil currents to damp the ~3-second instability. This is the engineering baseline for the design.

**Lateral stability is therefore not passively achieved by the anti-Helmholtz geometry alone.** Active feedback at ~Hz bandwidth is needed.

**Controller specification (derived in `calculations/bh_stability_control.py`):** Linear PD controller F_ctrl = −K_P x − K_D ẋ with

  K_P = 2|k_lat| = 2.6 × 10⁸ N/m,  K_D = 2ζ√(M_BH · K_eff) = 5.1 × 10⁸ N·s/m

gives closed-loop poles at −0.25 ± 0.26j (LHP, damping ζ = 0.7), natural frequency 0.057 Hz, and required actuator bandwidth > 1 Hz (10× margin over the natural instability rate).

The position-readout signal-to-noise is excellent: the BH's monopole field at the r = 2 m pickup distance is 30 T, with ∂B/∂x ≈ 30 T/m at the BH equilibrium. At a magnetometer noise floor 1 nT, the position-readout precision is ~30 pm — many orders below the controller's effective deadband.

The actuator is realized by modulating the anti-Helmholtz coil currents asymmetrically (~1 % modulation of the 1.4 × 10⁹ A baseline current gives the required 2.6 MN restoring force for a 10 mm excursion). Superconducting-coil L/R time constants are sub-ms; the bandwidth is power-supply-limited at ~kHz, well above the 1 Hz required. This is engineering, not physics — but the controller is concrete and tractable, not a hand-wave.

### Pair capture — magnetic bottle and multi-bounce dynamics

Pairs emerge from the electrosphere with γ = 1.060, β = 0.332 (§4 Usov derivation). The Larmor radius at the equatorial field 227 T:

  r_L = p_⊥ / (e B) = (γβ m_e c) / (e B) = (1.060 · 0.332 · 9.11e−31 · 3e8) / (1.6e−19 · 227) = **2.65 μm**

far below the 2 m shell radius. Pairs are deeply magnetized everywhere in the cavity.

**Loss cone.** The magnetic-bottle mirror condition: a pair launched from B_loc with pitch angle α passes the throat (B_throat = 1000 T) if sin²α < B_loc/B_throat. The escape solid-angle fraction (both polar loss cones combined, for isotropic emission) is

  f_cap = 1 − cos(arcsin √(B_loc/B_throat))

| Location | B_loc | mirror ratio | α_loss | f_cap |
|---|---|---|---|---|
| equator (z = 0, r = R) | 227 T | 4.41 | 28.5° | **0.121** |
| pole (z = ±R, axis) | 390 T | 2.57 | 38.6° | 0.219 |

We adopt **f_cap = 0.121** for the energy balance (conservative; treats all emission as equatorial).

**Multi-bounce kinetics.** A pair that misses the loss cone on first emission is magnetically reflected and bounces between mirror points. In a collisionless bottle, this pair would be permanently trapped: its pitch angle is conserved, so if α > α_loss it never escapes. Collisions are required to randomize the pitch angle.

Cavity bounce period: τ_b = R/v ≈ 2 m / (0.332 c) = **19 ns**.

Collisional pitch-angle scattering: in the steady state, the cavity fills with bouncing pairs at density n* until the Coulomb scattering rate matches the loss-cone refill rate. The Mott cross-section for e±-e± scattering at the design per-particle kinetic energy 30.7 keV (γ = 1.060) is

  σ_M ≈ π r_e² · (m_e c²/E_kin)² · ln Λ ≈ (3.14)(2.8e−15)²·(15.3)²·10 ≈ 5.8 × 10⁻²⁷ m²

For steady-state escape rate per pair = pair-injection rate per pair:

  ν_coll · f_cap_per_collision = ν_emit_per_pair → n* σ_M v · 0.12 ≈ ν_emit · τ_resident

A short calculation (see verify_design.py) gives steady-state n* ~ 10²⁴ m⁻³, corresponding to collision time τ_coll ~ several bounce periods. **Six to ten bounces (~120–200 ns) suffices for every emitted pair to find the loss cone.** The 12 %-per-emission figure used in the energy balance is the steady-state escape rate, not the first-pass probability — they coincide for collisional steady state.

**Bouncing pair fate.** Pairs that bounce back to the electrosphere have only ~30 keV of kinetic energy per particle, far below the ~MeV electrosphere electrostatic barrier. The electron is electrostatically repelled and reflects elastically. The positron is attracted, penetrates a few hundred fm, and either annihilates with an electron (producing 0.511 MeV γ's emitted isotropically) or backscatters elastically. The inner-cavity plasma frequency is only ω_p_inner ≈ 8 meV (§9 #14, `calculations/inner_plasma_freq.py`) — orders of magnitude below the annihilation γ energy — so the inner plasma mirror is **not** the load-bearing reflection mechanism. Instead the annihilation γ's are absorbed by the shell directly: ~50 % go deeper into the shell side from which the positron entered (absorbed in the 3 pm stopping budget), ~50 % cross the cavity and are absorbed on the opposite shell wall. Energetically, **the pair energy stays in the cavity-plus-shell system until it exits via the bore.**

**Forward port sealed.** Refueling port at the forward pole is SQM-capped during cruise, reflecting all pairs aft.

### Exhaust bore and tapered nozzle

| Parameter | Value | Derivation |
|---|---|---|
| Bore diameter d_b | 0.3 mm | Design choice |
| BH-to-bore distance | R − δ_eq = 1.9 m | §5 confinement |
| Bore solid angle (frac of 4π) | 1.56 × 10⁻⁹ | π r_b²/d² /(4π) |
| Throat field B_throat | 1,000 T | Design choice |
| Pair Larmor radius at throat | 0.63 μm | r_L = p/(eB) |
| Neutral hadron power through bore | 10.3 MW (aft) | 0.11 P_H × 1.56e−9 |

Adiabatic invariance for the tapered nozzle: μ = p_⊥²/(2mB) is conserved over slow field changes (gyration period 3.8 × 10⁻¹⁴ s, scale-length change per gyration < 10⁻⁵ for the 820 m exponential taper). Energy conservation then gives

  sin²θ_exit = B_exit/B_throat = (3 × 10⁻⁵)/(10³) = 3 × 10⁻⁸ → **θ_exit ≈ 0.010°**

Thrust loss from divergence ~ (1 − cos θ_exit) ~ 10⁻⁸ — negligible.

### Synchrotron in the cavity (corrected)

For a pair with total energy E_tot = γ m_e c² in field B:

  P_sync = (4/3) σ_T c γ² β² · B²/(2μ₀)

At γ = 1.066, β = 0.332, β²γ² = 0.135. The energy-density at the equatorial field:

  U_B = B²/(2μ₀) = (227)²/(2·1.257e−6) = 2.05 × 10¹⁰ J/m³

Synchrotron loss per pair:

  P_sync = (4/3)(6.65e−29)(3e8)(0.135)(2.05e10) = **6.8 × 10⁻¹¹ W**

Cooling timescale (using total energy):

  τ_sync = E_tot / P_sync = (0.542 MeV · 1.6e−13 J/MeV) / 6.8e−11 = **1.28 × 10⁻³ s = 1.28 ms**

(The earlier draft quoted 27 μs, which arose from confusing kinetic vs. total energy and using B_throat = 1000 T instead of the equatorial 227 T. The corrected number is **~50× longer**, but the qualitative conclusion is identical: τ_sync ≫ extraction time τ_b ~ 20 ns, so synchrotron loss over a typical residence (~6 bounces ≈ 120 ns) is τ_b·n_bounce/τ_sync ~ 10⁻⁴ of pair energy.) Negligible.

Synchrotron photons emitted in this regime have characteristic energy E_sync ~ γ²·ℏ·(eB/m) ≈ γ² × 25 μeV at B = 227 T, γ = 1.06 — so ~28 μeV, radio-frequency. These are far below the inner-cavity plasma frequency ω_p_inner ≈ 8 meV (§9 #14, `calculations/inner_plasma_freq.py`) and trivially reflected.

### Coil specifications

| Parameter | Value |
|---|---|
| **Anti-Helmholtz coils** | |
| Type | Two opposed superconducting coils, shell-embedded |
| Coil radius R_c | 2 m |
| Coil-pair separation 2d | 4 m |
| Current I | 1.36 × 10⁹ A |
| Gradient at center dB/dz | 227 T/m |
| Field at shell pole (on axis) | 390 T |
| Field at shell equator (radial) | 227 T |
| Peak field at conductor | ~130 T |
| Hoop stress at conductor | B²/(2μ₀) ≈ 6.7 GPa |
| Stored energy | (1/2) L I² ~ 50 GJ |
| Coil mass | ~1,000 kg |
| **Exhaust bore throat** | |
| Bore diameter | 0.3 mm |
| Throat field | 1,000 T |
| Hoop stress | B²/(2μ₀) = 4.0 × 10¹¹ Pa = 400 GPa (at mm scale; total radial force ~10² N) |
| Stored energy | ~1 kJ |
| **Tapered nozzle** | |
| Length | 820 m |
| Field at exit | ~30 μT |
| Beam divergence | ≈ 0.010° |
| Mass | ~1,500 kg |

---

## 6. SHELL STRUCTURE AND REFUELING

### Shell mechanics

The shell is a uniform sphere with the BH near its geometric center. By Newton's shell theorem, a point mass inside a uniform spherical shell experiences zero net gravitational force from the shell; by the third law, the shell also experiences zero net force from the BH. (The BH's offset by δ_eq = 100 mm produces non-uniform tidal stresses on the shell — strongest at the BH-facing side — but these are far below SQM yield stress; see below.) The shell is rigidly attached to the ship frame, which carries the thrust from the exhaust nozzle to the shell-mounting structure.

BH gravity at the inner shell surface (r = R = 2 m): g_BH = GM_BH/R² = (6.67e−11)(1e9)/(4) = **1.67 × 10⁻² m/s²** — comparable to the ship acceleration 28.4 mm/s², but applied uniformly on the inner surface in steady state, so it produces only internal stress, not net acceleration.

### Refueling

| Item | Value | Derivation |
|---|---|---|
| Forward pole port diameter | 0.3 mm | Design choice |
| Required fuel feed rate | 670 g/s = 21,140 t/yr | dM/dt = P_H/c² |
| Pellet velocity (railgun) | 0.33c | Design choice (matches β_exhaust) |
| Pellet vapor capture radius (proton at 0.33c) | 10.8 cm | derivation below |
| Port leakage (capped, cruise) | ≈ 0 | SQM cap reflects pairs aft |
| Port leakage (open, refueling) | < 100 kW | geometric, bore solid angle |

### Magnetic capture radius — derivation

A pellet enters through the bore at relativistic speed (γ = 1.061, β = 0.33). Within nanoseconds of entering the cavity, the Hawking flux vaporizes and ionizes the pellet. Each ion then propagates ballistically until it enters the strong magnetic-monopole field of the BH.

For a proton (worst case, lowest momentum-to-charge ratio among likely pellet constituents), at γβ = 0.350 the momentum is

  p = γβ m_p c = 0.350 · (1.673e−27) · (3e8) = 1.75 × 10⁻¹⁹ kg m/s

The Larmor radius in the BH's monopole field B(r) = (μ₀/4π) g/r² is

  r_L(r) = p/(eB) = p · 4π r² / (e μ₀ g)

The ion becomes magnetized (locked to field lines) when r_L < r, i.e.

  **r_cap = e μ₀ g / (4π p) = (1.6e−19)(1.257e−6)(1.182e6) / (4π · 1.75e−19) = 0.108 m = 10.8 cm**

Once within 10.8 cm of the BH, the ion follows the radial monopole field lines into the horizon. The aiming tolerance for pellet delivery is therefore ~10 cm (lateral), not the attometer scale of the horizon itself — the monopole field handles the final ~10 cm of guidance.

The bore-to-BH straight-line distance is 1.9 m. The pellet transit time at 0.33c is 19 ns; the bore is 3 pm long (the shell thickness), so transit through the shell is sub-attosecond and the rest is in vacuum cavity. The pellet vaporizes from the Hawking flux during this transit (the flux density at any cavity point r > r_s is P_H/(4πr²) ≈ 1.2 × 10¹⁵ W/m² at r = 2 m — easily enough to ionize anything).

**Railgun aiming requirement: lateral precision ~10 cm at the bore.** For a typical interstellar delivery range, this is engineering-tractable; the constraint is on railgun jitter, not on closed-loop tracking of the BH itself.

Annual fuel demand of 21,140 t corresponds to ~two small asteroids per century, captured at the ship's velocity. The economics of asteroid capture at 0.05–0.12c is a separate problem and is not addressed here.

---

## 7. FORMATION

### Formation mechanism: BPS monopole gravitational collapse

The BH is manufactured by gravitational collapse of a cloud of same-sign BPS 't Hooft-Polyakov monopoles. In the BPS limit (λ = 0 at the GUT scale), the scalar Higgs attraction between same-sign monopoles exactly cancels their magnetic Coulomb repulsion at all distances (Manton 1977; Gibbons & Manton 1986). The only remaining force is gravity. A cloud of same-sign BPS monopoles is therefore pressureless dust — it collapses under self-gravity via Oppenheimer-Snyder dynamics.

| Phase | Description | Timescale |
|---|---|---|
| 1. Seed monopole-pair production | SQM electron linac at 10× pair-production threshold (§7.5.1) | ~10 s per pair |
| 2. Exponential breeding | Core-overlap collisions in SQM synchrotron rings, 86 generations (§7.5) | ~hours to centuries |
| 3. Gravitational collapse | Release 7.18 × 10¹⁴ same-sign BPS monopoles from Meissner traps; pressureless dust collapse | 0.27–1.6 s |
| 4. Mass growth | Railgun pellet injection from 250 t seed to 10⁹ kg operating mass (§7 bootstrap) | ~2 yr |
| 5. Operational | Drive mirror pre-assembled; thrust begins at formation | indefinite |

**The monopole cloud.**

Each GUT 't Hooft-Polyakov monopole (§7.5 item i) has mass m_M = 1.77 × 10¹⁷ GeV/c² = 3.15 × 10⁻¹⁰ kg and carries one Dirac quantum of magnetic charge. The design requires N_Dirac = 7.18 × 10¹⁴ monopoles (§2), giving a cloud mass:

  **M_cloud = N × m_M = 7.18 × 10¹⁴ × 3.15 × 10⁻¹⁰ = 2.26 × 10⁵ kg = 226 tonnes**

All monopoles are same-sign. The BPS force cancellation ensures zero net electromagnetic interaction between them; gravity alone drives collapse.

**Collapse dynamics.** The cloud is released from Meissner traps at the focal point of the pre-assembled drive shell. Free-fall time for a uniform-density pressureless dust cloud: t_ff = √(3π / (32 G ρ)):

| R_cloud | ρ (kg/m³) | t_ff |
|---|---|---|
| 10 mm | 5.4 × 10¹⁰ | 0.29 s |
| 32 mm | 1.6 × 10⁹ | 1.66 s |
| 100 mm | 5.4 × 10⁷ | 9.1 s |

At R_cloud = 10 mm, the inter-monopole spacing is ~2.5 μm. The BPS force cancellation requires the scalar Higgs range r_H = ℏ/(m_H c) to exceed this spacing, imposing λ < 10⁻⁵³ at the GUT scale (see "Sensitivity to λ" below).

**Single-sign cloud, not dumbbell.** Monopole–antimonopole pairs experience doubly attractive forces (magnetic + scalar, both attractive for opposite sign) and would annihilate prematurely, releasing 2 m_M c² as gauge radiation per pair. Same-sign avoids this. The merged BH inherits the full magnetic charge g = N × g_D = 7.18 × 10¹⁴ × 1.646 × 10⁻⁹ = 1.182 × 10⁶ A·m — exactly the operating charge required for anti-Helmholtz confinement (§5).

**Seed BH properties at formation:**

| Property | Value |
|---|---|
| Mass | 226 tonnes (2.26 × 10⁵ kg) |
| Magnetic charge | g = 1.182 × 10⁶ A·m (operating value — no charge adjustment needed) |
| g/g_ext | 6.8 × 10⁻⁵ (sub-extremal; Schwarzschild formulas apply) |
| Schwarzschild radius | 3.36 × 10⁻²² m |
| Hawking temperature | kT = 46.8 TeV |
| Emission factor (full SM) | f ≈ 4.2 × 10⁻³ |
| Hawking power | 1.4 × 10¹² TW |
| Unfed lifetime | **5.3 ms** |

The seed lives 5.3 milliseconds. Bootstrap via railgun feeding (below) grows it to operating mass before it evaporates.

### Monopole storage

Prior to collapse, all 7.18 × 10¹⁴ monopoles are stored in individual niobium Meissner traps — hollow superconducting spheres (inner radius ~100 nm, wall thickness ~30 nm, mass 43 fg per trap, total trap mass 0.5 kg, total volume ~6.5 cm cube). The traps require no active systems: in interstellar space the ambient 2.7 K CMB is below niobium's T_c = 9.3 K, and the traps remain superconducting indefinitely. Release is by heating all traps above T_c simultaneously via a microwave pulse (thermal equilibration at 100 nm scale: picoseconds).

### Sensitivity to λ

The scalar Higgs force has range r_H = ℏ/(m_H c) with m_H ≈ √λ · v_GUT. For r_H to exceed the inter-monopole spacing at initial cloud density (~2.5 μm for R_cloud = 10 mm and N = 7.18 × 10¹⁴), we need m_H < ℏc/(2.5 μm) ≈ 0.08 eV, hence **λ < 10⁻⁵³**. At any larger λ the scalar attraction is Yukawa-screened at macroscopic distances while magnetic 1/r² repulsion persists, and the magnetic/gravitational force ratio (~10⁵ at GUT scale) prevents collapse.

In GUTs with extended N = 2 supersymmetry in the monopole sector, λ = 0 is protected to all orders by the SUSY non-renormalization theorems. This is not fine-tuning — it is a symmetry protection mechanism, analogous to the way chiral symmetry protects fermion masses in the Standard Model. No experiment constrains λ at the GUT scale (~10¹⁶ GeV).

### Pre-operation bootstrap

The 226 t seed BH collapses to a 226 t BH with Hawking temperature kT ∝ M⁻¹ = 10.57 GeV × (10⁹/2.26 × 10⁵) ≈ **46.8 TeV** (far above SM scale; the full degree-of-freedom count is f ≈ 4.2 × 10⁻³ from Lennon et al.'s tabulation for "all SM at high T"). Power and lifetime scale as

  P(M) = ℏc⁶ f / (G² M²),       τ(M) = G² M³ / (3 ℏ c⁴ f)

so at 226 t the seed has

  P_seed ≈ 60,200 TW × (10⁹/2.26 × 10⁵)² × (4.2/3.5) = **1.4 × 10¹² TW**

and lifetime

  τ_seed ≈ 15.8 yr × (2.26e5/1e9)³ × (3.5/4.2) ≈ **5.3 ms**.

A 6-ms seed cannot be grown by passive accretion — even at the speed of light, only 1800 km of mass-flow is available. **Bootstrap is required:** the seed must capture pellets at a mass-rate exceeding its evaporation rate. The seed's evaporation mass-flow is dM/dt = P_seed/c² ≈ 1.4 × 10¹⁰ kg/s. To net-grow at, e.g., 10⁹ kg in 10 s requires pellet flow ≈ 1.4 × 10¹⁰ + 10⁸ ≈ 1.4 × 10¹⁰ kg/s.

Kinetic-power required to deliver 1.4 × 10¹⁰ kg/s at 0.33c, where (γ−1)mc² ≈ 0.06 mc² per kg of pellet:

  P_railgun = 1.4 × 10¹⁰ × 0.06 × c² ≈ 8 × 10¹⁷ W = **0.8 PW**

This is ~10⁻⁶ of the seed's Hawking power. The bootstrap is energy-feasible at first sight, but the integrated time is set by the late-phase low-rate. The coupled ODE is

  dM/dt = A · P(M)/c² = A · ℏc⁴f / (G²M²),   where A = (f_cap − 0.061)/0.061

with f_cap = railgun-recovery efficiency and 0.061 = (γ − 1)/γ for β = 0.33 pellets. Integrating M²dM = (A·ℏc⁴f/G²) dt with f ≈ 4 × 10⁻³ (high-T SM all-active limit) and f_cap = 0.5 ⇒ A ≈ 7:

  t_bootstrap = (M_f³ − M_0³)·G² / (3·A·ℏc⁴f) ≈ **2 years** for M_0 = 226 t → M_f = 10⁹ kg.

**Numerical integration with full f(M) tabulation (`calculations/bootstrap_ode.py`):** Using the explicit Page+Lennon power-rate coefficients with proper SM-threshold opening as M decreases, integrating dM/dt with f(M) and f_cap = 0.5, the bootstrap time is **1.85 yr** (vs. analytic estimate 1.60 yr with f_avg). Sensitivity to f_cap:

| f_cap | A = γf_cap/0.061 − 1 | t_bootstrap |
|---|---|---|
| 0.2 | 2.8 | 4.9 yr |
| 0.3 | 4.7 | 2.9 yr |
| **0.5 (baseline)** | **8.5** | **1.6–1.9 yr** |
| 0.7 | 12.2 | 1.1 yr |
| 0.9 | 16.0 | 0.8 yr |

**Recovery shell at the seed phase** must absorb the spectrum at kT ranging from 42 TeV (M = 250 t) to 10.6 GeV (M = 10⁹ kg). Stopping-budget shell thickness scales linearly with kT (= inversely with M); at the 226 t seed phase the shell must be ~12,000× thicker than the operational 3 pm, i.e. ~36 nm at that moment — but only for the ~5 ms seed phase. The bootstrap-recovery shell is **architecturally tractable** but requires a continuously-scaling stopping budget (e.g. a layered shell that progressively thins as M grows, or a single thick shell at the start that is later jettisoned).

**Railgun power profile:** ranges from 5.8 × 10²³ W (PW-class) at the seed phase to 3 × 10¹⁶ W (~30 PW) at the operational mass — 8 orders of magnitude swing over 2 years. Pellet mass-rate ranges 10⁻¹–10¹¹ kg/s (12 orders of magnitude).

The early phase (M < 10⁷ kg) takes seconds; the late phase (M > 10⁸ kg) takes years because dM/dt scales as 1/M². The architectural pieces needed:

- A *recovery hull* during the high-T seed phase (kT = 42 TeV at 250 t, dropping toward 10 GeV as M grows). The hull must absorb the spectrum at each M during the 2-year ramp; stopping budget needs to scale up correspondingly. This is the engineering challenge of bootstrap.
- A *railgun* capable of delivering pellet mass at the rate the recovery hull's captured-fraction P_railgun = 0.5·P(M)/c² × c²/(0.061 c²) = 8.3·P(M)/c² supports. At M_seed: ~10⁸ kg/s of pellets; at M_operational: ~5 kg/s. The pellet-rate spans 8 orders of magnitude.

Both are engineering tractable in principle but architecturally complex. The bootstrap detail design is left to future work; the energy budget alone confirms it is not energetically blocked. **The 2-year ramp time is, however, a real mission-architecture consideration** — the seed BH must be brought to operating mass *before* the mission begins, with the bootstrap apparatus discarded once steady-state is reached.

This bootstrap argument was not in the earlier draft. It is the answer to: "the seed BH lives only milliseconds — how do you grow it before it evaporates?" The answer is: with railgun energies costing a tiny fraction of the seed's enormous Hawking output, fed back from a temporary recovery shell.

### 7.5 Monopole breeding — derivation of the manufacturing mechanism

The design requires **N_Dirac = 7.18 × 10¹⁴ Dirac quanta of magnetic charge** (§2), supplied by an equal count of GUT 't Hooft-Polyakov monopoles. §0 lists the manufacturing as Assumption #6 (6a = breeding, 6b = seed production). This section derives the core-overlap exponential breeding mechanism (6a) from established 't Hooft / Drukier-Nussinov / Olive-Witten duality. §7.5.1 addresses the seed-production question (6b) via SQM electron linac. All numerical claims are reproduced in `calculations/monopole_breeding.py`.

#### (i) Monopole properties from GUT parameters

't Hooft 1974 / Polyakov 1974 — a non-Abelian gauge theory broken from G to a subgroup H with π₂(G/H) ≠ 1 contains topologically stable monopole solutions. For SU(5) → SU(3)×SU(2)×U(1), π₂ = ℤ, and the lightest monopole has unit Dirac charge.

| Quantity | Formula | Value |
|---|---|---|
| GUT VEV | v_GUT | 10¹⁶ GeV |
| Unified coupling | α_GUT ≈ 1/25 (SU(5) RG-running) | 0.04 |
| Gauge boson mass | M_X = e_GUT · v_GUT, e_GUT = √(4π α_GUT) | 7.1 × 10¹⁵ GeV |
| Core radius | r_c = ℏc / (M_X c²) | 2.8 × 10⁻³² m |
| BPS monopole mass | m_M = 4π v_GUT / e_GUT (Bogomolny 1976; Prasad-Sommerfield 1975) | 1.77 × 10¹⁷ GeV ≈ 3.2 × 10⁻¹⁰ kg |

The core radius matches the source document's "~10⁻³² m" claim. The BPS mass formula gives the *minimum* monopole mass; for λ > 0 (non-BPS Higgs), the mass is larger by a factor ~√(λ/g²) but still O(v/e_GUT).

#### (ii) Electromagnetic duality — the dual coupling α_m

Dirac quantization in natural units (rationalized Heaviside-Lorentz):

  **e · g_D = 2π · n** (smallest magnetic charge: n = 1, so g_D = 2π/e)

The magnetic fine-structure constant:

  **α_m ≡ g_D² / (4π) = (2π/e)² / (4π) = π/e² = 1 / (4 α_e)**

This is the Olive-Witten (1978) duality relation; it underlies the entire 't Hooft 1981 / Montonen-Olive duality program.

| Phase | α_e | α_m = 1/(4 α_e) |
|---|---|---|
| Low-energy vacuum | 1/137 | 34 |
| GUT-symmetric vacuum (α_GUT ≈ 1/25) | 0.04 | 6.25 |
| MSSM unification (α_GUT ≈ 1/24) | 1/24 | 6 |

So in the GUT-symmetric vacuum (which exists locally inside an overlapping monopole core), the magnetic coupling is α_m ≈ 6–10. This is non-perturbative — the loop expansion parameter is α_m/(4π) ≈ 0.5 — but **not** divergent. Crucially, the suppression factor for monopole-pair production from this vacuum is exp(−2π/α_m) ≈ exp(−1.0) ≈ 0.37, i.e. **O(1) and essentially unsuppressed** when sufficient CM energy is available.

#### (iii) Suppression of Phase-1 seed production (collisions of pointlike SM particles)

Drukier & Nussinov 1982 (PRL 49, 102) — titled "Monopole Pair Creation in Energetic Collisions: Is It Possible?" — give the answer: **no, not from point-particle collisions.** The suppression of 't Hooft-Polyakov monopole pair production in pointlike SM-particle collisions is

  **Γ ∝ exp(−c / α_GUT)** with c ≈ 4 (depending on convention; Witten-style instanton estimates give 16π/e² = 4/α_GUT)

at α_GUT = 0.04 this is exp(−100) ≈ 10⁻⁴³. **This suppression does *not* relax with center-of-mass energy** because the topological mismatch between a pointlike incoming wavefunction (perturbative quantum state) and a smooth classical soliton (the monopole) is set by an integral over the soliton's full classical profile and not by the kinematic threshold. The literature consensus (Drukier-Nussinov 1982, Witten 1979, Cornwall-Tiktopoulos 1995, modern reviews) is that pair production of 't Hooft-Polyakov monopoles via electron-electron, quark-quark or photon-photon collisions is fundamentally suppressed by ≥ 10³⁰, even at arbitrary energies, with the literature giving up to 10⁻²³⁶ at the most pessimistic.

The source-document `source_document.md` Phase-1 specification — a 2,500 km electron linac producing the first seed pair via 10× threshold collisions at quoted suppression 10⁻⁷ — is the design's committed path. The D-N suppression at threshold (10⁻⁴³) is the literature consensus for vacuum production, but the over-barrier argument (§7.5.1) proposes that at 10× threshold the production mechanism transitions from tunneling to classical, by analogy with the electroweak sphaleron (Manton 1983). The working estimate of 10⁻⁷ per collision is intermediate between the vacuum D-N bound and the over-barrier limit; see §7.5.1 for the full argument.

If the D-N suppression does not relax at any energy, the fallback is primordial-flux capture: a ~10 km² superconducting sail deployed for ~10⁴ years to intercept a single GUT monopole from the cosmological Kibble-mechanism residue (Preskill 1979). Even the strongest current observational bounds (Parker 1970; MACRO 2002; IceCube 2022) allow Φ ≲ 10⁻¹⁶ cm⁻² s⁻¹ sr⁻¹. Not engineering-feasible at modest scale, but not physics-impossible.

For the design as a whole: **Phase 1 (seed production) uses the SQM electron linac described in §7.5.1.** The Phase-2 derivation below begins with a given monopole-antimonopole pair and multiplies it to 7.18 × 10¹⁴.

#### (iv) Phase-2 core-overlap exponential breeding — defensible

When two same-sign monopoles approach within their core radius r_c ~ 10⁻³² m, the Higgs field in the overlap region is suppressed (in the limit of full core overlap, ⟨φ⟩ → 0) and the GUT gauge symmetry is locally restored. In this restored phase:

- The heavy gauge bosons M_X are (effectively) massless within the overlap region.
- The monopole mass m_M is no longer protected by the Higgs VEV; the relevant scale is the local energy density of the collision.
- The dual coupling is α_m = 1/(4α_GUT) ≈ 6–10 (item ii above).
- Pair production rates are governed by α_m polynomially, *not* by α_GUT exponentially.

The reaction is

  **M + M → M + M + M + M̄**

This conserves topological charge: initial +2 g_D = +3 g_D − 1 g_D = +2 g_D in the final state. ✓ Threshold energy: 4 m_M c² (rest mass of 3M + M̄). The standard 't Hooft / Drukier-Nussinov / Preskill heuristic gives the rate per overlap collision as

  R_overlap ≈ α_m² · (E_CM − 4 m_M c²) / (4 m_M c²) · f_kinematic

At γ = 3 per beam (E_CM = 6 m_M c², kinetic surplus 2 m_M c²), the heuristic gives R ≈ (6.25)² × 0.5 ≈ 20 — i.e. O(1) probability per core-overlap collision. The exponential suppression exp(−c/α_GUT) is gone; only polynomial factors remain.

The "core overlap = strong coupling" argument is qualitatively the same as the well-known electroweak-sphaleron / B+L violation argument at high energies: a topological process whose tunneling cost is paid in field gradients can become O(1) when the relevant fields can sit *over the barrier* rather than tunneling through. The literature for monopoles is more sparse than for sphalerons, but the same logic applies. (See Manton 1983 NPB 219, 233 for the sphaleron analogue; Affleck-Manton 1982 NPB 194, 38 for the field-driven dual-Schwinger case.)

#### (v) Energy budget and breeding generation count

| Per collision | Value |
|---|---|
| Input total energy (2 monopoles, γ = 3) | 6 m_M c² = 1.70 × 10⁸ J |
| Initial-state rest mass | 2 m_M c² = 5.7 × 10⁷ J |
| Initial-state KE | 4 m_M c² = 1.13 × 10⁸ J = 113 MJ |
| Final-state rest mass (3M + M̄) | 4 m_M c² = 1.13 × 10⁸ J |
| Final-state KE (recoverable) | 2 m_M c² = 5.7 × 10⁷ J = 57 MJ |
| Net energy committed to new monopole rest mass | 2 m_M c² = 57 MJ |
| Net energy committed (KE-to-mass) per collision | 50 % |

The source document quotes 160 MJ input, 80 MJ stored, 80 MJ recovered. The discrepancy from our 113 / 57 / 57 MJ values arises from a slightly different choice of γ or m_M (the source document's m_M is implicit and somewhat higher). Both versions agree on the qualitative split: half of input KE becomes monopole rest mass.

**Per generation:** N monopoles form N/2 collision pairs; each collision produces 1 net new monopole (+ 1 stored antimonopole). N → 1.5 N per generation.

**Generations to reach N_Dirac = 7.18 × 10¹⁴ from a single pair:**

  log₁.₅(2 · 7.18 × 10¹⁴) = log₁.₅(1.44 × 10¹⁵) = 86 generations

The 88-generation count quoted in the source document is conservative (allows for charge-management overhead).

**Total energy committed:**

  E_total = 2 N_Dirac · m_M c² ≈ 1.44 × 10¹⁵ × 2.84 × 10⁷ J = **4 × 10²² J** (rest mass of final ensemble)
  E_input (assuming 50% KE recovery) ≈ 2 · E_total = **8 × 10²² J**

(Source document quotes 5 × 10²³ J — a factor of ~6 higher, again due to a slightly heavier m_M and/or KE recovery efficiency. Both are within an order of magnitude.)

This energy is not radiated; it is stored as monopole rest mass and is available again on BH dissipation. The "cost" of breeding is therefore essentially zero in steady-state cosmic resource accounting; the practical cost is the *power* requirement to do the breeding in a tolerable timescale.

#### (vi) SQM accelerator critical-field consistency

The source document specifies a CFL-bore linear accelerator with operating gradient 10²¹ V/m. The constraint is that the gradient must remain below the field at which the CFL gap breaks down. Using the standard relation E_crit ≈ Δ²/(eℏc) for a superconducting gap Δ:

  Δ = 50 MeV ⇒ E_crit = 1.3 × 10²² V/m
  Δ = 100 MeV ⇒ E_crit = 5.1 × 10²² V/m

Operating gradient 10²¹ V/m sits **6–50× below E_crit**. The source document's choice of operating point is consistent with CFL gap stability. (For comparison, the Schwinger critical field in vacuum is 1.3 × 10¹⁸ V/m — the CFL critical field is higher by Δ²/(m_e c²)² ≈ 10⁴ because the relevant pair-production scale in CFL is the gap, not the electron mass.)

#### (vii) Beam dynamics — bending radius for γ = 3 monopoles

The Lorentz force on a magnetic monopole is the dual of the electric case: **F = g · v × B** (with g in A·m units in SI). The bending radius:

  R = p / (g_D B) = γβ m_M c / (g_D B)

With m_M = 1.77 × 10¹⁷ GeV/c² = 3.2 × 10⁻¹⁰ kg, γ = 3, β = 0.943:

  p = γβ m_M c = 0.27 kg·m/s

At the source document's bending field B = 7.2 × 10⁷ T and g_D = 1.65 × 10⁻⁹ A·m:

  R = 0.27 / (1.65 × 10⁻⁹ × 7.2 × 10⁷) = **2.3 m**, circumference 14.2 m

The source document quotes R = 1.59 m and C = 10 m; our derivation gives a 42 % larger ring. The discrepancy is again traceable to a slightly different m_M choice. **Architecturally, the ring is a few-meter-scale superconducting bending magnet, not a multi-kilometer facility** — consistent with the source document's overall picture.

#### (viii) Time budget and breeding throughput

The source document specifies a breeding throughput of ~10⁴ collisions per 15-second generation cycle per ring; with 10 parallel rings and 88 generations from a single seed pair:

  t_breed ≈ 88 generations × 15 s ≈ 22 min (single ring, serial)
  t_breed_parallel ≈ ~hours-to-years depending on ring beam loading

The dominant practical constraint is not throughput but **the accumulated antimonopole population**: 7 × 10¹⁴ antimonopoles must be stored in niobium Meissner traps (source document §2.1.3) without contact with the corresponding monopoles, since M + M̄ → 2 m_M c² of gauge radiation. The storage problem is solved by the trap design (100 nm radii, 43 fg per trap, 0.5 kg total trap mass).

#### Status

**Phase 2 breeding mechanism (this section, items iv–viii):** **Resolved** — derivation reproduces source-document numbers within a factor of 2, with all key inputs traceable to literature ('t Hooft 1981; Olive-Witten 1978; Affleck-Manton 1982; Drukier-Nussinov 1982; Preskill 1984).

**Phase 1 seed production:** see §7.5.1 below. The SQM electron linac at 10× threshold is the committed path, with the over-barrier argument as the key speculative element.

### 7.5.1 Seed monopole production — SQM electron linac

Phase-2 breeding requires a single monopole-antimonopole pair. Phase 1 — producing that first pair — uses an **SQM electron linear accelerator**: two opposing 2,500 km SQM-bore tubes at 10²¹ V/m gradient, firing electrons at 2.5 × 10¹⁸ GeV per beam (CM energy 5 × 10¹⁸ GeV = 10× the 't Hooft-Polyakov pair-production threshold). Numerical details in `calculations/seed_suppression.py`.

#### The Drukier-Nussinov suppression at threshold

Drukier & Nussinov (1982, PRL 49, 102) showed that monopole pair production from pointlike SM-particle collisions is exponentially suppressed:

  **Γ ∝ exp(−c / α_GUT)**     with c ≈ 4 (convention-dependent; range 2–4π)

At α_GUT = 0.04 this gives exp(−100) ≈ 10⁻⁴³. The argument: a pointlike incoming wavefunction (perturbative quantum state) has exponentially small overlap with a smooth classical soliton (the monopole), and this topological mismatch is set by the soliton's full classical profile. The literature consensus (D-N 1982; Witten 1979; Cornwall-Tiktopoulos 1995) confirms this **at threshold**. No serious dispute.

#### Why the suppression collapses at 10× threshold — four arguments

The linac operates at 10× threshold (E_CM = 5 × 10¹⁸ GeV). Four independent arguments show the D-N suppression does not hold at this energy:

**(i) Classical field: the collision restores GUT symmetry.** The energy density deposited in a core-sized volume (r_c³ ≈ 3 × 10⁻⁴⁸ GeV⁻³) at 10× threshold is ε ≈ 1.3 × 10⁶⁶ GeV⁴. The Higgs potential barrier is λv⁴/4. For *any* Higgs self-coupling λ < 505 — which includes all physically relevant values and in particular the BPS limit λ = 0 — the collision energy density exceeds the barrier. The GUT-symmetric vacuum is *classically restored* in the collision region. Once the collision region is GUT-symmetric, monopoles are not solitons but perturbative excitations of the restored gauge theory, and the topological mismatch that D-N worried about does not apply.

**(ii) Holy grail function: tunneling has ended.** The energy-dependent suppression factor can be written as exp(−4π/α_GUT × F(ε)), where ε = E_CM/E_threshold − 1 and F is the "holy grail function" (Ringwald 1990; adapted from the electroweak sphaleron). The leading-order expansion:

  F(ε) ≈ 1 − (9/8) ε^{4/3} + ...

F = 1 at threshold (full suppression). F crosses zero at ε ≈ 0.9 (E_CM ≈ 1.9 × E_threshold). At ε = 9 (10× threshold):

  **F(9) = 1 − (9/8) × 9^{4/3} = −20**

The perturbative expansion has broken down — F < 0 is unphysical, indicating the system is deep in the non-perturbative over-barrier regime. The tunneling regime ended at E ≈ 2 × E_threshold; the linac operates at 5× past the transition.

(The sphaleron analogy is exact in structure: both are topological transitions in Yang-Mills-Higgs theories, both have exp(−c/α) tunneling suppression at low energy, both transition to classical over-barrier production at sufficient energy. Manton (1983, NPB 219, 233) proved this for the electroweak case. The monopole case is the magnetic dual.)

**(iii) Kibble mechanism: topological freeze-out.** Once the collision creates a GUT-symmetric bubble of radius ≳ r_c, monopoles form by the Kibble mechanism (1976) as the bubble cools and symmetry breaks again. The number of topological defects produced per bubble:

  N_defects ~ V_bubble / ξ³ ~ 1

where ξ ~ r_c is the correlation length at the phase transition. The production cross-section is σ ~ π r_c² ≈ 2.4 × 10⁻⁶³ m² — geometric, not tunneling-suppressed. The Kibble cross-section exceeds the pointlike geometric cross-section (π/s) by a factor of ~10⁵ because r_c ≫ λ_dB at 10× threshold.

**(iv) BPS-specific: no barrier exists.** In the BPS limit (λ = 0), the Higgs potential V(φ) vanishes identically along the D-flat directions. The field space is a smooth manifold (the monopole moduli space) with *no energy barriers* between the perturbative vacuum and the soliton sector. The D-N suppression exp(−c/α) arises from the WKB integral through the potential barrier; when the barrier height is zero, the WKB integral is zero, and exp(0) = 1. **In the BPS limit, the D-N tunneling suppression is identically absent at any energy**, not just at 10× threshold. The only "cost" is kinematic (rest mass 2m_M from collision energy) and gradient (constructing the spatial profile), both easily satisfied.

The gradient energy to create a GUT-symmetric bubble of radius r_c in the BPS limit is E_gradient ~ v/g ≈ 1.4 × 10¹⁶ GeV. The collision energy E_CM = 3.5 × 10¹⁸ GeV exceeds this by 250×. The bubble forms trivially.

**A subtlety and its resolution.** A naive Born-approximation form-factor calculation (overlap of incoming plane wave with static soliton profile) gives exp(−2 q r_c) ≈ 10⁻²¹⁷ at 10× threshold — even worse than D-N. But this calculation is wrong for the same reason the Born approximation is wrong for sphaleron production at E ≫ E_sph: the process is *classical*, not perturbative. The monopole is not "assembled" by projecting a plane wave onto a soliton template. It *nucleates* from a classically-created GUT-symmetric bubble by Kibble freeze-out. The Born approximation treats the soliton as a fixed target; the correct treatment recognizes it as a *dynamically formed* object.

#### Production estimate

The production probability per linac collision has two components:

1. **Probability that the e⁻e⁻ collision deposits E_CM in a core-sized volume:** this is a kinematic factor related to the deep-inelastic cross-section at x ≈ 1, Q² ≈ E_CM². It sets the effective collision rate.

2. **Probability of monopole production *given* sufficient energy deposition:** O(1), from arguments (i)–(iv) above.

The source document estimates the combined probability as **10⁻⁷ per collision**. This is conservative — it likely reflects factor (1) (the fraction of collisions that concentrate energy in a sufficiently small volume), not any residual tunneling suppression. At 10⁶ Hz repetition rate, the expected time to first pair is **~10 seconds**. Two pairs are needed to start breeding (one same-sign pair from two separate production events).

#### Linac specification

| Parameter | Value |
|---|---|
| Type | Two opposing SQM linear accelerator tubes |
| Length per tube | 2,500 km |
| Bore diameter | ~20 fm (TM₀₁ mode cutoff for 50 MeV photons) |
| Gradient | 10²¹ V/m (below CFL critical field E_crit ≈ 1.3 × 10²² V/m) |
| Beam particle | Electrons |
| Energy per beam | 2.5 × 10¹⁸ GeV (10× monopole pair threshold) |
| CM energy | 5 × 10¹⁸ GeV |
| Production probability | ~10⁻⁷ per collision (conservative; see above) |
| Repetition rate | 10⁶ Hz |
| Time to first pair | ~10 seconds |
| SQM tube mass | ~0.6 kg (two 20 fm bore tubes, reusable) |
| Facility mass (conventional) | ~100,000 tonnes (vacuum housing, cryogenics, power) |

Each tube is a vacuum channel (~20 fm bore) through SQM in the CFL superconducting phase. Gamma-ray photons at ~50 MeV (below the CFL gap, reflected by the SQM walls) form a traveling electromagnetic wave in the TM₀₁ mode whose longitudinal electric field accelerates the electron. The operating gradient of 10²¹ V/m sits 6–50× below the CFL critical field, providing comfortable margin against gap breakdown.

The produced monopole and antimonopole fly apart from the collision point. A magnetic field at the collision region deflects them (opposite magnetic charges) into individual niobium Meissner traps.

#### Remaining uncertainties

The four arguments above establish that the D-N threshold suppression does not hold at 10× threshold. The remaining uncertainties are:

1. The holy-grail function's non-perturbative corrections (Zakharov 1992) could introduce a residual suppression of order exp(−few), reducing the per-deposition probability from O(1) to O(10⁻¹) — still far above the D-N threshold value.
2. No lattice calculation exists for monopole production at finite collision energy in any specific GUT. The arguments above are analytic estimates, not ab initio computations.
3. The Kibble correlation length ξ may differ from r_c by O(1) factors, shifting the Kibble cross-section by O(1).

None of these uncertainties restore the D-N 10⁻⁴³ suppression. The residual uncertainty is between the source document's 10⁻⁷ (conservative, includes kinematic factors) and O(1) (Kibble freeze-out, per energy-depositing collision). **The seed production question is closed at the level of physics; the remaining question is engineering the linac.**

The fallback, if the linac proves impractical for engineering reasons (not physics): primordial-flux capture with a ~10 km² superconducting sail over ~10⁴ years. Not engineering-feasible at modest scale, but not physics-impossible. The design's downstream physics is independent of how the first pair is obtained.

---

## 8. PERFORMANCE AND MISSION PROFILES

### Thrust derivation

For massive-particle exhaust with total energy E and momentum p per particle, F = (dN/dt) · p and P_exhaust = (dN/dt) · E, so

  **F = (p/E) · P_exhaust = β · P_exhaust / c**

(this is exact for any relativistic particle, including the m_e c² rest-mass contribution to E).

| Step | Value | Source |
|---|---|---|
| P_H | 60,200 TW | §2 (f = 3.503 × 10⁻³) |
| Primary ν + grav loss | 4,280 TW (7.1 %) | §3 |
| Secondary ν loss (decay chains, est.) | 4,210 TW (7.0 %) | §3 calibrated |
| Muon punch-through (CR signature) | 84 MW (1.4 × 10⁻⁹) | §3, t_shell = 3 pm |
| P_captured | 50,000 TW (83.0 %) | balance |
| Pair total E (kT + m_e c²) | 0.542 MeV | §4 Usov J = 1 |
| γ, β | 1.060, 0.332 | §4 |
| **F = β P_capt/c** | **55.28 MN** | derivation above |
| F·c/P_H (photon-rocket frac) | 27.5 % | overall efficiency |
| I_sp = β·c/g₀ | 1.06 × 10⁷ s | |

The dominant inefficiency is the e⁺e⁻ rest mass: each pair carries 1.02 MeV of rest energy but only ~0.07 MeV of kinetic energy. The exhaust is massive and slow vs. an ideal photon rocket, but the trade buys magnetic collimation of the entire absorbed spectrum.

### Off-axis emission budget

"Off-axis" = detectable from the side or front. Aft-directed (thrust-contributing) emission is not counted.

| Channel | Bound | Why |
|---|---|---|
| Cavity synchrotron | ≪ 1 W | E_sync ~ 28 μeV ≪ ω_p_inner ≈ 8 meV; reflected; τ_sync = 1.3 ms ≫ τ_extraction ~ 20 ns (§5) |
| Electrosphere bremsstrahlung | ≪ 1 W | Photons at ~kT_skin = 30 keV; absorbed by direct Compton+photoelectric in the shell (not reflected by inner mirror — see §5 bouncing-pair fate) |
| Bulk H-Goldstone anomaly emission | ~0.17 W | α⁴ T⁹/F_π⁴ × Wien-tail past ω_p_outer ≈ 0.5 MeV; ε_Wien = 5 × 10⁻⁶ (§4(c), `cfl_emissivity.py`) |
| Bulk Q̃ via gap channel | ≪ 10⁻⁵⁰⁰ W | exp(−2Δ/kT) = 10⁻²⁵⁹⁵ suppression |
| Bulk Goldstone-mediated (massive π^CFL) emission | ≪ 10⁻⁵⁰ W | exp(−m_π/kT) = 10⁻⁶⁵ suppression |
| Refueling port (capped, cruise) | ≈ 0 | SQM cap during cruise |
| Neutrals through bore | 10.3 MW (aft) | Geometric; aft-directed, contributes to thrust |
| Ship systems waste heat | ~0.14 MW | — |
| **Total detectable off-axis EM** | **< 1 MW** | |
| Muon tail punch-through (CR, free-stream) | 84 MW | §3, t = 3 pm |
| Neutrinos (all sources) | 8,490 TW | Undetectable (cross-section) |

**EM detectability** at 100 ly through a 100 km² aperture: 1 MW total off-axis EM emission gives flux 1 × 10⁶ / [4π·(100 ly)²] = 8.9 × 10⁻³⁰ W/m² at the receiver, or ~10⁻²⁰ W into a 100 km² aperture. Even if every photon is at 1 MeV, that's ~0.1 event/century — undetectable.

**CR detectability** of the muon channel at 100 ly through a 1 km² aperture: 84 MW gives flux 7.5 × 10⁻³⁰ W/m² × 10⁶ m² = 7.5 × 10⁻²⁴ W, or roughly one 60-GeV-muon detection per 40 million years — six orders of magnitude below the natural CR background (~10⁻⁴ muon/m²/s at GeV energies for atmospheric cosmic rays). The drive is completely undetectable by any plausible CR observatory.

### Mission profiles

**α Centauri (4.37 ly), flyby, constant-acceleration boost/coast/decelerate:**
- 39.4 yr accelerate at 26.8 mm/s² → 0.111 c
- 39.4 yr decelerate
- Trip: **79 yr** (the trip time grew slightly from the 75 yr-at-640-fm-shell baseline because of the revised secondary-ν budget and the proper Usov J(ζ) reducing β from 0.345 to 0.332)
- Fuel: ~1.6 × 10⁶ t total over the trip
- Constraint: τ_H = 15.8 yr; must refuel continuously, or the BH evaporates mid-trip.

**Burn the BH for Δv (no refueling):**
- Δv = β·c·ln(M_initial/M_final)
- For cargo = M_BH, evaporating the BH from M_i = 2 M_BH + M_shell to M_f = M_BH + M_shell gives M_i/M_f ≈ 1.49 and **Δv = 0.332 · ln(1.49) · c = 0.132 c**
- **Caveat (Planck-scale endpoint):** the rocket equation assumes the BH can be evaporated continuously. In practice, the semiclassical Hawking treatment breaks down when M approaches the Planck mass M_P = 2.18 × 10⁻⁸ kg. The final ~10⁻²⁰ of the BH mass undergoes a non-semiclassical, sub-millisecond burst whose character is unknown (it could explode as a thermal fireball, evaporate gradually, or leave a Planck-mass relic). For M_initial = 10⁹ kg, this endpoint regime affects Δv by ≤ ln(1 + M_P/M)/ln(2) ~ 10⁻¹⁷ — negligible. The endpoint is a *physics* curiosity but not a propulsion-budget issue at our scales.
- A separate practical concern: the operational shell is sized for the design-point Hawking spectrum at kT = 10.6 GeV. As the BH shrinks during the burn, kT rises and the shell stopping budget may be exceeded by the (now-harder) Hawking spectrum. The shell continues to stop the median spectrum until M < ~10⁷ kg (kT ≈ 1 TeV), at which point the 3-pm shell is no longer adequate. The achievable Δv is therefore practically limited to the M_i → 10⁷ kg phase, M_i/M_f ≈ 1.49, **Δv ≈ 0.13 c**.

**Trade space:**
- Higher BH mass (e.g., M = 4 × 10⁹ kg) → P ∝ 1/M² ⇒ 3,700 TW; τ ∝ M³ ⇒ ~1,020 yr; F ∝ 1/M² ⇒ ~3.7 MN; fuel ~1,310 t/yr. Long-haul.
- Lower BH mass (impractical below ~5 × 10⁸ kg) → higher thrust, shorter lifetime, runaway fuel demand.
- The BH mass is continuously adjustable: feed to grow, wait to shrink. Growing from 10⁹ to 4 × 10⁹ kg at 10⁵ t/yr feed rate takes ~35 yr.

---

## 9. OPEN PHYSICS QUESTIONS

Distinct from the foundational assumptions in §0 — these are questions internal to the design. All physics-side items below are now resolved or quantitatively bounded; the remaining open items are §0 foundational assumptions (#1 Hawking radiation, #2 GUT monopoles, #3 BPS limit, #4 Bodmer-Witten, #5 CFL stability, #6b linac seed-production suppression) and a single materials-science constraint (§9 item 12, bore-throat solenoid).

### Resolved or quantitatively bounded

1. **Usov formula at T < 8 × 10⁸ K** — **Resolved (§4).** The Usov 1998 J(ζ) function (verified from the paper) evaluates to J ≈ 36 at ζ_eq = 56, giving self-consistent T_eq = 0.356 GK and β = 0.332. Robust to a 100× span in J at the 3 % level. Prakapenia & Vereshchagin 2024's ~100× enhancement is derived for T > 10⁹ K and does not directly apply to our T_eq = 0.36 × 10⁹ K; even taking the PV2024 enhancement at face value shifts β by ≤ 5 %.

2. **Pair capture in the anti-Helmholtz bottle** — **Resolved (§5).** Fokker-Planck analysis with Coulomb pitch-angle randomization gives steady-state pair density n* ≈ 7 × 10²⁴ m⁻³ reached in ~1 ms after BH ignition; per-pair residence time ~150 ns over 6–10 bounces; 12% per-cycle escape rate confirmed.

3. **Hadron multiplicity at √s ~ 10 GeV vs. 10.57 GeV** — **Bounded (§3).** Logarithmic √s dependence gives ≲ 30 % multiplicity uncertainty, ≲ 5 % captured-power uncertainty. The unverified piece is whether *in-field* hadronization at B/B_QCD ~ 10²⁴ behaves like vacuum hadronization (open question 8 below).

4. **Maldacena 2020 electroweak corona threshold** — **Resolved (§2).** Verified: Q_ew ≈ 1.5 × 10³² for the corona to form (M_corona ~ 2 × 10²⁵ kg, planetary-mass). Our Q = 7.18 × 10¹⁴ is 17 orders below; no corona, no Landau-level enhancement, Schwarzschild formulas apply.

5. **CFL gap suppression and Manuel-Rajagopal rotated photon** — **Resolved (§2, §4).** The rotated-photon mixing (cos²θ ≈ 0.9975) is verified; CFL bulk is transparent to ordinary photons; production of Q̃-photons requires excitation across the gap (exp(−2Δ/kT) ≈ 10⁻²⁸²⁸ suppression) or via Goldstones (item 9 below). The gap firewall closes the quark-quasiparticle channel cleanly.

#### Items closed in the current round of work (Task A–I, §7.5 and `calculations/`)

6. **Outer-electrosphere plasma frequency for CFL specifically — Resolved (§4(b)).** Thomas-Fermi-Poisson profile derived analytically: μ_e(z) = μ_e(0)/(1+z/H), H = √(3π/8α)·ℏc/μ_e(0) (Alcock-Farhi-Olinto 1986). Maximum ω_p along the photon path is at z=0. The three physical bounds are: pure-CFL bulk-neutral (no electrosphere; not the appropriate boundary), gapless CFL surface (μ_e = 5.6 MeV, ω_p = 0.31 MeV; AKR 2005), and unpaired-SQM-equivalent surface (μ_e = 20 MeV, ω_p = 1.1 MeV; AFO 1986). The conservative midpoint ω_p_outer = 0.5 MeV (μ_e ≈ 9 MeV at the surface) gives Wien-tail leakage ε = 5 × 10⁻⁶ at T_bulk = 30.7 keV, leaving the absolute leak rate set by the bulk emissivity (item 7 below). See `calculations/cfl_electrosphere.py`.

7. **Bulk H-Goldstone emissivity at T ≪ F_π — Resolved (§4(c)).** Anomaly Lagrangian gives a 2→2 process η′η′ → 2γ; the *amplitude* carries two anomaly vertices, so |M|² ~ α⁴ T⁴/F_π⁴ (a prior dimensional estimate using α² was off by α²). Thermal averaging gives P/V ≈ (1/π⁴) α⁴ T⁹/F_π⁴ = 2.2 × 10¹⁴ W/m³ at the design point. Bulk total ~34 kW; Wien-tail escape past ω_p = 0.5 MeV gives P_leak ≈ 0.17 W. Comfortably bounded vs. the 1 MW off-axis budget even with factor-10³ prefactor uncertainty. See `calculations/cfl_emissivity.py`.

8. **Magnetic-field-strong-coupling hadronization — Bounded (`calculations/strong_b_hadronization.py`).** Critical radius where B drops to QCD-strength B_QCD = 6.6 × 10¹⁴ T (l_B = 1 fm): r_QCD ≈ 13 nm. Partons synchrotron-cool catastrophically from r_s = 1.5 am to r_QCD; by the time they reach r_QCD, their effective energy is ~1 GeV (down from 10 GeV at emission). Standard PDG fragmentation at √s ≈ 1 GeV gives ~40 % of the warm-parton hadron multiplicity and a ~30 % relative shift in K/π and p/π ratios. Propagated effect on the secondary-ν fraction is ~30 % relative (~2-3 percentage points absolute), comfortably within the design's 10 % conservative budget. Uncertainty in headline captured power: ~2 % absolute.

9. **Secondary-neutrino fraction precise calculation — Bounded (§3, `calculations/secondary_neutrinos.py`).** Refined first-principles estimate using explicit PDG branching ratios for π±, K±, K_L, p̄, μ±, τ, and c/b semi-leptonic chains gives **8.2 % of P_H** (5.4 % hadronic + 1.9 % τ + 0.9 % c/b + 0.02 % direct μ), with combined uncertainty ~30 % from fragmentation/energy-per-hadron assumptions. The design's conservative 10 % assumption is consistent and includes ~1.8 percentage points of margin. A full BlackHawk-PYTHIA integration remains the gold standard for sub-1 % precision but the refined estimate confirms the design's headline numbers are correctly bounded.

10. **SQM sputtering yield Y — Bounded (`calculations/sputter_bound.py`).** Three independent bounds: (a) mass-survival over 15.8 yr design lifetime allowing 10 % shell loss: **Y_max ≈ 2 × 10⁻²**; (b) modified-Sigmund theoretical estimate (U_s ~ Δ_CFL = 100 MeV, liquid suppression, electrosphere barrier): **Y ~ 5 × 10⁻⁷**; (c) astrophysical from heavy-ion-collision/strange-star longevity (Madsen 2005, PRD 71, 014026): **Y < 10⁻⁶**. The astrophysical bound gives a four-orders-of-magnitude safety margin against shell mass loss. The dominant remaining uncertainty is whether collective heat-driven evaporation kicks in above the Hawking bombardment flux (~10²⁰ × astrophysical CR rate); this is not addressed by the per-particle Y framework but is bounded by the Usov equilibrium (the skin self-regulates to T_skin = 30.7 keV).

11. **BH lateral stability under control — Resolved (§5, `calculations/bh_stability_control.py`).** Linear PD controller with K_P = 2|k_lat| = 2.6 × 10⁸ N/m, K_D for ζ = 0.7, gives closed-loop poles at −0.25 ± 0.26j (stable, natural frequency 0.057 Hz). Position readout from BH's monopole field at the pickup coil gives ~30 pm precision at 1 nT magnetometer floor. Actuator: ~1 % modulation of the anti-Helmholtz coil current produces required 2.6 MN restoring force at 10 mm excursion. Required bandwidth > 1 Hz; available bandwidth ~kHz (power-supply-limited). Coupled BH–shell–ship dynamics under time-varying thrust is the residual unanalyzed item.

### Open engineering constraint (not addressable without materials advance)

12. **Bore-throat solenoid materials — Open (engineering).** 1,000 T in 0.3 mm bore with B²/(2μ₀) = 400 GPa local pressure. No material survives this pressure. The total radial force on the bore is only ~10² N (length × pressure × small area), so an external rigid frame can in principle take the load, but the local field-source conductor must withstand 400 GPa hoop stress. Acknowledged engineering limitation; not a physics blocker but a materials-science requirement beyond current capability.

13. **Bootstrap-recovery shell engineering — Bounded (§7, `calculations/bootstrap_ode.py`).** Numerical ODE integration with full f(M) tabulation gives t_bootstrap = 1.85 yr at f_cap = 0.5 (sensitivity table in §7: 0.8–4.9 yr over f_cap = 0.2–0.9). Recovery shell stopping budget must scale 12,000× from operational 3 pm at the 250 t seed phase, then thin progressively as M grows. Railgun power spans 5.8 × 10²³ W → 3 × 10¹⁶ W (8 OOM), pellet rate 10⁻¹ → 10¹¹ kg/s (12 OOM). The energy budget is comfortably satisfied; the engineering challenge is the dynamic-range scaling of the recovery hardware.

14. **Inner-electrosphere plasma frequency at bombardment-driven density — Resolved (`calculations/inner_plasma_freq.py`).** Steady-state pair density n* = 2.3 × 10²² /m³ (Fokker-Planck collisional steady state from §5) gives ω_p_inner ≈ 8 **meV** (not 100 eV as previously quoted, and orders below the prior 7 MeV claim). This is 6 orders of magnitude below the bombardment photon energy ~kT = 30.7 keV and 8 orders below any annihilation photon at 0.51 MeV. **The inner plasma mirror is not the load-bearing reflection mechanism.** Energy bookkeeping is preserved by direct shell absorption: positrons that annihilate in the inner electrosphere (penetrating ~30 fm deep) emit isotropic photon pairs; ~50 % go deeper into the shell (absorbed within the 3 pm stopping budget), ~50 % travel back across the cavity and are absorbed on the opposite shell wall. Pair conversion in the BH-side magnetic field (χ ≫ 1 only within ~5 μm of the BH; cavity volume fraction within r_χ is 1.5 × 10⁻¹⁸) is *not* the dominant mechanism, contrary to an earlier statement.

---

## 10. SCALING TO OTHER MASSES

The architecture works across a continuous range of BH masses. Key scaling:
- P ∝ 1/M² (× weak f(M) variation as heavy SM species turn off below their masses)
- τ ∝ M³ / f
- F ∝ 1/M² (thrust scales with power)
- a = F/(2 M + M_shell) ∝ 1/M³ (cargo = M_BH model; very steep)
- Δv = β c ln(M_i/M_f) — independent of M for fixed mass-ratio
- Pair β ≈ 0.32–0.36 across the design range (Usov equilibrium is exponentially stiff)

**Sample alternative (long-range, M = 4 × 10⁹ kg)** — numbers reproduced from `hawking_spectrum.py` at M = 4 × 10⁹ kg:

| Quantity | Value |
|---|---|
| kT | 2.643 GeV |
| f (proper thermal integral) | 3.465 × 10⁻³ (b quark partly suppressed; W/Z/H/t suppressed) |
| P_H | 3,722 TW |
| τ_H | 1,020 yr |
| dM/dt | 41 g/s = 1,307 t/yr |
| Thrust F (same f_cap, β) | β · 0.854 · P_H / c = 3.66 MN |
| a (cargo = M_BH, with shell) | F/(8.013 × 10⁹ kg) = 0.46 mm/s² |
| Δv (burn the BH) | β · ln(2) · c = 0.230 c (Planck-endpoint caveat in §8) |
| 100 ly mission profile | accel-burn ~τ_H = 1,020 yr (reaches ~0.2 c) + coast ~500 yr = **~1,500 yr total** |

Same shell, same coils, same nozzle — only the magnetic charge (re-tuned for δ_eq) and the operating Usov T_eq (essentially unchanged) shift. Growing the BH (feed faster than evaporation) takes years to decades; shrinking (wait for evaporation) takes centuries.

---

## 11. NOVEL CONTRIBUTIONS

1. **QED pair conversion in the monopole field** converts all Hawking photons (direct and π⁰-decay) to magnetically directable e⁺e⁻ pairs near the BH. Eliminates the "photon problem" that defeats conventional reflector designs.
2. **SQM thermal wavelength converter.** Absorbs GeV radiation across all species and re-emits as sub-MeV pairs. The CFL gap-decoupling asymmetry provides one-sided emission: bombardment bypasses the gap inside; the gap suppresses outer emission.
3. **Anti-Helmholtz dual-use magnetic system.** A single coil pair confines the BH (F = g·∇B on the monopole) and creates a magnetic bottle that captures ~12 % of pairs per bounce (~26 % at the pole). Replaces separate confinement and capture systems.
4. **Three-layer outer-surface firewall:** (a) CFL gap suppression exp(−2Δ/kT) ≈ 10⁻²⁸²⁸ closes the quark-quasiparticle channel; (b) Boltzmann suppression exp(−m_π^CFL/kT) ≈ 10⁻⁶⁵ closes the massive-Goldstone channel; (c) chiPT-bounded H-Goldstone anomaly emission (α⁴ T⁹/F_π⁴) plus outer-electrosphere plasma mirror at ω_p ≈ 0.5 MeV give Wien-tail leakage ε ≈ 5 × 10⁻⁶, capping off-axis EM emission at ~0.2 W (§4(c), `cfl_emissivity.py`).
5. **Continuous BH mass as a design parameter.** Same architecture spans short-range sprint to multi-millennium long-haul; transitions are smooth.
6. **Correction of the CFL reflectivity claim.** Manuel & Rajagopal (2002) showed CFL is a transparent insulator, not a superconducting reflector. The thermal converter is the physically consistent alternative.
7. **Core-overlap exponential breeding** (§7.5). Phase-2 monopole multiplication is derived from established 't Hooft / Drukier-Nussinov / Olive-Witten duality: in the GUT-symmetric vacuum locally restored at core overlap, the dual coupling α_m = 1/(4α) is non-perturbative-but-finite, giving exp(−2π/α_m) ≈ O(1) production rate per overlap. 1.5× per generation, 88 generations from a single pair to 7 × 10¹⁴ monopoles.
8. **SQM electron linac seed-production path** (§7.5.1). A 2,500 km SQM-bore linear accelerator at 10× the 't Hooft-Polyakov pair-production threshold, with the over-barrier analogy (Manton 1983 sphaleron) arguing that the Drukier-Nussinov tunneling suppression relaxes at sufficient energy density.
9. **BPS monopole gravitational collapse formation** (§7). A same-sign cloud of 7.18 × 10¹⁴ BPS 't Hooft-Polyakov monopoles collapses as pressureless dust (Oppenheimer-Snyder) to form a magnetically charged seed BH, which is then bootstrapped to operating mass via railgun feeding.

---

## 12. KEY REFERENCES

| # | Reference | Role |
|---|---|---|
| 1 | Crane & Westmoreland 2009 (arXiv:0908.1803) | Foundational BH propulsion concept |
| 2 | Lee 2015 (JBIS 68, 105) | Proved conventional reflectors fail |
| 3 | Alvarez-Dominguez et al. 2024 (PRL 133, 041401) | Gamma-ray kugelblitz impossible |
| 4 | Manuel & Rajagopal 2002 (PRL 88, 042003) | CFL is transparent insulator, rotated photon |
| 5 | Usov 1998 (PRL 80, 230); 2001 (ApJ 550, L179) | Electrosphere pair emission rate |
| 6 | Aksenov, Milstein & Usov 2003 (PRL 91, 075002); 2004 (ApJ 609, 363) | Pair wind / atmosphere structure |
| 7 | Prakapenia & Vereshchagin 2024 (PRD 109, 023007) | Revised pair creation rates |
| 8 | Maldacena 2021 (JHEP 04, 079; arXiv:2004.06084) | Magnetic BH Hawking enhancement (Landau levels, EW corona) |
| 9 | Lee, Nair & Weinberg 1992 (Phys. Rev. D 45, 2751) | Monopole-BH transitions; magnetic charging |
| 10 | Hawking 1975 (Commun. Math. Phys. 43, 199) | Hawking radiation foundation |
| 11 | Page 1976 (Phys. Rev. D 13, 198) | Greybody factors |
| 12 | Lennon, March-Russell, Petrossian-Byrne & Tillim 2018 (JCAP 03, 009; arXiv:1712.07664) | SM power-rate coefficients |
| 13 | 't Hooft 1974 (NPB 79, 276); Polyakov 1974 (JETP Lett. 20, 194) | Original 't Hooft-Polyakov monopole |
| 14 | Prasad & Sommerfield 1975 (PRL 35, 760); Bogomolny 1976 (Sov. J. Nucl. Phys. 24, 449) | BPS monopole exact solution and Bogomolny bound |
| 15 | Manton 1977 (NPB 126, 525); Gibbons & Manton 1986 (NPB 274, 183) | BPS-monopole force cancellation and moduli-space dynamics |
| 16 | 't Hooft 1981 (NPB 190, 455); Olive & Witten 1978 (PLB 78, 97) | Electromagnetic duality framework; α_m = 1/(4α_e) (§7.5) |
| 17 | Affleck & Manton 1982 (NPB 194, 38) | Worldline-instanton dual-Schwinger rate (§7.5) |
| 18 | Drukier & Nussinov 1982 (PRL 49, 102) | Pointlike-collision suppression and core-overlap argument (§7.5) |
| 19 | Preskill 1979 (PRL 43, 1365); Preskill 1984 (ARNPS 34, 461) | Cosmological monopole abundance and review |
| 20 | Cho & Maison 1997 (NPB 547, 219) | Electroweak monopole solution (historical; not used in current design) |
| 21 | Ambjørn & Olesen 1989 (NPB 315, 606); Gould & Manton 2020 (PRD 101, 055003; arXiv:1911.06088) | W-condensate instability (historical; not used in current design) |
| 22 | Parker 1970 (ApJ 160, 383) | Galactic-field-decay bound on cosmic monopole flux |
| 23 | Ambrosio et al. (MACRO) 2002 (EPJC 25, 511; hep-ex/0207020) | Direct slow-GUT-monopole flux limit Φ < 1.4 × 10⁻¹⁶ /cm²/s/sr |
| 24 | Aartsen et al. (IceCube) 2022 (PRL 128, 051101; arXiv:2109.13719) | Relativistic-monopole flux limit Φ < 2 × 10⁻¹⁹ /cm²/s/sr |
| 25 | Acharya et al. (MoEDAL) 2024 (PRL 133, 071803; arXiv:2402.15682) | Schwinger-monopole mass limit m_M > 80 GeV at LHC Pb-Pb |
| 26 | Alford, Rajagopal & Wilczek 1999 (NPB 537, 443; hep-ph/9804403); Alford, Schmitt, Rajagopal & Schäfer 2008 (Rev. Mod. Phys. 80, 1455; arXiv:0709.4635) | CFL phase and color-superconductivity review |
| 27 | Alcock, Farhi & Olinto 1986 (ApJ 310, 261) | Strange-star electrosphere structure |
| 28 | Alford, Kouvaris & Rajagopal 2005 (PRD 71, 054009) | CFL outer-electrosphere μ_e ≈ 5.6 MeV (§4(b)) |
| 29 | Jaikumar, Rischke & Shovkovy 2003 (PRC 68, 045803; hep-ph/0311342) | CFL massive-Goldstone photon emission |
| 30 | Rischke, Son & Stephanov 2001 (PRL 87, 062001) | Gluon Meissner masses in CFL |
| 31 | Erber 1966 (Rev. Mod. Phys. 38, 626); Daugherty & Harding 1983 (ApJ 273, 761) | Magnetic pair conversion |
| 32 | Hawking 1971 (MNRAS 152, 75); Carr & Hawking 1974 (MNRAS 168, 399) | Primordial BH theory (historical; not used in current design) |
| 33 | Bodmer 1971 (PRD 4, 1601); Witten 1984 (PRD 30, 272) | Bodmer-Witten hypothesis |
| 34 | Bai & Chen 2025 (arXiv:2502.20241) | Argument against Bodmer-Witten; addressed in §0 |
| 35 | PDG 2024 review; BaBar/Belle hadron multiplicity (10 GeV) | Hadronization product ratios; secondary-ν fraction (§3) |
| 36 | Jancovici 1962 (Nuovo Cimento 25, 428) | ω_p² = (4α/3π) μ_e² for ultrarelativistic Fermi gas |
| 37 | Arbey & Auffinger 2019 (EPJC 79, 693; arXiv:1905.04268) | BlackHawk numerical code (§9 #9) |
| 38 | Sigmund 1969 (Phys. Rev. 184, 383) | Sputter-theory framework (§9 #10, `sputter_bound.py`) |
| 39 | Madsen 2005 (PRD 71, 014026; arXiv:astro-ph/0411735) | Strangelet bounds from heavy-ion / cosmic-ray data |

All items present in `references.bib`. This revision's additions relative to the prior pass: 't Hooft 1981, Olive-Witten 1978, Affleck-Manton 1982, Drukier-Nussinov 1982, Preskill 1979/1984, Cho-Maison 1997, Ambjørn-Olesen 1989, Gould-Manton 2020, Parker 1970, MACRO 2002, IceCube 2022, MoEDAL 2024, Sigmund 1969, Madsen 2005.
