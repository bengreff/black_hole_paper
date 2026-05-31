# Paper Strategic Plan

**Working Title:** Magnetically Charged Micro Black Holes as Photon Drive Sources: Formation, Confinement, and Performance

**Target Journal:** Journal of the British Interplanetary Society (JBIS)

**Target Length:** 6,000-8,000 words + equations, tables, figures

---

## I. Research Phase

### A. Literature to Read and Cite (Priority Order)

**Must-cite (directly relevant, forms the conversation the paper joins):**

| Paper | Why it matters | Status |
|---|---|---|
| Crane & Westmoreland 2009 (arXiv:0908.1803) — "Are Black Hole Starships Possible?" | The foundational BH propulsion paper. Our paper extends/replaces their formation mechanism. Must compare directly. | To read |
| Alvarez-Dominguez et al. 2024 (PRL 133, 041401) — "No Black Holes from Light" | Kills gamma-ray kugelblitz formation. Makes our monopole approach the only remaining option. Critical framing device. | To read |
| Page 2025 (arXiv:2505.16202) — "Light Black Holes from Light" | Don Page's rebuttal to Alvarez-Dominguez. Argues idealized photon BHs are possible. Must acknowledge but note it doesn't restore practical kugelblitze. | To read |
| Lee, Nair & Weinberg 1992 (Phys. Rev. D 45, 2751) — "Black Holes in Magnetic Monopoles" | Shows monopoles form BHs at critical VEV. Closest prior work to our formation mechanism. | To read |
| Lue & Weinberg 1999 (Phys. Rev. D 60, 084025) — "Magnetic Monopoles Near the Black Hole Threshold" | Dynamic collapse of monopole to extremal BH. Directly relevant to our collapse section. | To read |
| Maldacena 2020 (arXiv:2004.06084) — "Comments on Magnetic Black Holes" | Magnetically charged BH Hawking enhancement via Landau levels. Must confirm our operating point is Schwarzschild-like. | To read |
| Page 1976 — Particle emission from Schwarzschild BHs | Greybody factors we use for Hawking spectrum calculation. | To read |
| Hawking 1975 — "Particle Creation by Black Holes" | Foundation of Hawking radiation. Required citation. | To read |

**Must-cite (foundational assumptions):**

| Paper | Assumption it supports |
|---|---|
| 't Hooft 1974; Polyakov 1974 — Monopole solutions | Assumption 2 (monopoles exist) |
| Bogomolny 1976; Prasad & Sommerfield 1975 — BPS bound | Assumption 3 (BPS limit) |
| Bodmer 1971; Witten 1984 — Strange quark matter hypothesis | Assumption 4 (SQM stable) |
| Farhi & Jaffe 1984 — "Strange Matter" | Quantitative SQM stability |
| Alford, Rajagopal & Wilczek 1999 — CFL phase | SQM superconducting properties |
| Affleck & Manton 1982 — Monopole pair production | Assumption 5 baseline (breeding suppression) |
| Preskill 1979/1984 — Cosmological monopole production | Monopole mass/charge properties |
| Gibbons & Manton 1986 — BPS monopole dynamics | BPS monopole interactions |

**Should-cite (strengthens the paper):**

| Paper | Purpose |
|---|---|
| Bai, Berger, Korwar & Orlofsky 2020 (arXiv:2007.03703) | Magnetic BH phenomenology, electroweak corona |
| Brihaye et al. 2018 (arXiv:1801.03044) | Dynamical monopole collapse |
| MacGibbon & Webber 1990 | QCD hadronization of Hawking radiation |
| Dong et al. 2016 (arXiv:1712.07664) | Power-rate greybody coefficients |
| Bai & Chen 2025 (arXiv:2502.20241) | Argument against Bodmer-Witten — must address |
| Madsen 1999/2000 | Strangelet properties, charge |
| Shaw et al. 1989 (Nature 337, 436) | SQM growth concept |
| Drukier & Nussinov 1982 | Exponential suppression of soliton production |
| Alford et al. 2008 (Rev. Mod. Phys. 80, 1455) | Color superconductivity review |

### B. Physics to Verify or Derive More Rigorously

