# Windows subprocess hook to hide console windows
import os
import sys
import subprocess
import ctypes

# Only apply on Windows
if sys.platform == 'win32':
    # Original subprocess.Popen
    original_popen = subprocess.Popen
    
    # Constants for CreateProcess flags
    CREATE_NO_WINDOW = 0x08000000
    
    # Subclass Popen to hide console windows
    class NoConsolePopen(subprocess.Popen):
        def __init__(self, *args, **kwargs):
            # Add CREATE_NO_WINDOW flag for all process creation
            if 'creationflags' in kwargs:
                kwargs['creationflags'] |= CREATE_NO_WINDOW
            else:
                kwargs['creationflags'] = CREATE_NO_WINDOW
                
            # Call original Popen
            super().__init__(*args, **kwargs)
    
    # Replace subprocess.Popen with our version
    subprocess.Popen = NoConsolePopen
    
    # For modules that use ctypes to create processes
    if hasattr(ctypes, 'windll') and hasattr(ctypes.windll, 'kernel32'):
        # Try to get the original CreateProcessW
        try:
            original_create_process = ctypes.windll.kernel32.CreateProcessW
            
            # TODO: If needed, hook CreateProcessW to force CREATE_NO_WINDOW flag
            # This is more complex and may not be necessary if subprocess.Popen patching works
        except AttributeError:
            pass
