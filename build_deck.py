#!/usr/bin/env python3
"""Draft deck: Next Tech procurement issue analysis (tight ~12-slide version)."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

NAVY = RGBColor(0x1F, 0x38, 0x64)
GREY = RGBColor(0x44, 0x44, 0x44)
ACCENT = RGBColor(0xC0, 0x39, 0x2B)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def add_slide():
    return prs.slides.add_slide(BLANK)


def title_box(slide, text, sub=None):
    tb = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.3), Inches(1.1))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = text
    r.font.size = Pt(28); r.font.bold = True; r.font.color.rgb = NAVY
    if sub:
        p2 = tf.add_paragraph()
        r2 = p2.add_run(); r2.text = sub
        r2.font.size = Pt(15); r2.font.color.rgb = ACCENT; r2.font.italic = True
    return slide


def body(slide, items, top=1.5, left=0.6, width=12.1, height=5.6, size=16):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    first = True
    for level, text, bold in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.level = level
        r = p.add_run(); r.text = text
        r.font.size = Pt(size - level * 1)
        is_assumption = text.lstrip().lower().startswith("assumption")
        r.font.bold = bold
        if is_assumption:
            r.font.italic = True
            r.font.color.rgb = ACCENT
        else:
            r.font.color.rgb = NAVY if bold and level == 0 else GREY
        p.space_after = Pt(5)
    return slide


# ---- 1. Title ----
s = add_slide()
tb = s.shapes.add_textbox(Inches(0.8), Inches(2.5), Inches(11.7), Inches(2.6))
tf = tb.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; r = p.add_run()
r.text = "Procurement Problem Analysis & Prioritisation"
r.font.size = Pt(34); r.font.bold = True; r.font.color.rgb = NAVY
p2 = tf.add_paragraph(); r2 = p2.add_run()
r2.text = "Client: Multinational Semiconductor Major  |  Manager's internal review"
r2.font.size = Pt(17); r2.font.color.rgb = GREY
p3 = tf.add_paragraph(); r3 = p3.add_run()
r3.text = "1. The issues, evidence & impact   2. Prioritisation   3. Questions for the client"
r3.font.size = Pt(15); r3.font.italic = True; r3.font.color.rgb = ACCENT

# ---- 2. Context ----
s = add_slide(); title_box(s, "Context: one company running as 59")
body(s, [
    (0, "A multinational semiconductor major grew through M&A but never integrated the acquired businesses.", True),
    (0, "59 operating locations run as independent organisations, each with its own procurement processes, supplier community and back-end systems (Oracle, SAP, PeopleSoft).", False),
    (0, "Two central procurement teams are accountable for end-to-end process across all 59 locations.", False),
    (0, "Scale: ~1.8 million procurement transactions every day — so every inefficiency is multiplied massively.", True),
    (0, "A manager's internal analysis surfaced the issues that follow.", False),
], top=1.5, size=17)

# ---- 3. Issues: root causes ----
s = add_slide(); title_box(s, "1. The issues — root causes (the drivers)", "Problem | evidence | business impact")
body(s, [
    (0, "R1  No executive sponsorship to enforce compliance", True),
    (1, "Teams are accountable but have no mandate; 'control of all 59 is a huge challenge' -> nothing can be standardised. The keystone issue.", False),
    (0, "R2  59 independent units from M&A, never integrated", True),
    (1, "Own processes, suppliers and systems -> duplication, no single source of truth, no buying leverage.", False),
    (0, "R3  No standardised process design", True),
    (1, "Staff upskilled to process invoices many different ways -> errors, slow cycles, no end-to-end visibility.", False),
    (0, "R4  Fragmented, poorly integrated systems (Oracle / SAP / PeopleSoft)", True),
    (1, "'Not well integrated', 'a lot of manual processes' -> rework, high IT/training cost, no consolidated spend data.", False),
], top=1.5, size=16)

# ---- 4. Issues: symptoms ----
s = add_slide(); title_box(s, "1. The issues — symptoms (what hurts day to day)")
body(s, [
    (0, "S1  Protracted payables (stated)", True),
    (1, "Assumption: drives late-payment penalties, lost early-payment discounts and strained supplier relationships.", False),
    (0, "S2  Lost economies of scale (stated)", True),
    (1, "Fragmented spend -> higher prices and duplicate contracts (see supplier evidence next).", False),
    (0, "S3  Catalogue proliferation & tail spend (stated)", True),
    (1, "Low-value items need multiple orders to different suppliers — costly at 1.8M txns/day.", False),
    (0, "S4  Resourcing imbalance (stated)", True),
    (1, "Team 1: 2 FTE + part-timers + 2 vacancies (slow).  Team 2: 7 + 2 seniors (fast).", False),
    (0, "S5  Low morale — procurement seen as low-value back-office work (stated)", True),
    (1, "Assumption: creates attrition risk and change fatigue.", False),
], top=1.4, size=15)

# ---- 5. Evidence spotlight: supplier trend ----
s = add_slide(); title_box(s, "Evidence: the supplier base is fragmenting, not consolidating")
body(s, [
    (0, "2023:  224 suppliers  |  $900M spend", True),
    (0, "2024:  264 suppliers  |  $1,045M spend", True),
    (1, "Suppliers +40 (+18%); spend +$145M (+16%).", False),
    (1, "Average spend per supplier FELL: $4.02M -> $3.96M.", False),
    (0, "So spend is rising but buying leverage per supplier is falling — adding suppliers faster than consolidating them.", True),
    (1, "Direct evidence for S2 (lost economies of scale) and R2 (fragmented, un-integrated units).", False),
    (0, "Assumption: figures are group-wide; a per-unit / per-category split would size the consolidation opportunity.", False),
], top=1.5, size=16)

# ---- 6. Most important ----
s = add_slide(); title_box(s, "Which issue matters most?", "Our view")
body(s, [
    (0, "Most important = R1: secure executive sponsorship and a compliance mandate.", True),
    (1, "Not the most expensive problem, but the dependency that unblocks everything else.", False),
    (1, "With 59 autonomous units, you cannot standardise processes, consolidate systems or rationalise suppliers unless leadership mandates it.", False),
    (1, "Business impact: without it, spend and the supplier base keep fragmenting (as 2023->2024 shows). Low cost, high leverage — fix it first.", False),
], top=1.7, size=18)

# ---- 7. Prioritisation ----
s = add_slide(); title_box(s, "2. Prioritisation — three high-impact moves", "Prioritised issue and why — not a full redesign")
body(s, [
    (1, "1.  R1 — Secure executive sponsorship & a compliance mandate", True),
    (2, "Low cost, fast, unlocks every other fix. Highest leverage move available.", False),
    (1, "2.  R3 + S3 — Standardise procure-to-pay & rationalise catalogue / tail spend", True),
    (2, "Biggest near-term efficiency gain at 1.8M txns/day — achievable WITHOUT replacing systems.", False),
    (1, "3.  S4 — Rebalance the two central teams (fill Team 1 vacancies / shift workload)", True),
    (2, "Fast operational win that lifts throughput and morale.", False),
    (0, "Assumption: these three deliver most of the benefit; structural changes are deferred until data justifies them.", False),
], top=1.5, size=16)

# ---- 8. Long-term / related issues ----
s = add_slide(); title_box(s, "Related issues — longer-term focus", "Higher cost / risk: later-stage, data-led decisions")
body(s, [
    (0, "R4 — Consolidate / better integrate the ERPs (Oracle, SAP, PeopleSoft)", True),
    (0, "S2 — Rationalise the supplier base to rebuild buying leverage", True),
    (0, "R2 — Move the 59 units toward one operating model / shared services", True),
    (0, "Assumption: a full ERP consolidation is NOT assumed to be the right answer yet — it should be a business case decided on spend, cost-to-serve and lock-in data.", False),
], top=1.6, size=17)

# ---- 9. Organisational factors that make this a priority ----
s = add_slide(); title_box(s, "Why this is a priority — organisational factors", "People · Process · Governance · Systems")
body(s, [
    (0, "People", True),
    (1, "Imbalanced teams (Team 1 understaffed, 2 vacancies, part-timers) + low morale + 'low-value' perception = limited capacity and appetite to deliver change.", False),
    (0, "Process", True),
    (1, "No standard P2P, manual processes, catalogue proliferation, multiple orders for low-value items — inefficiency scales to 1.8M txns/day.", False),
    (0, "Governance", True),
    (1, "No executive mandate; teams accountable but cannot enforce compliance across 59 units — this is what elevates everything to a priority.", False),
    (0, "Systems", True),
    (1, "Three poorly integrated ERPs (Oracle/SAP/PeopleSoft) -> manual rework, no consolidated spend data, high IT/training cost.", False),
], top=1.4, size=15)

# ---- 10. Risks / constraints / dependencies ----
s = add_slide(); title_box(s, "Key risks, constraints & dependencies affecting prioritisation")
body(s, [
    (0, "Dependency: executive sponsorship is the gating dependency — the plan stalls without it.", True),
    (0, "Constraint: 59 autonomous units will resist giving up control (cultural).", False),
    (0, "Constraint: multinational tax / statutory / regulatory rules limit a single standard.", False),
    (0, "Constraint: thin Team 1 capacity + low morale limit bandwidth to absorb change.", False),
    (0, "Risk: ERP consolidation carries cost, business-continuity and data-migration risk.", False),
    (0, "Risk: ongoing M&A may keep re-introducing fragmentation; contractual lock-ins on systems/suppliers.", False),
], top=1.5, size=16)

# ---- 10. Info needed ----
s = add_slide(); title_box(s, "Information needed before confirming priorities")
body(s, [
    (0, "Spend by unit / category / supplier, and supplier overlap across units.", False),
    (0, "Invoice volumes, cycle times, late-payment penalties and maverick-spend rates.", False),
    (0, "Cost of running the three ERPs (licences + support).", False),
    (0, "Share of the 1.8M daily transactions that is low-value/tail vs strategic, and cost-to-process per order.", False),
    (0, "Number of catalogue items and contracts; contractual lock-ins.", False),
    (0, "Budget, timeline and genuine executive appetite for change.", False),
], top=1.5, size=17)

# ---- 11. Five questions ----
s = add_slide(); title_box(s, "3. Five questions for the client", "To better inform our work")
body(s, [
    (0, "1.  Spend & suppliers — total spend, split across the 59 units, and how much supplier overlap exists between them?", True),
    (0, "2.  Governance — is there executive appetite to mandate a single, compliant operating model, and who would sponsor it?", True),
    (0, "3.  Transaction mix — of the 1.8M daily transactions, what share is low-value/tail, and what does one order cost to process today?", True),
    (0, "4.  Systems — is ERP consolidation on the table, what lock-ins exist, and is the target shared services or continued unit autonomy?", True),
    (0, "5.  People — what's driving low morale, are Team 1's vacancies funded, and can resource move between the two teams?", True),
], top=1.4, size=15)

out = "/home/user/-irri-website/NextTech_Procurement_Analysis.pptx"
prs.save(out)
print("saved", out, "slides:", len(prs.slides._sldIdLst))