These are the calculations that need to be tightened from the source document's engineering estimates to paper-grade derivations:

1. **Hawking spectrum species counting at kT = 2.68 GeV**
   - Reproduce f = 2.85 x 10^-3 from Page's greybody factors species by species
   - Show partial suppression of charm, tau, bottom explicitly with Boltzmann/Fermi-Dirac weighting
   - Confirm the 91% non-neutrino fraction

2. **Meissner confinement equilibrium**
   - Derive the force on a monopole charge inside a superconducting hemisphere from boundary-value magnetostatics (not just the flat-plane image charge)
   - Compute linearized restoring force for axial and lateral displacements
   - Derive oscillation frequency for small perturbations
   - Show the equilibrium is dynamically stable

3. **Oppenheimer-Snyder collapse of the monopole lobes**
   - Verify the free-fall time for the two-lobe geometry
   - Confirm horizon formation before lobe merger for the given masses and separation
   - Address the BPS third-law issue: cite relevant work and show sub-extremal formation avoids it

4. **BH mass optimization**
   - Derive the optimal mass from competing constraints (lifetime > mission duration, thrust sufficient for vehicle mass, temperature compatible with mirror survival)
   - Present as a trade-space plot, not a single design point

5. **Magnetic charge evolution**
   - Confirm Schwinger discharge timescale for electric charge (justify "nanoseconds" quantitatively)
   - Confirm magnetic charge stability (Schwinger monopole pair production rate negligible)
   - Derive charge adjustment schedule over operational life

6. **Reissner-Nordstrom corrections**
   - Confirm that at 0.027% of extremal, the Schwarzschild approximation is valid (<10^-6 correction)
   - Cross-check against Maldacena's Landau-level enhancement — confirm it's negligible at this charge

### C. Open Questions to Investigate

1. Can we bound the monopole breeding cross-section without a full QFT calculation? Even an order-of-magnitude argument based on dimensional analysis or known strong-coupling results would strengthen the paper.

2. What is the minimum monopole inventory for a viable BH? If breeding is 10x less efficient, does the design degrade gracefully to a smaller BH with shorter lifetime but still-useful thrust?

3. The CFL reflectivity claim (R = 1 - 10^-30) — can we derive this more rigorously from the CFL gap and optical conductivity, or should we show the drive works even at much lower reflectivity (e.g., R = 1 - 10^-10)?

4. The BPS third-law constraint — does forming a sub-extremal BH cleanly avoid it? Need to read the relevant papers carefully.

---

## II. Paper Structure

### Abstract (~200 words)
- State the problem: artificial micro BH formation for propulsion
- Note that gamma-ray kugelblitze are now ruled out (Alvarez-Dominguez 2024)
- Propose monopole gravitational collapse as alternative
- State key results: self-consistent system at [mass], [thrust], [Isp], [lifetime]
- Note assumptions required

### 1. Introduction (~1,200 words)
- The interstellar propulsion problem: specific impulse vs. thrust
- Photon rockets as the theoretical maximum (Isp = c/g0)
- Hawking radiation as a photon rocket source (Crane & Westmoreland 2009)
- The formation problem: gamma-ray kugelblitze ruled out (Alvarez-Dominguez 2024)
- This paper: monopole-based formation as the remaining viable mechanism
- Statement of five foundational assumptions (brief, honest)

### 2. Black Hole Mass Selection (~1,200 words)
- Competing constraints define a mass window
- Lifetime constraint: tau > mission duration
- Thrust constraint: F > minimum for vehicle mass class
- Temperature constraint: kT determines spectrum composition and mirror requirements
- Derive the optimal mass range; show 3.94 x 10^9 kg sits within it
- Figure: trade-space plot (mass vs. lifetime, thrust, temperature)

### 3. Formation via Monopole Collapse (~1,800 words)
- BPS monopole properties and the exact force cancellation
- Monopole inventory requirements
- Two-lobe dumbbell geometry and Oppenheimer-Snyder collapse
- Horizon formation before merger (derive timescales)
- Seed BH properties at formation
- Mass growth via pellet injection (brief — the key point is that the seed can be fed)
- Table: formation parameters

