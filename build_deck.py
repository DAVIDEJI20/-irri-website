#!/usr/bin/env python3
"""Draft deck: Next Tech procurement issue analysis (~12 slides, plain human wording)."""
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
r.text = "Procurement Problem Analysis and Prioritisation"
r.font.size = Pt(34); r.font.bold = True; r.font.color.rgb = NAVY
p2 = tf.add_paragraph(); r2 = p2.add_run()
r2.text = "Client: a multinational semiconductor major  |  Manager's internal review"
r2.font.size = Pt(17); r2.font.color.rgb = GREY
p3 = tf.add_paragraph(); r3 = p3.add_run()
r3.text = "1. The issues, evidence and impact     2. What to prioritise     3. Questions for the client"
r3.font.size = Pt(15); r3.font.italic = True; r3.font.color.rgb = ACCENT

# ---- 2. Context ----
s = add_slide(); title_box(s, "The situation: one company running as 59")
body(s, [
    (0, "This is really one problem, not 59. The company grew through acquisitions but never brought those businesses together.", True),
    (0, "All 59 sites still run as separate organisations, each with its own procurement, supplier base and back-end systems (Oracle, SAP and PeopleSoft).", False),
    (0, "Two central teams are meant to cover procurement across every site.", False),
    (0, "The company handles about 1.8 million procurement transactions a day, so even a small inefficiency adds up fast.", True),
    (0, "Everything here comes from the manager's own internal analysis.", False),
], top=1.5, size=17)

# ---- 3. Issues: root causes ----
s = add_slide(); title_box(s, "1. The issues: root causes (the real drivers)", "Problem, evidence and business impact")
body(s, [
    (0, "R1  No executive backing to enforce a common way of working", True),
    (1, "The central teams are responsible for the process but have no authority to make 59 independent sites follow it, so nothing gets standardised. This is the one that holds everything else back.", False),
    (0, "R2  59 separate units from M&A that were never joined up", True),
    (1, "Each has its own processes, suppliers and systems, which means duplication, no single view of spend and no buying power.", False),
    (0, "R3  No standard process", True),
    (1, "Staff are trained to process invoices in lots of different ways, which causes errors, slow cycles and poor visibility.", False),
    (0, "R4  Systems that barely talk to each other", True),
    (1, "Three ERPs (Oracle, SAP, PeopleSoft) are poorly connected, so people fall back on manual workarounds and there is no joined-up spend data.", False),
], top=1.5, size=16)

# ---- 4. Issues: symptoms ----
s = add_slide(); title_box(s, "1. The issues: what it costs day to day")
body(s, [
    (0, "S1  Slow payments to suppliers (from the analysis)", True),
    (1, "Assumption: this likely brings late-payment charges, missed early-payment discounts and frustrated suppliers.", False),
    (0, "S2  Loss of buying power (from the analysis)", True),
    (1, "Spread across so many suppliers, the company pays more and ends up with duplicate contracts (see the next slide).", False),
    (0, "S3  Too many catalogue items and small purchases (from the analysis)", True),
    (1, "A single low-value item can mean several separate orders to different suppliers, which is expensive at 1.8 million transactions a day.", False),
    (0, "S4  Uneven teams (from the analysis)", True),
    (1, "Team 1 has 2 full-timers plus part-timers and 2 open roles, and is slow. Team 2 has 7 people plus 2 seniors and is much quicker.", False),
    (0, "S5  Low morale, with procurement seen as low-value admin (from the analysis)", True),
    (1, "Assumption: this risks people leaving and makes change harder.", False),
], top=1.4, size=15)

# ---- 5. Evidence spotlight ----
s = add_slide(); title_box(s, "Evidence: the supplier base is growing, not consolidating")
body(s, [
    (0, "2023:  224 suppliers,  $900M spend", True),
    (0, "2024:  264 suppliers,  $1,045M spend", True),
    (1, "That is 40 more suppliers (up 18%) and $145M more spend (up 16%).", False),
    (1, "But the average spend per supplier fell, from $4.02M to $3.96M.", False),
    (0, "So spend is rising while it is being spread across more suppliers, which is the opposite of building buying power.", True),
    (1, "This backs up the loss of buying power and the fact the units were never joined up.", False),
    (0, "Assumption: these look like group totals, so a breakdown by site or category would show where the opportunity sits.", False),
], top=1.5, size=16)

# ---- 6. Most important ----
s = add_slide(); title_box(s, "The issue I think matters most", "My view")
body(s, [
    (0, "For me it is R1, the lack of executive backing.", True),
    (1, "It is not the costliest problem, but it is the one that has to be solved before any of the others can move.", False),
    (1, "Across 59 independent sites you cannot standardise processes, bring systems together or tidy up suppliers unless leadership requires it.", False),
    (1, "If it is left alone, spend and the supplier base just keep spreading, which is exactly what the 2023 to 2024 figures show. It is cheap to fix and it makes everything else possible.", False),
], top=1.7, size=18)

