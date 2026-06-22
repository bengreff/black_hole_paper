#!/usr/bin/env python3
"""Convert draft_5_submission.md to a LaTeX document, then compile to PDF via tectonic."""

import re
import os
import subprocess

os.chdir('/Users/ben/black_hole_paper')

with open('drafts/draft_5_submission.md', 'r') as f:
    lines = f.readlines()

# ── LaTeX equation definitions (replacing OMML) ──
EQ = {}
EQ[1] = r'kT = \frac{\hbar c^3}{8\pi G M} = 10.57 \text{ GeV}'
EQ[2] = r'r_s = \frac{2GM}{c^2} = 1.485 \times 10^{-18} \text{ m}'
EQ[3] = r'P = \frac{\hbar c^6 f}{G^2 M^2} = 60{,}200 \text{ TW}'
EQ[4] = r'\tau = \frac{G^2 M^3}{3\hbar c^4 f} = 15.8 \text{ yr}'
EQ[5] = r'f = \sum_i g_i \, \alpha_{s_i} \, S(m_i/kT)'
EQ[6] = r'E_c = 80 \text{ MeV/fm} \times 3000 \text{ fm} = 240 \text{ GeV}'
EQ[7] = r'\varepsilon(x_c) = \frac{e^{-x_c}(x_c^2 + 4x_c + 6)}{7\pi^4/120}, \quad x_c = E_c/kT'
EQ[8] = r'f_{\pm} = 10^{39.2} \, T_9^3 \, \exp(-11.9/T_9) \, J(\zeta) \quad [\text{pairs cm}^{-2} \text{ s}^{-1}]'
EQ[9] = r'L_\text{pair} = \frac{P_\text{abs}}{A \cdot f_\text{cap}} = 8.21 \times 10^{15} \text{ W/m}^2'
EQ[10] = r'T_\text{eq} = 0.356 \text{ GK}, \quad kT = 30.7 \text{ keV}, \quad \gamma = 1.060, \quad \beta = 0.332'
EQ[11] = r'P/V \approx \frac{\alpha^4 T^9}{\pi^4 F_\pi^4}'
EQ[12] = r'\omega_p = \sqrt{\frac{4\alpha}{3\pi}} \, \mu_e = 0.50 \text{ MeV}'
EQ[13] = r'B_z(z) = \frac{\mu_0 I R_c^2}{2} \left[ \frac{1}{(R_c^2 + (d-z)^2)^{3/2}} - \frac{1}{(R_c^2 + (d+z)^2)^{3/2}} \right]'
EQ[14] = r'\left.\frac{dB_z}{dz}\right|_{z=0} = \frac{3\mu_0 I R_c^2 d}{(R_c^2 + d^2)^{5/2}} = 227 \text{ T/m}'
EQ[15] = r'g \cdot \frac{dB}{dz} \cdot \delta_\text{eq} = F_\text{thrust} \cdot \frac{M_\text{BH}}{M_\text{ship}}'
EQ[16] = r'g = 1.182 \times 10^6 \text{ A\,m}'
EQ[17] = r'\tau_\text{lat} = \sqrt{\frac{M_\text{BH}}{|k_r|}} \approx 2.8 \text{ s}'
EQ[18] = r'r_L = \frac{\gamma \beta m_e c}{eB} = 2.65 \text{ \textmu m}'
EQ[19] = r'f_\text{cap} = 1 - \cos\!\left(\arcsin\sqrt{\frac{B_\text{loc}}{B_\text{throat}}}\right) = 12.1\%'
EQ[20] = r'\sin^2\theta_\text{exit} = \frac{B_\text{exit}}{B_\text{throat}} = 3 \times 10^{-8}, \quad \theta_\text{exit} \approx 0.010°'
EQ[21] = r't_\text{ff} = \sqrt{\frac{3\pi}{32 G\rho}} = 0.29 \text{ s}'
EQ[22] = r'\Gamma \propto \exp(-c/\alpha_\text{GUT}), \quad c \approx 4'
EQ[23] = r'\sigma \sim \pi r_c^2 \sim 2.4 \times 10^{-63} \text{ m}^2'
EQ[24] = r'\frac{dM}{dt} = A \cdot \frac{P(M)}{c^2}'
EQ[25] = r'A = \frac{\gamma f_\text{cap}}{(\gamma - 1)/\gamma} - 1'
EQ[26] = r't_\text{boot} = \frac{G^2(M_f^3 - M_0^3)}{3A\hbar c^4 f}'
EQ[27] = r'F = \frac{\beta P_\text{cap}}{c} = 55.3 \text{ MN}'
EQ[28] = r'v_\text{peak} = c \tanh\!\left(\frac{v_\text{eff}}{c} \ln R_\text{leg}\right)'


