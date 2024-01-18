import matplotlib.pyplot as plt
import pandas as pd

def printing_var(obj):
    var = dict()
    for attr in dir(obj):
        if not attr.startswith("__"):
            try: 
                getattr(obj, attr)()
            except:
                print(f"{obj} = {getattr(obj, attr)}")
                var[obj] = getattr(obj,attr)
            else:
                print(f"{attr} = {getattr(obj, attr)()}")
                var[obj] = getattr(obj,attr)()
    
def direxcept(obj):
    oblist = dir(obj)
    return [attr for attr in oblist if not attr.startswith('_')]

def namedict(obj):
    return {item.name():item for item in obj}

def ploting(results: pd.DataFrame,mode:str):
    '''
    mode에 따라 다른 그래프를 그린다.
    mode = 'reward' : reward 그래프
    mode = 'fail' : 실패한 epoisode 그래프
    '''
    if mode =="reward":
        columns = 0
        plt.plot(_filter_column(results, 'reward'))
        plt.title('Reward')
        plt.xlabel('Episode')
        plt.ylabel('Reward')
    
def _filter_column(df: pd.DataFrame, keyword: str):
    return df[[col for col in df.columns if keyword in col]]