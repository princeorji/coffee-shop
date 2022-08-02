import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

# ROUTES
@app.route('/drinks')
def drinks():
    data = Drink.query.all()
    drinks = [drink.short() for drink in data]

    return jsonify({
        'success': True,
        'drinks': drinks
    })

@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def drink_details(token):
    data = Drink.query.all()
    drinks = [drink.long() for drink in data]

    return jsonify({
        'success': True,
        'drinks': drinks
    })

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(token):
    drink = request.get_json()
    try:
        drink = Drink(
            name = drink.get('name', None),
            recipe = drink.get('recipe', None)
        )
        drink.insert()
        
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except:
        abort(422)

@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(token, drink_id):
    drink = request.get_json()
    try:
        drink = Drink.query.filter(Drink.id==drink_id).one_or_none()
        if drink is None:
            abort(404)

        drink.title = drink.get('title')
        drink.recipe = drink.get('recipe')        
        drink.update()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except:
        abort(422)

@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(token, drink_id):
    try:
        drink = Drink.query.filter(Drink.id==drink_id).one_or_none()
        if drink is None:
            abort(404)

        drink.delete()

        return jsonify({
            'success': True,
            'delete': drink_id,
            })
    except:
        abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "page not found"
    }), 404


@app.errorhandler(AuthError)
def not_authenticated(auth_error):
    return jsonify({
        "success": False,
        "error": auth_error.status_code,
        "message": auth_error.error
    }), 401
