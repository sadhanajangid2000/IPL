import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn style
sns.set(style="darkgrid")

# Load datasets
matches = pd.read_csv("matches.csv")
deliveries = pd.read_csv("deliveries.csv")

# View available columns
print("Matches Columns:", matches.columns)
print("Deliveries Columns:", deliveries.columns)

# Data Cleaning
matches['winner'].fillna('No Result', inplace=True)
if 'umpire3' in matches.columns:
    matches.drop(['umpire3'], axis=1, inplace=True)

# 1. Most Matches Won by Teams
plt.figure(figsize=(12,6))
wins = matches['winner'].value_counts()
sns.barplot(x=wins.index, y=wins.values, hue=wins.index, palette="viridis", dodge=False, legend=False)
plt.xticks(rotation=45)
plt.title('Most Matches Won by Teams')
plt.ylabel('Total Wins')
plt.xlabel('Team')
plt.tight_layout()
plt.show()

# 2. Win by Runs Distribution
if 'win_by_runs' in matches.columns:
    plt.figure(figsize=(10,5))
    sns.histplot(matches['win_by_runs'], bins=30, kde=True, color='orange')
    plt.title('Distribution of Win by Runs')
    plt.xlabel('Win by Runs')
    plt.ylabel('Number of Matches')
    plt.tight_layout()
    plt.show()
else:
    print(" Column 'win_by_runs' not found in matches.csv.")

# 3. Win by Wickets Distribution
if 'win_by_wickets' in matches.columns:
    plt.figure(figsize=(10,5))
    sns.histplot(matches['win_by_wickets'], bins=30, kde=True, color='purple')
    plt.title('Distribution of Win by Wickets')
    plt.xlabel('Win by Wickets')
    plt.ylabel('Number of Matches')
    plt.tight_layout()
    plt.show()
else:
    print(" Column 'win_by_wickets' not found in matches.csv.")

# 4. Toss Impact Analysis
if 'toss_winner' in matches.columns and 'winner' in matches.columns:
    toss_match_win = matches[matches['toss_winner'] == matches['winner']]
    toss_win_percent = len(toss_match_win) / len(matches) * 100
    print(f"Toss Impact: {toss_win_percent:.2f}% of toss winners also won the match.")

    if 'toss_decision' in matches.columns:
        plt.figure(figsize=(8,5))
        sns.countplot(data=matches, x='toss_decision', hue='toss_winner', legend=False)
        plt.title('Toss Decision Trends')
        plt.xlabel('Toss Decision')
        plt.tight_layout()
        plt.show()

# 5. Top 10 Run Scorers
if 'batsman' in deliveries.columns and 'batsman_runs' in deliveries.columns:
    top_scorers = deliveries.groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(10,5))
    sns.barplot(x=top_scorers.index, y=top_scorers.values, palette="crest")
    plt.title("Top 10 Run Scorers")
    plt.ylabel("Total Runs")
    plt.xlabel("Batsman")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# 6. Top 10 Wicket Takers
if 'bowler' in deliveries.columns and 'dismissal_kind' in deliveries.columns:
    dismissals = deliveries[deliveries['dismissal_kind'].notnull()]
    top_wickets = dismissals.groupby('bowler').size().sort_values(ascending=False).head(10)
    plt.figure(figsize=(10,5))
    sns.barplot(x=top_wickets.index, y=top_wickets.values, palette="rocket")
    plt.title("Top 10 Wicket Takers")
    plt.ylabel("Wickets Taken")
    plt.xlabel("Bowler")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# 7. Matches per Season
if 'season' in matches.columns:
    season_count = matches['season'].value_counts().sort_index()
    plt.figure(figsize=(10,5))
    sns.barplot(x=season_count.index, y=season_count.values, palette="mako")
    plt.title("Matches Played Per Season")
    plt.xlabel("Season")
    plt.ylabel("Number of Matches")
    plt.tight_layout()
    plt.show()
