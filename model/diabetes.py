# Import Required Libraries
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
from ucimlrepo import fetch_ucirepo

class DiabetesModel:
    """A class used to represent the Diabetes Model for predicting diabetes status (healthy, pre-diabetic, diabetic)."""
    _instance = None
    
    def __init__(self):
        self.model = None
        # Updated feature names to match the dataset columns
        self.features = ['HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'Stroke', 
                         'HeartDiseaseorAttack', 'PhysActivity']
        self.target = 'Diabetes_binary'
        
        # Fetch the CDC diabetes dataset
        cdc_diabetes_health_indicators = fetch_ucirepo(id=891)
        self.data = pd.concat([cdc_diabetes_health_indicators.data.features, cdc_diabetes_health_indicators.data.targets], axis=1)
        
    def _clean(self):
        """Clean and prepare the dataset for model training."""
        # Handle missing values by dropping any rows with missing data
        self.data.dropna(inplace=True)
        
        # Check if the 'Sex' column exists in the dataset and handle it
        if 'Sex' in self.data.columns:
            # Convert binary columns to integers (1 for male, 0 for female)
            self.data['Sex'] = self.data['Sex'].apply(lambda x: 1 if x == 'male' else 0)
        else:
            print("Warning: 'Sex' column not found in the dataset.")

    def _train(self):
        """Train the diabetes model using logistic regression."""
        X = self.data[self.features]
        y = self.data[self.target]
        
        # Split into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        # Initialize and train logistic regression model
        self.model = LogisticRegression(max_iter=1000)
        self.model.fit(X_train, y_train)
        
        # Make predictions on the test set
        y_pred = self.model.predict(X_test)
        
        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        print(f'Model Accuracy: {accuracy:.2f}')
        
    @classmethod
    def get_instance(cls):
        """Get, clean, and train the diabetes model."""
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._clean()
            cls._instance._train()
        return cls._instance

    def predict(self, patient_data):
        """Predict diabetes status for a new patient."""
        # Convert input data to DataFrame
        patient_df = pd.DataFrame(patient_data, index=[0])
        
        # Predict using the trained model
        prediction = self.model.predict(patient_df)  # Ensure it returns an array
        
        return int(prediction) if isinstance(prediction, (np.int64, int)) else int(prediction[0])



def initDiabetesModel():
    """ Initialize the Diabetes Model. """
    DiabetesModel.get_instance()

def testDiabetesModel():
    """ Test the Diabetes Model with a new patient's data. """
    
    # Define a new patient's data
    patient = {
        'highbp': [1], 
        'highchol': [0], 
        'cholcheck': [1], 
        'bmi': [30], 
        'smoker': [0], 
        'stroke': [0], 
        'heartdiseaseorattack': [0], 
        'physactivity': [1]
    }

    # Get an instance of the trained DiabetesModel
    diabetesModel = DiabetesModel.get_instance()

    # Make a prediction
    prediction = diabetesModel.predict(patient)
    print(f"Diabetes Prediction: {prediction[0]}")  # 0 for healthy, 1 for pre-diabetic/diabetic

if __name__ == "__main__":
    print("Initializing Diabetes Model...")
    initDiabetesModel()
    
    print("Testing Diabetes Model...")
    testDiabetesModel()
