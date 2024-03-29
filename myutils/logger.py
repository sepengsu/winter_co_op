from deprl.vendor.tonic.utils import normalize_path_decorator
import datetime
import os
import time

import numpy as np
import pandas as pd
import termcolor
import torch
import yaml

current_logger = None

@normalize_path_decorator
def create_resumed_results_path(config, env):
    if env is None or env.results_dir is None:
        path = os.path.join(config["working_dir"], config["tonic"]["name"])
        postfix = None
    else:
        path = os.path.join(env.results_dir, config["tonic"]["name"])
        postfix = f".{env.unwrapped.model.name()}"
    folders = [x for x in os.walk(path)]
    if len(folders) != 0:
        folder = get_sorted_folders(folders[0][1])[-1]
        return os.path.join(path, folder)
    else:
        log("starting new training.")
        return (
            os.path.join(path, get_datetime())
            if postfix is None
            else os.path.join(path, get_datetime() + postfix)
        )
def get_sorted_folders(folders):
    def get_datetime_key(s):
        date_time_str = s.split(".")[0] + s.split(".")[1]
        try:
            # Assuming date_time_str is in the format "YYMMDDHHMMSS"
            dt = time.strptime(date_time_str, "%y%m%d%H%M%S")
            return dt
        except ValueError:
            return None

    # Sort the strings using the custom sorting key
    sorted_folders = sorted(folders, key=get_datetime_key)
    return sorted_folders

@normalize_path_decorator
def create_results_path(config, env):
    if env is None or env.results_dir is None:
        return os.path.join(
            config["working_dir"], config["tonic"]["name"], get_datetime()
        )
    # Scone experiments are saved in results_dir
    return os.path.join(
        env.results_dir,
        config["tonic"]["name"],
        get_datetime() + f".{env.unwrapped.model.name()}",
    )

class MyLogger:
    def __init__(
        self,
        width=60,
        script_path=None,
        config=None,
        test_env=None,
        resume=False,
    ):
        env = test_env.environments[0] if test_env is not None else None
        self.path = (
            create_resumed_results_path(config, env)
            if resume
            else create_results_path(config, env)
        )
        self.log_file_path = os.path.join(self.path, "log.csv")

        # Save the launch script.
        if script_path:
            with open(script_path, "r", encoding = 'utf-8' or 'cp949') as script_file:
                script = script_file.read()
                try:
                    os.makedirs(self.path, exist_ok=True)
                except Exception:
                    pass
                script_path = os.path.join(self.path, "script.py")
                with open(script_path, "w") as config_file:
                    config_file.write(script)

        # Save the configuration.
        if config:
            try:
                os.makedirs(self.path, exist_ok=True)
            except Exception:
                pass
            config_path = os.path.join(self.path, "config.yaml")
            with open(config_path, "w") as config_file:
                yaml.dump(config, config_file)

        self.known_keys = set()
        self.stat_keys = set()
        self.epoch_dict = {}
        self.width = width
        self.last_epoch_progress = None
        self.start_time = time.time()

    def store(self, key, value, stats=False):
        """Keeps named values during an epoch."""

        if key not in self.epoch_dict:
            self.epoch_dict[key] = [value]
            if stats:
                self.stat_keys.add(key)
        else:
            self.epoch_dict[key].append(value)

    
    def dump(self):
        """Displays and saves the values at the end of an epoch."""

        # Compute statistics if needed.
        keys = list(self.epoch_dict.keys())
        for key in keys:
            values = self.epoch_dict[key]
            if key in self.stat_keys and key in ["train/episode_score","test/episode_score"]:
                self.epoch_dict[key + "/mean"] = np.mean(values)
                self.epoch_dict[key + "/min"] = np.min(values)
                self.epoch_dict[key + "/max"] = np.max(values)
                self.epoch_dict[key + "/size"] = len(values)
                del self.epoch_dict[key]
            else:
                self.epoch_dict[key] = np.mean(values)

        # Check if new keys were added.
        new_keys = [
            key for key in self.epoch_dict.keys() if key not in self.known_keys
        ]
        if new_keys:
            first_row = len(self.known_keys) == 0
            if not first_row:
                warning(f"Logging new keys")
            # List the keys and prepare the display layout.
            for key in new_keys:
                self.known_keys.add(key)
            self.final_keys = list(sorted(self.known_keys))
            self.console_formats = []
            known_keys = set()
            for key in self.final_keys:
                *left_keys, right_key = key.split("/")
                for i, k in enumerate(left_keys):
                    left_key = "/".join(left_keys[: i + 1])
                    if left_key not in known_keys:
                        left = "  " * i + k.replace("_", " ")
                        self.console_formats.append((left, None))
                        known_keys.add(left_key)
                indent = "  " * len(left_keys)
                right_key = right_key.replace("_", " ")
                self.console_formats.append((indent + right_key, key))

        # Save the data to the log file
        vals = [self.epoch_dict.get(key) for key in self.final_keys]
        if new_keys:
            if first_row:
                try:
                    os.makedirs(self.path, exist_ok=True)
                except Exception:
                    pass
                with open(self.log_file_path, "w") as file:
                    file.write(",".join(self.final_keys) + "\n")
                    file.write(",".join(map(str, vals)) + "\n")
            else:
                with open(self.log_file_path, "r") as file:
                    lines = file.read().splitlines()
                old_keys = lines[0].split(",")
                old_lines = [line.split(",") for line in lines[1:]]
                new_indices = []
                j = 0
                for i, key in enumerate(self.final_keys):
                    if key == old_keys[j]:
                        j += 1
                    else:
                        new_indices.append(i)
                assert j == len(old_keys)
                for line in old_lines:
                    for i in new_indices:
                        line.insert(i, "None")
                with open(self.log_file_path, "w") as file:
                    file.write(",".join(self.final_keys) + "\n")
                    for line in old_lines:
                        file.write(",".join(line) + "\n")
                    file.write(",".join(map(str, vals)) + "\n")
        else:
            with open(self.log_file_path, "a") as file:
                file.write(",".join(map(str, vals)) + "\n")
        
        # display 일부
        if 'train/episode_score/mean' in self.epoch_dict.keys():
            log(f"학습   평균 reward: {round(self.epoch_dict['train/episode_score/mean'],2)}") 
        elif self.epoch_dict['First']:
            error("reward가 없음!!! 오류발생!!!!")
        else:
            error("학습 평균 reward: None")

        log(f"테스트 평균 reward: {round(self.epoch_dict['test/episode_score/mean'],2)}")
        self.epoch_dict.clear()
        self.last_epoch_progress = None
        self.last_epoch_time = time.time()

