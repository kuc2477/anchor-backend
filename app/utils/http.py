from flask import jsonify


def error(reason, code=400, **kwargs):
    payload = {'reason': reason}
    payload.update(kwargs)
    return jsonify(payload), code

def message(message, code=200, **kwargs):
    payload = {'message': message}
    payload.update(kwargs)
    return jsonify(payload), code
