import pandas as pd


# Converting the string data to a dataframe
df = pd.read_csv('../data_analyse/data_result/all_data-3.csv')

# Columns to convert to percentages
columns_to_convert = ['Swap Space', 'Idle Memory', 'Buffer', 'Cache']

# Calculate the total for the columns to be converted
total = df[columns_to_convert].sum(axis=1)[0]

# Convert the specified columns to percentages
for column in columns_to_convert:
    df[column] = (df[column] / total) * 100

# Save the dataframe to a csv file
df.to_csv('../data_analyse/data_result/all_data-3.csv', index=False)
