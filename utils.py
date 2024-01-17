import datetime
import time
from deprl import main
import os
def run_training(config:dict,eporchs:int):
    print(datetime.datetime.now().strftime("%Y년 %m월 %d일 %H:%M:%S"))
    for i in range(eporchs):
        # Set the custom trainer with increasing steps for each iteration
        config['tonic']['trainer'] = f'deprl.custom_trainer.Trainer(steps=int(1e5)*{i+1}, epoch_steps=int(2e4), save_steps=int(2e4))'
        
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

