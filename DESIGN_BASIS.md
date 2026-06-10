# DESIGN BASIS — Musina 33/11 kV Brownfield Substation Protection Review

**Document ID:** MUS‑DB‑001‑R0  
**Project:** Brownfield protection review and deficiency register  
**Location:** Musina Municipal Substation, Limpopo, South Africa  
**Date:** 2026‑06‑10  
**Author:** Mangena
**Reviewer:** [Engineer]

---

## 1. PURPOSE AND SCOPE

This document defines all engineering assumptions, data sources, and parameter values used in the network reconstruction, fault study, protection coordination, earthing assessment, SSEG impact analysis, and IEC 61850 readiness assessment for the Musina 33/11 kV substation.

Where a parameter could not be verified by drawing or measurement, the assumed value, its justification, and the sensitivity to error are explicitly noted, in accordance with NRS 034‑1 Clause 4.1.

---

## 2. SOURCE IMPEDANCE AT 33 kV ESKOM BUS

| Parameter | Value | Justification |
|-----------|-------|---------------|
| Ssc,max | 400 MVA | Eskom Protection department verbal confirmation for Musina substation; historical fault level data for 33 kV network in this area. |
| Ssc,min | 180 MVA | Minimum infeed scenario (N‑1 Eskom generation, winter morning light load). Used for relay pickup sensitivity checks per IEC 60255‑151. |
| X/R ratio (max & min) | 0.1 | Typical for strong transmission‑connected 33 kV bus; confirmed with Eskom Planning. |

**Engineering note:**  
- Maximum infeed (400 MVA) determines the highest fault current that protection must interrupt safely.  
- Minimum infeed (180 MVA) determines whether relays will pick up for remote faults under weak system conditions. Minimum infeed is more demanding for IDMT grading and SEF sensitivity.

**Sensitivity:** If Ssc,min is lower in reality (e.g., 120 MVA during extreme N‑2), feeder IDMT curves may not meet the 0.3 s coordination time interval at far‑end faults. Recommendation: request updated Eskom fault levels annually.

---

## 3. TRANSFORMER DATA (T1 — 20 MVA, Dyn11)

| Parameter | Value | Source |
|-----------|-------|--------|
| Rated power | 20 MVA (ONAN) | Nameplate photograph taken 2026‑05‑12 |
| Voltage ratio | 33 000 / 11 000 V | Nameplate |
| Vector group | Dyn11 | Nameplate |
| Impedance voltage (Z%) | 9.5 % | Nameplate |
| X/R ratio | 18 | IEC 60076 typical for 20 MVA unit of 2003 vintage |
| Copper loss (vkr%) | 0.5 % | Estimate — no test report available; flagged as assumption |
| Iron loss | 25 kW | Estimate from IEC 60076 loss tables |
| Magnetising current | 0.5 % | Estimate |
| Neutral earthing (11 kV) | NER, 300 A design limit | Verified from NER nameplate in substation yard |
| Tap changer | Off‑load, ±2×2.5 % (assumed) | Not verified; no drawing shows tap position |

**Sensitivity:** Z% tolerance is ±10 % per IEC. If actual Z% is 8.5 %, fault levels on the 11 kV bus increase by ~11 %, potentially causing instantaneous element overreach. The fault study uses 9.5 % as baseline; sensitivity to 8.5 % and 10.5 % will be flagged in the coordination report.

---

## 4. FEEDER LINE PARAMETERS

| Feeder | Conductor | Length (km) | r (Ω/km) | x (Ω/km) | Source of length |
|--------|-----------|-------------|----------|----------|-------------------|
| F1 — Hospital / Water Treatment | ACSR Mink | 4.2 | 0.554 | 0.350 | GIS map (Municipal Town Planner, 2024) |
| F2 — CBD / Border Post | ACSR Mink | 3.1 | 0.554 | 0.350 | GIS map |
| F3 — Residential (SSEG) | ACSR Mink | 6.8 | 0.554 | 0.350 | GIS map |
| F4 — Industrial (Cold storage, Brick) | ACSR Mink | 2.9 | 0.554 | 0.350 | GIS map |

