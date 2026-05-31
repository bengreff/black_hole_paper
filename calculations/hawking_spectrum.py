"""
Hawking spectrum species counting at kT = 2.68 GeV.

This script reproduces the emission factor f from Page's greybody coefficients,
counting all Standard Model species with rest energy below ~kT.

Reference: Page 1976, Dong et al. 2016 (arXiv:1712.07664)
"""

import numpy as np

# Power-rate greybody transmission coefficients (Page 1976, power-rate convention)
# Per degree of freedom
ALPHA_SCALAR = 7.24e-5      # spin 0
ALPHA_FERMION = 4.09e-5     # spin 1/2 (Weyl fermion)
ALPHA_VECTOR = 1.68e-5      # spin 1 (per polarization)
ALPHA_GRAVITON = 1.92e-6    # spin 2 (per polarization)

# Hawking temperature
def hawking_temperature_keV(M_kg):
    """Hawking temperature kT in GeV for mass M in kg."""
    hbar = 1.0546e-34
    c = 2.998e8
    G = 6.6743e-11
    kB = 1.3806e-23
    T = hbar * c**3 / (8 * np.pi * G * M_kg * kB)
    kT_GeV = kB * T / 1.602e-10  # convert J to GeV
    return kT_GeV

# Standard Model particle data
# (name, spin_type, DOF, mass_GeV)
# spin_type: 'scalar', 'fermion', 'vector', 'graviton'
# DOF: number of independent degrees of freedom
#   fermion DOF = Weyl fermions (each Dirac fermion = 2 Weyl)
#   vector DOF = polarizations
SM_PARTICLES = [
    # Quarks: each flavor has 3 colors, particle+antiparticle, 2 helicities = 12 Weyl DOF
    ("up quark",       "fermion", 12, 0.0022),
    ("down quark",     "fermion", 12, 0.0047),
    ("strange quark",  "fermion", 12, 0.095),
    ("charm quark",    "fermion", 12, 1.27),
    ("bottom quark",   "fermion", 12, 4.18),
    ("top quark",      "fermion", 12, 173.0),

    # Charged leptons: particle+antiparticle, 2 helicities = 4 Weyl DOF each
    ("electron",       "fermion", 4, 0.000511),
    ("muon",           "fermion", 4, 0.1057),
    ("tau",            "fermion", 4, 1.777),

    # Neutrinos: 3 flavors, particle+antiparticle, 1 helicity each = 6 Weyl DOF
    ("neutrinos",      "fermion", 6, 0.0),

    # Gluons: 8 colors, 2 polarizations = 16 vector polarizations
    ("gluons",         "vector", 16, 0.0),

    # Photon: 2 polarizations
    ("photon",         "vector", 2, 0.0),

    # W bosons: W+ and W-, 3 polarizations each = 6
    ("W bosons",       "vector", 6, 80.4),

    # Z boson: 3 polarizations
    ("Z boson",        "vector", 3, 91.2),

    # Higgs: 1 scalar DOF
    ("Higgs",          "scalar", 1, 125.0),

    # Graviton: 2 polarizations
    ("graviton",       "graviton", 2, 0.0),
]

def boltzmann_suppression(mass_GeV, kT_GeV):
    """Approximate suppression factor for massive species."""
    if mass_GeV == 0:
        return 1.0
    x = mass_GeV / kT_GeV
    if x > 10:
        return 0.0
    # Rough suppression from thermal spectrum integration
    # More accurate would use the full greybody + thermal integral
    return np.exp(-x) * (1 + x + 0.5 * x**2)  # crude approximation

def compute_emission_factor(M_kg, verbose=True):
    """Compute the emission factor f(M) for a BH of mass M."""
    kT = hawking_temperature_keV(M_kg)
    if verbose:
        print(f"Black hole mass: {M_kg:.3e} kg")
        print(f"Hawking temperature kT: {kT:.3f} GeV")
        print(f"{'Species':<20} {'Type':<10} {'DOF':>5} {'Mass (GeV)':>12} {'Suppression':>12} {'Contribution':>14}")
        print("-" * 85)

    f_total = 0.0
    f_neutrino = 0.0

    for name, spin_type, dof, mass in SM_PARTICLES:
        supp = boltzmann_suppression(mass, kT)

        if spin_type == "scalar":
            alpha = ALPHA_SCALAR
        elif spin_type == "fermion":
            alpha = ALPHA_FERMION
        elif spin_type == "vector":
            alpha = ALPHA_VECTOR
        elif spin_type == "graviton":
            alpha = ALPHA_GRAVITON

        contribution = dof * alpha * supp
        f_total += contribution

        if "neutrino" in name:
            f_neutrino += contribution

        if verbose and supp > 1e-6:
            print(f"{name:<20} {spin_type:<10} {dof:>5} {mass:>12.4f} {supp:>12.4f} {contribution:>14.6e}")

    if verbose:
        print("-" * 85)
        print(f"{'Total f':<20} {'':>10} {'':>5} {'':>12} {'':>12} {f_total:>14.6e}")
        print(f"{'Neutrino fraction':<20} {'':>10} {'':>5} {'':>12} {'':>12} {f_neutrino/f_total:>14.4f}")
        print()

        # Derived quantities
        hbar = 1.0546e-34
        c = 2.998e8
        G = 6.6743e-11

        dMdt = hbar * c**4 * f_total / (G**2 * M_kg**2)
        tau = G**2 * M_kg**3 / (3 * hbar * c**4 * f_total)
        P = dMdt * c**2

        print(f"Mass loss rate: {dMdt*1000:.2f} g/s")
        print(f"Lifetime: {tau:.3e} s = {tau/(365.25*86400):.0f} years")
        print(f"Total power: {P:.3e} W = {P/1e12:.0f} TW")
        print(f"Non-neutrino power: {P*(1-f_neutrino/f_total):.3e} W = {P*(1-f_neutrino/f_total)/1e12:.0f} TW")
        print(f"Thrust (F = P_beam/c): {P*(1-f_neutrino/f_total)/c:.3e} N = {P*(1-f_neutrino/f_total)/c/1e6:.2f} MN")
        print(f"Isp: {P*(1-f_neutrino/f_total)/c / (dMdt * 9.81):.3e} s")

    return f_total, f_neutrino

if __name__ == "__main__":
    print("=" * 85)
    print("HAWKING SPECTRUM SPECIES COUNTING")
    print("=" * 85)
    print()

    # Operational mass
    M_operational = 3.94e9  # kg
    f, f_nu = compute_emission_factor(M_operational)

    print()
    print("=" * 85)
    print("NOTE: The Boltzmann suppression used here is approximate.")
    print("For the paper, use the full thermal integral with greybody factors.")
    print("This script is a starting point for verification, not a final result.")
    print("=" * 85)
