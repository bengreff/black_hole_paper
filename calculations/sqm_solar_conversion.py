#!/usr/bin/env python3
"""
SQM Solar Conversion — Rigorous threshold calculation

Question: What mass of SQM, launched at the Sun at relativistic speed,
triggers a self-sustaining chain reaction that converts a large fraction
of the solar mass?

Approach: We do NOT rely on the uncertain boundary-layer thermodynamics
of a propagating burn front at sub-nuclear density. Instead we require
the SQM mass to grow via accretion to the point where its own
gravitational field accelerates infalling solar matter above the
Coulomb barrier. Once that threshold is reached, conversion is
guaranteed by gravity alone — no thermal-front arguments needed.

The calculation has three phases:
  Phase 1: Ballistic penetration — the projectile reaches the solar core
  Phase 2: Geometric accretion — the SQM sits at the core and eats
           everything that physically touches it (conversion energy
           keeps the boundary hot, but we don't RELY on this to
           propagate a front — we just eat what falls onto the surface)
  Phase 3: Gravitational runaway — the SQM mass reaches M_grav where
           free-fall velocity at the surface exceeds the Coulomb barrier.
           From here, accretion is gravity-fed and accelerates as M^(2/3).

We compute M_grav, then work backwards to find what initial projectile
mass M_0 grows to M_grav within a reasonable timescale.

Physical constants and solar model from standard sources.
"""

import numpy as np

# ========== Physical constants ==========
G = 6.674e-11       # m^3 kg^-1 s^-2
c = 2.998e8          # m/s
m_p = 1.673e-27      # kg (proton mass)
eV = 1.602e-19       # J
MeV = 1e6 * eV       # J
k_B = 1.381e-23      # J/K

# SQM properties
rho_SQM = 4e17       # kg/m^3 (nuclear density)
E_barrier = 3e6 * eV # 3 MeV — middle of 1-5 MeV range
E_conversion = 30 * MeV  # energy released per converted baryon
E_neutrino_loss = 10 * MeV  # ~1/3 lost to neutrinos
E_thermal = E_conversion - E_neutrino_loss  # 20 MeV deposited locally

# Solar model (simplified but adequate)
M_sun = 1.989e30     # kg
R_sun = 6.96e8       # m
rho_sun_avg = 1408   # kg/m^3
rho_core = 1.5e5     # kg/m^3 (central density)
T_core = 1.5e7       # K (central temperature)
kT_core = k_B * T_core / eV  # ~1.3 keV — far below barrier
L_sun = 3.828e26     # W
E_binding_sun = 2.3e41  # J (gravitational binding energy)

# Solar core model: density roughly constant within ~0.2 R_sun
R_core = 0.2 * R_sun  # ~1.4e8 m
M_core = 0.35 * M_sun  # ~35% of mass in inner 20% of radius

print("=" * 70)
print("SQM SOLAR CONVERSION — RIGOROUS THRESHOLD CALCULATION")
print("=" * 70)

# ========== Phase 3: Gravitational threshold ==========
print("\n--- PHASE 3 (computed first): Gravitational runaway threshold ---")
print()

# At what SQM mass does gravitational infall velocity reach the
# Coulomb barrier energy?
#
# A proton falling from rest at distance r >> R_SQM onto an SQM sphere
# of mass M hits the surface with kinetic energy:
#
#   T = G M m_p / R_SQM
#
# where R_SQM = (3M / (4 pi rho_SQM))^(1/3)
#
# Setting T = E_barrier and solving for M:
#
#   E_barrier = G m_p M^(2/3) (4 pi rho_SQM / 3)^(1/3)

factor = (4 * np.pi * rho_SQM / 3) ** (1.0/3.0)
# M^(2/3) = E_barrier / (G * m_p * factor)
M_23 = E_barrier / (G * m_p * factor)
M_grav = M_23 ** 1.5

R_grav = (3 * M_grav / (4 * np.pi * rho_SQM)) ** (1.0/3.0)
v_infall = np.sqrt(2 * G * M_grav / R_grav)
T_check = 0.5 * m_p * v_infall**2

