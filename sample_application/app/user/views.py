import datetime
import json

from flask import Blueprint, request, Response, render_template, \
                  flash, g, session, redirect, url_for, jsonify
from flask import current_app
from flask.views import MethodView

user_module = Blueprint('user', __name__, url_prefix='')


class UserView(MethodView):

    def get(self, user_id):
        """
        Function: get
        Get user details

        Parameters:
        self - default param
        user_id - Id of the user

        Returns:
        response_obj - response object
        """
        response = Response(headers={})
        response.headers['Content-Type'] = 'application/json'

        response.status_code = 200
        response.data = json.dumps(dict(
            success = True,
            message = 'Done!',
            results = []
        ))
        return response