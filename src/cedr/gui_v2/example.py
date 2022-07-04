import dearpygui.dearpygui as dpg

def nested_radio_button_example(self):
    with dpg.window(label='Example'):
        dpg.add_checkbox(
            tag='button_1a', label='1a',
            default_value=True,
            callback=toggle_related_set,
            
        )

        dpg.add_radio_button(
            label='nested_buttons',
            items=['1b','1c','1d'],
            indent=24
        )

        dpg.add_checkbox(
            tag='button_2a', 
            label='2a',
            callback=toggle_related_set
        )

        dpg.add_checkbox(
            tag='button_3a', 
            label='3a',
            callback=toggle_related_set
        )

def toggle_related_set(sender):
    buttons = ['button_1a', 'button_2a', 'button_3a']
    print(dpg.get_value(sender))
    for button in buttons:
        if not button == sender:
            dpg.set_value(button, False)
        else:
            if not dpg.get_value(sender):
                dpg.set_value(sender, True)