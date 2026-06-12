#!/usr/bin/env python3
"""
GOOSE Subscriber — Musina 33/11 kV Brownfield Protection Review
Simulates a bay controller / CB driver IED receiving the F1 trip GOOSE.
Demonstrates: state change detection, loss-of-GOOSE watchdog, TTL monitoring.

In a real substation:
  - This runs inside a merging unit or bay controller IED
  - On trip assertion, a hardware output drives the CB trip coil (~2ms)
  - Loss-of-GOOSE after TTL expiry triggers a configurable fallback action
"""

import struct
import time
import sys
import threading
from scapy.all import sniff, Ether

GOOSE_ETHERTYPE = 0x88B8
TTL_MS          = 4000   # timeAllowedToLive — declared in publisher

# Shared state
state = {
    "stnum":    0,
    "sqnum":    0,
    "trip":     False,
    "last_rx":  time.time(),
    "ttl_ms":   TTL_MS,
    "active":   True,
}


def decode_goose_pdu(data: bytes) -> dict:
    """
    Extract key fields from a received GOOSE PDU.
    Parses the fixed-offset header fields; allData boolean is the last byte.
    """
    if len(data) < 20:
        return {}
    try:
        appid  = struct.unpack(">H", data[0:2])[0]
        length = struct.unpack(">H", data[2:4])[0]

        # Walk inner TLV to find stNum (tag 0x86) and sqNum (tag 0x87)
        stnum, sqnum, ttl = 0, 0, TTL_MS
        idx = 8  # skip 8-byte header
        if idx < len(data) and data[idx] == 0x61:
            idx += 2  # skip wrapper tag and length
        while idx < len(data) - 3:
            tag = data[idx]
            ln  = data[idx+1]
            val = data[idx+2 : idx+2+ln]
            if tag == 0x86 and ln == 4:
                stnum = struct.unpack(">I", val)[0]
            elif tag == 0x87 and ln == 4:
                sqnum = struct.unpack(">I", val)[0]
            elif tag == 0x88 and ln == 4:
                ttl   = struct.unpack(">I", val)[0]
            idx += 2 + ln

        trip = data[-1] == 0xFF
        return {"appid": appid, "stnum": stnum, "sqnum": sqnum,
                "ttl": ttl, "trip": trip}
    except Exception:
        return {}


def watchdog_thread():
    """
    Monitors timeAllowedToLive. If no GOOSE frame received within TTL,
    declare loss-of-GOOSE — a critical alarm in a real substation.
    In IEC 61850 this triggers a configurable fallback (e.g. block reclose).
    """
    while state["active"]:
        time.sleep(0.5)
        elapsed_ms = (time.time() - state["last_rx"]) * 1000
        if elapsed_ms > state["ttl_ms"]:
            print(f"\n  *** LOSS-OF-GOOSE: No frame received for {elapsed_ms:.0f} ms "
                  f"(TTL={state['ttl_ms']} ms) ***")
            print(f"  *** FALLBACK: Block auto-reclose on F1 until comms restored ***")
            state["last_rx"] = time.time()  # reset to avoid repeated alarm


def process_goose(pkt):
    if not pkt.haslayer(Ether):
        return
    if pkt[Ether].type != GOOSE_ETHERTYPE:
        return

    data   = bytes(pkt[Ether].payload)
    fields = decode_goose_pdu(data)
    if not fields:
        return

    state["last_rx"] = time.time()
    rx_time = time.strftime('%H:%M:%S.') + f"{int(time.time()*1000)%1000:03d}"

    if fields["stnum"] != state["stnum"]:
        # State change — this is the actionable event
        prev_stnum    = state["stnum"]
        state["stnum"] = fields["stnum"]
        state["sqnum"] = fields["sqnum"]
        state["trip"]  = fields["trip"]

        print(f"\n{'─'*55}")
        print(f" [{rx_time}] STATE CHANGE DETECTED")
        print(f"  stNum:  {prev_stnum} → {fields['stnum']}")
        print(f"  sqNum:  {fields['sqnum']}")
        print(f"  trip:   {fields['trip']}")
        print(f"  TTL:    {fields['ttl']} ms")
        print(f"{'─'*55}")

        if fields["trip"]:
            print(f"  ACTION: *** TRIP — CB F1 trip coil energised ***")
            print(f"  CB mechanical opening time: ~50 ms")
            print(f"  Total fault clearing from relay pickup: ~70-90 ms")
        else:
            print(f"  ACTION: RESET — CB F1 may reclose per reclose scheme")

    else:
        # Retransmit heartbeat — update watchdog timer only
        print(f"  [hb {rx_time}] sqNum={fields['sqnum']:3d} | "
              f"stNum={fields['stnum']} | trip={fields['trip']}", end='\r')


def monitor_goose(interface: str = "lo", timeout: int = 40):
    print(f"\nGOOSE Subscriber active")
    print(f"Interface:  {interface}")
    print(f"EtherType:  0x{GOOSE_ETHERTYPE:04X}")
    print(f"TTL watch:  {TTL_MS} ms")
    print(f"Timeout:    {timeout} s")
    print(f"Waiting for GOOSE frames...\n")

    wd = threading.Thread(target=watchdog_thread, daemon=True)
    wd.start()

    sniff(iface=interface,
          filter=f"ether proto 0x{GOOSE_ETHERTYPE:04X}",
          prn=process_goose,
          store=False,
          timeout=timeout)

    state["active"] = False
    print("\nSubscriber session ended.")


if __name__ == "__main__":
    iface = sys.argv[1] if len(sys.argv) > 1 else "lo"
    monitor_goose(interface=iface)
