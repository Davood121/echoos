import os
import subprocess
import glob

class SystemIntegrator:
    def __init__(self):
        self.apps = {}
        self.scan_apps()

    def scan_apps(self):
        """
        Scans /usr/share/applications for .desktop files to discover installed apps.
        """
        print("Scanning installed applications...")
        desktop_files = glob.glob("/usr/share/applications/*.desktop")
        for file_path in desktop_files:
            try:
                name = None
                exec_cmd = None
                with open(file_path, 'r', errors='ignore') as f:
                    for line in f:
                        if line.startswith("Name=") and not name:
                            name = line.strip().split("=")[1].lower()
                        if line.startswith("Exec=") and not exec_cmd:
                            exec_cmd = line.strip().split("=")[1].split()[0] # Take first part of command
                            # Remove %U, %F etc placeholders
                            exec_cmd = exec_cmd.replace("%U", "").replace("%F", "")
                
                if name and exec_cmd:
                    self.apps[name] = exec_cmd
            except Exception as e:
                continue
        print(f"Discovered {len(self.apps)} applications.")

    def get_app_command(self, app_name):
        """
        Returns the command to launch an app (fuzzy match).
        """
        app_name = app_name.lower()
        if app_name in self.apps:
            return self.apps[app_name]
        
        # Fuzzy search
        for name, cmd in self.apps.items():
            if app_name in name:
                return cmd
        return None

    def set_volume(self, level_percent):
        """
        Sets system volume (0-100).
        """
        try:
            # Using amixer (ALSA)
            cmd = f"amixer -D pulse sset Master {level_percent}%"
            subprocess.run(cmd, shell=True, check=True)
            return True
        except Exception as e:
            print(f"Error setting volume: {e}")
            return False

    def set_brightness(self, level_percent):
        """
        Sets screen brightness (requires brightnessctl).
        """
        try:
            cmd = f"brightnessctl set {level_percent}%"
            subprocess.run(cmd, shell=True, check=True)
            return True
        except Exception as e:
            print(f"Error setting brightness: {e}")
            return False

    def toggle_wifi(self, enable=True):
        """
        Toggles Wi-Fi on/off using nmcli.
        """
        state = "on" if enable else "off"
        try:
            cmd = f"nmcli radio wifi {state}"
            subprocess.run(cmd, shell=True, check=True)
            return True
        except Exception as e:
            print(f"Error toggling Wi-Fi: {e}")
            return False

if __name__ == "__main__":
    sys_int = SystemIntegrator()
    
    # Test App Discovery
    chrome_cmd = sys_int.get_app_command("firefox")
    if chrome_cmd:
        print(f"Found Firefox command: {chrome_cmd}")
    else:
        print("Firefox not found.")

    # Test Volume (Be careful running this!)
    # sys_int.set_volume(50)
