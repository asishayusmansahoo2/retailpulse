# Churn Model: Leakage Check

## Original label (recency > 90)
- With recency + segment as features: AUC 1.000 (label leakage)
- Without recency + segment: AUC 0.612

## Forward-looking label (features before cutoff, label after cutoff)
- 30-day window: 413 churners (20.6%), CV AUC 0.540
- 45-day window: 197 churners (9.8%), CV AUC 0.485
- 60-day window: 70 churners (3.5%), CV AUC 0.482

## Conclusion
Transactions were generated with customers chosen at random, so customers share the same behavior.
A forward-looking churn label therefore has no signal (AUC about 0.5).
The AUC of 1.0 in earlier reports came from recency being both the label source and a feature.