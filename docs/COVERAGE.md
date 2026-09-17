# Infrastructure coverage — development pack 2.0.0

## Recognition catalogue

608 infrastructure signatures combine the original explicit series, broad product signatures and the wireless/service expansion below. Series are not distinct software drivers, and recognition never establishes credentials, physical links, host/guest ownership or universal firmware compatibility.

| Manufacturer | Role | Explicit series | Reference |
| --- | --- | ---: | --- |
| Cisco | switch | 44 | [Manufacturer](https://www.cisco.com/c/en/us/products/switches/index.html) |
| Aruba | switch | 26 | [Manufacturer](https://www.arubanetworks.com/products/switches/) |
| Juniper | switch | 29 | [Manufacturer](https://www.juniper.net/us/en/products/switches.html) |
| Alcatel-Lucent Enterprise | switch | 14 | [Manufacturer](https://www.al-enterprise.com/en/products/switches) |
| Extreme | switch | 23 | [Manufacturer](https://www.extremenetworks.com/products/switches) |
| Ruckus | switch | 12 | [Manufacturer](https://www.ruckusnetworks.com/products/ethernet-switches/) |
| Dell | switch | 24 | [Manufacturer](https://www.dell.com/en-us/dt/networking/index.htm) |
| HPE | switch | 13 | [Manufacturer](https://www.hpe.com/us/en/networking.html) |
| H3C | switch | 17 | [Manufacturer](https://www.h3c.com/en/Products_and_Solutions/InterConnect/Switches/) |
| Huawei | switch | 19 | [Manufacturer](https://e.huawei.com/en/products/switches) |
| Arista | switch | 17 | [Manufacturer](https://www.arista.com/en/products) |
| Fortinet | switch | 12 | [Manufacturer](https://www.fortinet.com/products/ethernet-switches) |
| NETGEAR | switch | 6 | [Manufacturer](https://www.netgear.com/business/wired/switches/) |
| MikroTik | switch | 12 | [Manufacturer](https://mikrotik.com/products/group/switches) |
| Allied Telesis | switch | 11 | [Manufacturer](https://www.alliedtelesis.com/us/en/products/switches) |
| Palo Alto Networks | firewall | 30 | [Manufacturer](https://www.paloaltonetworks.com/network-security/next-generation-firewall) |
| Cisco | management | 9 | [Manufacturer](https://www.cisco.com/c/en/us/products/wireless/wireless-lan-controller/index.html) |
| Ruckus | management | 6 | [Manufacturer](https://www.ruckusnetworks.com/products/network-control-and-management/) |
| HPE | server | 13 | [Manufacturer](https://www.hpe.com/us/en/servers/proliant-dl-servers.html) |
| Dell | server | 17 | [Manufacturer](https://www.dell.com/en-us/shop/servers-storage-and-networking/sf/poweredge) |
| Lenovo | server | 9 | [Manufacturer](https://www.lenovo.com/us/en/servers-storage/servers/) |
| Cisco | server | 7 | [Manufacturer](https://www.cisco.com/c/en/us/products/servers-unified-computing/index.html) |
| HPE | storage | 11 | [Manufacturer](https://www.hpe.com/us/en/storage.html) |
| Dell | storage | 11 | [Manufacturer](https://www.dell.com/en-us/dt/storage.htm) |
| NetApp | storage | 15 | [Manufacturer](https://www.netapp.com/data-storage/) |
| QNAP | storage | 14 | [Manufacturer](https://www.qnap.com/en/product/) |
| Synology | storage | 8 | [Manufacturer](https://www.synology.com/en-us/products) |
| APC | management | 4 | [Manufacturer](https://www.se.com/us/en/work/products/product-launch/local/apc/) |
| Eaton | management | 6 | [Manufacturer](https://www.eaton.com/us/en-us/products/backup-power-ups-surge-it-power-distribution.html) |
| Vertiv | management | 5 | [Manufacturer](https://www.vertiv.com/en-us/products-catalog/) |

## New collection families

| Software family | Core evidence | Validation |
| --- | --- | --- |
| Arista EOS | Identity, interfaces, VLANs, LLDP, MAC tables, ARP | Synthetic command-to-topology tests; live verification pending |
| Ruckus / Brocade FastIron | Identity, interfaces, VLANs, LLDP, MAC tables, ARP | Synthetic command-to-topology tests; live verification pending |
| HPE / H3C Comware | Identity, interfaces, VLANs, LLDP, MAC tables, ARP | Synthetic command-to-topology tests; live verification pending |
| Huawei VRP switches | Identity, interfaces, VLANs, LLDP, MAC tables, ARP | Synthetic command-to-topology tests; live verification pending |

These collectors require desktop engine 2. New model series using existing supported software families use those collectors only after device identity confirms the software family. Other products are recognition-only inventory until an appropriate collector is implemented. Configuration backups, stack/LACP membership, routing and health collection for the four new families are not included.

Useful immediate coverage includes ESXi/Proxmox recognition from the existing broad rules, HPE/Dell/Lenovo server series, iLO/iDRAC broad rules, QNAP/Synology/NetApp/Dell storage, APC/Eaton/Vertiv power, and broader campus-switch identification. The catalogue does not identify an unknown device solely from a VMware MAC or a generic certificate.

## Sources for the new read plans

- [Arista LLDP manual](https://www.arista.com/en/um-eos/eos-link-layer-discovery-protocol)
- [Ruckus FastIron command reference](https://docs-be.commscope.com/bundle/fastiron-08030-commandref/raw/resource/enus/fastiron-08030-commandref.pdf)
- [H3C support documentation](https://www.h3c.com/en/Support/Resource_Center/)
- [Huawei switch interface command reference](https://info.support.huawei.com/enterprise/en/doc/EDOC1100333403/cdd85713/basic-interface-configuration-commands)

Sources describe product families and command syntax; they are not evidence that these collectors have been exercised on every model.

## Wireless controllers and network services

The 135 rules maintained in `tools/expand_services.py` add 115 entries and refine 20 existing entries. They cover recognition/inventory, not new CLI/API collectors. Existing ArubaOS controller collection, ClearPass backup and NIOS collection remain separate capabilities. New recognition never grants a collector, backup operation, credentials, HA membership or physical links.

| Category | Products covered |
| --- | --- |
| Wireless controllers | Cisco AireOS and Catalyst 9800/CW9800; Ruckus SmartZone/vSZ/ZoneDirector; ExtremeCloud IQ Controller, IdentiFi and VX/NX platforms; FortiWLC; Huawei AC/AirEngine controllers; H3C WX; TP-Link Omada; UniFi Network Application |
| NAC / authentication | Cisco ISE and SNS-3700 appliances; legacy ACS; Forescout CounterACT/eyeSight/eyeControl; PacketFence; Portnox CORE; FortiAuthenticator; Ivanti/Pulse Policy Secure |
| DDI | BlueCat Address Manager, DNS/DHCP Server, Integrity and Micetro; EfficientIP SOLIDserver and DNS Guardian |
| Management | Catalyst/DNA Center, Prime Infrastructure/Network Registrar, AirWave, Central On-Premises, Extreme Site Engine, FortiManager/FortiAnalyzer and NSX Manager |
| ADC / security services | F5 BIG-IP/BIG-IQ/VELOS/rSeries, A10 Thunder, NetScaler, Kemp LoadMaster, Radware, Avi/NSX load balancers, FortiADC/FortiWeb |
| Out-of-band management | Opengear Operations Manager/Console Manager/Lighthouse, Lantronix SLC/LM and Vertiv Avocent ACS |

Each row includes an official reference. Software identities cover virtual deployments without using a VMware MAC as proof. An SNS appliance identity alone does not prove ISE is installed; it is kept as an access-control appliance. Generic RADIUS/DHCP services and acronyms are insufficient. SaaS products are not fabricated as local devices. Detection requires direct product evidence from the endpoint or its neighbour advertisement.

Controller identities take precedence over generic Cisco IOS-XE switching hints. TP-Link Omada Controller is not a router. AP product signatures remain under the existing fixed-equipment policy. Conflicting products and documentation pages remain unresolved. These changes add no network requests or authentication attempts.

Regenerate with `python tools/expand_catalogue.py` (both lists) or `python tools/expand_services.py` (services only). Run the public validation suite before signing. Desktop engine 2 raises the infrastructure rule limit to 1,024; fixed equipment remains capped at 512 and the complete pack at 2 MiB. The public engine-1 stable channel has not been changed.
