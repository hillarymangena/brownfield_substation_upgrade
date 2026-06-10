#!/usr/bin/env python3
"""
reconstruct_network.py
Musina 33/11 kV Municipal Substation — Network reconstruction from partial information.
Brownfield Protection Review, Limpopo Municipality.
Standards: NRS 034, IEC 60255, IEEE 80, SANS 10313.
"""

import pandapower as pp
import pandapower.shortcircuit as sc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def build_musina_network(ssc_mva=400):
    """
    Construct the pandapower network model of Musina 33/11 kV substation.
    
    Parameters
    ----------
    ssc_mva : float
        Short-circuit MVA at the 33 kV Eskom busbar (max infeed). 
        Default 400 MVA as per DESIGN_BASIS.md.
    
    Returns
    -------
    net : pandapowerNet
        Complete network ready for load flow and short-circuit studies.
    """
    net = pp.create_empty_network(f_hz=50, sn_mva=20)
    
    # ---- Busbars ----
    b_33kv = pp.create_bus(net, vn_kv=33, name="Bus_33kV_Incomer")
    b_11kv = pp.create_bus(net, vn_kv=11, name="Bus_11kV_Main")
    b_f1 = pp.create_bus(net, vn_kv=11, name="Bus_F1_Hospital")
    b_f2 = pp.create_bus(net, vn_kv=11, name="Bus_F2_CBD")
    b_f3 = pp.create_bus(net, vn_kv=11, name="Bus_F3_Residential")
    b_f4 = pp.create_bus(net, vn_kv=11, name="Bus_F4_Industrial")
    
    # ---- External grid (Eskom source) ----
    pp.create_ext_grid(net, bus=b_33kv, vm_pu=1.02,
                       s_sc_max_mva=ssc_mva, s_sc_min_mva=180,
                       rx_max=0.1, rx_min=0.1,
                       name="Eskom_Musina_Source")
    
    # ---- 20 MVA Dyn11 Transformer ----
    pp.create_transformer_from_parameters(
        net, hv_bus=b_33kv, lv_bus=b_11kv,
        sn_mva=20, vn_hv_kv=33, vn_lv_kv=11,
        vkr_percent=0.5, vk_percent=9.5,
        pfe_kw=25, i0_percent=0.5,
        shift_degree=330,  # Dyn11 = -30° = 330
        name="T1_20MVA_Dyn11"
    )
    
    # ---- 11 kV feeders (ACSR Mink) ----
    r_per_km = 0.554   # Ω/km
    x_per_km = 0.350   # Ω/km
    
    feeder_data = [
        ("F1_Hospital",    b_11kv, b_f1, 4.2, 180),
        ("F2_CBD",         b_11kv, b_f2, 3.1, 210),
        ("F3_Residential", b_11kv, b_f3, 6.8, 140),
        ("F4_Industrial",  b_11kv, b_f4, 2.9, 195),
    ]
    
    for name, fb, tb, length_km, load_kw in feeder_data:
        pp.create_line_from_parameters(
            net, from_bus=fb, to_bus=tb,
            length_km=length_km,
            r_ohm_per_km=r_per_km,
            x_ohm_per_km=x_per_km,
            c_nf_per_km=10, max_i_ka=0.3,
            name=f"Line_{name}"
        )
        pp.create_load(net, bus=tb,
                       p_mw=load_kw/1000,
                       q_mvar=(load_kw * 0.4)/1000,  # PF ~0.93, typical
                       name=f"Load_{name}")
    
    return net

if __name__ == "__main__":
    # Build and run a quick load flow for interactive verification
    net = build_musina_network()
    pp.runpp(net, algorithm='nr', calculate_voltage_angles=True, tolerance_mva=1e-8)
    print("Bus voltage results:\n", net.res_bus)
    print("\nLine loading:\n", net.res_line)
    print("\nTransformer loading:\n", net.res_trafo)
