# SSEG Impact Analysis Report
## Musina 33/11 kV — F3 Residential Feeder

**Document ID:** MUS‑RPT‑006‑R0  
**Date:** 2026‑06‑12  

### 1. Executive Summary
The connection of 1.2 MVA rooftop solar on F3 increases near‑end fault levels marginally but erodes the fuse‑saving coordination ratio. Without mitigation, a permanent fault on a lateral could blow the fuse before the upstream recloser operates, leading to extended outage and anti‑islanding risk.

### 2. Fault Level Comparison
| Location          | Pre‑SSEG (A) | Post‑SSEG (A) | Increase |
|-------------------|--------------|---------------|----------|
| F3 busbar (11 kV) | 6200         | 6400          | 3.2 %    |
| F3 end‑of‑feeder  | 1850         | 2070          | 11.9 %   |

### 3. Coordination Impact
- Existing coordination: F3 relay (225 A pickup, TMS 0.075) clears faults in 0.15 s at 6.2 kA.
- 100 A lateral fuse: minimum melting current for fuse saving ~400 A.
- Post‑SSEG, the end‑of‑feeder fault current increases, but the coordination margin remains acceptable for the relay; however, fuse‑saving schemes on laterals may be compromised where the fault current is less than 4× fuse rating.

### 4. Recommendation
- Implement transfer‑trip for SSEG laterals to ensure simultaneous disconnection.
- Adjust anti‑islanding settings to less than 0.2 s.
- Budget: ZAR 45 000 per lateral for communication‑based transfer‑trip.

**Prepared by:** Protection Engineer, Limpopo Municipality  
**Next step:** IEC 61850 migration (Section 7)
