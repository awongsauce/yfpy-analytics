import pandas as pd
import re
import unicodedata
import requests
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Regex to find full name from pattern
def extract_full_name(text):
    match = re.search(r'"full":\s*"([^"]+)"', str(text))
    if match:
        return match.group(1)
    return None

# Stripping any unicode/accents from names in case need to merge with other lists
def strip_accents(text):
    if isinstance(text, str):
        return ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )
    return text

# Takes draft results and adds player names, league team names, and NBA team names
def expanded_draft_results(query):
    # Load in draft results, league teams, and league players after relevant queries
    df_draft = pd.DataFrame(query.get_league_draft_results())
    df_teams = pd.DataFrame(query.get_league_teams())
    df_players = pd.DataFrame(query.get_league_players())

    # Process draft results
    df_draft = df_draft.rename(columns={0: "Overall pick", 1: "Round", 2: "team_id", 3: "player_id"})

    # Process teams
    df_teams = df_teams.rename(columns={0: "team_id", 2: "Team"})
    df_team = df_teams[["team_id", "Team"]]

    # Process players
    df_players = df_players.rename(columns={0: "player_id", 2: "player_dict"})

    # Apply full name extraction
    df_players["full_name"] = df_players["player_dict"].apply(extract_full_name)

    # Regex to extract Team name, looking for any 3 capital letters in a row, ignoring injury tags and name suffixes
    #  Future code can use player codes or search from team list
    exceptions = 'INJ|III|GTD'
    regex_pattern = r'(?!' + exceptions + r')([A-Z]{3})'
    search_cols = df_players.columns.tolist()
    combined_series = df_players[search_cols].fillna('').astype(str).agg(' '.join, axis=1)
    df_players['Team code'] = combined_series.str.extract(regex_pattern)

    # Taking relevant columns
    df_p = df_players[["full_name", "player_id", 'Team code']]

    # Merging draft with player list
    df_draft_m = df_draft.merge(df_p, on='player_id', how="left")

    # Merging draft + player list with team list
    df_draft_m = df_draft_m.merge(df_team, on="team_id", how="left")



        # Apply
    df_draft_m["player_name_clean"] = df_draft_m["full_name"].apply(strip_accents)
    return (df_draft_m)

