# Sepsis Prediction API

This project implements a Flask-based API for predicting sepsis in patients using machine learning. The API provides endpoints for health checking and making predictions based on patient data.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Setup](#setup)
3. [API Endpoints](#api-endpoints)
4. [Machine Learning Model](#machine-learning-model)
5. [Testing](#testing)

## Project Structure

The project is organized as follows:

- `main.py`: The entry point of the application, setting up the Flask app and Swagger documentation.
- `ML/`: Directory containing machine learning related files.
  - `data_sepsis.csv`: Dataset used for training the model.
  - `model.py`: Script for training and saving the machine learning model.
- `routes/`: Directory containing API route definitions.
  - `predict.py`: Defines the prediction and health check routes.
- `tests/`: Directory containing unit tests.
  - `test_predict.py`: Tests for the API routes.

## Setup

To set up the project:

1. Install required dependencies (Flask, flasgger, pandas, scikit-learn, joblib).
2. Run `model.py` to train and save the machine learning model.
3. Start the Flask application by running `main.py`.

## API Endpoints

The API provides the following endpoints:

1. `GET /health_check`: Returns the health status of the API.
2. `POST /predict/patient`: Accepts patient data and returns a sepsis prediction.

For detailed API documentation, access the Swagger UI when running the application.

## Machine Learning Model

The sepsis prediction model is trained using AutoML from the FLAML library. It automatically selects the best machine learning algorithm and hyperparameters based on the provided dataset.

Key features of the model training process:
- Uses accuracy as the optimization metric
- Has a time budget of 10 seconds for AutoML
- Performs a train-test split (80% train, 20% test)
- Saves the best model for later use in predictions

## Testing

Unit tests are provided in `tests/test_predict.py`. These tests cover:
- Health check endpoint
- Prediction endpoint with valid input
- Prediction endpoint with missing fields
- Prediction endpoint with invalid input types

Run the tests using a Python test runner like pytest.
