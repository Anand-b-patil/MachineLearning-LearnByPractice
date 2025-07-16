import pickle
from flask import Flask, request, render_template

app = Flask(__name__)

# Load the trained model and scaler once
model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        cgpa = float(request.form['cgpa'])
        iq = float(request.form['iq'])
    except ValueError:
        return render_template('index.html', prediction_text="Invalid input. Please enter numeric values.")

    features = scaler.transform([[cgpa, iq]])
    prediction = model.predict(features)
    result = 'Placed' if prediction[0] == 1 else 'Not Placed'
    return render_template('index.html', prediction_text=f'Student will be: {result}')

if __name__ == "__main__":
    app.run(debug=True)
