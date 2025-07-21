import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set Seaborn style
sns.set(style="darkgrid")

# Title
st.title("IPL Cricket EDA Dashboard")

# Upload datasets
st.sidebar.header("Upload Datasets")
matches_file = st.sidebar.file_uploader("Upload matches.csv", type=["csv"])
deliveries_file = st.sidebar.file_uploader("Upload deliveries.csv", type=["csv"])

if matches_file is not None and deliveries_file is not None:
    matches = pd.read_csv(matches_file)
    deliveries = pd.read_csv(deliveries_file)

    # Clean matches data
    matches['winner'].fillna('No Result', inplace=True)
    if 'umpire3' in matches.columns:
        matches.drop(['umpire3'], axis=1, inplace=True)

    st.sidebar.success("Datasets loaded successfully!")

    # Tabs for navigation
    tab1, tab2, tab3, tab4 = st.tabs(["Team Wins", " Toss Analysis", "Player Stats", " Season Insights"])

    with tab1:
        st.subheader("Most Matches Won by Teams")
        wins = matches['winner'].value_counts()
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=wins.index, y=wins.values, hue=wins.index, palette="viridis", dodge=False, legend=False, ax=ax)
        plt.xticks(rotation=45)
        plt.ylabel("Total Wins")
        plt.xlabel("Team")
        st.pyplot(fig)

        if 'win_by_runs' in matches.columns:
            st.subheader("Win by Runs Distribution")
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            sns.histplot(matches['win_by_runs'], bins=30, kde=True, color='orange', ax=ax2)
            st.pyplot(fig2)

        if 'win_by_wickets' in matches.columns:
            st.subheader("Win by Wickets Distribution")
            fig3, ax3 = plt.subplots(figsize=(10, 5))
            sns.histplot(matches['win_by_wickets'], bins=30, kde=True, color='purple', ax=ax3)
            st.pyplot(fig3)

    with tab2:
        st.subheader("Toss Impact Analysis")
        toss_match_win = matches[matches['toss_winner'] == matches['winner']]
        toss_win_percent = len(toss_match_win) / len(matches) * 100
        st.metric("Toss Winner also won match (%)", f"{toss_win_percent:.2f}%")

        if 'toss_decision' in matches.columns:
            st.subheader("Toss Decision Trends")
            fig4, ax4 = plt.subplots(figsize=(8, 5))
            sns.countplot(data=matches, x='toss_decision', hue='toss_winner', ax=ax4)
            plt.xticks(rotation=0)
            st.pyplot(fig4)

    with tab3:
        st.subheader("Top 10 Run Scorers")
        if 'batsman' in deliveries.columns and 'batsman_runs' in deliveries.columns:
            top_scorers = deliveries.groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False).head(10)
            fig5, ax5 = plt.subplots(figsize=(10, 5))
            sns.barplot(x=top_scorers.index, y=top_scorers.values, palette="crest", ax=ax5)
            plt.xticks(rotation=45)
            st.pyplot(fig5)

        st.subheader("Top 10 Wicket Takers")
        if 'bowler' in deliveries.columns and 'dismissal_kind' in deliveries.columns:
            dismissals = deliveries[deliveries['dismissal_kind'].notnull()]
            top_wickets = dismissals.groupby('bowler').size().sort_values(ascending=False).head(10)
            fig6, ax6 = plt.subplots(figsize=(10, 5))
            sns.barplot(x=top_wickets.index, y=top_wickets.values, palette="rocket", ax=ax6)
            plt.xticks(rotation=45)
            st.pyplot(fig6)

    with tab4:
        st.subheader("Matches Played Per Season")
        if 'season' in matches.columns:
            season_count = matches['season'].value_counts().sort_index()
            fig7, ax7 = plt.subplots(figsize=(10, 5))
            sns.barplot(x=season_count.index, y=season_count.values, palette="mako", ax=ax7)
            st.pyplot(fig7)

else:
    st.info("Please upload both matches.csv and deliveries.csv files from the IPL Kaggle dataset.")
