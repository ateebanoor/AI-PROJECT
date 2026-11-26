| Agent | Avg score | Std score | Max score | Avg survival (steps) | Std survival | Avg nodes expanded / move |
|---|---|---|---|---|---|---|
| BFS | 28.37 | 6.52 | 45 | 234.2 | 70.8 | 28.6 |
| A* | 27.24 | 5.99 | 43 | 222.6 | 66.4 | 8.3 |
| GA | 36.82 | 6.16 | 50 | 398.0 | 99.0 | - |

Cause of death over 100 games:

- BFS: wall=28, self=72
- A*: wall=27, self=73
- GA: wall=21, self=77, starved=2
