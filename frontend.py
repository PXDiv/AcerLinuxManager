import tkinter as tk
from tkinter import messagebox, ttk
import os
import json
import elevate
import DriverManager
import HardwareStatus

# Config file path
CONFIG_FILE = "fan_config.json"

# Default speed values (multiples of 128)
minSpeedValue = 640
maxSpeedValue = 2560

tempCPUValue = minSpeedValue
tempGPUValue = minSpeedValue

svAllFanSliderValue = minSpeedValue
svCPUFanSliderValue = minSpeedValue
svGPUFanSliderValue = minSpeedValue

currentCPUTemp = 40
currentGPUTemp = 40


def save_settings():
    """Save the current settings to a JSON file."""
    settings = {
        "minSpeedValue": minSpeedValue,
        "maxSpeedValue": maxSpeedValue,
        "tempCPUValue": tempCPUValue,
        "tempGPUValue": tempGPUValue,
        
        "mixedFanSlider": mixedFanSlider.get(),
        "cpuFanSlider": cpuFanSlider.get(),
        "gpuFanSlider": gpuFanSlider.get(),
        "loadDriverOnStart" : _loadDriversOnStart.get()
    }
    with open(CONFIG_FILE, "w") as file:
        json.dump(settings, file)
    print("Settings saved!")

def load_settings_values():
    """Load settings from a JSON file and apply them."""
    global minSpeedValue, maxSpeedValue, tempCPUValue, tempGPUValue, _loadDriversOnStart

    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            settings = json.load(file)
            minSpeedValue = int(settings.get("minSpeedValue", minSpeedValue))
            maxSpeedValue = int(settings.get("maxSpeedValue", maxSpeedValue))
            tempCPUValue = int(settings.get("tempCPUValue", tempCPUValue))
            tempGPUValue = int(settings.get("tempGPUValue", tempGPUValue))
            _loadDriversOnStart.set(bool(settings.get("loadDriverOnStart", False)))
            print("Values loaded!")
    
def setVisualValuesFromSave():
        global minSpeedValue, maxSpeedValue, tempCPUValue, tempGPUValue
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                settings = json.load(file)
                mixedFanSlider.set(settings.get("mixedFanSlider", minSpeedValue))
                cpuFanSlider.set(settings.get("cpuFanSlider", minSpeedValue))
                gpuFanSlider.set(settings.get("gpuFanSlider", minSpeedValue))
                
                minFanSpeedInput.delete(0, tk.END)
                minFanSpeedInput.insert(0, str(minSpeedValue))

                maxFanSpeedInput.delete(0, tk.END)
                maxFanSpeedInput.insert(0, str(maxSpeedValue))
                
                if _loadDriversOnStart.get() == True:
                    loadDriversOnStartCheckbutton.select()
                
                print("Values Set!")
                

def UpdateSpeedPercentage():
    cpuFanSpeedPercentageLabel.config(text=f"CPU Fan: {(tempCPUValue/maxSpeedValue)*100:.1f}%")
    gpuFanSpeedPercentageLabel.config(text=f"GPU Fan: {(tempGPUValue/maxSpeedValue)*100:.1f}%")

def SetFanSpeed(fanNo, fanSpeed):
    if 0 < int(fanNo) < 3:
        print(f"Set Fan {fanNo} Speed to: {fanSpeed}")
        os.system(f"sudo echo {fanSpeed} | tee /dev/fan{fanNo}")
    else:
        print("Invalid Fan No. Must be 1 or 2.")

def SetTempCPUValue(val):
    """Set CPU fan speed without affecting Mixed slider."""
    global tempCPUValue
    tempCPUValue = int(val)

def SetTempGPUValue(val):
    """Set GPU fan speed without affecting Mixed slider."""
    global tempGPUValue
    tempGPUValue = int(val)

def SetTempMixedValue(val):
    """When mixed slider is moved, update temp values but do not apply immediately."""
    global tempCPUValue, tempGPUValue
    tempCPUValue = int(val)
    tempGPUValue = int(val)

def ApplyMixedChanges():
    """Apply mixed mode fan speed settings and sync separate sliders."""
    global tempCPUValue, tempGPUValue
    SetFanSpeed(1, tempCPUValue)
    SetFanSpeed(2, tempGPUValue)
    
    # Sync separate sliders when mixed is applied
    cpuFanSlider.set(tempCPUValue)
    gpuFanSlider.set(tempGPUValue)

    UpdateSpeedPercentage()
    save_settings()
    print("Applied Mixed Fan Speed Changes.")

def ApplySeparateChanges():
    """Apply separate CPU/GPU fan speeds without syncing the mixed slider."""
    global tempCPUValue, tempGPUValue
    SetFanSpeed(1, tempCPUValue)
    SetFanSpeed(2, tempGPUValue)

    UpdateSpeedPercentage()
    save_settings()
    print("Applied Separate Fan Speed Changes.")
    
