def pre_find_module_path(hook_api):
    """
    This hook runs before the module is imported.
    It ensures the application starts without a console window on Windows.
    """
    import sys
    if sys.platform == 'win32':
        # This will be processed by PyInstaller to set the appropriate flags
        hook_api.add_runtime_option('--noconsole')
        hook_api.add_runtime_option('--windowed') 