#!/usr/bin/env python3
"""Regenerate fig2 (spectrum) and fig4 (bootstrap) from scratch."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import os

os.chdir('/Users/ben/black_hole_paper')

plt.rcParams.update({
    'font.family': 'serif', 'font.size': 10, 'axes.linewidth': 0.7,
    'xtick.direction': 'in', 'ytick.direction': 'in',
    'xtick.top': False, 'ytick.right': True,
    'xtick.major.size': 3.5, 'ytick.major.size': 3.5,
    'legend.frameon': False, 'figure.dpi': 300,
    'savefig.bbox': 'tight', 'savefig.pad_inches': 0.08,
})

G    = 6.674e-11
hbar = 1.055e-34
c    = 2.998e8
yr   = 3.156e7


# ═══════════════════════════════════════════════════════════════════
# FIG 2 — Hawking power budget
#
# Design: simple TABLE figure, not a bar chart.
# Two rows: "By species" and "By fate". Clear, no ambiguity.
# Actually: just use TWO simple pie-style horizontal bars,
# each self-contained with a clean legend below.
#
# Simplest possible: a single horizontal bar with segments,
# plus a second bar below showing captured vs lost.
# No floating labels. Every label INSIDE its segment or in
# a legend.
# ═══════════════════════════════════════════════════════════════════
def make_fig2():
    fig, axes = plt.subplots(2, 1, figsize=(6.0, 2.2),
                              gridspec_kw={'height_ratios': [1, 0.6],
                                           'hspace': 0.6})

    # ── Top bar: by species ──
    ax = axes[0]
    segs = [
        ('Quarks + gluons',  77.7, '#1a3a5c', 'white'),
        ('e, μ',              9.3, '#2980b9', 'white'),
        ('τ',                 4.7, '#5dade2', 'white'),
        ('Sec. ν',            9.5, '#999',    'black'),
        ('Prim. ν',           7.0, '#ccc',    'black'),
        ('Other',             1.8, '#e8e8e8', '#666'),
    ]
    left = 0
    for name, frac, col, tcol in segs:
        ax.barh(0, frac, left=left, height=0.7, color=col,
                edgecolor='white', lw=0.3)
        if frac > 6:
            ax.text(left + frac/2, 0, f'{name}\n{frac}%',
                    ha='center', va='center', fontsize=7, color=tcol,
                    linespacing=0.85)
        left += frac

    # Small-segment labels as a legend row below the bar
    small = [(s[0], s[1]) for s in segs if s[1] <= 6]
    legend_txt = '   '.join(f'{n}: {f}%' for n, f in small)
    ax.text(50, -0.65, legend_txt, ha='center', va='top', fontsize=7,
            color='#444')

    ax.set_xlim(0, 100)
    ax.set_ylim(-1.1, 0.55)
    ax.set_yticks([])
    ax.set_xticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.text(-1, 0, 'By\nspecies', ha='right', va='center', fontsize=8,
            fontweight='bold')

    # ── Bottom bar: by fate ──
    ax2 = axes[1]
    fate = [
        ('Captured as pairs', 83.0, '#1a3a5c', 'white'),
        ('Lost (ν, gravitons)', 17.0, '#ccc', 'black'),
    ]
    left = 0
    for name, frac, col, tcol in fate:
        ax2.barh(0, frac, left=left, height=0.7, color=col,
                 edgecolor='white', lw=0.3)
        ax2.text(left + frac/2, 0, f'{name}  {frac}%',
                 ha='center', va='center', fontsize=8, color=tcol,
                 fontweight='bold')
        left += frac

    ax2.set_xlim(0, 100)
    ax2.set_ylim(-0.6, 0.55)
    ax2.set_yticks([])
    ax2.set_xlabel('Fraction of total Hawking power (%)')
    for sp in ['top', 'right', 'left']:
        ax2.spines[sp].set_visible(False)
    ax2.text(-1, 0, 'By\nfate', ha='right', va='center', fontsize=8,
             fontweight='bold')

    fig.savefig('figures/fig2_spectrum.png', dpi=300)
    plt.close()
    print('  fig2_spectrum.png  ✓')


# ═══════════════════════════════════════════════════════════════════
# FIG 4 — Bootstrap M(t)
# Fix: y-axis from 2e5 to 2e9 so the curve sits in the middle,
# not jammed against the top.
# ═══════════════════════════════════════════════════════════════════
def make_fig4():
    fig, ax = plt.subplots(figsize=(3.4, 3.0))

    A = 8.5

    def f_M(M):
        kT = hbar * c**3 / (8 * np.pi * G * M) / 1.602e-10
        if kT > 80:   return 4.2e-3
        elif kT < 15: return 3.5e-3
        else:         return 3.5e-3 + (kT - 15) / (80 - 15) * 0.7e-3

    def rhs(t, y):
        return [A * hbar * c**4 * f_M(y[0]) / (G**2 * y[0]**2)]

    M0 = 2.26e5
    Mf = 1.0e9
    sol = solve_ivp(rhs, [0, 7e7], [M0], max_step=5e4, dense_output=True)
    tt = np.linspace(0, sol.t[-1], 3000)
    MM = sol.sol(tt)[0]

    ax.semilogy(tt / yr, MM, 'k-', lw=1.5)
    ax.axhline(Mf, color='#888', ls='--', lw=0.6)
    ax.plot(0, M0, 'ko', ms=4, zorder=5)

    ax.text(0.15, 4e5, '226 t seed', fontsize=8)
    ax.text(1.0, 1.5e9, r'$10^9$ kg operating mass', fontsize=8, color='#666')

    ax.set_xlabel('Time (yr)')
    ax.set_ylabel('Black hole mass (kg)')
    ax.set_xlim(0, 2.0)
    ax.set_ylim(1e5, 5e9)

    fig.savefig('figures/fig4_bootstrap.png', dpi=300)
    plt.close()
    print('  fig4_bootstrap.png  ✓')


if __name__ == '__main__':
    make_fig2()
    make_fig4()