def latex_escape(s):
    """Escape text for LaTeX body, converting inline math notation."""
    # Escape only the special chars that actually appear in prose
    s = s.replace('%', r'\%')
    s = s.replace('#', r'\#')
    s = s.replace('&', r'\&')
    # Convert -- to em dash
    s = re.sub(r'(?<!\-)--(?!\-)', '---', s)
    # Convert Unicode Greek to LaTeX commands FIRST (before subscript handling)
    # Use placeholder tokens that won't interfere with subscript regex
    for char, cmd in [
        ('ℏ','GRHBAR'),('α','GRALPHA'),('β','GRBETA'),('γ','GRGAMMA'),('δ','GRDELTA'),
        ('ε','GREPSLN'),('ζ','GRZETA'),('η','GRETA'),('θ','GRTHETA'),('λ','GRLAMBDA'),
        ('μ','GRMU'),('ν','GRNU'),('ξ','GRXI'),('π','GRPI'),('ρ','GRRHO'),('σ','GRSIGMA'),
        ('τ','GRTAU'),('φ','GRPHI'),('ω','GROMEGA'),
        ('Δ','GRDLTA'),('Σ','GRSGMA'),('Ω','GROMGA'),('Φ','GRPHI2'),('Γ','GRGMMA'),
    ]:
        s = s.replace(char, cmd)
    # Convert X_{multi} brace subscript patterns FIRST (handles α_{s_i}, α_{1/2})
    s = re.sub(r'([A-Za-z][A-Z]*)_\{([^}]+)\}',
               lambda m: f'${m.group(1)}_{{{m.group(2)}}}$', s)
    # Convert simple subscripts (X_Y where no braces)
    # (?<!\{) prevents matching inside brace-handler output like _{s_i}
    def sub_repl(m):
        base, sub = m.group(1), m.group(2)
        if len(sub) == 1:
            return f'${base}_{sub}$'
        return f'${base}_{{\\text{{{sub}}}}}$'
    s = re.sub(r'(?<!\{)([A-Za-z][A-Z]*)_([A-Za-z0-9]+)', sub_repl, s)
    # Now restore Greek placeholders to LaTeX commands
    for tok, cmd in [
        ('GRHBAR',r'\hbar'),('GRALPHA',r'\alpha'),('GRBETA',r'\beta'),('GRGAMMA',r'\gamma'),
        ('GRDELTA',r'\delta'),('GREPSLN',r'\varepsilon'),('GRZETA',r'\zeta'),('GRETA',r'\eta'),
        ('GRTHETA',r'\theta'),('GRLAMBDA',r'\lambda'),('GRMU',r'\mu'),('GRNU',r'\nu'),
        ('GRXI',r'\xi'),('GRPI',r'\pi'),('GRRHO',r'\rho'),('GRSIGMA',r'\sigma'),
        ('GRTAU',r'\tau'),('GRPHI',r'\varphi'),('GROMEGA',r'\omega'),
        ('GRDLTA',r'\Delta'),('GRSGMA',r'\Sigma'),('GROMGA',r'\Omega'),('GRPHI2',r'\Phi'),
        ('GRGMMA',r'\Gamma'),
    ]:
        # If inside $...$, just replace. If standalone, wrap in $...$
        s = s.replace(tok, cmd)
    # Fix \text{\command} → \command (Greek in subscripts should stay as math)
    greek_cmds = r'hbar|alpha|beta|gamma|delta|varepsilon|zeta|eta|theta|lambda|mu|nu|xi|pi|rho|sigma|tau|varphi|omega|Delta|Sigma|Omega|Phi|Gamma'
    s = re.sub(r'\\text\{(\\(?:' + greek_cmds + r'))\}', r'\1', s)
    # Wrap any bare LaTeX commands not already in math mode
    s = re.sub(r'(?<!\$)(\\(?:' + greek_cmds + r'))(?!\})', r'$\1$', s)
    # Convert Unicode superscripts
    sup_map = {'⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9','⁻':'-','⁺':'+'}
    result = []
    i = 0
    while i < len(s):
        if s[i] in sup_map:
            sup = []
            while i < len(s) and s[i] in sup_map:
                sup.append(sup_map[s[i]])
                i += 1
            result.append('$^{' + ''.join(sup) + '}$')
        else:
            result.append(s[i])
            i += 1
    s = ''.join(result)
    # Escape any remaining bare _ not inside $...$ (e.g. f_± where ± isn't alphanumeric)
    # Convert remaining X_nonalpha to $X_{\text{nonalpha}}$ or just escape the _
    def fix_bare_underscore(m):
        pre = m.group(1)
        post = m.group(2)
        return f'${pre}_{{{post}}}$'
    s = re.sub(r'([A-Za-z])_([±°·])', fix_bare_underscore, s)
    # Escape any remaining bare underscores that weren't consumed by subscript handlers
    # Split on $...$ to avoid touching math mode content
    parts = re.split(r'(\$[^$]*\$)', s)
    for j in range(len(parts)):
        if not parts[j].startswith('$'):
            parts[j] = parts[j].replace('_', r'\_')
    s = ''.join(parts)
    # Merge adjacent math modes: $X$ $Y$ -> $X Y$, and $...$$ -> $...$
    s = re.sub(r'\$\s*\$', ' ', s)
    # Convert e+e- notation
    s = s.replace('e+e-', r'$e^+e^-$')
    # Convert >=
    s = s.replace('>=', r'$\geq$')
    s = s.replace('->', r'$\to$')
    # Convert ~ to \sim
    s = re.sub(r'(?<![\\$])~(?!\s*\\)', r'$\\sim$', s)
    return s


