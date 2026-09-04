# use-simple: comp.compilers replay (26/09/04)

- input: yyy.mbox (tpd-21), 33,814 messages, 1988-2013
- one signed post per message, ~3 kB payloads, OPEN chain
- 13,890 distinct users (one ed25519 key each, lazy keygen)
- zero clamps: the sorted archive replays as-is
- freechains: 260902-snapshots build (tip file + K-anchors)

| N     | post avg | users  | packed | sweep |
|-------|----------|--------|--------|-------|
|  5000 | 0.137s   |  2,867 |  15 MB |  5.3s |
| 10000 | 0.246s   |  5,255 |  30 MB |  8.9s |
| 15000 | 0.361s   |  7,530 |  44 MB | 12.6s |
| 20000 | 0.482s   |  9,784 |  59 MB | 17.5s |
| 25000 | 0.610s   | 11,781 |  75 MB | 23.6s |
| 30000 | 0.748s   | 13,182 |  91 MB | 31.3s |

- total: 4h34m (16,472s); growth LINEAR (~0.12s per 5k)
- vs chat sim at 30k (0.63s): +19% -- the 14k-member ledger
  (vs 2k) outweighs the payload bytes, which ride hash-object
- tpd-21 checks: "5000 users" at 10k msgs -> measured 5,255;
  "3kB per message" holds (payload = full record)
