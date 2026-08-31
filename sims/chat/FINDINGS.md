# Chat simulation findings (freechains.vcs, 2026-08-28..31)

- Input: `wikimedia.chat`, 155,528 messages, 2010-08-25..2012-11-01
- Sims: `chat-02.lua` (gated chain, reps/likes/begs) and
  `chat-simple.lua` (open chain, signed posts only)
- Machine: 15 GB RAM, git 2.43.0, lua 5.4
- Logs: `chat-02-raw.log`, `chat-02-sweep-summary.txt`,
  `chat-simple-1k.txt`, `chat-simple-5k.txt`,
  `chat-simple-10k.log`, `chat-simple-50k.log`

# Reference run (open chain, sweep every 5k, 50k msgs)

| N   | post avg | loose before | sweep   | pack after | KB/msg |
|-----|----------|--------------|---------|------------|--------|
| 5k  | 0.18 s   | 1.0 GB       | 77 s    | 5 MB       | 1.0    |
| 10k | 0.38 s   | 3.0 GB       | 6 min   | 15 MB      | 1.5    |
| 15k | 0.65 s   | 5.0 GB       | 12 min  | 26 MB      | 1.7    |
| 20k | 0.85 s   | 7.0 GB       | 21 min  | 44 MB      | 2.2    |
| 25k | 3.01 s   | 9.1 GB       | 31 min  | 65 MB      | 2.6    |
| 30k | 2.84 s   | 11.1 GB      | 41 min  | 82 MB      | 2.7    |
| 35k | 1.70 s   | 13.2 GB      | 54 min  | 104 MB     | 3.0    |
| 40k | 2.73 s   | 15.4 GB      | 70 min  | 126 MB     | 3.2    |
| 45k | 3.70 s   | 17.5 GB      | 87 min  | 154 MB     | 3.4    |
| 50k | 4.98 s   | 19.6 GB      | 103 min | 183 MB     | 3.7    |

- growth: post = linear floor + activity spikes;
  loose and sweep = quadratic; pack = super-linear
- totals: 29.2 h posting, 7.1 h sweeping, final pack 183 MB
- runs are deterministic: same N gives identical bytes across runs

# Latency

- per-post cost measured at N=22.5k (11 MB state, 136 authors):
    - git read blob 0.04 s, hash-object + update-ref 0.03 s
    - lua parse snapshot 0.13 s          (O(N))
    - lua serialize + write 0.47 s       (O(N), worst fixed term)
    - `ordered()` sort, twice, 0.10 s    (O(N log N))
    - `advance()` discount scan 0..3.6 s (O(A*N), A = posts in 12h)
- git is NOT the bottleneck; the state model is
- write (serialize) is ~3.6x read (parse)
- latency is NOT monotone in N: windows 25k..50k swing
  1.7..5.0 s with chat activity (A), not with N
- sweeping does not affect post time (loose count irrelevant)

# Disk

- every action snapshots the full state -> O(N^2) raw bytes
    - raw run reached 134 GB at N=90k (old gated sim)
- packed floor is small but SUPER-linear (1.0 -> 3.7 KB/msg):
  `advance` rewrites old entries (maturity, times, reps) on every
  action, so consecutive snapshots differ in O(N) places and
  deltas widen with N
- state never shrinks: at 22.5k, 16.8k entries parked in `12-24`
  (consolidation pays one `earn` per author per day; queue grows)

# Sweep (git gc)

- reclaim works: 19.6 GB -> 0.23 GB at 50k (85..200x)
- per-sweep cost O(N) -> cumulative O(N^2); 103 min at 50k;
  overtakes posting time from ~35k on: not a viable policy
- OOM: default gc needs > 6.6 GB at N >= 10k (git pack window
  over thousands of MB-sized blobs); killed by the kernel
    - fix: `pack.windowMemory=512m`, `pack.threads=2`
    - `gc.bigPackThreshold` did NOT make gc incremental
    - extra caps cost ~40% sweep time; only value is memory safety
- never gc with a concurrent writer (post briefly unanchored)

# Gated chain economy (old chat-02, before open chains)

- single faucet: only the pioneer likes; 50 likes from the
  initial 50k reps + 3 earned = 53 likes, exhausted by N~5k
- like refund/earn go to the LIKED author, nothing returns to
  the liker; pioneer earn requires pioneer posting daily
- result: 15 users ever admitted; blocked rate climbs 32->58%
  (both never-admitted users and admitted users that burst)
- admitted users hover near 0 reps (450+500+1000/day drains fast)

# Fix plan (see .claude/plans/260829-otim.md)

- 1: `advance()` one pass (kills the O(A*N) spikes)
- 2: bound `G.actions` (evict consolidated/queued entries)
- 3: append effect-log instead of snapshots
    - `act`/`reps`/`mature` lines; state = fold of prefix
    - write O(1), disk O(N), no gc, checkpoints bound read
- 4: cheaper serializer (only if 3 is skipped)
