"""
Secondary neutrino loss fraction from the Hawking spectrum.

Tightens the §3 first-principles estimate by explicitly tabulating PDG decay
branching ratios for each post-hadronization species.  Substitute for the
BlackHawk/PYTHIA integration listed as Task D in HANDOFF_PLAN.md; the result
should be reconciled against BlackHawk in a future pass.

Reference: PDG 2024 Review of Particle Physics, Phys. Rev. D 110, 030001.

Method:
  1. Take Hawking-power energy fractions per species from verify_design.py.
  2. Quark+gluon fraction (~78% of P_H) hadronizes; partition into
     pi+-, pi0, K+-, K_S, K_L, p/pbar, n/nbar, other.
  3. For each charged hadron species, fold KE deposition (captured) with
     decay-at-rest neutrino fraction.
  4. For taus, fold in-flight decay (~50% of tau energy to neutrinos averaged
     over all channels).
  5. For direct muons at ~GeV (Hawking-spectrum-peak energy), the secondary-
     decay ν fraction per muon is m_mu / (2 E_mu) -- small at GeV energies.
"""

import numpy as np

def banner(s):
    print("\n" + "="*78); print(s); print("="*78)

# Hawking energy-fraction distribution at M = 1e9 kg
# (these reproduce verify_design.py §3 within 1%)
f_qg = 0.776         # quark + gluon power fraction
f_mu = 0.0467        # direct muon fraction
f_tau = 0.0467       # direct tau fraction (same as mu by accident -- mass suppression similar)
f_nu_prim = 0.0701   # primary neutrino
f_e_direct = 0.094   # direct e- emission + photon -> e+e- conversion
f_grav = 0.001

# Mass scales (MeV)
m_pi = 139.6
m_pi0 = 135.0
m_K = 493.7
m_K0 = 497.6
m_p = 938.3
m_mu = 105.7
m_tau = 1776.9
m_e = 0.511

# =============================================================================
# 1. HADRONIZATION DISTRIBUTION (LEP/SLC/B-factory data, ~10 GeV jets)
# =============================================================================
banner("1. HADRONIC ENERGY FRACTIONS (per jet, PDG fragmentation data)")

# Energy fractions of jet energy carried by each species (approximate,
# averaged over quark vs gluon jets, PDG 2024 fragmentation function tables):
f_hadron = {
    "pi+-":   0.50,    # leading hadron + spectators
    "pi0":    0.25,    # half of charged-pion fraction by isospin
    "K+-":    0.10,
    "K0":     0.05,    # K_S + K_L combined
    "p+pbar": 0.04,
    "n+nbar": 0.03,
    "other":  0.03,    # eta, eta', omega, etc.
}
print(f"  Sum = {sum(f_hadron.values()):.3f}")
for s, f in f_hadron.items():
    print(f"    {s:<10s}  {f:.2%}")

# Typical particle energy after hadronization at sqrt(s) = 10 GeV jet pair:
# multiplicity ~ 10, so <E_hadron> ~ 1 GeV (about half is in the leading hadron,
# but for our estimate we'll use the mean).
E_typical_hadron_MeV = 1000.0

# =============================================================================
# 2. NEUTRINO FRACTION PER SPECIES (decay-at-rest, then KE-weighted)
# =============================================================================
banner("2. NEUTRINO FRACTION PER STOPPED HADRON (decay-at-rest)")

# Per stopped charged pion (pi+ -> mu+ + nu_mu, then mu+ -> e+ + nu_e + nu_mu_bar)
# Decay at rest: ν_μ from π carries (m_π^2 - m_μ^2)/(2 m_π) MeV = 29.8 MeV
nu_pi_first  = (m_pi**2 - m_mu**2) / (2 * m_pi)
# Stopped muon: Michel spectrum gives e ~ 52.8 MeV avg, 2 nu carry ~52.9 MeV total
nu_mu_from_pi = m_mu * 0.50
nu_per_pi_at_rest = nu_pi_first + nu_mu_from_pi
ratio_pi = nu_per_pi_at_rest / m_pi
print(f"  Stopped pi+ chain:")
print(f"    nu_mu (pi -> mu nu): {nu_pi_first:.1f} MeV  ({nu_pi_first/m_pi*100:.1f}% of m_pi)")
print(f"    2nu (mu -> e 2nu):   {nu_mu_from_pi:.1f} MeV  ({nu_mu_from_pi/m_pi*100:.1f}% of m_pi)")
print(f"    TOTAL nu per pi:     {nu_per_pi_at_rest:.1f} MeV  ({ratio_pi*100:.1f}% of m_pi rest mass)")

