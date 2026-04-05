"""
CMS Prior Authorization database — real HCPCS/CPT codes from CMS.
Sources: CMS-0057-F, 42 CFR 414.234, CMS PA Model data.
"""

ALL_PA_CODES = {
    # ── Lower Limb Prosthetics (6) ─────────────────────────────────────────
    "L5856": {
        "description": "Addition to lower extremity prosthesis, endoskeletal knee-shin system, microprocessor control feature, swing and stance phase",
        "category": "Lower Limb Prosthetics",
        "effective_date": "12/01/2020 Nationwide",
        "program": "DMEPOS",
    },
    "L5857": {
        "description": "Addition to lower extremity prosthesis, endoskeletal knee-shin system, microprocessor control feature, swing phase only",
        "category": "Lower Limb Prosthetics",
        "effective_date": "12/01/2020 Nationwide",
        "program": "DMEPOS",
    },
    "L5858": {
        "description": "Addition to lower extremity prosthesis, endoskeletal knee-shin system, microprocessor control feature, stance phase only",
        "category": "Lower Limb Prosthetics",
        "effective_date": "12/01/2020 Nationwide",
        "program": "DMEPOS",
    },
    "L5973": {
        "description": "Endoskeletal ankle foot system, microprocessor controlled feature, dorsiflexion control",
        "category": "Lower Limb Prosthetics",
        "effective_date": "12/01/2020 Nationwide",
        "program": "DMEPOS",
    },
    "L5974": {
        "description": "Addition, endoskeletal system, below knee, ultra-light material (titanium, carbon fiber)",
        "category": "Lower Limb Prosthetics",
        "effective_date": "12/01/2020 Nationwide",
        "program": "DMEPOS",
    },
    "L5980": {
        "description": "All lower extremity prostheses, flex-walk system or equal",
        "category": "Lower Limb Prosthetics",
        "effective_date": "12/01/2020 Nationwide",
        "program": "DMEPOS",
    },

    # ── Orthoses (15) ──────────────────────────────────────────────────────
    "L0631": {"description": "Lumbar-sacral orthosis, sagittal-coronal control, anterior-posterior-lateral control, custom-fabricated", "category": "Orthoses", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "L0632": {"description": "Lumbar-sacral orthosis, sagittal-coronal control, anterior-posterior-lateral control, prefabricated", "category": "Orthoses", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "L0633": {"description": "Lumbar-sacral orthosis, sagittal-coronal control, anterior-posterior-lateral control, prefabricated, off-the-shelf", "category": "Orthoses", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "L0634": {"description": "Lumbar-sacral orthosis, sagittal-coronal control, anterior-posterior-lateral control, custom-fitted", "category": "Orthoses", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "L1600": {"description": "Hip orthosis, abduction control of hip joints, flexible, prefabricated", "category": "Orthoses", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "L1610": {"description": "Hip orthosis, abduction control of hip joints, flexible, custom-fabricated", "category": "Orthoses", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "L1620": {"description": "Hip orthosis, abduction control of hip joints, semi-flexible (foam or rubber), prefabricated", "category": "Orthoses", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "L1630": {"description": "Hip orthosis, abduction control of hip joints, semi-rigid, prefabricated", "category": "Orthoses", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "L1640": {"description": "Hip orthosis, abduction control of hip joints, static, pelvic band and thigh cuff, custom-fabricated", "category": "Orthoses", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "L1650": {"description": "Hip orthosis, abduction control of hip joints, static, adjustable, custom-fabricated", "category": "Orthoses", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "L1660": {"description": "Hip orthosis, abduction control of hip joints, static, plastic, custom-fabricated", "category": "Orthoses", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "L1680": {"description": "Hip orthosis, dynamic, pelvic control, pull strap assist", "category": "Orthoses", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "L1685": {"description": "Hip orthosis, abduction control, dynamic adjustable, custom-fabricated", "category": "Orthoses", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "L1686": {"description": "Hip orthosis, abduction panel, custom-fabricated", "category": "Orthoses", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "L1690": {"description": "Combination, bilateral, lumbo-sacral, hip, femur orthosis, custom-fabricated", "category": "Orthoses", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},

    # ── Pneumatic Compression Devices (2) ──────────────────────────────────
    "E0650": {"description": "Pneumatic compressor, non-segmental home model", "category": "Pneumatic Compression Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "E0651": {"description": "Pneumatic compressor, segmental home model without calibrated gradient pressure", "category": "Pneumatic Compression Devices", "effective_date": "04/13/2026 Nationwide", "program": "DMEPOS"},

    # ── Power Mobility Devices (46) ────────────────────────────────────────
    "K0800": {"description": "Power operated vehicle, group 1 standard, patient weight capacity up to and including 300 pounds", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0801": {"description": "Power operated vehicle, group 1 heavy duty, patient weight capacity 301 to 450 pounds", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0802": {"description": "Power operated vehicle, group 1 very heavy duty, patient weight capacity 451 to 600 pounds", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0806": {"description": "Power operated vehicle, group 2 standard, patient weight capacity up to and including 300 pounds", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0807": {"description": "Power operated vehicle, group 2 heavy duty, patient weight capacity 301 to 450 pounds", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0808": {"description": "Power operated vehicle, group 2 very heavy duty, patient weight capacity 451 to 600 pounds", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0812": {"description": "Power operated vehicle, group 3 standard, patient weight capacity up to and including 300 pounds", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0813": {"description": "Power wheelchair, group 1 standard, patient weight capacity up to and including 300 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0814": {"description": "Power wheelchair, group 1 heavy duty, patient weight capacity 301 to 450 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0815": {"description": "Power wheelchair, group 1 very heavy duty, patient weight capacity 451 to 600 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0816": {"description": "Power wheelchair, group 1 extra heavy duty, patient weight capacity 601 lbs or more", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0820": {"description": "Power wheelchair, group 2 standard, patient weight capacity up to and including 300 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0821": {"description": "Power wheelchair, group 2 heavy duty, patient weight capacity 301 to 450 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0822": {"description": "Power wheelchair, group 2 very heavy duty, patient weight capacity 451 to 600 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0823": {"description": "Power wheelchair, group 2 standard, captains chair, patient weight capacity up to and including 300 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0824": {"description": "Power wheelchair, group 2 heavy duty, captains chair, patient weight capacity 301 to 450 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0825": {"description": "Power wheelchair, group 2 very heavy duty, captains chair, patient weight capacity 451 to 600 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0826": {"description": "Power wheelchair, group 2 extra heavy duty, captains chair, patient weight capacity 601 lbs or more", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0827": {"description": "Power wheelchair, group 2 standard, single power option, patient weight capacity up to and including 300 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0828": {"description": "Power wheelchair, group 2 heavy duty, single power option, patient weight capacity 301 to 450 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0829": {"description": "Power wheelchair, group 2 very heavy duty, single power option, patient weight capacity 451 to 600 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0835": {"description": "Power wheelchair, group 2 standard, multiple power option, patient weight capacity up to and including 300 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0836": {"description": "Power wheelchair, group 2 heavy duty, multiple power option, patient weight capacity 301 to 450 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0837": {"description": "Power wheelchair, group 2 very heavy duty, multiple power option, patient weight capacity 451 to 600 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0838": {"description": "Power wheelchair, group 2 extra heavy duty, multiple power option, patient weight capacity 601 lbs or more", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0839": {"description": "Power wheelchair, group 2 standard, power seat elevation, patient weight capacity up to and including 300 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0840": {"description": "Power wheelchair, group 2 extra heavy duty, power seat elevation, patient weight capacity 601 lbs or more", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0841": {"description": "Power wheelchair, group 2 standard, power standing system, patient weight capacity up to and including 300 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0842": {"description": "Power wheelchair, group 2 very heavy duty, power standing system, patient weight capacity 451 to 600 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0843": {"description": "Power wheelchair, group 3 standard, patient weight capacity up to and including 300 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0848": {"description": "Power wheelchair, group 3 heavy duty, patient weight capacity 301 to 450 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0849": {"description": "Power wheelchair, group 3 very heavy duty, patient weight capacity 451 to 600 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0850": {"description": "Power wheelchair, group 3 extra heavy duty, patient weight capacity 601 lbs or more", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0851": {"description": "Power wheelchair, group 3 standard, single power option, patient weight capacity up to and including 300 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0852": {"description": "Power wheelchair, group 3 heavy duty, single power option, patient weight capacity 301 to 450 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0853": {"description": "Power wheelchair, group 3 very heavy duty, single power option, patient weight capacity 451 to 600 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0854": {"description": "Power wheelchair, group 3 extra heavy duty, single power option, patient weight capacity 601 lbs or more", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0855": {"description": "Power wheelchair, group 3 standard, multiple power option, patient weight capacity up to and including 300 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0856": {"description": "Power wheelchair, group 3 heavy duty, multiple power option, patient weight capacity 301 to 450 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0857": {"description": "Power wheelchair, group 3 very heavy duty, multiple power option, patient weight capacity 451 to 600 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0858": {"description": "Power wheelchair, group 3 extra heavy duty, multiple power option, patient weight capacity 601 lbs or more", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0859": {"description": "Power wheelchair, group 3 standard, power seat elevation, patient weight capacity up to and including 300 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0860": {"description": "Power wheelchair, group 3 heavy duty, power seat elevation, patient weight capacity 301 to 450 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0861": {"description": "Power wheelchair, group 3 standard, power standing system, patient weight capacity up to and including 300 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0862": {"description": "Power wheelchair, group 4 standard, patient weight capacity up to and including 300 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0863": {"description": "Power wheelchair, group 4 heavy duty, patient weight capacity 301 to 450 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0864": {"description": "Power wheelchair, group 4 very heavy duty, patient weight capacity 451 to 600 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0868": {"description": "Power wheelchair, group 4 standard, single power option, patient weight capacity up to and including 300 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "K0869": {"description": "Power wheelchair, group 4 standard, multiple power option, patient weight capacity up to and including 300 lbs", "category": "Power Mobility Devices", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},

    # ── Pressure Reducing Support Surfaces (5) ─────────────────────────────
    "E0193": {"description": "Powered air flotation bed (low air loss therapy)", "category": "Pressure Reducing Support Surfaces", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "E0194": {"description": "Air fluidized bed", "category": "Pressure Reducing Support Surfaces", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "E0277": {"description": "Powered pressure-reducing air mattress", "category": "Pressure Reducing Support Surfaces", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "E0371": {"description": "Nonpowered advanced pressure-reducing overlay for mattress, standard mattress length and width", "category": "Pressure Reducing Support Surfaces", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},
    "E0372": {"description": "Powered pressure-reducing mattress overlay", "category": "Pressure Reducing Support Surfaces", "effective_date": "09/01/2018 Nationwide", "program": "DMEPOS"},

    # ── OPD: Blepharoplasty (11) ───────────────────────────────────────────
    "15820": {"description": "Blepharoplasty, lower eyelid", "category": "Blepharoplasty", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "15821": {"description": "Blepharoplasty, lower eyelid; with extensive herniated fat pad", "category": "Blepharoplasty", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "15822": {"description": "Blepharoplasty, upper eyelid", "category": "Blepharoplasty", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "15823": {"description": "Blepharoplasty, upper eyelid; with excessive skin weighting down lid", "category": "Blepharoplasty", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "67900": {"description": "Repair of brow ptosis (supraciliary, mid-forehead or coronal approach)", "category": "Blepharoplasty", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "67901": {"description": "Repair of blepharoptosis; frontalis muscle technique with suture or other material", "category": "Blepharoplasty", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "67902": {"description": "Repair of blepharoptosis; frontalis muscle technique with autologous fascial sling", "category": "Blepharoplasty", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "67903": {"description": "Repair of blepharoptosis; (tarso) levator resection or advancement, internal approach", "category": "Blepharoplasty", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "67904": {"description": "Repair of blepharoptosis; (tarso) levator resection or advancement, external approach", "category": "Blepharoplasty", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "67906": {"description": "Repair of blepharoptosis; superior rectus technique with fascial sling", "category": "Blepharoplasty", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "67908": {"description": "Repair of blepharoptosis; conjunctivo-tarso-Muller's muscle-levator resection", "category": "Blepharoplasty", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},

    # ── OPD: Botulinum Toxin (6) ───────────────────────────────────────────
    "64612": {"description": "Chemodenervation of muscle(s); muscle(s) innervated by facial nerve, unilateral", "category": "Botulinum Toxin", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "64615": {"description": "Chemodenervation of muscle(s); muscle(s) innervated by facial, trigeminal, cervical spinal and accessory nerves, bilateral", "category": "Botulinum Toxin", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "64616": {"description": "Chemodenervation of muscle(s); neck muscle(s), excluding muscles of the larynx, unilateral", "category": "Botulinum Toxin", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "64617": {"description": "Chemodenervation of larynx; percutaneous, needle electromyograph guidance", "category": "Botulinum Toxin", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "64642": {"description": "Chemodenervation of one extremity; 1-4 muscle(s)", "category": "Botulinum Toxin", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "64644": {"description": "Chemodenervation of one extremity; 5 or more muscles", "category": "Botulinum Toxin", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},

    # ── OPD: Panniculectomy (3) ────────────────────────────────────────────
    "15830": {"description": "Excision, excessive skin and subcutaneous tissue (includes lipectomy); abdomen, infraumbilical panniculectomy", "category": "Panniculectomy", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "15847": {"description": "Excision, excessive skin and subcutaneous tissue (includes lipectomy); abdomen (e.g., abdominoplasty) (includes umbilicoplasty, if performed)", "category": "Panniculectomy", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "17999": {"description": "Unlisted procedure, skin, mucous membrane and subcutaneous tissue", "category": "Panniculectomy", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},

    # ── OPD: Rhinoplasty (12) ──────────────────────────────────────────────
    "30400": {"description": "Rhinoplasty, primary; lateral and alar cartilages and/or elevation of nasal tip", "category": "Rhinoplasty", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "30410": {"description": "Rhinoplasty, primary; complete, external parts including bony pyramid, lateral and alar cartilages", "category": "Rhinoplasty", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "30420": {"description": "Rhinoplasty, primary; including major septal repair", "category": "Rhinoplasty", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "30430": {"description": "Rhinoplasty, secondary; minor revision (small amount of nasal tip work)", "category": "Rhinoplasty", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "30435": {"description": "Rhinoplasty, secondary; intermediate revision (bony work with osteotomies)", "category": "Rhinoplasty", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "30450": {"description": "Rhinoplasty, secondary; major revision (nasal tip work and osteotomies)", "category": "Rhinoplasty", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "30460": {"description": "Rhinoplasty for nasal deformity secondary to congenital cleft lip and/or palate, including columellar lengthening; tip only", "category": "Rhinoplasty", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "30462": {"description": "Rhinoplasty for nasal deformity secondary to congenital cleft lip and/or palate, including columellar lengthening; tip, septum, osteotomies", "category": "Rhinoplasty", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "30465": {"description": "Repair of nasal vestibular stenosis (e.g., spreader grafting, lateral nasal wall reconstruction)", "category": "Rhinoplasty", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "30520": {"description": "Septoplasty or submucous resection, with or without cartilage scoring, contouring or replacement with graft", "category": "Rhinoplasty", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "30540": {"description": "Repair choanal atresia; intranasal", "category": "Rhinoplasty", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "30545": {"description": "Repair choanal atresia; transpalatine", "category": "Rhinoplasty", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},

    # ── OPD: Vein Ablation (8) ─────────────────────────────────────────────
    "36470": {"description": "Injection of sclerosant; single incompetent vein (other than telangiectasia)", "category": "Vein Ablation", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "36471": {"description": "Injection of sclerosant; multiple incompetent veins (other than telangiectasia), same leg", "category": "Vein Ablation", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "36475": {"description": "Endovenous ablation therapy of incompetent vein, extremity, inclusive of all imaging guidance and monitoring, percutaneous, radiofrequency; first vein treated", "category": "Vein Ablation", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "36476": {"description": "Endovenous ablation therapy of incompetent vein, extremity, inclusive of all imaging guidance and monitoring, percutaneous, radiofrequency; second and subsequent veins treated", "category": "Vein Ablation", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "36478": {"description": "Endovenous ablation therapy of incompetent vein, extremity, inclusive of all imaging guidance and monitoring, percutaneous, laser; first vein treated", "category": "Vein Ablation", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "36479": {"description": "Endovenous ablation therapy of incompetent vein, extremity, inclusive of all imaging guidance and monitoring, percutaneous, laser; second and subsequent veins treated", "category": "Vein Ablation", "effective_date": "09/01/2018 Nationwide", "program": "OPD"},
    "36482": {"description": "Endovenous ablation therapy of incompetent vein, extremity, inclusive of all imaging guidance and monitoring, percutaneous, mechanochemical; first vein treated", "category": "Vein Ablation", "effective_date": "09/01/2018 Nationwide", "program": "OPD"},
    "36483": {"description": "Endovenous ablation therapy of incompetent vein, extremity, inclusive of all imaging guidance and monitoring, percutaneous, mechanochemical; second and subsequent veins treated", "category": "Vein Ablation", "effective_date": "09/01/2018 Nationwide", "program": "OPD"},

    # ── OPD: Cervical Fusion (2) ───────────────────────────────────────────
    "22551": {"description": "Arthrodesis, anterior interbody, including disc space preparation, discectomy, osteophytectomy and decompression of spinal cord and/or nerve roots; cervical below C2", "category": "Cervical Fusion", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "22552": {"description": "Arthrodesis, anterior interbody, including disc space preparation, discectomy, osteophytectomy and decompression of spinal cord and/or nerve roots; cervical below C2, each additional interspace", "category": "Cervical Fusion", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},

    # ── OPD: Spinal Neurostimulators (1) ──────────────────────────────────
    "63650": {"description": "Percutaneous implantation of neurostimulator electrode array, epidural", "category": "Spinal Neurostimulators", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},

    # ── OPD: Facet Joint Interventions (8) ────────────────────────────────
    "64490": {"description": "Injection(s), diagnostic or therapeutic agent, paravertebral facet (zygapophyseal) joint (or nerves innervating that joint) with image guidance (fluoroscopy or CT), cervical or thoracic; single level", "category": "Facet Joint Interventions", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "64491": {"description": "Injection(s), diagnostic or therapeutic agent, paravertebral facet (zygapophyseal) joint (or nerves innervating that joint) with image guidance (fluoroscopy or CT), cervical or thoracic; second level", "category": "Facet Joint Interventions", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "64492": {"description": "Injection(s), diagnostic or therapeutic agent, paravertebral facet (zygapophyseal) joint (or nerves innervating that joint) with image guidance (fluoroscopy or CT), cervical or thoracic; third and any additional level(s)", "category": "Facet Joint Interventions", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "64493": {"description": "Injection(s), diagnostic or therapeutic agent, paravertebral facet (zygapophyseal) joint (or nerves innervating that joint) with image guidance (fluoroscopy or CT), lumbar or sacral; single level", "category": "Facet Joint Interventions", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "64494": {"description": "Injection(s), diagnostic or therapeutic agent, paravertebral facet (zygapophyseal) joint (or nerves innervating that joint) with image guidance (fluoroscopy or CT), lumbar or sacral; second level", "category": "Facet Joint Interventions", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "64495": {"description": "Injection(s), diagnostic or therapeutic agent, paravertebral facet (zygapophyseal) joint (or nerves innervating that joint) with image guidance (fluoroscopy or CT), lumbar or sacral; third and any additional level(s)", "category": "Facet Joint Interventions", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "64633": {"description": "Destruction by neurolytic agent, paravertebral facet joint nerve(s), with image guidance (fluoroscopy or CT); cervical or thoracic, single facet joint", "category": "Facet Joint Interventions", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},
    "64634": {"description": "Destruction by neurolytic agent, paravertebral facet joint nerve(s), with image guidance (fluoroscopy or CT); cervical or thoracic, each additional facet joint", "category": "Facet Joint Interventions", "effective_date": "07/01/2012 Nationwide", "program": "OPD"},

    # ── New 2026 Codes effective April 13, 2026 (7) ────────────────────────
    "L0651": {"description": "Lumbar-sacral orthosis, sagittal-coronal control, flexion-extension-lateral control, custom-fabricated", "category": "Orthoses", "effective_date": "04/13/2026 Nationwide", "program": "DMEPOS"},
    "L1844": {"description": "Knee orthosis, rigid, without joint(s), includes soft interface, custom-fabricated", "category": "Orthoses", "effective_date": "04/13/2026 Nationwide", "program": "DMEPOS"},
    "L1846": {"description": "Knee orthosis, rigid, without joint(s), includes soft interface, prefabricated, off-the-shelf", "category": "Orthoses", "effective_date": "04/13/2026 Nationwide", "program": "DMEPOS"},
    "L1852": {"description": "Knee orthosis, without knee joint(s), rounds or condylar pads and soft interface only with or without posterior straps, prefabricated", "category": "Orthoses", "effective_date": "04/13/2026 Nationwide", "program": "DMEPOS"},
    "L1932": {"description": "Ankle foot orthosis, rigid anterior tibial section, total contact, prefabricated, off-the-shelf", "category": "Orthoses", "effective_date": "04/13/2026 Nationwide", "program": "DMEPOS"},
    "E0652": {"description": "Pneumatic compressor, segmental home model with calibrated gradient pressure", "category": "Pneumatic Compression Devices", "effective_date": "04/13/2026 Nationwide", "program": "DMEPOS"},
}

REGULATORY_RULES = {
    "rule": "CMS-0057-F — Improving Prior Authorization Processes for Medicaid, CHIP, and Medicare Advantage Plans",
    "effective_date": "January 1, 2026",
    "api_deadline": "January 1, 2027",
    "standard_decision_timeframe": "7 calendar days",
    "expedited_decision_timeframe": "72 hours",
    "affected_payers": [
        "Medicare Advantage Organizations (MAOs)",
        "State Medicaid Fee-for-Service programs",
        "CHIP programs",
        "Medicaid Managed Care Organizations",
        "CHIP Managed Care Entities",
    ],
    "required_public_metrics": [
        "Total prior auth requests received",
        "Total approvals and denials by service category",
        "Average time from request to final decision",
        "Number of requests requiring additional information",
        "Appeals filed and outcomes",
    ],
    "pa_api_requirements": [
        "FHIR-based Prior Authorization API",
        "Payer-to-payer data exchange",
        "Patient Access API updates",
        "Provider Access API",
        "Interoperability and burden reduction",
    ],
    "key_provisions": [
        "Impacted payers must send PA decisions within 7 calendar days (standard) or 72 hours (expedited)",
        "Reasons for denial must be specific and actionable",
        "PA must be valid for the duration of treatment",
        "Continuity of care protections when patients switch plans",
        "Gold carding: waiving PA for providers with high approval rates",
    ],
}

DMEPOS_DOCUMENTATION_REQUIREMENTS = {
    "source": "42 CFR 414.234 — Prior Authorization of Durable Medical Equipment",
    "requirements": [
        "Written order/prescription from treating practitioner",
        "Medical records documenting medical necessity",
        "Detailed product description (HCPCS code, brand, model)",
        "Proof of delivery (once item is dispensed)",
        "Face-to-face examination documentation within required timeframe",
        "Applicable clinical criteria met per LCD (Local Coverage Determination)",
    ],
    "face_to_face_requirement": "Practitioner examination within 6 months prior to written order",
    "lcd_sources": "CMS Medical Review Contractors (Noridian, Palmetto, CGS, National Government Services)",
}

STATS = {
    "total_codes_in_database": len(ALL_PA_CODES),
    "dmepos_codes": 74,
    "opd_codes": 51,
    "new_2026_codes": 7,
    "ama_survey_pa_requests_per_physician_per_week": 39,
    "caqh_annual_cost_billions": 1.3,
    "cert_improper_payment_rate_orthoses": "61.5-78.9%",
    "cert_improper_payment_rate_power_mobility": "45-60%",
    "cert_improper_payment_rate_pressure_surfaces": "30-40%",
    "cert_years": "2021-2024",
    "cert_source": "CMS CERT (Comprehensive Error Rate Testing)",
    "ama_benchmark_manual_pa_minutes": 45,
    "caqh_cost_per_manual_pa": 31.00,
}


def lookup_cms_pa_requirement(code: str) -> dict:
    """Look up a specific HCPCS/CPT code in the CMS PA database."""
    code = code.upper().strip()
    if code in ALL_PA_CODES:
        return {"found": True, "code": code, "data": ALL_PA_CODES[code]}
    return {"found": False, "code": code, "message": f"Code {code} not found in CMS prior authorization database"}


def search_pa_codes(keyword: str) -> list:
    """Search CMS PA codes by keyword in description or category."""
    keyword = keyword.lower()
    results = []
    for code, data in ALL_PA_CODES.items():
        if keyword in data["description"].lower() or keyword in data["category"].lower():
            results.append({"code": code, **data})
    return results[:20]  # cap at 20


def get_new_2026_codes() -> dict:
    """Get the 7 new codes effective April 13, 2026."""
    new_codes = ["L0651", "L1844", "L1846", "L1852", "L1932", "E0651", "E0652"]
    return {code: ALL_PA_CODES[code] for code in new_codes if code in ALL_PA_CODES}


def get_all_categories() -> dict:
    """Get all codes organized by category."""
    categories: dict = {}
    for code, data in ALL_PA_CODES.items():
        cat = data["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append({"code": code, "description": data["description"]})
    return categories


def get_regulatory_rules() -> dict:
    """Get CMS-0057-F regulatory rules."""
    return REGULATORY_RULES


def get_documentation_requirements() -> dict:
    """Get DMEPOS documentation requirements from 42 CFR 414.234."""
    return DMEPOS_DOCUMENTATION_REQUIREMENTS
