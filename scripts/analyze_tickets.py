import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_PATH = Path("data/tickets_dataset.csv")
OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_PATH, parse_dates=["created_date", "resolved_date"])

# KPI globaux
total_tickets = len(df)
resolved_tickets = df["status"].isin(["Resolved", "Closed"]).sum()
open_tickets = df["status"].isin(["Open", "In Progress"]).sum()
resolution_avg = df["resolution_time_hours"].mean()
sla_breach_rate = df["sla_breached"].mean() * 100
satisfaction_avg = df["user_satisfaction"].mean()

summary = pd.DataFrame({
    "metric": [
        "Total tickets",
        "Resolved/Closed tickets",
        "Open/In Progress tickets",
        "Average resolution time (hours)",
        "SLA breach rate (%)",
        "Average user satisfaction"
    ],
    "value": [
        total_tickets,
        resolved_tickets,
        open_tickets,
        round(resolution_avg, 2),
        round(sla_breach_rate, 2),
        round(satisfaction_avg, 2)
    ]
})

summary.to_csv("data/kpi_summary.csv", index=False)

# Performance par équipe
team_perf = (
    df.groupby("assigned_team")
    .agg(
        tickets=("ticket_id", "count"),
        avg_resolution_hours=("resolution_time_hours", "mean"),
        sla_breach_rate=("sla_breached", "mean"),
        avg_satisfaction=("user_satisfaction", "mean")
    )
    .reset_index()
)

team_perf["avg_resolution_hours"] = team_perf["avg_resolution_hours"].round(2)
team_perf["sla_breach_rate"] = (team_perf["sla_breach_rate"] * 100).round(2)
team_perf["avg_satisfaction"] = team_perf["avg_satisfaction"].round(2)
team_perf.to_csv("data/team_performance.csv", index=False)

# Performance par catégorie
category_perf = (
    df.groupby("category")
    .agg(
        tickets=("ticket_id", "count"),
        avg_resolution_hours=("resolution_time_hours", "mean"),
        sla_breach_rate=("sla_breached", "mean")
    )
    .reset_index()
)

category_perf["avg_resolution_hours"] = category_perf["avg_resolution_hours"].round(2)
category_perf["sla_breach_rate"] = (category_perf["sla_breach_rate"] * 100).round(2)
category_perf.to_csv("data/category_performance.csv", index=False)

# Volume quotidien
daily_tickets = (
    df.groupby(df["created_date"].dt.date)
    .size()
    .reset_index(name="ticket_count")
)
daily_tickets.to_csv("data/daily_ticket_volume.csv", index=False)

# Graphique 1 : tickets par priorité
priority_counts = df["priority"].value_counts()
plt.figure(figsize=(8, 5))
priority_counts.plot(kind="bar")
plt.title("Tickets by Priority")
plt.xlabel("Priority")
plt.ylabel("Number of Tickets")
plt.tight_layout()
plt.savefig("data/tickets_by_priority.png")
plt.close()

# Graphique 2 : tickets par équipe
team_counts = df["assigned_team"].value_counts()
plt.figure(figsize=(8, 5))
team_counts.plot(kind="bar")
plt.title("Tickets by Assigned Team")
plt.xlabel("Team")
plt.ylabel("Number of Tickets")
plt.tight_layout()
plt.savefig("data/tickets_by_team.png")
plt.close()

# Graphique 3 : volume de tickets dans le temps
plt.figure(figsize=(10, 5))
plt.plot(pd.to_datetime(daily_tickets["created_date"]), daily_tickets["ticket_count"])
plt.title("Daily Ticket Volume")
plt.xlabel("Date")
plt.ylabel("Number of Tickets")
plt.tight_layout()
plt.savefig("data/daily_ticket_volume.png")
plt.close()

print("Analysis completed.")
print("\n=== KPI SUMMARY ===")
print(summary)
print("\n=== TEAM PERFORMANCE ===")
print(team_perf)
print("\n=== CATEGORY PERFORMANCE ===")
print(category_perf)