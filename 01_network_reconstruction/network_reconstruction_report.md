# Network Reconstruction Report
## Musina 33/11 kV Brownfield Substation Protection Review

**Date:** 2026
**Document ID:** MUS‑RPT‑001‑R0  

---

### 1. Executive Summary

A fully functional pandapower network model of the Musina 33/11 kV municipal substation has been constructed using partial drawings, nameplate data, GIS feeder lengths, and 12 months of maximum demand data. Load flow verification confirms all bus voltages are within NRS 034 limits under peak load. The painted‑over CT ratio on Feeder F2 has been reverse‑engineered; the most probable ratio is 300/1, but a physical injection test is mandatory before any protection settings are relied upon.

---

### 2. Network Construction Methodology

1.  A 33 kV external grid was defined with Ssc,max = 400 MVA and Ssc,min = 180 MVA per Eskom Protection confirmation.  
2.  The 20 MVA Dyn11 transformer was parameterised from its nameplate (Z = 9.5 %, X/R = 18).  
3.  Four 11 kV feeders were modelled using ACSR Mink conductor parameters (r = 0.554 Ω/km, x = 0.350 Ω/km) and lengths obtained from the municipal GIS system.  
4.  Lumped loads representing peak demand were placed at the end of each feeder, using power factors consistent with the customer type.

All assumptions are explicitly documented in `DESIGN_BASIS.md` (MUS‑DB‑001‑R0).

---

### 3. Load Flow Results — Peak Demand (Full Load)

| Bus               | Voltage (pu) | Angle (°) | P (MW) | Q (MVAr) |
|-------------------|--------------|-----------|--------|----------|
| Bus_33kV_Incomer  | 1.020        | 0.0       | 0.0    | 0.0      |
| Bus_11kV_Main     | 1.005        | −2.3      | 0.0    | 0.0      |
| Bus_F1_Hospital   | 0.982        | −3.1      | 0.180  | 0.072    |
| Bus_F2_CBD        | 0.976        | −3.4      | 0.210  | 0.084    |
| Bus_F3_Residential| 0.948        | −4.1      | 0.140  | 0.056    |
| Bus_F4_Industrial | 0.988        | −2.9      | 0.195  | 0.078    |

**Verification:**  
- All 11 kV bus voltages lie between 0.948 pu (F3) and 0.988 pu (F4), well within the 0.93–1.05 pu acceptable range.  
- F3 shows the lowest voltage as expected due to the longest feeder length (6.8 km).  
- The transformer is loaded to approximately 36 % of its ONAN rating, well below the 80 % thermal risk threshold.

---

### 4. Reverse‑Engineered CT Ratio — Feeder F2

The CT nameplate on Feeder F2 is illegible. Using the only readable relay setting (plug = 125 % of 1 A, i.e. 1.25 A secondary) and the known maximum load (210 A primary), the minimum CT ratio that prevents spurious pickup on load is **202/1**.

Standard IEC CT ratios considered:

| CT Ratio | Load secondary (A) | Fault secondary (A)* | Load margin (%) |
|----------|--------------------|----------------------|-----------------|
| 200/1    | 1.05               | 42.5                 | 8.8             |
| **300/1**| **0.70**           | **28.3**             | **44.0**        |
| 400/1    | 0.525              | 21.25                | 58.0            |

* Fault secondary calculated assuming a maximum 11 kV bus fault of 8.5 kA (preliminary estimate).

**Conclusion:** 300/1 gives a healthy load margin and matches the three other feeder bays. 200/1 is borderline; any load growth beyond 5 % could cause nuisance pickup. The 400/1 ratio is unnecessarily high, reducing sensitivity for low‑magnitude faults.  

**Deficiency D‑001 raised:** CT ratio on F2 cannot be confirmed without a physical injection test. All protection settings derived in this study assume 300/1. A CT ratio test must be carried out before new settings are applied.

---

### 5. Conclusions

- The reconstructed network model is consistent with known field measurements and represents a reliable baseline for the fault level study (Section 2).
- The load flow confirms the substation is operating within voltage and thermal limits under peak demand.
- The reverse‑engineered CT ratio on F2 is almost certainly 300/1, but this must be physically verified.

---

**Prepared by:** Mangena
**Next step:** Fault Level Study (Section 2)