# Compares how the league drafted vs ADP of hashtagbasketball
def league_draft_vs_ADP(draft_results):
    df = draft_results

    # Get ADP data from hashtagbasketball

    url = "https://hashtagbasketball.com/fantasy-basketball-adp"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    tables = pd.read_html(response.text)

    df_adp = tables[0]
    df_adp

    """
    #Hashtag list updates with time, if prefer to use custom csv or excel file:

    df_adp = pd.read_csv('your_custom_ADP.csv')
    df_adp = pd.read_excel('your_custom_ADP.xlsx')
    """

    # Process names from hashtag list so they match yahoo's

    # strip accents
    df_adp["PLAYER"] = df_adp["PLAYER"].apply(strip_accents)

    # fix name mismatches from hashtag to yahoo, needs to be checked manually
    # will need to update for 2027 season
    df_adp["PLAYER"] = df_adp['PLAYER'].replace({
        'Jimmy Butler': 'Jimmy Butler III',
        'Alexandre Sarr': 'Alex Sarr',
        'Nicolas Claxton': 'Nic Claxton',
        'Hansen Yang': 'Yang Hansen'
    })

    df_draft_adp = df.merge(df_adp, left_on="player_name_clean", right_on='PLAYER', how='left')

    # Using blend here, but can choose Yahoo, ESPN, or fantrax instead
    df_draft_adp["BLEND"] = df_draft_adp["BLEND"].fillna('300')  # fill na values with 300

    # convert ADP from object to float
    df_draft_adp["BLEND"] = df_draft_adp["BLEND"].astype(float)

    # Calcualte difference of actual pick position from ADP
    df_draft_adp["ADP diff"] = df_draft_adp["BLEND"] - df_draft_adp["Overall pick"]

    # Graph ADP differences, grouped by team, x-axis is Round #, y-axis is ADP differences, labelling players picked above/below chosen threshhold

    fig, ax = plt.subplots(figsize=(12, 8))

    for team, group in df_draft_adp.groupby("Team"):
        # Plot dots
        plt.plot(group["Round"], group["ADP diff"],
                 marker='o', linestyle='', label=team)

        # Conditional labeling, set at +/- 15 difference from ADP
        for i, row in group.iterrows():
            if row["ADP diff"] > 15 or row["ADP diff"] < -15:
                plt.text(row["Round"], row["ADP diff"],
                         row["full_name"],  # the column to use for labels
                         fontsize=7, ha='right', va='bottom')
    ax.axhline(0, color='gray', lw=1, linestyle='--')

    """ Extra flavor text
    ax.text(1.02, 0.75, "Risers (reaches?)", transform=ax.transAxes,
            rotation=-90, fontsize=12, color='dodgerblue',
            va='center', ha='center')

    # Slips (negative)
    ax.text(1.02, 0.25, "Fallers (steals?)", transform=ax.transAxes,
            rotation=-90, fontsize=12, color='orangered',
            va='center', ha='center')
    """

    plt.xticks(df_draft_adp["Round"])
    plt.legend(title="Teams", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.xlabel("Round")
    plt.ylabel("ADP difference")
    plt.title("ADP Difference by Round and Team")
    plt.tight_layout()
    plt.show(block=False)

    # Give the option to save image
    save_option = input("Would you like to save the file? (y/n): ")

    if save_option.lower() == 'y':
        filename = input('What would you like to name the file? ')
        fig.savefig(filename + '.png')

    else:
        pass

    plt.close(fig)

    return df_draft_adp

#Take league matchups and make into readable dataframe
def week_results_concat_explode(df):
    # Regex to extract team names from matchups
    def team_name(text):
        match = re.findall(r'"name":\s*"([^"]+)"', text)
        if match:
            return match
        return None

    # Search all columns for stats
    search_cols = df.columns.tolist()
    combined_series = df[search_cols].fillna('').astype(str).agg(' '.join, axis=1)

    dfc = df.copy()

    # Apply regex to extract team name
    dfc['Team_name'] = combined_series.apply(team_name)

    # Explode team name column so 1 team per row
    df_exploded = dfc.explode('Team_name')
    df_exploded = df_exploded.reset_index(drop=True)

    # Map of [Stat name]: [Stat_ID]
    STAT_MAPPING = {
        'FG%': 5,
        'FT%': 8,
        '3PTM': 10,
        'PTS': 12,
        'REB': 15,
        'AST': 16,
        'STL': 17,
        'BLK': 18,
        'TO': 19,
    }

    # Regex pattern to find stat value
    BASE_PATTERN = r'("stat_id":\s*{stat_id},\s*"value":\s*)(\d*\.\d+|\d+)'

    # 1. Collect results as lists
    results_data = []

    for combined_string in combined_series:
        row_metrics = {}
        max_instances = 0

        for metric_name, stat_id in STAT_MAPPING.items():
            regex_pattern = BASE_PATTERN.format(stat_id=stat_id)
            # Get all values for this specific metric
            matches = [m[1] for m in re.findall(regex_pattern, combined_string)]
            row_metrics[metric_name] = matches
            # Track how many rows we need to create for this original entry
            max_instances = max(max_instances, len(matches))

        # Standardize length: ensure all lists are the same length by padding with None
        # This is crucial if Metric A appears twice but Metric B appears once
        for metric_name in row_metrics:
            while len(row_metrics[metric_name]) < max_instances:
                row_metrics[metric_name].append(None)

        results_data.append(row_metrics)

    # 2. Create a DataFrame where columns contain lists
    temp_df = pd.DataFrame(results_data)

    # 3. Use 'explode' to turn list elements into individual rows
    # We pass the list of all column names to explode them simultaneously
    df_stats = temp_df.explode(list(STAT_MAPPING.keys())).reset_index(drop=True)

    # 4. Join back to any metadata from your original df if needed
    # Note: Since the rows multiplied, you'd usually join on the index of the original df

    win_counts = []
    win_points = []

    # Join team name to week stats
    week_results = df_stats.join(df_exploded['Team_name'])

    # Convert FG% and FT% to float. Convert 3PTM, PTS, REB, AST, STL, BLK, and TO to int.
    float_columns = week_results.columns[0:2]
    int_columns = week_results.columns[2:9]

    week_results[float_columns] = week_results[float_columns].apply(pd.to_numeric, errors='coerce').astype(float)
    week_results[int_columns] = week_results[int_columns].apply(pd.to_numeric, errors='coerce').astype(int)

    for i in range(0, len(week_results), 2):
        cats_won1 = 0
        cats_won2 = 0
        win_points1 = 0
        win_points2 = 0

        diff = week_results.iloc[i, :-1] - week_results.iloc[i + 1, :-1]
        diff.iloc[-1] = diff.iloc[-1] * -1 # less turnovers is better so taking negative value here

        categories = week_results.columns[:-1]

        #totalling up how many categories were won in the week

        for j, cat in enumerate(categories):
            val = diff[j]
            if val > 0:
                cats_won1 += 1
                win_points1 += 1
            if val < 0:
                cats_won2 += 1
                win_points2 += 1
            elif val == 0: #for ties, count as 0.5 point for each team
                win_points1 += 0.5
                win_points2 += 0.5

        win_counts.append(cats_won1)
        win_counts.append(cats_won2)
        win_points.append(win_points1)
        win_points.append(win_points2)

    week_results['Cats_won'] = win_counts
    week_results['Win_points'] = win_points #for overall performance

    return week_results


# Create h2h charts

def h2h_charts(week_results):
    epsilon = 1e-6  # Small constant to prevent division by zero
    week_short = week_results.iloc[:, :-1]
    plt.style.use('default')

    for i in range(0, len(week_short), 2):
        team1 = week_short.iloc[i, -2]
        team2 = week_short.iloc[i + 1, -2]

        # Calculate normalized difference
        diff = week_short.iloc[i, :-2] - week_short.iloc[i + 1, :-2]
        total = week_short.iloc[i, :-2] + week_short.iloc[i + 1, :-2]

        # Taking negative volue of turnovers since less is better
        diff.iloc[-1] = diff.iloc[-1] * -1
        norm_diff = diff / (total + epsilon)

        categories = week_short.columns[:-2]
        y = np.arange(len(categories))
        colors = ['darkgreen' if x > 0 else 'darkred' for x in norm_diff]
        fig, ax = plt.subplots(figsize=(10, 6))

        # Horizontal bars
        ax.barh(y, norm_diff, color=colors)
        ax.axvline(0, color='gray', linestyle='--', linewidth=0.8)

        # Y-axis labels
        ax.set_yticks(y)
        ax.set_yticklabels(categories)
        ax.invert_yaxis()  # top category first

        # X-axis limits for normalization
        ax.set_xlim(-1, 1)

        # Place "vs" in the middle of the plot
        ax.text(0.5, 1.02, "vs", transform=ax.transAxes,
                fontsize=16, fontweight='bold', color='black',
                ha='center', va='center', alpha=0.7)

        ax.set_xlabel("Normalized difference")

        # Add stats as annotations
        for j, cat in enumerate(categories):
            score1 = week_short.iloc[i, j]
            score2 = week_short.iloc[i + 1, j]
            val = norm_diff[j]

            if val >= 0:
                x_pos = val + 0.02
                ha = 'left'
                color = 'darkgreen'
                annotation = f"({score1} vs {score2})"  # shows winning cat value first for winning side
            else:
                x_pos = val - 0.02
                ha = 'right'
                color = 'darkred'
                annotation = f"({score2} vs {score1})"

            ax.text(x_pos, j, annotation, va='center', ha=ha, color=color, fontsize=9)

        # ax.text(0.75, 1.02, team1 + ' (' + str(cats_won1) + ')', transform=ax.transAxes, color='darkgreen', fontsize=12, ha='center')
        # ax.text(0.25, 1.02, team2 + ' (' + str(cats_won2) + ')', transform=ax.transAxes, color='darkred', fontsize=12, ha='center')

        ax.text(0.75, 1.02, team1 + ' (' + str(week_short.iloc[i, -1]) + ')', transform=ax.transAxes, color='darkgreen',
                fontsize=12, ha='center')
        ax.text(0.25, 1.02, team2 + ' (' + str(week_short.iloc[i + 1, -1]) + ')', transform=ax.transAxes,
                color='darkred', fontsize=12, ha='center')

        filename = f"{team1} vs {team2}.png"



        plt.tight_layout()
        plt.show()

        save_option = input("Save these plots? (y/n): ").strip().lower()

        if save_option.lower() == 'y':

            fig.savefig(filename + '.png')



        else:
            print('Charts not saved')


# Creating a chart that normalizes all stats by comparing to the highest stat output of the week
def normalized_performance_chart(week_results):
    # more colors
    cmap = plt.get_cmap('tab20')

    week_short = week_results.iloc[:, :-2]
    cols_to_normalize = week_short.columns[:-1]  # choose all columns except team name and cats won
    df_basic = week_short.drop(columns=["TO"]).copy()
    df_basic[cols_to_normalize] = week_short[cols_to_normalize].apply(
        lambda col: ((col / col.max()) * 100 - 1)
    )

    df_basic["TO"] = week_short["TO"].min() / week_short["TO"] * 100 - 1

    df_melted_basic = df_basic.melt(id_vars='Team_name', var_name='Category', value_name='Value')

    # 1. Create a mapping for the categorical X-axis (Category -> Index)
    categories = df_melted_basic['Category'].unique()
    category_to_index = {name: i for i, name in enumerate(categories)}

    # 2. Map the Category strings to their new numeric index
    df_melted_basic['Category_Index'] = df_melted_basic['Category'].map(category_to_index)

    # --- Plotting ---
    fig = plt.figure(figsize=(14, 7))
    # plt.style.use('ggplot')

    # Loop through each team and plot its points
    """for team, data in df_melted_basic.groupby('Team_name'):
        plt.scatter(
            data['Category_Index'], # Plot the numeric index on X
            data['Value'],
            label=team,
            s=80, # size of the marker
            alpha=0.8
        )"""

    for i, (team, data) in enumerate(df_melted_basic.groupby('Team_name')):
        plt.scatter(
            data['Category_Index'],
            data['Value'],
            label=team,
            s=80,
            alpha=0.8,
            color=cmap(i % 20)  # 3. Assign the color using the index
        )



    labels_to_plot = df_melted_basic[df_melted_basic['Value'] > 90].copy()

    # Vertical shift constant (may need to tune this)
    VERTICAL_OFFSET = 1

    # Group the filtered data by the X-axis (Category_Index) for stacking
    for category_index, data_group in labels_to_plot.groupby('Category_Index'):
        # Sort by value so the highest-performing teams are labeled first
        data_group = data_group.sort_values(by='Value', ascending=False)

        # Initialize the offset for the current category
        # Start at -0.5 to center the labels near the top of the point
        current_offset_count = -0.5

        # Loop through the labels in this category to apply the stack
        for _, row in data_group.iterrows():
            # Calculate the Y position: base value minus the accumulated offset
            if row['Value'] == 99:
                label_y = row['Value'] - (current_offset_count * VERTICAL_OFFSET)

                # Plot the text label
                plt.text(
                    row['Category_Index'],  # Use the numeric index for X
                    label_y,
                    row['Team_name'],
                    fontsize=7,
                    ha='left',
                    va='top'  # Align the top of the text to the calculated position
                )

                # Increment the offset for the next label in the same category
                current_offset_count += 1

    # --- Final Plot Formatting ---
    plt.title("Team Performance by Category")
    plt.xlabel("Category")
    plt.ylabel("Value")

    # Set the X-ticks to use the correct category names
    plt.xticks(
        ticks=np.arange(len(categories)),  # Use the range of indices
        labels=categories,  # Use the actual category names
        rotation=45,
        ha='right'
    )

    plt.legend(title="Teams", bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()  # Adjust plot to make room for rotated labels

    plt.show()

    #Ask if want to save the outputted chart
    save_option = input("Save this chart? (y/n): ").strip().lower()

    if save_option.lower() == 'y':
        filename = input('What would you like to name the file? ')
        fig.savefig(filename + '-team-performance.png')


    else:
        print('Chart not saved')


# Creating a cat ranking heat map
def cat_heat_map_chart(week_results):
    week_short = week_results.iloc[:, :-2] #omit cats and points won
    cols_to_normalize = week_short.columns[:-1] # ignore team name
    df_ranked = week_short.copy()
    df_ranked[cols_to_normalize] = week_short[cols_to_normalize].rank(axis=0, ascending=True)
    df_ranked["TO"] = df_ranked["TO"].rank(ascending=False) #reverse order for turnovers

    df_ranked["SUM"] = df_ranked.sum(numeric_only=True, axis=1) #take sum of categories
    df_ranked_sort = df_ranked.sort_values(by=['SUM'], ascending=False) #sort by team with highest sum
    y_labels = df_ranked_sort["Team_name"]
    fig = plt.figure(figsize=(10, 6))
    sns.heatmap(df_ranked_sort.drop(columns=['SUM']).select_dtypes(include='number'), annot=True, cmap='coolwarm',
                yticklabels=y_labels)

    plt.title("Category rankings")
    plt.show()

    save_option = input("Save this chart? (y/n): ").strip().lower()

    if save_option.lower() == 'y':
        filename = input('What would you like to name the file? ')
        fig.savefig(filename + '-cat-heat-map.png',dpi=300, bbox_inches='tight')


    else:
        print('Chart not saved')

# Get league transactions
def get_transactions(query):
    trans_results = query.get_league_transactions()
    df = pd.DataFrame(trans_results)
    df = df.rename(columns={5: 'Log'})

    df = df.astype('string')  # convert object to string so can perform regex
    df["Log"] = df["Log"].apply(strip_accents)  # remove any accents from names
    df[4] = df[4].apply(strip_accents)

    return df

#Extract team name
def team_name(text):
    # Check if text is null or not a string
    if not isinstance(text, str):
        return None

    match = re.search(r'team_name":\s*"([^"]+)"', text)
    if match:
        return match.group(1)
    return None

# Extract team key in case team name changes
def team_key(text):
    # Check if text is null or not a string
    if not isinstance(text, str):
        return None

    # ... your existing logic for team_key ...
    match = re.search(r'team_key":\s*"([^"]+)"', text)
    if match:
        return match.group(1)
    return None

# Get player names for adds and drops
def extract_add_drop(text):
    if not isinstance(text, str):
        return pd.Series({"adds": "", "drops": ""})

    pattern = r'"full"\s*:\s*"([^"]+)"[\s\S]*?"type"\s*:\s*"(add|drop)"'
    matches = re.findall(pattern, text)

    adds = [name for name, t in matches if t == "add"]
    drops = [name for name, t in matches if t == "drop"]

    # Convert lists → comma-separated string (or empty)
    adds_str = ", ".join(adds)
    drops_str = ", ".join(drops)

    return pd.Series({"adds": adds_str, "drops": drops_str})

# Get nba team of player being added/dropped
def nba_team(text):
    if not isinstance(text, str):
        return None

    match = re.search(r'editorial_team_abbr":\s*"([^"]+)"', text)
    if match:
        return match.group(1)
    return None

# Get traded players infos
def extract_trade_info(text):
    text = str(text)
    return {
        "players": re.findall(r'"full":\s*"([^"]+)"', text),
        "destinations": re.findall(r'"destination_team_name":\s*"([^"]+)"', text),
        "sources": re.findall(r'"source_team_name":\s*"([^"]+)"', text),
    }

# Modifies transaction dataframe and adds information
def insert_transact_info(df):
    df[['adds', 'drops']] = df['Log'].apply(extract_add_drop)
    df["Team name"] = df['Log'].apply(team_name)
    df["Team key"] = df['Log'].apply(team_key)
    df["NBA team"] = df['Log'].apply(nba_team)

    trade_info = df.iloc[:, 9].apply(extract_trade_info)

    # Maximum number of players in any trade
    max_players = trade_info.apply(lambda x: len(x["players"])).max()

    # Create columns dynamically
    for i in range(max_players):
        df[f"player_{i + 1}"] = trade_info.apply(
            lambda x: x["players"][i] if i < len(x["players"]) else None
        )

        df[f"destination_team_{i + 1}"] = trade_info.apply(
            lambda x: x["destinations"][i] if i < len(x["destinations"]) else None
        )

        df[f"source_team_{i + 1}"] = trade_info.apply(
            lambda x: x["sources"][i] if i < len(x["sources"]) else None
        )

    # convert seconds into readable time format
    df[4] = df[4].astype(int)
    df['PST datetime'] = (pd.to_datetime(df[4], unit='s').dt.tz_localize('utc').dt.tz_convert('America/Los_Angeles'))

    return df

# Below functions need to be tested

# Gives results of every week from 1 until current week and adds up cumulative points
def full_season_standings(current_week):
    all_weeks = {}

    # Get all matchups results from week1 1 to current week

    current_week_plus_one = current_week + 1

    for week in range(1, current_week_plus_one):
        # Fetch data
        league_matchups = query.get_league_matchups_by_week(week)
        df_raw = pd.DataFrame(league_matchups)

        # Process data using your existing function
        # Note: Ensure week_results_concat_explode is defined in your script
        processed_df = week_results_concat_explode(df_raw)

        # 3. Store in dictionary with the week number as the key
        all_weeks[week] = processed_df

    # Append list of lists of all weeks into a single dataframe

    all_data_list = []

    for week, df in all_weeks.items():
        # Make sure we know which week this is
        df['week'] = week
        all_data_list.append(df)

    # Create one big DataFrame
    full_season_df = pd.concat(all_data_list, ignore_index=True)

    # 1. Sort to ensure weeks are in order (1, 2, 3...)
    full_season_df = full_season_df.sort_values(['Team_name', 'week'])

    # 2. Calculate the cumulative sum of categories won grouped by Team
    full_season_df['cum_points'] = full_season_df.groupby('Team_name')['Win_points'].cumsum()



    return full_season_df


# Chart overall season standings, week by week
def season_standings_chart(full_season_df):
    # 2. Find the max 'cum_wins' for EACH week
    # .transform('max') broadcasts the week's highest score to every row in that week
    full_season_df['week_leader_score'] = full_season_df.groupby('week')['cum_points'].transform('max')

    # 3. Calculate the "Games Behind" (Difference from Max)
    # We use (Max - Team Score) so the leader is at 0 and others are positive numbers behind
    full_season_df['games_behind'] = full_season_df['week_leader_score'] - full_season_df['cum_points']

    # Get the 'tab20' colormap
    cmap = plt.get_cmap('tab20')

    filename = 'Season_long'
    # 1. Pivot the data so each team has its own column
    # Rows = Week, Columns = Team Names, Values = Games Behind
    plot_data = full_season_df.pivot(index='week', columns='Team_name', values='games_behind')

    # 2. Create the plot
    plt.figure(figsize=(14, 7))

    """
    # Plot each team line
    for team in plot_data.columns:
        plt.plot(plot_data.index, plot_data[team], marker='o', label=team, linewidth=2)
    """
    for i, team in enumerate(plot_data.columns):
        # i % 20 ensures it stays within the index range if you have >20 teams
        color = cmap(i % 20)
        plt.plot(plot_data.index, plot_data[team], marker='o', label=team, linewidth=2, color=color)

    # 3. Flip the Y-axis so 0 (the leader) is at the top
    plt.gca().invert_yaxis()

    # 4. Final touches (Labels, Grid, Legend)
    plt.title('Overall League Standings by Week (Cumulative)', fontsize=14, pad=15)
    plt.xlabel('Week', fontsize=12)
    plt.ylabel('Games Behind', fontsize=12)
    plt.xticks(plot_data.index)  # Ensure every week shows on x-axis
    plt.grid(True, linestyle='--', alpha=0.7)

    # Place legend outside the chart so it doesn't block the lines
    plt.legend(title='Teams', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

    save_option = input("Save this chart? (y/n): ").strip().lower()

    if save_option.lower() == 'y':
        filename = input('What would you like to name the file? ')
        fig.savefig(filename + '-cumulative-standings.png', dpi=300, bbox_inches='tight')


    else:
        print('Chart not saved')