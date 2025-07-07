import uuid
import requests
import sys
import json
import os
from datetime import datetime, timedelta

def get_machine_id():
    """Returns MAC address as integer"""
    return str(uuid.getnode())

def get_cache_file_path():
    """Get the path to the license cache file"""
    if getattr(sys, 'frozen', False):
        # Running in a bundle
        base_path = os.path.dirname(sys.executable)
    else:
        # Running in development
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, "license_cache.json")

def load_cached_license():
    """Load cached license data if it exists and is still valid"""
    cache_file = get_cache_file_path()
    
    if not os.path.exists(cache_file):
        return None
    
    try:
        with open(cache_file, 'r') as f:
            cache_data = json.load(f)
        
        # Check if cache is still valid (not older than 30 days)
        cached_time_str = cache_data.get('cached_time', '2000-01-01')
        cached_time = datetime.fromisoformat(cached_time_str)
        current_time = datetime.now()
        
        if current_time - cached_time < timedelta(days=30):
            return cache_data
        else:
            # Cache expired, remove it
            print(f"Cache expired (cached: {cached_time}, current: {current_time})")
            os.remove(cache_file)
            return None
    except Exception as e:
        # If there's any error reading cache, remove it and return None
        print(f"Error reading cache: {e}")
        try:
            os.remove(cache_file)
        except:
            pass
        return None

def save_license_cache(license_key, machine_id, api_url, server_response):
    """Save license validation to cache"""
    cache_file = get_cache_file_path()
    
    cache_data = {
        'license_key': license_key,
        'machine_id': machine_id,
        'api_url': api_url,
        'cached_time': datetime.now().isoformat(),
        'status': 'valid',
        'server_response': server_response  # Store the full server response
    }
    
    try:
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)
        return True
    except Exception:
        return False

def clear_license_cache():
    """Clear the license cache file"""
    cache_file = get_cache_file_path()
    try:
        if os.path.exists(cache_file):
            os.remove(cache_file)
            return True
    except Exception:
        pass
    return False

def prompt_license_key_gui(machine_id):
    """Show a GUI dialog for license key input"""
    try:
        import wx
        
        # Create a simple dialog
        app = wx.App()
        
        # Create the dialog - much larger size
        dialog = wx.Dialog(None, title="License Validation", size=(600, 450))
        dialog.SetBackgroundColour(wx.Colour(240, 240, 240))
        
        # Main sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Title
        title = wx.StaticText(dialog, label="RAG Assistant License")
        title_font = title.GetFont()
        title_font.SetPointSize(16)
        title_font.SetWeight(wx.FONTWEIGHT_BOLD)
        title.SetFont(title_font)
        main_sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER, 15)
        
        # Machine ID display
        machine_id_label = wx.StaticText(dialog, label="Your Machine ID:")
        machine_id_label.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        main_sizer.Add(machine_id_label, 0, wx.LEFT | wx.RIGHT | wx.TOP, 15)
        
        machine_id_text = wx.TextCtrl(dialog, value=machine_id, style=wx.TE_READONLY | wx.TE_CENTER)
        machine_id_text.SetBackgroundColour(wx.Colour(255, 255, 255))
        main_sizer.Add(machine_id_text, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        
        # Instructions
        instructions = wx.StaticText(dialog, label="Please send this Machine ID to the developer to request a license key.")
        instructions.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))
        main_sizer.Add(instructions, 0, wx.LEFT | wx.RIGHT | wx.TOP, 15)
        
        # License key input
        license_label = wx.StaticText(dialog, label="License Key:")
        license_label.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        main_sizer.Add(license_label, 0, wx.LEFT | wx.RIGHT | wx.TOP, 15)
        
        # License key input with scrollbar and larger size
        license_input = wx.TextCtrl(dialog, style=wx.TE_PASSWORD | wx.TE_MULTILINE | wx.TE_RICH2 | wx.TE_WORDWRAP, size=(-1, 120))
        license_input.SetFocus()
        main_sizer.Add(license_input, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        
        # Add a hint about the license key format
        hint_text = wx.StaticText(dialog, label="Tip: You can paste your license key here. Long keys will automatically wrap to multiple lines.")
        hint_text.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        hint_text.SetForegroundColour(wx.Colour(100, 100, 100))
        main_sizer.Add(hint_text, 0, wx.LEFT | wx.RIGHT | wx.TOP, 5)
        
        # Buttons
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        ok_button = wx.Button(dialog, wx.ID_OK, "Validate License", size=(120, 35))
        ok_button.SetDefault()
        cancel_button = wx.Button(dialog, wx.ID_CANCEL, "Cancel", size=(120, 35))
        
        button_sizer.Add(ok_button, 1, wx.RIGHT, 10)
        button_sizer.Add(cancel_button, 1, wx.LEFT, 10)
        
        main_sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALL, 20)
        
        dialog.SetSizer(main_sizer)
        dialog.Layout()
        
        # Center the dialog
        dialog.Center()
        
        # Show the dialog
        result = dialog.ShowModal()
        
        if result == wx.ID_OK:
            license_key = license_input.GetValue().strip()
            dialog.Destroy()
            app.Destroy()
            return license_key
        else:
            dialog.Destroy()
            app.Destroy()
            return None
            
    except ImportError:
        # Fallback to CLI if wx is not available
        print(f"\nYour Machine ID: {machine_id}")
        print("Please send this to the developer to request a license.\n")
        try:
            return input("Enter your license key: ").strip()
        except KeyboardInterrupt:
            print("\nAborted.")
            sys.exit(1)

