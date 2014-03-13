from flask import Flask, redirect, url_for, session, request, jsonify, abort
from flask_oauthlib.client import OAuth
from pprint import pprint


def create_client(app):
    oauth = OAuth(app)

    remote = oauth.remote_app(
        'Awesome app 1',
        consumer_key='52a03d9982353569195f73eb',
        consumer_secret='gdmh48h14f',
        request_token_params={'scope': 'email'},
        base_url='http://127.0.0.1:5000/',
        request_token_url=None,
        access_token_method='GET',
        access_token_url='http://127.0.0.1:5000/oauth/token',
        authorize_url='http://127.0.0.1:5000/oauth/authorize'
    )

    @app.route('/')
    def index():
        if 'dev_token' in session:
            #ret = remote.get('email')
            ret = remote.get('getusers')
            pprint (ret)
            return jsonify(ret.data)
        return redirect(url_for('login'))

    @app.route('/login')
    def login():
        return remote.authorize(callback=url_for('authorized', _external=True))

    @app.route('/logout')
    def logout():
        session.pop('dev_token', None)
        return redirect(url_for('index'))

    @app.route('/authorized')
    @remote.authorized_handler
    def authorized(resp):
        if resp is None:
            return 'Access denied: error=%s' % (
                request.args['error']
            )
        if isinstance(resp, dict) and 'access_token' in resp:
            session['dev_token'] = (resp['access_token'], '')
            pprint (resp)
            return jsonify(resp)
        return str(resp)

    @app.route('/address')
    def address():
        ret = remote.get('address/hangzhou')
        if ret.status not in (200, 201):
            return abort(ret.status)
        return ret.raw_data

    @app.route('/method/<name>')
    def method(name):
        func = getattr(remote, name)
        ret = func('method')
        return ret.raw_data

    @remote.tokengetter
    def get_oauth_token():
        return session.get('dev_token')
        
    @app.route('/getusers')
    def get_users():
        ret = remote.get('/getusers')
        if ret.status not in (200,201):
            return abort(ret.status)
        return ret.raw_data

    return remote

    @app.route('/user')
    def get_users():
        ret = remote.get('/user')
        if ret.status not in (200,201):
            return abort(ret.status)
        return ret.raw_data

    return remote
    

# {
#   "access_token": "3iOizsZwn0Wh6gHyfIILX0wzfH1197", 
#   "refresh_token": "CJtwe3Pq8bd13uwYlA45gsvJ4aeSe5", 
#   "scope": "email", 
#   "token_type": "Bearer"
# }

if __name__ == '__main__':
    import os
    os.environ['DEBUG'] = 'true'
    # DEBUG=1 python oauth2_client.py
    app = Flask(__name__)
    app.debug = True
    app.secret_key = 'development'
    create_client(app)
    app.run(host='localhost', port=8000)