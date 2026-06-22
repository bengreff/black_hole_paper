#!/usr/bin/env python3
"""
Create JBIS Word doc with inline tables, then convert to PDF.
Tables placed at first-reference positions. No end-matter TABLES/FIGURE CAPTIONS.
Equations in 3-column invisible tables with OMML.
"""

from docx import Document
from docx.shared import Pt, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from lxml import etree
from xml.sax.saxutils import escape as xesc
import re, os, sys

os.chdir('/Users/ben/black_hole_paper')

# ── Unicode superscript/subscript maps ──
SUPER_MAP = {
    '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4',
    '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9',
    '⁻': '−', '⁺': '+', 'ᐟ': '/',
}
SUPER_CHARS = set(SUPER_MAP.keys())

SUB_MAP = {
    '₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4',
    '₅': '5', '₆': '6', '₇': '7', '₈': '8', '₉': '9',
}
SUB_CHARS = set(SUB_MAP.keys())


def add_formatted_text(paragraph, text, font_size=Pt(12), font_name='Times New Roman',
                       bold=False, italic=False):
    """Add text to a paragraph with proper subscript/superscript/em-dash formatting.

    Handles:
    - X_{multi} → X with subscript 'multi'
    - X_Y (single char) → X with subscript Y
    - Unicode superscripts (⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺) → Word superscript
    - ^{text} → Word superscript
    - -- → em dash
    - e⁺e⁻ → proper superscripts
    """
    # First convert -- to em dash
    text = re.sub(r'(?<!\-)--(?!\-)', '—', text)

    # Tokenize the text into segments with formatting info
    # Each segment: (text, is_super, is_sub)
    segments = []
    i = 0
    while i < len(text):
        # Check for ^{...} superscript
        if text[i] == '^' and i + 1 < len(text) and text[i+1] == '{':
            end = text.find('}', i + 2)
            if end != -1:
                segments.append((text[i+2:end], 'super'))
                i = end + 1
                continue

        # Check for _{...} subscript
        if text[i] == '_' and i + 1 < len(text) and text[i+1] == '{':
            end = text.find('}', i + 2)
            if end != -1:
                segments.append((text[i+2:end], 'sub'))
                i = end + 1
                continue

        # Check for _XYZ multi-char subscript (only after a letter/digit/Greek)
        if (text[i] == '_' and i + 1 < len(text)
            and i > 0 and (text[i-1].isalnum() or text[i-1] in 'αβγδεζηθικλμνξπρστυφχψωΔΣΩℏ')
            and (text[i+1].isalnum() or text[i+1] in 'αβγδεζηθικλμνξπρστυφχψωΔΣΩℏ')):
            j = i + 1
            while j < len(text) and (text[j].isalnum() or text[j] in 'αβγδεζηθικλμνξπρστυφχψωΔΣΩℏ'):
                j += 1
            segments.append((text[i+1:j], 'sub'))
            i = j
            continue

        # Check for Unicode superscript sequence
        if text[i] in SUPER_CHARS:
            sup_text = []
            while i < len(text) and text[i] in SUPER_CHARS:
                sup_text.append(SUPER_MAP[text[i]])
                i += 1
            segments.append((''.join(sup_text), 'super'))
            continue

        # Check for Unicode subscript sequence
        if text[i] in SUB_CHARS:
            sub_text = []
            while i < len(text) and text[i] in SUB_CHARS:
                sub_text.append(SUB_MAP[text[i]])
                i += 1
            segments.append((''.join(sub_text), 'sub'))
            continue

        # Regular character — accumulate plain text
        plain = []
        while i < len(text):
            if text[i] in SUPER_CHARS or text[i] in SUB_CHARS:
                break
            if text[i] == '^' and i + 1 < len(text) and text[i+1] == '{':
                break
            if text[i] == '_' and i + 1 < len(text) and text[i+1] == '{':
                break
            if (text[i] == '_' and i + 1 < len(text)
                and len(plain) > 0 and (plain[-1].isalnum() or plain[-1] in 'αβγδεζηθικλμνξπρστυφχψωΔΣΩℏ')
                and (text[i+1].isalnum() or text[i+1] in 'αβγδεζηθικλμνξπρστυφχψωΔΣΩℏ')):
                break
            plain.append(text[i])
            i += 1
        if plain:
            segments.append((''.join(plain), 'normal'))

    # Create runs
    for seg_text, seg_type in segments:
        run = paragraph.add_run(seg_text)
        run.font.name = font_name
        run.font.size = font_size
        run.font.bold = bold
        run.font.italic = italic
        if seg_type == 'super':
            run.font.superscript = True
        elif seg_type == 'sub':
            run.font.subscript = True


