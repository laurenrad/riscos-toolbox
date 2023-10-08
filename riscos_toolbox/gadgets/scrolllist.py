from . import Gadget
from ..events import ToolboxEvent

import ctypes
import swi

class ScrollList(Gadget):
    Selection = 0x140181
    
    # Method flags
    SelectionChangingMethod_OnAll     = 2
    SelectionChangingMethod_SendEvent = 1

    @property
    def state(self):
        return swi.swi("Toolbox_ObjectMiscOp","0iIi;I",
                       self.window.id, 16410, self.id)

    @state.setter
    def state(self, state):
        swi.swi("Toolbox_ObjectMiscOp","0iIiI",
                self.window.id, 16411, self.id, state)

    def add_item(self, text, index):
        swi.swi('Toolbox_ObjectMiscOp','0IIIs00I',
                self.window.id, 16412, self.id, text, index)

    def delete_items(self, start, end):
        swi.swi('Toolbox_ObjectMiscOp','0IIIII',
                self.window.id, 16413, self.id, start, end)

    def get_selected(self, offset=-1):
        return swi.swi('Toolbox_ObjectMiscOp','0IIIi;i',
                        self.window.id, 16416, self.id, offset)

    def make_visible(self, index):
        swi.swi('Toolbox_ObjectMiscOp','0iIii',
                self.window.id, 16417, self.id, index)
                
    def set_font(self, name, width, height):
        swi.swi('Toolbox_ObjectMiscOp','0iIisii', self.window.id,
                16420, self.id, name, width, height)
                
    # Select an item at the given index.
    # If 'all' is true, select all and ignore index.
    # If 'send_event' is true, a ScrollListSelectionEvent will be sent.
    def select_item(self, index, all=False, send_event=False):        
        flags = 0
        if all:
            flags |= ScrollList.SelectionChangingMethod_OnAll
        if send_event:
            flags |= ScrollList.SelectionChangingMethod_SendEvent
        swi.swi('Toolbox_ObjectMiscOp','IiIii', flags, self.window.id,
                16414, self.id, index)
        
    # Deselect an item at the given index.
    # Uses the same optional arguments as select_item.        
    def deselect_item(self, index, all=False, send_event=False):
        flags = 0
        if all:
            flags |= ScrollList.SelectionChangingMethod_OnAll
        if send_event:
            flags |= ScrollList.SelectionChangingMethod_SendEvent
        swi.swi('Toolbox_ObjectMiscOp','IiIii', flags, self.window.id,
                16415, self.id, index)
                
    def count_items(self):
        return self._miscop_get_int(16422)

    @property
    def multisel(self):
        return self.state & 1 != 0

    @multisel.setter
    def multisel(self, multisel):
        self.state = 1 if multisel else 0

class ScrollListSelectionEvent(ToolboxEvent):
    event_id = ScrollList.Selection

    Flags_Set         = 1<<0
    Flags_DoubleClick = 1<<1
    Flags_AdjustClick = 1<<2

    _fields_ = [ ("sel_flags", ctypes.c_uint32), ("item", ctypes.c_int32) ]

