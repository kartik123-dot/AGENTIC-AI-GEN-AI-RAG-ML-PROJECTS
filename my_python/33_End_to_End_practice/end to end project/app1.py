# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import joblib

app = Flask(__name__)

model = joblib.load(
    r"D:\project\end to end project\student_mark_predictor.pkl"
)
model.positive = False

df = pd.DataFrame()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    global df

    try:
        input_features = [float(x) for x in request.form.values()]

        if len(input_features) != 1:
            raise ValueError

    except ValueError:
        return render_template(
            'index.html',
            prediction_text='Please enter your study hours.'
        )

    study_hours = input_features[0]

    if study_hours <= 0 or study_hours > 24:
        return render_template(
            'index.html',
            prediction_text='Please enter study hours between 1 and 24.'
        )

    features_value = np.array(input_features).reshape(1, -1)
    output = round(float(model.predict(features_value).ravel()[0]), 2)

    new_row = pd.DataFrame({
        'Study Hours': [study_hours],
        'Predicted Output': [output]
    })

    df = pd.concat([df, new_row], ignore_index=True)
    print(df)

    df.to_csv(
        r"D:\project\end to end project\smp_data_from_app.csv",
        index=False
    )

    return render_template(
        'index.html',
        prediction_text=f'You will get {output}% marks when you study {study_hours:g} hours per day.'
    )


if __name__ == "__main__":
    app.run(host='127.0.0.1')