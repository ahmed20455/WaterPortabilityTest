from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

API_KEY = "jlrICNWYSlTqFdEs-iBzRL00d57u6W-lze-Q_CWgTJDh"
MODEL_ENDPOINT = 'https://eu-de.ml.cloud.ibm.com/ml/v4/deployments/2fe7ba46-e045-48ba-a9e4-9e65aad15d84/predictions?version=2021-05-01'

def get_access_token(api_key):
    token_response = requests.post(
        'https://iam.cloud.ibm.com/identity/token', 
        data={
            "apikey": api_key, 
            "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'
        }
    )
    return token_response.json()["access_token"]

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/Aboutus')
def about():
    return render_template("About.html")

@app.route('/diseases')
def disease():
    return render_template("disease.html")

# @app.route('/submit', methods=['POST'])
# def submit():
#     ph = request.form['ph']
#     hardness = request.form['hardness']
#     solids = request.form['solids']
#     chloramines = request.form['chloramines']
#     sulfate = request.form['sulfate']
#     conductivity = request.form['conductivity']
#     organic_carbon = request.form['organic_carbon']
#     trihalomethanes = request.form['trihalomethanes']
#     turbidity = request.form['turbidity']

#     array_of_input_fields = [
#         "ph", "Hardness", "Solids", "Chloramines", 
#         "Sulfate", "Conductivity", "Organic_carbon", 
#         "Trihalomethanes", "Turbidity"
#     ]
#     array_of_values_to_be_scored = [
#         [ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity]
#     ]

#     payload_scoring = {
#         "input_data": [
#             {
#                 "fields": array_of_input_fields, 
#                 "values": array_of_values_to_be_scored
#             }
#         ]
#     }

#     mltoken = get_access_token(API_KEY)
#     response_scoring = requests.post(
#         MODEL_ENDPOINT, 
#         json=payload_scoring,
#         headers={'Authorization': 'Bearer ' + mltoken}
#     )

#     return jsonify(response_scoring.json())

@app.route('/submit', methods=['POST'])
def submit():
    try:
        ph = request.form['ph']
        hardness = request.form['hardness']
        solids = request.form['solids']
        chloramines = request.form['chloramines']
        sulfate = request.form['sulfate']
        conductivity = request.form['conductivity']
        organic_carbon = request.form['organic_carbon']
        trihalomethanes = request.form['trihalomethanes']
        turbidity = request.form['turbidity']

        # Prepare input for model prediction
        payload_scoring = {
            "input_data": [
                {
                    "fields": ["ph", "Hardness", "Solids", "Chloramines", "Sulfate", "Conductivity", "Organic_carbon", "Trihalomethanes", "Turbidity"],
                    "values": [
                        [float(ph), float(hardness), float(solids), float(chloramines), float(sulfate), float(conductivity), float(organic_carbon), float(trihalomethanes), float(turbidity)]
                    ]
                }
            ]
        }

        # Get access token
        mltoken = get_access_token(API_KEY)

        # Call model API for prediction
        response_scoring = requests.post(
            MODEL_ENDPOINT,
            json=payload_scoring,
            headers={'Authorization': 'Bearer ' + mltoken}
        )

        # Parse prediction result
        prediction_result = response_scoring.json()["predictions"][0]["values"][0][0]

        # Render result page with form data and prediction result
        return render_template('result.html', 
                               ph=ph, hardness=hardness, solids=solids, 
                               chloramines=chloramines, sulfate=sulfate, 
                               conductivity=conductivity, organic_carbon=organic_carbon, 
                               trihalomethanes=trihalomethanes, turbidity=turbidity, 
                               prediction=prediction_result)

    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
