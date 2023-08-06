import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the data
df = pd.read_csv('/Users/m237958/Downloads/COVID_output.csv')

# Binning the age variable
bins = [18, 30, 40, 50, 60, 70, 80, 90]
labels = ['18-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89']
df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)

# List of variables for ridge plot
variables = ['sex', 'WHO_Region', 'race', 'age_group', 'ethnic_group']

# Function to create ridge plot for a given y-axis
def create_ridge_plot(y_axis):
    for variable in variables:
        unique_values = df[variable].dropna().unique()
        colors = sns.color_palette("tab10", n_colors=len(unique_values))
        fig, axes = plt.subplots(nrows=len(unique_values), sharex=True, figsize=(10, 6))
        plt.suptitle(f'Ridge Plot of {variable} vs {y_axis}', y=1.02)
        for i, value in enumerate(unique_values):
            subset = df[df[variable] == value]
            sns.kdeplot(x=y_axis, data=subset, shade=True, lw=1.5, alpha=0.7, color=colors[i], ax=axes[i])
            axes[i].text(0.95, 0.5, str(value), ha='center', va='center', transform=axes[i].transAxes, rotation=0)
            axes[i].set_yticks([])
            axes[i].set_ylabel('')
            sns.despine(left=True, ax=axes[i]) # Despine left side to remove Y-axis lines
        plt.show()

# Creating the ridge plot for "day_prior_covid19_symptoms"
create_ridge_plot("day_prior_covid19_symptoms")

# Creating the ridge plot for "days_prior_covid_testing"
create_ridge_plot("days_prior_covid_testing")



import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the data
path = "/Users/m237958/Downloads/WHOscoresID.csv"
df = pd.read_csv(path)

# Combine WHO scores into one variable
df['WHOscore'] = df[['WHOscore3', 'WHOscore4', 'WHOscore5', 'WHOscore6', 'WHOscore7', 'WHOscore8']].sum(axis=1)

# Binning the 'days_prior_covid_testing' variable
bins = [float('-inf'), -1, 5, 10, 14, float('inf')]
labels = ['negative', '0-5', '5-10', '10-14', '14 plus']
df['days_prior'] = pd.cut(df['days_prior_covid_testing'], bins=bins, labels=labels, right=False)

# Group the data by 'days_prior' and 'WHOscore', and count the number of occurrences
sankey_data = df.groupby(['days_prior', 'WHOscore']).size().reset_index(name='count')

# Pivot the data to get 'WHOscore' in the columns and 'days_prior' in the index
heatmap_data = sankey_data.pivot(index='days_prior', columns='WHOscore', values='count').fillna(0)

# Plot the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu', fmt='.0f') # Changed fmt to '.0f' to display numbers without exponential notation
plt.title('WHO Score by Days Prior to COVID Testing')
plt.ylabel('Days Prior to Testing')
plt.xlabel('WHO Score')
plt.show()
