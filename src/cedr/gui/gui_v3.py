import os
import sys
import ctypes
import time
import dearpygui.dearpygui as dpg

from cedr.utils.analysis import Analyzer
from cedr.utils.metrics import Metrics


class GUI():
    def __init__(self, maximise: bool) -> None:
        self.analyzer = Analyzer()
        self.metrics = Metrics()

        self.current_visible_table = None

        self.dear_pygui_mandatory_setup()
        self.dear_pygui_configuration(maximise)
        
        self.initialize_windows()

        self.start_render_loop()

    """
        Dear pygui setup, config and initialisation functions
    """
    def dear_pygui_mandatory_setup(self) -> None:
        dpg.create_context()
        dpg.setup_dearpygui()
        dpg.create_viewport(title='GA Inspector')
        dpg.show_viewport()
        
    def dear_pygui_configuration(self, maximise: bool) -> None:
        dpg.set_global_font_scale(1.25)

        self.set_global_theme()

        user32 = ctypes.windll.user32
        screen_w = user32.GetSystemMetrics(0) 
        screen_h = user32.GetSystemMetrics(1)

        if maximise:
            dpg.maximize_viewport()
            self.viewport_width = screen_w
            self.viewport_height = screen_h
        else:
            self.viewport_width = dpg.get_viewport_width()
            self.viewport_height = dpg.get_viewport_height()

    def start_render_loop(self):
        while dpg.is_dearpygui_running():
            self.dynamically_position_intro_window()
            self.show_or_hide_toggle_all_checkbox()

            dpg.render_dearpygui_frame()

        dpg.destroy_context()

    """
        Render loop functions
    """
    def dynamically_position_intro_window(self):
        if dpg.does_item_exist('win_intro'):
            width = 950
            height = 150

            self.viewport_width = dpg.get_viewport_width()
            self.viewport_height = dpg.get_viewport_height()

            x = self.viewport_width // 2 - width // 2
            y = self.viewport_height // 2 - height // 2

            dpg.configure_item('win_intro',pos=(x,y))

    def show_or_hide_toggle_all_checkbox(self):
        if dpg.does_item_exist('ch_select') and dpg.does_item_exist('tgl_all'):
            if dpg.get_value('ch_select'):
                dpg.show_item('tgl_all')
            else:
                dpg.hide_item('tgl_all')


    """
        GUI Styling
    """
    def set_global_theme(self):
        with dpg.theme() as global_theme:

            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(
                    dpg.mvThemeCol_WindowBg, 
                    value=(0, 0, 0), 
                    category=dpg.mvThemeCat_Core
                )

                dpg.add_theme_style(
                    dpg.mvStyleVar_FrameRounding, 
                    x=5, 
                    category=dpg.mvThemeCat_Core
                )

                dpg.add_theme_style(
                    dpg.mvStyleVar_WindowPadding, 
                    x=15, 
                    y=10, 
                    category=dpg.mvThemeCat_Core
                )

                dpg.add_theme_style(
                    dpg.mvStyleVar_FrameBorderSize, 
                    x=1,
                    category=dpg.mvThemeCat_Core
                )

                dpg.add_theme_style(
                    dpg.mvStyleVar_FramePadding, 
                    x=12,
                    y=4,
                    category=dpg.mvThemeCat_Core
                )

                dpg.add_theme_style(
                    dpg.mvStyleVar_FrameRounding,
                    x=2,
                    category=dpg.mvThemeCat_Core
                )

                dpg.add_theme_style(
                    dpg.mvStyleVar_ItemInnerSpacing, 
                    x=20,
                    category=dpg.mvThemeCat_Core
                )

                dpg.add_theme_style(
                    dpg.mvStyleVar_ItemSpacing,
                    x=20,
                    y=12,
                    category=dpg.mvThemeCat_Core
                )

        dpg.bind_theme(global_theme)      

    """
        GUI Windows
    """
    def initialize_windows(self):
        # Navigation
        self.menu_bar()
        self.file_explorer()

        # Core windows
        self.intro_window()
        self.run_inspector()
        self.metrics_view()

        # Incorrect use warnings
        self.duplicate_selection_popup()

    def menu_bar(self):
         with dpg.viewport_menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(
                    label="File Explorer", 
                    callback=lambda: dpg.show_item("win_file_explorer")
                )
                dpg.add_menu_item(label="Quit", callback=self.exit)   

    @staticmethod
    def intro_window():
        width = 950
        height = 150

        message = ("Welcome!\n"
                   "This is an interactive GUI made for inspecting and "
                   "evaluating individuals from the GAs that you've run.\n"
                   "To get started, load a population by clicking"
                   "the button below.")    

        btn_x = width // 2 - 60
        btn_y = height // 1.5

        with dpg.window(
                    label="Introduction", tag="win_intro",
                    width=width, height=height, no_resize=True,
                    no_collapse=True, no_close=True, no_move=True
                ):
            dpg.add_text(message)
            dpg.add_button(
                label="Load population",
                tag="btn_intro",
                pos=(btn_x, btn_y), 
                callback=lambda: dpg.show_item("win_file_explorer")
            )

    def file_explorer(self):
        with dpg.file_dialog(
                    id='win_file_explorer',
                    width=1000, height=600,
                    default_path=os.path.join(os.getcwd()[:-4], 'runs'),
                    show=False, modal=True,
                    directory_selector=True,
                    callback=self.explorer_select
                ):
            dpg.add_file_extension(extension='.*')
            dpg.add_file_extension(
                extension='.txt',
                color=(255, 0, 255, 255),
                custom_text='[Text]'
            )
            dpg.add_file_extension(
                extension='.py',
                color=(0, 255, 0, 255),
                custom_text='[Python]'
            )   

    def run_inspector(self):
        with dpg.window(
                    label='Runs', 
                    tag='win_runs',
                    width=825,
                    height=980, 
                    pos=(5,30),
                    show=False
                ):
            dpg.add_combo(
                label='Run select', 
                tag='cmb_run_select',
                callback=self.select_run    
            )

            with dpg.collapsing_header(
                        label='Run parameters', 
                        parent='ch_run_params'
                    ):
                dpg.add_text(label="Parameters")

            dpg.add_combo(
                label='Generation select', 
                tag='cmb_generation_select',
                callback=self.select_generation    
            )

    def metrics_view(self):
        self.enable_box_row = 0
        self.box_counter = 0

        x = dpg.get_item_configuration('win_runs')['width']
        with dpg.window(
                    label='Metrics', 
                    tag='win_metrics',
                    width=1080,
                    height=980, 
                    pos=(x+10,30),
                    show=False
                ):
            
            with dpg.collapsing_header(label="Enable run", tag='ch_select'):
                with dpg.group( 
                            tag=f'enable_box_row-{self.enable_box_row}', 
                            indent=4,
                            horizontal=True, 
                            horizontal_spacing=25
                        ):
                    pass
                
                dpg.add_checkbox(
                    enabled=True,
                    default_value=True,
                    label="Enable all",
                    tag='enable_all',
                    callback=self.toggle_all,
                    indent=4
                )

    def duplicate_selection_popup(self):
        with dpg.window(
                label='Warning: Duplicate run',
                tag='win_duplicate_run_warning',
                width=280,
                height=110,
                modal=True,
                show=False 
            ):
                dpg.add_text("This run is already loaded.")
                
                dpg.add_button(
                    label='OK', 
                    callback=self.toggle_popup,
                    user_data='win_duplicate_run_warning',
                    pos=[120, 70]
                )

    """
        Callbacks
    """
    @staticmethod
    def exit():
        sys.exit(0)

    def explorer_select(self, sender, app_data, user_data):
        dpg.hide_item('win_intro')


        path = app_data['current_path']
        run_name = path.split('\\')[-1]

        time.sleep(0.02)
        if run_name in dpg.get_item_configuration('cmb_run_select')['items']:
            self.position_and_show_popup('win_duplicate_run_warning')
        else:
            self.analyzer.load_run(path, run_name)

        self.update_run_selector()
        self.update_generation_selector(run_name)
        self.add_metrics_checkbox()

        dpg.show_item('win_runs')
        dpg.show_item('win_metrics')

    @staticmethod
    def toggle_popup(sender, app_data, user_data):
        item_config = dpg.get_item_configuration(user_data)
        show_status = item_config['show']

        dpg.configure_item(user_data, show=not show_status)

    def select_run(self, sender, app_data, user_data):
        self.update_generation_selector(app_data)

    def select_generation(self, sender, app_data, user_data):
        self.update_run_table(app_data)

    def individual_select(self, sender, app_data, user_data):
        pass

    def toggle_all(self, sender):
        checkbox_tags = [f"cb_enable_box_{i+1}" 
                         for i in range(self.box_counter)]
        print(checkbox_tags)
        state = dpg.get_value(sender)

        if state:
            for tag in checkbox_tags:
                dpg.set_value(tag, True)
            # self.active_pops = [1 for _ in self.active_pops]
        else:
            for tag in checkbox_tags:
                dpg.set_value(tag, False)
            # self.active_pops = [0 for _ in self.active_pops]

    """
        State functions
    """
    def position_and_show_popup(self, tag):
        item_config = dpg.get_item_configuration(tag)
        item_w, item_h = item_config['width'], item_config['height']       

        dpg.set_item_pos(
            tag, 
            pos=[
                self.viewport_width // 2 - item_w // 2,
                self.viewport_height // 2 - item_h // 2
            ]
        )
        dpg.configure_item(tag, show=True)

    def update_run_selector(self):
        dpg.configure_item(
            'cmb_run_select', 
            items=list(self.analyzer.runs.keys())
        )

        dpg.set_value(
            'cmb_run_select', 
            value=list(self.analyzer.runs.keys())[-1]
        )

    def update_generation_selector(self, run_name):
        dpg.configure_item(
            'cmb_generation_select', 
            items=list(self.analyzer.runs[run_name].keys())
        )

    def update_run_table(self, generation):
        selected_run = dpg.get_value('cmb_run_select')

        # print(dpg.get_item_configuration('tbl_generation_view'))
        if self.current_visible_table:
            dpg.hide_item(self.current_visible_table)

        population = self.analyzer.runs[selected_run][generation]


        with dpg.table(
                    parent='win_runs',
                    tag=f'tbl_{selected_run}-{generation}',
                    header_row=True, 
                    borders_innerV=True,
                    borders_outerV=True,
                    borders_outerH=True,
                    pad_outerX=True,
                    show=True
                ):
            dpg.add_table_column(label="Rank", width_fixed=True)
            dpg.add_table_column(label="Genome")
            dpg.add_table_column(label="Fitness", width_fixed=True)
            for rank, individual in population.items():
                individual = list(individual)[0]
                with dpg.table_row(parent=f'tbl_{selected_run}-{generation}'):
                    dpg.add_text(f"{int(rank)+1}")
                    dpg.add_button(
                        label=f"{individual.genome}", 
                        callback=self.individual_select, 
                        user_data=individual.genome
                    )
                    dpg.add_text(f"{round(float(individual.fitness),2)}")

        self.current_visible_table = f'tbl_{selected_run}-{generation}'

    def add_metrics_checkbox(self):
        self.box_counter += 1

        if self.box_counter % 6 == 0:
            self.enable_box_row += 1
            with dpg.group(
                        parent='ch_select',
                        tag=f'enable_box_row-{self.enable_box_row}', 
                        indent=4,
                        horizontal=True, 
                        horizontal_spacing=25
                    ):
                pass

        dpg.add_checkbox(
            enabled=True,
            default_value=True,
            label=list(self.analyzer.runs.keys())[-1],
            tag=f"cb_enable_box_{self.box_counter}",
            parent=f"enable_box_row-{self.enable_box_row}",
            # callback=self.toggle_select,
            user_data=self.box_counter-1,
        )

        

if __name__ == '__main__':
    gui = GUI(True)