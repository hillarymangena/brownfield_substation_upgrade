#!/usr/bin/env python3
"""
GOOSE Publisher — Musina 33/11 kV Brownfield Protection Review
Simulates an IED (SEL-351S on F1) publishing a protection trip via GOOSE.
IEC 61850-8-1: Layer 2 multicast, EtherType 0x88B8, exponential retransmit backoff.

Key IEC 61850 concepts demonstrated:
  - stNum increments on every state change (trip/reset) — subscribers act on this
  - sqNum increments on every retransmit — subscribers use this as a watchdog
  - timeAllowedToLive: if no frame received within this window, subscriber declares loss-of-GOOSE
  - Retransmit intervals: T1(2ms) T2(4ms) T3(8ms) T4(16ms) ... T0(1000ms steady state)
  - VLAN priority 4: IEC 61850 mandates high priority for GOOSE on managed switches
"""

import struct
import time
import sys
from scapy.all import Ether, sendp, raw

GOOSE_MULTICAST_DST = "01:0c:cd:01:00:01"  # IEC 61850 standard GOOSE multicast MAC
GOOSE_ETHERTYPE     = 0x88B8               # IEC 61850 GOOSE EtherType
GOOSE_APPID         = 0x0001               # Application ID — unique per GOOSE control block
VLAN_ID             = 0x000                # VLAN 0 for untagged simulation
VLAN_PRIORITY       = 4                    # IEC 61850 mandated priority for GOOSE


def encode_goose_pdu(trip: bool, sqnum: int, stnum: int,
                     goID: bytes = b"MUSINA_F1_TRIP_GoCB") -> bytes:
    """
    Encode a GOOSE PDU approximating IEC 61850-8-1 ASN.1 BER structure.
    Sufficient for Wireshark to decode with the IEC 61850 dissector.

    PDU layout:
      [APPID 2B][Length 2B][Reserved1 2B][Reserved2 2B]
      [goID tag+len+value][timestamp 8B][stNum 4B][sqNum 4B]
      [timeAllowedToLive 4B][numDatSetEntries 1B][BOOLEAN tag 1B][value 1B]
    """
    timestamp_ms = int(time.time() * 1000)

    # GOOSE PDU inner content
    inner  = b'\x80' + bytes([len(goID)]) + goID          # goID [0] IMPLICIT VisibleString
    inner += b'\x84' + b'\x08' + struct.pack(">Q", timestamp_ms)  # t [4] UtcTime
    inner += b'\x86' + b'\x04' + struct.pack(">I", stnum)  # stNum [6] UINT32
    inner += b'\x87' + b'\x04' + struct.pack(">I", sqnum)  # sqNum [7] UINT32
    inner += b'\x88' + b'\x04' + struct.pack(">I", 4000)   # timeAllowedToLive [8] UINT32 ms
    inner += b'\x8b' + b'\x04' + struct.pack(">I", 1)      # numDatSetEntries [11] UINT32

    # allData — one BOOLEAN entry
    bool_val = b'\xff' if trip else b'\x00'
    inner += b'\xab' + b'\x03' + b'\x83\x01' + bool_val   # allData [11] SEQUENCE OF

    # GOOSE PDU wrapper tag 0x61
    pdu  = b'\x61' + bytes([len(inner)]) + inner

    # GOOSE header: APPID, Length, Reserved1, Reserved2
    total_len = 8 + len(pdu)
    header = struct.pack(">HHHh", GOOSE_APPID, total_len, 0x0000, 0x0000)

    return header + pdu


def build_vlan_goose_frame(src_mac: str, pdu: bytes) -> bytes:
    """
    Build a raw Ethernet frame with 802.1Q VLAN tag and GOOSE EtherType.
    Frame: [dst 6B][src 6B][8100 2B][VLAN TCI 2B][88B8 2B][PDU]
    """
    dst  = bytes.fromhex(GOOSE_MULTICAST_DST.replace(":", ""))
    src  = bytes.fromhex(src_mac.replace(":", ""))
    vlan_tci = (VLAN_PRIORITY << 13) | VLAN_ID
    frame  = dst + src
    frame += struct.pack(">HH", 0x8100, vlan_tci)  # 802.1Q tag
    frame += struct.pack(">H", GOOSE_ETHERTYPE)
    frame += pdu
    return frame


def publish_goose(interface: str = "lo", trip: bool = True,
                  src_mac: str = "02:00:00:00:01:01"):
    """
    Publish a GOOSE trip or reset with IEC 61850 retransmit backoff.
    Retransmit schedule: 2ms, 4ms, 8ms, 16ms, 32ms, 1000ms (steady state).
    """
    stnum = 2 if trip else 1
    retransmit_ms = [2, 4, 8, 16, 32, 1000]

    state = "TRIP" if trip else "RESET"
    print(f"\n{'='*55}")
    print(f" GOOSE Publisher — {state}")
    print(f" IED:       SEL-351S F1 (Hospital feeder)")
    print(f" goID:      MUSINA_F1_TRIP_GoCB")
    print(f" APPID:     0x{GOOSE_APPID:04X}")
    print(f" Interface: {interface}")
    print(f"{'='*55}")

    t0 = time.perf_counter()

    for i, interval_ms in enumerate(retransmit_ms):
        pdu   = encode_goose_pdu(trip=trip, sqnum=i, stnum=stnum)
        frame = build_vlan_goose_frame(src_mac=src_mac, pdu=pdu)

        # Use scapy sendp with raw bytes wrapped in Ether for loopback compatibility
        eth_frame = Ether(dst=GOOSE_MULTICAST_DST, src=src_mac,
                          type=GOOSE_ETHERTYPE) / raw(pdu)
        sendp(eth_frame, iface=interface, verbose=False)

        elapsed_ms = (time.perf_counter() - t0) * 1000
        print(f"  [{elapsed_ms:7.2f} ms] sqNum={i:2d} | stNum={stnum} | "
              f"trip={trip} | next_tx={interval_ms} ms")

        time.sleep(interval_ms / 1000.0)

    print(f"\n  Burst complete. Steady-state retransmit at 1000 ms.")
    print(f"  Subscriber loss-of-GOOSE declared if no frame within 4000 ms (TTL).")


if __name__ == "__main__":
    iface = sys.argv[1] if len(sys.argv) > 1 else "lo"
    print("Simulating F1 fault detection — CDG relay pickup → SEL-351S GOOSE trip")
    time.sleep(0.5)
    publish_goose(interface=iface, trip=True)
    print("\nWaiting 3 seconds — simulating dead time / fault arc extinction...")
    time.sleep(3)
    print("Fault cleared — publishing GOOSE RESET")
    publish_goose(interface=iface, trip=False)
