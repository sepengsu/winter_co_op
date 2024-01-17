import datetime
import time
from deprl import main
import os
def run_training(config:dict,eporchs:int):
    print(datetime.datetime.now().strftime("%Y년 %m월 %d일 %H:%M:%S"))
    for i in range(eporchs):    
        # trainer set
        config['tonic']['trainer'] = make_trainer_string(config['tonic']['trainer'],config['tonic']['step_per_epoch'],i+1)
        # Capture the start time
        start_time = time.time()
        
        # Start the training process
        main.main(config)
        
        # Capture the end time
        end_time = time.time()
        
        # Calculate and print the duration
        duration = end_time - start_time
        minutes, seconds = divmod(duration, 60)
        
        print("-" * 30)    
        print(f"Iteration {i+1}, Duration: {int(minutes)}분 {int(seconds)}초")
        print(f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
        print("-" * 30)

def get_directory_path():
    dir_path = [
        r"C:\Users\PC\Documents\SCONE\results",
        r"C:\Users\na062\Documents\SCONE\results"
    ]
    
    for path in dir_path:
        if os.path.exists(path) or os.path.isdir(path):
            return path
    while True:
        name = input("사용자 이름: ")
        dir_path = r"C:\Users\{}\Documents\SCONE\results".format(name)
        if os.path.exists(dir_path) or os.path.isdir(dir_path):
            return dir_path
        else:
            print("경로를 찾을 수 없습니다.")
            print("경로를 다시 입력하세요.")
            continue

def configmake(config:dict):
    while True:
        cur =input("설정을 바꾸시겠습니까? (y/n)")
        if cur =="N" or cur =="n":
            break
        sel = input("어떤 것을 바꾸시겠습니가? 1: 이름만, 2: step만, 3: 모두")
        if sel =="1":
            config['tonic']["name"] = input("이름을 입력하세요")
        elif sel =="2":
            config['tonic']["trainer"], config["tonic"]['step_per_epoch'] = generate_trainer_string(input("ex) 2e5,2e5,2e5").split(","))
        elif sel =="3":
            config['tonic']["name"] = input("이름을 입력하세요")
            config['tonic']["trainer"], config["tonic"]['step_per_epoch'] = generate_trainer_string(input("ex) 2e5,2e5,2e5").split(","))
        else:
            print("잘못된 입력입니다.")
            continue
    return config    

def generate_trainer_string(inputs:list):
        return inputs[0],f"deprl.custom_trainer.Trainer(steps={int(inputs[0])}, epoch_steps={int(inputs[1])}, save_steps={int(inputs[2])})"

def make_trainer_string(trainer:str,steps:str,epoch:int):
    return trainer.replace(f"steps={int(steps)}",f"steps={int(steps)*epoch}")

