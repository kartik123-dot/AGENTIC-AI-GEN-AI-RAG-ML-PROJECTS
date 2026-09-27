import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

dataset = pd.read_csv(
    r"D:\my_python\33_investment_dataset_practice\House_data.csv"
)

# Column at index 4 is the value to predict
y = dataset.iloc[:, 4]
x = dataset.drop(columns=dataset.columns[4])

# Convert text categories into numeric columns
x = pd.get_dummies(x, dtype=int)

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=0
)

regressor = LinearRegression()
regressor.fit(x_train, y_train)

y_pred = regressor.predict(x_test)

print("Coefficients:", regressor.coef_)
print("Intercept:", regressor.intercept_)

comparison = pd.DataFrame({
    "Actual": y_test.to_numpy(),
    "Predicted": y_pred
})
print(comparison)


bias = regressor.score(x_train, y_train)
bias

variance = regressor.score(x_test, y_test)
variance

# After regressor.fit(x_train, y_train)
model_path = r"D:\my_python\33_investment_dataset_practice\house_model.pkl"

with open(model_path, "wb") as file:
    pickle.dump({
        "model": regressor,
        "feature_columns": x.columns.tolist()
    }, file)

print("Model saved:", model_path)