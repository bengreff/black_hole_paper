#!/usr/bin/env python3
"""Fix fig2 and fig5. Corrected fuel split for Tsiolkovsky."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

os.chdir('/Users/ben/black_hole_paper')

plt.rcParams.update({
    'font.family': 'serif', 'font.size': 10, 'axes.linewidth': 0.7,
    'xtick.direction': 'in', 'ytick.direction': 'in',
    'xtick.top': False, 'ytick.right': True,
    'xtick.major.size': 3.5, 'ytick.major.size': 3.5,
    'legend.frameon': False, 'figure.dpi': 300,
    'savefig.bbox': 'tight', 'savefig.pad_inches': 0.05,
})

c  = 2.998e8
yr = 3.156e7
ly = 9.461e15


def make_fig2():
    fig, ax = plt.subplots(figsize=(6.5, 1.6))

    names  = ['Quarks +\ngluons', 'e, μ', 'τ', 'γ + other', 'Sec. ν', 'Prim. ν']
    fracs  = [77.7, 9.3, 4.7, 1.3, 9.5, 7.0]
    colors = ['#1a3a5c', '#2980b9', '#5dade2', '#aed6f1', '#b0b0b0', '#d0d0d0']
    tcols  = ['white', 'white', 'white', '#333', '#333', '#333']

    left = 0.0
    for nm, fr, co, tc in zip(names, fracs, colors, tcols):
        ax.barh(0, fr, left=left, height=0.55, color=co,
                edgecolor='white', linewidth=0.4)
        if fr >= 7:
            ax.text(left + fr/2, 0, f'{nm}\n{fr}%', ha='center', va='center',
                    fontsize=7, color=tc, linespacing=0.85)
        elif fr >= 3:
            ax.text(left + fr/2, 0, f'{nm}\n{fr}%', ha='center', va='center',
                    fontsize=6, color=tc, linespacing=0.85)
        else:
            ax.text(left + fr/2, 0, f'{fr}%', ha='center', va='center',
                    fontsize=5.5, color=tc)
        left += fr

    y_br = -0.45
    ax.plot([0, 83], [y_br, y_br], 'k-', lw=1.0, clip_on=False)
    ax.plot([0, 0], [y_br-.06, y_br+.06], 'k-', lw=.8, clip_on=False)
    ax.plot([83, 83], [y_br-.06, y_br+.06], 'k-', lw=.8, clip_on=False)
    ax.text(41.5, y_br-.15, 'Captured  83%', ha='center', fontsize=9,
            fontweight='bold', clip_on=False)
    ax.plot([83, 100], [y_br, y_br], '-', color='gray', lw=.8, clip_on=False)
    ax.plot([100, 100], [y_br-.06, y_br+.06], '-', color='gray', lw=.8,
            clip_on=False)
    ax.text(91.5, y_br-.15, 'Lost 17%', ha='center', fontsize=8,
            color='gray', clip_on=False)

    ax.set_xlim(0, 100)
    ax.set_ylim(-0.9, 0.5)
    ax.set_xlabel('Fraction of total Hawking power (%)')
    ax.set_yticks([])
    for sp in ['top', 'right', 'left']:
        ax.spines[sp].set_visible(False)
    fig.savefig('figures/fig2_spectrum.png', dpi=300)
    plt.close()
    print('  fig2_spectrum.png  ✓')


def simulate(F, dm, M_dry, R_total, D):
    """
    Simulate boost / coast / decel for Alpha Centauri.

    KEY FIX: fuel split is NOT 50/50. The Tsiolkovsky equation gives
    R_leg = sqrt(R_total), and the correct split is:
      fuel_boost = M_wet - M_wet/R_leg = M_wet(1 - 1/R_leg)
      fuel_decel = M_wet/R_leg - M_dry = M_mid(1 - 1/R_leg)
    More fuel is burned during boost (heavier ship) than decel (lighter).
    """
    M_fuel = M_dry * (R_total - 1)
    M_wet  = M_dry + M_fuel
    R_leg  = np.sqrt(R_total)
    M_mid  = M_wet / R_leg           # mass after boost
    fuel_boost = M_wet - M_mid       # boost fuel
    fuel_decel = M_mid - M_dry       # decel fuel

    dt = 500.0  # s (finer timestep for accuracy)

    # ── BOOST ──
    t_list = [0.0]
    v_list = [0.0]
    m = M_wet
    v = 0.0
    x = 0.0
    burned = 0.0

    while burned < fuel_boost:
        step = min(dt, (fuel_boost - burned) / dm)
        a = F / m
        v_new = v + a * step
        x += (v + v_new) / 2 * step
        v = v_new
        m -= dm * step
        burned += dm * step
        t_list.append(t_list[-1] + step)
        v_list.append(v)

    v_peak = v
    x_boost = x

    # ── COAST (if boost didn't reach halfway) ──
    if x_boost < D / 2:
        coast_dist = D - 2 * x_boost
        coast_time = coast_dist / v_peak if v_peak > 0 else 0
        n_pts = max(int(coast_time / 1e6), 50)  # ~50 points during coast
        dt_c = coast_time / n_pts
        for i in range(1, n_pts + 1):
            t_list.append(t_list[-1] + dt_c)
            v_list.append(v_peak)

    # ── DECEL ──
    m = M_mid  # mass at start of decel (= mass after boost, ignoring coast fuel)
    v = v_peak
    burned = 0.0

    while burned < fuel_decel and v > 0:
        step = min(dt, (fuel_decel - burned) / dm)
        a = F / m
        v_new = v - a * step
        if v_new < 0:
            v_new = 0.0
        v = v_new
        m -= dm * step
        burned += dm * step
        t_list.append(t_list[-1] + step)
        v_list.append(v)

    return np.array(t_list), np.array(v_list)


def make_fig5():
    fig, ax = plt.subplots(figsize=(6.5, 3.0))

    D = 4.37 * ly

    missions = [
        {'label': r'Reference ($10^9$ kg), 79 yr',
         'F': 55.3e6, 'dm': 0.67, 'Md': 2.06e9, 'R': 1.7,
         'ls': '-', 'c': 'black'},
        {'label': r'High-thrust ($2{\times}10^8$ kg), 19 yr',
         'F': 1.375e9, 'dm': 16.65, 'Md': 6.0e8, 'R': 9.4,
         'ls': '--', 'c': '#444'},
        {'label': r'Sprint ($5{\times}10^7$ kg), 11 yr',
         'F': 2.18e10, 'dm': 264.0, 'Md': 7.0e8, 'R': 34.0,
         'ls': '-.', 'c': '#888'},
    ]

    for m in missions:
        t, v = simulate(m['F'], m['dm'], m['Md'], m['R'], D)
        ax.plot(t/yr, v/c, ls=m['ls'], lw=1.5, color=m['c'], label=m['label'])
        print(f"    {m['label'][:15]:15s}  v_peak = {max(v)/c:.3f}c  "
              f"trip = {t[-1]/yr:.1f} yr")

    ax.set_xlabel('Time (yr)')
    ax.set_ylabel(r'$v\;/\;c$')
    ax.set_xlim(0, 85)
    ax.set_ylim(0, 0.55)
    ax.legend(fontsize=7.5, loc='upper right')
    fig.savefig('figures/fig5_missions.png', dpi=300)
    plt.close()
    print('  fig5_missions.png  ✓')


if __name__ == '__main__':
    make_fig2()
    make_fig5()
