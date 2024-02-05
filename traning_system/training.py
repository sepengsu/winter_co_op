from tkinter import ttk
import os
import re
from typing import Any
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import sys
buttonlist = ['checkbox', 'selectbox']
gym_list = ['0918','1622','1922','2190']
_current_dir =  r"C:\Users\PC\Desktop\SJW\dep\customreward"
customreward_list = [name.split('\\')[-1] for name in os.listdir(_current_dir) if (not name.startswith('__')) and not (name=='reward.py')]

class MyTkinter:
    def __init__(self):
        self.window = Tk()
        self.window.title("Train System for Scone")
        self.window.state('zoomed')  # Maximize the window
        self.window.resizable(True, True)
        self.window.config(bg="white")
        self.trainoption = Option()
        self.create_widgets()
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)  # Add this line
        self.window.mainloop()
    def close_window(self):
        self.window.destroy()

    def create_widgets(self):
        self.name_widgets()
        self.gym_widgets()
        self.option_widgets()

    def name_widgets(self):
        self.nameframe = Frame(self.window)
        # 이름 입력 레이블
        name_label = Label(self.nameframe, text="이름:")
        name_label.pack()

        # 이름 입력 텍스트 상자
        name_entry = Entry(self.nameframe)
        name_entry.pack()

        # 확인 버튼
        confirm_button = Button(self.nameframe, text="확인", command=lambda: self.get_name(name_entry.get()))
        confirm_button.pack()

        self.nameframe.pack()

    def gym_widgets(self):
        self.optionframe = Frame(self.window)
        # 옵션 레이블
        option_label = Label(self.optionframe, text="옵션:")
        option_label.pack()

        # 옵션 콤보 상자
        option_combobox = ttk.Combobox(self.optionframe, values=gym_list, state="readonly")
        option_combobox.pack()

        # 확인 버튼
        confirm_button = Button(self.optionframe, text="확인", command=lambda: self.gym_command(option_combobox.get()))
        confirm_button.pack()

        self.optionframe.pack()
    def gym_command(self, option):
        self.trainoption.get_option(option)
        self.input_widgets()

    def option_widgets(self):
        # 옵션 프레임
        self.optionframe = Frame(self.window)

        # 옵션 레이블
        option_label = Label(self.optionframe, text="옵션:")
        option_label.pack()

        # 옵션 체크박스들
        for i,custom in enumerate(customreward_list):
            s = f"self.checkbox_{i+1} = Checkbutton(self.optionframe, text='{custom}')"
            exec(s)
            s = f"self.checkbox_{i+1}.pack(side = 'left')"
            exec(s)

        # 확인 버튼
        confirm_button = Button(self.optionframe, text="확인", command=self.option_command)
        confirm_button.pack()
        self.optionframe.pack()

    def option_command(self):
        for i in range(1, len(customreward_list)+1):
            s=f"option = self.checkbox_{i+1}.get()"
            exec(s)
            s='setattr(self.trainoption, f"option_{i}", option)'
            exec(s)
        print(vars(self.trainoption))

    def input_widgets(self):
        self.inputframe = Frame(self.window)
        # 입력 레이블
        input_label = Label(self.inputframe, text="입력:")
        input_label.pack()

        # 입력 텍스트 상자
        input_entry = Entry(self.inputframe)
        input_entry.pack()

        # 확인 버튼
        confirm_button = Button(self.inputframe, text="확인", command=lambda: self.input_command(input_entry.get()))
        confirm_button.pack()
        
        self.inputframe.pack()
    
    def input_command(self, input):
        input = slicing(input)
        print(input)
        self.trainoption.get_types(input)

    def get_name(self, name):
        self.option
        print("입력된 이름:", name)
    
class Checkbox:
    def __init__(self):
        pass   

class Option:
    def __init__(self):
        pass

    def get_name(self, name):
        self.name = name

    def get_types(self, option):
        self.types = option
    
    def get_option(self, option):
        self.option = option
def slicing(name: str):
    for sliced in buttonlist:
        name = re.sub(sliced, '', name)
    return name


if __name__ == "__main__":
    n = MyTkinter()