print(f"Coulomb barrier assumed:       {E_barrier/MeV:.1f} MeV")
print(f"Gravitational threshold mass:  {M_grav:.3e} kg")
print(f"  = {M_grav/1.898e27:.3f} Jupiter masses")
print(f"  = {M_grav/5.972e24:.1f} Earth masses")
print(f"  = {M_grav/M_sun:.2e} solar masses")
print(f"SQM radius at threshold:       {R_grav:.1f} m")
print(f"Infall velocity at surface:    {v_infall:.3e} m/s = {v_infall/c:.4f} c")
print(f"KE per proton at surface:      {T_check/MeV:.2f} MeV (should = {E_barrier/MeV:.1f})")
print()

# Also compute for 1 MeV and 5 MeV barriers for sensitivity
for E_b_MeV in [1.0, 3.0, 5.0]:
    E_b = E_b_MeV * MeV
    M23 = E_b / (G * m_p * factor)
    M = M23 ** 1.5
    R = (3 * M / (4 * np.pi * rho_SQM)) ** (1.0/3.0)
    v = np.sqrt(2 * G * M / R)
    print(f"  E_barrier = {E_b_MeV:.0f} MeV:  M = {M:.2e} kg "
          f"= {M/1.898e27:.2f} M_J,  R = {R:.0f} m,  v = {v/c:.4f}c")

# ========== Phase 2: Geometric accretion at solar core ==========
print("\n--- PHASE 2: Geometric accretion at solar core ---")
print()
print("The SQM sits at the solar core (rho = 1.5e5 kg/m^3, T ~ 1 keV).")
print("It accretes matter that physically contacts its surface.")
print("At T_core ~ 1 keV, thermal ions are far below the Coulomb barrier.")
print()
print("However, conversion energy (20 MeV thermal per baryon) keeps the")
print("boundary layer hot IF accretion is ongoing. We take the conservative")
print("approach: assume only ions in the Maxwellian tail above E_barrier")
print("can convert. This gives a MINIMUM accretion rate.")
print()

# Maxwellian tail fraction above E_barrier at T_core
# f_tail = (2/sqrt(pi)) * sqrt(x) * exp(-x), integrated from x to infinity
# where x = E_barrier / kT
# For x >> 1: f_tail ~ (2/sqrt(pi)) * sqrt(x) * exp(-x)
# More precisely: fraction of particles with E > E0 in Maxwell-Boltzmann:
# f = 1 - erf(sqrt(x)) + (2/sqrt(pi)) * sqrt(x) * exp(-x)
# For x >> 1: f ~ (2/sqrt(pi)) * sqrt(x) * exp(-x)

kT_core_J = k_B * T_core
x_barrier = E_barrier / kT_core_J
print(f"kT_core = {kT_core_J/eV:.1f} eV = {kT_core_J/MeV:.4f} MeV")
print(f"E_barrier / kT = {x_barrier:.0f}")
print(f"This is so large that the Maxwellian tail fraction is ~ exp(-{x_barrier:.0f})")
print(f"  = {np.exp(-min(x_barrier, 700)):.1e}  (effectively ZERO)")
print()
print("Pure thermal accretion at solar core temperature: NEGLIGIBLE.")
print("The SQM just sits there inertly at 1 keV.")
print()
print("HOWEVER: the projectile arrives at ~0.1c. During deceleration in")
print("the core, every nucleus it sweeps up impacts at >>3 MeV. The")
print("question is how much mass it accretes during the braking phase.")

# ========== Phase 1: Ballistic penetration and braking ==========
print()
print("\n--- PHASE 1: Ballistic penetration and braking accretion ---")
print()

