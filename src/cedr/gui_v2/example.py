import dearpygui.dearpygui as dpg

from collections import namedtuple

Style = namedtuple('Style', ['x', 'y', 'category', 'label'])
Color = namedtuple('Color', ['value', 'category', 'label'])

WINDOW_PRESET = [
    Style(x=10, y=10, category=0, label='WindowRounding'),
    Style(x=10, y=10, category=0, label='WindowPadding'),
    Style(x=10, y=10, category=0, label='WindowBorderSize'),
    Color(value=[255, 0, 0], category=0, label='WindowBg')

]

CHILD_PRESET = [
    Color(value=[0, 255, 0], category=0, label='ChildBg'),
    Style(x=10, y=10, category=0, label='ChildRounding')
]


def apply_theme_preset(item, preset):
    with dpg.theme() as item_theme:
        with dpg.theme_component():
            for component in preset:
                if isinstance(component, Color):
                    target = getattr(dpg, f'mvThemeCol_{component.label}')
                    dpg.add_theme_color(
                        target, 
                        value=component.value,
                        category=component.category
                    )

                elif isinstance(component, Style):
                    target = getattr(dpg, f'mvStyleVar_{component.label}')
                    dpg.add_theme_style(
                        target, 
                        x=component.x,
                        y=component.y,
                        category=component.category
                    )

    dpg.bind_item_theme(item, item_theme)


def window_example(self):
    with dpg.window(label='Test Window', tag='window_test'):
        with dpg.child_window(tag='child_test',width=300, height=300):
            pass

    apply_theme_preset('window_test', WINDOW_PRESET)
    apply_theme_preset('child_test', CHILD_PRESET)