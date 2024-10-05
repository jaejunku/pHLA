import pandas as pd

# Load the CSV file
input_file_path = '/Users/jaejunku/Desktop/HLA-1-Data-Keskin/Keskin_pos_peptides.csv'
df = pd.read_csv(input_file_path)

# Create the new DataFrame with the required columns
df['peptide'] = df['Peptide']
df['length'] = df['Length']
df['HLA'] = 'HLA-' + df['Allele'].str[:1] + '*' + df['Allele'].str[1:3] + ':' + df['Allele'].str[3:]
df['label'] = 1
df['HLA_sequence'] = ''  # Empty HLA_sequence column

# Print the number of peptides by length
peptide_length_counts = df['length'].value_counts().sort_index()
print("Number of peptides by length:")
print(peptide_length_counts)

# Print the number of HLA alleles by their first letter (A, B, C, G)
hla_first_letter_counts = df['Allele'].str[0].value_counts()
print("\nNumber of HLA alleles by first letter (A, B, C, G):")
print(hla_first_letter_counts)


# Reorder the columns to match the desired output
output_df = df[['peptide', 'length', 'HLA', 'label', 'HLA_sequence']]

# Save to the new CSV file with index as the first column and unnamed
output_file_path = '/Users/jaejunku/Desktop/HLA-1-Data-Keskin/all_positive_keskin_data.csv'
output_df.to_csv(output_file_path, index=True, index_label='')


print(f"Converted data saved to {output_file_path}")