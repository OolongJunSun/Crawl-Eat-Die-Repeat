from collections import namedtuple

Style = namedtuple('Style', ['x', 'y', 'category', 'label'])
Color = namedtuple('Color', ['value', 'category', 'label'])

# Colors
BLACK = [0, 0, 0, 255]
DARK_GRAY = [40, 40, 40, 255]
GRAY = [70, 70, 70, 255]
BLUE = [0, 75, 128, 255]

# Themes
PRESET_THEMES = {
    'GLOBAL_THEME_STANDARD': [
        Color(value=DARK_GRAY, category=0, label='MenuBarBg'),
        Color(value=BLACK, category=0, label='WindowBg'),
        Style(x=0, y=0, category=0, label='WindowBorderSize'),
        Style(x=15, y=10, category=0, label='WindowPadding'),
        Style(x=0, y=6, category=0, label='FramePadding'),
        Style(x=12, y=6, category=0, label='ItemSpacing')
    ],
    'PRIMARY_WINDOW': [
        Color(value=DARK_GRAY, category=0, label='Border'),
        Style(x=4, y=4, category=0, label='WindowBorderSize')
    ],
    'MENUBAR_STANDARD': [
        Color(value=GRAY, category=0, label='HeaderHovered'),
        Color(value=DARK_GRAY, category=0, label='PopupBg'),
        Style(x=0, y=0, category=0, label='PopupBorderSize'),
        Style(x=12, y=6, category=0, label='WindowPadding'),
    ],
    'CHILD_START': [
        Color(value=BLACK, category=0, label='ChildBg'),
        Style(x=25, y=25, category=0, label='WindowPadding')
    ],
    'CHILD_STANDARD': [
        Color(value=BLACK, category=0, label='ChildBg'),
        Style(x=0, y=0, category=0, label='ChildBorderSize'),
        Style(x=0, y=0, category=0, label='ScrollbarSize')
    ],
    'BUTTON_STANDARD': [
        Color(value=BLUE, category=0, label='Button'),
        Color(value=GRAY, category=0, label='ButtonHovered'),
        Color(value=DARK_GRAY, category=0, label='ButtonActive'),
        Style(x=12, y=12, category=0, label='FrameRounding'),
        Style(x=0, y=0, category=0, label='FramePadding')
    ],
    'BUTTON_RUN_TABLE': [
        Color(value=BLACK, category=0, label='Button'),
        Style(x=6, y=6, category=0, label='FrameRounding'),
        Style(x=12, y=6, category=0, label='FramePadding')
    ],
    'TAB_BAR_STANDARD': [
        Style(x=20, y=20, category=0, label='FramePadding'),
        Style(x=10, y=0, category=0, label='ItemInnerSpacing')
    ],
    'TAB_STANDARD': [
        Color(value=DARK_GRAY, category=0, label='TabHovered'),
        Color(value=BLUE, category=0, label='TabActive'),
        Style(x=12, y=12, category=0, label='FrameRounding')
    ],
    'TREE_NODE_STANDARD': [
        Color(value=BLUE, category=0, label='HeaderHovered'),
        Style(x=12, y=12, category=0, label='FramePadding')
    ],
    'COMBO_STANDARD': [
        Color(value=DARK_GRAY, category=0, label='FrameBgHovered'),
        Color(value=DARK_GRAY, category=0, label='HeaderHovered'),
        Color(value=BLACK, category=0, label='FrameBg'),
        Style(x=1, y=1, category=0, label='FrameBorderSize'),
        Style(x=0, y=0, category=0, label='FrameRounding'),
        Style(x=0, y=0, category=0, label='PopupBorderSize'),
        Style(x=20, y=6, category=0, label='WindowPadding'),
        Style(x=12, y=6, category=0, label='FramePadding'),
        Style(x=20, y=0, category=0, label='ItemInnerSpacing')
    ],
    'COLLAPSING_HEADER_STANDARD': [
        Color(value=GRAY, category=0, label='FrameBgHovered'),
        Color(value=GRAY, category=0, label='HeaderHovered'),
        Color(value=BLUE, category=0, label='HeaderActive'),
        Style(x=0, y=0, category=0, label='FrameBorderSize'),
        Style(x=12, y=6, category=0, label='FramePadding'),
        Style(x=3, y=0, category=0, label='FrameRounding'),  
    ],
    'SLIDER_STANDARD': [
        Color(value=BLACK, category=0, label='FrameBg'),
        Color(value=DARK_GRAY, category=0, label='FrameBgHovered'),
        Color(value=BLUE, category=0, label='SliderGrab'),
        Style(x=1, y=1, category=0, label='FrameBorderSize'),
        Style(x=12, y=12, category=0, label='GrabRounding')
    ],
    'TABLE_STANDARD': [
        Color(value=BLACK, category=0, label='FrameBg'),
    ],
    'INPUT_STANDARD': [
        Color(value=BLACK, category=0, label='FrameBg'),    
        Style(x=1, y=1, category=0, label='FrameBorderSize'),
        Style(x=20, y=0, category=0, label='ItemInnerSpacing'),
        Style(x=12, y=6, category=0, label='FramePadding')
    ],
    'LISTBOX_STANDARD': [
        Color(value=BLACK, category=0, label='FrameBg'),
        Style(x=2, y=2, category=0, label='FrameBorderSize'),
        Style(x=12, y=6, category=0, label='FramePadding')
    ]
}

