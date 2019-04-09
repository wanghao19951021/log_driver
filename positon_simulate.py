# coding=utf-8
import time
from threading import *
import wx
import os

dict_device_motion = {}
dict_device_temperate = {}


# list_button_temp_lists = [wx.NewId() for keys in dict_device_temperate]
EVT_RESULT_ID = wx.NewId()
EVT_STATE_ID = wx.NewId()

# Button definitions
ID_START = wx.NewId()
ID_STOP = wx.NewId()
ID_BUTTON = wx.NewId()

dict_device = \
    {
        "M047": (160, 120), "M046": (120, 310), "M045": (160, 560), "L001": (110, 710), "M027": (140, 1080),
        "L003": (290, 1050), "L004": (330, 1880), "M031": (370, 1350), "T003": (370, 1380), "M032": (370, 1570),
        "M033": (370, 1790), "M048": (460, 120), "M049": (460, 310), "T004": (460, 350), "M050": (460, 560),
        "M043": (460, 900), "M028": (460, 1080), "M044": (490, 740), "D004": (520, 790), "M036": (650, 1360),
        "M035": (650, 1570), "M034": (650, 1790), "E002": (670, 610), "T005": (670, 700), "D003": (690, 1180),
        "M042": (740, 900), "M029": (740, 1080), "M030": (740, 1220), "M037": (900, 1080), "D005": (900, 1160),
        "M038": (960, 1270), "M039": (960, 1520), "L006": (960, 1600), "M040": (960, 1740), "M041": (960, 1820),
        "L007": (960, 1880), "D006": (990, 1780), "F001": (1120, 1590), "F002": (1120, 1870), "L002": (1130, 710),
        "L005": (1160, 1250),
        "R002": (1380, 630), "I001": (1390, 840), "M025": (1420, 1830), "I012": (1430, 870), "M026": (1430, 1600),
        "D013": (1440, 790), "M004": (1460, 160), "M003": (1460, 430), "M002": (1460, 670), "L009": (1530, 1770),
        "D001": (1570, 1970), "M001": (1690, 920), "M023": (1690, 1010), "M022": (1690, 1270), "M021": (1690, 1530),
        "M024": (1690, 1830), "M005": (1750, 160), "M006": (1750, 430), "T001": (1750, 430), "M007": (1750, 670),
        "D012": (1840, 1070), "L011": (1950, 1780), "M020": (1960, 1740), "M019": (1970, 1530), "M008": (1980, 780),
        "I008": (2010, 510), "I009": (2010, 580), "M011": (2050, 160), "M010": (2050, 430), "M009": (2050, 670),
        "R001": (2050, 1370), "D008": (2060, 1030), "D009": (2060, 1090), "D010": (2060, 1220), "E001": (2160, 200),
        "D002": (2220, 20), "L010": (2260, 1220), "M051": (2290, 1770), "M015": (2300, 930), "M016": (2300, 1010),
        "M017": (2300, 1270), "T002": (2300, 1320), "M018": (2300, 1530), "M012": (2370, 160), "M013": (2370, 430),
        "M014": (2370, 670), "D011": (2450, 1760), "I007": (2490, 130), "D016": (2510, 1050), "D017": (2510, 1300),
        "D014": (2550, 1440), "D015": (2550, 1540)
    }




list_button_lists = [wx.NewId() for keys in dict_device]


# Define notification event for thread completion
list_button_motion_lists = []
list_button_motion_states = []
for keys in dict_device:
    dict_device_motion[keys] = wx.NewId()
    list_button_motion_lists.append(dict_device_motion[keys])
    list_button_motion_states.append(wx.NewId())



def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)


def EVT_STATE(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_STATE_ID, func)


def EVT_MOTION_STATE(win, func, motionID):
    """Define Motion State Event."""
    win.Connect(-1, -1, dict_motions_pairs[motionID], func)


class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data


class StateEvent(wx.PyEvent):
    """Simple event to carry state  data of a button."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_STATE_ID)
        self.data = data


class MotionStateEvent(wx.PyEvent):
    """Simple event to carry state  data of a Motion button."""
    def __init__(self, Motion_ID, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(dict_motions_pairs[Motion_ID])
        self.data = data


class ButtonFrame(wx.Frame):

    def __init__(self, data):
        wx.Frame.__init__(self, data)
        self.button.SetLabel(data)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)

    def OnClick(self, event):

        if self.button.GetLabel() == "ON":
            self.button.SetLabel("OFF")
        else:
            self.button.SetLabel("ON")

    def autoClick(self, value):

        self.button.SetLabel(value)


# GUI Frame class that spins off the worker thread
class MainFrame(wx.Frame):
    """Class MainFrame."""
    def __init__(self, parent, id):
        """Create the MainFrame."""
        wx.Frame.__init__(self, parent, id, 'Thread Test')
        self.states = []
        # Dumb sample frame with two buttons
        i = 0
        self.dict_motions_index = {}
        for keys in dict_device:
            pos_x = dict_device[keys][0] * 0.65
            pos_y = dict_device[keys][1] / 2
            wx.Button(self, list_button_motion_lists[i], str(keys), pos=(pos_x, pos_y), size=(50, 20))
            self.states.append(wx.Button(self, list_button_motion_states[i], 'START'
                                         , pos=(pos_x + 50, pos_y), size=(50, 20)))
            self.dict_motions_index[keys] = i
            # wx.Button(self, list_button_motion_states[i], 'START', pos=(100 * (i % 12), 50+int(i / 12) * 100))
            # dict_motions_pairs[list_button_motion_lists[i]] = list_button_motion_states[i]
            i = i + 1

        wx.Button(self, ID_START, 'Start', pos=(0, 300))
        wx.Button(self, ID_STOP, 'Stop', pos=(0, 400))
        wx.Button(self, ID_BUTTON, 'Initial', pos=(0, 500))


    def OnStart(self, event):
        """Start Computation."""
        # Trigger the worker thread unless it's already busy
        if not self.worker:
            self.status.SetLabel('Starting computation')
            self.worker = WorkerThread(self)

    def OnStop(self, event):
        """Stop Computation."""
        # Flag the worker thread to stop if running
        if self.worker:
            self.status.SetLabel('Trying to abort computation')
            self.worker.abort()

    def OnResult(self, event):
        """Show Result status."""
        if event.data is None:
            # Thread aborted (using our convention of None return)
            self.status.SetLabel('Computation aborted')
        else:
            # Process results here
            self.status.SetLabel('Computation Result: %s' % event.data)
        # In either event, the worker is done
        self.worker = None

    def OnState(self, event):
        """Show State status."""
        if event.data is "ON":
            # Thread aborted (using our convention of None return)
            self.status.SetLabel('ON')
        else:
            # Process results here
            self.status.SetLabel('OFF')
        # In either event, the worker is done
        self.worker = None

    def OnMotion(self, event):

        # dict_motions_pairs[botton_id]
        self.states[self.dict_motions_index[event.data[0]]].SetLabel(event.data[1])
        self.worker = None


class MainApp(wx.App):
    """Class Main App."""
    def OnInit(self):
        """Init Main App."""
        self.frame = MainFrame(None, -1)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True


if __name__ == '__main__':

    app = MainApp(0)
    app.MainLoop()