def SetLoadOnStart():
    global _loadDriversOnStart
    print (_loadDriversOnStart.get())
    save_settings()
    

def ValidateAndApplyFanSpeed():
    """Validate min/max fan speed input and apply changes."""
    global minSpeedValue, maxSpeedValue

    try:
        minVal = int(minFanSpeedInput.get())
        maxVal = int(maxFanSpeedInput.get())

        if minVal % 128 != 0 or maxVal % 128 != 0:
            messagebox.showerror("Invalid Input", "Values must be multiples of 128.")
            minSpeedValue = 640; maxSpeedValue = 2560
            minFanSpeedInput
            
            # Reset input fields
            minFanSpeedInput.delete(0, tk.END)
            minFanSpeedInput.insert(0, str(minSpeedValue))

            maxFanSpeedInput.delete(0, tk.END)
            maxFanSpeedInput.insert(0, str(maxSpeedValue))
            return

        if minVal >= maxVal:
            messagebox.showerror("Invalid Input", "Min speed must be less than max speed.")
            
            # Reset input fields

            minSpeedValue = 640; maxSpeedValue = 2560
            minFanSpeedInput.delete(0, tk.END)
            minFanSpeedInput.insert(0, str(minSpeedValue))

            maxFanSpeedInput.delete(0, tk.END)
            maxFanSpeedInput.insert(0, str(maxSpeedValue))
            return

        minSpeedValue = minVal
        maxSpeedValue = maxVal

        # Update sliders
        mixedFanSlider.config(from_=minSpeedValue, to=maxSpeedValue)
        cpuFanSlider.config(from_=minSpeedValue, to=maxSpeedValue)
        gpuFanSlider.config(from_=minSpeedValue, to=maxSpeedValue)

        messagebox.showinfo("Success", f"Fan speed range updated: {minSpeedValue} - {maxSpeedValue}")

        save_settings()

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers.")
        # Reset input fields
        minSpeedValue = 640; maxSpeedValue = 2560
        minFanSpeedInput.delete(0, tk.END)
        minFanSpeedInput.insert(0, str(minSpeedValue))

        maxFanSpeedInput.delete(0, tk.END)
        maxFanSpeedInput.insert(0, str(maxSpeedValue))

def InstallDrivers():
    DriverManager.main()
    
def UnloadDrivers():
    DriverManager.remove_module()

def CleanCompiledDrivers():
    DriverManager.remove_compiled_drivers()

def check_root():
    if os.getuid() == 0:
        print("Acquired Root Privileges")
    else:
        messagebox.showerror(message="Root Privilages not aquired, Run the app with sudo")
        
def update_info():
    """Update temperature and fan speed labels."""
    global currentCPUTemp, currentGPUTemp
    currentCPUTemp = HardwareStatus.get_cpu_temp()
    currentGPUTemp = HardwareStatus.get_gpu_temp()
    
    
    cpuTempLabel.config(text=f"CPU Temp: {HardwareStatus.get_cpu_temp()}°C | Fan Speed: {HardwareStatus.get_cpu_fan_speed()} RPM")
    gpuTempLabel.config(text=f"GPU Temp: {HardwareStatus.get_gpu_temp()}°C | Fan Speed: {HardwareStatus.get_gpu_fan_speed()} RPM")
    # fanSpeedLabel.config(text=f"Fan Speeds: {HardwareStatus.get_fan_speed()} RPM")

    root.after(1000, update_info)  # Refresh every second

elevate.elevate(graphical=False)
check_root()

## Create the main window
root = tk.Tk()
_loadDriversOnStart = tk.BooleanVar()
root.title("Acer WMI Control")
root.geometry("1200x1000")

load_settings_values()

# Top Info 
topLabel = ttk.Label(root, text="Acer Linux Manager", font=("bold", 16))
topLabel.pack(pady=20)

infoFrame = tk.Frame(root)
cpuTempLabel = ttk.Label(infoFrame, text="CPU Temp")
gpuTempLabel = ttk.Label(infoFrame, text="GPU Temp")

cpuFanSpeedPercentageLabel = ttk.Label(infoFrame, text="Configure and set the correct min and max fan speed range (Multiples of 128)")
cpuFanSpeedPercentageLabel.grid(row=3)

gpuFanSpeedPercentageLabel = ttk.Label(infoFrame, text="Incorrect values may set the fan speed to 0 and cause damage")
gpuFanSpeedPercentageLabel.grid(row=4)


cpuTempLabel.grid(row=1)
gpuTempLabel.grid(row=2)
infoFrame.pack(pady=(0,20))

notebook = ttk.Notebook(root)

## Mixed Control Tab
mixedControlFrame = tk.Frame(notebook)
seperateControlFrame = tk.Frame(notebook)
advancedControlFrame = tk.Frame(notebook)

