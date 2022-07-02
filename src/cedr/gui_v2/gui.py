import os
import dearpygui.dearpygui as dpg

from collections import namedtuple

from cedr.utils.analysis import Analyzer
from cedr.utils.metrics import Metrics
from cedr.utils.schemata import Schemata
from cedr.utils.encoding import hex_to_bin
from individual_preview import Previewer
from theme_presets import *

class GUI():
    def __init__(self) -> None:
        self.analyzer = Analyzer()
        self.previewer = Previewer()

        self.dear_pygui_mandatory_setup()
        self.dear_pygui_configuration()

        # dpg.show_style_editor()
        # dpg.show_item_registry()
        # dpg.show_debug()

        self.apply_theme(None, GLOBAL_THEME_STANDARD, True)

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
        dpg.maximize_viewport()

    def dear_pygui_configuration(self) -> None:
        dpg.set_global_font_scale(1.5)

    def start_render_loop(self):
        while dpg.is_dearpygui_running():
            self.dynamically_position_window_start()
            self.dynamically_position_window_main()
            dpg.render_dearpygui_frame()

        dpg.destroy_context()


    """
        Render loop functions
    """
    def dynamically_position_window_start(self):
        if dpg.does_item_exist('cwin_start'):
            self.viewport_width = dpg.get_viewport_width()
            self.viewport_height = dpg.get_viewport_height()
            
            self.cwin_start_width = self.viewport_width / 2

            btn_x = self.cwin_start_width / 2 - 100
            btn_y = (
                dpg.get_item_rect_size('intro_message_container')[1] + 
                dpg.get_item_rect_size('tab_intro')[1] +
                40
            )

            dpg.configure_item(
                item='btn_intro_load_pop',
                pos=[btn_x,btn_y]
            )

            # Weird function layout -> 
            # btn_x depends on intro_window width &
            # intro_window height depends on btn_y
     
            self.cwin_start_height = self.viewport_height / 2
            x = self.viewport_width / 4
            y = self.viewport_height / 4

            dpg.configure_item(
                item='cwin_start', 
                width=self.cwin_start_width,
                height=btn_y+80, 
                pos=(x,y)
            )

    def dynamically_position_window_main(self):
        if dpg.does_item_exist('cwin_selector'):
            self.viewport_width = dpg.get_viewport_width()
            self.viewport_height = dpg.get_viewport_height()

            self.cwin_selector_width = self.viewport_width / 2 - 80
            self.cwin_main_height = self.viewport_height - 98

            dpg.configure_item(
                item='cwin_selector',
                width=self.cwin_selector_width,
                height = self.cwin_main_height,
            )

            # dpg.configure_item(
            #     item='cwin_data',
            #     width=self.cwin_selector_width,
            #     height=self.cwin_main_height,
            # )

            dpg.configure_item(
                item='lst_box_runs',
                width=self.cwin_selector_width - 250
            )

    """
        GUI Styling
    """
    @staticmethod
    def apply_theme(
                items: list[str],
                preset: list[namedtuple],
                global_flag: bool = False
            ):
        if items is None or not isinstance(items, list):
            items = [items]

        for item in items:
            with dpg.theme() as theme:
                with dpg.theme_component():  
                    for component in preset:
                        if isinstance(component, Color):
                            dpg.add_theme_color(
                                getattr(dpg, f'mvThemeCol_{component.label}'), 
                                value=component.value,
                                category=component.category
                            )
                        elif isinstance(component, Style):
                            dpg.add_theme_style(
                                getattr(dpg, f'mvStyleVar_{component.label}'), 
                                x=component.x,
                                y=component.y,
                                category=component.category
                            )

            if global_flag:
                dpg.bind_theme(theme)
            else:
                dpg.bind_item_theme(item, theme)

    """
        GUI Windows
    """
    def initialize_windows(self):
        # Navigation
        self.menu_bar()
        self.file_explorer()

        # Core windows
        self.window_primary()
        self.child_window_start()

        # Layout
        self.group_main()

    def menu_bar(self):
        with dpg.viewport_menu_bar(tag='menu_bar'):
            dpg.add_spacer(height=15)
            
            with dpg.menu(label="File", tag='mb_file'):
                dpg.add_menu_item(
                    label="File Explorer", tag='mb_file_explorer',
                    callback=lambda: dpg.show_item("win_file_explorer")
                )
                dpg.add_menu_item(
                    label="Quit", tag='mb_quit',
                    callback=lambda: os._exit(0)
                )

            with dpg.menu(label="View", tag='mb_view'):
                dpg.add_menu_item(
                    label="Show sidebar", tag='mb_show_sidebar',
                    # callback=self.toggle_sidebar
                )
            with dpg.menu(label="Help", tag='mb_help'):
                dpg.add_menu_item(
                    label="Toggle start dialogue", tag='mb_show_start',
                    # callback=self.toggle_start
                )
                dpg.add_menu_item(
                    label='Shortcuts', tag='mb_shortcuts'
                )

        menubar_items = ['mb_file', 'mb_view', 'mb_help']

        self.apply_theme(menubar_items, MENUBAR_STANDARD)

    def file_explorer(self):
        with dpg.file_dialog(
                    id='win_file_explorer',
                    width=1000, height=600,
                    default_path=os.path.join(os.getcwd()[:-7], 'runs'),
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

    # @staticmethod
    def window_primary(self):
        dpg.add_window(
            tag='win_primary', no_resize=True, no_title_bar=True,
            no_collapse=True, no_close=True, no_move=True
        )

        dpg.set_primary_window('win_primary', True)

        self.apply_theme('win_primary', PRIMARY_WINDOW)

    def child_window_start(self):
        message = ("Welcome!\n\n"
                   "This is an interactive GUI made for inspecting and "
                   "evaluating individuals from the GAs that you've run.\n\n"
                   "To get started, load a population by clicking "
                   "the button below.\n\n")    

        features = [
            'Load populations from file explorer',
            'Run simulations with modifiable parameters',
            'Visualise fitness and diversity across runs',
            'Visualise diversity via heatmap'
        ]

        with dpg.child_window(tag='cwin_start', parent='win_primary'):
            with dpg.tab_bar(tag='tab_bar_start'):
                with dpg.tab(label=' Introduction ', tag='tab_intro'):
                    dpg.add_spacer(height=5)
                    with dpg.group(tag='intro_message_container'):
                        dpg.add_text(
                            default_value=message, tag='txt_intro_message',
                            wrap=dpg.get_item_width('cwin_start')
                        )
                        dpg.add_spacer(height=5)
                    
                    dpg.add_button(
                        label='Load population', tag='btn_intro_load_pop',
                        width=200, height=35,
                        callback=lambda: dpg.show_item('win_file_explorer')
                    )
                with dpg.tab(label=' Features ', tag='tab_features'):
                    dpg.add_spacer(height=5)
                    with dpg.group(tag='features_container'):
                        for feature in features:
                            dpg.add_text(
                                feature, bullet=True,
                                wrap=dpg.get_item_width('cwin_start'),
                            )

        tabs = ['tab_intro', 'tab_features']

        self.apply_theme('cwin_start', CHILD_START)
        self.apply_theme('btn_intro_load_pop', BUTTON_STANDARD)
        # self.apply_theme('tab_bar_start', TAB_BAR_STANDARD)
        self.apply_theme(tabs, TAB_STANDARD)

    def child_window_selector(self):
        dpg.add_spacer(parent='grp_main')
        with dpg.child_window(tag='cwin_selector', parent='grp_main'):
            dpg.add_text('Runs')

            with dpg.group(
                        tag='grp_runs_filters',
                        horizontal=True, horizontal_spacing=25
                    ):
                self.run_selector_filters('grp_runs_filters')
            dpg.add_spacer(height=2)

            with dpg.group(
                        tag='grp_run_selector', 
                        horizontal=True, horizontal_spacing= 25
                    ):
                dpg.add_listbox(
                    label=None, tag='lst_box_runs', 
                    num_items=10, callback=self.select_run
                )
                with dpg.group(tag='grp_selector_btns'):
                    dpg.add_spacer(height=157)
                    self.run_selector_buttons('grp_selector_btns')

            dpg.add_spacer(height=16)
            dpg.add_separator()
            dpg.add_spacer(height=16)

            dpg.add_text('Run simulation')
            dpg.add_spacer(height=8)
            self.simulation_paramater_tree(parent='cwin_selector')
            dpg.add_spacer(height=50)

        self.apply_theme('cwin_selector', CHILD_STANDARD)

    """
        Item Groups
    """
    def run_selector_filters(self, parent):
        sort_methods = [
            'Alphabetical (asc.)',
            'Alphabetical (desc.)',
            'Date (asc.)',
            'Date (desc.)'    
        ]

        dpg.add_combo(
            label='Sort by', tag='cmb_list_box_sort', parent=parent,
            width=300, items=sort_methods, callback=self.sort_listbox
        )

        dpg.add_input_text(
            label="Filter", tag='inpt_list_box_filter', parent=parent,
            width=300, callback=self.filter_listbox
        )

        self.apply_theme('cmb_list_box_sort', COMBO_STANDARD)
        self.apply_theme('inpt_list_box_filter', INPUT_STANDARD)

    def run_selector_buttons(self, parent):
        dpg.add_button(
            label='Show Individuals', tag='btn_show_ind', parent=parent,
            width=200, height=30, 
            # callback=self.update_run_table, user_data=None
        )
        dpg.add_button(
            label='Generate metrics', tag='btn_gen_metrics', parent=parent,
            width=200, height=30
        )
        dpg.add_button(
            label='Remove run', tag='btn_remove_run',  parent=parent,
            width=200, height=30, callback=self.delete_run
        )

        buttons = ['btn_show_ind', 'btn_gen_metrics', 'btn_remove_run']

        self.apply_theme(buttons, BUTTON_STANDARD)

    def simulation_paramater_tree(self, parent):
        with dpg.tree_node(
                    label='Parameters', 
                    tag='tree_sim_params', 
                    parent=parent
                ):
            for category in self.previewer.cfg:
                with dpg.tree_node(label=category.capitalize()):
                    for key, value in self.previewer.cfg[category].items():
                        if isinstance(value, int):
                            dpg.add_input_int(
                                label=key,
                                default_value=value,
                                min_value=0
                            )
                        elif isinstance(value, float):
                            dpg.add_input_float(
                                label=key,
                                default_value=value,
                                min_value=0
                            ) 

        self.apply_theme('tree_sim_params', TREE_NODE_STANDARD)

    """
        Layout
    """
    def group_main(self):
        dpg.add_spacer(height=50, parent='win_primary')
        
        dpg.add_group(tag='grp_main', parent='win_primary',
                      horizontal=True, horizontal_spacing=30)


    """
        Callbacks
    """
    def explorer_select(self, sender, app_data, user_data):
        if dpg.does_item_exist('cwin_start'):
            dpg.delete_item('cwin_start')

        if not dpg.does_item_exist('cwin_selector'):
            self.child_window_selector()

        items = dpg.get_item_configuration(item='lst_box_runs')['items']

        for path in app_data['selections'].values():
            formatted_path = '\\'.join(path.split('\\')[:-2])
            run_name = path.split('\\')[-1]

            formatted_path = os.path.join(formatted_path, run_name)

            if not dpg.does_item_exist(f'tl_{run_name}'):
                self.analyzer.load_run(formatted_path, run_name)

            items.append(run_name)
            dpg.configure_item(
                item='lst_box_runs', 
                items=items
            )

    def filter_listbox(self, sender, app_data, user_data):
        items = [key for key in self.analyzer.runs] 
        filtered_items = [item for item in items if app_data in item]

        dpg.configure_item(
            item='lst_box_runs', 
            items=filtered_items
        )

    def sort_listbox(self, sender, app_data, user_data):
        items = dpg.get_item_configuration('lst_box_runs')['items']

        if app_data == 'Alphabetical (asc.)':
            items.sort()
        elif app_data == 'Date (asc.)':
            pass

        if 'desc' in app_data:
            items = items[::-1]

        dpg.configure_item(
            item='lst_box_runs', 
            items=items
        )

    def select_run(self, sender, app_data, user_data):
        pass

    def delete_run(self, sender, app_data, user_data):
        items = dpg.get_item_configuration('lst_box_runs')['items']
        selected_item = dpg.get_value('lst_box_runs')

        self.analyzer.runs.pop(selected_item)
        items.remove(selected_item)

        dpg.configure_item(
            item='lst_box_runs', 
            items=items
        )


if __name__ == '__main__':
    GUI()