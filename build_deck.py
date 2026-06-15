#!/usr/bin/env python3
"""Draft deck: Next Tech procurement issue analysis."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

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
    r.font.size = Pt(30); r.font.bold = True; r.font.color.rgb = NAVY
    if sub:
        p2 = tf.add_paragraph()
        r2 = p2.add_run(); r2.text = sub
        r2.font.size = Pt(15); r2.font.color.rgb = ACCENT; r2.font.italic = True
    return slide


def body(slide, items, top=1.5, left=0.6, width=12.1, height=5.5, size=16):
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
        p.space_after = Pt(6)
    return slide


# ---- Title ----
s = add_slide()
tb = s.shapes.add_textbox(Inches(0.8), Inches(2.6), Inches(11.7), Inches(2.5))
tf = tb.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; r = p.add_run()
r.text = "Procurement Transformation — Problem Analysis & Prioritisation"
r.font.size = Pt(34); r.font.bold = True; r.font.color.rgb = NAVY
p2 = tf.add_paragraph(); r2 = p2.add_run()
r2.text = "Client: Multinational Semiconductor Major  |  Prepared for the Manager's internal review"
r2.font.size = Pt(17); r2.font.color.rgb = GREY
p3 = tf.add_paragraph(); r3 = p3.add_run()
r3.text = "1. The issues   2. Prioritisation   3. Questions for the client"
r3.font.size = Pt(15); r3.font.italic = True; r3.font.color.rgb = ACCENT

# ---- Context ----
s = add_slide(); title_box(s, "Context: one company running as 59")
body(s, [
    (0, "A multinational semiconductor major grew through M&A but never integrated the acquired businesses.", True),
    (0, "59 operating locations run as independent organisations, each with its own:", True),
    (1, "Procurement processes and process design", False),
    (1, "Supplier community", False),
    (1, "Back-end systems (Oracle, SAP, PeopleSoft)", False),
    (0, "Two central procurement teams are accountable for end-to-end process across all 59 locations.", True),
    (0, "Scale: ~1.8 million procurement transactions every day — so every inefficiency is multiplied massively.", True),
    (0, "An internal analysis by the manager surfaced the issues on the following slides.", False),
])

# ===== SECTION 1 DIVIDER =====
s = add_slide(); title_box(s, "1.  The Issues", "Problem statement | Evidence | Business impact")
body(s, [
    (0, "We have grouped the findings into ROOT CAUSES (the drivers) and SYMPTOMS (what hurts day to day).", True),
    (0, "Root causes:", True),
    (1, "R1 — No executive sponsorship / governance to enforce compliance", False),
    (1, "R2 — Fragmented operating model: 59 independent units from M&A", False),
    (1, "R3 — No standardised process design", False),
    (1, "R4 — Fragmented, poorly integrated systems (Oracle / SAP / PeopleSoft)", False),
    (0, "Symptoms:", True),
    (1, "S1 — Protracted payables    S2 — Lost economies of scale", False),
    (1, "S3 — Catalogue proliferation & tail spend    S4 — Resourcing imbalance    S5 — Low morale", False),
], top=1.5)

# Root cause detail slides
def issue_slide(code_title, problem, evidence, impact):
    s = add_slide(); title_box(s, code_title)
    body(s, [
        (0, "Problem statement", True), (1, problem, False),
        (0, "Evidence", True), (1, evidence, False),
        (0, "Impact on the business", True), (1, impact, False),
    ], top=1.4, size=17)
    return s

issue_slide("R1 — No executive sponsorship / governance",
    "The two central teams are accountable for end-to-end process but have no executive mandate to enforce compliance across the 59 units.",
    "Internal analysis: 'lack of executive support to drive compliance'; 'keeping control of all 59 is a huge challenge'.",
    "Standardisation cannot be enforced. Every other fix stalls without this — it is the keystone issue.")

issue_slide("R2 — Fragmented operating model (59 independent units)",
    "M&A bolted businesses together but never integrated them; each unit runs its own procurement, suppliers and systems.",
    "59 locations operating as independent organisations with different supplier communities and back-end processes.",
    "Duplication of effort and contracts, no single source of truth, and no aggregated buying leverage.")

issue_slide("R3 — No standardised process design",
    "There is no common procure-to-pay process; each unit invoices and buys its own way.",
    "Internal analysis: 'lack of standard process design'; staff must be upskilled to process invoices many different ways.",
    "Errors, slow cycle times, high training burden, and no end-to-end control or visibility.")

issue_slide("R4 — Fragmented, poorly integrated systems",
    "Three or more ERPs (Oracle, SAP, PeopleSoft) operate in parallel with weak integration, forcing manual workarounds.",
    "Internal analysis: systems 'not well integrated', 'a lot of manual processes' needed; staff upskilled across many systems.",
    "Manual rework, reconciliation pain, high IT/training cost, and no consolidated spend data.")

# Symptoms summary slide
s = add_slide(); title_box(s, "Symptoms — what these root causes produce")
body(s, [
    (0, "S1  Protracted payables (stated in the analysis)", True),
    (1, "Assumption: this drives late-payment penalties, strained supplier relationships and lost early-payment discounts.", False),
    (0, "S2  Lost economies of scale (stated)", True),
    (1, "Assumption: fragmented spend means higher unit prices, duplicate contracts and no volume discounts.", False),
    (0, "S3  Catalogue proliferation & tail spend (stated)", True),
    (1, "Low-value items require multiple orders to different suppliers — costly at 1.8M txns/day.", False),
    (0, "S4  Resourcing imbalance (stated)", True),
    (1, "Team 1: 2 FTE + part-timers + 2 vacancies (slow).  Team 2: 7 + 2 seniors (fast). Inconsistent service.", False),
    (0, "S5  Low morale / perception (stated)", True),
    (1, "Assumption: this creates attrition risk and change fatigue.", False),
], top=1.4, size=15)

# Most important
s = add_slide(); title_box(s, "Which issue matters most?", "Our view")
body(s, [
    (0, "Most important = R1: secure executive sponsorship and a governance mandate.", True),
    (1, "It is not the most expensive problem, but it is the dependency that unblocks everything else.", False),
    (1, "With 59 autonomous units, you cannot standardise processes, consolidate systems or rationalise suppliers unless leadership mandates compliance.", False),
    (1, "Low cost, high leverage — fix it first.", False),
], top=1.6, size=18)

# ===== SECTION 2 =====
s = add_slide(); title_box(s, "2.  Prioritisation", "Three high-impact moves first — not a full redesign")
body(s, [
    (0, "We deliberately focus on a few high-impact, low-disruption actions rather than a multi-year transformation:", False),
    (1, "1.  R1 — Secure executive sponsorship & a compliance mandate", True),
    (2, "Low cost, fast, and unlocks every other fix. Highest leverage move available.", False),
    (1, "2.  R3 + S3 — Standardise the procure-to-pay process & rationalise catalogue / tail spend", True),
    (2, "Biggest near-term efficiency gain at 1.8M txns/day — achievable WITHOUT replacing systems.", False),
    (1, "3.  S4 — Rebalance the two central teams (fill Team 1 vacancies / shift workload)", True),
    (2, "Fast operational win that lifts throughput and morale.", False),
    (0, "Assumption: these three deliver most of the benefit; bigger structural changes are deferred until data justifies them.", False),
], top=1.4, size=15)

s = add_slide(); title_box(s, "Longer-term — only if the data justifies it")
body(s, [
    (0, "These are higher cost / higher risk, so treat as later-stage options, not day-one commitments:", False),
    (1, "R4 — Consolidate / better integrate the ERPs (Oracle, SAP, PeopleSoft)", True),
    (1, "S2 — Rationalise the supplier base to rebuild buying leverage", True),
    (1, "R2 — Move the 59 units toward one operating model / shared services", True),
    (0, "Assumption: a full ERP consolidation is NOT assumed to be the right answer yet — it should be a business case decided on spend, cost-to-serve and lock-in data.", False),
], top=1.5, size=16)

s = add_slide(); title_box(s, "Risks, dependencies & organisational factors")
body(s, [
    (0, "Cultural resistance from 59 autonomous units to giving up control", False),
    (0, "Lack of executive support is itself the #1 dependency — the plan stalls without it", True),
    (0, "ERP consolidation carries cost, business-continuity and data-migration risk", False),
    (0, "Multinational complexity — local tax / statutory / regulatory rules limit a single standard", False),
    (0, "Low morale + thin Team 1 capacity — limited bandwidth to absorb change work", False),
    (0, "Ongoing M&A may keep re-introducing fragmentation", False),
    (0, "Contractual lock-ins on systems and suppliers", False),
], top=1.5, size=17)

s = add_slide(); title_box(s, "Information needed before confirming priorities")
body(s, [
    (0, "Spend cube — spend by unit / category / supplier, and supplier overlap across units", False),
    (0, "Invoice volumes, cycle times, late-payment penalties, error / maverick-spend rates", False),
    (0, "Cost of running the three ERPs (licences + support)", False),
    (0, "Share of the 1.8M daily transactions that is low-value/tail vs strategic, and cost-to-process per order", False),
    (0, "Number of catalogue items and contracts; contractual lock-ins", False),
    (0, "Budget, timeline and genuine executive appetite for change", False),
], top=1.5, size=17)

s = add_slide(); title_box(s, "Assumptions we have made", "To be confirmed with the client")
body(s, [
    (0, "Assumption: protracted payables are causing real cost (penalties, lost discounts) — not yet quantified.", False),
    (0, "Assumption: fragmented spend is losing meaningful volume discounts across the 59 units.", False),
    (0, "Assumption: a large share of the 1.8M daily transactions is low-value/tail spend that can be consolidated.", False),
    (0, "Assumption: executive sponsorship is currently absent rather than present-but-ignored.", False),
    (0, "Assumption: the three named ERPs are the main systems; there may be more across 59 units.", False),
    (0, "Assumption: standardising process and catalogue delivers most of the benefit before any system replacement.", False),
], top=1.5, size=16)

# ===== SECTION 3 =====
s = add_slide(); title_box(s, "3.  Five questions for the client", "To better inform our work")
body(s, [
    (0, "1.  Spend & suppliers — What is total procurement spend, how does it split across the 59 units, and how much supplier overlap exists between them?", True),
    (0, "2.  Governance — Is there executive appetite to mandate a single, compliant operating model, and who would sponsor it?", True),
    (0, "3.  Transaction mix — Of the 1.8M daily transactions, what share is low-value/tail spend, and what does it cost to process one order today?", True),
    (0, "4.  Systems — Is ERP consolidation on the table, what contractual lock-ins exist, and is the target a shared-services model or continued unit autonomy?", True),
    (0, "5.  People — What is driving the low morale, are Team 1's vacancies funded, and can resource move between the two central teams?", True),
], top=1.4, size=15)

out = "/home/user/-irri-website/NextTech_Procurement_Analysis.pptx"
prs.save(out)
print("saved", out, "slides:", len(prs.slides._sldIdLst))
