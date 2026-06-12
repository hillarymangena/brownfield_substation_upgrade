#!/usr/bin/env python3
"""
Hardwired vs GOOSE trip timing comparison.
Musina 33/11 kV Brownfield Protection Review — Section 7.
"""
import pandas as pd

print("=" * 70)
print(" HARDWIRED vs GOOSE TRIP TIMING — Musina 33/11 kV")
print("=" * 70)

timing = [
    # (Action, Hardwired ms, GOOSE ms, Notes)
    ("Relay detects fault (overcurrent pickup)",
     "20–40", "20–40", "Dominant term — identical for both"),
    ("Relay contact closes / GOOSE T1 frame sent",
     "5–10",  "2",     "Hardwired: CDG disc + contact | GOOSE: T1=2ms"),
    ("Trip coil energised",
     "2",     "1",     "Wire propagation | Ethernet <1ms + IED output ~1ms"),
    ("CB opens (mechanical)",
     "50–80", "50–80", "Vacuum CB: 50ms | Oil CB: 80ms — identical"),
    ("─── TOTAL FAULT CLEARING ───",
     "77–132","73–123","GOOSE saves ~4ms — CB mechanical dominates"),
    ("",      "",      "", ""),
    ("Loss-of-GOOSE declared (TTL expiry)",
     "N/A",   "4000",  "If no frame in 4s, subscriber triggers fallback"),
    ("Scheme change (add interlock)",
     "Rewire", "Config file", "GOOSE: no copper change, edit SCD only"),
    ("Event log granularity",
     "Flag only", "1ms timestamp", "GOOSE via MMS: full waveform + sequence of events"),
    ("Remote SCADA visibility",
     "9600 baud modem", "100 Mbit Ethernet", "Current Musina SCADA replaced entirely"),
]

df = pd.DataFrame(timing,
                  columns=["Action", "Hardwired", "GOOSE", "Notes"])
print(df.to_string(index=False))

print("\n" + "=" * 70)
print(" KEY FINDINGS")
print("=" * 70)
print("""
  1. GOOSE does NOT dramatically improve fault clearing speed.
     The CB mechanical time (50-80ms) dominates — GOOSE saves ~4ms.
     Selling IEC 61850 on speed alone is technically incorrect.

  2. The real value for Musina municipality is:
     a. Replace 9600 baud modem SCADA with 100Mbit Ethernet MMS
        → real-time fault data, sequence of events, waveform capture
        → the 51-minute outage response time drops to <5 minutes
     b. Flexible interlocking — add/change bus coupler permissives
        by editing the SCD file, not rewiring the panel
     c. IED health monitoring over MMS — detect relay failures
        before they become protection gaps (the empty bay problem)

  3. For this substation, recommended phasing:
     Phase 1 (immediate): SEL-351S on F1 → MMS over Ethernet to
                          municipal control room. Cost: ~ZAR 45,000.
     Phase 2 (3 years):   Replace CDG relays on F2-F4 with numeric
                          IEDs. Full station bus. Cost: ~ZAR 380,000.
     Phase 3 (5 years):   Process bus (merging units, GOOSE trips).
                          Full IEC 61850-9-2 sampled values.
                          Cost: ~ZAR 850,000.
""")

print("=" * 70)
print(" COST-BENEFIT SUMMARY (ZAR)")
print("=" * 70)
costs = [
    ("Phase 1: SEL-351S MMS + fibre + managed switch",   "45,000",  "Immediate"),
    ("Phase 2: 3× numeric IEDs + station bus",           "380,000", "Year 3"),
    ("Phase 3: Full process bus + merging units",        "850,000", "Year 5"),
    ("Current annual arrester replacement (D-007)",      "12,000",  "Recurring"),
    ("Cost of one 51-min hospital outage (NERSA penalty)","~150,000","Per event"),
]
df2 = pd.DataFrame(costs, columns=["Item", "ZAR", "Timeline"])
print(df2.to_string(index=False))
print("\n  Phase 1 pays for itself after one avoided NERSA penalty event.")
