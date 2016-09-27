import os
from typing import Dict

from plenum.common.looper import Looper
from plenum.common.util import getlogger, randomString
from plenum.test.helper import genHa
from sovrin.agent.agent import WalletedAgent
from sovrin.client.client import Client
from sovrin.client.wallet.wallet import Wallet
from sovrin.common.util import getConfig

logger = getlogger()


class FaberAgent(WalletedAgent):
    def __init__(self,
                 basedirpath: str,
                 client: Client=None,
                 wallet: Wallet=None,
                 port: int=None):
        if not basedirpath:
            config = getConfig()
            basedirpath = basedirpath or os.path.expanduser(config.baseDir)

        super().__init__('Faber College', basedirpath, client, wallet, port)

    def getClaimList(self):
        return [{
            "name": "Transcript",
            "version": "1.2",
            "claimDefSeqNo": "<claimDefSeqNo>",
            "values": {
                "student_name": "Alice Garcia",
                "ssn": "123456789",
                "degree": "Bachelor of Science, Marketing",
                "year": "2015",
                "status": "graduated"
            }
        }]

    def getAvailableClaimList(self):
        return [{
            "name": "Transcript",
            "version": "1.2",
            "claimDefSeqNo": "<claimDefSeqNo>",
            "definition": {
                "attributes": {
                    "student_name": "string",
                    "ssn": "string",
                    "degree": "string",
                    "year": "string",
                    "status": "string"
                }
            }
        }]

def runFaber(name=None, wallet=None, basedirpath=None, startRunning=True):
    _, port = genHa()
    _, clientPort = genHa()
    client = Client(randomString(6),
                    ha=("0.0.0.0", clientPort),
                    basedirpath=basedirpath)

    faber = FaberAgent(basedirpath=basedirpath,
                       client=client,
                       wallet=wallet,
                       port=port)
    if startRunning:
        with Looper(debug=True) as looper:
            looper.add(faber)
            logger.debug("Running Faber now...")
            looper.run()
    else:
        return faber


if __name__ == "__main__":
    runFaber()
