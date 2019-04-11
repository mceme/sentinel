"""
dashd JSONRPC interface
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
import config
import base58
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from masternode import Masternode
from decimal import Decimal
import time
from dashd import DashDaemon


class SibcoinDaemon(DashDaemon):

    @classmethod
    def from_sibcoin_conf(self, sibcoin_dot_conf):
        from sib_config import SibcoinConfig
        config_text = SibcoinConfig.slurp_config_file(sibcoin_dot_conf)
        creds = SibcoinConfig.get_rpc_creds(config_text, config.network)

        return self(**creds)

    @classmethod
    def from_dash_conf(self, dash_dot_conf):
        raise RuntimeWarning('This method should not be used with sibcoin')


