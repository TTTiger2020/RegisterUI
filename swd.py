from pyocd.board.board import Board
from pyocd.core.helpers import ConnectHelper
from pyocd.core.target import Target
from pyocd.core.memory_map import MemoryType
from pyocd.coresight.cortex_m import CortexM

def UlinkInit():
    session = ConnectHelper.session_with_chosen_probe(target_override="CMSDK_CM4_FP")
    session.open()
    board = session.board
    target = board.target
    return session,target

def UlinkWrite(regAddr, regdata, target):
    target.write32(regAddr,regdata)
    return

def UlinkRead(regAddr, target):
    val = target.read32(regAddr)
    return val

def UlinkClose(session):
    session.close()
