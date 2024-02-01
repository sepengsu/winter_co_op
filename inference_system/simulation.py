import gym
import sys
sys.path.append("C:/Program Files/SCONE/bin")
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import sconegym
import yaml
import deprl
from myutils.load_utils import load
from myutils import inference, plot_2d, plot_3d, get_directory_path
import datetime
import numpy as np
import pandas as pd

class Simulation:
    def __init__(self):
        """Initialize simulation class."""

    def nameing(self,name:str,config_dir  = r"C:\Users\PC\Desktop\SJW\dep\trainconfig"):
        self.config_dir = config_dir
        self.name = name   
        self.dir_path = self.directory_path()
        self.config = self.load_config()
        self.checkpoint = self.best_checkpoint()
        if self.checkpoint == None:
            raise ValueError("There is no checkpoint.")
        self.env, self.policy = self.loading()
    
    def directory_path(self):
        """Get directory path of the current file.

        Returns:
            dir_path (str): Directory path of the current file.
        """
        dir_path = get_directory_path()
        path = os.path.join(dir_path,self.name)
        names = os.listdir(path)[0]
        path = os.path.join(path,names)
        return path
    
    def load_config(self):
        """Load config file.

        Returns:
            config (dict): Config dictionary.
        """
        assert os.path.exists(f'{self.config_dir}/{self.name}.yaml'), "There is no such file."
        with open(f'{self.config_dir}/{self.name}.yaml','r') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
        return config

    def best_checkpoint(self):
        log = pd.read_csv(f'{self.dir_path}/log.csv')
        ch = _find_max_mean(log)
        return ch

    def loading(self):
        env = eval(self.config['tonic']['environment'])
        policy = deprl.load(os.path.join(self.dir_path,'checkpoints'),env,checkpoint=self.checkpoint)

        return env, policy

    # Simulation
    def inferencing(self,save = True,Max=True,more=False):
        """Run inference of the simulation.

        Args:
            save (bool, optional): Save the result. Defaults to True.
            Max (bool, optional): Save the maximum value of the simulation. Defaults to True.
            more (bool, optional): Save more data. Defaults tdo False.
        """
        time = datetime.datetime.now() 
        self.env.set_output_dir('re'+self.config['tonic']['name']+f'{_make_dict(time)}')
        return inference(self.env,self.policy,save=save,Max=Max,more=more,num = 2)

class Ploting:
    def __init__(self,pos,vel,is_2d=True,is_3d=True):
        """Initialize ploting class."""
        self.is_2d = is_2d
        self.is_3d = is_3d
        self.fig_2d = None
        self.fig_3d = None
        self.pos = pos
        self.vel = vel
    
    def plot(self,options):
        """Plot the simulation.

        Args:
            sim (Simulation): Simulation class.
        """
        if self.is_2d:
            self.fig_2d = plot_2d(self.pos,self.vel,Max=options.Max)
        if self.is_3d:
            self.fig_3d = plot_3d(self.pos,self.vel,Max=options.Max)



def _make_dict(time:datetime.datetime):
    day = str(time.day).zfill(2)
    hour = str(time.hour).zfill(2)
    minute = str(time.minute).zfill(2)
    return day+hour+minute


def _find_max_mean(df):
    df = _per_5(df)
    df = df.reset_index()
    max_mean = df['test/episode_score/mean'].max()
    max_mean_index = np.where(df['test/episode_score/mean']==max_mean)[0][-1]
    print(f"The maximum mean value of the test episodes is {round(max_mean,2)} at index {max_mean_index}.")
    return str(int(round(max_mean_index+1,0)*1e6))

def _per_5(df):
    result = pd.DataFrame()
    for i in range(len(df)//5):
        temp = df[i*5:(i+1)*5].mean()
        result = pd.concat([result,pd.DataFrame([temp])])
    return result