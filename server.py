from flask import Flask, request, jsonify, render_template
import util
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('app.html')
@app.route('/get_location_names')
def get_location_names():
    locations = util.get_location_names()
    print("DEBUG - Locations from util:", locations)  # 🔍 Debug line

    response = jsonify({
        'locations': locations
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/get_estimated_price', methods=['POST'])
def get_estimated_price():
    total_sqft = request.form.get('total_sqft')
    location = request.form.get('location')
    bhk = request.form.get('bhk')
    bath = request.form.get('bath')

    print("Received input:", total_sqft, location, bhk, bath)  # Debug line

    if not all([total_sqft, location, bhk, bath]):
        return jsonify({'error': 'Missing required parameters'}), 400

    try:
        total_sqft = float(total_sqft)
        bhk = int(bhk)
        bath = int(bath)
    except ValueError:
        return jsonify({'error': 'Invalid input type'}), 400

    response = jsonify({
        'estimated_price': util.get_estimated_price(location, total_sqft, bhk, bath)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    print("Server started sucessfully.")
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)