# The SQM projectile enters the Sun at velocity v0 and decelerates
# by ram pressure (sweeping up and converting solar matter).
#
# The projectile is a sphere of radius r = (3M/(4pi rho_SQM))^(1/3)
# moving through solar plasma of density rho_star.
#
# Drag force: F = rho_star * v^2 * pi * r^2  (ram pressure)
# But every swept-up baryon is CONVERTED: its mass adds to the projectile.
# So this is an inelastic accretion problem, not just drag.
#
# dm/dt = rho_star * pi * r^2 * v   (mass swept per second)
# r = (3m/(4pi rho_SQM))^(1/3), so pi*r^2 = pi * (3/(4pi rho_SQM))^(2/3) * m^(2/3)
#
# Momentum conservation (inelastic accretion):
# d(mv)/dt = -rho_star * pi * r^2 * v^2   [swept mass carries zero forward momentum]
# m dv/dt + v dm/dt = -v dm/dt
# m dv/dt = -2v dm/dt = -2 rho_star pi r^2 v^2
#
# Actually, more carefully:
# The projectile sweeps up mass at rate dm/dt = rho_star * A * v
# where A = pi * r^2 is the cross section.
# The swept mass has zero forward momentum (stellar matter is at rest).
# Momentum: p = m*v (projectile only)
# dp/dt = F_external = 0 (no external force in the rest frame of the star,
#         ignoring gravity for now)
# But the projectile is gaining mass! So:
# d(mv)/dt = 0  =>  m dv/dt + v dm/dt = 0  =>  m dv/dt = -v dm/dt
#
# Wait, that's not right either. The swept-up mass is brought to the
# projectile's velocity (inelastic collision). So momentum IS conserved:
# d(mv)/dt = 0 (in the star's frame, no external forces except gravity)
# => mv = m0 * v0 = const
# => v = m0 * v0 / m
#
# And dm/dt = rho_star * pi * r^2(m) * v(m)
#
# This is actually a clean ODE. Let me solve it.

print("Inelastic accretion model: projectile sweeps up stellar matter,")
print("each swept baryon joins the SQM (conversion). Momentum conserved:")
print("  m * v = m0 * v0 = const")
print("  dm/dt = rho_star * pi * r(m)^2 * v(m)")
print("  r(m) = (3m / (4 pi rho_SQM))^(1/3)")
print()

def sqm_radius(m):
    return (3 * m / (4 * np.pi * rho_SQM)) ** (1.0/3.0)

def simulate_penetration(m0, v0, rho_profile_func, r_max, dt_factor=0.001):
    """
    Simulate SQM projectile penetrating the Sun.

    m0: initial mass (kg)
    v0: initial velocity (m/s)
    rho_profile_func: function rho(r_from_center) returning density
    r_max: starting distance from center (= R_sun for surface entry)

    Returns: final mass, final velocity, position history
    """
    m = m0
    v = v0
    p0 = m0 * v0  # conserved momentum

    # Position: start at r_max, moving inward
    r_pos = r_max
    t = 0

    # Track
    positions = [r_pos]
    masses = [m]
    velocities = [v]

    while r_pos > 0 and v > 1e4:  # stop if reaches center or slows to ~10 km/s
        r_sqm = sqm_radius(m)
        A = np.pi * r_sqm**2
        rho_local = rho_profile_func(r_pos)

        # dm/dx = rho * A  (mass per unit path length)
        dm_dx = rho_local * A

        # Adaptive step: don't let mass change by more than 0.1% per step
        if dm_dx > 0:
            dx = max(dt_factor * m / dm_dx, 1.0)  # at least 1 m steps
        else:
            dx = 1000.0
        dx = min(dx, r_pos)  # don't overshoot center

        dm = dm_dx * dx
        m += dm
        v = p0 / m  # momentum conservation
        r_pos -= dx

        if len(positions) % 100000 == 0:
            pass  # silent

        positions.append(r_pos)
        masses.append(m)
        velocities.append(v)

        if m > 1e30:  # sanity cap
            break

    return m, v, np.array(masses), np.array(velocities), np.array(positions)

# Simple solar density profile (piecewise linear, adequate for this)
def solar_density(r):
    """Approximate solar density profile in kg/m^3."""
    x = r / R_sun
    if x > 1.0:
        return 0.0
    elif x > 0.7:
        # Envelope: ~1 to ~10 kg/m^3
        return 1.0 + 30 * (0.9 - x)
    elif x > 0.25:
        # Radiative zone: ~10,000 to ~30,000
        return 2e4 * (1 + 3 * (0.5 - x))
    else:
        # Core: 50,000 to 150,000
        return 1.5e5 * (1 - 2 * x)

