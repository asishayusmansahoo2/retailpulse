# Prophet tuning results

Hyperparameters were chosen on two earlier 30-day validation windows.
The final MAPE is measured on the last 30 days, which were never used for training or tuning.

- Best config: changepoint_prior_scale=0.1, seasonality_mode=additive, monthly_seasonality=False
- Final holdout MAPE: 12.44% (target <= 12%)

## Top 5 configs by validation MAPE

- 10.19% (changepoint_prior_scale=0.1, mode=additive, monthly=False)
- 10.19% (changepoint_prior_scale=0.05, mode=multiplicative, monthly=False)
- 10.20% (changepoint_prior_scale=0.05, mode=additive, monthly=False)
- 10.22% (changepoint_prior_scale=0.01, mode=additive, monthly=False)
- 10.31% (changepoint_prior_scale=0.01, mode=multiplicative, monthly=False)
