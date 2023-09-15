import nlpaug.augmenter.word as naw
import pandas as pd
from sklearn.utils import shuffle

# Define the augmenter
aug = naw.SynonymAug(aug_src='wordnet')

# Define the number of samples per class you want
samples_per_class = 600

# Get the unique labels
unique_labels = df['label'].unique()

# Initialize an empty DataFrame to store the augmented data
augmented_data = pd.DataFrame(columns=df.columns)

# Loop over each unique label
for label in unique_labels:
    # Get all rows with this label
    label_df = df[df['label'] == label]

    # If this label has less than the desired number of samples
    if len(label_df) < samples_per_class:
        # Calculate the number of new samples needed
        new_samples_needed = samples_per_class - len(label_df)

        # Initialize an empty list to store the new samples
        new_samples = []

        # Loop until we have enough new samples
        for _ in range(new_samples_needed):
            # Randomly select a sample from the label_df
            sample = label_df.sample(1)

            # Augment the text of this sample
            augmented_text = aug.augment(sample['Body'].values[0])

            # Add the augmented sample to the new_samples list
            new_samples.append([augmented_text, label])

        # Convert the new_samples list to a DataFrame and append it to the label_df
        new_samples_df = pd.DataFrame(new_samples, columns=['Body', 'label'])
        label_df = pd.concat([label_df, new_samples_df], ignore_index=True)

    # Append the label_df to the augmented_data DataFrame
    augmented_data = pd.concat([augmented_data, label_df], ignore_index=True)

# Shuffle the augmented_data DataFrame
augmented_data = shuffle(augmented_data)

# Reset the index of the augmented_data DataFrame
augmented_data.reset_index(drop=True, inplace=True)

augmented_data.to_csv('augmented_data.csv', index=False)