# GLOBAL_THEME_STANDARD = [
#     Color(value=DARK_GRAY, category=0, label='MenuBarBg'),
#     Color(value=BLACK, category=0, label='WindowBg'),
#     Style(x=0, y=0, category=0, label='WindowBorderSize'),
#     Style(x=15, y=10, category=0, label='WindowPadding'),
#     Style(x=0, y=6, category=0, label='FramePadding'),
#     Style(x=12, y=6, category=0, label='ItemSpacing')
# ]

# PRIMARY_WINDOW = [
#     Color(value=DARK_GRAY, category=0, label='Border'),
#     Style(x=4, y=4, category=0, label='WindowBorderSize')
# ]

# MENUBAR_STANDARD = [
#     Color(value=GRAY, category=0, label='HeaderHovered'),
#     Color(value=DARK_GRAY, category=0, label='PopupBg'),
#     Style(x=0, y=0, category=0, label='PopupBorderSize'),
#     Style(x=12, y=6, category=0, label='WindowPadding'),
# ]

# CHILD_START = [
#     Color(value=BLACK, category=0, label='ChildBg'),
#     Style(x=25, y=25, category=0, label='WindowPadding')
# ]

# CHILD_STANDARD = [
#     Color(value=BLACK, category=0, label='ChildBg'),
#     Style(x=0, y=0, category=0, label='ChildBorderSize'),
#     Style(x=0, y=0, category=0, label='ScrollbarSize')
# ]

# BUTTON_STANDARD = [
#     Color(value=BLUE, category=0, label='Button'),
#     Color(value=GRAY, category=0, label='ButtonHovered'),
#     Color(value=DARK_GRAY, category=0, label='ButtonActive'),
#     Style(x=12, y=12, category=0, label='FrameRounding'),
#     Style(x=0, y=0, category=0, label='FramePadding')
# ]

# BUTTON_RUN_TABLE = [
#     Color(value=BLACK, category=0, label='Button'),
#     Style(x=6, y=6, category=0, label='FrameRounding'),
#     Style(x=12, y=6, category=0, label='FramePadding')
# ]

# TAB_BAR_STANDARD = [
#     Style(x=20, y=20, category=0, label='FramePadding'),
#     Style(x=10, y=0, category=0, label='ItemInnerSpacing')
# ]

# TAB_STANDARD = [
#     Color(value=DARK_GRAY, category=0, label='TabHovered'),
#     Color(value=BLUE, category=0, label='TabActive'),
#     Style(x=12, y=12, category=0, label='FrameRounding')
# ]

# TREE_NODE_STANDARD = [
#     Color(value=BLUE, category=0, label='HeaderHovered'),
#     Style(x=12, y=12, category=0, label='FramePadding')
# ]

# COMBO_STANDARD = [
#     Color(value=DARK_GRAY, category=0, label='FrameBgHovered'),
#     Color(value=DARK_GRAY, category=0, label='HeaderHovered'),
#     Color(value=BLACK, category=0, label='FrameBg'),
#     Style(x=1, y=1, category=0, label='FrameBorderSize'),
#     Style(x=0, y=0, category=0, label='FrameRounding'),
#     Style(x=0, y=0, category=0, label='PopupBorderSize'),
#     Style(x=20, y=6, category=0, label='WindowPadding'),
#     Style(x=12, y=6, category=0, label='FramePadding'),
#     Style(x=20, y=0, category=0, label='ItemInnerSpacing')
# ]

# COLLAPSING_HEADER_STANDARD = [
#     Color(value=GRAY, category=0, label='FrameBgHovered'),
#     Color(value=GRAY, category=0, label='HeaderHovered'),
#     Color(value=BLUE, category=0, label='HeaderActive'),
#     Style(x=0, y=0, category=0, label='FrameBorderSize'),
#     Style(x=12, y=6, category=0, label='FramePadding'),
#     Style(x=3, y=0, category=0, label='FrameRounding'),  
# ]

# SLIDER_STANDARD = [
#     Color(value=BLACK, category=0, label='FrameBg'),
#     Color(value=DARK_GRAY, category=0, label='FrameBgHovered'),
#     Color(value=BLUE, category=0, label='SliderGrab'),
#     Style(x=1, y=1, category=0, label='FrameBorderSize'),
#     Style(x=12, y=12, category=0, label='GrabRounding')
# ]

# TABLE_STANDARD = [
#     Color(value=BLACK, category=0, label='CellBg'),
# ]

# INPUT_STANDARD = [
#     Color(value=BLACK, category=0, label='FrameBg'),    
#     Style(x=1, y=1, category=0, label='FrameBorderSize'),
#     Style(x=20, y=0, category=0, label='ItemInnerSpacing'),
#     Style(x=12, y=6, category=0, label='FramePadding')
# ]

# LISTBOX_STANDARD = [
#     Color(value=BLACK, category=0, label='FrameBg'),
#     Style(x=2, y=2, category=0, label='FrameBorderSize'),
#     Style(x=12, y=6, category=0, label='FramePadding')
# ]