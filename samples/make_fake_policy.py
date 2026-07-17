"""Generate a fake-but-realistic Indian health insurance policy PDF for testing
the Insurance Decoder. Fictional insurer. Deliberately loaded with the classic
traps: looks cheap upfront, brutal at claim time."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

styles = getSampleStyleSheet()
H1 = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=15, spaceAfter=6)
H2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=11, spaceBefore=10, spaceAfter=4)
P = ParagraphStyle('P', parent=styles['Normal'], fontSize=8.5, leading=11.5)
FINE = ParagraphStyle('FINE', parent=styles['Normal'], fontSize=7, leading=9, textColor=colors.HexColor('#444444'))

def tbl(data, widths=None, font=8):
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.4, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dce6f1')),
        ('FONTSIZE', (0,0), (-1,-1), font),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    return t

doc = SimpleDocTemplate("SurakshaPlus_Health_Policy.pdf", pagesize=A4,
                        topMargin=14*mm, bottomMargin=14*mm, leftMargin=15*mm, rightMargin=15*mm)
E = []

# ---------- Page 1: the shiny schedule ----------
E += [Paragraph("BHAROSA GENERAL INSURANCE COMPANY LIMITED", H1),
      Paragraph("Regd. Office: 4th Floor, Ekta Tower, Andheri (E), Mumbai 400069 | IRDAI Regn. No. 187 | CIN: U66000MH2009PLC194321", FINE),
      Spacer(1, 6),
      Paragraph("<b>SURAKSHA PLUS FAMILY HEALTH POLICY — SCHEDULE</b>", H2),
      Paragraph("UIN: BHAHLIP26041V010405 | Policy No: SP/2026/07/0483321", P), Spacer(1, 4)]

E.append(tbl([
    ["Proposer", "Rahul Sharma", "Policy Period", "05-Jul-2026 to 04-Jul-2027 (both days incl.)"],
    ["Plan", "Suraksha Plus – Value Zone B", "Sum Insured (Floater)", "Rs. 5,00,000"],
    ["Insured Persons", "Self (34), Spouse (31), Son (4)", "Pre-Policy Check-up", "Waived (declaration basis)"],
], [28*mm, 62*mm, 38*mm, 52*mm], 7.5))
E.append(Spacer(1, 8))

E.append(Paragraph("<b>PREMIUM COMPUTATION</b>", H2))
E.append(tbl([
    ["Component", "Amount (Rs.)"],
    ["Base Premium (Zone A rates)", "9,120"],
    ["Zone B Discount (see Cl. 5.4)*", "(1,368)"],
    ["Floater Loading @ 18%", "1,642"],
    ["Aggregate Deductible Credit (Cl. 4.9)", "(912)"],
    ["Health Questionnaire Loading @ 10% (BMI/declaration)", "912"],
    ["Voluntary Co-payment Discount (15% co-pay opted, Cl. 4.7)", "(1,394)"],
    ["Sub-total", "8,000"],
    ["GST @ 18%", "1,440"],
    ["TOTAL PREMIUM PAYABLE", "9,440"],
], [110*mm, 40*mm]))
E.append(Paragraph("*Zone B discount is applicable only where all treatment is availed in Zone B/C cities. "
    "Treatment availed in Zone A cities shall attract an additional co-payment of 20% of admissible claim "
    "amount over and above any co-payment stated elsewhere in this Policy (Cl. 5.4.2).", FINE))
E.append(Spacer(1, 6))
E.append(Paragraph("<b>KEY BENEFITS AT A GLANCE</b>", H2))
E.append(tbl([
    ["Benefit", "Limit"],
    ["In-patient Hospitalisation", "Up to Sum Insured"],
    ["Room Rent / Boarding", "1% of Sum Insured per day (Rs. 5,000/day); ICU 2%"],
    ["Pre / Post Hospitalisation", "30 days / 60 days (capped at 10% of admissible claim)"],
    ["Day Care Procedures", "141 listed procedures only"],
    ["Ambulance", "Rs. 1,500 per hospitalisation"],
    ["Cumulative Bonus", "5% per claim-free year, max 25%; reduces by 10% per claim year"],
    ["Restoration of Sum Insured", "Once, for unrelated illness only, after full exhaustion"],
], [90*mm, 60*mm]))
E.append(PageBreak())

# ---------- Page 2: definitions & the traps ----------
E += [Paragraph("PART II — OPERATIVE CLAUSES, DEFINITIONS AND CONDITIONS", H2),
 Paragraph("<b>3.12 Room Rent Eligibility & Proportionate Deduction.</b> Where the Insured Person is admitted "
   "to a room whose rent exceeds the eligible limit stated in the Schedule, the Company shall be liable only for "
   "a proportionate share of ALL Associated Medical Expenses (including surgeon's fees, anaesthetist fees, OT "
   "charges, diagnostics, and medicines billed during hospitalisation) in the ratio which the eligible room rent "
   "bears to the actual room rent occupied. Illustration: eligible room Rs. 5,000, occupied room Rs. 10,000 — "
   "the Company pays 50% of all such expenses irrespective of Sum Insured available.", P),
 Paragraph("<b>4.7 Voluntary Co-payment.</b> The Insured has opted for a voluntary co-payment of 15% on each and "
   "every claim in consideration of the premium discount reflected in the Schedule. This co-payment applies in "
   "addition to (and shall be computed after) the Zone-based co-payment under Cl. 5.4.2 and the age-based "
   "co-payment of 10% applicable to any Insured Person aged 61 years or above at the time of claim.", P),
 Paragraph("<b>4.9 Aggregate Deductible.</b> An aggregate deductible of Rs. 25,000 per policy year applies to all "
   "claims other than accidental hospitalisation. The deductible credit shown in the premium computation is "
   "consideration for this deductible and does not constitute a reduction thereof.", P),
 Paragraph("<b>5.1 Initial Waiting Period.</b> 30 days from inception for all illnesses (not applicable to accidents).", P),
 Paragraph("<b>5.2 Specified Disease Waiting Period — 24 months:</b> cataract; benign prostatic hypertrophy; hernia; "
   "hydrocele; fissure/fistula; piles; sinusitis; gall bladder stones; kidney/urinary stones; joint replacement "
   "unless due to accident; varicose veins; ENT disorders requiring surgery.", P),
 Paragraph("<b>5.3 Pre-Existing Diseases — 48 months.</b> Any condition, ailment, injury or disease diagnosed, or "
   "for which medical advice or treatment was received, within 48 months prior to inception, and any complication "
   "arising therefrom, is excluded for 48 months of continuous coverage. Non-disclosure of any such condition "
   "in the proposal shall render the Policy voidable ab initio under Cl. 8.1.", P),
 Paragraph("<b>5.5 Sub-limits per Policy Year (within Sum Insured):</b>", P),
]
E.append(tbl([
    ["Treatment", "Maximum Payable"],
    ["Cataract (per eye)", "Rs. 24,000"],
    ["Total Knee Replacement (per knee)", "Rs. 80,000"],
    ["Cardiac procedures (incl. angioplasty, CABG)", "Rs. 1,50,000"],
    ["Cerebrovascular / neuro surgery", "Rs. 1,50,000"],
    ["Renal complications incl. dialysis (annual aggregate)", "Rs. 75,000"],
    ["Cancer treatment (annual aggregate, all modalities)", "Rs. 2,00,000"],
    ["Modern treatments (robotic surgery, immunotherapy etc.)", "25% of Sum Insured"],
], [100*mm, 50*mm]))
E += [Spacer(1, 4),
 Paragraph("<b>6. PERMANENT EXCLUSIONS (Standard & Specific).</b> Expenses attributable to: (a) consumables, "
   "non-medical items per Annexure-II (gloves, syringes, PPE kits, admission kits, nebulisation kits, thermometer, "
   "crepe bandage etc.); (b) treatment taken outside India; (c) obesity/weight control treatment; (d) treatment "
   "of sleep apnoea; (e) stem cell therapy; (f) dental treatment unless necessitated by accident and requiring "
   "hospitalisation; (g) maternity, infertility and allied expenses; (h) external congenital anomalies; "
   "(i) unproven/experimental treatment; (j) domiciliary hospitalisation; (k) OPD expenses of any nature; "
   "(l) any hospitalisation primarily for investigation/evaluation/observation; (m) treatment at any hospital "
   "excluded in the Company's list of de-empanelled providers as updated on the Company website from time to time.", P),
 Paragraph("<b>7.3 Claim Intimation.</b> Planned hospitalisation must be intimated at least 72 hours in advance; "
   "emergency hospitalisation within 24 hours of admission, failing which the Company may reduce the admissible "
   "claim by 25% or reject the claim where prejudice is caused. Cashless facility is available only at Network "
   "Providers in Zone B/C under this plan variant; reimbursement claims must be filed within 15 days of discharge "
   "with original bills, failing which the claim shall lapse.", P),
 Paragraph("<b>8.4 Renewal Loading.</b> Notwithstanding anything contained herein, upon renewal the Company may "
   "apply a claims-linked loading of up to 50% of renewal premium where claims ratio in the expiring policy year "
   "exceeds 80%, subject to IRDAI norms.", P),
 Spacer(1, 8),
 Paragraph("This document is a computer generated policy and does not require signature. For the detailed policy "
   "wording, Annexure-II (non-payable items, 199 entries) and grievance redressal, visit www.bharosagi.in. "
   "Insurance is the subject matter of solicitation.", FINE),
 Paragraph("— FICTIONAL DOCUMENT FOR SOFTWARE TESTING ONLY. 'Bharosa General Insurance' does not exist. —", FINE),
]
doc.build(E)
print("written SurakshaPlus_Health_Policy.pdf")
