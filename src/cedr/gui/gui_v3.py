import os
import sys
import ctypes
import time
import numpy as np
import dearpygui.dearpygui as dpg
from itertools import combinations
from cedr.utils.analysis import Analyzer
from cedr.utils.metrics import Metrics
from cedr.utils.schemata import Schemata
from cedr.utils.encoding import hex_to_bin
from individual_preview import Previewer

import dearpygui.demo as demo

class GUI():
    def __init__(self, maximise: bool) -> None:
        self.analyzer = Analyzer()
        self.metrics = Metrics()
        self.schemata = Schemata()
        self.previewer = Previewer()

        self.current_visible_table = None

        self.dear_pygui_mandatory_setup()
        self.dear_pygui_configuration(maximise)
        
        self.initialize_windows()
        self.initialize_handlers()

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
        dpg.configure_app(docking=True, docking_space=True)
        dpg.set_global_font_scale(1.25)

        self.set_global_theme()
        self.set_important_btn_theme()
        self.set_previewer_theme()
        
        # demo.show_demo()
        # dpg.show_implot_demo()
        # dpg.show_imgui_demo()

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

    def show_or_hide_previewer_tooltip(self):
        # previewer_state = dpg.get_item_configuration('win_previewer')
        # previewer_shown = previewer_state['show']

        # if not previewer_shown: 
        #     with dpg.tooltip(f'{individual.genome}'):
        #         dpg.add_text('Click to add to previewer')
        pass


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

    def set_important_btn_theme(self):
        with dpg.theme() as self.important_btn_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(
                    dpg.mvThemeCol_Button, 
                    (255, 255, 255), 
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_Text, 
                    (0, 0, 0), 
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_ButtonHovered, 
                    (200, 200, 200), 
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_ButtonActive, 
                    (100, 100, 100), 
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_Border, 
                    (255, 255, 255), 
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_FrameRounding, 
                    100, 
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_ItemSpacing,
                    x=20,
                    y=12,
                    category=dpg.mvThemeCat_Core
                )

    def set_previewer_theme(self):
        with dpg.theme() as self.previewer_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(
                    dpg.mvThemeCol_WindowBg, 
                    value=(0, 0, 0), 
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_TitleBgActive,
                    value=(100, 0, 100),
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
                    dpg.mvStyleVar_FramePadding, 
                    x=12,
                    y=4,
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_ItemSpacing,
                    x=20,
                    y=16,
                    category=dpg.mvThemeCat_Core
                )

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
        self.individual_preview()

        # State popups
        self.simulation_in_progress_popup()

        # Incorrect use warnings
        self.duplicate_selection_popup()

    def initialize_handlers(self):
        self.genome_hover_handler()

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

            with dpg.group(
                        label='grp_generate_metrics',
                        horizontal=True,
                        horizontal_spacing=15
                    ):
                dpg.add_button(
                    label='Generate metrics for this run',
                    tag='btn_generate_metrics',
                    callback=self.calculate_run_metrics
                )
                dpg.bind_item_theme(
                    'btn_generate_metrics',
                    self.important_btn_theme
                )
                dpg.add_progress_bar(
                    label='Progress = X',
                    tag='prg_generate_metrics',
                    width=495,
                    show=False
                )
            
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

            with dpg.collapsing_header(
                        label="Fitness Plots",
                        tag='ch_fit_plots'
                    ):
                
                with dpg.collapsing_header(
                        label="Mean fitness",
                        tag='ch_mean_fitness',
                        indent=12,
                    ):
                

                    with dpg.plot(
                            tag='plot_mean_fitness',
                            width=1030,
                            height=320,
                            anti_aliased=True,
                            no_mouse_pos=True,
                            
                        ):
                        dpg.add_plot_axis(
                            label='Generation',
                            tag='x_axis_mean_fitness',
                            axis=0,
                            lock_min=True,
                        )
                        dpg.add_plot_axis(
                            label='Fitness',
                            tag='y_axis_mean_fitness',
                            axis=1,
                            lock_min=True,
                        )
                        dpg.add_plot_legend(
                            parent='plot_mean_fitness',
                            location=dpg.mvPlot_Location_SouthEast,
                        )


                with dpg.collapsing_header(
                        label="Median fitness",
                        tag='ch_median_fitness',
                        indent=12,
                    ):
                
                    with dpg.plot(
                            tag='plot_median_fitness',
                            width=1030,
                            height=320,
                            anti_aliased=True,
                            no_mouse_pos=True,
                        ):
                        dpg.add_plot_axis(
                            tag='x_axis_median_fitness',
                            axis=0,
                            lock_min=True,
                        )
                        dpg.add_plot_axis(
                            label='Fitness',
                            tag='y_axis_median_fitness',
                            axis=1,
                            lock_min=True,
                        )
                        dpg.add_plot_legend(
                            location=dpg.mvPlot_Location_SouthEast,
                        )

                with dpg.collapsing_header(
                        label="Cut-off fitness",
                        tag='ch_cutoff_fitness',
                        indent=12,
                    ):
                
                    with dpg.plot(
                            tag='plot_cutoff_fitness',
                            width=1030,
                            height=320,
                            anti_aliased=True,
                            no_mouse_pos=True,
                        ):
                        dpg.add_plot_axis(
                            tag='x_axis_cutoff_fitness',
                            axis=0,
                            lock_min=True,
                        )
                        dpg.add_plot_axis(
                            label='Fitness',
                            tag='y_axis_cutoff_fitness',
                            axis=1,
                            lock_min=True,
                        )
                        dpg.add_plot_legend(
                            location=dpg.mvPlot_Location_SouthEast,
                            drop_callback=None
                        )

            with dpg.collapsing_header(
                        label='Diversity',
                        tag='ch_diversity'
                    ):
                with dpg.collapsing_header(
                        label="Mean diversity",
                        tag='ch_mean_diversity',
                        indent=12,
                    ):
                    with dpg.plot(
                            tag='plot_mean_diversity',
                            width=1030,
                            height=320,
                            anti_aliased=True,
                            no_mouse_pos=True,
                        ):
                        dpg.add_plot_axis(
                            tag='x_axis_mean_diversity',
                            axis=0,
                            lock_min=True,
                        )
                        dpg.add_plot_axis(
                            label='Diversity',
                            tag='y_axis_mean_diversity',
                            axis=1,
                            lock_min=True,
                        )
                        dpg.add_plot_legend(
                            location=dpg.mvPlot_Location_NorthEast,
                            drop_callback=None
                        )

                with dpg.collapsing_header(
                        label="Diversity matrix",
                        tag='ch_diversity_matrix',
                        indent=12,
                    ):

                    self.colormaps = [
                        dpg.mvPlotColormap_Default,
                        dpg.mvPlotColormap_Plasma,
                        dpg.mvPlotColormap_Viridis,
                        dpg.mvPlotColormap_Pastel,
                        # dpg.mvPlotColormap_Spectral,
                        # dpg.mvPlotColormap_Greys,
                        dpg.mvPlotColormap_Paired,
                        dpg.mvPlotColormap_Deep,
                        # dpg.mvPlotColormap_BrBG,
                        # dpg.mvPlotColormap_RdBu,
                        # dpg.mvPlotColormap_PiYG,
                        dpg.mvPlotColormap_Cool,
                        dpg.mvPlotColormap_Hot,
                        dpg.mvPlotColormap_Jet,
                        dpg.mvPlotColormap_Twilight,
                    ]

                    self.active_colormap = 0

                    self.previous_heatmap = None
                    with dpg.group(
                                tag='grp_heatmap_config',
                                horizontal=True, 
                                horizontal_spacing=25
                            ):
                        dpg.add_slider_int(
                            label='Generation',
                            tag='slide_diversity_matrix',
                            indent=12,
                            callback=self.generate_diversity_matrix
                        )
                        dpg.add_colormap_button(
                            label='Change colormap',
                            width=200,
                            height=50,
                            tag='btn_colormap',
                            default_value=dpg.mvPlotColormap_Plasma,
                            callback=self.set_heatmap_colors
                        )
                    
                    with dpg.group(
                        tag='grp_heatmap_display',
                        horizontal=True,
                        horizontal_spacing=25
                    ):
                        with dpg.plot(
                                    tag='plot_diversity_heatmap',
                                    width=640,
                                    height=640,
                                    anti_aliased=False,
                                    no_mouse_pos=True,
                                    equal_aspects=True
                                ):
                            dpg.add_plot_axis(
                                label='Individual',
                                tag='x_axis_diversity_heatmap',
                                axis=0,
                                # lock_min=True,
                                # lock_max=True
                            )
                            dpg.add_plot_axis(
                                label='Individual',
                                tag='y_axis_diversity_heatmap',
                                axis=1,
                                # lock_min=True,
                                # lock_max=True
                            )


            with dpg.collapsing_header(
                        label='Schemata',
                        tag='ch_schemata'
                    ):
                pass

    def individual_preview(self):
        with dpg.window(
                    label='Previewer',
                    tag='win_previewer',
                    show=False,
                    autosize=True
                ):
            
            dpg.add_combo(
                label='Selected Individul',
                tag='cmb_individual_select',
                width=700,
                callback=None,
                items=[]
            )
            with dpg.collapsing_header(
                        label='Simulation configuration',
                        tag='ch_sim_cfg'
                    ):

                for category in self.previewer.cfg:
                    for param, value in self.previewer.cfg[category].items():
                        dpg.add_input_int(
                            label=param,
                            tag=f'input_{param}',
                            default_value=value,
                            indent=12,
                            callback=self.update_simulation_config,
                            user_data=[category, param, value]
                        )   

            dpg.add_button(
                label='Run',
                tag='btn_run_simulation',
                callback=self.run_simulation
            )

        dpg.bind_item_theme(
            'win_previewer',
            self.previewer_theme
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

    def simulation_in_progress_popup(self):
        with dpg.window(
                    label='Simulation in progress',
                    tag='win_sim_in_prog',
                    width=200,
                    height=100,
                    modal=True,
                    show=False
                ):
            pass

    """
        Callbacks
    """
    @staticmethod
    def exit():
        sys.exit(0)

    def explorer_select(self, sender, app_data, user_data):
        dpg.hide_item('win_intro')


        print('--------------------------------------------------')
        if self.current_visible_table:
            dpg.hide_item(self.current_visible_table)

        for path in app_data['selections'].values():
            
        
            formtatted_path = '\\'.join(path.split('\\')[:-2])
            run_name = path.split('\\')[-1]

            formtatted_path = os.path.join(formtatted_path, run_name)
            print(formtatted_path)
            print(run_name)

            print('')
            time.sleep(0.02)
            if run_name in dpg.get_item_configuration('cmb_run_select')['items']:
                self.position_and_show_popup('win_duplicate_run_warning')
            else:
                self.analyzer.load_run(formtatted_path, run_name)

            self.update_run_selector()
            self.update_generation_selector(run_name)

        dpg.show_item('win_runs')

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
        window_state = dpg.get_item_configuration('win_previewer')
        window_shown = window_state['show']

        if not window_shown:
            dpg.show_item('win_previewer')

        items = dpg.get_item_configuration('cmb_individual_select')['items']

        items.append(f'{user_data}')

        dpg.configure_item(
            'cmb_individual_select', 
            items=items
        )
        
    def toggle_all(self, sender):
        runs = self.metrics.runs

        checkbox_tags = [f"cb_enable_box_{run}" 
                         for run in runs]

        state = dpg.get_value(sender)
        
        for tag, run in zip(checkbox_tags, runs):
            if state:
                dpg.set_value(tag, True)
            else:
                dpg.set_value(tag, False)

            callback = dpg.get_item_callback(tag)(
                sender=tag,
                app_data=None,
                user_data=run
            )

    def calculate_run_metrics(self):
        dpg.show_item('prg_generate_metrics')
        run = dpg.get_value('cmb_run_select')
        
        self.tracked_metrics = [
            'mean_fitness',
            'median_fitness',
            'cutoff_fitness',
            'mean_diversity'
        ]

        for i, (gen, population) in enumerate(self.analyzer.runs[run].items()):
            fitnesses = [float(individual.fitness) for individual in population]
            genomes = [individual.genome for individual in population]

            self.metrics.mean_fitness(fitnesses)
            self.metrics.median_fitness(fitnesses)
            self.metrics.cutoff_fitness(fitnesses, 0.2)
            self.metrics.population_diversity(genomes)
            self.metrics.mean_diversity()
            self.metrics.update_run_stats(gen)

            dpg.set_value(
                'prg_generate_metrics', 
                i / (len(self.analyzer.runs[run]) - 1)
            )

        
        self.add_metrics_checkbox()
        self.metrics.add_to_runs(run)
        self.add_line_plots(self.tracked_metrics)

        if dpg.does_item_exist('win_metrics'):
            dpg.configure_item(
                'slide_diversity_matrix', 
                max_value=len(self.analyzer.runs[run])-1
            )

        dpg.hide_item('prg_generate_metrics')
        dpg.show_item('win_metrics')
        
    def toggle_run_metrics(self, sender, app_data, user_data):
        state = dpg.get_value(sender)
        for metric in self.tracked_metrics:
            if state:
                dpg.show_item(f'ls_{user_data}-{metric}')
            else:
                dpg.hide_item(f'ls_{user_data}-{metric}')

    def run_simulation(self):
        dpg.show_item('win_sim_in_prog')

        self.previewer.genome = dpg.get_value('cmb_individual_select')
        self.previewer.create_individual()
        self.previewer.create_environment()
        self.previewer.simulate()

        dpg.hide_item('win_sim_in_prog')

    def update_simulation_config(self, sender, app_data, user_data):
        value = dpg.get_value(sender)
        self.previewer.cfg[user_data[0]][user_data[1]] = value

    def generate_diversity_matrix(self, sender):
        run = dpg.get_value('cmb_run_select')
        state = dpg.get_value(sender)
        gen = f'generation-{state}'



        genomes = [individual.genome.replace(' ', '') 
                   for individual in self.analyzer.runs[run][gen]]

        binary_genes = [np.fromstring(hex_to_bin(genome),'u1') - ord('0') 
                        for genome in genomes]

        diversity = [np.count_nonzero(base_genome!=comparison_genome) 
                     for base_genome in binary_genes
                     for comparison_genome in binary_genes]

        if dpg.does_item_exist('heatmap_scale'):
            dpg.delete_item('heatmap_scale')

        dpg.add_colormap_scale(
            tag='heatmap_scale',
            colormap=self.colormaps[self.active_colormap],
            parent='grp_heatmap_display',
            height=640,
            width=100,
            min_scale=0,
            max_scale=125
        )

        if dpg.does_item_exist(self.previous_heatmap):
            dpg.delete_item(self.previous_heatmap)

        dpg.add_heat_series(
            label='Heat map',
            tag=f'hm_diversity-{run}-{gen}',
            parent='x_axis_diversity_heatmap',
            x=diversity,
            scale_min=0,
            scale_max=125,
            bounds_min=(0,0),
            bounds_max=(len(genomes),len(genomes)),
            rows=len(genomes),
            cols=len(genomes),
            format='',
            contribute_to_bounds=False
        )

        dpg.configure_item(
            item='plot_diversity_heatmap',
            label=f'{run} {gen}'
        )
        # dpg.bind_colormap(
        #     item='plot_diversity_heatmap', 
        #     source=self.active_colormap
        # )

        self.previous_heatmap = f'hm_diversity-{run}-{gen}'

    def set_heatmap_colors(self, sender):
        self.active_colormap += 1
        self.active_colormap = self.active_colormap % len(self.colormaps)

        dpg.bind_colormap(sender, self.colormaps[self.active_colormap])
        dpg.bind_colormap(
            item='plot_diversity_heatmap', 
            source=self.colormaps[self.active_colormap]
        )

        print(self.active_colormap)

        dpg.configure_item(
            item='heatmap_scale',
            colormap=self.colormaps[self.active_colormap]
        )

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
        dpg.set_value('cmb_generation_select', None)

    def update_run_table(self, generation):
        selected_run = dpg.get_value('cmb_run_select')

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
            dpg.add_table_column(label='Rank', width_fixed=True)
            dpg.add_table_column(label='Genome')
            dpg.add_table_column(label='Fitness', width_fixed=True)
            for rank, individual in enumerate(population):
                with dpg.table_row(parent=f'tbl_{selected_run}-{generation}'):
                    dpg.add_text(f'{int(rank)+1}')
                    dpg.add_button(
                        tag=f'{generation}_{rank}_{individual.genome}',
                        label=f'{individual.genome}', 
                        callback=self.individual_select, 
                        user_data=individual.genome
                    )
                    dpg.add_text(f"{round(float(individual.fitness),2)}")

                # dpg.bind_item_handler_registry(
                #     f'{individual.genome}',
                #     'hndler_genome_hover'
                # )

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

        run = dpg.get_value('cmb_run_select')

        dpg.add_checkbox(
            enabled=True,
            default_value=True,
            label=list(self.analyzer.runs.keys())[-1],
            tag=f'cb_enable_box_{run}',
            parent=f'enable_box_row-{self.enable_box_row}',
            callback=self.toggle_run_metrics,
            user_data=run
        )

    def add_line_plots(self, metrics: list[str]):
        run = dpg.get_value('cmb_run_select')

        for metric in metrics:
            n_generations = len(self.metrics.runs[run])
            value_series = [float(generation[metric]) 
                            for generation in self.metrics.runs[run].values()]

            dpg.add_line_series(
                parent=f'x_axis_{metric}',
                tag=f'ls_{run}-{metric}',
                label=run,
                x=list(range(n_generations)),
                y=value_series
            )

    def show_genome_preview(self, sender):
        print(sender)
        with dpg.tooltip(sender):
            dpg.add_text("A tooltip")

        print('hovered')
        # with dpg.window(label="TEST"):
        #     pass



    """
        Handlers
    """
    def genome_hover_handler(self):
        with dpg.item_handler_registry(tag="hndler_genome_hover"):
            dpg.add_item_hover_handler(callback=self.show_genome_preview)

       

if __name__ == '__main__':
    gui = GUI(True)