# from python
import logging
import logging.handlers
import time
import os
from datetime import datetime
from datetime import timedelta, datetime

# from flask
from flask import Flask
from flask import g, abort
from flask import jsonify
from flask import redirect
from flask import request, render_template
from flask import session
from flask import url_for, current_app
from flask.ext.babel import Babel
from flask.ext.babel import gettext as _
from flask.ext.mongoengine import MongoEngine
# from project.extensions import mail

# from project
from project.config import DefaultConfig as base_config

__all__ = ['create_app']

DEFAULT_APP_NAME = 'project'


def create_app(config=None, app_name=DEFAULT_APP_NAME):
    """
    Tabe asli hast ke app ro misaze va configesh mikone.
    be in tabe tanzimate barname tahte name config ersal mishe va on tabzimat dar dakhele object
    app zakhire va negahdari mishe

    @param config: class ya objecte haviye tanzimate kolliye app mibashad.
    @param app_name: name asliye narm afzar
    """

    # TODO: static_folder va template_folder bayad dar method joda set beshe
    app = Flask(app_name, static_folder='media/statics', template_folder='media/templates')

    configure_app(app, config)
    configure_logger(app)
    # configure_site(app)
    configure_i18n(app)
    configure_blueprints(app)
    configure_errorhandlers(app)
    configure_mongodb(app)
    configure_before_handlers(app)
    # configure_template_tag(app)
    # configure_extentions(app)
    # configure_user(app)
    return app


def configure_app(app, config):
    """
    tanzimate kolli app ke mamolan dar yek file zakhore mishavat tavasote in tabe
    megdar dehi va load mishavad
    """

    # config default ro dakhele app load mikone
    app.config.from_object(base_config())
    # sys.path.append(os.path.dirname(os.path.realpath(__file__)))
    if config is not None:
        # agar config degari be create_app ersal shode bashe dar in bakhsh load mishe
        # agar tanzimate in bakhsh gablan va dakhele defalt config tanzim shode
        # bashe dobare nevisi mishe
        app.config.from_object(config)

    # dar sorati ke environment variable baraye tanzimat set shode bashe ham
    # load mishe
    app.config.from_envvar('project_CONFIG', silent=True)


def configure_blueprints(app):
    """
    Tanzimate marbot be blueprint ha va load kardan ya nasbe onha ro inja anjam midim
    """

    app.config.setdefault('INSTALLED_BLUEPRINTS', [])
    blueprints = app.config['INSTALLED_BLUEPRINTS']
    for blueprint_name in blueprints:
        bp = __import__('project.apps.%s' % blueprint_name, fromlist=['views'])

        try:
            mod = __import__('project.%s' % blueprint_name, fromlist=['urls'])
        except ImportError:
            pass
        else:
            mod.urls.add_url_rules(bp.views.mod)
        try:
            app.register_blueprint(bp.views.mod)
        except:
            # report has no views
            pass


def configure_i18n(app):
    """
    tanzimate marbot be i18n va systeme tarjome dar in bakhsh emal mishavad
    """

    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match([g.marketplace.language])
        # user = getattr(g, 'user', None)
        # if user is not None:
        #     pass
        # accept_languages = app.config.get('ACCEPT_LANGUAGES', ['fa', 'en'])
        # return request.accept_languages.best_match(accept_languages)


def configure_errorhandlers(app):
    """
    tavasote in method baraye error haye asli va mamol khatahaye monaseb bargasht dade mishavad
    """

    if app.testing:
        return

    @app.errorhandler(404)
    def page_not_found(error):
        # import_cart_to_list(error)
        if request.is_xhr:
            return jsonify(error=_('Sorry, page not found'))
        if request.blueprint == 'api':
            return jsonify(msg='Sorry, page not found', code=404)
        return render_template("errors/404.html", error=error), 404

    @app.errorhandler(403)
    def forbidden(error):
        # import_cart_to_list(error)
        if request.is_xhr:
            return jsonify(error=_('Sorry, not allowed'))
        if request.blueprint == 'api':
            return jsonify(msg='Sorry, not allowed', code=403)
        return render_template("errors/403.html", error=error), 403

    @app.errorhandler(500)
    def server_error(error):
        import_cart_to_list(error)
        if request.is_xhr:
            # import_cart_to_list(error)
            return jsonify(error=_('Sorry, an error has occurred')), 500
        return render_template('errors/500.html')

    @app.errorhandler(401)
    def unauthorized(error):
        if request.is_xhr:
            return jsonify(error=_("Login required"))
        return redirect(url_for("profile.login", next=request.path))


def configure_mongodb(app):
    MongoEngine(app)


def configure_before_handlers(app):
    pass


def configure_logger(app):
    """
    This function Configure Logger for given Application.

    :param app: Application Object
    :type app: Object
    """

    # from project.utils.extended_logging import wrap_app_logger
    # wrap_app_logger(app)
    # if app.debug or app.testing:
    #     from project.utils.extended_logging import wrap_app_logger
    #     wrap_app_logger(app)
    #     app.logger.create_logger('debuging')
    #     return

    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s '
                                  '[in %(pathname)s:%(lineno)d]')

    debug_file_handler = logging.handlers.RotatingFileHandler(
        app.config['DEBUG_LOG'], maxBytes=100000, backupCount=10)

    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(formatter)
    app.logger.addHandler(debug_file_handler)

    error_file_handler = logging.handlers.RotatingFileHandler(
        app.config['ERROR_LOG'], maxBytes=100000, backupCount=10)

    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)


# def configure_template_tag(app):
#     from project.utils.template_tag import init_filters
#     init_filters(app)

# def configure_extentions(app):
#     mail.init_app(app)
#     # telegram.init_app(app)


# def configure_user(app):
#     """
#     """

#     @app.before_request
#     def before_request():
#         """
#         """
#         now = datetime.now()
#         email = session.get('email', '')
#         if not email:
#             g.user = GuestUser()
#             return
#         try:
#             if g.marketplace.is_backpanel:
#                 user = User.objects.get(email=email, marketplace=g.marketplace.current)
#                 if len(user.stores) == 1:
#                     g.store = user.stores[0].store
#                     session['current_store'] = str(g.store.id)
#                 current_store = session.get('current_store', '')
#                 if current_store:
#                     g.store = Store.objects.get(pk=current_store)
#             else:
#                 user = Customer.objects.get(email=email, store=g.store)
#         except:

#             g.user = GuestUser()
#             return

#         # last_seen = session.get('last_seen', now)
#         # remember_me = session.get('remember', False)
#         # if not remember_me and (now - last_seen).total_seconds() > app.config['TIMEOUT_SESSION']:
#         #     if 'email' in session:
#         #         del(session['email'])
#         session['last_seen'] = now
#         g.user = user

#     @app.before_request
#     def store_control():
#         if g.marketplace.is_backpanel:
#             return
#         if g.store.registering_freeze:
#             g.store.ordering_freeze = True
#             # if g.user.can('login'):
#             #     check_status = check_store_status()
#             #     if not check_status:
#             #         return
#             #     return redirect(check_status)

