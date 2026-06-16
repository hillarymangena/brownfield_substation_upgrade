# Fault Level Study Report
## Musina 33/11 kV Brownfield Substation Protection Review

**Document ID:** MUS‑RPT‑002‑R0  
**Date:** 2026‑06‑10  

### 1. Executive Summary

Three‑phase and earth fault currents have been calculated for max and min infeed scenarios on the Musina 33/11 kV network. The fault current attenuation profile along each 11 kV feeder reveals that a close‑in fault on F3 produces approximately 6.2 kA at the 11 kV busbar, a current value seen identically by all feeder relays due to the lack of directional blocking and identical TMS settings. This confirms the root cause of the 51‑minute hospital outage as simultaneous tripping caused by ungraded CDG relays.

### 2. Fault Current Summary

| Bus               | Ik’’ max (kA) | Ik’’ min (kA) | Ratio max/min |
|-------------------|---------------|---------------|---------------|
| Bus_33kV_Incomer  | 7.0           | 3.1           | 2.25          |
| Bus_11kV_Main     | 6.2           | 2.8           | 2.21          |
| Bus_F1_Hospital   | 1.9           | 0.87          | 2.18          |
| Bus_F2_CBD        | 2.4           | 1.09          | 2.20          |
| Bus_F3_Residential| 1.85          | 0.83          | 2.23          |
| Bus_F4_Industrial | 2.1           | 0.95          | 2.21          |

### 3. Earth Fault Blindness

The 11 kV system is resistance‑earthed via a 300 A NER. Earth fault secondary current at a 300/1 CT is 1.0 A, below the typical CDG‑11 plug setting of 1.25 A. Therefore, **phase overcurrent relays cannot detect high‑impedance earth faults**. This is a safety deficiency (D‑004). The incident fault was therefore a low‑impedance fault (3‑phase or phase‑phase) that did produce enough current to operate the overcurrent relays.

### 4. Overreach Mechanism

The fault current attenuation profile shows that for a fault near the 11 kV busbar on F3, all four feeder relays experience approximately the same fault current (6.2 kA). With identical TMS settings (0.1) and no directional blocking, F1, F2, and F3 all trip simultaneously. The instantaneous element (if enabled) would make this even faster. This is the primary root cause of the incident (D‑002, D‑003).

### 5. Recommendations

- Perform a full protection coordination study (Section 3) to assign graded TMS values.
- Disable instantaneous elements on all CDG relays until coordination is verified.
- Install or commission SEF protection on all feeders.

**Prepared by:** Mangena  
**Next step:** Section 3 — Protection Coordination



