# AshleyFabian_2025-0773_STP_RootClaim_P1

## Ataque STP Root Claim — Manipulación del Root Bridge
**Estudiante:** Ashley Fabian  
**Matrícula:** 2025-0773  
**Práctica:** P1  
**Asignatura:** Seguridad en Redes  
**Plataforma:** GNS3 — Kali Linux  

---

## Descripción

Este repositorio contiene el script y la documentación técnica del ataque STP Root Claim. El atacante envía BPDUs con prioridad 0 para reclamar el rol de Root Bridge en la red, alterando la topología lógica L2, causando reconvergencia en todos los switches y posicionándose en el camino del tráfico.

---

## Contenido del repositorio

| Archivo | Descripción |
|---|---|
| `AshleyFabian_2025-0773_STP_RootClaim_P1.py` | Script del ataque |
| `AshleyFabian_2025-0773_Informe_STP_RootClaim_P1.pdf` | Documentación técnica profesional |

---

## Topología de red

| Dispositivo | IP | Conexiones |
|---|---|---|
| R1 (CSR1000v) | 25.7.73.1/24 | Gi1 → SW1 Gi0/0 |
| SW1 (vIOS L2) | 25.7.73.2/24 | Gi0/1→SW2, Gi0/2→SW3 |
| SW2 (vIOS L2) | 25.7.73.3/24 | Gi0/0→SW1, Gi0/1→PC1, Gi0/2→SW3 |
| SW3 (vIOS L2) | 25.7.73.4/24 | Gi0/0→SW1, Gi0/1→Kali, Gi0/2→SW2 |
| Kali Linux | 25.7.73.50/24 | eth0 → SW3 Gi0/1 |
| PC1 (VPCS) | 25.7.73.20/24 | eth0 → SW2 Gi0/1 |

**Red:** 25.7.73.0/24 (basada en matrícula 2025-0773)  
**STP:** PVST habilitado en SW1, SW2 y SW3

---

## Uso del script

```bash
# Ejecutar el ataque (continuo)
sudo python3 AshleyFabian_2025-0773_STP_RootClaim_P1.py -i eth0

# Verificar reconvergencia en los switches
SW1# show spanning-tree vlan 1
SW2# show spanning-tree vlan 1
SW3# show spanning-tree vlan 1

# Parámetros disponibles
# -i  Interfaz de red
# -c  Cantidad de BPDUs (0=continuo)
# -d  Delay entre BPDUs en segundos (default: 1)
# -p  Prioridad del bridge falso (default: 0)
```

---

## Evidencia del ataque

- SW3 muestra Kali como Root Bridge con prioridad 0
- SW1 y SW2 reconvergen hacia Kali
- Root Port de SW3 cambia a Gi0/1 (hacia Kali)

---

## Contra-medida

```
SW3(config)# interface GigabitEthernet0/1
SW3(config-if)# spanning-tree bpduguard enable

# Resultado: puerto Gi0/1 entra en err-disabled
# SW1 recupera el rol de Root Bridge
```

---

## Video de demostración

🎬 [Ver video en YouTube](https://youtu.be/7DFTso8LxRw?si=Udm5RgDB0isuHoW9)

> El video muestra el ataque en funcionamiento y la aplicación de la contra-medida.

---

## Requisitos

- Kali Linux
- Python 3.6+
- Scapy: `sudo apt install python3-scapy`
- GNS3 con CSR1000v y 3x vIOS L2
- Ejecutar como root