def latex_math(s):
    """Convert inline notation to LaTeX for use INSIDE math mode (no $...$)."""
    # Greek — add {} after to prevent command-name collisions like \betam
    for char, cmd in [
        ('ℏ',r'\hbar'),('α',r'\alpha'),('β',r'\beta'),('γ',r'\gamma'),('δ',r'\delta'),
        ('ε',r'\varepsilon'),('ζ',r'\zeta'),('η',r'\eta'),('θ',r'\theta'),('λ',r'\lambda'),
        ('μ',r'\mu'),('ν',r'\nu'),('ξ',r'\xi'),('π',r'\pi'),('ρ',r'\rho'),('σ',r'\sigma'),
        ('τ',r'\tau'),('φ',r'\varphi'),('ω',r'\omega'),
        ('Δ',r'\Delta'),('Σ',r'\Sigma'),('Ω',r'\Omega'),('Φ',r'\Phi'),('Γ',r'\Gamma'),
    ]:
        s = s.replace(char, cmd + '{}')
    # Subscripts with braces
    s = re.sub(r'([A-Za-z])_\{([^}]+)\}', r'\1_{\2}', s)
    # Simple subscripts
    def sub_repl(m):
        base, sub = m.group(1), m.group(2)
        if len(sub) == 1:
            return f'{base}_{sub}'
        return f'{base}_{{\\text{{{sub}}}}}'
    s = re.sub(r'(?<!\{)([A-Za-z])_([A-Za-z0-9]+)', sub_repl, s)
    # Unicode superscripts
    sup_map = {'⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9','⁻':'-','⁺':'+'}
    result = []
    i = 0
    while i < len(s):
        if s[i] in sup_map:
            sup = []
            while i < len(s) and s[i] in sup_map:
                sup.append(sup_map[s[i]])
                i += 1
            result.append('^{' + ''.join(sup) + '}')
        else:
            result.append(s[i])
            i += 1
    s = ''.join(result)
    s = s.replace('·', r'\cdot')
    s = s.replace('~', r'\sim ')
    s = s.replace('>=', r'\geq ')
    s = s.replace('->', r'\to ')
    return s


# ── Hardcoded tables as LaTeX ──
TABLES = {}

