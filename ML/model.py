from flaml import AutoML
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Chargez le dataset
data = pd.read_csv("data_sepsis.csv")

# Créez un objet AutoML
automl = AutoML()
# Définissez les paramètres de AutoML
automl_settings = {
    "time_budget": 10,  # in seconds
    "metric": 'accuracy',
    "task": 'classification'
}

X = data.drop(['ID', 'Sepssis'], axis=1) # Supprimez les colonnes ID et Sepssis
y = data['Sepssis']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) # Divisez le dataset en train et test
automl.fit(X_train=X_train, y_train=y_train,**automl_settings) # Entraînez le modèle
print('Best ML leaner:', automl.best_estimator) # Affichez le meilleur modèle
print('Best hyperparmeter config:', automl.best_config) # Affichez la meilleure configuration
print('Best accuracy on validation data: {0:.4g}'.format(1-automl.best_loss)) # Affichez la meilleure accuracy
print('Training duration of best run: {0:.4g} s'.format(automl.best_config_train_time)) # Affichez le temps d'entraînement du meilleur modèle

y_pred = automl.predict(X_test) # Faites des prédictions sur le test set
accuracy = accuracy_score(y_test, y_pred) # Calculez l'accuracy
print(f"Accuracy: {accuracy:.2f}") # Affichez l'accuracy
print(classification_report(y_test, y_pred)) # Affichez le rapport de classification

joblib.dump(automl, 'sepsis_model.pkl') # Sauvegardez le modèle