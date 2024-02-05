import matplotlib.pyplot as plt
import pandas as pd
import os

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

def plot_log(name:str):
    '''
    name에 따라 다른 그래프를 그린다.
    name = 'reward' : reward 그래프
    name = 'fail' : 실패한 epoisode 그래프
    '''
    from myutils.config_utils import get_directory_path
    dir_path = get_directory_path()
    path = os.path.join(dir_path,name)
    names = os.listdir(path)[0]
    path = os.path.join(path,names)
    log = pd.read_csv(os.path.join(path,'log.csv'))

    fig = plt.figure(figsize=(10, 2))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    
    # Plot for train/episode_score/mean
    ax1.plot(log[['train/episode_score/mean','train/episode_score/max']])
    # ax1.plot(log['train/episode_score/mean'])
    ax1.set_xlabel('Episode')
    ax1.set_title('Train Reward')

    # Plot for train/episode_score/max
    # ax2.plot(log[['test/episode_score/mean','test/episode_score/max']])
    ax2.plot(log['test/episode_score/mean'])
    ax2.set_xlabel('Episode')
    ax2.set_title('Test Reward')
    plt.subplots_adjust(wspace=0.08)

    return fig

# Adjust the spacing between the subplots
def _filter_column(df: pd.DataFrame, keyword: str):
    return df[[col for col in df.columns if keyword in col]]