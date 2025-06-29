import sys
import subprocess
import platform

if platform.system() == 'Windows':
    # Hide the console window if running as an executable
    try:
        import win32gui
        import win32con
        hwnd = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
    except ImportError:
        pass

    # Store original Popen
    original_popen = subprocess.Popen

    # Create a subclass of Popen that hides the console window
    class NoConsolePopen(subprocess.Popen):
        def __init__(self, *args, **kwargs):
            if platform.system() == 'Windows':
                # Force creation flags to hide window
                if 'startupinfo' not in kwargs:
                    kwargs['startupinfo'] = subprocess.STARTUPINFO()
                    kwargs['startupinfo'].dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    kwargs['startupinfo'].wShowWindow = subprocess.SW_HIDE
                if 'creationflags' not in kwargs:
                    kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
            super().__init__(*args, **kwargs)

    # Replace the original Popen with our version
    subprocess.Popen = NoConsolePopen

    # Patch subprocess.run to use our NoConsolePopen
    original_run = subprocess.run
    def patched_run(*args, **kwargs):
        if platform.system() == 'Windows':
            if 'startupinfo' not in kwargs:
                kwargs['startupinfo'] = subprocess.STARTUPINFO()
                kwargs['startupinfo'].dwFlags |= subprocess.STARTF_USESHOWWINDOW
                kwargs['startupinfo'].wShowWindow = subprocess.SW_HIDE
            if 'creationflags' not in kwargs:
                kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
        return original_run(*args, **kwargs)
    
    subprocess.run = patched_run 