#!/usr/bin/env python3
"""
Build Deficiency Register for Musina 33/11 kV Substation.
Exports to Excel for municipal council and NERSA audit.
"""
import pandas as pd

deficiencies = [
    {"ID": "D-001", "Location": "F2 Bay", "Description": "CT ratio unverifiable (painted over).",
     "Risk": "HIGH", "Root Cause": "Poor maintenance record‑keeping.",
     "Consequence": "Incorrect relay settings possible.", "Action": "Physical inspection and CT injection test.",
     "Priority": "IMMEDIATE", "NRS_Reference": "NRS 034‑1 Cl 4.3", "Cost_Estimate_ZAR": "5 000"},
    {"ID": "D-002", "Location": "All feeders", "Description": "No protection coordination (all TMS=0.1).",
     "Risk": "CRITICAL", "Root Cause": "No coordination study since commissioning.",
     "Consequence": "Simultaneous tripping — 51‑min hospital outage.", "Action": "Apply graded TMS per Section 3.",
     "Priority": "IMMEDIATE", "NRS_Reference": "NRS 034‑1 Cl 6.2", "Cost_Estimate_ZAR": "15 000"},
    {"ID": "D-003", "Location": "All feeder CDG‑11s", "Description": "Instantaneous elements not applicable (non‑directional).",
     "Risk": "HIGH", "Root Cause": "Common busbar topology prevents safe setting.",
     "Consequence": "Overreach if misapplied.", "Action": "Keep disabled; implement directional I>> on F1 SEL‑351S.",
     "Priority": "IMMEDIATE", "NRS_Reference": "IEC 60255‑151", "Cost_Estimate_ZAR": "Incl. in D‑002"},
    {"ID": "D-004", "Location": "All 11 kV feeders", "Description": "No dedicated Sensitive Earth Fault protection.",
     "Risk": "HIGH", "Root Cause": "Original design omitted SEF.", "Consequence": "High‑impedance earth faults undetected.",
     "Action": "Enable SEF on SEL‑351S (F1); specify SEF relays for remaining bays.",
     "Priority": "SHORT‑TERM", "NRS_Reference": "NRS 034‑1 Cl 7.1", "Cost_Estimate_ZAR": "47 000"},
    {"ID": "D-005", "Location": "Transformer T1", "Description": "No differential or REF protection.",
     "Risk": "HIGH", "Root Cause": "2003 standard did not mandate diff for 20 MVA.",
     "Consequence": "Slow internal fault clearance; catastrophic failure risk.",
     "Action": "Install SEL‑387 diff relay + high‑impedance REF.", "Priority": "MEDIUM‑TERM",
     "NRS_Reference": "IEC 60255‑8", "Cost_Estimate_ZAR": "180 000"},
    {"ID": "D-006", "Location": "Substation earth grid", "Description": "Grid not tested since 1998; touch potentials likely exceed IEEE 80.",
     "Risk": "HIGH", "Root Cause": "No periodic earthing audit programme.",
     "Consequence": "Personnel and public safety risk.", "Action": "Soil resistivity test, fall‑of‑potential, extend grid.",
     "Priority": "SHORT‑TERM", "NRS_Reference": "SANS 10313 / IEEE 80", "Cost_Estimate_ZAR": "35 000"},
    {"ID": "D-007", "Location": "33 kV surge arresters", "Description": "Annual arrester failures due to poor earthing and undersized energy class.",
     "Risk": "MEDIUM", "Root Cause": "Poor earthing elevates surge stress.", "Consequence": "Loss of overvoltage protection.",
     "Action": "Replace with Class 3 arresters; improve earthing.", "Priority": "SHORT‑TERM",
     "NRS_Reference": "IEC 60099‑4", "Cost_Estimate_ZAR": "12 000"},
    {"ID": "D-008", "Location": "SCADA system", "Description": "9600 baud RS‑232 modem — no remote fault data.",
     "Risk": "MEDIUM", "Root Cause": "System never upgraded.", "Consequence": "Delayed fault response; no post‑fault records.",
     "Action": "Install IEC 61850 MMS over fibre to control room.", "Priority": "MEDIUM‑TERM",
     "NRS_Reference": "IEC 61850‑5", "Cost_Estimate_ZAR": "85 000"},
    {"ID": "D-009", "Location": "F3 Residential feeder", "Description": "SSEG degrades fuse‑saving coordination; anti‑islanding window narrow.",
     "Risk": "HIGH", "Root Cause": "SSEG connected without protection review.", "Consequence": "Possible reclosing onto live island.",
     "Action": "Implement transfer‑trip communication for SSEG laterals.", "Priority": "SHORT‑TERM",
     "NRS_Reference": "NRS 097‑2‑1:2024", "Cost_Estimate_ZAR": "45 000"},
    {"ID": "D-010", "Location": "All 11 kV feeders", "Description": "Conductor type not verified — drawings show ACSR Mink but later tap‑offs possible.",
     "Risk": "MEDIUM", "Root Cause": "No post‑modification survey.", "Consequence": "Fault level calculations may be optimistic.",
     "Action": "Physical conductor survey on F3 laterals.", "Priority": "SHORT‑TERM",
     "NRS_Reference": "NRS 034‑1 Cl 4.1", "Cost_Estimate_ZAR": "3 000"},
]

df = pd.DataFrame(deficiencies)
df.to_excel("08_deficiency_register/deficiency_register.xlsx", index=False)
print("Deficiency register exported with {} items.".format(len(df)))
print("\nCRITICAL:", len(df[df.Risk == 'CRITICAL']))
print("HIGH:", len(df[df.Risk == 'HIGH']))
print("MEDIUM:", len(df[df.Risk == 'MEDIUM']))
