import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# Load the data
df = pd.read_csv('countypres_2000-2020.csv')

# Filter for 2020 election and the two candidates
df = df[(df['year'] == 2020) & ((df['candidate'] == 'JOSEPH R BIDEN JR') | (df['candidate'] == 'DONALD J TRUMP'))]

# Separate the vote counts for each candidate
trump_votes = df[df['candidate'] == 'DONALD J TRUMP']['candidatevotes'].values
biden_votes = df[df['candidate'] == 'JOSEPH R BIDEN JR']['candidatevotes'].values

# Function to count leading digits
def count_leading_digits(votes):
    digit_count = defaultdict(int)
    for vote in votes:
        if vote > 0:  # Only count positive vote counts
            leading_digit = int(str(vote)[0])
            digit_count[leading_digit] += 1
    return digit_count

# Count leading digits
trump_digit_count = count_leading_digits(trump_votes)
biden_digit_count = count_leading_digits(biden_votes)

# Create bar charts
fig, ax = plt.subplots(1, 2, figsize=(16, 6))

ax[0].bar(trump_digit_count.keys(), trump_digit_count.values())
ax[0].set_title('Trump Vote Counts Leading Digit Distribution')
ax[0].set_xlabel('Digits')
ax[0].set_ylabel('Frequency')

ax[1].bar(biden_digit_count.keys(), biden_digit_count.values())
ax[1].set_title('Biden Vote Counts Leading Digit Distribution')
ax[1].set_xlabel('Digits')
ax[1].set_ylabel('Frequency')

plt.show()
