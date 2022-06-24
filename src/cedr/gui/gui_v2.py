import os
import sys
import ctypes
import time
import dearpygui.dearpygui as dpg

from cedr.utils.analysis import Analyzer
from cedr.utils.metrics import Metrics

user32 = ctypes.windll.user32
screen_w, screen_h = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

class GUI():
    def __init__(self, maximise: bool) -> None:
        self.analyzer = Analyzer()
        self.metrics = Metrics()

        self.pop_counter = 0
        self.pop_row_index = 0
        self.active_pops = []

        print(os.getcwd())

        dpg.create_context()
        dpg.setup_dearpygui()
        dpg.create_viewport(title="GA Population Inspector")
        dpg.show_viewport()
        dpg.set_global_font_scale(1.25)

        dpg.show_imgui_demo()

        if maximise:
            dpg.maximize_viewport()
            self.viewport_width = screen_w
            self.viewport_height = screen_h
        else:
            self.viewport_width = dpg.get_viewport_width()
            self.viewport_height = dpg.get_viewport_height()

        self.create_menu_bar()
        self.create_introduction_window()
        self.create_file_explorer()

        self.style_gui()
        # self.style_disabled_item()


        while dpg.is_dearpygui_running():
            width = 800
            height = 120

            self.viewport_width = dpg.get_viewport_width()
            self.viewport_height = dpg.get_viewport_height()

            x = self.viewport_width // 2 - width // 2
            y = self.viewport_height // 2 - height // 2

            dpg.configure_item("intro",pos=(x,y))

            if dpg.does_item_exist("ch_select") and dpg.does_item_exist("tgl_all"):
                if dpg.get_value("ch_select"):
                    dpg.show_item("tgl_all")
                else:
                    dpg.hide_item("tgl_all")

            print(self.active_pops)

            dpg.render_dearpygui_frame()

        dpg.destroy_context()

    def exit(self):
        sys.exit(0)

    def style_gui(self):
        with dpg.theme() as global_theme:

            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0, 0, 0), category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, x=15, y=10, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, x=15, y=15, category=dpg.mvThemeCat_Core)

        dpg.bind_theme(global_theme)

    def style_selected_item(self, item):
        with dpg.theme() as item_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (255, 255, 255), category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 0, category=dpg.mvThemeCat_Core)

        dpg.bind_item_theme(item, item_theme)

    def style_disabled_item(self):
        with dpg.theme() as disabled_theme:
            with dpg.theme_component(dpg.mvInputFloat, enabled_state=False):
                dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 0, 0])
                dpg.add_theme_color(dpg.mvThemeCol_Button, [255, 0, 0])

            with dpg.theme_component(dpg.mvInputInt, enabled_state=False):
                dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 0, 0])
                dpg.add_theme_color(dpg.mvThemeCol_Button, [255, 0, 0])

        dpg.bind_theme(disabled_theme)

    def style_plot_container(self):
        with dpg.theme() as container_theme:

            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, x=15, y=0, category=dpg.mvThemeCat_Core)

        dpg.bind_item_theme("ch_plots", container_theme)

    def create_menu_bar(self):
         with dpg.viewport_menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="File Explorer", callback=lambda: dpg.show_item("file_dialog_id"))
                dpg.add_menu_item(label="Quit", callback=self.exit)

    def create_introduction_window(self):
        width = 800
        height = 150

        x = self.viewport_width // 2 - width // 2
        y = self.viewport_height // 2 - height // 2

        message = ("Welcome!\n"
                   "This is an interactive GUI made for inspecting "
                   "and evaluating individuals from the GAs that you've run.\n"
                   "To get started, load a population by clicking the button below.")

        btn_x = width // 2 - 60
        btn_y = height - 40

        with dpg.window(label="Introduction", tag="intro", width=width, height=height, pos=(x,y)):
            dpg.add_text(message)

            btn = dpg.add_button(label="Load population", pos=(btn_x, btn_y))
            dpg.set_item_callback(btn, callback=lambda: dpg.show_item("file_dialog_id"))

    def create_file_explorer(self):
        with dpg.file_dialog(
            width=1000,
            height=600,
            default_path=os.getcwd()[:-4],
            directory_selector=False,
            show=False,
            modal=True,
            callback=self.explorer_select, 
            id="file_dialog_id"
        ):
            dpg.add_file_extension(".*")
            dpg.add_file_extension(".txt", color=(255, 0, 255, 255), custom_text="[Text]")
            dpg.add_file_extension(".py", color=(0, 255, 0, 255), custom_text="[Python]")

    def create_population_inspector(self):
        with dpg.window(label="Population Inspector", tag="win_pop-insp"):
            dpg.add_tab_bar(tag="tb_pop-insp", reorderable=True)
            # with dpg.collapsing_header(label="Run parameters", parent="win_pop-insp"):
            #     dpg.add_text("HERE be the params doe")

    def append_population_tab(self):
        for n, (generation, individual) in enumerate(self.analyzer.populations.items()):
            if n == self.pop_counter-1:
                with dpg.tab(label=generation, tag=f"tbt{self.pop_counter}_pop-insp", parent="tb_pop-insp"):
                    
                    with dpg.table(
                        header_row=True, 
                        borders_innerV=True,
                        borders_outerV=True,
                        # borders_innerH=True,
                        borders_outerH=True,
                        # row_background=True,
                        pad_outerX=True,
                        
                    ):
                        dpg.add_table_column(label="Rank", width_fixed=True)
                        dpg.add_table_column(label="Genome")
                        dpg.add_table_column(label="Fitness", width_fixed=True)

                        for rank, individual in enumerate(individual):
                            with dpg.table_row():
                                dpg.add_text(f"{rank+1}")
                                dpg.add_button(label=f"{individual.genome}", callback=self.individual_select, user_data=individual.genome)
                                dpg.add_text(f"{round(float(individual.fitness),2)}")

    def create_metrics_viewer(self):
        x = dpg.get_item_width("win_pop-insp")
        w = self.viewport_width - x - 15
        h = self.viewport_height
        with dpg.window(label="Metrics", tag="win_metrics", width=w, height=h, pos=(x,0)):
            
            with dpg.collapsing_header(label="Select", tag='ch_select'):
                with dpg.group(label="populations", tag=f"pops-{self.pop_row_index}", indent=4,
                               horizontal=True, horizontal_spacing=25):
                    pass

            dpg.add_checkbox(
                enabled=True,
                default_value=True,
                label="Toggle all",
                tag='tgl_all',
                callback=self.toggle_all,
                indent=4
            )

            # with dpg.child_window(label="Data", tag="data"):
            with dpg.collapsing_header(label="Summary", tag='ch_summary'):
                with dpg.table(
                    label="Summary",
                    tag="tb_summary",
                    header_row=True, 
                    borders_innerV=True,
                    borders_outerV=True,
                    # borders_innerH=True,
                    borders_outerH=True,
                    row_background=True,
                    pad_outerX=True,
                ):
                    dpg.add_table_column(label="Name")
                    dpg.add_table_column(label="Max f.")
                    dpg.add_table_column(label="Min f.")
                    dpg.add_table_column(label="Mean f.")
                    dpg.add_table_column(label="Median f.")
                    dpg.add_table_column(label="Cutoff f.")
                    dpg.add_table_column(label="Mean d.")
                    dpg.add_table_column(label="Maximum d.")

            with dpg.collapsing_header(label="Plots", tag='ch_plots'):
                    with dpg.collapsing_header(label="Histograms", tag='ch_histo', indent=8):
                        with dpg.child_window(
                            label="histograms",
                            tag="histograms",
                            autosize_x=True, 
                            height=300,
                            indent=8    
                        ):
                            pass

                    with dpg.collapsing_header(label="Line Plots", tag='ch_line_plots', indent=8):
                        with dpg.child_window(
                            label="line_plots",  
                            autosize_x=True, 
                            height=300,
                            indent=8    
                        ):
                            pass



    def add_metrics_checkbox(self):
        if self.pop_counter % 7 == 0:
            self.pop_row_index += 1
            with dpg.group(label="populations", tag=f"pops-{self.pop_row_index}", indent=4,
                           horizontal=True, horizontal_spacing=25, parent="header_sel"):
                pass

        dpg.add_checkbox(
            enabled=True,
            default_value=True,
            label=list(self.analyzer.populations.keys())[self.pop_counter-1],
            tag=f"cb_pop_{self.pop_counter-1}",
            parent=f"pops-{self.pop_row_index}",
            callback=self.toggle_select,
            user_data=self.pop_counter-1,
        )

        self.active_pops.append(0)

    def update_summary_table(self):
        fitness_values = [
            int(float(individual.fitness))  
            for individual in self.analyzer.populations[f"population-{self.pop_counter}"]
        ]

        self.metrics.mean_fitness(fitness_values)
        self.metrics.median_fitness(fitness_values)
        self.metrics.cutoff_fitness(fitness_values, 0.2)

        ranked_genomes = [
            individual.genome 
            for individual in self.analyzer.populations[f"population-{self.pop_counter}"]
        ]
        self.metrics.population_diversity(ranked_genomes)
        self.metrics.population_mean_diversity()
        self.metrics.update_run_stats(self.pop_counter-1)

        with dpg.table_row(parent="tb_summary"):
            dpg.add_text(f'populaion-{self.pop_counter}')
            dpg.add_text(f'{fitness_values[0]}')
            dpg.add_text(f'{fitness_values[-1]}')
            dpg.add_text(f"{self.metrics.run_stats[f'generation-{self.pop_counter-1}']['mean_fitness']}")
            dpg.add_text(f"{self.metrics.run_stats[f'generation-{self.pop_counter-1}']['median_fitness']}")
            dpg.add_text(f"{self.metrics.run_stats[f'generation-{self.pop_counter-1}']['cutoff_fitness']}")
            dpg.add_text(f"{self.metrics.run_stats[f'generation-{self.pop_counter-1}']['mean_diversity']}")


    def plot_population_fitness_histogram(self):
        fitnesses = [int(float(individual.fitness)) for individual in self.analyzer.populations[f"population-{self.pop_counter}"]]
        dpg.add_simple_plot(
            tag=f"histo-population-{self.pop_counter}",
            default_value=fitnesses, 
            histogram=True, 
            height=200,
            width=1000,
            parent="histograms",
            autosize=False,
        )

    def explorer_select(self, sender, app_data, user_data):
        dpg.hide_item("intro")

        self.pop_counter += 1

        self.analyzer.load_population(list(app_data['selections'].values())[0], self.pop_counter)

        if self.pop_counter == 1:
            self.create_population_inspector()
        
        self.append_population_tab()

        time.sleep(0.05)
        if self.pop_counter == 1:
            self.create_metrics_viewer()

        self.add_metrics_checkbox()

        self.plot_population_fitness_histogram()
        self.update_summary_table()

    def toggle_select(self, sender, app_data, user_data):
        state = dpg.get_value(sender)
        if state:
            self.active_pops[user_data] = 1
        else:
            self.active_pops[user_data] = 0


    def toggle_all(self, sender):
        checkbox_tags = [f"cb_pop_{i}" for i in range(self.pop_counter)]
        state = dpg.get_value(sender)

        if state:
            for tag in checkbox_tags:
                dpg.set_value(tag, True)
            # self.active_pops = [1 for _ in self.active_pops]
        else:
            for tag in checkbox_tags:
                dpg.set_value(tag, False)
            # self.active_pops = [0 for _ in self.active_pops]

    def individual_select(self, sender, user_data, app_data):
        print(f"You selected individual {app_data}")



if __name__ == "__main__":
    gui = GUI(maximise=True)
