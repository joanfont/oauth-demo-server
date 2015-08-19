from api import views

routing = {
    '/': {
        'class': views.HomeView,
        'name': 'home',
        'methods': ['GET', 'POST'],
        'oauth': False,
    },
    '/client': {
        'class': views.ClientView,
        'name': 'client',
        'methods': ['GET'],
        'oauth': False,
    },
    '/api/me': {
        'class': views.MeView,
        'name': 'api_me',
        'methods': ['GET'],
        'oauth': True,
    }
}