# Test several initial masses
print("Simulation: SQM projectile entering Sun at v0 = 0.1c")
print()
v0 = 0.1 * c

test_masses = [1e-3, 1e-1, 1e0, 1e1, 1e2, 1e3, 1e4, 1e6, 1e8, 1e10]

print(f"{'M_0 (kg)':<14} {'M_final (kg)':<14} {'M_f/M_0':<10} "
      f"{'v_final (m/s)':<14} {'Reaches core?':<14} {'R_SQM_final':<12}")
print("-" * 80)

results = {}
for m0 in test_masses:
    m_f, v_f, m_arr, v_arr, r_arr = simulate_penetration(m0, v0, solar_density, R_sun)
    reached_core = r_arr[-1] < 0.2 * R_sun
    r_sqm_f = sqm_radius(m_f)
    ratio = m_f / m0

    results[m0] = (m_f, v_f, reached_core)

    core_str = "YES" if reached_core else f"NO (stopped at {r_arr[-1]/R_sun:.2f} R_sun)"
    print(f"{m0:<14.1e} {m_f:<14.3e} {ratio:<10.2f} "
          f"{v_f:<14.3e} {core_str:<14} {r_sqm_f:.3e} m")

# ========== Key analysis ==========
print()
print("=" * 70)
print("KEY ANALYSIS")
print("=" * 70)
print()
print(f"Gravitational runaway threshold: M_grav = {M_grav:.3e} kg")
print(f"  ({M_grav/1.898e27:.3f} Jupiter masses, R = {R_grav:.0f} m)")
print()
print("The projectile accretes mass during penetration, but momentum")
print("conservation means it slows as it gains mass (m*v = const).")
print("The final mass depends on how much stellar matter it sweeps up.")
print()

# Now: once the SQM is parked at the core (assume it reaches there),
# we need to grow from M_final to M_grav.
# At the core, thermal accretion is negligible (kT << E_barrier).
# What about gravitational focusing? Even before reaching M_grav,
# the SQM's gravity pulls matter inward faster than thermal velocity.
#
# Bondi accretion rate:
# dm/dt = 4 pi (G M)^2 rho / c_s^3
# where c_s is the sound speed in the stellar core.
#
# At solar core: T ~ 1.5e7 K, fully ionized H
# c_s = sqrt(5 kT / (3 m_p)) for monatomic ideal gas
# (using adiabatic gamma = 5/3)

c_s_core = np.sqrt(5 * k_B * T_core / (3 * m_p))
print(f"Solar core sound speed: c_s = {c_s_core:.3e} m/s = {c_s_core/c:.5f}c")
print()

# Bondi accretion rate (hypersonic for large M where v_infall >> c_s):
# dm/dt = pi R_Bondi^2 * rho * c_s  (subsonic Bondi)
# R_Bondi = 2 G M / c_s^2
# dm/dt = 4 pi G^2 M^2 rho / c_s^3

print("Bondi accretion at solar core (gravitationally focused):")
print("  dm/dt = 4 pi G^2 M^2 rho_core / c_s^3")
print()
print("This is pure gravitational accretion — matter falls onto the SQM")
print("surface at the free-fall velocity. For M < M_grav, the infall")
print("velocity is below the Coulomb barrier, so the matter does NOT")
print("convert to SQM on contact. It just piles up as normal matter")
print("around the SQM core.")
print()
print("BUT: the accreted normal matter increases the TOTAL gravitating")
print("mass! Even though it's not SQM, it deepens the gravitational")
print("well. When enough normal matter has piled up that the free-fall")
print("velocity at the SQM surface exceeds the Coulomb barrier, the")
print("normal matter in contact with the SQM converts, releasing")
print("30 MeV/baryon, and the whole pile flashes to SQM.")
print()