def validate_license_with_server(license_key, machine_id, api_url):
    """Validate license with the server and return response"""
    payload = {
        "license_key": license_key,
        "machine_id": machine_id
    }
    
    try:
        resp = requests.post(api_url, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return True, data, None  # Success, response data, no error
    except requests.exceptions.RequestException as e:
        return False, None, str(e)  # Failed, no data, error message
    except Exception as e:
        return False, None, str(e)  # Failed, no data, error message

def check_license(api_url):
    """Main license validation function with all the requested logic"""
    machine_id = get_machine_id()
    
    # Step 1: Check if we have a valid cached license
    cached = load_cached_license()
    if cached and cached.get('machine_id') == machine_id:
        print("✅ Found cached license, validating with server...")
        
        # Step 2: Always contact the server to check for revocation
        server_success, server_data, server_error = validate_license_with_server(
            cached['license_key'], machine_id, api_url
        )
        
        if server_success:
            # Server is reachable
            if server_data.get("status") == "valid":
                print("✅ License validated with server - using cached license")
                # Update cache with fresh server response
                save_license_cache(cached['license_key'], machine_id, api_url, server_data)
                return True
            else:
                # License was revoked or invalidated
                print(f"❌ License invalidated by server: {server_data.get('reason', 'unknown')}")
                clear_license_cache()
                # Fall through to prompt for new license
        else:
            # Server is unreachable, but we have valid cache
            print(f"⚠️ Server unreachable ({server_error}), using cached license")
            return True  # Allow app to run with cached license
    
    # Step 3: No valid cache or license was revoked - prompt for new license
    print("🔑 License validation required")
    license_key = prompt_license_key_gui(machine_id)
    
    if not license_key:
        print("❌ No license key provided")
        return False
    
    # Step 4: Validate new license with server
    server_success, server_data, server_error = validate_license_with_server(
        license_key, machine_id, api_url
    )
    
    if server_success:
        if server_data.get("status") == "valid":
            print("✅ License valid. Welcome!")
            # Save to cache for 30 days
            save_license_cache(license_key, machine_id, api_url, server_data)
            return True
        else:
            print(f"❌ License invalid: {server_data.get('reason', 'unknown error')}")
            return False
    else:
        # Server is unreachable and no valid cache
        print(f"❌ Server unreachable ({server_error}) and no valid cached license")
        print("Please check your internet connection and try again.")
        return False

# Example usage:
if __name__ == "__main__":
    # Replace with your actual URL:
    API_URL = "https://demo.freshlook.hu/license-api/verify_license.php"
    if not check_license(API_URL):
        print("Exiting application.")
        sys.exit(1)
    # ... continue with your app ...
