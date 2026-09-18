# gh-simple: GitHub issues replay (yt-dlp/yt-dlp)

- corpus: 12,077 issues (all, 2021-2026), 67,428 posts (issues
  + comments), 21,032 up / 2,097 down reactions (9.1% down),
  3,449 minimized comments (5.1% of posts), 18,377 logins
- first corpus with LIKE and REVOKE on the same events
- mapping: post = signed by login; 👍/👎 = like/dislike 1000
  action by the reacting login; minimized = revoke by the
  `maintainer` key at comment ts + 1h (minimize time is not
  exposed), amount = 1000 + likes on the target
- freechains: branch 260914-tree-trash (state as git tree),
  v0.21.0, installed 26/09/17

## OPEN chain, full corpus (26/09/18)

- 94,006 events in 6h47m; zero skips, zero clamps
- the same replay on the Sep-9 blob build died at 36k after
  12 h (1.17 s/ev, 2 h sweeps): see logs/*-forkage-36k.log

| N     | ev avg | likes  | dislikes | revokes | packed |
|-------|--------|--------|----------|---------|--------|
| 10000 | 0.211s |  1,075 |       58 |     311 |  44 MB |
| 30000 | 0.231s |  4,154 |      159 |   1,559 | 169 MB |
| 50000 | 0.243s |  8,425 |      298 |   2,453 | 316 MB |
| 70000 | 0.260s | 13,061 |      522 |   2,853 | 484 MB |
| 90000 | 0.262s | 19,758 |    1,999 |   3,366 | 658 MB |
| END   |        | 21,032 |    2,097 |   3,449 | 713 MB |

- latency FLAT (0.21 -> 0.26 s over 9x N); sweeps seconds;
  floor linear ~7.6 KB/event
- dislikes are bursty: 723 -> 1,999 in the 80k-90k window (the
  2025 controversies), 9.1% overall vs SE's 7-8%
- revoke reasons: resolved 1,092, off-topic 1,112, outdated
  415, duplicate 388, spam 298, abuse 130, low-quality 14
- TUG-OF-WAR: 3,449 revokes issued, 3,216 still revoked at END
  -> 233 minimized comments (6.8%) were UN-revoked by later
  community likes (a like on a revoked post re-supplies the
  payload and counts on the revoke axis)
    - by reason: pending (gated run logs revoke/un-revoke
      events per cid)

## GATED (dictator = maintainer) -- running

- begs + welcomes; votes only when affordable (smoke: 66% of
  votes unaffordable at 1000); resurrection split; revoke
  reasons as labels for precision