# Stopped pi0 -> 2 gamma -> e+e- (pair-converts in BH field):  0% nu
print(f"  Stopped pi0 -> 2 gamma: 0% nu (pair-converts in BH field, no weak decay)")

# K+- BR-weighted neutrino fraction:
# K+ -> mu+ nu (63.4%)  +  K+ -> pi+ pi0 (20.7%)  +  K+ -> pi+ pi+ pi- (5.6%) + others
# Approximate: average nu fraction per K+ decay at rest ~ 0.50 m_K (the mu-nu chain
# alone gives nu_mu(K) = (m_K^2-m_mu^2)/(2 m_K) = 235 MeV = 47.6% of m_K, plus the
# subsequent muon decay adds another 0.5*m_mu = 52.8 MeV)
nu_K_mu_first = (m_K**2 - m_mu**2)/(2*m_K)
nu_K_chain    = 0.634 * (nu_K_mu_first + 0.5*m_mu) \
              + 0.207 * (0.213 * m_pi)              \
              + 0.056 * (3*0.213 * m_pi/2)          \
              + 0.10  * (0.30 * m_K)
ratio_K = nu_K_chain / m_K
print(f"  Stopped K+ (BR-weighted): TOTAL nu = {nu_K_chain:.1f} MeV "
      f"({ratio_K*100:.1f}% of m_K rest mass)")

# K_L semi-leptonic decays: BR(K_L -> pi e nu) = 41%, BR(K_L -> pi mu nu) = 27%,
# BR(K_L -> 3 pi) ~ 30%.  Average nu per K_L decay ~ 0.20 m_K.
ratio_K0 = 0.20
nu_per_K0 = ratio_K0 * m_K0
print(f"  K_L (BR-weighted): TOTAL nu ~ {nu_per_K0:.1f} MeV ({ratio_K0*100:.1f}% of m_K)")

# Stopped antiprotons annihilate with shell protons -> ~5 pions.  Each pion
# then decays as above.  Average: ~ 50% of (m_p + m_pbar) c^2 = 1876 MeV is
# released into pions of typical energy 400 MeV each, then nu fraction per pion
# folds the in-flight decay (ratio_pi for at-rest plus extra KE smearing).
# Rough estimate: 30% of m_p_pair -> nu.
nu_per_pbar_pair = 0.30 * 2 * m_p
ratio_pbar = nu_per_pbar_pair / (2*m_p)
print(f"  p + pbar annihilation: TOTAL nu = {nu_per_pbar_pair:.1f} MeV "
      f"({ratio_pbar*100:.1f}% of pair rest mass)")

# Stopped proton: absorbed into baryon number, no weak decay -> 0% nu
# Stopped neutron: free n half-life 880 s; in SQM these are absorbed before decay
print(f"  Stopped p: 0% nu (absorbed into baryon sea)")
print(f"  Stopped n: 0% nu (absorbed before free decay can occur)")
print(f"  Stopped nbar: ~ same as pbar (annihilation chain)")

# =============================================================================
# 3. ENERGY-WEIGHTED SECONDARY-NU FRACTION FROM HADRONIZATION
# =============================================================================
banner("3. ENERGY-WEIGHTED HADRONIC nu FRACTION")

# Pion energy in jet: E_pi ~ 1 GeV.  Per pion total energy:
# nu fraction = (nu rest-mass fraction * m_pi) / E_pi   (KE thermalized in shell)
# For E_pi = 1 GeV, ratio_pi * m_pi / E_pi = 0.607 * 0.140 = 8.5% of pion energy
hadronic_nu_fraction_components = {}
contrib_per_species = {}

E_pi_typical = E_typical_hadron_MeV
nu_frac_pi = ratio_pi * m_pi / E_pi_typical
contrib_per_species["pi+-"] = f_hadron["pi+-"] * nu_frac_pi
print(f"  pi+- at E_pi = {E_pi_typical/1000:.1f} GeV: nu fraction per pi = "
      f"{nu_frac_pi*100:.2f}% of pi energy; contributes "
      f"{contrib_per_species['pi+-']*100:.2f}% of hadronic")

nu_frac_pi0 = 0.0
contrib_per_species["pi0"] = f_hadron["pi0"] * nu_frac_pi0
print(f"  pi0:                                       contributes 0%")

E_K_typical = 1500.0    # kaons are heavier; carry slightly more energy
nu_frac_K = ratio_K * m_K / E_K_typical
contrib_per_species["K+-"] = f_hadron["K+-"] * nu_frac_K
print(f"  K+- at E_K = {E_K_typical/1000:.1f} GeV: nu fraction per K = "
      f"{nu_frac_K*100:.2f}% of K energy; contributes "
      f"{contrib_per_species['K+-']*100:.2f}% of hadronic")

