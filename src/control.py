import os
import sys

import conf

import win32com.client as win32

class ole_recorder():
    def __init__(self):
        self.Rec = win32.gencache.EnsureDispatch('VisionRecorder.Application')
    
    def stop_recording(self):
        self.Rec.Acquisition.StopRecording()
        
    def stop_viewing(self):
        self.Rec.Acquisition.StopViewing()
    
    def load_workspace(self, workspace):
        self.Rec.CurrentWorkspace.Load(workspace)

    def start_viewing(self):
        self.Rec.Acquisition.ViewData()
        
    def start_recording(self, file):
        if file[-4:] != '.eeg':
            file += '.eeg'
        self.start_viewing()
        self.Rec.Acquisition.StartRecording(file)
        
    def stop_recording(self):
        self.Rec.Acquisition.StopRecording()
        
    def initialize_recorder(self, workspace):
        self.stop_recording()
        self.stop_viewing()
        self.load_workspace(workspace)
        self.start_viewing()

if __name__ == "__main__":
    
    workspace = os.path.join(conf.workspace_base, "simon_test.rwksp")
    
    rec = ole_recorder()
    
    input("press any ket to continue.")
    rec.initialize_recorder(workspace)
    
    input("press any key to continue.")
    rec.start_recording(os.path.join(conf.repository_base, "src", "test"))

    input("press any key to continue.")
    
    rec.stop_recording()
    input("press any key to continue.")
    