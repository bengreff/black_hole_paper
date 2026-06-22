# Paper Drafting Plan — Draft by Draft

**Working Title:** Solving the Three Open Problems of Black Hole Propulsion: Formation, Energy Capture, and Confinement

**Target:** JBIS (Journal of the British Interplanetary Society), 8,000–10,000 words + equations, tables, figures

**Starting material:** `DESIGN_SUMMARY.md` (~30,000 words, 12 calculation scripts, 39-entry bibliography)

**Core challenge:** Compress 30k words of internal design documentation into a 9k-word paper with a clear narrative, without losing the quantitative rigor that makes it publishable.

---

## The paper's argument in one paragraph

Crane & Westmoreland (2009) proposed using Hawking radiation from a micro black hole as an interstellar propulsion source. Three problems have stalled the concept for 15 years: (1) formation — gamma-ray kugelblitzes are impossible (Alvarez-Dominguez et al. 2024); (2) energy capture — no known material reflects GeV radiation, limiting performance to 0.0001c (Lee 2015); (3) confinement — no mechanism exists to hold the BH at the system's focal point. We solve all three under six stated physics assumptions (Hawking radiation, GUT monopoles, BPS limit, Bodmer-Witten, CFL stability, core-overlap breeding). The key innovation is a CFL strange-quark-matter spherical shell that *absorbs* the full Hawking spectrum and *re-emits* it as magnetically-directable keV electron-positron pairs — converting an omnidirectional GeV source into a collimated beam at β = 0.33. Performance: 55 MN thrust, I_sp = 10⁷ s, α Centauri in 79 yr.

---

## What changed since the old PLAN.md

The design evolved substantially. The old plan's solutions no longer match:

| Problem | Old plan | Current design |
|---|---|---|
| Formation | BPS monopole gravitational collapse | BPS monopole gravitational collapse (§7) — restored and strengthened |
| Energy capture | Parabolic SQM mirror (reflection) | Spherical SQM shell (absorption + re-emission via Usov electrosphere) (§4) |
| Confinement | Meissner repulsion from SQM secondary | Anti-Helmholtz magnetic bottle + active feedback control (§5) |
| Shell geometry | Parabolic primary + hemispherical secondary | Single 2m-radius spherical shell, 3 pm thick |
| Monopole type | GUT 't Hooft-Polyakov only | GUT 't Hooft-Polyakov (BPS limit, N=2 SUSY protected) |
| Seed production | Electron linac (source document) | SQM electron linac at 10× threshold (§7.5.1), with over-barrier argument vs D-N |

---

## Paper structure (current design)

Target word counts are guideposts, not hard caps.

### Abstract (~200 words)
Three problems, six assumptions, three solutions, headline numbers.

### 1. Introduction (~1,400 words)
- The interstellar propulsion problem: I_sp vs. thrust
- Hawking radiation as a propulsion source (Crane & Westmoreland 2009)
- **The three open problems:**
  - Formation: kugelblitze impossible (Alvarez-Dominguez 2024; Page 2025 rebuttal acknowledged)
  - Energy capture: no material reflects GeV radiation; titanium absorption yields 0.0001c (Lee 2015)
  - Confinement: no proposed mechanism (Crane & Westmoreland hand-waved "particle beams")
