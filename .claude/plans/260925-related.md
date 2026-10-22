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
    - [x] 26/10/16 Nostr in single-user/multi-node: relays, no
      ordering, 35 relays/post (`p2p.nostr`), spec `p2p.nostr.nip01`
    - multi/multi attempts paragraph (26/10/16), three levels:
      no consensus / bought consensus / intrinsic reputation
        - axis: who pays for spam, and when it is rejected
          (local filters after replication vs FC admission)
        - Sybil defenses, abstractly (26/10/21): identities bound
          to something not forgeable for free
            - external resource (money, computation): stake, fees,
              PoW; the only defense both permissionless and
              authority-free (Douceur); drawbacks: plutocracy,
              votes purchasable (Li 2019 bots), base capturable
              (Hive fork), currency external to the forum
            - social attestation: members vouch (friend links,
              trust lists, SybilGuard graph cuts); covered by
              federation and F2F in sec.related.users; FMS = trust
              lists over Freenet, one clause there or drop
            - central authority: accounts, CAPTCHAs; federations
            - behavior over time (reputation): multiplier on top of
              the two above, never the entry test (no history)
            - non-defense, local filtering: Frost flooded, Nostr
              relay policy (already in sec.related.nodes)
            - FC = attestation at entry (likes, begs) + behavior
              (reps per tick, time as the only resource) + shared
              record by consensus; claim: permissionless nodes,
              socially admitted members; trades full
              permissionlessness for an intrinsic defense
            - multi/multi text: lead + resource-priced systems
              (Aether no order; Steem/Hive, Farcaster, chains rent
              order from validators) + FC's reputation handing
              over to sec.related.reps
        - table of works (26/10/21), columns: identity scarcity /
          post cost / global order / moderation
            - Frost: none / none / no / none; flooded, dead
            - Freenet FMS: intro puzzle + trust lists / none / no /
              per-user trust lists
            - Aether: none / PoW per post / no (flood, local
              views) / elected mods, per-user impeach, posts expire
            - closed writer sets (Autobase quorum; Automerge,
              Pushpin CRDTs; BFT prototypes): invitation / none /
              yes / owners; Sybil-free by construction, not public
              forums; reuses orphan keys p2p.autobase,
              p2p.automerge, p2p.pushpin
            - Steem/Hive: account fee, stake / resource credits /
              yes, DPoS 21 witnesses / stake downvotes, front-ends
            - Farcaster: on-chain id fee / storage rent / yes,
              Snapchain validators / client labels
            - ICP forums (DSCVR 2021, Taggr, OpenChat): wallet /
              cycles paid by the app / yes, appointed BFT
              validators per subnet (node providers voted by
              governance) / app owners
            - chain forums (DeSo, Lens, Memo.cash): wallet /
              gas, fee / yes, host chain / front-ends
            - Freechains: vouched by members (likes, begs) / 500
              reps / yes, reputation consensus / revokes in reps
        - validators axis (26/10/21): who may validate separates
          the works better than permissioned/permissionless users
          (all are open to post): none (Aether, FMS, Frost) /
          open (PoW, PoS chains) / elected (Steem DPoS) /
          appointed (ICP, Snapchain, Hyperledger prototypes);
          permissioning only moves authority to the validators,
          a federation of operators under another name
            - no deployed forum on Hyperledger-style chains;
              SLR items are fake-news and notarization prototypes
              (Dhall et al. Fabric PBFT; Saad et al. BFT); Ushare
              (Chakravorty and Rong, IMCOM 2017) design only
        - links (26/10/21, all reachable): Frost and FMS
          github.com/hyphanet/wiki/wiki/{Frost,FMS},
          github.com/SeekingFor/FMS; Aether getaether.net,
          github.com/nehbit/aether; Autobase
          docs.pears.com/building-blocks/autobase; Automerge
          automerge.org, github.com/automerge/pushpin,
          inkandswitch.com/local-first; Steem
          steem.com/steem-whitepaper.pdf, hive.io/whitepaper.pdf,
          arxiv.org/abs/1904.07310; Farcaster docs.farcaster.xyz,
          github.com/farcasterxyz/protocol; ICP dscvr.one,
          taggr.link, oc.app, internetcomputer.org/whitepaper.pdf;
          DeSo docs.deso.org; Lens lens.xyz; Memo memo.cash/protocol;
          SybilGuard doi 10.1145/1159913.1159945; SybilLimit doi
          10.1109/SP.2008.13
        - text split (26/10/21): permissioned (closed sets, one
          sentence) / permissionless with local verdicts (Frost,
          FMS, Aether) / permissionless with rented order (Steem,
          Farcaster, ICP, chains; Jeong 2025 front-end moderation)
          / Freechains (order and scarcity from the forum's reps)
        - local verdicts vs federation (26/10/21): they do not
          collapse; federation and F2F delegate to a trusted node
          (spam stopped before relay by its policy); Frost, FMS,
          Aether delegate nothing: open transport, every node gets
          everything, filter after replication per user; missing
          only the shared verdict; FMS trust lists pick identities
          to read, not links; Aether mods are defaults each user
          can impeach
        - Aether (26/10/21): two axes; Sybil/spam defense = PoW on
          every entity (keys, posts, votes), computation not money;
          verdict local (votes, elected mods per client, posts
          expire); bridge case: a resource test rate-limits spam
          but yields no shared verdict, chains add validators for
          that; use it to open the rented-order paragraph
        - [x] 26/10/21 multi/multi drafted in main.tex: lead by
          the author (permissioned vs external resource), then
          permissioned identities/nodes (Autobase, CRDTs, FMS;
          ICP forums, Farcaster), Aether (PoW, no consensus),
          social blockchains (Steem/Hive, chain forums; bots,
          Hive fork, front-end moderation), FC closing; stub
          list removed; 9 bib entries added (p2p.fms, p2p.icp,
          p2p.farcaster, p2p.steem, p2p.steemit.bots,
          dosn.navigating, blockchain.osn, sybil.guard,
          sybil.limit); orphan keys autobase/automerge/pushpin
          reused; Frost dropped
        - [x] 26/10/21 author rewrite: permissioned paragraph =
          CRDTs + Autobase (quorum of permissioned indexers); FMS,
          Frost dropped (p2p.fms removed from bib); Aether PoW
          "dubious defense given the hardware asymmetry";
          Farcaster (elected committee, storage rent) and ICP
          (node providers approved by governance) moved into the
          social-blockchains list; Farcaster is permissionless for
          users, validators elected (Snapchain whitepaper)
        - [x] 26/10/21 social blockchains paragraph: permissioned
          validators (Steem/Hive, Farcaster, ICP) vs open chains
          (DeSo, Lens, Memo.cash); "order rented from an external
          currency" + intro drawbacks (\S sec.introduction): pay
          to post, bots, Hive fork, no revocation, front-ends
        - [x] 26/10/21 two examples each: Steem/Hive, Farcaster
          (permissioned validators) / DeSo, Lens (open chains);
          ICP and Memo.cash dropped, p2p.icp removed, p2p.deso and
          p2p.lens added
        - [x] 26/10/21 verbatim support collected: Steem wp "21
          witnesses ... selected by approval voting", "purchase
          more SP to improve voting power"; Snapchain wp
          "Validators are selected through a voting committee",
          "Users must rent a storage unit"; DeSo docs
          "Permissionlessly run validators with no staking
          minimums", "<1/10,00th of a cent per post"; Lens docs
          "layer 2 leveraging ZKsync", sponsorships "cover gas
          fees"; text fixed: "elected by stake or by vote", "open
          chains" (Lens is an L2); Steem wp in pdfs/
        - [x] 26/10/21 cited works only: Steem/Hive (wp, Li 2019),
          Farcaster (spec, Ye et al. IMC 2026 "Behind Farcaster":
          "struggles to maintain a consistent state across hubs",
          "$2.6M in storage fees, no redistribution"), others via
          dosn.navigating; p2p.deso, p2p.lens removed;
          p2p.farcaster.imc added; optional p2p.steem.wealth
          (Guidi, Michienzi, Ricci, IEEE TCSS 2024)
        - [x] 26/10/21 final: social blockchains = external
          currency, consensus assumed correct and permissionless;
          text focuses on drawbacks (intro a-d, bots, Hive fork,
          no revocation, front-ends); validators/witnesses/
          committees out of the text (stake election = resource,
          only Farcaster's committee is permissioned)
        - [x] 26/10/21 not all pay per post: Steem wp "eliminate
          the need for fees", "bandwidth-per-share" rationing by
          stake; Farcaster storage rent (IMC: "$2.6M in storage
          fees"); Guidi 2021 Table 1 fees Steem/Hive "-"; text:
          "either as a fee per action or as stake that rations
          actions", "admission is paid in that currency"
        - subsection reads as "who decides": nobody (local
          verdicts) / a validator set (rented order) / the members
          (Freechains)
        - superseded (26/10/20) the 26/10/16 split (permissioned
          vs local moderation); split by Sybil defense (refined
          26/10/21 above):
            - lead: consistency with no authority makes Sybils
              the fundamental problem (free identities, any
              majority rule is for sale)
            - trust among known peers: Freenet FMS (trust lists,
              intro puzzles; subjective, no consensus); Frost (no
              defense, died by flooding)
            - priced identities or posts: Aether (PoW per post,
              posts expire); Farcaster (on-chain id fee, storage
              rent); Steem/Hive (stake, DPoS witnesses)
            - closing: only the priced ones reach a global order,
              rented from a validator set (Steem 21 witnesses,
              Farcaster Snapchain) or a public chain (DeSo, Lens,
              Memo.cash); Hive fork 2020 = stake is capturable;
              FC keeps order intrinsic to authoring reputation;
              hands over to sec.related.reps
            - [x] 26/10/21 F2F paragraph at the end of
              sec.related.users; bib p2p.retroshare (team blog
              2013), p2p.briar (quick start); stub item removed
            - Retroshare/Briar moved out (26/10/20): F2F forums
              flood over personal links with no order or shared
              verdict, i.e., Usenet with users as servers; one
              clause in sec.related.users after Usenet:
              "federations in which each user is their own
              server"
            - main.tex ea9b64e: "multi-user/multi-node aim" lacks
              "forums"; dangling "IRC/Discord or Usenet/Reddit."
            - closing (26/10/16): the permissionless and
              consensus-based ones are blockchain-hosted forums,
              posting by chain fee: DeSo/BitClout (own chain),
              Memo.cash (BCH), Peepeth (Ethereum), Lens (Polygon),
              Subsocial (Polkadot); Steem/Hive borderline (DPoS,
              21 witnesses)
                - contrast: consensus rented from an external
                  currency; admission pay-to-post, votes buyable,
                  moderation money-gated; FC keeps ordering
                  intrinsic to the forum's own reps
                - [x] verified (26/10/16): the Guidi survey is
                  "When Blockchain meets Online Social Networks",
                  Pervasive and Mobile Computing 62, 2020, 101131
                  (doi 10.1016/j.pmcj.2020.101131); paywalled,
                  Pisa repository behind Cloudflare; not fetched
                - surveys fetched to `pdfs/` (26/10/16):
                    - `dosn.navigating-jeong2025` arXiv 2504.00071,
                      Jeong, Ng, Carley, Liu: four architectures
                      (federated, P2P, blockchain, hybrid);
                      blockchain = Steemit/Hive, Lens, DeSo, Minds;
                      Farcaster hybrid; "bifurcated model: strong
                      protocol-level censorship resistance combined
                      with necessary front-end moderation";
                      "consensus-driven blacklisting ... reserved
                      for extreme cases" -> best opener
                    - `blockchain.osn-guidi2021` Applied Sciences
                      11(21):9880 (OA): Steem/Hive/EOS/Ethereum/
                      Klaytn, all permissionless, DPoS/PoW/PBFT;
                      "DPoS ... may not be a desirable approach
                      for ... highly decentralized social media";
                      rewards "incentivize bot activity"
                    - `blockchain.slr-hisseine2022` Applied
                      Sciences 12(13):6567, SLR of 42 papers: fake
                      news and privacy; little on moderation
                    - `steemit-li2019` arXiv 1904.07310 (WebSci
                      2019): >16% of transfers to suspected bots
                - [x] bib: Jeong 2025 (opener), Guidi 2021 (DPoS,
                  fees), Li 2019 (bots); Guidi 2020 optional;
                  cite 2-3 systems only
        - Aether (`p2p.ecosystem`): flood, stores all, PoW,
          elected mods, impeach = per-user view, posts expire
        - Freenet FMS (new @misc): own outboxes, trust lists,
          intro puzzles; rejects spam before download, but
          subjective (no consensus); Frost died by flooding
        - Steem/Hive (new: white paper; Li and Palanisamy,
          WebSci 2019): on-chain posts/votes, DPoS 21 witnesses,
          resource credits by stake, 2020 Sun takeover -> Hive
          fork; reputation bought with external stake
        - Farcaster (optional): on-chain ids, storage rent,
          hubs CRDT -> Snapchain BFT (2025); consensus by
          validators, posts by payment
        - Retroshare/Briar: see 26/10/20 above (sec.related.users)
        - [x] 26/10/22 checked: Steem, Li 2019 in bib
          (p2p.steem, p2p.steemit.bots); Aether via
          p2p.ecosystem; FMS -> won't do
    - [x] 26/10/16 dVCS: cite only in CRDTs Merkle DAG sentence;
      \iffalse paragraph dropped
    - [x] 26/10/16 author: CRDTs and DHTs subsections removed,
      subsubsections -> subsections (`sec.related.users/nodes/
      multi`); opener as lead + description list (4 items)
    - [x] CRDTs: one paragraph inside multi/multi as root of the
      local-moderation group (Automerge/Pushpin: honest replicas,
      no admission); Autobase quorum in the permissioned group;
      DHTs dropped, IPFS cite stays at the 128 KB rule
    - [x] 26/10/21 reputation systems written: Resnick systems,
      Wang/EigenTrust webs of trust; cheap pseudonyms (newcomers
      start at zero) and sybilproof (asymmetric flow from a seed)
      -> FC pioneers, likes, begs; old three aspects kept; Steem
      reputation = stake (p2p.steem.wealth); closing line; bib
      rep.sybilproof, p2p.steem.wealth added
    - [x] 26/10/21 rewritten as a survey (author: "sounded like
      design discussion"): works first, FC in one closing
      sentence; three aspects and design refs dropped; Slashdot
      karma added (forum.slashdot, Lampe and Resnick CHI 2004)
    - [x] 26/10/21 "webs of trust" -> "trust scores" (term in
      neither paper; verbatim checked: EigenTrust "aggregates the
      local trust values", "choose the peers from whom they
      download"; Wang "arrange the list according to its trust")
    - [x] 26/10/21 Slashdot: "karma gates moderation" -> "grants
      moderation points only to users whose karma ... is positive"
    - [x] 26/10/21 karma sentence covers Reddit too (forum.reddit.karma,
      Richterich JoPP 2014: "quasi-monetary incentive"); forum.reddit
      (Gilbert 2013) was already the author's, cited in design
    - [x] 26/10/21 file sharing split local view (Wang: "those few
      peers that it trusts most") vs global view (EigenTrust: pre-trusted
      peers "essential ... break up malicious collectives" = pioneers)
    - [x] 26/10/21 Sybil results as two sentences (author intro):
      F&R "distrust of newcomers is an inherent social cost of easy
      identity changes"; C&F "no symmetric sybilproof reputation
      function", "asymmetric reputation function based on flow";
      Cheng 2005 PDF saved (sigcomm.org)
    - [x] 26/10/21 results shortened, no authors, cites at end; FC
      closing clause: no reps for newcomers, reps flow from pioneers
      to contributing members through taxed likes; Wang -> "a
      Bayesian trust model"; author moved results to subsection end
    - [x] 26/10/21 review pass (tex + pdf), applied: "In FC takes",
      Sybils (not members) rate each other, "sybilproof" term, intro
      roadmap lists four subsections, drop "Finally", "Such
      pre-trusted seeds", Hypercore (formerly Dat)
    - [x] 26/10/21 review leftovers: FC sentence moved to close §5.4
      ("Unlike all of the above"); sybil.guard/sybil.limit cited at
      "trusted parties" (no orphans left there); "takeover that
      forked Hive from Steem"
    - [x] 26/10/21 opener cites: decentralized forums -> p2p.ecosystem
      only (p2p.dosn/p2p.osn stay in intro); §5.3 item cites
      blockchain.osn (Guidi 2021 overview)
    - won't do: Aether has no paper, stays cited via p2p.ecosystem;
      §5.4 stretch goes away once §Conclusion has text
    - [x] 26/10/21 deleted: both %%% rules, old P2P Protocols block,
      old related leftovers and 2021 experiments; old Conclusion kept
      in \iffalse (ln ~1508-1562) as source for the new one
    - [x] 26/10/16 cites only, no text: p2p.local, p2p.dag.sync,
      permissionless + blockchain.wild, forums p2p.survey ->
      p2p.dosn + p2p.osn, fed.usenet (RFC 977, new),
      p2p.flocking
    - [x] 26/10/22 new bib + text: Aether, Steem/Hive, SybilGuard
      done; FMS -> won't do; fcs.sbseg20/23 (double-blind?) open
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
- dVCS paragraph in multi/multi: short paper, not forums
- Freenet FMS: no paper, not in text; Sybil defenses covered
- orphan bib keys: BibTeX skips uncited entries; cap, kahn,
  p2p.bittorrent, p2p.dvcs, p2p.kademlia, p2p.proofs, p2p.sec,
  pubsub.* (cited only in deleted old text)
