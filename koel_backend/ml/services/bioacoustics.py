'''
testbed for bioacoustics model
'''
import torch
import pandas as pd
from opensoundscape import load_model
import tensorflow as tf


# model = load_model('./BirdNET_GLOBAL_6K_V2.4_Model_FP16.tflite')
model = torch.hub.load('kitzeslab/bioacoustics-model-zoo', 'BirdNET',trust_repo=True)
# model = torch.hub.load('./BirdNET_GLOBAL_6K_V2.4_Model_FP16.tflite', 'BirdNET',trust_repo=True)

# predictions = model.predict(['test.mp3']) # predict on the model's classes
predictions = model.predict(['STRAW-HEADED-BULBUL.mp3']) # predict on the model's classes
# embeddings = model.generate_embeddings(['One Hour Forest 1 mins.mp3']) # generate embeddings on each 5 sec of audio



print(predictions)
# Convert predictions to a pandas DataFrame
# Assuming predictions are in a list of dictionaries
predictions_df = pd.DataFrame(predictions)

# Save predictions to a CSV file
predictions_csv_file = 'predictions1.csv'
predictions_df.to_csv(predictions_csv_file, index=False)

print(f"Predictions saved to {predictions_csv_file}")

# Filter columns with positive values
positive_columns = predictions_df.columns[(predictions_df > 0).any()].tolist()

# Include start_time and end_time in the list of columns to return
relevant_columns = positive_columns

# Filter the DataFrame to include only the relevant columns
filtered_df = predictions_df[relevant_columns]

# Print the filtered DataFrame
print(filtered_df)

if positive_columns == None:
    print("Headers with positive values: None")

else:
    print("Headers with positive values:", positive_columns)
    print(filtered_df)

# print(embeddings)