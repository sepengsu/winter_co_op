import datetime
import time
from deprl.main import main
import os
import re

def run_training(config:dict,starts =0,epochs = 2):
    if epochs <2 or starts <0:
        raise KeyError("eporchs는 2이상, starts는 0이상의 정수여야 합니다.")
    
    print(datetime.datetime.now().strftime("%Y년 %m월 %d일 %H:%M:%S"))

    for i in range(starts,starts+epochs):    
        # trainer set
        config['tonic']['trainer'] = _make_trainer_string(config['tonic']['trainer'],config['tonic']['step_per_epoch'],epoch=i+1)
        print(f"trainer: {config['tonic']['trainer']}")

        # Capture the start time
        start_time = time.time()
        
        # Start the training process
        main(config)
        
        # Capture the end time
        end_time = time.time()
        
        # Calculate and print the duration
        duration = end_time - start_time
        minutes, seconds = divmod(duration, 60)
        
        print("-" * 30)
        # if i == 0:
        #     print(f"Iteration {i+1}은 초기화 과정으로 생략합니다.")
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
    config["tonic"]['step_per_epoch'] = _step_per_epoch(config["tonic"]['trainer'])
    while True:
        cur =input("설정을 바꾸시겠습니까? (y/n)")
        if cur =="N" or cur =="n":
            print("설정을 바꾸지 않고 종료합니다.")
            break
        elif cur =="Y" or cur =="y":
            sel = input("어떤 것을 바꾸시겠습니가? 1: 이름만, 2: step만, 3: 모두")
            if sel =="1":
                config['tonic']["name"] = input("이름을 입력하세요")
                break
            elif sel =="2":
                config['tonic']["trainer"], config["tonic"]['step_per_epoch'] = _generate_trainer_string(input("epoch_steps: ex)2e4"))
                break
            elif sel =="3":
                config['tonic']["name"] = input("이름을 입력하세요")
                config['tonic']["trainer"], config["tonic"]['step_per_epoch'] =  _generate_trainer_string(input("epoch_steps: ex)2e4"))
                break
            else:
                print("잘못된 입력입니다.")
                continue
        else:
            print("잘못입력되어 수정 없이 종료합니다")
            break
    # config파일 중 trainer에 대하여 2e4등을 2e4 그대로 저장.
    return config    

def _generate_trainer_string(inputs:str):
        inputs = re.sub(" ", "", inputs)
        return f"deprl.custom_trainer.Trainer(steps=int({inputs}), epoch_steps=int({inputs}), save_steps=int({inputs}))", inputs

def _make_trainer_string(trainer:str,steps:str,epoch:int):
    before = re.search(r'[(]steps=int\(.*?\)', trainer)[0]
    if before[-1] == ",":
        before = before[:-1]
    n_steps = _sim(int(float(steps))*(epoch))
    return trainer.replace(before,f"(steps=int({n_steps})")

def _step_per_epoch(code:str):
    step_match = re.search(r'steps=(.*?)[,\)]', code)[0]
    if step_match[-1] == ",":
        step_match = step_match[:-1]
        return step_match[6:]
    return step_match[10:-1]

def _sim(number:int):
    """
    Converts a number to exponential format without '+' sign and leading zero in the exponent.
    """
    # Convert to exponential format
    exponential_format = "{:.0e}".format(number)

    # Remove 'e+' and any leading zero in the exponent part
    simplified_exponential_format = exponential_format.replace("e+0", "e").replace("e+","e")
    return simplified_exponential_format


if __name__ == "__main__":
    # Example usage
    string = 'deprl.custom_trainer.Trainer(steps=int(2e4), epoch_steps=int(2e4), save_steps=int(2e4))'
    string, s = _generate_trainer_string('4e5')
    print(f'원래: {string}')
    i=2
    values = _step_per_epoch(string)
    print(f'나중: {_make_trainer_string(string,values,i)}')