M_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

# ── OMML helpers ──
def t(s):
    return f'<m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t xml:space="preserve">{xesc(s)}</m:t></m:r>'
def it(s):
    return f'<m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t xml:space="preserve">{xesc(s)}</m:t></m:r>'
def fr(n, d):
    return f'<m:f><m:fPr><m:type m:val="bar"/></m:fPr><m:num>{n}</m:num><m:den>{d}</m:den></m:f>'
def sp(b, e):
    return f'<m:sSup><m:e>{b}</m:e><m:sup>{e}</m:sup></m:sSup>'
def sb(b, s):
    return f'<m:sSub><m:e>{b}</m:e><m:sub>{s}</m:sub></m:sSub>'
def sbsp(b, s, e):
    return f'<m:sSubSup><m:e>{b}</m:e><m:sub>{s}</m:sub><m:sup>{e}</m:sup></m:sSubSup>'
def par(*c):
    return f'<m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e>{"".join(c)}</m:e></m:d>'
def brk(*c):
    return f'<m:d><m:dPr><m:begChr m:val="["/><m:endChr m:val="]"/></m:dPr><m:e>{"".join(c)}</m:e></m:d>'
def sq(c):
    return f'<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr><m:deg/><m:e>{c}</m:e></m:rad>'

def make_omath(content):
    xml = f'<m:oMathPara xmlns:m="{M_NS}" xmlns:w="{W_NS}"><m:oMath>{content}</m:oMath></m:oMathPara>'
    return etree.fromstring(xml.encode())

