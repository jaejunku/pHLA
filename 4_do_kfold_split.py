import pandas as pd
from sklearn.model_selection import KFold, train_test_split

# Function to print counts and ratios
def print_counts_and_ratios(series, description):
    counts = series.value_counts().sort_index()
    total = len(series)
    ratios = (counts / total) * 100
    print(f"\n{description} Counts:\n{counts}")
    print(f"\n{description} Ratios (%):\n{ratios.round(2)}")


# Load the combined data, dropping any "Unnamed: 0" column if it exists
data = pd.read_csv("final_combined_data.csv").drop(columns=['Unnamed: 0'], errors='ignore')

print("\nOriginal Data Summary:")
print(f"Total samples: {len(data)}")
print_counts_and_ratios(data['label'], 'Label (1: positive, 0: negative)')
print_counts_and_ratios(data['length'], 'Peptide Length')

# First, split off 10% of the data as the independent set
train_test_data, independent_data = train_test_split(data, test_size=0.1, random_state=39)

# Re-index the independent set and save it, with index included
output_dir = "Keskin_Data/"
independent_file_name = "keskin_independent_data.csv"
independent_data = independent_data.reset_index(drop=True)  # Reset index to start from 0
independent_data.to_csv(output_dir + independent_file_name, index=True)  # Include index in the output file
print(f"Independent set saved: {independent_file_name}")

# Print summary of the independent set
print("\nIndependent Set Summary:")
print(f"Total samples: {len(independent_data)}")
print_counts_and_ratios(independent_data['label'], 'Label (1: positive, 0: negative)')
print_counts_and_ratios(independent_data['length'], 'Peptide Length')

# Define the number of folds for k-fold cross-validation on the remaining 90% (train + test)
kf = KFold(n_splits=5, shuffle=True, random_state=39)

# Initialize fold counter
fold = 0

# Perform k-fold cross-validation on the remaining 90% of the data
for train_index, test_index in kf.split(train_test_data):
    # Split the train_test_data into training and testing sets for this fold
    train_data = train_test_data.iloc[train_index].reset_index(drop=True)  # Reset index to start from 0
    test_data = train_test_data.iloc[test_index].reset_index(drop=True)  # Reset index to start from 0

    # Print summary of the current fold
    print(f"\nFold {fold} Summary:")
    
    print(f"Training set: {len(train_data)} samples")
    print_counts_and_ratios(train_data['label'], 'Training Label (1: positive, 0: negative)')
    print_counts_and_ratios(train_data['length'], 'Training Peptide Length')

    hla_first_letter_train = train_data['HLA'].str[4]
    print_counts_and_ratios(hla_first_letter_train, 'Training HLA alleles by first letter (A, B, C, G)')
    
    print(f"Testing set: {len(test_data)} samples")
    print_counts_and_ratios(test_data['label'], 'Testing Label (1: positive, 0: negative)')
    print_counts_and_ratios(test_data['length'], 'Testing Peptide Length')

    hla_first_letter_test = test_data['HLA'].str[4]
    print_counts_and_ratios(hla_first_letter_test, 'Testing HLA alleles by first letter (A, B, C, G)')

    # Define output file names for training and testing sets
    train_file_name = f"keskin_train_data_fold{fold}.csv"
    test_file_name = f"keskin_val_data_fold{fold}.csv"
    
    # Save the training and testing sets to CSV files, with index included
    train_data.to_csv(output_dir + train_file_name, index=True)  # Include index
    test_data.to_csv(output_dir + test_file_name, index=True)  # Include index

    print(f"Fold {fold} train indices: {train_index[:10]} ...")  # Print first 10 indices for brevity
    print(f"Fold {fold} test indices: {test_index[:10]} ...")   # Print first 10 indices for brevity
    
    # Print completion message for the current fold
    print(f"Fold {fold} data saved: {train_file_name}, {test_file_name}")
    
    # Increment fold counter
    fold += 1

# Notify completion
print("5-fold cross-validation data split and files saved.")
