import yaml
import os


class Config:
    def __init__(self,option, types, name):
        self.options = option
        self.types = types
        self.name = name

    def loading(self):
        with open(f'.config/scone_walk_h{self.name}.yaml', 'r') as f:
            self.config = yaml.safe_load(f)
    
    def making(self):
        pass