**Conductor verification:** One readable annotation on the 1998 11 kV SLD confirms “ACSR Mink” for F1. The other three feeders were re‑strung during a 2005 refurbishment; the same conductor type was specified in the works order (municipal records). No physical measurement has been taken. The positive‑sequence impedance values are taken from manufacturer data for ACSR Mink at 75 °C conductor temperature.

**Sensitivity:** If F3 is actually ACSR Rabbit (r=1.37 Ω/km) due to a later tap‑off not reflected in drawings, the far‑end fault current would drop by ~15 %, potentially making the existing IDMT pickup borderline. This risk is noted as Deficiency D‑010 (conductor verification required).

---

## 5. LOAD DATA

Based on 12 months of maximum demand from the municipal billing system (Jan–Dec 2025):

| Feeder | Peak load (A) | Power factor (assumed) | Notes |
|--------|---------------|------------------------|-------|
| F1 | 180 | 0.95 lag | Hospital base load + water treatment plant (2 pumps) |
| F2 | 210 | 0.90 lag | CBD commercial, border post lighting |
| F3 | 140 | 0.98 lag | Residential with growing rooftop solar (SSEG — see Section 6) |
| F4 | 195 | 0.85 lag | Cold storage compressors, brick manufacturer induction motors |

**Assumptions:**
- Load is balanced three‑phase at the feeder level for modelling purposes. In reality, F3 is single‑phase‑dominated; this simplification will not affect fault‑level calculations but may affect the SEF pickup assessment.
- The billing system captures only active energy (kWh). Power factors are estimated from typical load profiles for each customer class. The selected values are conservative for fault studies (higher power factor → lower current → slightly lower voltage drop, but negligible impact on fault levels).

---

## 6. CT RATIOS

| Bay | CT Ratio | Source |
|-----|----------|--------|
| F1 | 300/1 | Panel nameplate, readable |
| F2 | **UNKNOWN — see D‑001** | Nameplate painted over during 2014 repaint. Reverse‑engineered in Section 1.3. Most probable: 300/1. |
| F3 | 300/1 | Panel nameplate, readable |
| F4 | 300/1 | Panel nameplate, readable |
| 33 kV Incomer | 600/5 | Metering panel label |

**Method for reverse‑engineering F2 CT ratio:**  
From Section 1.3: with maximum load 210 A, CDG‑11 plug setting 125 % of 1 A (1.25 A secondary), and a 1.2 × load‑pickup safety margin, the minimum CT ratio to avoid pickup on load is 202/1. Standard IEC ratios above this are 200/1, 300/1, 400/1. The 200/1 gives marginal margin; 300/1 provides comfortable margin and matches the other three bays. A physical CT injection test must confirm.

**Deficiency D‑001:** CT ratio on F2 unverifiable. Relay settings calculated in this study assume 300/1; prior to energising any new settings, a CT ratio test and secondary injection test must be performed.

---

## 7. RELAY TYPES AND ORIGINAL SETTINGS

| Bay | Relay Model | Plug Setting | TMS | I>> (Inst) | Notes |
|-----|-------------|--------------|-----|------------|-------|
| F1 | GEC CDG‑11 (electromechanical) | 100 % (1 A tap) | 0.10 | Not observed | Curve: IEC Very Inverse. Installed 2003, last serviced 2018. |
| F2 | GEC CDG‑11 | 100 % (1 A tap) | 0.10 | Not observed | Curve: IEC Very Inverse. |
| F3 | GEC CDG‑11 | 75 % (1 A tap) | 0.10 | Not observed | Curve: IEC Very Inverse. |
| F4 | GEC CDG‑11 | 100 % (1 A tap) | 0.10 | Not observed | Curve: IEC Very Inverse. |
| Incomer | GEC CDG‑11 | 100 % (1 A tap at 600/5) | 0.15 | Not observed | Curve: IEC Very Inverse. |
| F1 (new) | SEL‑351S (numeric, installed 2019) | N/A | N/A | N/A | Settings not retrieved from relay — unit was locked. Will be addressed in Section 7. |
| Spare bay | Empty — relay removed after 2022 failure | — | — | — | Bay is de‑energised, no circuit breaker connected. |

