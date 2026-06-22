#!/usr/bin/env python3
"""Fig 2 — Hawking power budget. All labels OFF the bars, uniform style."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

os.chdir('/Users/ben/black_hole_paper')

plt.rcParams.update({
    'font.family': 'serif', 'font.size': 9, 'axes.linewidth': 0.7,
    'xtick.direction': 'in', 'ytick.direction': 'in',
    'xtick.top': False, 'ytick.right': False,
    'figure.dpi': 300, 'savefig.bbox': 'tight', 'savefig.pad_inches': 0.1,
})

fig, axes = plt.subplots(2, 1, figsize=(5.5, 3.0),
                          gridspec_kw={'height_ratios': [1.2, 0.8], 'hspace': 1.2})

# ── Top bar: by species ──
ax = axes[0]
segs = [
    ('Quarks + gluons', 77.7, '#1a3a5c'),
    ('e, μ',             9.3, '#2980b9'),
    ('τ',                4.7, '#5dade2'),
    ('Sec. ν',           9.5, '#999'),
    ('Prim. ν',          7.0, '#ccc'),
    ('Other',            1.8, '#e8e8e8'),
]

left = 0
midpoints = []
for name, frac, col in segs:
    ax.barh(0, frac, left=left, height=0.5, color=col,
            edgecolor='white', linewidth=0.3)
    midpoints.append(left + frac / 2)
    left += frac

# Labels above bar. Stagger heights for the crowded right side.
heights = [0.45, 1.1, 0.45, 1.1, 0.45, 1.1]
for i, (name, frac, col) in enumerate(segs):
    mx = midpoints[i]
    h = heights[i]
    ax.plot([mx, mx], [0.25, h - 0.02], '-', color='#aaa', lw=0.4)
    ax.text(mx, h, f'{name}  {frac}%', ha='center', va='bottom',
            fontsize=7, color='black')

ax.set_xlim(0, 100)
ax.set_ylim(-0.5, 1.9)
ax.set_yticks([])
ax.set_xticks([])
for sp in ax.spines.values():
    sp.set_visible(False)
ax.text(-2, 0, 'By species', ha='right', va='center', fontsize=8)

# ── Bottom bar: by fate ──
ax2 = axes[1]
fate = [
    ('Captured as pairs', 83.0, '#1a3a5c'),
    ('Lost (ν, gravitons)', 17.0, '#ccc'),
]

left = 0
midpoints2 = []
for name, frac, col in fate:
    ax2.barh(0, frac, left=left, height=0.5, color=col,
             edgecolor='white', linewidth=0.3)
    midpoints2.append(left + frac / 2)
    left += frac

# Labels below the bar
for i, (name, frac, col) in enumerate(fate):
    mx = midpoints2[i]
    ax2.plot([mx, mx], [-0.25, -0.42], '-', color='#888', lw=0.4)
    ax2.text(mx, -0.48, f'{name}  {frac}%', ha='center', va='top',
             fontsize=8, color='black')

ax2.set_xlim(0, 100)
ax2.set_ylim(-1.1, 0.4)
ax2.set_yticks([])
ax2.set_xlabel('Fraction of total Hawking power (%)')
for sp in ['top', 'right', 'left']:
    ax2.spines[sp].set_visible(False)
ax2.text(-2, 0, 'By fate', ha='right', va='center', fontsize=8)

fig.savefig('figures/fig2_spectrum.png', dpi=300)
plt.close()
print('fig2_spectrum.png  ✓')