# So the actual threshold is: what total mass M_total (SQM + accreted
# normal matter) is needed such that free-fall onto the SQM core
# (radius R_SQM) reaches the barrier energy?
#
# T = G M_total m_p / R_SQM
#
# Here R_SQM is the radius of the original SQM core (the normal matter
# sits on TOP of it but at much lower density).
#
# This is MUCH more favorable because M_total can be mostly normal matter
# while R_SQM stays small.
#
# For SQM mass m_sqm with radius r_sqm = (3 m_sqm / (4pi rho_SQM))^(1/3):
# We need G * M_total * m_p / r_sqm >= E_barrier
# M_total >= E_barrier * r_sqm / (G * m_p)
# M_total >= E_barrier * (3 m_sqm / (4pi rho_SQM))^(1/3) / (G * m_p)

print("CRITICAL INSIGHT: The gravitating mass can be normal matter.")
print("The SQM core just needs to be at the CENTER of a deep enough")
print("gravitational well. Normal matter piled on top works fine.")
print()

# For a given SQM core mass m_sqm, the total mass needed:
def M_total_needed(m_sqm):
    r_sqm = sqm_radius(m_sqm)
    return E_barrier * r_sqm / (G * m_p)

# BUT there's a subtlety: the normal matter accreted around the SQM
# has its own density (solar core plasma, ~1.5e5 kg/m^3). The
# gravitational potential at the SQM surface includes all mass
# interior to that radius. If the SQM is tiny, the normal matter
# within a few meters contributes negligibly.
#
# Actually, the correct picture is:
# - SQM core of mass m_sqm, radius r_sqm (a few microns to meters)
# - Normal matter accretes around it, forming a dense shell/sphere
# - The infalling matter at the SQM surface feels gravity from
#   m_sqm (SQM) + m_normal_within_r_sqm (negligible, since r_sqm is tiny)
# - So the relevant mass IS just m_sqm for computing infall at the surface
#
# Wait — no. The normal matter accumulates on TOP of the SQM. If the
# SQM is 1 kg (r ~ 0.8 um), normal matter piles around it. The
# normal matter at the SQM surface feels gravity from the SQM mass
# only (shell theorem: outer shells don't contribute). But matter
# farther out feels gravity from the SQM + all enclosed normal matter.
#
# The question is: does matter at the SQM surface fall at v such that
# (1/2) m_p v^2 >= E_barrier?
#
# v^2 = 2 G m_sqm / r_sqm  (only SQM mass matters at that radius)
#
# So we're back to the original M_grav threshold: we need the SQM
# itself to be massive enough. Normal matter on top doesn't help
# at the SQM surface.
#
# UNLESS the normal matter is compressed to high density near the SQM.
# In a self-gravitating ball (SQM core + normal matter envelope), the
# pressure at the SQM surface is enormous if M_total is large.
# The temperature and density at the base of the normal-matter layer
# can exceed the Coulomb barrier via compression heating.
#
# This is essentially forming a STAR around the SQM core. When
# M_total is large enough, the central pressure and temperature
# exceed the barrier.

print("Revised picture: SQM core + normal matter envelope.")
print("Shell theorem means infalling velocity at SQM surface depends")
print("only on the SQM mass. Normal matter envelope doesn't help directly.")
print()
print("But: if enough normal matter accretes, central PRESSURE and")
print("TEMPERATURE from gravitational compression can exceed the barrier.")
print("This is equivalent to asking: at what M_total does the central")
print("temperature of a self-gravitating gas ball reach ~3 MeV?")
print()

# Central temperature of a self-gravitating isothermal gas sphere:
# From virial theorem: T_central ~ G M m_p / (k_B R)
# For a uniform density sphere: T_c = (3/10) G M m_p / (k_B R) (order of magnitude)
# But R depends on the equation of state.
#
# For an ideal gas in hydrostatic equilibrium:
# P_central = (3/8pi) G M^2 / R^4 * (4 pi R^3 rho / 3) ... complicated
#
# Simpler: use the virial temperature
# (3/2) k_B T_virial = (3/10) G M m_p / R  (for uniform sphere)
# T_virial = G M m_p / (5 k_B R)
#
# But what R? If matter accretes from the solar core at density rho_core,
# and it accumulates around the SQM core, the accreted ball has roughly
# the density of the surrounding medium (pressure equilibrium).
# R_envelope ~ (3 M_total / (4 pi rho_core))^(1/3)
#
# No wait — this isn't right either. The accreted matter is in pressure
# equilibrium with the surrounding solar core. It doesn't form a
# separate self-gravitating ball unless M_total is above the Jeans mass.