notebook.add(mixedControlFrame, text=" Mixed Fan Control ")
notebook.add(seperateControlFrame, text=" Seperate Fan Control ")
notebook.add(advancedControlFrame, text=" Advanced Controls ")
notebook.pack(expand=True, fill="both")

allFanLabel = ttk.Label(mixedControlFrame, text="All Fans Speed: ")
allFanLabel.pack(pady=(50,0))

mixedFanSlider = tk.Scale(mixedControlFrame, from_=minSpeedValue, to=maxSpeedValue, orient="horizontal",
    length=400, width=40, command=SetTempMixedValue, resolution=128)
mixedFanSlider.pack()

applyMixedButton = ttk.Button(mixedControlFrame, text="Apply Changes", command=ApplyMixedChanges, width=25)
applyMixedButton.pack(pady=80)

## Seperate Control Tab
cpuFanLabel = ttk.Label(seperateControlFrame, text="CPU Fan Speed: ")
cpuFanLabel.pack(pady=(50,0))

cpuFanSlider = tk.Scale(seperateControlFrame, from_=minSpeedValue, to=maxSpeedValue, orient="horizontal",
    length=400, width=40, command=SetTempCPUValue, resolution=128)
cpuFanSlider.pack()

gpuFanLabel = ttk.Label(seperateControlFrame, text="GPU Fan Speed: ")
gpuFanLabel.pack(pady=(40,0))

gpuFanSlider = tk.Scale(seperateControlFrame, from_=minSpeedValue, to=maxSpeedValue, orient="horizontal",
    length=400, width=40, command=SetTempGPUValue, resolution=128)
gpuFanSlider.pack()

applySeparateButton = ttk.Button(seperateControlFrame, text="Apply Changes", command=ApplySeparateChanges,width=25)
applySeparateButton.pack(pady=(80,0))

## Advanced Tab
# Fan Speed Controls Frame
fanSpeedFrame = ttk.Frame(advancedControlFrame, borderwidth=3, relief="groove")
fanSpeedFrame.pack(pady=50)

# Center the Fan Speed Label
fanSpeedLabel = ttk.Label(fanSpeedFrame, text="Fan Speed Range Values: ")
fanSpeedLabel.pack(pady=20)  # Using pack() centers it automatically

# Use a subframe for min/max fan speed controls
fanSpeedInputsFrame = ttk.Frame(fanSpeedFrame)
fanSpeedInputsFrame.pack(pady=10)  # Keeps them grouped together

# Minimum Fan Speed Control
minFanLabel = ttk.Label(fanSpeedInputsFrame, text="Minimum: ")
minFanLabel.grid(row=0, column=0, padx=20, pady=5, sticky="w")

minFanSpeedInput = ttk.Entry(fanSpeedInputsFrame)
minFanSpeedInput.insert(0, minSpeedValue)
minFanSpeedInput.grid(row=1, column=0, padx=20, pady=5, sticky="s")

# Maximum Fan Speed Control
maxFanLabel = ttk.Label(fanSpeedInputsFrame, text="Maximum: ")
maxFanLabel.grid(row=0, column=1, padx=20, pady=5, sticky="w")

maxFanSpeedInput = ttk.Entry(fanSpeedInputsFrame)
maxFanSpeedInput.insert(0, maxSpeedValue)
maxFanSpeedInput.grid(row=1, column=1, padx=20, pady=5, sticky="w")

# Center the Apply Button
applySpeedRangeButton = ttk.Button(fanSpeedFrame, text=" Apply Speed Range ", command=ValidateAndApplyFanSpeed)
applySpeedRangeButton.pack(pady=20)  # Using pack() centers it automatically


# Load Drivers on Start
loadDriversOnStartCheckbutton = tk.Checkbutton(advancedControlFrame,text="Load Driver on Start", command=SetLoadOnStart, variable=_loadDriversOnStart   )
loadDriversOnStartCheckbutton.pack()

# Create a frame to hold the buttons in a row
buttonFrame = ttk.Frame(advancedControlFrame)
buttonFrame.pack(pady=10)  # Pack it normally in the main frame

# Add buttons inside buttonFrame using pack with side="left"
installDriversButton = ttk.Button(buttonFrame, text="Configure Drivers", command=InstallDrivers)
installDriversButton.pack(side="left", padx=10)

unloadDriversButton = ttk.Button(buttonFrame, text="Unload Drivers", command=UnloadDrivers)
unloadDriversButton.pack(side="left", padx=10)

cleanCompiledDriversButton = ttk.Button(buttonFrame, text="Remove Already Compiled Drivers", command=CleanCompiledDrivers)
cleanCompiledDriversButton.pack(side="left", padx=10)

setVisualValuesFromSave()

if _loadDriversOnStart.get() == True:
    DriverManager.load_driver()

update_info()
root.mainloop()