TABLES[1] = r"""
\begin{table}[h]
\centering
\caption{Assumption budget. All six assumptions are required simultaneously.}
\label{tab:assumptions}
\small
\begin{tabular}{clll}
\hline
\textbf{\#} & \textbf{Assumption} & \textbf{Status} & \textbf{If wrong} \\
\hline
1 & \parbox[t]{4.5cm}{Hawking radiation exists and is semiclassical at $M \sim 10^9$\,kg} & \parbox[t]{4cm}{Near-universal consensus; never observed} & No power source \\[6pt]
2 & GUT magnetic monopoles exist & \parbox[t]{4cm}{Predicted by all GUTs; never observed [11]} & No formation mechanism \\[6pt]
3 & \parbox[t]{4.5cm}{BPS limit ($\lambda = 0$ at GUT scale)} & \parbox[t]{4cm}{Protected by $N{=}2$ SUSY [12]; untested} & \parbox[t]{3cm}{Monopole cloud cannot collapse} \\[6pt]
4 & \parbox[t]{4.5cm}{Bodmer--Witten hypothesis (SQM is ground state)} & \parbox[t]{4cm}{Bai and Chen 2025 constrains unpaired SQM but not CFL} & No shell material \\[6pt]
5 & \parbox[t]{4.5cm}{CFL is ground state at operating chemical potential} & \parbox[t]{4cm}{Theoretical [13, 14]; never observed} & \parbox[t]{3cm}{Gap-decoupling firewall fails} \\[6pt]
6 & \parbox[t]{4.5cm}{Core-overlap monopole breeding at $O(1)$ rate} & \parbox[t]{4cm}{Derived from duality [12]; unsimulated} & \parbox[t]{3cm}{Cannot manufacture monopole inventory} \\
\hline
\end{tabular}
\end{table}
"""

TABLES[2] = r"""
\begin{table}[h]
\centering
\caption{Species contributions to $f$.}
\label{tab:species}
\small
\begin{tabular}{lllll}
\hline
\textbf{Species} & \textbf{DOF} & \textbf{$m/kT$} & \textbf{$S(m/kT)$} & \textbf{Contribution to $f$} \\
\hline
$u, d, s$ quarks & 36 Weyl & $\sim$0 & 1.000 & $1.472 \times 10^{-3}$ \\
$c$ quark & 12 Weyl & 0.120 & 1.000 & $4.91 \times 10^{-4}$ \\
$b$ quark & 12 Weyl & 0.395 & 0.9995 & $4.91 \times 10^{-4}$ \\
$t$ quark & 12 Weyl & 16.36 & $1.2 \times 10^{-5}$ & $3.6 \times 10^{-8}$ \\
$e, \mu$ leptons & 8 Weyl & $\sim$0 & 1.000 & $3.27 \times 10^{-4}$ \\
$\tau$ lepton & 4 Weyl & 0.168 & 1.000 & $1.64 \times 10^{-4}$ \\
Neutrinos (3 gen.) & 6 Weyl & 0 & 1.000 & $2.45 \times 10^{-4}$ \\
Gluons & 16 pol. & 0 & 1.000 & $2.69 \times 10^{-4}$ \\
Photon & 2 pol. & 0 & 1.000 & $3.36 \times 10^{-5}$ \\
$W^{\pm}$ & 6 pol. & 7.60 & 0.0511 & $5.15 \times 10^{-6}$ \\
$Z$ & 3 pol. & 8.63 & 0.0255 & $1.29 \times 10^{-6}$ \\
Higgs & 1 & 11.83 & 0.0024 & $1.74 \times 10^{-7}$ \\
Graviton & 2 pol. & 0 & 1.000 & $3.84 \times 10^{-6}$ \\
\hline
TOTAL & & & & $f = 3.503 \times 10^{-3}$ \\
\hline
\end{tabular}
\end{table}
"""

TABLES[3] = r"""
\begin{table}[h]
\centering
\caption{SQM shell parameters.}
\label{tab:shell}
\small
\begin{tabular}{ll}
\hline
\textbf{Parameter} & \textbf{Value} \\
\hline
Inner radius $R$ & 2\,m \\
Thickness $t$ & 3\,pm (3000\,fm) \\
Density $\rho$ & $4 \times 10^{17}$\,kg/m$^3$ ($\sim$2$\times$ nuclear) \\
Mass $M_\text{shell}$ & $6.0 \times 10^7$\,kg (60,000\,t) \\
Surface area $A$ & $4\pi R^2 = 50.3$\,m$^2$ \\
Phase & Colour-flavour locked (CFL) \\
Inner surface state & Bombardment-maintained electrosphere \\
Outer surface state & Ground-state electrosphere \\
\hline
\end{tabular}
\end{table}
"""

