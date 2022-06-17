import os
import re
import argparse
import tkinter as tk
from tkinter import Menu, ttk
from threading import Thread
from operator import attrgetter
from collections import namedtuple

from analysis import Analyzer
from schemata import Schemata

class GUI(tk.Tk):
    def __init__(self) -> None:
        self.window = super().__init__()

        self.analyzer = Analyzer()
        self.schemata = Schemata()

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

        self.pop_inspectors = {}
        self.inspector_scrollbars = {}
        self.pop_counter = 0

        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=50)
        self.grid_rowconfigure(2,weight=50)

        self.create_frames()
        self.position_frames()
        self.create_menu()
        self.create_directory_explorer()
        self.load_explorer()
        self.create_population_inspector()


    def onExit(self):
        self.quit()


    def create_frames(self):
        frm_menu = tk.Frame(master=self.window)
        frm_explorer = tk.Frame(master=self.window)
        frm_explorer_fcns = tk.Frame(master=self.window)
        frm_scrollbar = tk.Frame(master=self.window)
        frm_pop_inspector = tk.Frame(master=self.window)
        frm_pi_scrollbar = tk.Frame(master=self.window)


        self.frames = {
            "menu": frm_menu,
            "explorer": frm_explorer,
            "explorer_fcns": frm_explorer_fcns,
            "scrollbar": frm_scrollbar,
            "inspector": frm_pop_inspector,
            "i_sb": frm_pi_scrollbar,
        }

    def position_frames(self):
        self.frames["menu"].grid()
        self.frames["explorer"].grid(row=1, column=1, columnspan=2, rowspan=2, 
                                sticky='ns', padx=15, pady=(5, 15))
        self.frames["explorer_fcns"].grid(row=0, column=2, pady=(10,0))
        self.frames["scrollbar"].grid(row=1, column=3, rowspan=2,
                                      sticky='ns', pady=(5,15))
        self.frames["inspector"].grid(row=1, column=4, columnspan=3, 
                                        sticky='ns', pady=(5,15))
        # self.frames["inspector_2"].grid(row=2, column=4, 
        #                                 sticky='ns', pady=(5,15))
        self.frames["i_sb"].grid(row=1, column=8, 
                                  sticky='ns', pady=(5,15))
        # self.frames["isb_2"].grid(row=2, column=5, 
        #                           sticky='ns', pady=(5,15))

    def create_menu(self):
        self.menu_bar = Menu(self.frames["menu"].master)
        self.menu_bar.master.config(menu=self.menu_bar)

        self.file_menu = Menu(self.menu_bar)
        self.file_menu.add_command(label="Exit", command=self.onExit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

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

    def create_population_inspector(self):
        columns = ['fitness', 'genome']
        self.population_columns = namedtuple("Columns", " ".join(columns))        
        
        iid = 'inspector'

        self.pop_inspectors.update({
            iid: ttk.Treeview(
                self.frames[iid], 
                columns=columns,
                show="headings"
            )
        })
 
        self.pop_inspectors[iid].pack(expand=True, fill="y")
        self.pop_inspectors[iid].heading("fitness", text="Fitness")
        self.pop_inspectors[iid].heading("genome", text="Genome")
        self.pop_inspectors[iid].bind("<Double-1>", self.inspect_individual)

        self.inspector_scrollbars.update({
            iid: ttk.Scrollbar(
                self.frames['i_sb'], 
                orient=tk.VERTICAL, 
                command=self.pop_inspectors[iid].yview
            )
        })
        self.inspector_scrollbars[iid].pack(expand=True, fill='y')
        self.pop_inspectors[iid].configure(yscroll=self.inspector_scrollbars[iid].set)

        self.inspector_state = []      

    def folder_back(self):
        self.current_dir = self.current_dir.split('\\')[:-1]
        self.current_dir = "\\".join(self.current_dir)

        self.explorer_loc_var.set(self.current_dir[-64:])
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

        for item in self.explorer_state:
            self.explorer.insert('', tk.END, values=item, text=item)

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
            self.explorer_loc_var.set(self.current_dir[-64:])
            self.clear_explorer()
            self.load_explorer()
        elif file_name == "individuals.txt" and file_type == "Text Document":
            self.analyzer.load_population(os.path.join(self.current_dir, file_name), self.pop_counter)
            self.populate_inspector(self.pop_counter)
            self.pop_counter += 1
            

    def populate_inspector(self, counter):
        for individual in self.analyzer.populations[f'population-{counter}']:
            self.pop_inspectors['inspector'].insert('', tk.END, values=individual, text=individual)
            print(individual)
            # self.explorer.insert('', tk.END, values=elem, text=elem)

    def inspect_individual(self):
        pass
        

if __name__ == "__main__":
    app = GUI()
    app.mainloop()



