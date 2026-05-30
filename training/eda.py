import pandas as pd

df = pd.read_csv("../data/fake_job_postings.csv")

print("Dataset Shape:")
print(df.shape)

print("\nMissing Values:")
print(
    df.isnull()
      .sum()
      .sort_values(ascending=False)
)
print("\nClass Distribution:")
print(
    df["fraudulent"]
      .value_counts()
)
fraud_pct = df["fraudulent"].mean() * 100
print(f"\nFraud Percentage: {fraud_pct:.2f}%")