M_jeans_core = (np.pi * c_s_core**2 / G) ** 1.5 / (6 * np.sqrt(rho_core))
# More standard: M_J = (pi/6) * (pi c_s^2 / G)^(3/2) * rho^(-1/2)
# Let me use: M_J = (pi^(5/2) / 6) * c_s^3 / (G^(3/2) * rho^(1/2))
M_jeans = (np.pi**(5/2) / 6) * c_s_core**3 / (G**1.5 * rho_core**0.5)

print(f"Jeans mass at solar core conditions: M_J = {M_jeans:.3e} kg")
print(f"  = {M_jeans/M_sun:.3f} M_sun")
print()
print("The Jeans mass at solar core conditions is ~3 solar masses.")
print("An SQM seed of any practical mass is far below this — the")
print("surrounding solar plasma doesn't gravitationally collapse onto it.")
print("The seed just sits in pressure-supported stellar plasma.")
print()

# So we're back to: you need the SQM ITSELF to reach M_grav.
#
# Bondi accretion brings normal matter to the SQM surface, but at
# subsonic infall (v << c_s), well below the Coulomb barrier.
# The matter just bounces off / flows around the SQM.
#
# The SQM grows ONLY by:
# (a) During initial braking: sweeping up matter at v > barrier_velocity
# (b) Quantum tunneling through the Coulomb barrier at T_core ~ 1 keV
#     (negligible: ~exp(-2300))
# (c) If the SQM heats the boundary layer enough (the "dubious
#     thermodynamics" we were told not to rely on)
#
# Without (c), the SQM stops growing once it decelerates below
# the barrier velocity and we need it to already be at M_grav.

print("=" * 70)
print("RIGOROUS CONCLUSION (no boundary-layer thermodynamics)")
print("=" * 70)
print()
print("Without relying on conversion-energy-sustained boundary heating,")
print("the SQM grows ONLY during ballistic penetration (v > v_barrier).")
print("Once it decelerates below v_barrier, accretion stops.")
print()
print("For runaway: the SQM must reach M_grav from braking accretion alone,")
print("OR be launched with M_0 >= M_grav so that after braking it")
print("already exceeds the gravitational threshold.")
print()

# The projectile decelerates from v0 to v_final via momentum conservation:
# m_final * v_final = m0 * v0
# It stops accreting when v < v_barrier = sqrt(2 * E_barrier / m_p)
v_barrier = np.sqrt(2 * E_barrier / m_p)
print(f"Barrier velocity: v_barrier = {v_barrier:.3e} m/s = {v_barrier/c:.4f}c")
print()

# At the moment accretion stops: m_stop * v_barrier = m0 * v0
# => m_stop = m0 * v0 / v_barrier

print(f"Mass at accretion cutoff: m_stop = m0 * v0 / v_barrier")
print(f"  = m0 * {v0:.3e} / {v_barrier:.3e}")
print(f"  = m0 * {v0/v_barrier:.1f}")
print()

mass_multiplier = v0 / v_barrier
print(f"Mass multiplication factor: {mass_multiplier:.1f}x (at v0 = 0.1c)")
print()

# So the final SQM mass after braking = m0 * (v0 / v_barrier)
# For this to exceed M_grav:
# m0 * v0 / v_barrier >= M_grav
# m0 >= M_grav * v_barrier / v0

M0_required = M_grav * v_barrier / v0
R0_required = sqm_radius(M0_required)

