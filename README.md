# Car MPG Predictor

Predict the fuel efficiency (Miles Per Gallon - MPG) of a car using Machine Learning.

This project uses the classic Automobile MPG dataset to train regression models capable of estimating a vehicle's fuel efficiency based on its technical specifications. After experimenting with multiple algorithms, a Random Forest Regressor was selected as the final model due to its superior predictive performance.

---

## Features

- Predicts vehicle MPG using technical specifications
- Data cleaning and preprocessing pipeline
- Exploratory Data Analysis (EDA)
- Model comparison
  - Linear Regression
  - Random Forest Regressor
- Performance evaluation using multiple regression metrics
- Model serialization using Joblib
- Ready for deployment with Streamlit

---

## Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- Joblib

---

## Project Structure

```
Car-MPG-Predictor/
│
├── Automobile.csv              # Dataset
├── Car_Price_Predictor.ipynb   # Training notebook
├── car_mpg_model.pkl           # Trained Random Forest model
├── origin_encoder.pkl          # Label encoder
├── requirements.txt
└── README.md
```

---

## Dataset

The dataset contains information about automobiles including:

- Cylinders
- Displacement
- Horsepower
- Weight
- Acceleration
- Model Year
- Origin

Target Variable:

- MPG (Miles Per Gallon)

---

## Workflow

1. Load dataset
2. Explore and visualize data
3. Handle missing values
4. Encode categorical features
5. Split data into training and testing sets
6. Train multiple regression models
7. Compare performance
8. Save the best model
9. Make predictions on new data

---

## Exploratory Data Analysis

The notebook includes:

- MPG distribution
- Weight vs MPG
- Horsepower vs MPG
- Correlation heatmap
- MPG by number of cylinders
- Prediction error distribution

---

## Machine Learning Models

### Linear Regression

Used as a baseline model.

### Random Forest Regressor

Selected as the final model due to better prediction accuracy and stronger generalization.

---

## Evaluation Metrics

The models were evaluated using:

- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- R² Score

The Random Forest model achieved the best overall performance.

---

## Saved Model

The trained model is stored using Joblib.

```
car_mpg_model.pkl
```

The label encoder is also saved:

```
origin_encoder.pkl
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/yourusername/car-mpg-predictor.git
```

Move into the project

```bash
cd car-mpg-predictor
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the notebook

```bash
jupyter notebook
```

---

## Sample Prediction

Example input

| Feature | Value |
|---------|------:|
| Cylinders | 4 |
| Displacement | 150 |
| Horsepower | 100 |
| Weight | 2500 |
| Acceleration | 15 |
| Model Year | 70 |
| Origin | USA |

The trained model predicts the expected MPG for the vehicle.

---

## Author

**Priyanshi Saxena**
- GitHub: https://github.com/Priyanshi248

---
