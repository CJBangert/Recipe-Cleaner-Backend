from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

import recipe_scraper

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/getShortRecipe", methods=['GET'])
def getShortRecipe():
    print(request)
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400
    parsed = recipe_scraper.get_recipe(url)

    return parsed

