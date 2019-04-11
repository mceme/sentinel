import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
import argparse
import config

def is_valid_python_version():
    version_valid = False

    ver = sys.version_info
    if (2 == ver.major) and (7 <= ver.minor):
        version_valid = True

    if (3 == ver.major) and (4 <= ver.minor):
        version_valid = True

    return version_valid


def python_short_ver_str():
    ver = sys.version_info
    return "%s.%s" % (ver.major, ver.minor)


def are_deps_installed():
    installed = False

    try:
        import peewee
        import bitcoinrpc.authproxy
        import simplejson
        import inflection
        installed = True
    except ImportError as e:
        print("[error]: Missing dependencies")

    return installed


def is_database_correctly_configured():
    import peewee
    import config

    configured = False

    cannot_connect_message = "Cannot connect to database. Please ensure database service is running and user access is properly configured in 'sentinel.conf'."

    try:
        db = config.db
        db.connect()
        configured = True
    except (peewee.ImproperlyConfigured, peewee.OperationalError, ImportError) as e:
        print("[error]: %s" % e)
        print(cannot_connect_message)
        sys.exit(1)

    return configured


def has_sibcoin_conf():
    import config
    import io

    valid_sibcoin_conf = False

    # ensure dash_conf exists & readable
    #
    # if not, print a message stating that Dash Core must be installed and
    # configured, including JSONRPC access in dash.conf
    try:
        f = io.open(config.sibcoin_conf)
        valid_sibcoin_conf = True
    except IOError as e:
        print(e)

    return valid_sibcoin_conf
    
def has_imagecoin_conf():
    import config
    import io

    valid_imagecoin_conf = False

    # ensure dash_conf exists & readable
    #
    # if not, print a message stating that Dash Core must be installed and
    # configured, including JSONRPC access in dash.conf
    try:
        f = io.open(config.imagecoin_conf)
        valid_imagecoin_conf = True
    except IOError as e:
        print(e)

    return valid_imagecoin_conf

def process_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bypass-scheduler',
                        action='store_true',
                        help='Bypass scheduler and sync/vote immediately',
                        dest='bypass')
    parser.add_argument('-c', '--config',
                        help='Path to sentinel.conf (default: ../sentinel.conf)',
                        dest='config')
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='Enable debug mode',
                        dest='debug')
    args, unknown = parser.parse_known_args()

    return args

initmodule = sys.modules[__name__]
initmodule.options = False

# === begin main


def main():

    options = process_args()

    if options.config:
        config.sentinel_config_file = options.config

    # register a handler if SENTINEL_DEBUG is set
    if os.environ.get('SENTINEL_DEBUG', None) or options.debug:
        config.debug_enabled = True
        import logging
        logger = logging.getLogger('peewee')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.StreamHandler())

    initmodule.options = options

    from img_config import ImageCoinConfig
    config.sentinel_cfg = ImageCoinConfig.tokenize(config.sentinel_config_file)

    config.imagecoin_conf = config.get_imagecoin_conf()
    config.network = config.get_network()
    config.db = config.get_db_conn()

    install_instructions = "\tpip install -r requirements.txt"

    if not is_valid_python_version():
        print("Python %s is not supported" % python_short_ver_str())
        sys.exit(1)

    if not are_deps_installed():
        print("Please ensure all dependencies are installed:")
        print(install_instructions)
        sys.exit(1)

    if not is_database_correctly_configured():
        print("Please ensure correct database configuration.")
        sys.exit(1)

    if not has_imagecoin_conf():
        print("Imagecoin Core must be installed and configured, including JSONRPC access in imagecoin.conf")
        sys.exit(1)


main()
