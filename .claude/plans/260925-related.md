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

# BitTorrent and IPFS (26/09/25)

- ONE structural difference: hashing granularity
    - BT hashes the collection -> the collection is the unit
      of sharing; closed set with a known size and piece list,
      which is what enables rarest-first, endgame and
      TIT-FOR-TAT (both peers want the same finite set)
    - IPFS hashes each chunk -> dedup and linking across
      collections, but no "set" to reciprocate over, hence no
      incentive layer at all
    - DHT lookup, multi-peer download and hash verification
      are IDENTICAL in both: do not dress them up as different
- so both exist for one good reason: BT is a TRANSFER protocol
  (better when moving a known fileset), IPFS is a NAMING
  system (a permanent linkable id, embeddable in pages and
  other files); BT v2 Merkle hashes narrow the gap
- BT's DHT is an AFTERTHOUGHT (2005, BEP 5); 2001 had only
  trackers (an HTTP peer list; no data passes through it)
    - the layering is exactly what we propose for \FC:
      tracker (hub) -> PEX peer exchange (in-band addresses)
      -> DHT only as a trackerless cold-start fallback
- MOTIVATION ITEM: in-session tit-for-tat did not sustain
  seeding, so the community built PRIVATE TRACKERS with
  accounts and upload:download ratios -- persistent reputation
  that is centralized, per-site and non-portable
    - \FC is that accounting in-band, as chain state
    - also the closest prior art to our "intrinsic resource"
      claim: bandwidth actually contributed, not hash power
      or stake -- but scoped to one session

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

# Section 5 structure (26/09/25, decided)

- 5.1 CRDTs (done)
- 5.2 "Distributed Hash Tables" -- DECIDED 26/09/30, DHTs ONLY
    - keep label `sec.related.p2ps`; four paragraphs:
        - P1 one family: BitTorrent, Kademlia, IPFS (hash-named,
          immutable, DHT discovery; tracker -> PEX -> DHT)
        - P2 good for large popular content, bad for search and
          for continuous updates (a change is a new name)
        - P2b optional: tit-for-tat pairwise/first-hand, private
          trackers persistent but central; \reps in-band
        - P3 intersection 1, discovery: answered in-band
          (invite -> announcement posts -> relay via reachable
          peer); DHT by genesis hash = optional fallback
        - P4 intersection 2, payloads: 128 KB cap -> post carries
          a hash; replaces the stray `128KB also immutable`
    - drop: both Dat sentences (-> 5.3), the gossip paragraph
      (P5), the "could benefit from pubsubs" clause
    - NO libp2p; gossipsub/gossipsub2 become uncited -> either
      drop from bib or move the one Sybil sentence to sec.git
    - before writing: confirm the 128 KB rule number in
      `tab.rules`; check §3 states announcement posts (else P3
      says "assumes")
    - bib added 26/09/30: p2p.kademlia, p2p.bittorrent
    - 26/10/01: Autobase moved HERE (same Dat/Hypercore stack;
      collaboration tool, not a forum): one sentence after the
      "single authority" one -- permissioned, designated writers;
      `p2p.autobase` (@misc) added; nothing about it in 5.3
- (superseded detail below kept for reference)
- 5.2 DHTs -- ADJACENT INFRASTRUCTURE, not a rival design
    - one family: Kademlia, BitTorrent, IPFS; locate and
      distribute immutable hash-named content
    - state the TWO intersections with \FC and nothing else:
        - discovery: our problem too, answered in-band
          (invite -> announcement posts -> relay through any
          reachable peer); a DHT is the fallback we do not need
        - LARGE PAYLOADS: the real intersection -- the 128 KB
          cap sends media elsewhere, so a post carries a CID
          (this is the Merkle-payload aside at ln ~1264, now
          the punchline instead of a stray remark)
    - tracker/PEX/DHT layering, tit-for-tat and private
      trackers are context for those two points
- 5.3 Decentralized Forums (and their substrates), in order:
    - Dat/Hypercore + Autobase: pubkey-addressed signed logs,
      the closest substrate; Autobase = permissioned multiwriter
    - Scuttlebutt: same primitive, subjective, newcomers unseen
    - Nostr: signed events over relays, no ordering
    - federated: ActivityPub/Mastodon/Lemmy, Matrix
    - Aether: ephemeral, PoW, local votes
    - dVCS: external scoring
    - reputation systems: closing line
    - naming: say the first two are SUBSTRATES, or title the
      subsection "... and their Substrates"

# Idea: a tracker as a chain (application example)

- replace the private tracker's account database with a chain
    - announcements = posts carrying `infohash -> address`
    - a completed download is acknowledged by a LIKE from the
      downloader: seeding credit issued by the counterparty,
      not measured by a server
    - \reps then gate who may announce and who is trusted
- versus the two existing options
    - in-session tit-for-tat: credit dies with the session
    - private trackers: credit persists but is centralized,
      per-site and non-portable
- honest caveat: nobody can verify the bytes moved, so Sybil
  pairs could mint credit for each other -- the answer is the
  economy (a like costs the liker, 10% burns), same as fake
  likes, and it must be stated rather than hidden
- doubles as a NON-CONVERSATIONAL forum example: the "forum"
  is a swarm registry (discovery + reputation + revoking a
  lying peer)

# Status 26/10/02 and pendings

- done: 5.1 CRDTs; 5.2 DHTs (BT/IPFS/Dat, Autobase permissioned +
  quorum, 128 KB payload hook); 5.3 opener; 5.3 federations
  (Mastodon/Lemmy on ActivityPub, Matrix, drawbacks with
  defederation/blocklist cites, Matrix mitigation); 5.3 feeds
  opener + Scuttlebutt (shrunk, \Xon/\Xnn gone)
- bib added: p2p.kademlia, p2p.bittorrent, p2p.autobase,
  p2p.atproto, time.lamport, forum.lemmy, fed.defederation,
  fed.blocklists (all house style; header comment extended)
- PENDING, in order:
    - [x] 26/10/04 Bluesky sentence, end of the feeds paragraph:
      "Halfway to federations, Bluesky recovers a global view by
      crawling known feeds into a central index, which users query
      instead of replicating feeds, and which thus becomes the
      authority for ordering and moderation"
    - [x] 26/10/05 opener example -> "(e.g., Scuttlebutt)" only;
      Bluesky left out (halfway to federations, not a clean
      single-user/multi-node case)
    - [x] 26/10/04 "e.g. \emph{\#sports}" -> "e.g.,"
    - multi/multi attempts paragraph: Nostr (relays, no ordering,
      spam by relay policy; `p2p.nostr` unused in bib), Aether
      (ephemeral, PoW, local votes), dVCS (external scoring)
    - reputation systems closing (three aspects; closing line)
    - delete the \iffalse block and both %%% rules
    - Farcaster: still optional (staked storage as post cost)
- also: gossipsub/gossipsub2 now uncited (dropped with P5); keep
  under the bib's disabled-sections rule or move the Sybil
  sentence to sec.git

# Elsewhere in the paper

- `--dictator` deserves a SINGLE-USER / MULTI-NODE example:
  one person, many devices (laptop, phone, server) syncing a
  personal chain -- no admission problem, no economy, just
  signed append + replication
    - shows the dictator mode is not only "the platform", and
      gives the cheapest possible deployment story

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