TABLES[4] = r"""
\begin{table}[h]
\centering
\caption{Shell thickness versus muon punch-through.}
\label{tab:punchthrough}
\small
\begin{tabular}{llllll}
\hline
\textbf{$t$ (fm)} & \textbf{$E_c$ (GeV)} & \textbf{$x_c$} & \textbf{$\varepsilon(x_c)$} & \textbf{$P_\text{punch}$ (muon)} & \textbf{$M_\text{shell}$ (t)} \\
\hline
640 & 51 & 4.84 & $6.8 \times 10^{-2}$ & 380\,TW & 12,900 \\
2,500 & 200 & 18.9 & $4.7 \times 10^{-7}$ & 2.6\,GW & 50,000 \\
3,000* & 240 & 22.7 & $1.5 \times 10^{-8}$ & 84\,MW & 60,000 \\
4,000 & 320 & 30.3 & $1.3 \times 10^{-11}$ & 74\,kW & 80,000 \\
5,000 & 400 & 37.8 & $1.0 \times 10^{-14}$ & 58\,W & 100,000 \\
\hline
\multicolumn{6}{l}{\footnotesize * Adopted design point.} \\
\end{tabular}
\end{table}
"""

TABLES[5] = r"""
\begin{table}[h]
\centering
\caption{Thrust scaling with black hole mass.}
\label{tab:thrust}
\small
\begin{tabular}{llllll}
\hline
\textbf{$M$ (kg)} & \textbf{$kT$ (GeV)} & \textbf{$F$ (MN)} & \textbf{Shell} & \textbf{Fuel rate} & \textbf{Alpha Cen} \\
\hline
$10^9$* & 10.6 & 55 & 3\,pm, 60\,kt & 0.67\,kg/s & 79\,yr, $v_\text{peak}$\,0.07$c$, $R{=}1.7$ \\
$2 \times 10^8$ & 53 & 1,375 & 10\,pm, 200\,kt & 17\,kg/s & 19\,yr, $v_\text{peak}$\,0.30$c$, $R{=}9.4$ \\
$5 \times 10^7$ & 212 & 21,800 & 30\,pm, 600\,kt & 264\,kg/s & 11\,yr, $v_\text{peak}$\,0.45$c$, $R{=}34$ \\
\hline
\multicolumn{6}{l}{\footnotesize * Reference design.} \\
\end{tabular}
\end{table}
"""

TABLES[6] = r"""
\begin{table}[h]
\centering
\caption{Mission profiles with relativistic Tsiolkovsky accounting.}
\label{tab:missions}
\small
\begin{tabular}{llllll}
\hline
\textbf{Target} & \textbf{Design} & \textbf{$v_\text{peak}$} & \textbf{Mass ratio $R$} & \textbf{Fuel ($\times M_\text{dry}$)} & \textbf{Trip time} \\
\hline
Alpha Cen (4.37\,ly) & Reference ($10^9$\,kg) & 0.07$c$ & 1.7 & 0.7$\times$ & 79\,yr \\
Alpha Cen & High-thrust ($2{\times}10^8$\,kg) & 0.30$c$ & 9.4 & 8.4$\times$ & 19\,yr \\
Alpha Cen & Sprint ($5{\times}10^7$\,kg) & 0.45$c$ & 34 & 33$\times$ & 11\,yr \\
10\,ly & Reference & 0.10$c$ & 2.0 & 1.0$\times$ & 113\,yr \\
10\,ly & High-thrust & 0.35$c$ & 14 & 13$\times$ & 36\,yr \\
100\,ly & High-thrust & 0.50$c$ & 54 & 53$\times$ & 220\,yr \\
\hline
\end{tabular}
\end{table}
"""