# ── Equation definitions ──
EQ = {}
EQ[1] = it('kT') + t(' = ') + fr(t('ℏ')+sp(it('c'),t('3')), t('8π')+it('GM')) + t(' = 10.57 GeV')
EQ[2] = sb(it('r'),t('s')) + t(' = ') + fr(t('2')+it('GM'), sp(it('c'),t('2'))) + t(' = 1.485 × ')+sp(t('10'),t('−18'))+t(' m')
EQ[3] = it('P') + t(' = ') + fr(t('ℏ')+sp(it('c'),t('6'))+it('f'), sp(it('G'),t('2'))+sp(it('M'),t('2'))) + t(' = 60,200 TW')
EQ[4] = it('τ') + t(' = ') + fr(sp(it('G'),t('2'))+sp(it('M'),t('3')), t('3ℏ')+sp(it('c'),t('4'))+it('f')) + t(' = 15.8 yr')
EQ[5] = it('f') + t(' = ') + sb(t('Σ'),it('i'))+t(' ')+sb(it('g'),it('i'))+t(' ')+sb(it('α'),sb(it('s'),it('i')))+t(' ')+it('S')+par(sb(it('m'),it('i'))+t('/')+it('kT'))
EQ[6] = sb(it('E'),t('c')) + t(' = 80 MeV/fm × 3000 fm = 240 GeV')
EQ[7] = it('ε')+par(sb(it('x'),t('c')))+t(' = ')+fr(sp(it('e'),t('−')+sb(it('x'),t('c')))+par(sbsp(it('x'),t('c'),t('2'))+t(' + 4')+sb(it('x'),t('c'))+t(' + 6')), t('7')+sp(it('π'),t('4'))+t('/120'))
EQ[8] = sb(it('f'),t('±'))+t(' = ')+sp(t('10'),t('39.2'))+t(' ')+sp(sb(it('T'),t('9')),t('3'))+t(' exp')+par(t('−11.9/')+sb(it('T'),t('9')))+t(' ')+it('J')+par(it('ζ'))
EQ[9] = sb(it('L'),t('pair'))+t(' = ')+fr(sb(it('P'),t('abs')),it('A')+t(' · ')+sb(it('f'),t('cap')))+t(' = 8.21 × ')+sp(t('10'),t('15'))+t(' W/')+sp(t('m'),t('2'))
EQ[10] = sb(it('T'),t('eq'))+t(' = 0.356 GK,  ')+it('kT')+t(' = 30.7 keV,  ')+it('γ')+t(' = 1.060,  ')+it('β')+t(' = 0.332')
EQ[11] = it('P')+t('/')+it('V')+t(' ≈ ')+fr(sp(it('α'),t('4'))+sp(it('T'),t('9')), sp(it('π'),t('4'))+sp(sb(it('F'),it('π')),t('4')))
EQ[12] = sb(it('ω'),t('p'))+t(' = ')+sq(fr(t('4')+it('α'),t('3')+it('π')))+t(' ')+sb(it('μ'),t('e'))+t(' = 0.50 MeV')
EQ[13] = sb(it('B'),t('z'))+par(it('z'))+t(' = ')+fr(sb(it('μ'),t('0'))+it('I')+sbsp(it('R'),t('c'),t('2')),t('2'))+t(' ')+brk(fr(t('1'),sp(par(sbsp(it('R'),t('c'),t('2'))+t('+')+sp(par(it('d')+t('−')+it('z')),t('2'))),t('3/2')))+t(' − ')+fr(t('1'),sp(par(sbsp(it('R'),t('c'),t('2'))+t('+')+sp(par(it('d')+t('+')+it('z')),t('2'))),t('3/2'))))
EQ[14] = fr(t('d')+sb(it('B'),t('z')),t('d')+it('z'))+t(' = ')+fr(t('3')+sb(it('μ'),t('0'))+it('I')+sbsp(it('R'),t('c'),t('2'))+it('d'),sp(par(sbsp(it('R'),t('c'),t('2'))+t('+')+sp(it('d'),t('2'))),t('5/2')))+t(' = 227 T/m')
EQ[15] = it('g')+t(' · ')+fr(t('d')+it('B'),t('d')+it('z'))+t(' · ')+sb(it('δ'),t('eq'))+t(' = ')+sb(it('F'),t('thrust'))+t(' · ')+fr(sb(it('M'),t('BH')),sb(it('M'),t('ship')))
EQ[16] = it('g')+t(' = 1.182 × ')+sp(t('10'),t('6'))+t(' A·m')
EQ[17] = sb(it('τ'),t('lat'))+t(' = ')+sq(fr(sb(it('M'),t('BH')),t('|')+sb(it('k'),t('r'))+t('|')))+t(' ≈ 2.8 s')
EQ[18] = sb(it('r'),t('L'))+t(' = ')+fr(it('γβ')+sb(it('m'),t('e'))+it('c'),it('eB'))+t(' = 2.65 μm')
EQ[19] = sb(it('f'),t('cap'))+t(' = 1 − cos')+par(t('arcsin')+sq(fr(sb(it('B'),t('loc')),sb(it('B'),t('throat')))))+t(' = 12.1%')
EQ[20] = sp(t('sin'),t('2'))+sb(it('θ'),t('exit'))+t(' = ')+fr(sb(it('B'),t('exit')),sb(it('B'),t('throat')))+t(' = 3×')+sp(t('10'),t('−8'))+t(',  ')+sb(it('θ'),t('exit'))+t(' ≈ 0.010°')
EQ[21] = sb(it('t'),t('ff'))+t(' = ')+sq(fr(t('3')+it('π'),t('32')+it('Gρ')))+t(' = 0.29 s')
EQ[22] = it('Γ')+t(' ∝ exp')+par(t('−')+it('c')+t('/')+sb(it('α'),t('GUT')))+t(',  ')+it('c')+t(' ≈ 4')
EQ[23] = it('σ')+t(' ~ π')+sbsp(it('r'),t('c'),t('2'))+t(' ~ 2.4 × ')+sp(t('10'),t('−63'))+t(' ')+sp(t('m'),t('2'))
EQ[24] = fr(t('d')+it('M'),t('d')+it('t'))+t(' = ')+it('A')+t(' · ')+fr(it('P')+par(it('M')),sp(it('c'),t('2')))
EQ[25] = it('A')+t(' = ')+fr(it('γ')+sb(it('f'),t('cap')),par(it('γ')+t(' − 1'))+t('/')+it('γ'))+t(' − 1')
EQ[26] = sb(it('t'),t('boot'))+t(' = ')+fr(sp(it('G'),t('2'))+par(sbsp(it('M'),t('f'),t('3'))+t(' − ')+sbsp(it('M'),t('0'),t('3'))),t('3')+it('A')+t('ℏ')+sp(it('c'),t('4'))+it('f'))
EQ[27] = it('F')+t(' = ')+fr(it('β')+sb(it('P'),t('cap')),it('c'))+t(' = 55.3 MN')
EQ[28] = sb(it('v'),t('peak'))+t(' = ')+it('c')+t(' tanh')+par(fr(sb(it('v'),t('eff')),it('c'))+t(' ln ')+sb(it('R'),t('leg')))


