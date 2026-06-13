# 33/11 kV Brownfield Substation Protection Review
### Musina Municipal Substation — Limpopo, South Africa

This project is a fully simulated protection engineering review of an ageing 33/11 kV municipal substation, built entirely on Linux using open-source tools at zero cost. It models a realistic brownfield scenario serving 9,000 customers including a hospital, water treatment plant, CBD, and a residential area with significant rooftop solar penetration under NRS 097-2-1. The simulation is grounded in a real-world trigger: a 51-minute simultaneous outage on critical load feeders, traced to a complete absence of protection coordination — every relay on the 11 kV network was set identically with no grading between them.

The simulated review covers network reconstruction from partial drawings, fault level studies under maximum and minimum source infeed, relay coordination from scratch using IEC 60255 IDMT curves, transformer differential and REF protection calculations, earthing and lightning SPD analysis against IEEE 80 and SANS 10313, SSEG impact quantification using OpenDSS, and an IEC 61850 GOOSE trip simulation with live Wireshark packet capture. A full deficiency register with risk ratings, root cause analysis, and a phased upgrade roadmap concludes the work.

Every result, plot, and calculation is reproducible on any Linux machine with no licensed software required.

**Limitations:** pandapower and OpenDSS lack the integrated protection coordination and transient stability modules found in commercial platforms such as DIgSILENT PowerFactory or ETAP, which would allow dynamic simulation and full IEC 61850 SCL validation within a single validated environment — the natural next step for utility-grade work.

**Standards:** NRS 034 | NRS 047 | NRS 097-2-1 | IEC 60255 | IEC 61850 | IEEE 80 | SANS 10313
**Tools:** Python | pandapower | OpenDSS | Scapy | Wireshark | tshark
**Budget:** ZAR 0.00 | Platform: Linux
