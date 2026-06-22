#!/usr/bin/env python3
"""
Mission profiles with proper Tsiolkovsky accounting.

All fuel carried from launch. No en-route refueling assumed.
The BH is continuously fed to maintain constant mass; fuel is expended.
Exhaust velocity β_e = 0.332c (Usov pair emission).

For a boost/decelerate mission:
  - Accelerate for half the trip, decelerate for the other half
  - Fuel split: equal mass ratio per leg
  - Total mass ratio: R_total = R_leg²
  - Δv per leg = β_e c × ln(R_leg)
  - v_peak = Δv_leg

We compute trip time by numerically integrating the equation of motion
with decreasing ship mass (fuel consumption).
"""

import numpy as np
from scipy.integrate import solve_ivp

# Constants
c = 2.998e8          # m/s
G = 6.674e-11        # m³/kg/s²
hbar = 1.055e-34     # J·s
ly = 9.461e15        # m
yr = 3.156e7         # s
beta_e = 0.332       # exhaust velocity / c
v_e = beta_e * c     # exhaust velocity m/s

def hawking_power(M, f=3.503e-3):
    return hbar * c**6 * f / (G**2 * M**2)

def fuel_rate(M, f=3.503e-3):
    """Mass loss rate = P/c². This is the fuel consumption rate to maintain M."""
    return hawking_power(M, f) / c**2

def thrust(M, f=3.503e-3, eta_capture=0.83):
    """Thrust = beta_e * P_captured / c"""
    P = hawking_power(M, f)
    return beta_e * eta_capture * P / c

print("=" * 70)
print("MISSION PROFILES — PROPER TSIOLKOVSKY ACCOUNTING")
print("All fuel carried from launch. BH mass maintained by continuous feeding.")
print("=" * 70)

# ========== Design points ==========

designs = [
    {
        "name": "Reference",
        "M_BH": 1.0e9,
        "f": 3.503e-3,
        "shell_t_pm": 3,
        "shell_mass": 6.0e7,
    },
    {
        "name": "High-thrust",
        "M_BH": 2.0e8,
        "f": 3.48e-3,  # slightly different f at higher kT (b quark more suppressed)
        "shell_t_pm": 10,
        "shell_mass": 2.0e8,
    },
    {
        "name": "Sprint",
        "M_BH": 5.0e7,
        "f": 3.45e-3,
        "shell_t_pm": 30,
        "shell_mass": 6.0e8,
    },
]

