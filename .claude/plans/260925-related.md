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

# Citations to add (26/09/25)

- Decentralized Forums (one sentence each):
    - Nostr: relays + pubkey identities, spam/Sybil handled
      after the fact (NIP-13 PoW, web-of-trust lists)
    - AT Protocol/Bluesky: portable DIDs and composable
      moderation (third-party labelers) -- answers the
      non-portable identity critique we make of federation
    - Farcaster: posting capacity bought with staked storage,
      the closest deployed analogue of our post cost
    - Lemmy: the ActivityPub *forum* (Mastodon is microblog)
    - Usenet/NNTP: permissionless flooding ancestor, spam as
      the failure mode with no reputation (we replay it)
- Peer-to-Peer Protocols (thin after the BTC/PoW cut: only
  IPFS, Dat, gossipsub) -- rebuild it as a lineage arc:
    - NEW OPENING: unstructured flooding (Gnutella), anonymous
      publishing (Freenet), structured DHTs (Chord, Kademlia);
      none carries author identity or admission control
    - then BitTorrent/Kademlia as the DHT the next ones use
      (the DHT paragraph currently cites NO DHT paper)
    - then IPFS and Dat as today (data-centric)
    - Dat == Hypercore: renamed in 2020, same lineage, not a
      competitor (Hypercore = log, Hyperswarm = connectivity,
      Hyperdrive = fs; Holepunch/Pear since 2021) -> mention as
      a continuation clause, not a separate system
    - Autobase (Holepunch) is the REAL relative and must be
      cited: per-writer logs, causal DAG with clocks,
      deterministic linearization replayed into a view, and
      CHECKPOINTS that freeze the order -- same shape as our
      replay + settled prefix
        - PERMISSIONED (confirmed in the docs): writers are
          granted inside the `apply` handler (`addWriter`),
          no open writing by default, and checkpoints need an
          INDEXER MAJORITY; `optimistic` appends let a
          non-writer submit for validation, which is exactly
          where an app must invent the admission policy that
          \FC has in-protocol (\reps)
        - it is a DHT USER (Hyperswarm), not a DHT design
    - SPLIT THE TWO DHT ROLES (the text conflates them):
        - content routing (IPFS: which peer has this CID) --
          keep the existing critique, wrong fit for forums
        - discovery and NAT traversal (Hyperswarm: who is on
          this topic) -- see the discovery note below: \FC
          needs neither a DHT nor holepunching
    - libp2p as INFRA: gossipsub is one of its modules; the
      concrete referent for "FC could benefit from pubsubs to
      manage interconnections"
    - permissioned BFT (PBFT/Tendermint) one-liner: cited in
      the design (ln 1020) but absent from related work;
      Autobase's indexer majority is a live instance of it
- stray line in the P2P subsection: `128KB also immutable`
  (editing leftover, delete or turn into a sentence)

# Discovery and reachability (26/09/25, replaces the DHT idea)

- a DHT is NOT worth it here: it needs hardcoded bootstrap
  nodes anyway (so the recursion buys little), re-announces
  on a TTL, and an announcement only helps while online --
  which is when a direct address already works
- NO HOLEPUNCHING either: \FC sync is store-and-forward of a
  self-certifying DAG, not a live session
    - if an intermediary is reachable by both, SYNC THROUGH IT
      (it likely serves the same chain); it can delay but not
      forge, so relaying needs no trust
    - holepunching is for real-time protocols (the TML paper's
      deadlines), not for a gossip DAG
- THE CHAIN IS ITS OWN DIRECTORY: addresses are content
    - genesis: bootstrap addresses at `chains add init`, so an
      invite is just the genesis (immutable, ages, last resort)
    - announcement post: signed `host:port`, gossips for free,
      self-updating, survives the founder (main mechanism)
    - on the beg: the newcomer's first action carries its
      address, so the welcome doubles as an address exchange
      (and covers members who cannot afford a post)
- put the address in the PAYLOAD, not the metadata: payloads
  are revocable and swept; a signed IP that lives forever is
  dead weight and a doxxing vector (prefer a name or onion)
- decide: does an announcement cost \reps? (the beg
  attachment is the free path for the broke newcomer)
- one paper sentence: discovery is solved in-band by the
  forum; reachability needs at least one reachable peer,
  which is a deployment assumption, not a protocol feature

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
