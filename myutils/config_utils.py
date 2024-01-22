import os
import re

def get_directory_path():
    """
    사용자의 디렉토리 경로를 반환하는 함수입니다.

    Returns:
        str: 사용자의 디렉토리 경로
    """
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

def configmake(config:dict, skip_while_loop: bool = False):
    """
    주어진 config를 수정하는 함수입니다.

    Parameters:
        config (dict): 수정할 설정 정보를 담고 있는 딕셔너리
        skip_while_loop (bool): 수정할지 여부 (기본값: False)

    Returns:
        dict: 수정된 설정 정보를 담고 있는 딕셔너리
    """
    if skip_while_loop:
        print("설정을 바꾸지 않고 종료합니다.")
        return config
    
    config["tonic"]['step_per_epoch'] = _step_per_epoch(config["tonic"]['trainer'])
    cur = input("설정을 바꾸시겠습니까? (y/n)")
    if cur.lower() == "n":
        print("설정을 바꾸지 않고 종료합니다.")
        return config
    
    while True:
        if cur.lower() == "y":
            sel = input("어떤 것을 바꾸시겠습니가? 1: 이름만, 2: step만, 3: 모두")
            if sel == "1":
                config['tonic']["name"] = input("이름을 입력하세요")
                break
            elif sel == "2":
                config['tonic']["trainer"], config["tonic"]['step_per_epoch'] = _generate_trainer_string(input("epoch_steps: ex)2e4"))
                break
            elif sel == "3":
                config['tonic']["name"] = input("이름을 입력하세요")
                config['tonic']["trainer"], config["tonic"]['step_per_epoch'] =  _generate_trainer_string(input("epoch_steps: ex)2e4"))
                break
            else:
                print("잘못된 입력입니다.")
                continue
        else:
            print("잘못입력되어 수정 없이 종료합니다")
            break
    
    return config

def make_weight_dict(config,is_weight = False):
    '''
    make_weight_dict 함수는 주어진 config 딕셔너리에 reward_weight를 추가하는 함수입니다.
    input 함수를 통해 reward_type, weight_name, weight를 입력받아 reward_weight를 만듭니다.

    Guide:
        reward_type, weight_name, weight를 입력받아 reward_weight를 만듭니다.        
        reward_type, weight_name은 문자열이며, weight는 실수입니다.
        key를 input 할 때에는 reward_type , weight_name 이렇게 쓰세요.
        weight는 실수로 입력하세요.
        reward_weight를 추가할지 여부를 입력받아 추가할 경우 reward_type, weight_name, weight를 입력받습니다.
        reward_weight를 추가하지 않을 경우 config 딕셔너리를 그대로 반환합니다.
        
    Parameters:
        config (dict): 설정을 담고 있는 딕셔너리
        is_weight (bool, optional): weight를 추가할지 여부를 나타내는 불리언 값. 기본값은 False입니다.
    
    Returns:
        dict: reward_weight가 추가된 config 딕셔너리
    
    '''
    weight_dict = dict()
    while is_weight:
        reward_type, weight_name = input('reward type, weight name 이렇게 입력하세요: ').split(',')
        reward_type = reward_type.strip()
        weight_name = weight_name.strip()
        weight = float(input('weight를 입력하세요: '))
        weight_dict[f'{reward_type}_{weight_name}'] = weight
        is_weight = input('weight를 추가하시겠습니까? (y/n): ')
        if is_weight == 'n':
            is_weight = False
            
    config['reward_weight'] = weight_dict
    return config


# 숨겨진 함수
def _generate_trainer_string(inputs:str):
    """
    주어진 입력을 기반으로 Trainer 클래스의 문자열을 생성하는 함수입니다.

    Parameters:
        inputs (str): epoch_steps 값을 나타내는 문자열

    Returns:
        tuple: Trainer 클래스의 문자열과 입력값
    """
    inputs = re.sub(" ", "", inputs)
    return f"deprl.custom_trainer.Trainer(steps=int({inputs}), epoch_steps=int({inputs}), save_steps=int({inputs}))", inputs

def _make_trainer_string(trainer:str,steps:str,epoch:int):
    """
    주어진 trainer 문자열에서 steps 값을 수정하여 반환하는 함수입니다.

    Parameters:
        trainer (str): Trainer 클래스의 문자열
        steps (str): 수정할 steps 값을 나타내는 문자열
        epoch (int): 현재 에포크 값

    Returns:
        str: 수정된 trainer 문자열
    """
    before = re.search(r'[(]steps=int\(.*?\)', trainer)[0]
    if before[-1] == ",":
        before = before[:-1]
    n_steps = f'{int(steps[0])*epoch}{steps[1:]}'
    return trainer.replace(before,f"(steps=int({n_steps})")

def _step_per_epoch(code:str):
    """
    주어진 코드 문자열에서 step_per_epoch 값을 추출하여 반환하는 함수입니다.

    Parameters:
        code (str): Trainer 클래스의 문자열

    Returns:
        str: 추출된 step_per_epoch 값
    """
    step_match = re.search(r'steps=(.*?)[,\)]', code)[0]
    if step_match[-1] == ",":
        step_match = step_match[:-1]
        return step_match[6:]
    return step_match[10:-1]

if __name__ == "__main__":
    # Example usage
    string = 'deprl.custom_trainer.Trainer(steps=int(2e4), epoch_steps=int(2e4), save_steps=int(2e4))'
    string, s = _generate_trainer_string('4e5')
    print(f'원래: {string}')
    i=2
    values = _step_per_epoch(string)
    print(f'나중: {_make_trainer_string(string,values,i)}')