TABLES[7] = r"""
\begin{table}[h]
\centering
\caption{Comparison to prior work.}
\label{tab:comparison}
\small
\begin{tabular}{lllll}
\hline
 & \textbf{Crane \& W. 2009} & \textbf{Lee 2015} & \textbf{Present (ref.)} & \textbf{Present (sprint)} \\
\hline
Capture mechanism & \parbox[t]{2.5cm}{``Electron gas mirror'' (unspecified)} & \parbox[t]{2.2cm}{Titanium absorption} & \parbox[t]{2.5cm}{CFL SQM thermal converter} & Same \\[6pt]
Capture fraction & Assumed $\sim$100\% & 46.5\% & 83\% & 83\% \\
Alpha Cen trip & Not calculated & Not achievable & 79\,yr at 0.07$c$ & 11\,yr at 0.45$c$ \\
Thrust & Not calculated & --- & 55\,MN & 21,800\,MN \\
$I_\text{sp}$ & Not calculated & --- & $1.01 \times 10^7$\,s & Same \\
Fuel & Not specified & N/A & Any matter & \parbox[t]{2cm}{Any matter ($33\times M_\text{dry}$)} \\[4pt]
Thermal limit & Not addressed & \parbox[t]{2.2cm}{Titanium melting (33\,km standoff)} & \parbox[t]{2.5cm}{None (Usov self-regulation)} & Same \\[6pt]
Confinement & ``Particle beams'' & None & Anti-Helmholtz & Same \\
Formation & \parbox[t]{2.5cm}{Gamma-ray kugelblitz} & N/A & \parbox[t]{2.5cm}{BPS monopole collapse} & Same \\
\hline
\end{tabular}
\end{table}
"""

# Table injection points (inject BEFORE this section/subsection)
INJECT_BEFORE = {
    '1.4': [1],
    '2.4': [2],
    '3.3': [3],
    '3.5': [4],
    '6.2': [5],
    '6.5': [6],
    '7.': [7],
}

eq_re = re.compile(r'\((\d+)\)\s*$')

# Build LaTeX
tex = []
tex.append(r"""\documentclass[12pt,a4paper]{article}
\usepackage[margin=2.54cm]{geometry}
\usepackage{amsmath,amssymb}
\usepackage{times}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{textcomp}
\usepackage{booktabs}
\usepackage{array}

\title{\textbf{SOLVING THE THREE OPEN PROBLEMS OF BLACK HOLE PROPULSION}}
\author{B.\ Greff \\ Independent Researcher \\ Correspondence: ben@thegreffs.com}
\date{}

\begin{document}
\maketitle
\thispagestyle{empty}
""")

i = 0
past_refs = False
skip_end = False
in_abstract = False