def add_equation_row(doc, eq_num):
    """Add equation left-aligned with number right-aligned in a 2-column invisible table."""
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    # Remove borders
    tbl = table._tbl
    tblPr = tbl.tblPr if tbl.tblPr is not None else OxmlElement('w:tblPr')
    borders = OxmlElement('w:tblBorders')
    for border_name in ['top','left','bottom','right','insideH','insideV']:
        b = OxmlElement(f'w:{border_name}')
        b.set(qn('w:val'), 'none')
        b.set(qn('w:sz'), '0')
        b.set(qn('w:space'), '0')
        b.set(qn('w:color'), 'auto')
        borders.append(b)
    tblPr.append(borders)
    # Set total table width to full text area
    tblW = OxmlElement('w:tblW')
    tblW.set(qn('w:w'), '9026')
    tblW.set(qn('w:type'), 'dxa')
    tblPr.append(tblW)
    # Column widths: equation gets most space, number gets ~1 inch
    for ci, w in enumerate([7586, 1440]):
        tc = table.cell(0, ci)._tc
        tcPr = tc.get_or_add_tcPr()
        tcW = OxmlElement('w:tcW')
        tcW.set(qn('w:w'), str(w))
        tcW.set(qn('w:type'), 'dxa')
        tcPr.append(tcW)
    # Equation cell — left aligned
    cell_eq = table.cell(0, 0)
    p_eq = cell_eq.paragraphs[0]
    p_eq.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_eq.paragraph_format.space_before = Pt(2)
    p_eq.paragraph_format.space_after = Pt(2)
    if eq_num in EQ:
        p_eq._element.append(make_omath(EQ[eq_num]))
    else:
        p_eq.text = f'[Equation {eq_num}]'
    # Number cell — right aligned
    cell_num = table.cell(0, 1)
    p_num = cell_num.paragraphs[0]
    p_num.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_num.paragraph_format.space_before = Pt(2)
    p_num.paragraph_format.space_after = Pt(2)
    # Vertically center the number
    tc_num = cell_num._tc
    tcPr_num = tc_num.get_or_add_tcPr()
    vAlign = OxmlElement('w:vAlign')
    vAlign.set(qn('w:val'), 'center')
    tcPr_num.append(vAlign)
    run = p_num.add_run(f'({eq_num})')
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11)


