# coding: utf-8
import os
from flask.ext.babel import lazy_gettext as _

## MACRO ##


class DefaultConfig(object):
    DEBUG = True
    DEPLOYMENT = False

    MONGODB_DB = 'socialgram'
    MONGODB_HOST = '127.0.0.1'
    MONGODB_PORT = 27017
    MONGODB_ALIAS = 'default'

    SECRET_KEY = '9yid(3l%krngv1e4st(natn-$93*_k@^qpr85de3#utt$uun+m'

    ACCEPT_LANGUAGES = ['fa', 'en']

    BABEL_DEFAULT_LOCALE = 'fa'
    BABEL_DEFAULT_TIMEZONE = 'Asia/tehran'

    TEMP_FOLDER = "%s/project/media/temp/" % os.path.abspath(os.curdir)
    MEDIA_BASE = "%s/project/media/" % os.path.abspath(os.curdir)
    AVATAR_FOLDER = TEMP_FOLDER + "avatar/"
    UPLOAD_FOLDER = TEMP_FOLDER + "upload/"
    MINIFY_PAGE = True

    SITE_NAME = u'Socialgram'
    # Blueprint haye nasb shode dar app bayad be in list ezafe beshan
    INSTALLED_BLUEPRINTS = ('auth',)

    MAIL_VALIDATION = False
    LOGGER_NAME = 'socialgram'
    LOG_PATH = 'log/'    # '/var/log/project/'
    DEBUG_LOG = LOG_PATH + "debug.log"
    ERROR_LOG = LOG_PATH + "error.log"
    if DEBUG:
        LOG_FORMAT = '\033[1;35m[%(asctime)s]\033[1;m [\033[1;31m %(levelname)s \033[1;m] \033[1;32m[%(logger_name)s]\033[1;m: \
        \033[1;33m %(message)s \033[1;m'

    else:
        LOG_FORMAT = '[%(asctime)s] %(levelname)s [%(logger_name)s]: %(message)s'


class DeploymentConfig(DefaultConfig):
    DEBUG = False
    TESTING = False
    DEPLOYMENT = True


class DevelopmentConfig(DefaultConfig):
    MINIFY_PAGE = False
    DEBUG = True
    CACHE_TYPE = 'null'
