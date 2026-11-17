import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

df = pd.read_csv("data/customers_segmented.csv")
X = np.log1p(df[["recency", "frequency", "monetary"]])
Xs = StandardScaler().fit_transform(X)

km = KMeans(n_clusters=6, random_state=42, n_init=10)
df["kmeans_cluster"] = km.fit_predict(Xs)
print("Silhouette (k=6):", round(silhouette_score(Xs, df["kmeans_cluster"]), 3))

# Rank clusters by an RFM value score: high frequency + high spend + low recency
g = df.groupby("kmeans_cluster")[["recency", "frequency", "monetary"]].mean()
z = (g - g.mean()) / g.std(ddof=0)
score = z["frequency"] + z["monetary"] - z["recency"]
order = score.sort_values(ascending=False).index.tolist()
names = [
    "Champions",
    "Loyal Customers",
    "Slipping Loyalists",
    "Promising",
    "At Risk",
    "Hibernating",
]
df["segment"] = df["kmeans_cluster"].map(dict(zip(order, names)))
df.to_csv("data/customers_segmented.csv", index=False)

summary = (
    df.groupby("segment")
    .agg(
        customers=("customer_id", "count"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_monetary=("monetary", "mean"),
    )
    .round(1)
    .reindex(names)
)
print(summary)
