import pandas as pd

# Load the datasets
combined_data_path = '/Users/jaejunku/Desktop/HLA-1-Data-Keskin/combined_data.csv'
hla_sequence_path = '/Users/jaejunku/Desktop/HLA-1-Data-Keskin/keskin_common_hla_sequence.csv'

combined_df = pd.read_csv(combined_data_path)
hla_sequence_df = pd.read_csv(hla_sequence_path)

combined_df = combined_df.loc[:, ~combined_df.columns.str.contains('^Unnamed')]

# Drop the existing HLA_sequence column if it exists
if 'HLA_sequence' in combined_df.columns:
    combined_df = combined_df.drop(columns=['HLA_sequence'])

# Merge HLA sequences with the combined data
merged_df = pd.merge(combined_df, hla_sequence_df, on='HLA', how='left')

# Print HLA IDs that don't have a match
unmatched_hlas = merged_df[merged_df['HLA_sequence'].isna()]['HLA'].unique()
if len(unmatched_hlas) > 0:
    print("HLA IDs without a match:")
    print(unmatched_hlas)
else:
    print("All HLA IDs have matches.")

# Fill NaN HLA sequences with a placeholder text (if desired)
merged_df['HLA_sequence'] = merged_df['HLA_sequence'].fillna('NO_SEQUENCE_FOUND')

# Reindex the combined DataFrame
merged_df.reset_index(drop=True, inplace=True)

# Randomly shuffle the data
# shuffled_df = merged_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save the final combined DataFrame with HLA sequences to a new CSV file
output_file_path = '/Users/jaejunku/Desktop/HLA-1-Data-Keskin/final_combined_data.csv'
merged_df.to_csv(output_file_path, index=True)

print(f"Combined data with HLA sequences saved to {output_file_path}")