- This paper: we solve all three. State the six assumptions up front.
- Assumption table (from §0): Hawking radiation, GUT monopoles, BPS limit, Bodmer-Witten, CFL stability, core-overlap breeding. Each one a Nobel-scale discovery if confirmed.
- Address Bai & Chen 2025 in a paragraph (their argument doesn't constrain CFL specifically).

### 2. Black hole parameters and Hawking spectrum (~1,200 words)
- Mass selection: 10⁹ kg, kT = 10.57 GeV, P = 60,200 TW
- Emission factor f = 3.503 × 10⁻³ from proper thermal-integral power-rate suppression (not exp(−m/kT))
- Species-by-species table (from §2)
- Sub-extremality check (g/g_ext = 1.5 × 10⁻¹⁰; Schwarzschild formulas apply)
- Maldacena corona threshold check (m_W r_s = 0.605; no enhancement)
- Particle census after hadronization and pair conversion (§3)
- Loss budget: 7% primary ν, ~10% secondary ν, 83% captured → 50,000 TW
- **Table 1:** BH parameter summary
- **Table 2:** Species breakdown and capture fractions

### 3. The SQM shell — thermal wavelength converter (~2,200 words)
*This is the primary novel contribution. It gets the most space.*

- **3.1 Architecture.** Spherical CFL shell, R = 2 m, t = 3 pm = 3000 fm, ρ = 4 × 10¹⁷ kg/m³, M_shell = 60,000 t. Inner surface: bombardment-maintained electrosphere. Outer surface: cold ground-state electrosphere.
- **3.2 Absorption.** Bethe-Bloch at nuclear density → 80 MeV/fm → stopping budget 240 GeV at 3 pm thickness. All charged particles stopped. Muon punch-through analysis: Wien-tail escape ε = 1.5 × 10⁻⁸ → 84 MW residual (undetectable at 100 ly). Shell thickness trades off mass vs. punch-through margin; present the table from §3.
- **3.3 Pair re-emission.** Usov (1998) electrosphere pair emission. Self-consistent equilibrium: T_eq = 0.356 GK, kT = 30.7 keV, β = 0.332. J(ζ) function verified from Usov's paper. Robustness: β stable to ±3% over 100× variation in J.
- **3.4 The three-layer firewall.** Why the outer surface doesn't glow:
  - (a) CFL gap suppression: exp(−2Δ/kT) = 10⁻²⁸²⁸ (quark quasiparticles)
  - (b) Boltzmann suppression: exp(−m_π^CFL/kT) = 10⁻⁷¹ (massive Goldstones)
  - (c) H-Goldstone anomaly emission: α⁴ T⁹/F_π⁴ → 34 kW bulk, Wien-tail past ω_p = 0.5 MeV → **0.17 W leakage**
  - Total off-axis EM < 1 MW. Comparison to blackbody upper bound.
- **Why this is the key contribution.** Lee (2015) showed conventional materials fail. The SQM shell sidesteps the reflection problem entirely — it absorbs and re-emits rather than reflecting. Manuel & Rajagopal (2002) showed CFL is a transparent insulator, killing the superconducting-reflector concept. The thermal-converter architecture is the physically consistent alternative.
- **Figure 1:** System architecture cross-section (shell, BH, coils, bore, nozzle)

### 4. Confinement, capture, and exhaust (~1,500 words)
- **4.1 Anti-Helmholtz geometry.** Two opposed coils, R_c = d = 2 m, I = 1.36 × 10⁹ A, dB/dz = 227 T/m. Field zero at center; restoring force on monopole charge.
- **4.2 BH equilibrium.** F_mag = g·dB/dz·δ sets g = 1.18 × 10⁶ A·m for δ_eq = 100 mm. Passive axial stability. Lateral Earnshaw instability with τ_lat = 2.8 s. Active PD controller: K_P = 2.6 × 10⁸ N/m, bandwidth > 1 Hz, position readout 30 pm precision.
- **4.3 Magnetic bottle pair capture.** r_L = 2.6 μm at 227 T; pairs deeply magnetized. Loss cone: f_cap = 12.1% per cycle at equator. Multi-bounce dynamics: ~6 bounces to find loss cone, ~120 ns extraction time. Synchrotron loss negligible (τ_sync/τ_extract ~ 10⁴).
- **4.4 Exhaust nozzle.** 820 m exponential taper, B_throat = 1000 T → B_exit = 30 μT. Adiabatic invariance → θ_exit = 0.01°.
- **Figure 2:** Anti-Helmholtz field map with loss cone geometry

### 5. Formation and monopole production (~1,500 words)
- **5.1 BPS monopole gravitational collapse.** Same-sign cloud of 7.18 × 10¹⁴ GUT monopoles (226 t) collapses as pressureless dust (Oppenheimer-Snyder). Seed BH: 226 t, kT = 47 TeV, τ = 5.3 ms.
- **5.2 Monopole breeding (Phase 2).** Core-overlap exponential breeding from 't Hooft/Drukier-Nussinov/Olive-Witten duality. α_m = 1/(4α) is non-perturbative but O(1) per overlap. 1.5× per generation, 86 generations from a single pair to 7 × 10¹⁴ monopoles.
- **5.3 Seed production (Phase 1): SQM electron linac.** Two 2,500 km SQM-bore tubes, e⁻e⁻ at 10× pair-production threshold. D-N suppression vs over-barrier argument (sphaleron analogy). Working estimate 10⁻⁷ per collision; ~10 s to first pair.
- **5.4 Bootstrap ODE** (seed 226 t → 10⁹ kg). dM/dt = A·P(M)/c², t_bootstrap ≈ 2 yr. Sensitivity table.
- **Figure 3:** Bootstrap ODE integration (use existing `figures/bootstrap_ode.png`)
- **Table 3:** Seed-production options comparison (AO primary, primordial-flux fallback)

### 6. Performance and mission profiles (~800 words)
- Thrust F = β·P_captured/c = 55.3 MN. Efficiency η = F·c/P_H = 27.5%. I_sp = 1.01 × 10⁷ s.
- Off-axis emission budget: < 1 MW EM, 84 MW CR (muon tail). Detectability at 100 ly: undetectable.
- α Cen (4.37 ly): 79 yr, peak 0.111c, continuous refueling required.
- Burn-the-BH Δv: 0.23c (unfed), limited by shell stopping budget to practical 0.13c.
- Scaling: M = 4 × 10⁹ kg long-range variant (1,020 yr lifetime, 3.7 MN thrust).
- **Table 4:** Performance summary, comparison to Crane & Westmoreland (2009) and Lee (2015)

### 7. Discussion (~800 words)
- **Assumption sensitivity.** Table: what breaks if each assumption fails.
- **The SQM shell as the enabling physics.** Without it, Lee (2015) showed BH drives achieve 0.0001c. With it, 0.11c+. The shell is the load-bearing contribution.
- **Engineering vs. physics gaps.** All physics-side items in §9 are resolved or bounded. The remaining gaps are: bore-throat materials (400 GPa), 1000 T sustained coils, SQM linac fabrication (2,500 km SQM tubes), monopole breeding rings, SQM shell fabrication. All are engineering, not physics — except the D-N seed-production suppression, which is genuinely uncertain.
- **Limitations.** kT-scaling drives choice of M; secondary-ν budget has ~30% uncertainty; the Usov extrapolation to T < 10⁹ K introduces ~5% uncertainty in β; the Phase-1 seed AO accelerator is a planetary megastructure.
- **Relation to Bai & Chen 2025.** Their result constrains unpaired SQM, not CFL. Stated explicitly.
- **Future work.** Full BlackHawk-PYTHIA integration for sub-1% ν budget. Lattice QCD constraints on CFL gap at operating μ. Experimental monopole searches at MoEDAL / FCC-hh.

### 8. Conclusion (~400 words)
Three problems, three solutions, six assumptions, headline numbers. The concept is now self-consistent. The remaining question is whether the assumptions hold — each would be a Nobel-scale discovery.

### References (~40–50 citations)
Curate from the current 63-entry `references.bib`. Cut any that aren't cited in the paper text.

**Total: ~10,050 words.** Slightly over the 10k target — some compression needed, especially in §3 and §5.

---

## Figures needed

| # | Description | Source | Status |
|---|---|---|---|
| 1 | System architecture cross-section: shell, BH, coils, bore, nozzle, field lines | New (TikZ or Inkscape) | To create |
| 2 | Anti-Helmholtz field map + loss cone geometry | New (matplotlib from `bh_stability_control.py` or new script) | To create |
| 3 | Bootstrap ODE integration: M(t) and P(t) curves | `figures/bootstrap_ode.png` (exists) | Review for publication quality |
| 4 | Hawking spectrum species breakdown (stacked bar or pie) | New (matplotlib from `hawking_spectrum.py`) | To create |
| 5 | Mission profile: velocity vs. time for α Cen flyby | New (matplotlib) | To create |
| 6 | Muon punch-through vs. shell thickness (log-scale; the §3 table as a plot) | New (matplotlib) | To create |

---

## Draft-by-draft plan

### Draft 0 — Skeleton (1–2 days)

**Goal:** One paragraph per section, plus all tables and figure captions. No prose.

**What it looks like:** The section headers above, with each populated by:
- A topic sentence stating the section's argument
- A bullet list of the 3–5 claims made in the section
- Placeholder figure/table captions with exact data to be included
- The 2–3 key equations that appear in the section

**Why this draft exists:** To force a decision on *what goes where* before writing prose. The hardest part of compressing 30k → 9k is deciding what to cut. The skeleton is where you make those decisions.

**Deliverable:** `drafts/draft_0_skeleton.md`

**Gate to proceed:** You read the skeleton and agree the section-by-section flow makes sense narratively. Does the argument build? Does each section earn the next? Is anything missing?

### Draft 1 — Content dump (5–7 days)

**Goal:** Full prose, pulled from `DESIGN_SUMMARY.md`, targeted at ~12,000 words. Deliberately too long.

**What it looks like:** Real sentences, real equations, real numbers. Every claim has a citation or a derivation. But it's overlong, it reads like a technical report not a paper, and the voice is still internal ("we adopt," "the earlier draft quoted").

**Method:**
- For each section of the skeleton, find the corresponding §-numbered passage in `DESIGN_SUMMARY.md`
- Rewrite it in paper voice (third-person where appropriate, present tense for established results, future/conditional for speculative elements)
- Include all intermediate algebra that a reviewer might want to check
- Include all the numerical checks (these will be trimmed later but must exist first)
- Flag every spot where the prose says "see calculations/<file>.py" — these become either inline derivations, footnotes, or supplementary-material references

**Deliverable:** `drafts/draft_1_full.tex` (start in LaTeX now — JBIS uses numbered references, not author-year)

**Gate to proceed:** Every numerical claim in the draft can be traced to a `calculations/*.py` script or a cited paper. No gaps, no hand-waves, no "TBD."

### Draft 2 — Compression pass (3–5 days)

**Goal:** Cut from ~12k to ~9.5k words. Move derivations to supplementary material or footnotes.

**What gets cut:**
- Intermediate algebra for results that appear in a cited paper (keep only the result + citation)
- Numerical spot-checks that a reviewer can reproduce from the stated formula (these go into supplementary)
- Historical context that isn't load-bearing ("the earlier draft quoted…", "this was not in the previous version…")
- Sensitivity analyses for secondary parameters (move to supplementary; keep only the headline sensitivity)
- The BPS-collapse alternative formation route (mention in one sentence as an alternative; don't derive)
- The §10 scaling discussion (condense to one paragraph in §6)

**What must survive compression:**
- Every assumption in §0 must be stated and defended (or acknowledged as open)
- The Usov J(ζ) self-consistent solution must be derived (this is novel — reviewers will check it)
- The three-layer firewall must be quantitatively bounded (this is the main physics contribution)
- The loss-cone / magnetic-bottle analysis must be derived (no prior work does this for a Hawking-radiation system)
- The AO accelerator specification must be stated concretely (this is the committed seed path)

**Deliverable:** `drafts/draft_2_compressed.tex`

**Gate to proceed:** Word count ≤ 10,000. Every section ≤ its target word count ± 15%.

### Draft 3 — Narrative and voice pass (3–4 days)

**Goal:** Make it read like a *paper*, not a design document. Establish a consistent authorial voice. Write the abstract, introduction, and conclusion.

**Specific tasks:**
- Write the abstract (last, after everything else is stable)
- Rewrite the introduction to set up the "three open problems" as a narrative, not a list
- Ensure each section's opening sentence connects to the previous section's conclusion
- Replace all design-doc idioms ("we adopt," "the design choice is") with paper idioms ("we find," "the analysis yields," "this constrains")
- Add forward references ("as we show in §4, the firewall bounds…") to build narrative momentum
- Ensure the Discussion fairly presents limitations and does not oversell
- Write the Conclusion to land the "six assumptions, three solutions, one self-consistent system" message

**Deliverable:** `drafts/draft_3_narrative.tex`

**Gate to proceed:** Read the abstract alone. Does it convey the paper's contribution in 200 words? Read only the first sentence of each section. Does the paper's argument flow?

### Draft 4 — Figures and tables (3–5 days, can overlap with Draft 3)

**Goal:** Publication-quality figures. All tables finalized.

**Tasks:**
- Create Figures 1–6 (see figure list above)
- Use consistent style: black/white safe for print, legible at column width (~85 mm for JBIS)
- Write full captions (a figure caption should be self-contained — a reader scanning figures should get the paper's argument)
- Finalize all tables with consistent significant figures and units
- Cross-check every number in every table against `calculations/verify_design.py`

**Deliverable:** `figures/` directory with publication-quality PNG/PDF files; tables inline in the LaTeX

**Gate to proceed:** Print the figures at column width on paper. Are axes labels readable? Do captions tell a story?

### Draft 5 — Review-ready manuscript (2–3 days)

**Goal:** A complete manuscript suitable for sending to a physics mentor or potential co-author.

**Tasks:**
- Final consistency pass: every number in the text matches the tables matches the figures matches `verify_design.py`
- Reference audit: every \cite has a corresponding \bibitem; every referenced paper is real and says what we claim it says
- Notation audit: consistent use of g (magnetic charge), B (field), f (emission factor), β (exhaust velocity), etc.
- Format to JBIS style (check their author guidelines for font, margin, reference format)
- Write a cover letter for the mentor/co-author explaining the paper's context

**Deliverable:** `drafts/draft_5_review_ready.tex` + compiled PDF

**Gate to proceed:** You have sent it to at least one physicist for feedback.

### Draft 6 — Post-review revision (timeline depends on reviewer)

**Goal:** Incorporate feedback from mentor/co-author and/or JBIS referees.

**Likely feedback patterns to anticipate:**
- "Your Usov extrapolation is not justified below 10⁹ K" → cite the ±3% robustness check; add a footnote acknowledging the extrapolation
- "Core-overlap breeding rate is speculative" → acknowledge; present as O(1) estimate, not a precision calculation; note that the drive design depends on the *count* of monopoles not the breeding *rate*
- "You haven't addressed [specific paper]" → read it, cite it, incorporate or rebut
- "The assumption stack is too large" → this is the honest response: agree, restate that the paper is a conditional feasibility analysis, not an engineering roadmap
- "What about the Planck-scale endpoint?" → already addressed in §8 of DESIGN_SUMMARY; include the one-paragraph caveat
- "Where is the PYTHIA/BlackHawk cross-check?" → acknowledge as future work; cite Arbey & Auffinger 2019; note our first-principles estimate is consistent with their code's outputs

**Deliverable:** `drafts/draft_6_revised.tex`

**Gate to proceed:** Both you and your reviewer are satisfied. Submit.

---

## Supplementary material strategy

JBIS allows supplementary material hosted separately. Use this for:
- Full species-by-species f derivation with intermediate integrals
- All `calculations/*.py` scripts (or links to a public repository)
- Extended sensitivity tables (f_cap, shell thickness, ν budget)
- The full BPS-collapse alternative derivation
- Detailed bootstrap ODE integration with threshold-opening f(M)
- Extended firewall derivation (all three channels separately, with prefactor uncertainties)

This lets the paper be tight (~9k words) while giving reviewers the full derivation chain on request.

---

## Co-author and review strategy

You are not a physicist. This is not disqualifying — JBIS publishes work from non-academic authors. But a physics co-author or reviewer substantially increases the paper's credibility and catches errors that neither you nor an LLM would catch.

**Priority targets:**
1. Someone who works on strange quark matter or color superconductivity (the shell physics is the hardest to get right)
2. Someone who works on Hawking radiation / BH thermodynamics (validates the spectrum calculation)
3. Someone in advanced propulsion at an aerospace department (validates the framing and knows JBIS culture)

**Approach:** Draft 5 is the artifact you send. The cover letter should be honest: "I developed this design with substantial AI assistance for the calculations. I am looking for a physicist to review the manuscript for correctness and potentially co-author. The novel contributions are [the SQM thermal-converter shell, the anti-Helmholtz confinement analysis, the Cho-Maison/AO seed-production path]."

**If no co-author is found:** Submit anyway. JBIS has no affiliation requirement. The work stands on its published references and reproducible calculations. Be transparent about the AI-assisted methodology in the acknowledgments.

---

## Timeline

| Phase | Calendar time | Deliverable |
|---|---|---|
| Draft 0 (skeleton) | 2 days | Section-by-section outline with claims, equations, figure captions |
| Draft 1 (content dump) | 1 week | Full ~12k word manuscript in LaTeX |
| Draft 2 (compression) | 1 week | ≤ 10k words; supplementary material split off |
| Draft 3 (narrative + voice) | 1 week | Reads like a paper; abstract and conclusion written |
| Draft 4 (figures + tables) | 1 week (overlaps Draft 3) | 6 publication-quality figures |
| Draft 5 (review-ready) | 3 days | Complete formatted manuscript |
| External review | 2–8 weeks | Feedback from physicist |
| Draft 6 (revision) | 1–2 weeks | Incorporate feedback |
| Submission | 1 day | To JBIS |
| **Total to submission** | **~2–3 months** | |
| Review cycle | 2–4 months | Referee responses |
| **Total to publication** | **~5–8 months** | |

---

## Risk registry (updated)

| Risk | Impact | Mitigation |
|---|---|---|
| Bai & Chen 2025 persuades referees that Bodmer-Witten is dead | Undermines §0 assumption #4 | Already addressed: BC25 constrains unpaired SQM, not CFL. State this explicitly in §1. |
| Usov extrapolation below 10⁹ K challenged | Weakens §3 (pair emission rate) | The 100× robustness check shows β is stable to ±3%. Present the range, not a point estimate. |
| No physicist agrees to review | Paper may contain physics errors | Submit to arXiv first; community feedback is fast and public. Include all calculation scripts for reproducibility. |
| Referee demands PYTHIA/BlackHawk cross-check | Delays revision by weeks | Can actually run BlackHawk (it's open-source Python); include in revision if demanded. |
| JBIS rejects | Delays publication | Resubmit to Acta Astronautica, or post to arXiv as a standalone preprint. |
| Core-overlap breeding rate deemed too speculative | Weakens §5 (formation) | Paper's primary contribution is the shell, not formation. Scope formation as "conditional on breeding working at O(1) rate per overlap." |
| BPS limit λ = 0 seen as fine-tuning | Undermines formation mechanism | Argue N=2 SUSY non-renormalization protection; not fine-tuning but symmetry. Cite Gibbons & Manton 1986. |
| D-N seed-production suppression holds at all energies | No seed pair → no breeding → no BH | Present the over-barrier argument (sphaleron analogy) honestly. Acknowledge this is the most uncertain step. Fallback: primordial-flux capture (slow but physically sound). |
| The 1000 T / 400 GPa materials requirement seen as disqualifying | Dismissal as "science fiction" | Already framed as thought experiment in §0. Emphasize that the physics closes, even if the engineering doesn't — that's the paper's contribution. |
