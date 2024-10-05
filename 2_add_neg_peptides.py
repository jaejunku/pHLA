import pandas as pd
import random

# Load the positive peptide-HLA dataset
keskin_data_path = '/Users/jaejunku/Desktop/HLA-1-Data-Keskin/all_positive_keskin_data.csv'
keskin_df = pd.read_csv(keskin_data_path)

# Remove the "Unnamed: 0" column if it exists
if 'Unnamed: 0' in keskin_df.columns:
    keskin_df = keskin_df.drop(columns=['Unnamed: 0'])

# Set to store existing peptide-HLA combinations
existing_combinations = set(zip(keskin_df['peptide'], keskin_df['HLA']))

# List to store rows of the combined DataFrame
combined_data = []

# List to store error messages
error_messages = []

# Total rows to process for progress tracking
total_rows = len(keskin_df)

# Define amino acid mapping and prior probabilities
aa2int_mapping = {"A": 0, "C": 1, "D": 2, "E": 3, "F": 4,
                  "G": 5, "H": 6, "I": 7, "K": 8, "L": 9,
                  "M": 10, "N": 11, "P": 12, "Q": 13, "R": 14,
                  "S": 15, "T": 16, "V": 17, "W": 18, "Y": 19}
aa_prior = [0.0777, 0.0157, 0.0530, 0.0656, 0.0405,
            0.0691, 0.0227, 0.0591, 0.0595, 0.0960,
            0.0238, 0.0427, 0.0469, 0.0393, 0.0526,
            0.0694, 0.0550, 0.0667, 0.0118, 0.0311]
aa_order = list(aa2int_mapping.keys())

# Define decoy generator class
class generate_decoy:
    def __init__(self, aa_order, aa_prior):
        self.aa_prior = aa_prior
        self.aa_order = aa_order

    def generate_one(self, length):
        return ''.join(random.choices(self.aa_order, weights=self.aa_prior, k=length))

    def generate_n(self, length, n: int):
        return list(set([self.generate_one(length) for _ in range(n)]))

# Instantiate the decoy generator
decoy_generator = generate_decoy(aa_order, aa_prior)

# Iterate through each row in keskin_df
for index, row in keskin_df.iterrows():
    length = row['length']
    hla = row['HLA']
    
    # Add the original positive row to the combined data list
    combined_data.append(row)
    
    # Generate 5 negative decoys
    decoy_peptides = decoy_generator.generate_n(length, 5)
    
    # Add the decoy peptides to the combined data list with label 0
    for epitope_subset in decoy_peptides:
        new_row = {
            'peptide': epitope_subset,
            'length': length,
            'HLA': hla,
            'label': 0,
            'HLA_sequence': row['HLA_sequence']
        }
        combined_data.append(pd.Series(new_row))
    
    # Print progress
    if (index + 1) % 5000 == 0 or index + 1 == total_rows:
        print(f"Processed {index + 1}/{total_rows} rows")

# Create a DataFrame from the combined data list
combined_df = pd.DataFrame(combined_data)

# Check for duplicate peptide-HLA combinations
duplicate_rows = combined_df[combined_df.duplicated(subset=['peptide', 'HLA'], keep=False)]

if not duplicate_rows.empty:
    print("Duplicate peptide-HLA combinations found:")
    print(duplicate_rows[['peptide', 'HLA']])
else:
    print("No duplicate peptide-HLA combinations found.")

# Print the number of peptides by length
peptide_length_counts = combined_df['length'].value_counts().sort_index()
print("\nNumber of peptides by length:")
print(peptide_length_counts)

# Print the number of peptides by label (1 for positive, 0 for negative)
label_counts = combined_df['label'].value_counts()
print("\nNumber of peptides by label (1 for positive, 0 for negative):")
print(label_counts)

# Print the number of HLA alleles by their first letter (A, B, C, G)
hla_first_letter_counts = combined_df['HLA'].str[4].value_counts()  # 'HLA-' starts at index 4
print("\nNumber of HLA alleles by first letter (A, B, C, G):")
print(hla_first_letter_counts)

# Save the final combined DataFrame to a new CSV file
output_file_path = '/Users/jaejunku/Desktop/HLA-1-Data-Keskin/combined_data.csv'
combined_df.to_csv(output_file_path, index=True)

print(f"Combined data saved to {output_file_path}")

