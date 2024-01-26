"""
Creating and adding buttons and buttoncollections
defined in neagui.widgets.

Button collections are multiple buttons of the same
type and for the same purpose e.g. 
`buttoncollections.SingleSelectChannelButtons`
is a widget which contains a button for every exisiting scan
channel (M1A, O2A, Z etc.) and where only one button can be
active at a time.
"""

from neagui.widgets import buttons, buttoncollections

from PySide2 import QtWidgets

app = QtWidgets.QApplication()



master = QtWidgets.QWidget()
master.setLayout(QtWidgets.QVBoxLayout())



# 2 types of old style buttons:
# RoundedPushButton and RoundedToggleButton

push_btn1 = buttons.RoundedPushButton("Btn 1", button_size=50, color="#ff0000")
master.layout().addWidget(push_btn1)

tggl_btn1 = buttons.RoundedToggleButton(
    name="Togg", button_size=50, color="#00ff00", parent=master, enable=False, offname="Untogged" 
)
tggl_btn1.connect_(lambda btn: print(btn.display_name))
master.layout().addWidget(tggl_btn1)

# new style buttons which use instance of ButtonSettings to define everything
# ButtonSettings are then used to create instance of PushButton or ToggleButton

sub = QtWidgets.QWidget(master)
sub.setLayout(QtWidgets.QHBoxLayout())
master.layout().addWidget(sub)

push2_settings = buttons.ButtonSettings("Push2", "#cc0000", "P on", "P off", tooltip="Some text", hover_color="#aa0000")
push_btn2 = buttons.PushButton(push2_settings, sub)
push_btn2.clicked.connect(print)

togg2_settings = buttons.ButtonSettings("Push2", "#cccccc", "T on", "T off", tooltip="Some text", hover_color="#ddaadd")
togg_btn2 = buttons.ToggleButton(togg2_settings, sub)
togg_btn2.toggled.connect(print)

togg_btn2.subscribe_mouse_move_event(lambda btn_settings: print("Mouse on btn", btn_settings)) # reacts only if btn is toggled

sub.layout().addWidget(push_btn2)
sub.layout().addWidget(togg_btn2)

collection = buttoncollections.SingleSelectChannelButtons("M1A",master)
collection.subscribe_button_collection_changed(print)
collection.subscribe_mouse_move_event(lambda btn_settings: print("Mouse on btn", btn_settings))
master.layout().addWidget(collection)

master.show()

app.exec_()
