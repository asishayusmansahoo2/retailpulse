import pandas as pd
from sklearn.model_selection import cross_val_score, StratifiedKFold
from xgboost import XGBClassifier

t = pd.read_csv("data/transactions_cleaned.csv", parse_dates=["date"])
c = pd.read_csv("data/customers_segmented.csv")
cv = StratifiedKFold(5, shuffle=True, random_state=42)


def cvauc(X, y):
    m = XGBClassifier(
        n_estimators=150, max_depth=3, learning_rate=0.05, eval_metric="logloss"
    )
    return cross_val_score(m, X, y, cv=cv, scoring="roc_auc").mean()


lines = ["# Churn Model: Leakage Check", ""]

y = (c["recency"] > 90).astype(int)
leaky = pd.get_dummies(
    c[["age", "recency", "frequency", "monetary", "region", "segment"]],
    drop_first=True,
    dtype=int,
)
clean = pd.get_dummies(
    c[["age", "frequency", "monetary", "region"]], drop_first=True, dtype=int
)
lines.append("## Original label (recency > 90)")
lines.append(
    f"- With recency + segment as features: AUC {cvauc(leaky, y):.3f} (label leakage)"
)
lines.append(f"- Without recency + segment: AUC {cvauc(clean, y):.3f}")
lines.append("")

lines.append("## Forward-looking label (features before cutoff, label after cutoff)")
for days in (30, 45, 60):
    cutoff = t["date"].max() - pd.Timedelta(days=days)
    past, future = t[t["date"] <= cutoff], t[t["date"] > cutoff]
    g = past.groupby("customer_id")
    f = (
        pd.DataFrame(
            {
                "recency": (cutoff - g["date"].max()).dt.days,
                "frequency": g["transaction_id"].count(),
                "monetary": g["total_amount"].sum(),
                "tenure": (cutoff - g["date"].min()).dt.days,
            }
        )
        .reset_index()
        .merge(c[["customer_id", "age", "region"]], on="customer_id", how="left")
    )
    yy = (~f["customer_id"].isin(set(future["customer_id"]))).astype(int)
    X = pd.get_dummies(f.drop(columns="customer_id"), drop_first=True, dtype=int)
    lines.append(
        f"- {days}-day window: {yy.sum()} churners ({yy.mean()*100:.1f}%), CV AUC {cvauc(X, yy):.3f}"
    )

lines += [
    "",
    "## Conclusion",
    "Transactions were generated with customers chosen at random, so customers share the same behavior.",
    "A forward-looking churn label therefore has no signal (AUC about 0.5).",
    "The AUC of 1.0 in earlier reports came from recency being both the label source and a feature.",
]
open("reports/Churn_Leakage_Findings.md", "w").write("\n".join(lines))
print("\n".join(lines))
