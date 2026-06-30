Networking Terms (Day 8)
ping google.com
tracert google.com
nslookup google.com
nslookup google.com 8.8.8.8

# Day 8 — Networking Fundamentals

## Task
Run ping, tracert, and nslookup commands; document the output and explain 
IP address, port, and DNS in my own words.
---
## 1. Ping
### Command
ping google.com

### Output
Pinging google.com [2404:6800:4000:1015::8a] with 32 bytes of data:
Reply from 2404:6800:4000:1015::8a: time=81ms
Reply from 2404:6800:4000:1015::8a: time=79ms
Reply from 2404:6800:4000:1015::8a: time=71ms
Reply from 2404:6800:4000:1015::8a: time=132ms
Ping statistics for 2404:6800:4000:1015::8a:
Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
Minimum = 71ms, Maximum = 132ms, Average = 90ms

### Observation
- google.com resolved to IPv6 address `2404:6800:4000:1015::8a`.
- All 4 packets received, 0% packet loss — connection is stable.
- Average round-trip time: 90ms.

---
## 2. Tracert
### Command
tracert google.com

### Output
Tracing route to google.com [2404:6800:4000:1015::8b]
over a maximum of 30 hops:
1     3 ms     2 ms     3 ms  2409:40f4:3004:dca5::7d
2     *        *        *     Request timed out.
3    92 ms    40 ms    22 ms  2405:200:5218:23:3925::ff22
4     *        *        *     Request timed out.
5     *        *        *     Request timed out.
6   193 ms    49 ms    62 ms  2405:200:801:4a00::e8
7     *        *        *     Request timed out.
8     *        *        *     Request timed out.
9   177 ms    49 ms    43 ms  2404:6800:8202:440::1
10   563 ms   885 ms    59 ms  2404:6800:8202:440::1
11   127 ms   272 ms   250 ms  2001:4860:0:1::564a
12    59 ms    24 ms    31 ms  2001:4860:0:1::882a
13     *        *     1809 ms  2001:4860::c:4004:53be
14    70 ms    53 ms    48 ms  2001:4860::9:4002:d931
15  2521 ms   899 ms   222 ms  2001:4860:0:1::7747
16   721 ms     *       53 ms  2001:4860:0:1::712e
17     *        *        *     Request timed out.
18     *        *        *     Request timed out.
19     *        *        *     Request timed out.
20     *        *        *     Request timed out.
21     *        *        *     Request timed out.
22     *        *        *     Request timed out.
23    61 ms    55 ms    74 ms  cn-in-f139.1e100.net [2404:6800:4000:1015::8b]
Trace complete.

### Observation
- Took 23 hops to reach Google's server.
- Several hops timed out (`*`) — some routers don't reply to traceroute 
  probes, this is normal and not an error.
- Final hop `cn-in-f139.1e100.net` confirms arrival at Google's network 
  (1e100.net is Google's own domain used for reverse DNS).
- Response times varied across hops (e.g., hop 15 ranged from 222ms to 
  2521ms), which can indicate temporary congestion at that point in the path.

---
## 3. Nslookup
### Command (default DNS)
nslookup google.com

### Output
DNS request timed out.
timeout was 2 seconds.
Server:  UnKnown
Address:  10.127.121.183
DNS request timed out.
*** Request to UnKnown timed-out

### Command (using Google's public DNS)
nslookup google.com 8.8.8.8

### Output
Server:  dns.google
Address:  8.8.8.8
Non-authoritative answer:
Name:    google.com
Addresses:  2404:6800:4007:833::200e
142.251.223.238

### Observation
- Default DNS server (`10.127.121.183`, a local network DNS) timed out 
  and failed to resolve the query.
- Switching to Google's public DNS (`8.8.8.8`) successfully resolved 
  google.com to two addresses: an IPv4 (`142.251.223.238`) and an IPv6 
  (`2404:6800:4007:833::200e`).
- This shows DNS resolution depends on which DNS server is being used — 
  if one fails, a different one can still succeed.

---

## Concepts Explained (in my own words)

### IP Address
An IP address is the unique identifier for a device on a network — like 
a home address. When I pinged google.com, it resolved to 
`2404:6800:4000:1015::8a` (IPv6) — this is the specific address of 
Google's server that my computer sent packets to in order to reach it.

### Port
A port is like an apartment number inside that address — it identifies 
which specific application or service on a device should handle a 
request (for example, port 443 for HTTPS, port 80 for HTTP). My commands 
today didn't show ports directly, but every request to google.com from 
a browser goes to port 443 behind the scenes.

### DNS
DNS (Domain Name System) converts a human-readable domain name into an 
IP address that computers can use to communicate. I saw this directly: 
when my default DNS server timed out, I used `nslookup` with Google's 
public DNS (8.8.8.8) and got back the actual IP addresses for 
google.com. This proved DNS works like a directory — translating names 
into addresses — and that resolution depends on having a working DNS 
server to ask.

---

## Key Terms

- **IP Address** — Unique address identifying a device on a network.
- **Port** — Number identifying which service/app on a device receives data.
- **DNS** — System that translates domain names into IP addresses.
- **Ping** — Tests if a host is reachable and measures round-trip latency.
- **Tracert** — Shows the path (hops/routers) packets take to a destination.
- **Hop** — One intermediate router a packet passes through.
- **TTL** — Limits how many hops a packet can take before being dropped.
- **Packet Loss** — Percentage of packets that never got a reply.
- **TCP** — Reliable, ordered delivery protocol (e.g., file downloads, web pages).
- **UDP** — Fast, no-guarantee delivery protocol (e.g., video calls, streaming).
- **IPv4 vs IPv6** — IPv4 is the older 32-bit address format; IPv6 is the 
  newer 128-bit format with vastly more available addresses.