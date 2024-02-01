from tkinter import ttk
import os
import simulation as sim
import re
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import sys
buttonlist = ['checkbox', 'selectbox']

class MyTkinter:
    def __init__(self):
        self.window = Tk()
        self.window.title("Inference System for Scone")
        self.window.state('zoomed')  # Maximize the window
        self.window.resizable(True, True)
        self.window.config(bg="white")
        self.option = Option()
        self.data = Data()

        self.create_widgets()
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)  # Add this line
        self.window.mainloop()

    def close_window(self):
        self.window.destroy()
        sys.exit()  # Add this line

    def create_widgets(self):
        self.create_nameselectbox()
        self.create_checkboxes()  # Added checkboxes
        self.create_button()

    def create_nameselectbox(self):
        folder_path =  r"C:\Users\PC\Desktop\SJW\dep\trainconfig"
        file_names = os.listdir(folder_path)
        yaml_files = [file[:-5] for file in file_names if file.endswith(".yaml")]
        self.nameselectbox = ttk.Combobox(self.window, values=yaml_files)
        self.nameselectbox.pack()

    def create_checkboxes(self):
        '''
        (option)checkbox 형태로 attribute를 생성  
        '''
        self.checkdict = {'save':BooleanVar(), 'Max':BooleanVar(), 'more':BooleanVar(), \
                          'is_2d':BooleanVar(), 'is_3d':BooleanVar()}
        self.checkframe = Frame(master=self.window,width=300,height=60)

        self.savecheckbox = Checkbutton(self.checkframe, text="Save", variable=self.checkdict['save'])
        self.savecheckbox.pack(side=LEFT)

        self.Maxcheckbox = Checkbutton(self.checkframe, text="Max", variable=self.checkdict['Max'])
        self.Maxcheckbox.pack(side=LEFT)

        self.morecheckbox = Checkbutton(self.checkframe, text="More", variable=self.checkdict['more'])
        self.morecheckbox.pack(side=LEFT)

        self.is_2dcheckbox = Checkbutton(self.checkframe, text="2D", variable=self.checkdict['is_2d'])
        self.is_2dcheckbox.pack(side=LEFT)

        self.is_3dcheckbox = Checkbutton(self.checkframe, text="3D", variable=self.checkdict['is_3d'])
        self.is_3dcheckbox.pack(side=LEFT)
        self.checkframe.pack()

    def create_button(self):
        self.button = Button(self.window, text="Select", command=self.do)
        self.button.pack()

    def getting(self):
        self.option.name = self.nameselectbox.get()
        for key in self.checkdict:
            setattr(self.option, key, self.checkdict[key].get())

    def simulation(self):
        self.sim = sim.Simulation()
        try:
            self.sim.nameing(self.option.name)
        except Exception as e:
            print("\033[91m" + str(e) + "\033[0m")  # Print in red color
            return
        try:
            pos, vel = self.sim.inferencing(save=self.option.save, Max=self.option.Max, more=self.option.more)
            self.data.get_data(pos, vel)
        except Exception as e:
            print("\033[91m" + str(e) + "\033[0m")  # Print in red color
            return
    
    def plotting(self):
        self.plot = sim.Ploting(self.data.pos,self.data.vel,\
                                is_2d=self.option.is_2d,is_3d=self.option.is_3d)
        self.plot.plot(self.option)

    def drawing(self):
        if 'canvasframe' in dir(self):
            self.canvasframe.destroy()
        self.canvasframe = Frame(master=self.window,width=500,height=100)
        if self.option.is_2d and self.option.is_3d:
            self.canvas_2d = FigureCanvasTkAgg(self.plot.fig_2d, master=self.canvasframe)
            self.canvas_2d.get_tk_widget().pack(side=LEFT)
            self.canvas_2d.draw()
            self.canvas_3d = FigureCanvasTkAgg(self.plot.fig_3d, master=self.canvasframe)
            self.canvas_3d.get_tk_widget().pack(side=RIGHT)
            self.canvas_3d.draw()
        elif self.option.is_2d:
            self.canvas_2d = FigureCanvasTkAgg(self.plot.fig_2d, master=self.canvasframe)
            self.canvas_2d.get_tk_widget().pack(side=BOTTOM)
            self.canvas_2d.draw()
        elif self.option.is_3d:
            self.canvas_3d = FigureCanvasTkAgg(self.plot.fig_3d, master=self.canvasframe)
            self.canvas_3d.get_tk_widget().pack(side=BOTTOM)
            self.canvas_3d.draw()
        self.canvasframe.pack()


    def do(self):
        self.getting()
        self.simulation()
        self.plotting()
        self.drawing()
        self.window.update()


class Data:
    def __init__(self):
        self.pos = None
        self.vel = None

    def get_data(self, pos, vel):
        self.pos = pos
        self.vel = vel

class Option:
    def __init__(self):
        pass

def slicing(name: str):
    for sliced in buttonlist:
        name = re.sub(sliced, '', name)
    return name


if __name__ == "__main__":
    MyTkinter()


