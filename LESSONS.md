# Lessons learned

Dated entries. Read before preparing a new House of Graphs deposit. When a
deposit is corrected, a value is found wrong, or a description is misread, add
what happened and the rule going forward. Keep entries blunt and specific.

Entries before 2026-10-21 name modules that now live in the `hogledger/`
package: `verify.py` is `hogledger/primary.py`, `verify_witnesses.py` is
`hogledger/registry.py` plus `hogledger/gate.py` (run `python3 -m hogledger
verify`), and `manifests/` became `receipts/` and `provenance/`.

## 2026-06-30 -- Never call a Zarankiewicz witness "K_(3,4)-free"

**What:** The May 2 2026 House of Graphs deposits for the Zarankiewicz witnesses
z(10,10;3,4)=66 (HoG #56650) and z(9,10;3,4)=60 (#56652) each described the graph
as "K_(3,4)-free", in the comment prose and as a keyword. Both graphs DO contain
K_(3,4) as an abstract subgraph, in the transposed 4-by-3 orientation. Only
z(9,11;3,4)=66 (#56651) is genuinely K_(3,4)-free. Independent re-verification on
2026-06-30 caught it; the public comments and the source repo's JSON and README
were corrected.

**Why:** z(m,n;s,t) forbids only the s-rows-by-t-columns all-ones submatrix, an
ordered (one-sided) condition. But K_(3,4) = K_(4,3) as an abstract graph, and
House of Graphs stores graphs unlabeled, so "K_(3,4)-free" reads as the abstract
(both-orientation) claim, which is false for the transposed orientation. One
comment template was applied to all three witnesses; it is true only when the
graph also avoids the 4-by-3 block (z(9,11)).

**Rule going forward:** Never call a Zarankiewicz witness "K_(s,t)-free". State
the matrix condition ("no s-by-t all-ones submatrix") or the one-sided
neighbour-sharing condition ("no s row-vertices share t common columns"); both
are orientation-explicit and cannot be misread. When a claim about an ordered or
bipartite object will appear in an unlabeled-graph context such as House of
Graphs, re-express it so it stays true without the labels. Re-decode the graph6
you are about to deposit and re-check BOTH orientations before deposit. This
repo's contributions.yaml carries a `k34_free` flag per Zarankiewicz record;
verify_witnesses.py recomputes it (triple-based) so the value is never
hand-asserted.

## 2026-06-10 -- Verify every value against ground truth before claiming

**What:** A multi-agent review of prepared papers found fabricated tables and
propagated wrong facts that an earlier "verification" had missed: distribution
tables that did not sum to the known total, a displayed classical bound that the
paper's own values violated, a formula in an abstract that contradicted the
paper's own table, and a hallucinated citation. The common cause was
hand-transcription and checking only compilation and format, not every printed
number against the machine-verified data.

**Rule going forward:** A claimed value or witness is not trusted until it is
re-derived or re-checked from scratch by independent code, and every displayed
classical theorem is checked against the actual literature. For graph deposits
here: never hand-transcribe a graph6 string or an invariant. Decode the exact
graph6 that will be deposited, recompute the edge count and the defining property
(C6-free and C6-saturated, K_4-free and K_4-saturated, or the Zarankiewicz matrix
condition), and confirm the roundtrip decode(encode(G)) reproduces the edge set.
When a fact is corrected in one place, grep the whole tree for the same fact;
wrong constants propagate across companion artifacts.

## 2026-07-03 -- graph6 strings can contain a literal backtick; write them byte-exact

**Context:** Building this repo. Several witness graph6 strings contain a literal
backtick (ASCII 96): sat(9,C6)=12 is `HyOkc?` followed by a backtick;
sat(10,C6)=13 is `I{` then a backtick then `Q__H@?`; sat(8,C6)=11 and
sat(8,P_4)=4 and z(9,10;3,4)=60 each contain one too. A backtick is easy to lose
or turn into a different character when a string passes through Markdown, a shell,
or a copy-paste. Losing that one byte silently changes the graph.

**What was done:** The g6 files were written from explicit byte values (backtick =
byte 96), not typed into prose. verify_witnesses.py then re-decoded every file,
confirmed the roundtrip, the vertex count, the edge count, and the defining
property. Result on 2026-07-03: all 14 witnesses verified. The two new C6 values
checked out exactly: sat(9,C6)=12 is C6-free and C6-saturated at 12 edges;
sat(10,C6)=13 is C6-free and C6-saturated at 13 edges (both the primary witness
and the near-cubic alternate minimum).

**Rule going forward:** Store every graph6 as a byte-exact file under graphs/,
mirror it in contributions.yaml, and re-decode it with verify.py before any
deposit. Record the byte values in a comment when a string contains a backtick.
Treat any graph6 that fails its roundtrip or its property check as corrupt and
re-transcribe from the byte sequence, not from prose.

## 2026-07-14 -- Search canonical forms, not names

**What:** A live graph6 search found several queued witnesses already in House of
Graphs under unrelated names or for unrelated properties: sat(7,C6) is HoG #868,
one sat(9,C6) minimum is #21054, and all queued K_4 and P_4 witnesses also had
existing canonical matches. Their null `hog_id` fields meant "not checked," not
"absent."

**Why:** HoG stores unlabeled graphs and may know the same isomorphism class for a
different theorem. Text, invariant, and graph-name searches do not reliably detect
that overlap.

**Rule going forward:** Immediately before every upload, search the exact byte-
verified graph6 through HoG's canonical-form lookup. If it matches, record the live
id and add a concise comment explaining the new interpretation instead of creating
a duplicate. Treat absence as a time-stamped search result, never as an inference
from an unfamiliar graph name.

## 2026-10-17 -- An open general problem does not make every small value new

**What:** A deeper prior-art audit found the n=9,10 C6 saturation values and
their complete minimum families in Remark 1 of the 2012 Zhang-Luo-Shigeno
preprint, associated with DOI 10.1007/s00373-014-1422-4. Earlier records here
incorrectly described these values as new. The preprint's n=11 claim also
differs from our reproduced value; that discrepancy must be described with
the source version specified, not automatically attributed to the final paper.

**Rule:** Inspect small-case remarks, figures, computational tables, and
preprint/final-version differences. Absence of a general formula or a web
search match is not a novelty certificate. Correct inherited public claims
and source attribution before using them to motivate further contributions.

**Public correction:** On 2026-10-17 the comments on HoG 21054, 57168,
57169, 57170, 57171, 57167, and 57166 were edited to credit the 2012
preprint and explicitly withdraw the novelty claim. Each saved correction
was checked on the live graph page.

## Standing verification rules

- The final 2015 Zhang-Luo-Shigeno text was accessed on 2026-10-17. Remark 1,
  page 1089, retains the order-11 value 15 and already records the order-12
  value 16. Attribute the n=12 exact value to that source; distinguish the
  new complete minimum classification. The checked n=11 witness corrects
  the specific small-order computational claim, not the general bound.

- Registry verification is data-driven: every graph needs structured
  `verification` metadata, and every `.g6` file must have a registry record.
  Do not reintroduce a parallel hardcoded witness table.

- Re-verify every witness from its graph6 string before deposit: edge count,
  defining property, and roundtrip. verify_witnesses.py is the gate.
- Do not label a graph "deposited" unless a live House of Graphs id is confirmed.
  ready means verified and prepared; deposited means it has a hog_id.
- State bipartite or ordered conditions in an orientation-explicit form for any
  unlabeled-graph database. Never "K_(s,t)-free" for a one-sided Zarankiewicz
  condition.
- Cite the appropriate exact archived version. The current C6 release is
  v6, 10.5281/zenodo.23527267; preserve earlier version links when identifying
  historical evidence. Zarankiewicz: 10.5281/zenodo.19985042.
- External publication requires explicit user authorization. The current
  contribution goal authorizes Zenodo publication and HoG submissions or
  annotations after verification; login remains a user handoff when necessary.