nu_frac_K0 = ratio_K0 * m_K0 / E_K_typical
contrib_per_species["K0"] = f_hadron["K0"] * nu_frac_K0
print(f"  K0 (K_S + K_L): nu fraction per K0 = "
      f"{nu_frac_K0*100:.2f}% of K0 energy; contributes "
      f"{contrib_per_species['K0']*100:.2f}% of hadronic")

# nucleons: only p+pbar fraction contributes (pbar annihilates; p just absorbed)
# Among p+pbar, half is antiprotons.
E_p_typical = 2000.0
nu_frac_pbar = ratio_pbar * (2*m_p) / E_p_typical
contrib_per_species["p+pbar"] = 0.5 * f_hadron["p+pbar"] * nu_frac_pbar
print(f"  p+pbar (antiproton half): nu fraction per pbar pair = "
      f"{nu_frac_pbar*100:.2f}% of pair energy; contributes "
      f"{contrib_per_species['p+pbar']*100:.2f}% of hadronic")

# n+nbar: same accounting as p+pbar
contrib_per_species["n+nbar"] = 0.5 * f_hadron["n+nbar"] * nu_frac_pbar
print(f"  n+nbar: ~same accounting; contributes "
      f"{contrib_per_species['n+nbar']*100:.2f}% of hadronic")

# Other hadrons (eta, omega, etc.): mostly decay via gamma or pi chains.
# Rough estimate 5% nu per "other".
contrib_per_species["other"] = f_hadron["other"] * 0.05
print(f"  other (eta, etc.): rough 5% nu; contributes "
      f"{contrib_per_species['other']*100:.2f}% of hadronic")

hadronic_nu_frac = sum(contrib_per_species.values())
print(f"\n  Total hadronic nu fraction: {hadronic_nu_frac*100:.2f}% of hadronic energy")
print(f"  Hadronic energy fraction of P_H: {f_qg*100:.1f}%")
print(f"  Hadronic-channel nu contribution to P_H: {hadronic_nu_frac*f_qg*100:.2f}%")

# =============================================================================
# 4. DIRECT-LEPTON CONTRIBUTIONS
# =============================================================================
banner("4. DIRECT-LEPTON nu CONTRIBUTIONS")

# Direct muons: typical Hawking-spectrum energy ~10 GeV (peak), some at higher E.
# Most stop in the shell (3 pm stopping budget = 240 GeV).
# Per stopped muon at rest: 50% of m_mu to nu = 53 MeV.
# Per muon with E_mu = 10 GeV: nu fraction = 53/10000 = 0.53%
E_mu_typical = 10000.0
nu_frac_mu_each = 0.5 * m_mu / E_mu_typical
mu_channel_nu = f_mu * nu_frac_mu_each
print(f"  Direct muons: E_mu ~ {E_mu_typical/1000:.0f} GeV typical")
print(f"    nu fraction per stopped muon = 0.5 m_mu / E_mu = {nu_frac_mu_each*100:.3f}%")
print(f"    direct-mu channel contribution to P_H: {mu_channel_nu*100:.3f}%")
print(f"  (this is much smaller than the design's prior 1.5% claim;")
print(f"   the prior estimate may have confused decay-at-rest with total)")

# Direct taus: decay in flight (lab decay length ~ 0.5 mm at gamma ~ 5).
# Tau-decay branching ratios:
#   tau -> ntau + e + nu_e_bar (17.8%)    - 2 nu carrying ~67% of m_tau
#   tau -> ntau + mu + nu_mu_bar (17.4%)  - 2 nu carrying ~50% of m_tau (mu rest mass stays)
#   tau -> ntau + hadrons (65%)           - 1 nu (n_tau) carrying ~33% of m_tau
# Average nu fraction of m_tau ~ 0.45.
# Plus, at E_tau ~ 10 GeV, total tau energy is split as nu fraction ~ 45% of m_tau / E_tau
# OR, if the tau decays in flight, the KE of products is partly carried by the nu too.
# For relativistic tau decay: ~33-50% of TOTAL tau energy goes to neutrinos.
E_tau_typical = 10000.0
nu_frac_tau_avg = 0.40
tau_channel_nu = f_tau * nu_frac_tau_avg
print(f"\n  Direct taus: E_tau ~ {E_tau_typical/1000:.0f} GeV typical, decay in flight")
print(f"    nu fraction per tau (averaged over channels) ~ {nu_frac_tau_avg*100:.0f}% of E_tau")
print(f"    direct-tau channel contribution to P_H: {tau_channel_nu*100:.2f}%")

