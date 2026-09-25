# Related Work Rewrite

# Context

- Section 5 (`sec.related`) restructured on 2026-09-25 into
  CRDTs, Peer-to-Peer Protocols, Decentralized Forums
- roadmap sentence, CRDTs, and P2P subsections are done
- old pubsub, federated, and P2P remainder are disabled in
  `\iffalse ... \fi` (ln ~1300-1437) as source material
- DHT-vs-Merkle aside kept in P2P (ln ~1264-1268) by choice

# Decentralized Forums (`sec.related.apps`)

- two-axes opener is in place (federated vs Scuttlebutt vs FC)
- federated (from disabled ln ~1341): keep
    - server-side ordering and moderation (Matrix moderation footnote)
    - spam filtering left to servers (`pubsub.activitypub`)
    - non-portable identities (`fed.distributed`)
    - drop: real-time advantage paragraph and `\S\ref{sec.evaluation}`
- Scuttlebutt (disabled ln ~1395): shrink to
    - follow graph replicated in topology and storage
    - channels are tag filters over followed feeds
    - newcomers have no visibility
- Aether (disabled ln ~1414): keep
    - ephemeral mutable posts, no global consensus
    - PoW vs spam, local-only votes
- dVCS (`p2p.dvcs`, disabled ln ~1423): keep
    - external scoring function vs FC internal reputation
    - large graphs from byzantine nodes (`p2p.dag.sync`)
- reputation systems (`p2p.rep.wang`, `rep.eigentrust`): keep
    - content vs identity, subjective, depends on consensus
    - closing line: consensus on permissionless network is the key
- order: federated, Scuttlebutt, Aether, dVCS, reputation
- then delete the disabled block and the `%%%` rule

# Loose ends

- empty `\section{Evaluation}` at ln 1186 with `sec.evaluation`
  label duplicated at ln ~1451 inside the disabled block
- intro ln 197 promises Section 4 evaluation (see `260920-eval.md`)
- TODO.md: dangling Conclusion text on "three-layered CRDT
  architecture ... prototyped a dVCS" (disabled block)
- bib: `p2p.ecosystem` cited for both federated and Aether; check

# Won't do

- Ethereum mention in P2P: no bib entry, Bitcoin/PoS suffice
- restore Automerge as a standalone sentence: folded into CRDTs
