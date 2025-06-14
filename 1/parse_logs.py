#!/usr/bin/env python3
"""Print a quick textual summary of results.csv."""
import pandas as pd, sys

df = pd.read_csv(sys.argv[1])

# geometric-mean solve time, median memory, success-rate
geom  = df.groupby("solver").secs.apply(lambda s: (s.prod())**(1/len(s)))
mem   = df.groupby("solver").rss_mb.median()
succ  = (df.assign(ok=df.status.eq("Optimal"))
           .groupby("solver").ok.mean()
           .mul(100))

summary = pd.concat(
    [geom.rename("gmean_time_s"),
     mem.rename("median_rss_mb"),
     succ.rename("success_%")],
    axis=1
).round(2)

print(summary)