# 여기는 참조하여 수정함
def initialize(*args, **kwargs):
    global current_logger
    current_logger = MyLogger(*args, **kwargs)
    return current_logger

def get_current_logger():
    global current_logger
    if current_logger is None:
        current_logger = MyLogger()
    return current_logger

def store(*args, **kwargs):
    logger = get_current_logger()
    return logger.store(*args, **kwargs)

def dump(*args, **kwargs):
    logger = get_current_logger()
    return logger.dump(*args, **kwargs)

def show_progress(*args, **kwargs):
    logger = get_current_logger()
    return logger.show_progress(*args, **kwargs)

def get_path():
    logger = get_current_logger()
    return logger.path

def log(msg, color="green"):
    print(termcolor.colored(msg, color, attrs=["bold"]))

def warning(msg, color="yellow"):
    print(termcolor.colored("Warning: " + msg, color, attrs=["bold"]))

def error(msg, color="red"):
    print(termcolor.colored("Error: " + msg, color, attrs=["bold"]))

def save(path):
    logger = get_current_logger()
    return logger.save(path)

def load(path, time_dict):
    logger = get_current_logger()
    return logger.load(path, time_dict)

def filter_csv_by_steps(csv_file, threshold):
    logger = get_current_logger()
    return logger.filter_csv_by_steps(csv_file, threshold)

def create_path(path, post_fix):
    logger = get_current_logger()
    return logger.create_path(path, post_fix)

def get_datetime():
    # Get the current date and time
    return datetime.datetime.now()

def initialize(*args, **kwargs):
    global current_logger
    current_logger = MyLogger(*args, **kwargs)
    return current_logger

def get_current_logger():
    global current_logger
    if current_logger is None:
        current_logger = MyLogger()
    return current_logger

def store(*args, **kwargs):
    logger = get_current_logger()
    return logger.store(*args, **kwargs)

def dump(*args, **kwargs):
    logger = get_current_logger()
    return logger.dump(*args, **kwargs)

def show_progress(*args, **kwargs):
    logger = get_current_logger()
    return logger.show_progress(*args, **kwargs)

def get_path():
    logger = get_current_logger()
    return logger.path

def log(msg, color="green"):
    print(termcolor.colored(msg, color, attrs=["bold"]))

def warning(msg, color="yellow"):
    print(termcolor.colored("Warning: " + msg, color, attrs=["bold"]))

def error(msg, color="red"):
    print(termcolor.colored("Error: " + msg, color, attrs=["bold"]))

def save(path):
    logger = get_current_logger()
    log_dict = {
        "stat_keys": logger.stat_keys,
        "known_keys": logger.known_keys,
        "console_formats": logger.console_formats,
        "final_keys": logger.final_keys,
    }
    log_path = create_path(path, "logger")
    torch.save(log_dict, log_path)

def load(path, time_dict):
    logger = get_current_logger()
    log_path = create_path(path, "logger")
    log_dict = torch.load(log_path)
    for k, v in log_dict.items():
        setattr(logger, k, v)
    filter_csv_by_steps(logger.log_file_path, time_dict["steps"])

def filter_csv_by_steps(csv_file, threshold):
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(csv_file)

        # Ensure the 'train/steps' column exists
        if "train/steps" not in df.columns:
            return "Error: 'train/steps' column not found in the CSV file."

        # Filter rows where 'train/steps' is less than or equal to the threshold
        filtered_df = df[df["train/steps"] <= threshold]

        # Save the filtered DataFrame back to the CSV file
        filtered_df.to_csv(csv_file, index=False)
        return f"Filtered '{csv_file}' successfully."

    except Exception as e:
        return f"An error occurred: {str(e)}"

def create_path(path, post_fix):
    return path.split("step")[0] + post_fix + ".pt"

def get_datetime():
    # Get the current date and time
    now = datetime.datetime.now()
    # Format the date and time as "YYMMDD.HHMMSS"
    formatted_datetime = now.strftime("%y%m%d.%H%M%S")
    return formatted_datetime

def timeprinting(epoch,start_time, end_time):
     # Calculate and print the duration
    duration = end_time - start_time
    minutes, seconds = divmod(duration, 60)
    
    print("-" * 30)
    print(f"Epoch: {epoch}, Duration: {int(minutes)}분 {int(seconds)}초")
    print(f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
    print("-" * 30)