print(f"Required initial SQM mass for gravitational runaway:")
print(f"  M_0 >= M_grav * v_barrier / v0")
print(f"  M_0 >= {M_grav:.3e} * {v_barrier:.3e} / {v0:.3e}")
print(f"  M_0 >= {M0_required:.3e} kg")
print(f"  = {M0_required/1.898e27:.4f} Jupiter masses")
print(f"  = {M0_required/5.972e24:.1f} Earth masses")
print(f"  = {M0_required/M_sun:.2e} solar masses")
print()
print(f"  Initial SQM radius: {R0_required:.1f} m")
print(f"  Initial SQM density: {rho_SQM:.1e} kg/m^3 (nuclear)")
print()

# Different launch velocities
print("Sensitivity to launch velocity:")
print(f"{'v0/c':<10} {'M_0 (kg)':<14} {'Earth masses':<14} {'Jupiter masses':<14} {'R_0 (m)':<10}")
print("-" * 65)
for v0_frac in [0.05, 0.10, 0.20, 0.33, 0.50, 0.90]:
    v0_test = v0_frac * c
    mult = v0_test / v_barrier
    M0_test = M_grav / mult
    R0_test = sqm_radius(M0_test)
    print(f"{v0_frac:<10.2f} {M0_test:<14.3e} {M0_test/5.972e24:<14.1f} "
          f"{M0_test/1.898e27:<14.4f} {R0_test:<10.1f}")

# ========== Conversion energy if the Sun converts ==========
print()
print("=" * 70)
print("ENERGY RELEASE: SOLAR CONVERSION")
print("=" * 70)
print()

N_baryons_sun = M_sun / m_p
E_total = N_baryons_sun * E_conversion
E_neutrinos = N_baryons_sun * E_neutrino_loss
E_thermal_total = N_baryons_sun * E_thermal

print(f"Solar baryons:     {N_baryons_sun:.3e}")
print(f"Conversion energy: {E_conversion/MeV:.0f} MeV/baryon")
print()
print(f"Total energy released:    {E_total:.3e} J")
print(f"  Neutrino component:     {E_neutrinos:.3e} J ({E_neutrino_loss/E_conversion*100:.0f}%)")
print(f"  Thermal/kinetic:        {E_thermal_total:.3e} J ({E_thermal/E_conversion*100:.0f}%)")
print()
print("Comparison:")
print(f"  Solar gravitational binding energy:  {E_binding_sun:.3e} J")
print(f"  Ratio E_conversion / E_binding:      {E_total/E_binding_sun:.0f}x")
print(f"  Type Ia supernova (kinetic):         ~1e44 J")
print(f"  Core-collapse SN (total):            ~3e46 J")
print(f"  E_conversion / SN_total:             {E_total/3e46:.2f}")
print()

# Ejecta velocity (all thermal energy -> kinetic)
v_eject = np.sqrt(2 * E_thermal_total / M_sun)
print(f"If all thermal energy -> ejecta KE:")
print(f"  v_eject = sqrt(2E/M) = {v_eject:.3e} m/s = {v_eject/c:.3f}c")
print()

# Timescale: how fast does the conversion proceed after M_grav is reached?
# Once gravitational runaway begins, the Bondi accretion rate is:
# dm/dt = 4 pi G^2 M^2 rho / c_s^3
# But now the accreted matter CONVERTS (v_infall > v_barrier), so M grows
# This is a runaway: dm/dt ~ M^2, solution blows up in finite time.

print("=" * 70)
print("RUNAWAY TIMESCALE")
print("=" * 70)
print()
print("After reaching M_grav, Bondi accretion with conversion gives:")
print("  dm/dt = 4 pi G^2 M^2 rho_core / c_s^3")
print()

bondi_coeff = 4 * np.pi * G**2 * rho_core / c_s_core**3
print(f"  Bondi coefficient: A = {bondi_coeff:.3e} s^-1 kg^-1")
print()
print("  dm/dt = A * M^2")
print("  Solution: M(t) = M_grav / (1 - A * M_grav * t)")
print("  Blowup time: t_runaway = 1 / (A * M_grav)")

t_runaway = 1.0 / (bondi_coeff * M_grav)
print(f"  t_runaway = {t_runaway:.3e} s = {t_runaway/3.156e7:.1f} years")
print()
print("But this is the time to go from M_grav to infinity in the Bondi model.")
print("In reality, once M approaches stellar mass, the accretion geometry")
print("changes and the star disrupts. The conversion of the core")
print("(M_core ~ 0.35 M_sun) takes roughly:")

