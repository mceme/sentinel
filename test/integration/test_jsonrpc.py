import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from sibcoind import SibcoinDaemon
from sib_config import SibcoinConfig


def test_dashd():
    config_text = SibcoinConfig.slurp_config_file(config.sibcoin_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'00000c492bf73490420868bc577680bfc4c60116e7e85343bc624787c21efa4c'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000617791d0e19f524387f67e558b2a928b670b9a3b387ae003ad7f9093017'

    creds = SibcoinConfig.get_rpc_creds(config_text, network)
    sibcoind = SibcoinDaemon(**creds)
    assert sibcoind.rpc_command is not None

    assert hasattr(sibcoind, 'rpc_connection')

    # Dash testnet block 0 hash == 00000617791d0e19f524387f67e558b2a928b670b9a3b387ae003ad7f9093017
    # test commands without arguments
    info = sibcoind.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert sibcoind.rpc_command('getblockhash', 0) == genesis_hash
