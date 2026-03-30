import pandas as pd
import numpy as np

np.random.seed(42)
n = 1200

priorities = ["Low", "Medium", "High", "Critical"]
ticket_types = ["Incident", "Request"]
categories = ["CRM", "Sales Tool", "Reporting", "Access Management", "B2B App"]
teams = ["L1", "L2", "L3"]
statuses = ["Open", "In Progress", "Resolved", "Closed"]

created_dates = pd.date_range(start="2025-01-01", periods=n, freq="6H")

df = pd.DataFrame({
    "ticket_id": [f"TCKT-{i:05d}" for i in range(1, n + 1)],
    "created_date": np.random.choice(created_dates, n),
    "priority": np.random.choice(priorities, n, p=[0.3, 0.4, 0.2, 0.1]),
    "ticket_type": np.random.choice(ticket_types, n, p=[0.65, 0.35]),
    "category": np.random.choice(categories, n),
    "assigned_team": np.random.choice(teams, n, p=[0.55, 0.3, 0.15]),
    "status": np.random.choice(statuses, n, p=[0.1, 0.15, 0.45, 0.3]),
    "user_satisfaction": np.random.randint(1, 6, n)
})

resolution_map = {
    "Low": (4, 24),
    "Medium": (8, 48),
    "High": (12, 72),
    "Critical": (24, 96)
}

resolution_times = []
for p in df["priority"]:
    low, high = resolution_map[p]
    resolution_times.append(np.random.randint(low, high + 1))

df["resolution_time_hours"] = resolution_times
df["created_date"] = pd.to_datetime(df["created_date"])
df["resolved_date"] = df["created_date"] + pd.to_timedelta(df["resolution_time_hours"], unit="h")

sla_threshold = {
    "Low": 24,
    "Medium": 48,
    "High": 72,
    "Critical": 48
}

df["sla_breached"] = df.apply(
    lambda row: row["resolution_time_hours"] > sla_threshold[row["priority"]],
    axis=1
)

open_statuses = ["Open", "In Progress"]
df.loc[df["status"].isin(open_statuses), "resolved_date"] = pd.NaT

df = df.sort_values("created_date").reset_index(drop=True)

df.to_csv("data/tickets_dataset.csv", index=False)
print("Dataset generated: data/tickets_dataset.csv")
print(df.head())