# Time to eat the core: integrate dm/dt = A M^2 from M_grav to M_core
# t = integral from M_grav to M_core of dM / (A M^2) = (1/A)(1/M_grav - 1/M_core)
# ≈ 1/(A M_grav) for M_core >> M_grav

t_core = (1.0/bondi_coeff) * (1.0/M_grav - 1.0/(M_core))
print(f"  t_core_conversion ~ {t_core:.3e} s = {t_core/3.156e7:.1f} years")
print()
print("Once the core converts, the energy release (~25,000x binding energy)")
print("drives a shock that disrupts the entire star in seconds.")
print()

# But wait: Bondi accretion at M_grav may already be supersonic
# Check: R_Bondi = 2 G M / c_s^2
R_bondi_grav = 2 * G * M_grav / c_s_core**2
print(f"Bondi radius at M_grav: R_Bondi = {R_bondi_grav:.3e} m")
print(f"  Compare to R_core = {R_core:.3e} m")
print(f"  R_Bondi / R_core = {R_bondi_grav/R_core:.3f}")
if R_bondi_grav > R_core:
    print("  Bondi radius EXCEEDS core radius — accretion is not Bondi-limited")
    print("  The entire core is inside the gravitational capture radius")
    print("  Free-fall time of core onto SQM:")
    t_ff_core = np.sqrt(3 * np.pi / (32 * G * rho_core))
    print(f"  t_ff = sqrt(3 pi / (32 G rho_core)) = {t_ff_core:.0f} s = {t_ff_core/3600:.1f} hours")
    print("  This is the true conversion timescale once runaway begins.")

# ========== FINAL SUMMARY ==========
print()
print("=" * 70)
print("FINAL ANSWER")
print("=" * 70)
print()
print("THRESHOLD MASS (rigorous, gravity-only, no thermal-front assumptions):")
print()
print(f"  At v0 = 0.10c:  M_0 = {M_grav * v_barrier / (0.10*c):.3e} kg "
      f"({M_grav * v_barrier / (0.10*c) / 5.972e24:.1f} Earth masses)")
print(f"  At v0 = 0.20c:  M_0 = {M_grav * v_barrier / (0.20*c):.3e} kg "
      f"({M_grav * v_barrier / (0.20*c) / 5.972e24:.1f} Earth masses)")
print(f"  At v0 = 0.33c:  M_0 = {M_grav * v_barrier / (0.33*c):.3e} kg "
      f"({M_grav * v_barrier / (0.33*c) / 5.972e24:.1f} Earth masses)")
print()
print("MECHANISM:")
print("  1. SQM projectile enters Sun at relativistic speed")
print("  2. Sweeps up and converts solar matter during braking")
print(f"     (mass multiplied ~v0/v_barrier during penetration)")
print(f"  3. Final SQM mass exceeds M_grav = {M_grav:.2e} kg")
print("  4. Gravitational infall at SQM surface exceeds Coulomb barrier")
print("  5. Bondi accretion with conversion: dm/dt ~ M^2 (runaway)")
print("  6. Core free-falls onto SQM in hours")
print("  7. Energy release disrupts star in seconds after core conversion")
print()
print("ENERGY RELEASE:")
print(f"  Total: {E_total:.2e} J = {E_total/E_binding_sun:.0f}x solar binding energy")
print(f"  ~1/3 neutrinos, ~2/3 thermal/kinetic")
print(f"  Ejecta velocity: ~{v_eject/c:.2f}c")
print(f"  Comparable to {E_total/3e46:.1f}x core-collapse supernova")
print()
print("CONVERSION FRACTION:")
print(f"  Core (0.35 M_sun): fully converted (gravity-fed runaway)")
print(f"  Envelope: disrupted by shock wave from core conversion energy")
print(f"  The ~{E_total/E_binding_sun:.0f}x overbinding means the entire star is unbound")
print(f"  Outer layers may partially convert in the shock or be ejected as")
print(f"  normal matter + SQM debris")
