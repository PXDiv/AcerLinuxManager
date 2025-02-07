import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import elevate

DRIVER_DIR = "NitroDrivers"
MODULE_NAME = "acer_nitro_gaming_driver2.ko"
MODULE_PATH = os.path.join(DRIVER_DIR, MODULE_NAME)

def is_module_loaded():
    """Check if the module is currently loaded."""
    result = subprocess.run(["lsmod"], capture_output=True, text=True)
    return MODULE_NAME.split(".")[0] in result.stdout

def remove_module():
    """Remove the module if it is loaded."""
    messagebox.showinfo(message="Driver is already loaded. Removing it...")
    result = subprocess.run(["sudo", "rmmod", MODULE_NAME.split(".")[0]])
    if result.returncode == 0:
        print("Driver removed successfully.")
    else:
        print("Error: Failed to remove driver.")
        exit(1)

def remove_fan_control_files():
    """Remove fan control files if they exist."""
    for fan in ["/dev/fan1", "/dev/fan2"]:
        if os.path.exists(fan):
            print(f"Removing {fan}...")
            subprocess.run(["sudo", "rm", "-f", fan])

def compile_driver():
    """Compile the driver if not already compiled."""
    if not os.path.exists(MODULE_PATH):
        messagebox.showinfo(message="Driver not compiled. Running make...")
        try:
            process = subprocess.run("make", cwd=DRIVER_DIR, shell=True, check=True, capture_output=True, text=True)
            print(process.stdout)
            if process.stderr:
                messagebox.showerror(message =("Make Warnings/Errors:", process.stderr))
        except subprocess.CalledProcessError as e:
            messagebox.showerror(message ="Error: Make failed.")
            messagebox.showerror(message =("STDOUT:", e.stdout))
            messagebox.showerror(message =("STDERR:", e.stderr))
            exit(1)
        
        if not os.path.exists(MODULE_PATH):
            messagebox.showerror(message =f"Error: {MODULE_PATH} not found after make.")
            exit(1)
    else:
        messagebox.showinfo( message =f"Driver already compiled,\n Using the Compiled Driver")
        
def remove_compiled_drivers():
    """ Remove the Compiles."""
    if os.path.exists(MODULE_PATH):
        messagebox.showinfo(message="Found Driver already compiled. Running make clean...")
        try:
            process = subprocess.run("make clean", cwd=DRIVER_DIR, shell=True, check=True, capture_output=True, text=True)
            print(process.stdout)
            if process.stderr:
                messagebox.showerror(message =("Make Warnings/Errors:", process.stderr))
        except subprocess.CalledProcessError as e:
            messagebox.showerror(message ="Error: Make failed.")
            messagebox.showerror(message =("STDOUT:", e.stdout))
            messagebox.showerror(message =("STDERR:", e.stderr))
            exit(1)
        
        if not os.path.exists(MODULE_PATH):
            messagebox.showinfo( message =f"Complied Drivers have been Removed from the make directory, but not removed if they are running")
    else:
        messagebox.showerror( message =f"No Already compiled Drivers Found, The Make Folder is already clean")

def load_driver():
    """Load the compiled driver."""
    print("Loading driver...")
    if not os.path.exists(MODULE_PATH):
        messagebox.showerror(message="Drivers have not been Compiled, Please configure them from the advanced menu")
    
    result = subprocess.run(["sudo", "insmod", os.path.abspath(MODULE_PATH)])
    if result.returncode == 0:
        messagebox.showinfo(message ="Driver loaded successfully!")
    else:
        print("Error: Failed to load driver.")

def main():
    if is_module_loaded():
        remove_module()
    remove_fan_control_files()
    compile_driver()
    load_driver()
