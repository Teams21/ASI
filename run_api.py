import gradio as gr
from autogluon.tabular import TabularPredictor
import pandas as pd

# Load the pre-trained AutoGluon model
predictor = TabularPredictor.load('data/05_models/model/')

def predict(path: str):
    df = pd.read_csv(path)
    predictions = predictor.predict(df)
    # Convert predictions to DataFrame if necessary
    if not isinstance(predictions, pd.DataFrame):
        predictions = predictions.to_frame(name="Predictions")
        predictions['Class'] = df['Class']
        predictions['Result'] = predictions['Predictions'] == predictions['Class']

    # Save predictions to a CSV file
    csv_path = 'predictions.csv'
    predictions.to_csv(csv_path, index=False)

    return predictions, csv_path

iface = gr.Interface(
    fn=predict,
    inputs='file',  # Changed to 'file' to allow CSV file uploads
    outputs=[
        gr.Dataframe(label="Predictions"),  # Display the predictions as a DataFrame
        gr.File(label="Download Predictions CSV")  # Allow downloading the predictions CSV
    ],
    title="AutoGluon Model Prediction",
    description="Upload a CSV file to predict using an AutoGluon model."
)

# Run the Gradio app
if __name__ == "__main__":
    iface.launch(share=True)