while i < len(lines):
    line = lines[i]
    s = line.strip()
    if not s:
        i += 1
        continue

    leading = len(line) - len(line.lstrip())

    # Skip TABLES and FIGURE CAPTIONS end-matter
    if s in ('TABLES', 'FIGURE CAPTIONS'):
        skip_end = True
        i += 1; continue
    if skip_end:
        i += 1; continue

    # Skip title/author (handled by \maketitle)
    if 'SOLVING THE THREE OPEN PROBLEMS' in s or s in ('B. Greff', 'Independent Researcher') or s.startswith('Correspondence:'):
        i += 1; continue

    # Abstract
    if s.startswith('Black hole propulsion --'):
        tex.append(r'\begin{abstract}')
        tex.append(r'\noindent ' + latex_escape(s))
        tex.append(r'\end{abstract}')
        i += 1; continue

    # Keywords
    if s.startswith('Keywords:'):
        tex.append(r'\noindent \textit{' + latex_escape(s) + '}')
        tex.append(r'\bigskip')
        i += 1; continue

    # REFERENCES
    if s == 'REFERENCES':
        past_refs = True
        tex.append(r'\section*{REFERENCES}')
        tex.append(r'\small')
        tex.append(r'\begin{enumerate}')
        i += 1; continue

    # ACKNOWLEDGEMENTS
    if s == 'ACKNOWLEDGEMENTS':
        past_refs = False
        tex.append(r'\section*{ACKNOWLEDGEMENTS}')
        i += 1; continue

    # Ref items
    if past_refs and re.match(r'^\d+\.\s+', s):
        ref_text = re.sub(r'^\d+\.\s+', '', s)
        tex.append(r'\item ' + latex_escape(ref_text))
        i += 1; continue

    # End references list before next section
    if past_refs and not re.match(r'^\d+\.\s+', s):
        tex.append(r'\end{enumerate}')
        tex.append(r'\normalsize')
        past_refs = False
        # Don't increment i, reprocess this line

    # Section headings — check for table injection
    sec_match = re.match(r'^(\d+)\.\s+(.+)', s)
    if sec_match and re.match(r'^\d+\.\s+[A-Z]{2}', s):
        sec_num = sec_match.group(1) + '.'
        if sec_num in INJECT_BEFORE:
            for tbl_num in INJECT_BEFORE[sec_num]:
                tex.append(TABLES[tbl_num])
        sec_title = sec_match.group(2)
        tex.append(r'\section{' + latex_escape(sec_title) + '}')
        i += 1; continue

    # Subsection headings — check for table injection
    sub_match = re.match(r'^(\d+\.\d+)\s+(.+)', s)
    if sub_match:
        sub_num = sub_match.group(1)
        if sub_num in INJECT_BEFORE:
            for tbl_num in INJECT_BEFORE[sub_num]:
                tex.append(TABLES[tbl_num])
        sub_title = sub_match.group(2)
        tex.append(r'\subsection{' + latex_escape(sub_title) + '}')
        i += 1; continue

    # Numbered equations
    m = eq_re.search(s)
    if leading >= 16 and m:
        eq_num = int(m.group(1))
        if eq_num in EQ:
            tex.append(r'\begin{equation}')
            tex.append(EQ[eq_num])
            tex.append(r'\end{equation}')
        else:
            eq_text = s[:m.start()].rstrip()
            tex.append(r'\begin{equation}')
            tex.append(latex_escape(eq_text))
            tex.append(r'\end{equation}')
        i += 1; continue

    # Unnumbered centered equations
    if leading >= 16 and s and not s.startswith('Table') and not s.startswith('Figure'):
        tex.append(r'\[')
        tex.append(latex_math(s))
        tex.append(r'\]')
        i += 1; continue

    # Skip figure placeholders
    if '[INSERT FIGURE' in s:
        i += 1; continue

    # Skip table captions/data (tables injected at section boundaries)
    if s.startswith('Table ') and len(s) > 6 and s[6:7].isdigit():
        i += 1; continue
    if s.startswith('Figure ') and len(s) > 7 and s[7:8].isdigit():
        i += 1; continue

    # Table data rows — skip
    if line.startswith('  ') and leading < 16 and leading >= 2:
        while i < len(lines):
            ln = lines[i]
            st2 = ln.strip()
            ld = len(ln) - len(ln.lstrip())
            if not st2: i += 1; break
            if ld < 2: break
            if ld >= 16: break
            if st2.startswith('Table ') or st2.startswith('Figure ') or st2.startswith('[INSERT'): break
            if re.match(r'^\d+\.\s+[A-Z]{2}', st2) or re.match(r'^\d+\.\d+\s+\w', st2): break
            i += 1
        continue

    # Numbered list items (conclusion)
    if re.match(r'^(\d+)\.\s+\w', s) and not past_refs and not re.match(r'^\d+\.\s+[A-Z]{2}', s) and not re.match(r'^\d+\.\d+', s):
        num_match = re.match(r'^(\d+)\.\s+(.+)', s)
        if num_match:
            if num_match.group(1) == '1':
                tex.append(r'\begin{enumerate}')
            tex.append(r'\item ' + latex_escape(num_match.group(2)))
            # Check if next non-empty line is also a list item
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and not re.match(r'^\d+\.\s+\w', lines[j].strip()):
                tex.append(r'\end{enumerate}')
        i += 1; continue

    # Normal paragraph
    tex.append(latex_escape(s))
    tex.append('')  # blank line = paragraph break
    i += 1

# Close any open environments
if past_refs:
    tex.append(r'\end{enumerate}')
    tex.append(r'\normalsize')

tex.append(r'\end{document}')

# Write .tex file
tex_content = '\n'.join(tex)
tex_path = 'drafts/GREFF_2026_paper.tex'
with open(tex_path, 'w') as f:
    f.write(tex_content)
print(f'LaTeX written: {tex_path}')

# Compile with tectonic
pdf_path = 'drafts/GREFF_2026_paper.pdf'
result = subprocess.run(
    ['tectonic', '-o', 'drafts', tex_path],
    capture_output=True, text=True, timeout=120
)
if result.returncode == 0:
    print(f'PDF compiled: {pdf_path} ({os.path.getsize(pdf_path)//1024} KB)')
else:
    print(f'Tectonic errors:\n{result.stderr[-2000:]}')
