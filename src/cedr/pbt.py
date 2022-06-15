import os
import re
import argparse
import tkinter as tk
from tkinter import ttk
from threading import Thread
from operator import attrgetter
from collections import namedtuple

from utils.analysis import Analyzer
from utils.schemata import Schemata

parser = argparse.ArgumentParser(description='load and parse populations')
parser.add_argument('--name', '-n', help='name of the experiment folder')
args = parser.parse_args()


class GUI(tk.Tk):
    def __init__(self) -> None:
        self.window = super().__init__()

        self.title("Population analyzer")
        self.geometry("1600x800") 
        self.resizable = (1, 1)

        self.params = {}
        self.running = False

        self.current_dir = os.getcwd()

        self.file_types = {
            None: "File Folder",
            "py": "Python File",
            "json": "JSON FIle",
            "txt": "Text Document"
        }

        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=100)

        self.create_frames()
        self.position_frames()
        self.create_directory_explorer()
        self.load_explorer()

    def create_frames(self):
        frm_explorer = tk.Frame(master=self.window)
        frm_explorer_fcns = tk.Frame(master=self.window)
        frm_scrollbar = tk.Frame(master=self.window)

        self.frames = {
            "explorer": frm_explorer,
            "explorer_fcns": frm_explorer_fcns,
            "scrollbar": frm_scrollbar
        }

    def position_frames(self):
        self.frames["explorer"].grid(row=1, column=0, columnspan=2,
                                     sticky='ns', padx=15, pady=(5, 15))
        self.frames["explorer_fcns"].grid(row=0, column=1, pady=(10,0))
        self.frames["scrollbar"].grid(row=1, column=2, 
                                      sticky='ns', pady=(5,15))


    def create_directory_explorer(self):
        columns = ['name', 'type']
        self.explorer_columns = namedtuple("Columns", " ".join(columns))
        
        self.explorer_loc_var = tk.StringVar()
        self.explorer_loc_var.set(self.current_dir)
        self.explorer_loc = tk.Label(
            master=self.frames["explorer_fcns"],
            text=self.explorer_loc_var.get(),
            textvariable=self.explorer_loc_var,
            padx=5, pady=1,
            highlightbackground="gray", 
            highlightthickness=1,
            bg="white"
        )
        self.explorer_loc.grid(row=0, column=1, sticky='e')

        self.explorer = ttk.Treeview(
            self.frames["explorer"], 
            columns=columns,
            show="headings"
        )
        self.explorer.pack(expand=True, fill="y")
        self.explorer.heading("name", text="Name")
        self.explorer.heading("type", text="Type")
        self.explorer.bind("<Double-1>", self.on_double_click)

        self.explorer_scrollbar = ttk.Scrollbar(
            self.frames["scrollbar"], 
            orient=tk.VERTICAL, 
            command=self.explorer.yview
        )
        self.explorer_scrollbar.pack(expand=True, fill='y')
        self.explorer.configure(yscroll=self.explorer_scrollbar.set)
        
        self.btn_explorer_back = tk.Button(
            self.frames["explorer_fcns"],
            command=self.folder_back,
            text="<-"
        )
        self.btn_explorer_back.grid(row=0, column=0)

        self.explorer_state = []

    def folder_back(self):
        self.current_dir = self.current_dir.split('\\')[:-1]
        self.current_dir = "\\".join(self.current_dir)

        self.explorer_loc_var.set(self.current_dir)
        self.clear_explorer()
        self.load_explorer()

    def load_explorer(self):
        for file in os.listdir(self.current_dir): 
            if "." in file:
                _, ext = file.split(".")
            else:
                ext = None

            file_type = self.file_types[ext]

            self.explorer_state.append(
                self.explorer_columns(file, file_type)
            )

        self.explorer_state = sorted(self.explorer_state, key=attrgetter('type'))

        for elem in self.explorer_state:
            self.explorer.insert('', tk.END, values=elem, text=elem)

    def clear_explorer(self):
        for item in self.explorer.get_children():
            self.explorer.delete(item)
        self.explorer_state.clear()

    def on_double_click(self, event):
        item_id = self.explorer.selection()[0]
        item = self.explorer.item(item_id,"text")
        file_name = item.split(" ")[0]
        file_type = re.findall(r'\{.*?\}', item)[0].strip('\{\}')

        if file_type == 'File Folder':
            self.current_dir = os.path.join(self.current_dir, file_name)
            self.explorer_loc_var.set(self.current_dir)
            self.clear_explorer()
            self.load_explorer()
        elif file_type == "Text Document":
            pass

    def create_population_inspector(self):
        columns = ("fitess", "genome")




    def open(self):
        os.system("start C:/folder dir/")

    def draw_ui(self):
        pass
        

if __name__ == "__main__":
    app = GUI()
    app.mainloop()

    # analyzer = Analyzer()

    # print(args)
    # base_path = os.getcwd()
    # full_path = os.path.join(base_path, 'runs', args.name) 

    # analyzer.load_population(full_path)