# ---- 7. Prioritisation ----
s = add_slide(); title_box(s, "2. What I would prioritise: three moves that matter most", "The priorities and the reasoning, not a full rebuild")
body(s, [
    (1, "1.  Get executive backing and a clear requirement to comply", True),
    (2, "Quick, low cost, and it makes everything else possible.", False),
    (1, "2.  Agree one standard procure-to-pay process and tidy up the catalogue and small-value spend", True),
    (2, "The biggest near-term gain at 1.8 million transactions a day, and it does not need new systems.", False),
    (1, "3.  Even out the two teams by filling Team 1's open roles or moving work across", True),
    (2, "A quick win that also helps morale.", False),
    (0, "Assumption: these three give most of the benefit, so bigger changes can wait until the data backs them.", False),
], top=1.5, size=16)

# ---- 8. Long-term / related issues ----
s = add_slide(); title_box(s, "Related issues to come back to later", "Bigger, costlier changes that should be led by data")
body(s, [
    (0, "Bringing the ERPs (Oracle, SAP, PeopleSoft) together, or at least connecting them properly.", True),
    (0, "Tidying up the supplier base to rebuild buying power.", True),
    (0, "Moving the 59 sites towards one way of working, or a shared service.", True),
    (0, "Assumption: I am not assuming a full system merge is the right answer yet. That is a big call and should be based on spend, running costs and contract lock-ins.", False),
], top=1.6, size=17)

# ---- 9. Organisational factors ----
s = add_slide(); title_box(s, "Why this is a priority across the business", "People, process, governance and systems")
body(s, [
    (0, "People", True),
    (1, "The teams are uneven, morale is low and procurement is seen as low value, so there is limited capacity and appetite for change.", False),
    (0, "Process", True),
    (1, "No standard process, a lot of manual work and too many catalogue items, all multiplied across 1.8 million transactions a day.", False),
    (0, "Governance", True),
    (1, "No executive requirement to comply, which is what turns these problems into a real priority.", False),
    (0, "Systems", True),
    (1, "Three poorly connected ERPs and no single view of spend.", False),
], top=1.4, size=15)

# ---- 10. Risks / constraints / dependencies ----
s = add_slide(); title_box(s, "Risks, constraints and dependencies that affect the priorities")
body(s, [
    (0, "The big dependency is executive backing. Without it the whole plan stalls.", True),
    (0, "The 59 sites are used to running themselves, so expect pushback on giving up control.", False),
    (0, "As a global business, local tax and legal rules limit how far one standard can go.", False),
    (0, "Team 1 is stretched thin, so there is little spare capacity to take on change.", False),
    (0, "Bringing the ERPs together would be costly and carries a real risk to day-to-day operations.", False),
    (0, "More acquisitions could keep adding to the problem, and some systems or suppliers may be locked into contracts.", False),
], top=1.5, size=16)

# ---- 11. Info needed ----
s = add_slide(); title_box(s, "What I would want to know before confirming the priorities")
body(s, [
    (0, "Spend by site, category and supplier, and how much supplier overlap there is.", False),
    (0, "Invoice volumes, how long payments take, and any late-payment charges.", False),
    (0, "What it costs to run the three ERPs.", False),
    (0, "How much of the 1.8 million daily transactions is small-value, and what one order costs to process.", False),
    (0, "How many catalogue items and contracts there are, and which are locked in.", False),
    (0, "The budget, the timeline, and whether leadership is genuinely willing to change.", False),
], top=1.5, size=17)

# ---- 12. Five questions ----
s = add_slide(); title_box(s, "3. Five questions for the client", "To help us get this right")
body(s, [
    (0, "1.  Spend and suppliers: what is the total spend, how does it split across the 59 sites, and how much supplier overlap is there?", True),
    (0, "2.  Governance: is leadership willing to require one common way of working, and who would own it?", True),
    (0, "3.  Transactions: how much of the 1.8 million a day is small-value spend, and what does it cost to process one order today?", True),
    (0, "4.  Systems: is bringing the ERPs together on the table, what is locked in by contract, and is the goal a shared service or keeping sites independent?", True),
    (0, "5.  People: what is behind the low morale, are Team 1's open roles funded, and can people move between the two teams?", True),
], top=1.4, size=15)

out = "/home/user/-irri-website/NextTech_Procurement_Analysis.pptx"
prs.save(out)
print("saved", out, "slides:", len(prs.slides._sldIdLst))
