# TODO

- Proof of strong eventual consistency for the consensus order
    - no local clocks: all timestamps come from the DAG itself
      (post metadata), so the order is a pure function of the DAG
    - every rule is deterministic (reputation sums on the common
      prefix, activity thresholds counted on DAG posts, lexicographic
      tie-break on hashes)
    - hence two replicas with the same DAG compute the same order
      (convergence); DAG union is a CvRDT (see `260826-cvrdt.md`)
    - state the theorem + proof sketch in the consensus section;
      relate to SEC (Shapiro `p2p.crdts`) and BEC (`p2p.dag.sync`)
    - prove the DAG is a CvRDT: state = causally closed set of
      hash-addressed posts, merge = union; show merge is
      commutative, associative, idempotent, and updates are
      inflationary (posts only added; revoke erases payloads, not
      DAG entries); causal closure preserved under union
    - Git's role is exactly: build the state (`commit`, hashes) and
      deliver it (`fetch` = union); SEC = CvRDT + eventual delivery
      (Shapiro: eventual delivery, strong convergence, termination)
    - the proof needs nothing from Git (sync, storage, transport):
      DAG convergence is a G-Set union, trivial assuming Git is
      correct; the theorem is only "order = pure function f(DAG)"
    - CAVEAT: the hard-fork rule refers to the LOCAL branch (peer
      history, not DAG content), so f is not pure across settled
      forks; either state SEC "for replicas that have not
      hard-forked" or restate the rule as a symmetric DAG-only
      function (activity measured on each branch's own timestamps)

- Related Work / Federated: Usenet (NNTP) as the federated ancestor
    - server-to-server flooding, but users are clients of a server;
      peering is permissioned; no signatures or hash linking; order,
      expiry, and moderation are per-server; delivery best-effort
    - ties the experiments to a forum whose original protocol had
      none of the properties we add

- Related Work: one sentence on Stack Exchange -- reputation-gated
  posting works socially at scale, just centralized; closest
  centralized analogue to reps
    - also Lemmy/Kbin (federated Reddit, ActivityPub) next to
      Mastodon in Federated Protocols

- Related Work: position vs BEC / Kleppmann line -> see
  `260826-bec.md`

- Related Work: add AT Protocol / Bluesky (Kleppmann et al., ACM
  CoNEXT DAI-N 2024, doi 10.1145/3694809.3700740, arXiv 2402.03239)
    - fits "Federated Protocols" next to Mastodon/Matrix
    - contrast: multiple interoperable providers + account
      portability vs \FC permissionless reputation consensus
    - optional companion: Raman et al., IMC 2019 (Mastodon
      re-centralizes: few instances hold most users)

# won't do