**Original settings source:** Photocopy of a handwritten settings sheet found in the relay test cabinet. The sheet is dated “2003‑09‑10” and signed by a technician no longer with the municipality. Settings have not been verified by secondary injection since installation.

---

## 8. EARTHING GRID

| Parameter | Value | Source |
|-----------|-------|--------|
| Grid footprint | 40 m × 30 m | 1998 earthing drawing (only drawing recovered intact) |
| Conductor size | 25 mm² bare copper | Drawing annotation |
| Grid mesh spacing | 5 m × 5 m | Drawing annotation |
| Burial depth | 0.5 m | Drawing annotation |
| Soil resistivity | 120 Ω·m (assumed) | Not measured. Typical Limpopo red clay; value taken from regional geotechnical reports. Must be verified by Wenner test. |
| Surface layer | Crushed stone, 3000 Ω·m (assumed) | Visual inspection confirms stone layer exists; resistivity not measured. |
| Test records | **None since commissioning in 1998** | Deficiency D‑006 |

**Sensitivity:** If soil resistivity is actually 80 Ω·m, grid resistance drops, GPR improves, but the hazard is lower. If resistivity is 200 Ω·m, touch potentials exceed IEEE 80 limits even more severely. The earthing report uses 120 Ω·m as baseline with ±30 % sensitivity.

---

## 9. LIGHTNING AND SURGE ARRESTER DATA

| Parameter | Value | Source |
|-----------|-------|--------|
| Ground flash density (Ng) | 12 flashes/km²/year | SANS 10313 / IEC 62305 lightning ground flash density map for Limpopo |
| Substation collection area | 0.04 km² | Equivalent radius 113 m, based on 40 m × 30 m footprint plus 100 m perimeter for overhead lines |
| 33 kV surge arrester rating | Uc = 30 kV, In = 10 kA, Class 2 | Nameplate on one surviving arrester (two failed units discarded, rating assumed identical) |
| Failure history | 2 failures in last 3 years | Municipal maintenance logs |

**Finding:** The combination of high Ng and degraded earthing (D‑006) increases arrester energy stress beyond rated capacity. This mechanism is explored in Section 5.

---

## 10. SSEG (SOLAR) ASSUMPTIONS

| Parameter | Value | Source |
|-----------|-------|--------|
| Feeder with SSEG | F3 only | Municipal SSEG register (2025) — 38 rooftop installations, combined capacity 1.2 MVA |
| Individual inverter size | 3–5 kVA typical | Register data |
| Inverter fault contribution | 1.2 × rated for 3 cycles | NRS 097‑2‑1:2024 default for inverter‑based generation |
| Anti‑islanding protection | Required per NRS 097 | Verified from a sample of 5 inverter compliance certificates |

These values feed the OpenDSS model in Section 6 to assess coordination degradation.

---

## 11. STANDARDS REFERENCED

- NRS 034‑1: Electricity distribution — Protection settings and coordination
- NRS 047: Electricity distribution — SCADA and communication systems
- NRS 097‑2‑1: Grid connection of embedded generation — Small‑scale embedded generation
- IEC 60255‑151: Measuring relays and protection equipment — Functional requirements for over/under current protection
- IEC 60076‑1: Power transformers — General
- IEC 61850: Communication networks and systems for power utility automation
- IEC 62305‑2: Protection against lightning — Risk management
- IEEE 80: Guide for safety in AC substation grounding
- SANS 10313: Protection against lightning — Physical damage to structures and life hazard

---

## 12. DOCUMENT CONTROL

| Revision | Date | Author | Changes |
|----------|------|--------|---------|
| R0 | 2026‑06‑10 | Protection Engineer | Initial issue for internal review |

**Next review due:** After field verification of CT ratio (D‑001) and earth grid test (D‑006), or by 2026‑12‑10, whichever comes first.
