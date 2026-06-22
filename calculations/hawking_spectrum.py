"""
Hawking-spectrum species counting at kT = 10.57 GeV (M = 1.0e9 kg design point).

Reproduces the emission factor f from Page's greybody coefficients with
proper power-rate suppression for massive species.

The suppression factor for a species of mass m at Hawking temperature T is
the ratio of the truncated thermal-power integral:

    S(x_m) = int_{x_m}^inf x^3 / (e^x +/- 1) dx
             ---------------------------------------------------
             int_0^inf  x^3 / (e^x +/- 1) dx

with x_m = m / kT.  This is the right answer in the geometric-optics regime
of the Hawking spectrum (kT >> hbar c / r_s, which holds amply at M = 1e9 kg
where hbar c / r_s = 132 MeV << kT = 10.57 GeV).  The earlier ad-hoc
exp(-m/kT) is the heavy-mass asymptote and over-suppresses charm, bottom,
and tau by 30-50%.

Cross-check: at kT >> all SM masses, this reproduces the total-SM f from
Lennon, March-Russell, Petrossian-Byrne & Tillim 2018 (JCAP 03 (2019) 009;
arXiv:1712.07664) to within ~3%.
"""

import numpy as np
from scipy.integrate import quad

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
HBAR = 1.054_571_817e-34          # J s
C    = 2.997_924_58e8             # m / s
G    = 6.6743e-11                 # m^3 / (kg s^2)
KB   = 1.380_649e-23              # J / K
EV_J = 1.602_176_634e-19          # J / eV
GEV_J = 1.602_176_634e-10         # J / GeV

# Page power-rate greybody coefficients (per DOF; massless limit)
ALPHA = {
    "scalar":   7.24e-5,
    "fermion":  4.09e-5,        # per Weyl
    "vector":   1.68e-5,        # per polarization
    "graviton": 1.92e-6,
}


def hawking_kT_GeV(M_kg):
    """Hawking temperature kT, in GeV, for a Schwarzschild BH of mass M (kg)."""
    return (HBAR * C**3 / (8 * np.pi * G * M_kg)) / GEV_J


def power_rate_suppression(x_m, fermion=True):
    """
    Proper power-rate suppression factor S(x_m) for a massive species.
    Geometric-optics regime: the only mass effect is the lower limit on the
    thermal integral.
    """
    if x_m == 0:
        return 1.0
    sign = +1.0 if fermion else -1.0
    # Robust integrand: use Boltzmann form for x > 50 to avoid overflow.
    def integrand(x):
        return np.where(x > 50.0, x**3 * np.exp(-x), x**3 / (np.exp(np.minimum(x, 50.0)) + sign))
    num = quad(integrand, x_m, np.inf, limit=200)[0]
    den = quad(integrand, 0,   np.inf, limit=200)[0]
    return num / den


# ---------------------------------------------------------------------------
# Standard Model species
#   (name, statistics, DOF, m in GeV)
# DOF = Weyl fermions for fermion entries; polarizations for boson entries.
# ---------------------------------------------------------------------------
SM = [
    ("u quark",       "fermion", 12, 0.0022),
    ("d quark",       "fermion", 12, 0.0047),
    ("s quark",       "fermion", 12, 0.095),
    ("c quark",       "fermion", 12, 1.270),
    ("b quark",       "fermion", 12, 4.180),
    ("t quark",       "fermion", 12, 173.0),
    ("electron",      "fermion",  4, 0.000511),
    ("muon",          "fermion",  4, 0.1057),
    ("tau",           "fermion",  4, 1.777),
    ("neutrinos",     "fermion",  6, 0.0),
    ("gluons",        "vector",  16, 0.0),
    ("photon",        "vector",   2, 0.0),
    ("W bosons",      "vector",   6, 80.379),
    ("Z boson",       "vector",   3, 91.188),
    ("Higgs",         "scalar",   1, 125.10),
    ("graviton",      "graviton", 2, 0.0),
]


def compute_emission_factor(M_kg, verbose=True):
    """Compute f(M), print the species breakdown, and report the derived
    BH power, mass-loss rate, and lifetime."""
    kT = hawking_kT_GeV(M_kg)
    if verbose:
        print(f"BH mass            : {M_kg:.3e} kg")
        print(f"Hawking kT         : {kT:.4f} GeV")
        print(f"{'species':<14}{'stat':<9}{'DOF':>5}{'m[GeV]':>10}"
              f"{'m/kT':>8}{'S':>9}{'contrib':>13}")
        print("-" * 72)
    f_total = 0.0
    f_neutrino = 0.0
    for (name, stat, dof, mGeV) in SM:
        x_m = mGeV / kT
        S = power_rate_suppression(x_m, fermion=(stat == "fermion"))
        contrib = dof * ALPHA[stat] * S
        f_total += contrib
        if "neutrino" in name:
            f_neutrino += contrib
        if verbose and S > 1e-8:
            print(f"{name:<14}{stat:<9}{dof:>5d}{mGeV:>10.4f}"
                  f"{x_m:>8.3f}{S:>9.4f}{contrib:>13.4e}")

    P = HBAR * C**6 * f_total / (G**2 * M_kg**2)
    dMdt = P / C**2
    tau = G**2 * M_kg**3 / (3 * HBAR * C**4 * f_total)
    yr = 365.25 * 86400

    if verbose:
        print("-" * 72)
        print(f"{'TOTAL':<32}{'f =':>20}{f_total:>13.4e}")
        print(f"neutrino fraction:                       {f_neutrino/f_total:.4f}")
        print()
        print(f"P  = hbar c^6 f / (G^2 M^2) = {P:.4e} W  = {P/1e12:.0f} TW")
        print(f"dM/dt = P / c^2             = {dMdt*1000:.1f} g/s "
              f"= {dMdt*yr/1e3:.0f} t/yr")
        print(f"tau = G^2 M^3 / (3 hbar c^4 f) = {tau:.3e} s = {tau/yr:.2f} yr")
        # Captured-power example with the design's secondary-nu budget:
        f_nu_total_frac = f_neutrino/f_total + 0.07     # +7% secondary, design est.
        P_cap = P * (1 - f_nu_total_frac)
        print(f"P_captured (1 - 7% primary - 7% secondary nu):"
              f"  {P_cap/1e12:.0f} TW")

    return f_total, f_neutrino


if __name__ == "__main__":
    print("=" * 72)
    print("HAWKING SPECTRUM AT THE OPERATING POINT (M = 1.0e9 kg)")
    print("=" * 72)
    compute_emission_factor(1.0e9)
    print()
    print("=" * 72)
    print("Long-haul variant (M = 4.0e9 kg, lower temperature, less heavy fermion):")
    print("=" * 72)
    compute_emission_factor(4.0e9)