### 4. Magnetic Confinement (~1,500 words)
- Why magnetic charge, not electric (Schwinger discharge calculation)
- Meissner repulsion from superconducting secondary
- Equilibrium derivation
- Axial and lateral stability analysis
- Charge evolution over operational life
- Figure: confinement geometry diagram
- Figure: Meissner force vs. distance with equilibrium point

### 5. Performance (~1,000 words)
- Hawking spectrum at kT = 2.68 GeV (species counting, greybody factors)
- Non-neutrino fraction and effective beam power
- Thrust and specific impulse
- Comparison to Crane & Westmoreland's design
- Comparison to theoretical photon rocket limit
- Table: performance comparison

### 6. Discussion (~800 words)
- Assumption sensitivity: what breaks if each assumption fails
- Comparison to alternative formation mechanisms
- Implications for the BH starship concept
- Limitations of this analysis

### 7. Conclusion (~400 words)
- Summary of results
- The monopole formation mechanism as the key contribution
- Future work needed (breeding cross-section calculation, CFL reflectivity, etc.)

### References (~40-50 citations)

---

## III. Figures Needed

1. **Trade-space plot** — BH mass vs. lifetime, thrust, and Hawking temperature. Three y-axes or three subplot panels. Shows the design window.

2. **Confinement geometry** — Cross-section diagram showing primary mirror (paraboloid), BH at focus, secondary mirror (hemisphere), SQM pylons, exhaust beam, magnetic field lines. Clean engineering diagram.

3. **Meissner force curve** — Force vs. BH-secondary distance, with equilibrium point marked where F_Meissner = M_BH x a_ship.

4. **Hawking spectrum composition** — Bar chart or stacked chart showing power fraction by species at kT = 2.68 GeV. Visually shows the 91% capturable / 9% neutrino split.

5. **Formation timeline** — Schematic showing the five phases from monopole production through operational BH.

---

## IV. Mentor / Co-Author Strategy

- Identify 3-5 professors at nearby universities working in:
  - Advanced propulsion concepts (aerospace departments)
  - GR / black hole physics (physics departments)
  - Particle theory / monopoles (physics departments)
- Draft a cold-email template explaining the project and asking for review/mentorship
- JBIS membership may also connect to BIS members who mentor

---

## V. Timeline

| Phase | Duration | Deliverable |
|---|---|---|
| Literature reading | 3-4 weeks | Annotated bibliography, notes on each key paper |
| Physics derivations | 4-6 weeks | Verified calculations for Sections 2-5 |
| First draft | 3-4 weeks | Complete manuscript in LaTeX |
| Mentor review | 2-3 weeks | Feedback and revisions |
| Figures | 1-2 weeks (parallel with draft) | Publication-quality plots and diagrams |
| Final draft | 2 weeks | Revised manuscript incorporating feedback |
| Submission | 1 week | Format to JBIS specifications, submit |
| Review cycle | 2-4 months | Respond to referee comments |
| **Total: first draft** | **~3-4 months** | |
| **Total: published** | **~6-10 months** | |

---

## VI. Tools and Setup

- **Writing:** LaTeX (REVTeX or JBIS template if available)
- **Plots:** Python (matplotlib) or Mathematica
- **Diagrams:** TikZ, Inkscape, or similar
- **Reference management:** BibTeX
- **Version control:** This repo

---

## VII. Risk Registry

| Risk | Impact | Mitigation |
|---|---|---|
| Monopole breeding mechanism found to be previously proposed | Reduces novelty | Literature search (done — appears novel) |
| BPS third-law blocks sub-extremal formation | Kills Section 3 | Read Lee-Nair-Weinberg and Lue-Weinberg carefully; may need to show non-BPS formation works too |
| Bodmer-Witten conclusively excluded before publication | Weakens Assumption 4 | Paper already treats SQM as assumption; note Bai & Chen 2025 and frame as conditional |
| JBIS rejects | Delays publication | Resubmit to Acta Astronautica or post to arXiv |
| No mentor found | Paper taken less seriously | Submit anyway; JBIS accepts independent submissions |
| Referee demands full breeding cross-section calculation | Major additional work | Scope paper to not depend on specific breeding rate; show design works for a range |