def add_unnumbered_eq(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    omath_xml = f'<m:oMath xmlns:m="{M_NS}" xmlns:w="{W_NS}">{t(text)}</m:oMath>'
    p._element.append(etree.fromstring(omath_xml.encode()))


# ── Hardcoded tables ──
# Each: (caption, headers, rows, note_or_None)
TABLES = {}

TABLES[1] = (
    'Table 1. Assumption budget. All six assumptions are required simultaneously.',
    ['#', 'Assumption', 'Status', 'If wrong'],
    [
        ['1', 'Hawking radiation exists and is semiclassical at M ~ 10⁹ kg',
         'Near-universal consensus; never observed', 'No power source'],
        ['2', 'GUT magnetic monopoles exist',
         'Predicted by all GUTs; never observed [11]', 'No formation mechanism'],
        ['3', 'BPS limit (λ = 0 at GUT scale)',
         'Protected by N=2 SUSY [12]; untested', 'Monopole cloud cannot collapse'],
        ['4', 'Bodmer-Witten hypothesis (SQM is ground state)',
         'Bai and Chen 2025 constrains unpaired SQM but not CFL', 'No shell material'],
        ['5', 'CFL is ground state at operating chemical potential',
         'Theoretical [13, 14]; never observed', 'Gap-decoupling firewall fails'],
        ['6', 'Core-overlap monopole breeding at O(1) rate',
         'Derived from duality [12]; unsimulated', 'Cannot manufacture monopole inventory'],
    ], None)

TABLES[2] = (
    'Table 2. Species contributions to f.',
    ['Species', 'DOF', 'm/kT', 'S(m/kT)', 'Contribution to f'],
    [
        ['u, d, s quarks', '36 Weyl', '~0', '1.000', '1.472 × 10⁻³'],
        ['c quark', '12 Weyl', '0.120', '1.000', '4.91 × 10⁻⁴'],
        ['b quark', '12 Weyl', '0.395', '0.9995', '4.91 × 10⁻⁴'],
        ['t quark', '12 Weyl', '16.36', '1.2×10⁻⁵', '3.6 × 10⁻⁸'],
        ['e, μ leptons', '8 Weyl', '~0', '1.000', '3.27 × 10⁻⁴'],
        ['τ lepton', '4 Weyl', '0.168', '1.000', '1.64 × 10⁻⁴'],
        ['Neutrinos (3 gen.)', '6 Weyl', '0', '1.000', '2.45 × 10⁻⁴'],
        ['Gluons', '16 pol.', '0', '1.000', '2.69 × 10⁻⁴'],
        ['Photon', '2 pol.', '0', '1.000', '3.36 × 10⁻⁵'],
        ['W±', '6 pol.', '7.60', '0.0511', '5.15 × 10⁻⁶'],
        ['Z', '3 pol.', '8.63', '0.0255', '1.29 × 10⁻⁶'],
        ['Higgs', '1', '11.83', '0.0024', '1.74 × 10⁻⁷'],
        ['Graviton', '2 pol.', '0', '1.000', '3.84 × 10⁻⁶'],
        ['TOTAL', '', '', '', 'f = 3.503 × 10⁻³'],
    ], None)

TABLES[3] = (
    'Table 3. SQM shell parameters.',
    ['Parameter', 'Value'],
    [
        ['Inner radius R', '2 m'],
        ['Thickness t', '3 pm (3000 fm)'],
        ['Density ρ', '4 × 10¹⁷ kg/m³ (~2× nuclear)'],
        ['Mass M_shell', '6.0 × 10⁷ kg (60,000 t)'],
        ['Surface area A', '4πR² = 50.3 m²'],
        ['Phase', 'Color-flavor locked (CFL)'],
        ['Inner surface state', 'Bombardment-maintained electrosphere'],
        ['Outer surface state', 'Ground-state electrosphere'],
    ], None)

TABLES[4] = (
    'Table 4. Shell thickness versus muon punch-through.',
    ['t (fm)', 'E_c (GeV)', 'x_c', 'ε(x_c)', 'P_punch (muon channel)', 'M_shell (t)'],
    [
        ['640', '51', '4.84', '6.8 × 10⁻²', '380 TW', '12,900'],
        ['2,500', '200', '18.9', '4.7 × 10⁻⁷', '2.6 GW', '50,000'],
        ['3,000*', '240', '22.7', '1.5 × 10⁻⁸', '84 MW', '60,000'],
        ['4,000', '320', '30.3', '1.3 × 10⁻¹¹', '74 kW', '80,000'],
        ['5,000', '400', '37.8', '1.0 × 10⁻¹⁴', '58 W', '100,000'],
    ], '* Adopted design point.')

TABLES[5] = (
    'Table 5. Thrust scaling with black hole mass.',
    ['M (kg)', 'kT (GeV)', 'F (MN)', 'Shell', 'Fuel rate', 'Alpha Cen (fuel carried, relativistic)'],
    [
        ['10⁹*', '10.6', '55', '3 pm, 60 kt', '0.67 kg/s', '79 yr, v_peak 0.07c, R = 1.7'],
        ['2 × 10⁸', '53', '1,375', '10 pm, 200 kt', '17 kg/s', '19 yr, v_peak 0.30c, R = 9.4'],
        ['5 × 10⁷', '212', '21,800', '30 pm, 600 kt', '264 kg/s', '11 yr, v_peak 0.45c, R = 34'],
    ], '* Reference design.')

TABLES[6] = (
    'Table 6. Mission profiles with relativistic Tsiolkovsky accounting.',
    ['Target', 'Design', 'v_peak', 'Mass ratio R', 'Fuel (× M_dry)', 'Trip time'],
    [
        ['Alpha Cen (4.37 ly)', 'Reference (10⁹ kg)', '0.07c', '1.7', '0.7×', '79 yr'],
        ['Alpha Cen', 'High-thrust (2×10⁸ kg)', '0.30c', '9.4', '8.4×', '19 yr'],
        ['Alpha Cen', 'Sprint (5×10⁷ kg)', '0.45c', '34', '33×', '11 yr'],
        ['10 ly', 'Reference', '0.10c', '2.0', '1.0×', '113 yr'],
        ['10 ly', 'High-thrust', '0.35c', '14', '13×', '36 yr'],
        ['100 ly', 'High-thrust', '0.50c', '54', '53×', '220 yr'],
    ], None)

TABLES[7] = (
    'Table 7. Comparison to prior work.',
    ['', 'Crane & Westmoreland 2009', 'Lee 2015', 'Present work (reference)', 'Present work (sprint)'],
    [
        ['Capture mechanism', '"Electron gas mirror" (unspecified)', 'Titanium absorption',
         'CFL SQM thermal converter', 'Same'],
        ['Capture fraction', 'Assumed ~100%', '46.5%', '83%', '83%'],
        ['Alpha Cen trip', 'Not calculated', 'Not achievable', '79 yr at 0.07c', '11 yr at 0.45c'],
        ['Thrust', 'Not calculated', '—', '55 MN', '21,800 MN'],
        ['I_sp', 'Not calculated', '—', '1.01 × 10⁷ s', 'Same'],
        ['Fuel', 'Not specified', 'N/A', 'Any matter', 'Any matter (33× M_dry)'],
        ['Thermal limit', 'Not addressed', 'Titanium melting (33 km standoff)',
         'None (Usov self-regulation)', 'Same'],
        ['Confinement', '"Particle beams"', 'None', 'Anti-Helmholtz', 'Same'],
        ['Formation', 'Gamma-ray kugelblitz', 'N/A', 'BPS monopole collapse', 'Same'],
    ], None)


def add_data_table(doc, tbl_num):
    caption, headers, rows, note = TABLES[tbl_num]
    doc.add_paragraph(caption, style='Tab1')
    ncols = len(headers)
    nrows = len(rows) + 1
    tbl = doc.add_table(rows=nrows, cols=ncols)
    tbl.style = 'Table Grid'
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for ci, h in enumerate(headers):
        cell = tbl.cell(0, ci)
        cell.text = h
        for p in cell.paragraphs:
            for run in p.runs:
                run.font.size = Pt(9)
                run.font.name = 'Times New Roman'
                run.font.bold = True
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            cell = tbl.cell(ri + 1, ci)
            cell.text = val
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(9)
                    run.font.name = 'Times New Roman'
    if note:
        p = doc.add_paragraph(note, style='Normal')
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(8)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.size = Pt(9)
            run.font.italic = True


# Inject tables BEFORE these subsection/section headings
INJECT_BEFORE = {
    '1.4': [1],
    '2.4': [2],
    '3.3': [3],
    '3.5': [4],
    '6.2': [5],
    '6.5': [6],
    '7.': [7],
}


# ── Build document ──
with open('drafts/draft_5_submission.md', 'r') as f:
    lines = f.readlines()

doc = Document()
for sec in doc.sections:
    sec.top_margin = Cm(2.54)
    sec.bottom_margin = Cm(2.54)
    sec.left_margin = Cm(2.54)
    sec.right_margin = Cm(2.54)

s = doc.styles['Normal']
s.font.name = 'Times New Roman'
s.font.size = Pt(12)
s.paragraph_format.space_after = Pt(6)
s.paragraph_format.line_spacing = 1.15

for nm, sz, bd, it_flag, al, sb_pt, sa_pt in [
    ('Title1', 14, True, False, WD_ALIGN_PARAGRAPH.CENTER, 0, 12),
    ('Author1', 12, False, False, WD_ALIGN_PARAGRAPH.CENTER, 0, 4),
    ('Sec1', 12, True, False, None, 18, 6),
    ('Sub1', 11, True, True, None, 12, 4),
    ('Tab1', 10, True, False, None, 12, 4),
    ('Fig1', 10, False, True, None, 6, 6),
    ('Ref1', 9, False, False, None, 0, 2),
]:
    st = doc.styles.add_style(nm, WD_STYLE_TYPE.PARAGRAPH)
    st.font.name = 'Times New Roman'
    st.font.size = Pt(sz)
    st.font.bold = bd
    st.font.italic = it_flag
    if al: st.paragraph_format.alignment = al
    st.paragraph_format.space_before = Pt(sb_pt)
    st.paragraph_format.space_after = Pt(sa_pt)

doc.styles['Ref1'].paragraph_format.left_indent = Cm(0.6)
doc.styles['Ref1'].paragraph_format.first_line_indent = Cm(-0.6)

# ── Parse ──
i = 0
past_refs = False
skip_end = False
eq_re = re.compile(r'\((\d+)\)\s*$')

while i < len(lines):
    line = lines[i]
    s = line.strip()
    if not s: i += 1; continue

    leading = len(line) - len(line.lstrip())

    # Skip TABLES and FIGURE CAPTIONS end-matter
    if s in ('TABLES', 'FIGURE CAPTIONS'):
        skip_end = True
        i += 1; continue
    if skip_end:
        i += 1; continue

    # Title
    if 'SOLVING THE THREE OPEN PROBLEMS' in s:
        doc.add_paragraph(s, style='Title1'); i += 1; continue

    # Author
    if s in ('B. Greff', 'Independent Researcher') or s.startswith('Correspondence:'):
        p = doc.add_paragraph(s, style='Author1')
        if s.startswith('Correspondence:'): p.paragraph_format.space_after = Pt(18)
        i += 1; continue

    # Abstract
    if s.startswith('Black hole propulsion --'):
        p = doc.add_paragraph(style='Normal')
        run_label = p.add_run('ABSTRACT: ')
        run_label.font.bold = True
        run_label.font.size = Pt(10)
        run_label.font.name = 'Times New Roman'
        add_formatted_text(p, s, font_size=Pt(10), italic=True)
        p.paragraph_format.space_after = Pt(12)
        i += 1; continue

    # Keywords
    if s.startswith('Keywords:'):
        p = doc.add_paragraph()
        add_formatted_text(p, s, font_size=Pt(10), italic=True)
        p.paragraph_format.space_after = Pt(18)
        i += 1; continue

    # REFERENCES
    if s == 'REFERENCES':
        past_refs = True
        doc.add_paragraph(s, style='Sec1'); i += 1; continue

    # ACKNOWLEDGEMENTS
    if s == 'ACKNOWLEDGEMENTS':
        past_refs = False
        doc.add_paragraph(s, style='Sec1'); i += 1; continue

    # Ref items
    if past_refs and re.match(r'^\d+\.\s+[A-Z]', s):
        p = doc.add_paragraph(style='Ref1')
        add_formatted_text(p, s, font_size=Pt(9))
        i += 1; continue

    # Section headings — check for table injection
    sec_match = re.match(r'^(\d+)\.\s+[A-Z]{2}', s)
    if sec_match:
        sec_num = sec_match.group(1) + '.'
        if sec_num in INJECT_BEFORE:
            for tbl_num in INJECT_BEFORE[sec_num]:
                add_data_table(doc, tbl_num)
        doc.add_paragraph(s, style='Sec1'); i += 1; continue

    # Subsection headings — check for table injection
    sub_match = re.match(r'^(\d+\.\d+)\s+\w', s)
    if sub_match:
        sub_num = sub_match.group(1)
        if sub_num in INJECT_BEFORE:
            for tbl_num in INJECT_BEFORE[sub_num]:
                add_data_table(doc, tbl_num)
        p = doc.add_paragraph(style='Sub1')
        add_formatted_text(p, s, font_size=Pt(11), bold=True, italic=True)
        i += 1; continue

    # Numbered equations
    m = eq_re.search(s)
    if leading >= 16 and m:
        eq_num = int(m.group(1))
        add_equation_row(doc, eq_num)
        i += 1; continue

    # Unnumbered centered equations
    if leading >= 16 and s and not s.startswith('Table') and not s.startswith('Figure'):
        add_unnumbered_eq(doc, s)
        i += 1; continue

    # Skip figure placeholders
    if '[INSERT FIGURE' in s:
        i += 1; continue

    # Skip table captions in body (tables injected at section boundaries)
    if s.startswith('Table ') and len(s) > 6 and s[6:7].isdigit():
        i += 1; continue

    # Skip figure captions in body
    if s.startswith('Figure ') and len(s) > 7 and s[7:8].isdigit():
        i += 1; continue

    # Skip table data rows (indented 2-15 spaces)
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

    # Normal paragraph
    p = doc.add_paragraph(style='Normal')
    add_formatted_text(p, s)
    i += 1

# ── Save DOCX ──
out_docx = 'drafts/GREFF_2026_paper.docx'
doc.save(out_docx)
print(f'DOCX saved: {out_docx} ({os.path.getsize(out_docx)//1024} KB)')

print('For PDF, run: .venv/bin/python drafts/build_latex.py')
