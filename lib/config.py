"""
    Set up defaults and read sentinel.conf
"""
import sys
import os
from sib_config import SibcoinConfig
from img_config import ImageCoinConfig

default_sentinel_config = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '../sentinel.conf')
)


debug_enabled = os.environ.get('SENTINEL_DEBUG', False)

sentinel_config_file = os.environ.get('SENTINEL_CONFIG', default_sentinel_config)
sentinel_cfg = ImageCoinConfig.tokenize(sentinel_config_file)
sentinel_version = "1.1.0"
min_dashd_proto_version_with_sentinel_ping = 70207


def get_dash_conf():
    home = os.environ.get('HOME')

    dash_conf = os.path.join(home, ".dashcore/dash.conf")
    if sys.platform == 'darwin':
        dash_conf = os.path.join(home, "Library/Application Support/DashCore/dash.conf")

    dash_conf = sentinel_cfg.get('dash_conf', dash_conf)

    return dash_conf

def get_imagecoin_conf():
    home = os.environ.get('HOME')

    imagecoin_conf = os.path.join(home, ".imagecoincore/imagecoin.conf")
    if sys.platform == 'darwin':
        imagecoin_conf = os.path.join(home, "Library/Application Support/ImageCoin/imagecoin.conf")

    imagecoin_conf = sentinel_cfg.get('imagecoin_conf', imagecoin_conf)

    return imagecoin_conf
    
def get_sibcoin_conf():
    home = os.environ.get('HOME')

    sibcoin_conf = os.path.join(home, ".sibcoin/sibcoin.conf")
    if sys.platform == 'darwin':
        sibcoin_conf = os.path.join(home, "Library/Application Support/Sibcoin/sibcoin.conf")

    sibcoin_conf = sentinel_cfg.get('sibcoin_conf', sibcoin_conf)

    return sibcoin_conf


def get_network():
    return sentinel_cfg.get('network', 'mainnet')


def sqlite_test_db_name(sqlite_file_path):
    (root, ext) = os.path.splitext(sqlite_file_path)
    test_sqlite_file_path = root + '_test' + ext
    return test_sqlite_file_path


def get_db_conn():
    import peewee
    env = os.environ.get('SENTINEL_ENV', 'production')

    # default values should be used unless you need a different config for development
    db_host = sentinel_cfg.get('db_host', '127.0.0.1')
    db_port = sentinel_cfg.get('db_port', None)
    db_name = sentinel_cfg.get('db_name', 'sentinel')
    db_user = sentinel_cfg.get('db_user', 'sentinel')
    db_password = sentinel_cfg.get('db_password', 'sentinel')
    db_charset = sentinel_cfg.get('db_charset', 'utf8mb4')
    db_driver = sentinel_cfg.get('db_driver', 'sqlite')

    if (env == 'test'):
        if db_driver == 'sqlite':
            db_name = sqlite_test_db_name(db_name)
        else:
            db_name = "%s_test" % db_name

    peewee_drivers = {
        'mysql': peewee.MySQLDatabase,
        'postgres': peewee.PostgresqlDatabase,
        'sqlite': peewee.SqliteDatabase,
    }
    driver = peewee_drivers.get(db_driver)

    dbpfn = 'passwd' if db_driver == 'mysql' else 'password'
    db_conn = {
        'host': db_host,
        'user': db_user,
        dbpfn: db_password,
    }
    if db_port:
        db_conn['port'] = int(db_port)

    if driver == peewee.SqliteDatabase:
        db_conn = {}

    db = driver(db_name, **db_conn)

    return db


#dash_conf = get_dash_conf()
#sibcoin_conf = get_sibcoin_conf()
#network = get_network()
#db = get_db_conn()