# Direct electrons + photons: e+e- pair-convert in BH field, then synchrotron-cool
# in cavity, stop in shell.  No weak decays -> 0% nu.
print(f"\n  Direct electrons + pair-converted photons: 0% nu (no weak decay)")

# Charm and bottom quarks: enter hadronic chain via D and B meson decays.
# These are already approximately covered by the K and pi accounting above (D and B
# mesons decay to lighter hadrons + leptons before reaching the shell).
# At E_c, E_b ~ 10 GeV, the c/b weak decays give nu via semi-leptonic channels.
# BR(D -> Xe nu) ~ 16% per D meson; BR(B -> Xe nu) ~ 20% per B.
# Energy fraction of charm + bottom in P_H: (491+491)e-6 / 3503e-6 = 28%.
# But these are already part of f_qg.  Roughly 50% of the c and b energy ends up in
# semi-leptonic decays that produce additional nu beyond the pi/K chains.
f_cb_of_qg = (491 + 491) / 2723.0    # c+b fraction of quark+gluon
extra_nu_from_cb = 0.20 * 0.16        # 20% energy to semi-leptons, 16% leptonic BR -> 3.2%
extra_cb_nu = f_qg * f_cb_of_qg * extra_nu_from_cb
print(f"\n  Charm + bottom semi-leptonic decays: c+b fraction of P_qg = {f_cb_of_qg*100:.1f}%;")
print(f"    extra nu fraction from c, b semi-leptons (beyond pi/K chains): {extra_nu_from_cb*100:.2f}%")
print(f"    extra-cb contribution to P_H: {extra_cb_nu*100:.2f}%")

# =============================================================================
# 5. TOTAL SECONDARY-NU FRACTION
# =============================================================================
banner("5. TOTAL SECONDARY-NU FRACTION OF P_H")

total_secondary_nu = (
    hadronic_nu_frac * f_qg +
    mu_channel_nu +
    tau_channel_nu +
    extra_cb_nu
)
print(f"\n  Hadronization (pi, K, p, n chains): {hadronic_nu_frac * f_qg*100:>5.2f}% of P_H")
print(f"  Direct muons:                       {mu_channel_nu*100:>5.2f}% of P_H")
print(f"  Direct taus:                        {tau_channel_nu*100:>5.2f}% of P_H")
print(f"  Charm+bottom extra semi-leptonic:   {extra_cb_nu*100:>5.2f}% of P_H")
print(f"  ----------------------------------------")
print(f"  TOTAL SECONDARY nu:                 {total_secondary_nu*100:>5.2f}% of P_H")

# Combined with primary neutrinos:
print(f"\n  Primary nu (f_nu/f_total):          {f_nu_prim*100:>5.2f}% of P_H")
print(f"  Combined nu loss:                   {(f_nu_prim+total_secondary_nu)*100:>5.2f}% of P_H")
print(f"  Captured power (after nu losses):   "
      f"{(1 - f_nu_prim - total_secondary_nu)*100:>5.2f}% of P_H")

# =============================================================================
# 6. UNCERTAINTY ASSESSMENT
# =============================================================================
banner("6. UNCERTAINTY ASSESSMENT")

print("  Dominant uncertainty sources:")
print()
print("  (a) Energy-per-hadron <E_hadron>: assumed 1 GeV (jet multiplicity ~10).")
print("      Range 0.5-1.5 GeV is plausible; nu fractions scale as 1/E_hadron;")
print("      ~30% uncertainty in hadronic contribution.")
print()
print("  (b) Fragmentation fractions: ~10% uncertainty in pi/K/p split at sqrt(s)~10 GeV.")
print()
print("  (c) Tau nu fraction: 40% adopted; literature range 33-50%; ~25% uncertainty")
print("      in tau channel contribution.")
print()
print("  (d) Strong-B-field hadronization modifications (Task I): unknown effect on")
print("      the species mix; bounded order-of-magnitude.")
print()
print(f"  Combined uncertainty in total secondary nu: ~30-50%.")
print(f"  Best-estimate value: {total_secondary_nu*100:.1f}% of P_H.")
print(f"  Conservative design assumption (verify_design.py): 10% of P_H.")
print(f"  Difference: design conservatism = {(0.10 - total_secondary_nu)*100:.1f} percentage")
print(f"  points absorbed into the captured-power budget margin.")
print()
print("  CONCLUSION: the refined first-principles estimate is {0:.1f}%, against the".format(total_secondary_nu*100))
print("  design's 10% conservative assumption.  A full BlackHawk-PYTHIA integration")
print("  remains the gold standard for sub-1% precision, but the refined estimate")
print("  is within ~30% of the design assumption and does not motivate revising the")
print("  headline numbers downward (the conservative margin is preserved).")
