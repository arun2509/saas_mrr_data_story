#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# === Config ===
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "mrr_2024.csv"
CHARTS_PATH = Path(__file__).resolve().parents[1] / "charts"
CHARTS_PATH.mkdir(parents=True, exist_ok=True)

INDUSTRY_TARGET = 15.0

# === Load ===
df = pd.read_csv(DATA_PATH)
# Compute helper columns
order = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}
df["q_num"] = df["quarter"].map(order)
df = df.sort_values("q_num", ignore_index=True)
df["gap_to_target"] = df["mrr_growth"] - INDUSTRY_TARGET

# Summary metrics
avg_growth = df["mrr_growth"].mean()
min_q = df.loc[df["mrr_growth"].idxmin(), "quarter"]
max_q = df.loc[df["mrr_growth"].idxmax(), "quarter"]
min_val = df["mrr_growth"].min()
max_val = df["mrr_growth"].max()
latest_q = df.iloc[-1]["quarter"]
latest_val = df.iloc[-1]["mrr_growth"]
avg_gap = avg_growth - INDUSTRY_TARGET

# Save a summary CSV
summary = {
    "average_growth": round(avg_growth, 2),
    "average_gap_to_target": round(avg_gap, 2),
    "min_quarter": min_q,
    "min_value": round(min_val, 2),
    "max_quarter": max_q,
    "max_value": round(max_val, 2),
    "latest_quarter": latest_q,
    "latest_value": round(latest_val, 2),
    "industry_target": INDUSTRY_TARGET,
}
pd.DataFrame([summary]).to_csv(CHARTS_PATH / "summary.csv", index=False)

# === Chart 1: Growth trend vs. target (single plot) ===
plt.figure()
plt.plot(df["quarter"], df["mrr_growth"], marker="o", label="MRR Growth (Quarterly)")
plt.axhline(INDUSTRY_TARGET, linestyle="--", label="Industry Target (15)")
plt.title("MRR Growth Trend vs. Industry Target (2024)")
plt.xlabel("Quarter")
plt.ylabel("MRR Growth")
plt.legend()
plt.tight_layout()
plt.savefig(CHARTS_PATH / "mrr_growth_trend_vs_target.png", dpi=160)
plt.close()

# === Chart 2: Gap to target (single plot) ===
plt.figure()
plt.bar(df["quarter"], df["gap_to_target"], label="Gap to Target")
plt.axhline(0, linewidth=1)
plt.title("Gap to Industry Target by Quarter (2024)")
plt.xlabel("Quarter")
plt.ylabel("Gap (Growth - 15)")
plt.legend()
plt.tight_layout()
plt.savefig(CHARTS_PATH / "gap_to_target_by_quarter.png", dpi=160)
plt.close()

# Print a concise console summary
print("=== MRR Growth 2024 Summary ===")
print(f"Average growth: {avg_growth:.2f} (required: 15.00, gap: {avg_gap:.2f})")
print(f"Best quarter: {max_q} at {max_val:.2f}")
print(f"Lowest quarter: {min_q} at {min_val:.2f}")
print(f"Latest quarter ({latest_q}): {latest_val:.2f}")
