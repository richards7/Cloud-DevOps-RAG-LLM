# Networking Fundamentals

## OSI model (simplified, the layers that come up most)
1. **Physical**: cables, signals.
2. **Data Link**: MAC addresses, switches.
3. **Network**: IP addresses, routing (this is where "the internet" mostly happens).
4. **Transport**: TCP/UDP — ports, reliability.
5. **Application**: HTTP, DNS, SSH — what applications actually speak.

## TCP vs UDP
- **TCP**: connection-oriented, reliable, ordered delivery, retransmits lost packets —
  used for HTTP, SSH, most application traffic where correctness matters.
- **UDP**: connectionless, no delivery guarantee, lower overhead — used for DNS, video
  streaming, gaming, where speed matters more than guaranteed delivery.

## IP addressing basics
- **IPv4**: 32-bit addresses (e.g. `192.168.1.1`), the most common format still in use.
- **Private vs public IP**: private ranges (`10.0.0.0/8`, `172.16.0.0/12`,
  `192.168.0.0/16`) aren't routable on the public internet — used inside VPCs/local
  networks; a NAT gateway lets private-IP resources reach the internet outbound.
- **CIDR notation**: `10.0.0.0/24` means the first 24 bits are the network portion,
  leaving 8 bits (256 addresses) for hosts — this is how VPC/subnet sizing is
  expressed in every cloud provider.

## DNS (Domain Name System)
Translates human-readable domain names to IP addresses.
```bash
dig example.com          # detailed DNS lookup
nslookup example.com       # simpler lookup
```
Common record types: **A** (domain → IPv4), **AAAA** (→ IPv6), **CNAME** (alias to
another domain), **MX** (mail server), **TXT** (arbitrary text, often used for domain
verification).

## Ports (the ones that come up constantly)
- 22 — SSH
- 80 — HTTP
- 443 — HTTPS
- 3306 — MySQL
- 5432 — PostgreSQL
- 6379 — Redis
- 8080 — common alternate HTTP port for dev/apps

## Load balancing concepts
- **Layer 4 (transport)**: routes based on IP/port, faster, protocol-agnostic (e.g.
  AWS NLB).
- **Layer 7 (application)**: routes based on HTTP content — path, headers, hostname
  (e.g. AWS ALB, Nginx) — enables smarter routing but with slightly more overhead.
- **Algorithms**: round-robin (rotate evenly), least connections (send to the least
  busy server), IP hash (same client consistently hits the same server — useful for
  session stickiness).

## Common errors & fixes
- **"Connection refused"**: the port is reachable but nothing is listening — check the
  service is actually running and bound to the right interface (`0.0.0.0` not just
  `127.0.0.1` if it needs to accept external connections).
- **"Connection timed out"**: usually a firewall silently dropping packets, or a
  routing issue — check security groups/NACLs and route tables.
- **DNS not resolving**: check with `dig`/`nslookup`; propagation after a DNS change
  can take time (respect the record's TTL).
- **Intermittent latency spikes**: check for DNS lookup overhead (cache DNS results
  where appropriate) and connection pool exhaustion under load.
