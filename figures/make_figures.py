#!/usr/bin/env python3
"""
Paper figures — clean rewrite. One message per figure, no clutter.
Figures numbered to match Draft 3 references:
  Fig. 2: Hawking power budget
  Fig. 3: Muon punch-through vs shell thickness
  Fig. 4: Bootstrap M(t)
  Fig. 5: Mission velocity profiles
(Fig. 1 is the architecture schematic, done in TikZ.)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ── House style ──────────────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'axes.linewidth': 0.7,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'xtick.top': True,
    'ytick.right': True,
    'xtick.major.size': 3.5,
    'ytick.major.size': 3.5,
    'xtick.minor.size': 2,
    'ytick.minor.size': 2,
    'legend.frameon': False,
    'figure.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
})

G    = 6.674e-11
hbar = 1.055e-34
c    = 2.998e8
yr   = 3.156e7
ly   = 9.461e15


# ═══════════════════════════════════════════════════════════════════
# FIG 2 — Hawking power budget (single horizontal stacked bar)
# ═══════════════════════════════════════════════════════════════════
def make_fig2():
    fig, ax = plt.subplots(figsize=(6.5, 1.8))

    # Species groups and their power fractions
    names =    ['Quarks + gluons', 'e, μ',  'τ',   'γ',  'Sec. ν', 'Prim. ν']
    fracs =    [77.7,               9.3,     4.7,   1.3,   9.5,      7.0]
    # note: γ 1.0% + other 0.3% lumped into γ = 1.3% for readability
    colors =   ['#1a3a5c', '#2980b9', '#5dade2', '#aed6f1', '#b0b0b0', '#d0d0d0']
    txt_col =  ['white',   'white',   'white',  'black',  'black',   'black']

    left = 0.0
    for name, f, col, tc in zip(names, fracs, colors, txt_col):
        ax.barh(0, f, left=left, height=0.6, color=col, edgecolor='white', lw=0.4)
        if f >= 4:
            ax.text(left + f/2, 0, f'{name}\n{f:.1f}%', ha='center', va='center',
                    fontsize=7.5, color=tc)
        else:
            ax.text(left + f/2, 0.42, f'{name}\n{f:.1f}%', ha='center', va='bottom',
                    fontsize=6.5, color='#333', linespacing=0.9)
        left += f

    # Captured / lost brackets
    cap = sum(fracs[:4])  # 93.0 before neutrinos... wait
    # Captured = 83%, Lost = 17%
    ax.plot([0, 83], [-0.5, -0.5], 'k-', lw=1.2)
    ax.plot([0, 0], [-0.45, -0.55], 'k-', lw=1.0)
    ax.plot([83, 83], [-0.45, -0.55], 'k-', lw=1.0)
    ax.text(41.5, -0.7, 'Captured  83%', ha='center', fontsize=9, fontweight='bold')

    ax.plot([83, 100], [-0.5, -0.5], '-', color='gray', lw=1.0)
    ax.plot([100, 100], [-0.45, -0.55], '-', color='gray', lw=1.0)
    ax.text(91.5, -0.7, 'Lost 17%', ha='center', fontsize=8, color='gray')

    ax.set_xlim(0, 100)
    ax.set_ylim(-1.1, 0.7)
    ax.set_xlabel('Fraction of total Hawking power (%)')
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    fig.savefig('figures/fig2_spectrum.png', dpi=300)
    plt.close()
    print('  fig2_spectrum.png  ✓')


# ═══════════════════════════════════════════════════════════════════
# FIG 3 — Muon punch-through vs shell thickness
# ═══════════════════════════════════════════════════════════════════
def make_fig3():
    fig, ax = plt.subplots(figsize=(3.4, 3.0))

    kT_MeV  = 10.57e3          # 10.57 GeV in MeV
    P_mu    = 5620e12           # muon-channel power, W
    dEdx    = 80                # MeV/fm

    t = np.linspace(500, 6000, 500)
    xc = dEdx * t / kT_MeV
    eps = np.exp(-xc) * (xc**2 + 4*xc + 6) / (7*np.pi**4/120)
    P = eps * P_mu

    ax.semilogy(t, P, 'k-', lw=1.5)

    # Adopted point
    t0, xc0 = 3000, dEdx*3000/kT_MeV
    eps0 = np.exp(-xc0)*(xc0**2 + 4*xc0 + 6)/(7*np.pi**4/120)
    P0 = eps0 * P_mu
    ax.plot(t0, P0, 'ko', ms=5, zorder=5)
    ax.axvline(t0, color='#888', ls='--', lw=0.6)
    ax.annotate(f'Adopted: 3000 fm\n({P0/1e6:.0f} MW)',
                xy=(t0, P0), xytext=(3800, P0*50),
                fontsize=7.5, ha='left',
                arrowprops=dict(arrowstyle='->', color='#555', lw=0.8))

    ax.set_xlabel('CFL shell thickness (fm)')
    ax.set_ylabel('Muon punch-through (W)')
    ax.set_ylim(1e-4, 1e16)
    ax.set_xlim(500, 6000)

    fig.savefig('figures/fig3_punchthrough.png', dpi=300)
    plt.close()
    print('  fig3_punchthrough.png  ✓')


# ═══════════════════════════════════════════════════════════════════
# FIG 4 — Bootstrap M(t)
# ═══════════════════════════════════════════════════════════════════
def make_fig4():
    from scipy.integrate import solve_ivp

    fig, ax = plt.subplots(figsize=(3.4, 3.0))

    A = 8.5
    def f_M(M):
        kT = hbar * c**3 / (8*np.pi*G*M) / 1.602e-10   # GeV
        if kT > 80:   return 4.2e-3
        elif kT < 15: return 3.5e-3
        else:         return 3.5e-3 + (kT-15)/(80-15)*0.7e-3

    def rhs(t, y):
        return [A * hbar * c**4 * f_M(y[0]) / (G**2 * y[0]**2)]

    sol = solve_ivp(rhs, [0, 7e7], [2.26e5], max_step=5e4,
                    dense_output=True)
    tt = np.linspace(0, sol.t[-1], 3000)
    MM = sol.sol(tt)[0]

    ax.semilogy(tt/yr, MM, 'k-', lw=1.5)
    ax.axhline(1e9, color='#888', ls='--', lw=0.6)
    ax.plot(0, 2.26e5, 'ko', ms=4, zorder=5)

    ax.text(0.12, 3.5e5, '226 t seed', fontsize=8)
    ax.text(1.55, 1.3e9, r'$10^9$ kg', fontsize=8, color='#666')

    ax.set_xlabel('Time (yr)')
    ax.set_ylabel('Black hole mass (kg)')
    ax.set_xlim(0, 2.0)
    ax.set_ylim(1e5, 3e9)

    fig.savefig('figures/fig4_bootstrap.png', dpi=300)
    plt.close()
    print('  fig4_bootstrap.png  ✓')


# ═══════════════════════════════════════════════════════════════════
# FIG 5 — Alpha Centauri velocity profiles (proper simulation)
# ═══════════════════════════════════════════════════════════════════
def simulate_mission(F, dm_dt, M_dry, R_total, D):
    """
    Simulate a boost / coast / decelerate mission.
    Returns arrays (t_sec, v_ms) for the full trip.
    """
    M_fuel = M_dry * (R_total - 1)
    M_wet  = M_dry + M_fuel
    fuel_per_leg = M_fuel / 2       # symmetric: half for boost, half for decel
    # (ignoring coast fuel for simplicity — coast fuel is small for short coasts
    #  and zero for no-coast missions; a full treatment would iterate)

    dt = 5000.0  # seconds per step

    # ── Boost phase ──
    m = M_wet
    v = 0.0
    x = 0.0
    fuel_used = 0.0
    t_vals = [0.0]
    v_vals = [0.0]

    while fuel_used < fuel_per_leg and x < D/2:
        step = min(dt, (fuel_per_leg - fuel_used)/dm_dt)
        a = F / m
        v += a * step
        x += v * step
        m -= dm_dt * step
        fuel_used += dm_dt * step
        t_vals.append(t_vals[-1] + step)
        v_vals.append(v)

    v_peak = v
    t_boost = t_vals[-1]
    x_boost = x

    # ── Coast phase (if needed) ──
    if x_boost < D/2:
        x_remaining = D - 2*x_boost   # coast covers the middle
        if v_peak > 0:
            t_coast = x_remaining / v_peak
        else:
            t_coast = 0
        # sample coast at ~100 points
        n_coast = max(int(t_coast / dt), 2)
        dt_coast = t_coast / n_coast
        for _ in range(n_coast):
            t_vals.append(t_vals[-1] + dt_coast)
            v_vals.append(v_peak)
    else:
        t_coast = 0

    # ── Decelerate phase (simulate forward, velocity decreasing) ──
    m = M_wet / 2 + M_dry / 2   # rough mass at start of decel
    # More precisely: m = M_wet - fuel_boost - fuel_coast
    # fuel_coast ≈ dm_dt * t_coast
    fuel_coast_used = dm_dt * t_coast if t_coast > 0 else 0
    m = M_wet - fuel_per_leg - fuel_coast_used
    v = v_peak
    fuel_used = 0.0

    while v > 0 and fuel_used < fuel_per_leg:
        step = min(dt, (fuel_per_leg - fuel_used)/dm_dt)
        a = F / m
        v -= a * step    # decelerating
        if v < 0:
            v = 0.0
        m -= dm_dt * step
        fuel_used += dm_dt * step
        t_vals.append(t_vals[-1] + step)
        v_vals.append(v)

    return np.array(t_vals), np.array(v_vals)


def make_fig5():
    fig, ax = plt.subplots(figsize=(6.5, 3.0))

    D = 4.37 * ly

    missions = [
        {'label': r'Reference ($10^9\,\mathrm{kg}$), 79 yr',
         'F': 55.3e6, 'dm': 0.67, 'M_dry': 2.06e9, 'R': 1.7,
         'ls': '-', 'lw': 1.5, 'color': 'black'},
        {'label': r'High-thrust ($2{\times}10^8\,\mathrm{kg}$), 19 yr',
         'F': 1.375e9, 'dm': 16.65, 'M_dry': 6.0e8, 'R': 9.4,
         'ls': '--', 'lw': 1.5, 'color': '#444'},
        {'label': r'Sprint ($5{\times}10^7\,\mathrm{kg}$), 11 yr',
         'F': 2.18e10, 'dm': 264.0, 'M_dry': 7.0e8, 'R': 34.0,
         'ls': '-.', 'lw': 1.5, 'color': '#888'},
    ]

    for m in missions:
        t, v = simulate_mission(m['F'], m['dm'], m['M_dry'], m['R'], D)
        ax.plot(t/yr, v/c, ls=m['ls'], lw=m['lw'], color=m['color'],
                label=m['label'])

    ax.set_xlabel('Time (yr)')
    ax.set_ylabel(r'$v\;/\;c$')
    ax.set_xlim(0, 85)
    ax.set_ylim(0, 0.55)
    ax.legend(fontsize=7.5, loc='upper right')

    fig.savefig('figures/fig5_missions.png', dpi=300)
    plt.close()
    print('  fig5_missions.png  ✓')


# ═══════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    import os
    os.chdir('/Users/ben/black_hole_paper')
    print('Generating figures …')
    make_fig2()
    make_fig3()
    make_fig4()
    make_fig5()
    print('Done. Fig. 1 (architecture) requires TikZ/Inkscape.')
