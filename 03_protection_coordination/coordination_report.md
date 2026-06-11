# Protection Coordination Report
## Musina 33/11 kV Brownfield Substation Protection Review

**Document ID:** MUS‑RPT‑003‑R4  
**Date:** 2026‑06‑11  
**Revision:** R4 (final I>> philosophy: non‑directional feeder omitted, incomer window, directional F1)

### 1. Executive Summary
The original CDG‑11 settings gave zero grading (all feeders TMS = 0.1), the direct cause of the 51‑minute hospital outage. Correct IDMT settings with a 0.35 s CTI restore full selectivity. Instantaneous element analysis shows that non‑directional feeder I>> cannot be applied (busbar overreach), so it is deliberately omitted. The 33 kV incomer can safely host a non‑directional I>> set between the worst‑case feeder fault and the busbar fault level, giving fast busbar protection. The SEL‑351S on F1 is recommended to have a directional I>> enabled immediately to provide fast tripping for close‑in faults on the critical hospital feeder.

### 2. Original Settings — Failure Mode
| Bay     | Relay  | Is (A) | TMS  | I>> |
|---------|--------|--------|------|-----|
| F1      | CDG‑11 | 300    | 0.10 | –   |
| F2      | CDG‑11 | 300    | 0.10 | –   |
| F3      | CDG‑11 | 225    | 0.10 | –   |
| F4      | CDG‑11 | 300    | 0.10 | –   |
| Incomer | CDG‑11 | 120    | 0.15 | –   |

All feeder relays saw the same 6.2 kA for an F3 near‑end fault and tripped simultaneously (confirmed by TCC plot).

### 3. Corrected IDMT Settings
| Bay     | Is (A) | TMS    | t at 6.2 kA (s) |
|---------|--------|--------|------------------|
| F3      | 225    | 0.075  | 0.15             |
| F1 / F2 | 300    | 0.125  | 0.50             |
| Incomer | 120    | 0.225  | 0.85             |

### 4. Instantaneous Element Assessment

**Non‑directional feeder I>>**  
The 11 kV busbar fault is 6.2 kA, identical to the near‑end fault of any feeder. To avoid overreach, I>> must be > 1.25 × 6.2 kA = 7.75 kA — a value no feeder fault can reach. Non‑directional I>> is therefore not applied on the feeders. **D‑003 closed.**

**Incomer I>> (33 kV side)**  
The incomer sees the busbar fault (6.2 kA at 11 kV → 2.07 kA at 33 kV) and the worst feeder fault (F2 far end, 2.4 kA at 11 kV → 800 A at 33 kV). The worst feeder fault referred to 33 kV is actually the maximum of all feeder‑end faults referred: max(1950,2400,1850,2100) × (11/33) = 800 A.  
I>> setting = 1.25 × 800 A = **1000 A** primary at 33 kV.  
This lies below the busbar fault level (2.07 kA) and above any feeder‑through fault. A busbar fault causes an instantaneous incomer trip; feeder faults remain on IDMT grading.

**Directional I>> on F1 (SEL‑351S)**  
The SEL‑351S is configured with a forward directional element (busbar → feeder). This allows an I>> setting of 1.25 × F1 far‑end fault = 1.25 × 1950 A = **2438 A** primary. Only faults inside F1 cause an instantaneous trip; busbar faults are ignored. This is justified by the hospital and water treatment plant criticality and can be implemented immediately — the SEL‑351S hardware already supports it.

### 5. Deficiency Status
- **D‑002** (no coordination): **CLOSED** — graded settings provided.
- **D‑003** (instantaneous overreach): **CLOSED** — non‑directional feeder I>> deliberately omitted; incomer and directional F1 I>> correctly applied.

**Implementation cost:** ZAR 15 000 (injection test, relay re‑setting for TMS and incomer I>>, plus SEL‑351S directional element configuration).

**Prepared by:** Protection Engineer, Limpopo Municipality  
**Next step:** Transformer protection (Section 4)
