# coding=utf-8
import time
from threading import *
import wx
import os


def get_all_data_dirs(data_dir_root):

    list_files_dir = []
    for dirpath, dirnames, filenames in os.walk(data_dir_root):
        for filepath in filenames:
            list_files_dir.append(os.path.join(dirpath, filepath))

    return list_files_dir


data_dir_root = "D:\\wsuk1\\data"
all_data_dirs = get_all_data_dirs(data_dir_root)
print(len(all_data_dirs))
dict_device_motion = {}
dict_device_temperate = {}


def data_deal(dir):

    with open(dir, 'r+') as f:

        for line in f:
            line = line.strip()
            list_state = line.split('\t')
            if len(list_state) < 3:
                continue
            event_time = list_state[0]
            event_device = list_state[1]
            event_state = list_state[2]
            if event_device[0] == 'M':
                if event_device in dict_device_motion:

                    pass
                else:
                    dict_device_motion[event_device] = "M"

                    pass
            elif event_device[0] == 'T':
                if event_device in dict_device_temperate:

                    pass
                else:
                    dict_device_temperate[event_device] = 'T'
            print(event_time, event_device, event_state)


    return


data_deal(all_data_dirs[5])
print (dict_device_motion)
print (dict_device_temperate)

for keys in dict_device_motion:
    keys = wx.NewId()

# Button definitions
ID_START = wx.NewId()
ID_STOP = wx.NewId()
ID_BUTTON = wx.NewId()

list_button_motion_lists = [wx.NewId() for keys in dict_device_motion]
list_button_motion_states = [wx.NewId() for keys in dict_device_motion]
list_button_temp_lists = [wx.NewId() for keys in dict_device_temperate]
# Define notification event for thread completion
EVT_RESULT_ID = wx.NewId()
EVT_STATE_ID = wx.NewId()

def get_state(num):

    if num % 2 == 0:
        return "ON"
    else:
        return "OFF"


def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)


def EVT_STATE(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_STATE_ID, func)


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


# Thread class that executes processing
class WorkerThread(Thread):
    """Worker Thread Class."""
    def __init__(self, notify_window):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this
        self.start()

    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread. Simulation of
        # a long process (well, 10s here) as a simple loop - you will
        # need to structure your processing so that you periodically
        # peek at the abort variable
        for i in range(10):
            time.sleep(0.11)
            wx.PostEvent(self._notify_window, StateEvent(get_state(i)))

            if self._want_abort:
                # Use a result of None to acknowledge the abort (of
                # course you can use whatever you'd like or even
                # a separate event type)
                wx.PostEvent(self._notify_window, ResultEvent(None))
                return
        # Here's where the result would be returned (this is an
        # example fixed result of the number 10, but it could be
        # any Python object)
        wx.PostEvent(self._notify_window, ResultEvent(10))

    def abort(self):
        """abort worker thread."""
        # Method for use by main thread to signal an abort
        self._want_abort = 1


# GUI Frame class that spins off the worker thread
class MainFrame(wx.Frame):
    """Class MainFrame."""
    def __init__(self, parent, id):
        """Create the MainFrame."""
        wx.Frame.__init__(self, parent, id, 'Thread Test')

        # Dumb sample frame with two buttons
        i = 0
        dict_motions_pairs = {}
        for keys in dict_device_motion:
            wx.Button(self, list_button_motion_lists[i], str(keys), pos=(100*(i%12), int(i/12) *100))
            wx.Button(self, list_button_motion_states[i], 'START', pos=(100 * (i % 12), 50+int(i / 12) * 100))
            dict_motions_pairs[list_button_motion_lists[i]] = list_button_motion_states[i]
            i = i + 1


        wx.Button(self, ID_START, 'Start', pos=(0, 350))
        wx.Button(self, ID_STOP, 'Stop', pos=(0, 400))
        wx.Button(self, ID_BUTTON, 'Initial', pos=(0, 500))
        self.status = wx.StaticText(self, -1, '', pos=(0, 600))

        self.Bind(wx.EVT_BUTTON, self.OnStart, id=ID_START)
        self.Bind(wx.EVT_BUTTON, self.OnStop, id=ID_STOP)
        self.Bind(wx.EVT_BUTTON, self.OnState, id=ID_BUTTON)

        for motions in dict_motions_pairs:
            self.Bind(wx.EVT_BUTTON, self.OnMotion, id=dict_motions_pairs[motions])
            # dict_motions_pairs[motions](self, self.OnState)

        # Set up event handler for any worker thread results
        EVT_RESULT(self, self.OnResult)
        EVT_STATE(self, self.OnState)

        # And indicate we don't have a worker thread yet
        self.worker = None

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
        return

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