# Review: comments on Usenet measures (26/11/03)

- scope: main.tex §4.1, Storage to Forks & Merges (l.1366-1488)
- per measure: does the text analyze or judge the result?

# Items

1. [yes] Storage: snapshots tradeoff, every-N alternative
2. [yes] Operations: constant times key to scale, disk vs CPU
3. [??] Propagation: explains the green/yellow jumps, no
   judgement on 5h/23h
    - done: brackets per class jump in Fig. 9 (prop.py);
      text: green 3min, yellow 1-6h, red 6-30h, from schedules
4. [no] Fork depth: numbers only
    - done: forks are the norm, merged automatically
5. [yes] Merge time: within the window, no hard forks
6. [no] Clamps: numbers only
7. [??] Reorders: explains the lone post, no judgement

# Next steps

- go one by one on 3, 4, 6, 7
