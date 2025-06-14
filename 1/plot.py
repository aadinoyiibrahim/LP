#!/usr/bin/env python3
import sys, pandas as pd, matplotlib.pyplot as plt, numpy as np, os
if len(sys.argv) < 2:  raise SystemExit("Usage: plot.py results.csv")
df = pd.read_csv(sys.argv[1]); os.makedirs("figs", exist_ok=True); os.makedirs("tables", exist_ok=True)

for col in ["secs", "rss_mb", "iterations", "gap"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
df.dropna(subset=["secs"], inplace=True) 

figsize=(10,8)

# 1) SOLVE TIME -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10,4))
p = (df.groupby(["instance","solver"]).secs.median()
       .unstack().sort_values("highs"))        # hardest at right
p.plot.bar(logy=True, figsize=figsize,  ax=ax)
ax.grid(axis="y", color="0.85", linestyle="--", linewidth=0.7)
plt.ylabel("seconds  (log)")
# plt.title("Wall-clock time per instance")
plt.tight_layout() 
plt.savefig("figs/solve_time.png")


# 2) MEMORY -----------------------------------------------------------------
fig, ax = plt.subplots(figsize=(5,4))
df.boxplot(column="rss_mb", by="solver", ax=ax,
           grid=True, color=dict(boxes='0.3', whiskers='0.3',
                                 medians='0.3', caps='0.3'))
ax.grid(axis="y", color="0.85", linestyle="--", linewidth=0.7)  
ax.set_ylabel("peak RSS (MB)")
# ax.set_title("Memory footprint by solver")
plt.suptitle("")          # remove Pandas default title
plt.tight_layout()
plt.savefig("figs/memory.png")


# 3) ITERATIONS -------------------------------------------------------------
fig, ax = plt.subplots(figsize=figsize)
for i, solver in enumerate(["clp","glpk","highs"], 1):
    # y = df.loc[df.solver==solver, "iterations"].dropna()
    y = df.loc[df.solver==solver, "iterations"].fillna(1)
    x = np.full_like(y, i) + (np.random.rand(len(y))-0.5)*0.15   # jitter
    ax.scatter(x, y, alpha=.6, label=solver, marker="o", s=30)
ax.set_yscale("log")
ax.grid(axis="y", color="0.85", linestyle="--", linewidth=0.7)  
ax.set_xticks([1,2,3], ["clp","glpk","highs"])
ax.set_ylabel("iterations (log)")
# ax.set_title("Algorithmic work")
ax.legend()
plt.tight_layout()
plt.savefig("figs/iterations.png")


# 4) ROBUSTNESS HEAT-MAP ----------------------------------------------------
status = (df.assign(flag=df.status.ne("Optimal").astype(int))
            .pivot_table(index="instance", columns="solver", values="flag", aggfunc="max"))
status = status.reindex(index=sorted(status.index))       # alpha order
fig, ax = plt.subplots(figsize=(5,6))
im = ax.imshow(status, cmap="RdYlGn_r", vmin=0, vmax=1)
# ax.grid(color="0.85", linestyle="--", linewidth=0.7)
ax.set_xticks(range(3), status.columns)
ax.set_yticks(range(len(status.index)), status.index, fontsize=8)
plt.colorbar(im, label="0=Optimal  1=Error/Gap")
# plt.title("Numerical robustness") 
plt.tight_layout()
plt.savefig("figs/robustness.png")


# 5) SUMMARY TABLE ----------------------------------------------------------
# geom = df.groupby("solver").secs.apply(lambda s: np.exp(np.log(s).mean()))
geom = (df.groupby("solver").secs.apply(lambda s: np.exp(np.log(s).mean())))
mem  = df.groupby("solver").rss_mb.median()
succ = (df.assign(ok=df.status.eq("Optimal")).groupby("solver").ok.mean()*100)
summary = pd.concat([geom.rename("gmean_time_s"),
                     mem.rename("median_rss_mb"),
                     succ.rename("success_%")], axis=1).round(3)
summary.to_csv("tables/summary.csv")
print(summary)
