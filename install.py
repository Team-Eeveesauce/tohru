import win32service
import win32serviceutil
import win32event
import os
import subprocess
import time
import servicemanager

class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "Kanna"
    _svc_display_name_ = "Kanna - Tohru Companion"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        # Get the directory of the current service script
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the path to your external script
        external_script_path = os.path.join(current_dir, 'kanna.py')

        # Start the external script as a subprocess
        while True:
            servicemanager.LogInfoMsg("Starting external script...")
            subprocess.call(['python', external_script_path]) 
            servicemanager.LogInfoMsg("External script finished.")

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(MyService)
