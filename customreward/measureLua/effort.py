import os
# Set non-random initial muscle activations
import sys
from abc import ABC, abstractmethod
from typing import Optional

import gym
import numpy as np

# Add sconepy folders to path
if sys.platform.startswith("win"):
    sys.path.append("C:/Program Files/SCONE/bin")
elif sys.platform.startswith("linux"):
    sys.path.append("/opt/scone/lib")
elif sys.platform.startswith('darwin'):
    sys.path.append("/Applications/SCONE.app/Contents/MacOS/lib")

import sconepy

def efforts(model,eff_type:str):
    if eff_type=='Constant':
        pass
    elif eff_type=='TotalForce':
        return _total_force(model)
    elif eff_type=='Uchida2016':
        return _uchida2016(model)
    else:
        raise NameError('''effort type 설정에서 error가 발생했습니다.
           아래 가이드 참고하여 다시 작성해주세요
            --------------------------------
            1. TotalForce
            2. Uchida2016: 아직 구현하지 않음
            위의 두가지 중 하나를 선택하세요
            --------------------------------''')
def _total_force(model):
    return sum(model.muscle_force_array())
def _uchida2016(model):
    raise TypeError('아직 구현하지 않음')
    return None
