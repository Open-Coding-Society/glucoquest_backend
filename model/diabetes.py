from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.calibration import CalibratedClassifierCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
from ucimlrepo import fetch_ucirepo
import joblib

class DiabetesModel:
    """A class for predicting diabetes risk with probability outputs (0-100%)."""
    
    _instance = None
    
    def __init__(self):
        self.model = None
        self.features = ['HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 
                        'Stroke', 'HeartDiseaseorAttack', 'PhysActivity',
                        'Age', 'GenHlth', 'MentHlth', 'PhysHlth', 'DiffWalk',
                        'Sex', 'Income']
        self.target = 'Diabetes_binary'
        self.scaler = StandardScaler()
        self._load_data()
        self._clean()
        self._train()
        
    def _load_data(self):
        """Load and prepare the dataset."""
        cdc_diabetes = fetch_ucirepo(id=891)
        self.data = pd.concat([cdc_diabetes.data.features, 
                              cdc_diabetes.data.targets], axis=1)
        
        # Sample a subset if the full dataset is too large
        self.data = self.data.sample(frac=0.3, random_state=42) if len(self.data) > 100000 else self.data
        
    def _clean(self):
        """Clean and preprocess the data."""
        # Handle missing values
        self.data.dropna(inplace=True)
        
        # Feature engineering
        self.data['BMI_Category'] = pd.cut(self.data['BMI'],
                                         bins=[0, 18.5, 25, 30, 35, 40, 100],
                                         labels=['underweight', 'normal', 'overweight',
                                                'obese1', 'obese2', 'obese3'])
        
        # Convert categorical to dummy variables
        self.data = pd.get_dummies(self.data, columns=['BMI_Category'], drop_first=True)
        self.features.extend([col for col in self.data.columns if 'BMI_Category_' in col])
        
    def _train(self):
        """Train the model with probability calibration."""
        X = self.data[self.features]
        y = self.data[self.target]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y)
        
        # Create model pipeline
        model = Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', GradientBoostingClassifier(
                n_estimators=200,
                learning_rate=0.05,
                max_depth=5,
                random_state=42
            ))
        ])
        
        # Calibrate for better probability estimates
        self.model = CalibratedClassifierCV(model, method='isotonic', cv=3)
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        y_proba = self.model.predict_proba(X_test)[:, 1]
        
        print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
        print(f"AUC-ROC: {roc_auc_score(y_test, y_proba):.3f}")
        print(classification_report(y_test, y_pred))
        
    @classmethod
    def get_instance(cls):
        """Get singleton instance of the model."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def predict(self, patient_data):
        """
        Predict diabetes probability (0-1 scale).
        
        Args:
            patient_data: Dict of patient features
            
        Returns:
            float: Probability of diabetes (0-1)
        """
        # Convert to DataFrame and ensure all features are present
        patient_df = pd.DataFrame(patient_data, index=[0])
        
        # Add missing features with default values
        for feat in self.features:
            if feat not in patient_df.columns:
                if 'BMI_Category_' in feat:
                    patient_df[feat] = 0  # Default to not in this category
                else:
                    patient_df[feat] = 0  # Default value for other missing features
        
        # Ensure correct column order
        patient_df = patient_df[self.features]
        
        # Predict probability
        probability = self.model.predict_proba(patient_df)[0, 1]
        return float(probability)

    def save_model(self, path='diabetes_model.pkl'):
        """Save the trained model to disk."""
        joblib.dump(self.model, path)
        
    @classmethod
    def load_model(cls, path='diabetes_model.pkl'):
        """Load a trained model from disk."""
        cls._instance = cls()
        cls._instance.model = joblib.load(path)
        return cls._instance


def initDiabetesModel():
    """Initialize and train the diabetes model."""
    print("Initializing Diabetes Model...")
    DiabetesModel.get_instance()
    print("Model training complete.")

def testDiabetesModel():
    """Test the model with sample patient data."""
    # Sample patient data - should include all expected features
    patient = {
        'HighBP': 1,
        'HighChol': 0,
        'CholCheck': 1,
        'BMI': 30,
        'Smoker': 0,
        'Stroke': 0,
        'HeartDiseaseorAttack': 0,
        'PhysActivity': 1,
        'Age': 45,
        'GenHlth': 3,
        'MentHlth': 5,
        'PhysHlth': 2,
        'DiffWalk': 0,
        'Sex': 1,
        'Income': 6
    }
    
    # Add BMI categories (will be 0 for all except the correct one)
    bmi = patient['BMI']
    if bmi < 18.5:
        patient['BMI_Category_underweight'] = 1
    elif 18.5 <= bmi < 25:
        patient['BMI_Category_normal'] = 1
    elif 25 <= bmi < 30:
        patient['BMI_Category_overweight'] = 1
    elif 30 <= bmi < 35:
        patient['BMI_Category_obese1'] = 1
    elif 35 <= bmi < 40:
        patient['BMI_Category_obese2'] = 1
    else:
        patient['BMI_Category_obese3'] = 1
    
    model = DiabetesModel.get_instance()
    probability = model.predict(patient)
    
    print(f"\nTest Patient Prediction:")
    print(f"Diabetes Probability: {probability:.1%}")
    print(f"Risk Level: {'High' if probability > 0.7 else 'Medium' if probability > 0.3 else 'Low'}")

if __name__ == "__main__":
    initDiabetesModel()
    testDiabetesModel()