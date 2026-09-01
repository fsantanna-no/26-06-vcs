# TODO

- Restructure Section 3 into two subsections
    - 3.1 Design: overall design, bootstrapping, admission,
      proof-of-authoring, consensus
    - 3.2 Threats: attacks, nits, malicious behaviors, hard forks,
      double-spend, Byzantine faults

- Cite `p2p.mst` (Auvolat & Taiani, "Merkle Search Trees: Efficient
  State-Based CRDTs in Open Networks", SRDS 2019, doi
  10.1109/SRDS.2019.00032; bib added, pdfs/mst-auvolat2019-srds.pdf)
    - summary: op-based CRDTs need causal broadcast / vector clocks,
      impractical in open networks with churn; pure state-based
      CRDTs work if state merge is cheap; MST = balanced,
      key-ordered Merkle tree for hash-based anti-entropy; 66% less
      bandwidth than vector clocks; basis of Bluesky AT repos
    - places to cite
        - Sec.2 P1 SEC sentence, with `fed.matrix,p2p.byz`
        - CRDT section: state-based (DAG sync) vs op-based (patches)
          split; Git DAG as CvRDT
        - SEC proof: why no causal broadcast is needed (Git fetch
          is Merkle state merge)
        - Related Work / P2P: Bluesky repos are MSTs
        - protos plan: Merkle reconciliation is what buys delivery
    - caveat: honest-but-churning model only; no Byzantine, Sybil,
      or abuse discussion -> backs the mechanism, not Sybil claims
    - verbatim in `260826-refs.md` (Candidates)
    - comparison with the Git backend (both state-based CRDT sync
      over hashed state)
        - state: Git = Merkle DAG of commits (history, causal
          links); MST = Merkle search tree over a keyed set (no
          history)
        - root: Git has no single root (state = set of heads);
          MST has one root hash independent of insertion order
        - diff: Git `fetch` negotiates heads, walks ancestry to the
          common prefix, sends a packfile (cost ~ divergence, needs
          have/want dialogue); MST compares hashes top-down
          (cost ~ log n + diff, works between strangers)
        - causality: Git encodes parents, which the consensus order
          needs; MST has none (items carry their own keys)
        - deletion: both grow-only (Git gc prunes unreachable only;
          MST needs tombstones)
        - verdict: MST is not a competitor but an INDEX; Freechains
          needs Git's causal DAG; Bluesky layers an MST under a
          signed commit chain (closest cousin of DAG + hooks);
          MST is the upgrade path if fetch negotiation ever
          becomes the bottleneck (not at 10k posts)

- Review checkpoint (2026-08-28): abstract, Intro, and "\FC and
  Git" reviewed paragraph-by-paragraph and in the rendered PDF;
  NEXT = Section 3 intro + Overall Design (L367)
- Postponed PDF issues (visible in the draft):
    - "Section ??": label `sec.evaluation` does not exist yet
    - "TODO: expose results ..." prints (Intro, ~L204)
    - "prove its SEC property (TODO)" prints (roadmap, ~L211)
    - Section 3 internal roadmap ("Section 3.7 simulates ...") will
      go stale when Experiments moves to `sec.evaluation`
- Section 3 leftovers spotted while scanning:
    - L~508-517 `TODO >>> ... <<< TODO` old branch-1/2 narrative,
      redundant with the sbseg text above it
    - L~539 `TODO: duplicado abaixo` (consensus-order sentence)
    - L~1047 `TODO: fazer para periodo inteiro, explicar pack do git`

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
