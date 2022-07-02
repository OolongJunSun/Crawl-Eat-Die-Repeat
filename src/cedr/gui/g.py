import os
import sys
import ctypes
import time

import dearpygui.dearpygui as dpg
import dearpygui.demo as demo

from itertools import combinations
from cedr.utils.analysis import Analyzer
from cedr.utils.metrics import Metrics
from cedr.utils.schemata import Schemata
from cedr.utils.encoding import hex_to_bin
from individual_preview import Previewer


class GUI():
    def __init__(self) -> None:
        self.analyzer = Analyzer()
        self.previewer = Previewer()

        self.loaded_runs: list = []

        self.dear_pygui_mandatory_setup()
        self.dear_pygui_configuration()

        self.initialize_windows()
        
        # demo.show_demo()
        # dpg.show_implot_demo()
        # dpg.show_imgui_demo()

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

        self.set_global_theme()

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

            dpg.configure_item(
                item='cwin_data',
                width=self.cwin_selector_width,
                height=self.cwin_main_height,
            )

            dpg.configure_item(
                item='lst_box_runs',
                width=self.cwin_selector_width - 250
            )

    """
        GUI Styling
    """
    def set_global_theme(self):
        self.global_window_padding_x = 15
        self.global_window_padding_y = 10
        self.global_frame_padding_x = 0
        self.global_frame_padding_y = 6
        self.global_item_spacing_x = 12
        self.global_item_spacing_y = 6
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(
                    dpg.mvThemeCol_MenuBarBg,
                    value=(40, 40, 40),
                    category=dpg.mvThemeCat_Core
                )        
                dpg.add_theme_color(
                    dpg.mvThemeCol_WindowBg, 
                    value=(0, 0, 0), 
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_WindowBorderSize, 
                    x=0,
                    category=dpg.mvThemeCat_Core
                )                
                dpg.add_theme_style(
                    dpg.mvStyleVar_WindowPadding, 
                    x=self.global_window_padding_x,
                    y=self.global_window_padding_y,
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_FramePadding, 
                    x=self.global_frame_padding_x,
                    y=self.global_frame_padding_y,
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_ItemSpacing, 
                    x=self.global_item_spacing_x,
                    y=self.global_item_spacing_y,
                    category=dpg.mvThemeCat_Core
                )                

        dpg.bind_theme(global_theme)      

    @staticmethod
    def apply_menubar_theme(item):
        with dpg.theme() as item_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(
                    dpg.mvThemeCol_PopupBg, 
                    value=(40, 40, 40),
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_HeaderHovered, 
                    value=(70, 70, 70),
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_PopupBorderSize, 
                    x=0,
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_WindowPadding, 
                    x=12, y=6,
                    category=dpg.mvThemeCat_Core
                )

        dpg.bind_item_theme(item, item_theme)

    @staticmethod
    def apply_start_child_window_theme(item):
        with dpg.theme() as item_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(
                    dpg.mvThemeCol_ChildBg, 
                    value=(0, 0, 0),
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_WindowPadding, 
                    x=25, y=25,
                    category=dpg.mvThemeCat_Core
                )
        dpg.bind_item_theme(item, item_theme)

    @staticmethod
    def apply_selector_child_window_theme(item):
        with dpg.theme() as item_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(
                    dpg.mvThemeCol_ChildBg, 
                    value=(0, 0, 0),
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_ChildBorderSize, 
                    x=0,
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_ScrollbarSize, 
                    x=0,
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_ScrollbarRounding, 
                    x=200,
                    category=dpg.mvThemeCat_Core
                )
        dpg.bind_item_theme(item, item_theme)  

    @staticmethod
    def apply_standard_button_theme(items):
        if not isinstance(items, list):
            items = [items]

        for item in items:
            with dpg.theme() as item_theme:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(
                        dpg.mvThemeCol_Button, 
                        value=(0, 75, 128),
                        category=dpg.mvThemeCat_Core
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_ButtonHovered, 
                        value=(70, 70, 70),
                        category=dpg.mvThemeCat_Core
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_ButtonActive, 
                        value=(40, 40, 40),
                        category=dpg.mvThemeCat_Core
                    )            
                    dpg.add_theme_style(
                        dpg.mvStyleVar_FrameRounding, 
                        x=12,
                        category=dpg.mvThemeCat_Core
                    )
                    dpg.add_theme_style(
                        dpg.mvStyleVar_FramePadding, 
                        x=0, y=0,
                        category=dpg.mvThemeCat_Core
                    )           
            dpg.bind_item_theme(item, item_theme)

    @staticmethod
    def apply_standard_tab_bar_theme(item):
        with dpg.theme() as item_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(
                    dpg.mvStyleVar_FramePadding, 
                    x=20, y=0,
                    category=dpg.mvThemeCat_Core
                )

        dpg.bind_item_theme(item, item_theme)  

    @staticmethod
    def apply_standard_tab_theme(item):
        with dpg.theme() as item_theme:
            with dpg.theme_component(dpg.mvAll):
                # dpg.add_theme_color(
                #     dpg.mvThemeCol_Tab, 
                #     value=,
                #     category=dpg.mvThemeCat_Core
                # )
                dpg.add_theme_color(
                    dpg.mvThemeCol_TabHovered, 
                    value=(70, 70, 70),
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_TabActive, 
                    value=(0, 75, 128),
                    category=dpg.mvThemeCat_Core
                )            
                dpg.add_theme_style(
                    dpg.mvStyleVar_FrameRounding, 
                    x=12,
                    category=dpg.mvThemeCat_Core
                )

        dpg.bind_item_theme(item, item_theme)  

    @staticmethod
    def apply_standard_tree_node_theme(item):
        with dpg.theme() as item_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(
                    dpg.mvThemeCol_HeaderHovered, 
                    value=(0, 75, 128),
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_FramePadding, 
                    x=12,
                    category=dpg.mvThemeCat_Core
                )           


        dpg.bind_item_theme(item, item_theme)  

    @staticmethod
    def apply_standard_combo_theme(item):
        with dpg.theme() as item_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(
                    dpg.mvThemeCol_FrameBgHovered, 
                    value=(70, 70, 70),
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_HeaderHovered, 
                    value=(70, 70, 70),
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_FrameBg, 
                    value=(40, 40, 40),
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_FrameBorderSize, 
                    x=0,
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_FrameRounding, 
                    x=0,
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_PopupBorderSize, 
                    x=0,
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_WindowPadding, 
                    x=20, y=6,
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_FramePadding, 
                    x=12, y=6,
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_ItemInnerSpacing, 
                    x=20,
                    category=dpg.mvThemeCat_Core
                )

        dpg.bind_item_theme(item, item_theme)        

    @staticmethod
    def apply_standard_collapsing_header_theme(item):
        with dpg.theme() as item_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(
                    dpg.mvThemeCol_FrameBgHovered, 
                    value=(70, 70, 70),
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_HeaderHovered, 
                    value=(70, 70, 70),
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_HeaderActive, 
                    value=(0, 75, 128),
                    category=dpg.mvThemeCat_Core
                )                
            
                dpg.add_theme_style(
                    dpg.mvStyleVar_FrameBorderSize, 
                    x=0,
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_FramePadding, 
                    x=12, y=6,
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_FrameRounding, 
                    x=3,
                    category=dpg.mvThemeCat_Core
                )

        dpg.bind_item_theme(item, item_theme)        

    @staticmethod
    def apply_standard_slider_theme(item):
        with dpg.theme() as item_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(
                    dpg.mvThemeCol_FrameBgHovered, 
                    value=(70, 70, 70),
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_HeaderHovered, 
                    value=(70, 70, 70),
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_FrameBg, 
                    value=(40, 40, 40),
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_FrameBorderSize, 
                    x=0,
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_FrameRounding, 
                    x=0,
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_PopupBorderSize, 
                    x=0,
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_WindowPadding, 
                    x=20, y=6,
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_FramePadding, 
                    x=20, y=6,
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_ItemInnerSpacing, 
                    x=20,
                    category=dpg.mvThemeCat_Core
                )

        dpg.bind_item_theme(item, item_theme)         

    @staticmethod
    def apply_standard_table_theme(item):
        with dpg.theme() as item_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(
                    dpg.mvThemeCol_FrameBg, 
                    value=(40, 40, 40),
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_FrameBorderSize, 
                    x=0,
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_FrameRounding, 
                    x=3,
                    category=dpg.mvThemeCat_Core
                )

        dpg.bind_item_theme(item, item_theme)             

    @staticmethod
    def apply_standard_listbox_theme(item):
        with dpg.theme() as item_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(
                    dpg.mvThemeCol_FrameBg, 
                    value=(0, 0, 0),
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_FrameBorderSize, 
                    x=1,
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_FramePadding, 
                    x=20, y=12,
                    category=dpg.mvThemeCat_Core
                )
        dpg.bind_item_theme(item, item_theme)             

    @staticmethod
    def apply_vertical_button_group_theme(item):
        with dpg.theme() as item_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(
                    dpg.mvStyleVar_ItemSpacing, 
                    y=12,
                    category=dpg.mvThemeCat_Core
                )

        dpg.bind_item_theme(item, item_theme)

    @staticmethod
    def apply_standard_input_theme(item):
        with dpg.theme() as item_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(
                    dpg.mvStyleVar_ItemInnerSpacing, 
                    x=20,
                    category=dpg.mvThemeCat_Core
                )

        dpg.bind_item_theme(item, item_theme)

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
                    callback=self.toggle_start
                )
                dpg.add_menu_item(
                    label='Shortcuts', tag='mb_shortcuts'
                )

        self.apply_menubar_theme('mb_file')
        self.apply_menubar_theme('mb_view')
        self.apply_menubar_theme('mb_help')

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

    def window_primary(self):
        with dpg.window(
                    tag='win_primary',
                    no_resize=True, no_title_bar=True,
                    no_collapse=True, no_close=True, no_move=True
                ):
            pass

        dpg.set_primary_window('win_primary', True)

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

        self.apply_start_child_window_theme('cwin_start')
        self.apply_standard_button_theme('btn_intro_load_pop')
        # self.apply_standard_tab_bar_theme('tab_bar_start')
        self.apply_standard_tab_theme('tab_intro')
        self.apply_standard_tab_theme('tab_features')

    def child_window_main(self):
        dpg.add_spacer(height=50, parent='win_primary')
        with dpg.group(
                    tag='grp_main', parent='win_primary',
                    horizontal=True, horizontal_spacing=30
                ):
            dpg.add_spacer()
            with dpg.child_window(tag='cwin_selector', parent='grp_main'):

                dpg.add_text('Runs')

                with dpg.group(
                            tag='grp_list_box_filters',
                            horizontal=True, horizontal_spacing=25
                        ):
                    sort_methods = [
                        'Alphabetical (asc.)',
                        'Alphabetical (desc.)',
                        'Date (asc.)',
                        'Date (desc.)'    
                    ]

                    dpg.add_combo(
                        label='Sort by', tag='cmb_list_box_sort',
                        width=300, items=sort_methods,
                        callback=self.sort_listbox
                    )

                    dpg.add_input_text(
                        label="Filter", tag='inpt_list_box_filter',
                        width=300, callback=self.filter_listbox
                    )
                dpg.add_spacer(height=2)
                with dpg.group(
                            tag='grp_list_box_controls', 
                            horizontal=True, horizontal_spacing= 25
                        ):
                    with dpg.group():
                        dpg.add_listbox(
                            label=None, tag='lst_box_runs', 
                            num_items=10, callback=self.select_run
                        )
                    with dpg.group(tag='grp_btns_runs'):
                        dpg.add_spacer(height=157)
                        dpg.add_button(
                            label='Show Individuals', tag='btn_show_ind',
                            width=200, height=30,
                            callback=self.update_run_table,
                            user_data=None
                        )
                        dpg.add_button(
                            label='Generate metrics', tag='btn_gen_metrics',
                            width=200, height=30
                        )
                        dpg.add_button(
                            label='Delete run', tag='btn_delete_run',
                            width=200, height=30
                        )
                dpg.add_spacer(height=16)
                dpg.add_separator()
                dpg.add_spacer(height=16)

                dpg.add_text('Run simulation')
                dpg.add_spacer(height=8)
                with dpg.tree_node(label='Parameters'):
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
                dpg.add_spacer(height=50)               

                

            dpg.add_spacer(width=15)
            with dpg.child_window(tag='cwin_data', parent='grp_main'):
                with dpg.tab_bar(tag='tb_data'):
                    with dpg.tab(label=' Inspector ', tag='tab_inspector'):
                        dpg.add_combo(
                            label='Selected run', 
                            tag='cmb_select_run'
                        )
                        dpg.add_slider_int(
                            label='Generation',
                            tag='sld_select_generation'
                        )
                    with dpg.tab(label=' Metrics ', tag='tab_metrics'):
                        pass

            dpg.add_spacer()

        buttons = ['btn_show_ind', 'btn_gen_metrics', 'btn_delete_run']

        self.apply_selector_child_window_theme('cwin_selector')
        self.apply_standard_listbox_theme('lst_box_runs')

        self.apply_standard_slider_theme('sld_select_generation')
        self.apply_standard_input_theme('inpt_list_box_filter')
        self.apply_vertical_button_group_theme('grp_btns_runs')
        self.apply_standard_combo_theme('cmb_select_run')
        self.apply_standard_combo_theme('cmb_list_box_sort')
        self.apply_selector_child_window_theme('cwin_data')
        self.apply_standard_tab_theme('tab_metrics')
        self.apply_standard_tab_theme('tab_inspector')
        self.apply_standard_button_theme(buttons)



    """
        Callbacks
    """
    def toggle_start(self):
        if not dpg.does_item_exist('cwin_start'):
            self.child_window_start()
        else:
            dpg.delete_item('cwin_start')

    def explorer_select(self, sender, app_data, user_data):
        if dpg.does_item_exist('cwin_start'):
            dpg.delete_item('cwin_start')

        if not dpg.does_item_exist('cwin_selector'):
            self.child_window_main()

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
            # print(self.analyzer.runs)
            # self.update_run_selector()
            # self.update_generation_selector(run_name)



    def individual_select(self):
        pass

    def select_run(self, sender, app_data, user_data):
        pass
        # dpg.configure_item(sender, label=app_data)
        # print(sender)
        # print(dpg.get_item_configuration(sender))
        # print(app_data)
        # print(user_data)

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

    def update_run_table(self, sender, app_data, user_data):
        run = dpg.get_value('lst_box_runs')
        print(run)

        generation = 'generation-1'
        population = self.analyzer.runs[run][generation]

        with dpg.table(
                    label=run, tag=f'tbl_{run}', parent='tab_inspector',
                    header_row=True, borders_innerV=True, borders_outerV=True,
                    borders_outerH=True, pad_outerX=True, show=True
                ):
            dpg.add_table_column(label='Rank', width_fixed=True)
            dpg.add_table_column(label='Genome')
            dpg.add_table_column(label='Fitness', width_fixed=True)
            for rank, individual in enumerate(population):
                with dpg.table_row(parent=f'tbl_{run}-{generation}'):
                    dpg.add_text(f'{int(rank)+1}')
                    dpg.add_button(
                        tag=f'{generation}_{rank}_{individual.genome}',
                        label=f'{individual.genome}', 
                        callback=self.individual_select, 
                        user_data=individual.genome
                    )
                    dpg.add_text(f"{round(float(individual.fitness),2)}")

        items = dpg.get_item_configuration(item='cmb_select_run')['items']
        items.append(run)
        dpg.configure_item(
            item='cmb_select_run', 
            items=items
        )
        dpg.set_value(
            item='cmb_select_run',
            value=run
        )
        self.apply_standard_table_theme(f'tbl_{run}')

if __name__ == '__main__':
    GUI() 