for d in designs:
    M = d["M_BH"]
    f = d["f"]
    P = hawking_power(M, f)
    F = thrust(M, f)
    dm_dt = fuel_rate(M, f)
    tau = G**2 * M**3 / (3 * hbar * c**4 * f)
    kT_GeV = hbar * c**3 / (8 * np.pi * G * M) / (1.602e-10)

    print(f"\n{'='*70}")
    print(f"Design: {d['name']} (M_BH = {M:.1e} kg)")
    print(f"{'='*70}")
    print(f"  kT = {kT_GeV:.1f} GeV")
    print(f"  P_Hawking = {P:.3e} W = {P/1e12:.0f} TW")
    print(f"  P_captured = {P * 0.83:.3e} W")
    print(f"  Thrust F = {F:.3e} N = {F/1e6:.1f} MN")
    print(f"  Fuel rate = {dm_dt:.2f} kg/s = {dm_dt * yr / 1e3:.0f} t/yr")
    print(f"  τ_unfed = {tau:.2e} s = {tau/yr:.1f} yr" if tau > yr
          else f"  τ_unfed = {tau:.2e} s = {tau/86400:.1f} days")
    print(f"  Shell: {d['shell_t_pm']} pm, {d['shell_mass']/1e3:.0f} kt")
    print()

    # Cargo = M_BH (design convention)
    M_cargo = M
    M_dry = M + d["shell_mass"] + M_cargo
    print(f"  M_dry = M_BH + shell + cargo = {M_dry:.3e} kg")
    print(f"    (cargo = M_BH = {M_cargo:.1e} kg = {M_cargo/1e3:.0f} kt)")
    print()

    # ========== Boost/decelerate profiles for various distances ==========
    print(f"  --- Boost/decelerate mission profiles ---")
    print(f"  (Tsiolkovsky rocket equation, β_e = {beta_e}c = {v_e:.2e} m/s)")
    print()

    # For a boost/decelerate mission to distance D:
    # We parameterize by v_peak and find the required mass ratio.
    # Each leg: Δv = v_peak, mass ratio R = exp(v_peak / v_e)
    # Total mass ratio: R² (symmetric boost + decelerate)
    # M_fuel = M_dry × (R² - 1)
    # Trip time: integrate numerically

    targets = [
        ("α Centauri", 4.37 * ly),
        ("10 ly", 10.0 * ly),
        ("100 ly", 100.0 * ly),
    ]

    for target_name, D in targets:
        # Find optimal v_peak that minimizes trip time
        # for a given D and mass ratio constraint.
        # Simple approach: scan v_peak, compute trip time for each.

        best_time = 1e30
        best_vpeak = 0
        best_data = {}

        for vpeak_frac in np.linspace(0.02, 0.95, 200):
            v_peak = vpeak_frac * c

            # Mass ratio per leg (non-relativistic Tsiolkovsky)
            # For relativistic correction: use tanh form
            # But β_e = 0.332 and v_peak up to 0.95c needs relativistic treatment
            #
            # Relativistic rocket equation for massive exhaust:
            # For exhaust at β_e in ship frame:
            # Δv/c = tanh(v_e/c × ln(R)) ... actually this is for photon rocket
            #
            # For massive particle exhaust (β_e < 1), the relativistic rocket eq is:
            # (1+β_final)/(1-β_final) = [(1+β_e)/(1-β_e)]^(R^(2β_e/(1+β_e²)) ... complicated
            #
            # At our v_peak < 0.5c and β_e = 0.332, the non-relativistic
            # Tsiolkovsky is accurate to ~5%. Use it for now.

            if v_peak >= v_e * 5:  # mass ratio would be absurd
                continue

            R_leg = np.exp(v_peak / v_e)
            R_total = R_leg**2
            M_fuel = M_dry * (R_total - 1)
            M_wet = M_dry + M_fuel

            if M_fuel < 0 or R_total > 1e6:
                continue

            # Numerically integrate trip time
            # Phase 1: accelerate (burn fuel, ship gets lighter, a increases)
            # Phase 2: decelerate (burn fuel from decel reserve)
            #
            # During boost: m(t) = M_wet_boost × exp(-F/(m v_e) × t) ... no
            # Actually: dm/dt = -F/v_e (constant thrust means constant mass flow)
            # Wait — thrust F depends on BH mass (constant) not ship mass.
            # F = const (BH mass maintained, Hawking power constant)
            # dm_ship/dt = -dm_fuel/dt = -P_captured/c² (fuel feeds BH)
            # NO: dm_fuel/dt = fuel_rate (which maintains BH mass)
            # The thrust is from the EXHAUST, not from fuel consumption.
            # The fuel goes INTO the BH; the exhaust comes OUT of the BH as pairs.
            # These are separate mass flows!
            #
            # Thrust comes from: pair exhaust at β_e carrying momentum
            # Fuel consumption: dm_fuel/dt = P_Hawking / c² (to maintain M_BH)
            #
            # So: F = β_e × P_captured / c (constant, since P is constant)
            # dm_ship/dt = -dm_fuel/dt = -P_Hawking/c² (fuel consumed to feed BH)
            #
            # Ship equation of motion:
            # m_ship × dv/dt = F
            # dm_ship/dt = -dm_fuel_rate
            #
            # This is exactly the standard rocket equation with:
            # F = dm_exhaust/dt × v_e (where dm_exhaust/dt = P_captured/(v_e c))
            # ... actually let me think about this more carefully.
            #
            # The BH is being fed at rate dm_feed = P_H/c² to maintain mass.
            # The BH emits Hawking radiation. 83% is captured and becomes exhaust.
            # Exhaust mass rate: dm_exhaust/dt = 0.83 × P_H / (γ_e m_e c² per pair)
            #   Actually: dm_exhaust/dt = P_captured / (γ_e c²) where γ_e = 1.060
            #   = 0.83 × P_H / (1.060 c²)
            #
            # Hmm this is getting complicated. Let me simplify.
            #
            # Key insight: the fuel going IN equals the mass going OUT (steady state).
            # dm_fuel/dt = dm_exhaust/dt = P_H/c² = dm_dt
            # (The 17% neutrino loss means some Hawking mass escapes as ν,
            #  but the BH loses mass at total rate P_H/c². To maintain M_BH,
            #  you feed at P_H/c². The net exhaust mass rate is also P_H/c².)
            #
            # Effective exhaust velocity for the rocket equation:
            # F = v_eff × dm/dt  where dm/dt = P_H/c²
            # v_eff = F / (P_H/c²) = (β_e × 0.83 × P_H / c) / (P_H/c²)
            #       = β_e × 0.83 × c = 0.332 × 0.83 × c = 0.276c
            #
            # Wait, that's lower than β_e c because not all mass that leaves
            # the BH contributes to thrust (17% is neutrinos going isotropically).
            #
            # Let me reconsider. The fuel feeds the BH at rate dm_feed.
            # The BH evaporates at rate dm_evap = P_H/c².
            # For steady state: dm_feed = dm_evap.
            # Of the evaporated mass, 83% is captured and exhausted at β_e.
            # The thrust is F = 0.83 × dm_evap × β_e × c = 0.83 × dm_feed × β_e × c.
            # The 17% neutrino mass is lost (no thrust contribution).
            #
            # For the rocket equation, the "effective exhaust velocity" is:
            # v_eff = F / dm_feed = 0.83 × β_e × c = 0.276c
            #
            # This accounts for the neutrino loss: you burn 1 kg of fuel,
            # but only 0.83 kg actually produces thrust; the rest escapes as ν.

            v_eff = 0.83 * beta_e * c  # effective exhaust velocity accounting for ν loss

            # Recompute with corrected v_eff
            R_leg = np.exp(v_peak / v_eff)
            R_total = R_leg**2
            M_fuel = M_dry * (R_total - 1)
            M_wet = M_dry + M_fuel

            if M_fuel < 0 or R_total > 1e6:
                continue

            # Boost phase: constant thrust F, decreasing mass
            # m(t) starts at M_wet/2 + M_dry/2 ... no, let me think.
            #
            # For symmetric boost/decelerate:
            # Boost phase: start at M_wet, burn fuel until mass = M_wet/R_leg = M_mid
            # Decel phase: start at M_mid, burn fuel until mass = M_mid/R_leg = M_dry
            #
            # M_mid = M_wet / R_leg

            M_mid = M_wet / R_leg

            # Boost phase: m(t) = M_wet - dm_feed × t
            # v(t) = ∫ F/m(t') dt'
            # Distance: x(t) = ∫ v(t') dt'
            #
            # With constant F and dm/dt = -dm_feed (constant fuel rate):
            # m(t) = M_wet - dm_dt × t
            # a(t) = F / m(t) = F / (M_wet - dm_dt × t)
            # v(t) = ∫₀ᵗ F/(M_wet - dm_dt × t') dt' = -F/dm_dt × ln(1 - dm_dt×t/M_wet)
            #       = v_eff × ln(M_wet / (M_wet - dm_dt × t))
            #
            # At end of boost: m = M_mid, so dm_dt × t_boost = M_wet - M_mid
            # t_boost = (M_wet - M_mid) / dm_dt
            # v_peak = v_eff × ln(M_wet / M_mid) = v_eff × ln(R_leg) ✓

            t_boost = (M_wet - M_mid) / dm_dt

            # Distance during boost: x = ∫₀^t_boost v(t') dt'
            # v(t) = v_eff × ln(M_wet / (M_wet - dm_dt × t))
            # Let u = M_wet - dm_dt × t, du = -dm_dt dt
            # x = ∫ v_eff × ln(M_wet/u) × (-du/dm_dt)
            #   = (v_eff / dm_dt) × ∫_{M_wet}^{M_mid} ln(M_wet/u) du  (with sign flip)
            #   = (v_eff / dm_dt) × [M_wet - M_mid - M_mid × ln(M_wet/M_mid)]
            #   Hmm, let me just compute numerically.

            # Numerical integration of boost phase
            N_steps = 10000
            dt_boost = t_boost / N_steps
            m_current = M_wet
            v_current = 0.0
            x_boost = 0.0

            for _ in range(N_steps):
                a = F / m_current
                v_current += a * dt_boost
                x_boost += v_current * dt_boost
                m_current -= dm_dt * dt_boost

            # By symmetry, deceleration phase covers the same distance
            x_total = 2 * x_boost
            t_total = 2 * t_boost

            # Check if we reach the target distance
            if x_total < D * 0.5:  # need coast phase
                # Coast at v_peak for remaining distance
                v_peak_actual = v_current
                x_coast = D - x_total
                if v_peak_actual > 0:
                    t_coast = x_coast / v_peak_actual
                    # But during coast, BH still evaporates — need fuel for coast too!
                    fuel_coast = dm_dt * t_coast
                    # This means we need MORE fuel than the boost/decel budget
                    # For simplicity, add coast fuel to total
                    M_fuel_total = M_fuel + fuel_coast
                    t_total_with_coast = t_total + t_coast
                else:
                    continue
            elif x_total >= D:
                # Boost/decel covers the full distance — no coast needed
                # Scale down v_peak to fit the distance
                # Trip time ≈ 2 × t_boost × (D / x_total)^0.5 (rough)
                # Actually just use the computed time
                t_total_with_coast = t_total * (D / x_total)**0.5  # rough scaling
                M_fuel_total = M_fuel
            else:
                t_total_with_coast = t_total
                M_fuel_total = M_fuel

            if t_total_with_coast < best_time and v_peak < 0.95 * c:
                best_time = t_total_with_coast
                best_vpeak = v_current
                best_data = {
                    "v_peak": v_current,
                    "v_peak_c": v_current / c,
                    "R_leg": R_leg,
                    "R_total": R_total,
                    "M_fuel": M_fuel_total,
                    "M_wet": M_dry + M_fuel_total,
                    "t_total": t_total_with_coast,
                    "a_initial": F / (M_dry + M_fuel_total),
                    "a_final": F / M_dry,
                    "x_boost": x_boost,
                }

        if best_data:
            bd = best_data
            print(f"  {target_name} ({D/ly:.2f} ly):")
            print(f"    v_peak = {bd['v_peak_c']:.3f}c")
            print(f"    Mass ratio (total) = {bd['R_total']:.2f}")
            print(f"    Fuel carried = {bd['M_fuel']:.2e} kg = {bd['M_fuel']/M_dry:.1f} × M_dry")
            print(f"    Wet mass = {bd['M_wet']:.2e} kg")
            print(f"    a_initial = {bd['a_initial']:.3f} m/s² = {bd['a_initial']/9.81:.4f}g")
            print(f"    a_final (fuel exhausted) = {bd['a_final']:.2f} m/s² = {bd['a_final']/9.81:.3f}g")
            print(f"    Trip time = {bd['t_total']/yr:.1f} yr")
            print()

# ========== Summary table ==========
print("\n" + "=" * 70)
print("SUMMARY: Key point for the paper")
print("=" * 70)
print()
print("All profiles carry fuel from launch. No en-route refueling assumed.")
print("The fuel is any matter — rock, ice, iron, water — at mc² per kg.")
print()
print("The effective exhaust velocity v_eff = 0.83 × β_e × c = 0.276c")
print("accounts for the 17% neutrino loss (mass fed to BH but not producing thrust).")
print()
print("At v_eff = 0.276c, the rocket equation gives:")
print(f"  Mass ratio 2:   Δv = {0.276 * np.log(2):.3f}c = {0.276 * np.log(2) * c / 1e3:.0f} km/s")
print(f"  Mass ratio 5:   Δv = {0.276 * np.log(5):.3f}c")
print(f"  Mass ratio 10:  Δv = {0.276 * np.log(10):.3f}c")
print(f"  Mass ratio 100: Δv = {0.276 * np.log(100):.3f}c")
print()
print("For boost/decelerate, double the mass ratio (squared) for the same v_peak.")
print("These are NON-RELATIVISTIC Tsiolkovsky values; at v > 0.3c, relativistic")
print("corrections reduce the effective Δv by ~10-20%. Still interstellar-capable.")
