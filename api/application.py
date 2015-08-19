from api import app, db
from api import routing
from api import config
from api import views
from api.provider import MyProvider


def setup_config(_app):
    _app.secret_key = 'secret'
    _app.debug = True
    _app.config.update({
        'SQLALCHEMY_DATABASE_URI': config.SQLALCHEMY_DATABASE_URI
    })
    return _app


def setup_routing(_app):
    def _add_routing(p, o):
        view_class = o.get('class')
        view_name = o.get('name')
        view_methods = o.get('methods')
        view_func = view_class.as_view(view_name)

        _app.add_url_rule(p, view_func=view_func, methods=view_methods)

    for (pattern, options) in routing.routing.items():
        if isinstance(options, dict):
            options = [options]
        for option in options:
            if not option.get('oauth'):
                _add_routing(pattern, option)

    return _app


def setup_oauth_routes(_app, _oauth):
    def _add_oauth_required(o):
        view_class = o.get('class')
        view_name = o.get('name')
        view_fnx = view_class.as_view(view_name)

        decorator = _oauth.require_oauth()
        return decorator(view_fnx)

    def _add_routing(p, o, v):
        view_methods = o.get('methods')
        _app.add_url_rule(p, view_func=v, methods=view_methods)

    for (pattern, options) in routing.routing.items():
        if isinstance(options, dict):
            options = [options]

        for option in options:
            if option.get('oauth'):
                view_func = _add_oauth_required(option)
                _add_routing(pattern, option, view_func)

    return _app, _oauth


def setup_oauth_handlers(_app, _oauth):
    authorize_handler_fnx = views.AuthorizeView.as_view('authorize')
    authorize_handler_decorated = _oauth.authorize_handler(authorize_handler_fnx)

    access_token_handler_fnx = views.AccessTokenView.as_view('access_token')
    access_token_handler_decorated = _oauth.token_handler(access_token_handler_fnx)
    _app.add_url_rule('/oauth/authorize/', view_func=authorize_handler_decorated, methods=['GET', 'POST'])
    _app.add_url_rule('/oauth/token/', view_func=access_token_handler_decorated, methods=['GET', 'POST'])

    return _app, _oauth


def configure_app(_app):
    _app = setup_config(_app)
    _app = setup_routing(_app)
    return _app


def configure_oauth(_app, _oauth):
    _app, _oauth = setup_oauth_handlers(_app, _oauth)
    _app, _oauth = setup_oauth_routes(_app, _oauth)
    return _app, _oauth

app = configure_app(app)
oauth = MyProvider(app, db)
app, oauth = configure_oauth(app, oauth)
