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

# Temp CPU and GPU speed Values
tCPUValue = minSpeedValue
tGPUValue = minSpeedValue

svAllFanSliderValue = minSpeedValue
svCPUFanSliderValue = minSpeedValue
svGPUFanSliderValue = minSpeedValue

currentCPUTemp = 40
currentGPUTemp = 40

dynamicModeRefreshTime = 5

###
###                                         Loading and Saving Functions:
###

def save_settings():
    """Save the current settings to a JSON file."""
    settings = {
        "minSpeedValue": minSpeedValue,
        "maxSpeedValue": maxSpeedValue,
        "tempCPUValue": tCPUValue,
        "tempGPUValue": tGPUValue,
        
        "mixedFanSlider": mixedFanSlider.get(),
        "cpuFanSlider": cpuFanSlider.get(),
        "gpuFanSlider": gpuFanSlider.get(),
        "loadDriverOnStart" : _loadDriversOnStart.get(),
        
        # AutoFanSpeedsValuesSave
        "step1FanSpeed" : stepOneSlider.get(),
        "step1Temperature" : stepOneTempInput.get(),
        
        "step2FanSpeed" : stepTwoSlider.get(),
        "step2Temperature" : stepTwoTempInput.get(),
        
        "step3FanSpeed" : stepThreeSlider.get(),
        "step3Temperature" : stepThreeTempInput.get(),
        
        "step4FanSpeed" : stepFourSlider.get(),
        "step4Temperature" : stepFourTempInput.get(),
        
        "step5FanSpeed" : stepFiveSlider.get(),
        "step5Temperature" : stepFiveTempInput.get(),
        
        "step6FanSpeed" : stepSixSlider.get(),
        "step6Temperature" : stepSixTempInput.get()
    }
    with open(CONFIG_FILE, "w") as file:
        json.dump(settings, file)
    print("Settings saved!")

def load_settings_values():
    """Load settings from a JSON file and apply them."""
    global minSpeedValue, maxSpeedValue, tCPUValue, tGPUValue, _loadDriversOnStart

    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            settings = json.load(file)
            minSpeedValue = int(settings.get("minSpeedValue", minSpeedValue))
            maxSpeedValue = int(settings.get("maxSpeedValue", maxSpeedValue))
            tCPUValue = int(settings.get("tempCPUValue", tCPUValue))
            tGPUValue = int(settings.get("tempGPUValue", tGPUValue))
            _loadDriversOnStart.set(bool(settings.get("loadDriverOnStart", False)))
            print("Values loaded!")
    
def setVisualValuesFromSave():
        global minSpeedValue, maxSpeedValue, tCPUValue, tGPUValue
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
                
                # AutoTempLoadVisuals
                stepOneTempInput.insert(0, str(settings.get("step1Temperature")))
                stepOneSlider.set(settings.get("step1FanSpeed", minSpeedValue))
                
                stepTwoTempInput.insert(0, str(settings.get("step2Temperature")))
                stepTwoSlider.set(settings.get("step2FanSpeed", minSpeedValue))
                
                stepThreeTempInput.insert(0, str(settings.get("step3Temperature")))
                stepThreeSlider.set(settings.get("step3FanSpeed", minSpeedValue))
                
                stepFourTempInput.insert(0, str(settings.get("step4Temperature")))
                stepFourSlider.set(settings.get("step4FanSpeed" , minSpeedValue))
                
                stepFiveTempInput.insert(0, str(settings.get("step5Temperature")))
                stepFiveSlider.set(settings.get("step5FanSpeed", minSpeedValue))
                
                stepSixTempInput.insert(0, str(settings.get("step6Temperature")))
                stepSixSlider.set(settings.get("step6FanSpeed", minSpeedValue))
                
                if _loadDriversOnStart.get() == True:
                    loadDriversOnStartCheckbutton.select()
                
                print("Values Set!")
                


         
###
###                                                 Fan Speed Functions
###

def SetFanSpeed(fanNo, fanSpeed):
    if 0 < int(fanNo) < 3:
        print(f"Set Fan {fanNo} Speed to: {fanSpeed}")
        os.system(f"sudo echo {fanSpeed} | tee /dev/fan{fanNo}")
    else:
        print("Invalid Fan No. Must be 1 or 2.")

def SetTempCPUValue(val):
    """Set CPU fan speed without affecting Mixed slider."""
    global tCPUValue
    tCPUValue = int(val)

def SetTempGPUValue(val):
    """Set GPU fan speed without affecting Mixed slider."""
    global tGPUValue
    tGPUValue = int(val)

def SetTempMixedValue(val):
    """When mixed slider is moved, update temp values but do not apply immediately."""
    global tCPUValue, tGPUValue
    tCPUValue = int(val)
    tGPUValue = int(val)

def ApplyMixedChanges():
    """Apply mixed mode fan speed settings and sync separate sliders."""
    global tCPUValue, tGPUValue
    SetFanSpeed(1, tCPUValue)
    SetFanSpeed(2, tGPUValue)
    
    # Sync separate sliders when mixed is applied
    cpuFanSlider.set(tCPUValue)
    gpuFanSlider.set(tGPUValue)

    dynamic_speed_set.set(False)
    save_settings()
    print("Applied Mixed Fan Speed Changes.")

def ApplySeparateChanges():
    """Apply separate CPU/GPU fan speeds without syncing the mixed slider."""
    global tCPUValue, tGPUValue
    SetFanSpeed(1, tCPUValue)
    SetFanSpeed(2, tGPUValue)

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
    
# Boolean variable to enable/disable dynamic fan control
dynamic_speed_set = False

lastfanspeed = [minSpeedValue,minSpeedValue]

def dynamicFanSpeedSet():
    if not dynamic_speed_set.get():  # Check if dynamic speed control is enabled
        print("Dynamic Mode Not Enabled")
        return

    global lastfanspeed
    # Get current CPU and GPU temperatures
    cpu_temp = currentCPUTemp  # Assuming this is updated elsewhere in your code
    gpu_temp = currentGPUTemp  # Assuming this is updated elsewhere in your code

    # List of temperature input fields and corresponding sliders for CPU
    cpu_steps = [
        (stepOneTempInput, stepOneSlider),
        (stepTwoTempInput, stepTwoSlider),
        (stepThreeTempInput, stepThreeSlider),
        (stepFourTempInput, stepFourSlider),
        (stepFiveTempInput, stepFiveSlider),
        (stepSixTempInput, stepSixSlider),
    ]

    # List of temperature input fields and corresponding sliders for GPU
    gpu_steps = [
        (stepOneTempInput, stepOneSlider),  # Can be different sliders if needed
        (stepTwoTempInput, stepTwoSlider),
        (stepThreeTempInput, stepThreeSlider),
        (stepFourTempInput, stepFourSlider),
        (stepFiveTempInput, stepFiveSlider),
        (stepSixTempInput, stepFiveSlider)
    ]

    # Function to determine fan speed based on temperature thresholds
    def get_fan_speed(temp, steps):
        for temp_input, slider in reversed(steps):  # Check highest valid speed first
            try:
                step_temp = int(temp_input.get())  # Convert input to integer
                if temp >= step_temp:  # If current temp exceeds threshold
                    return slider.get()  # Return fan speed from slider
            except ValueError:
                continue  # Ignore invalid inputs
        return minSpeedValue  # Default to minimum speed if no match found

    # Set CPU and GPU fan speeds variables
    cpu_fan_speed = get_fan_speed(cpu_temp, cpu_steps)
    gpu_fan_speed = get_fan_speed(gpu_temp, gpu_steps)

    # Apply fan speeds using SetFanSpeed(FanNo, FanSpeed)
    if lastfanspeed[0] != cpu_fan_speed:
        SetFanSpeed(1, cpu_fan_speed)  # Fan No. 1 = CPU Fan
        lastfanspeed[0] = cpu_fan_speed
        
    if lastfanspeed[1] != gpu_fan_speed:
        SetFanSpeed(2, gpu_fan_speed)  # Fan No. 2 = GPU Fan
        lastfanspeed[1] = gpu_fan_speed

    # Schedule next execution if dynamic control is enabled
    if dynamic_speed_set.get():
        root.after(dynamicModeRefreshTime * 1000, dynamicFanSpeedSet)  # Run every 2 seconds

# Function to toggle dynamic fan speed setting
def toggleDynamicFanSpeed():
    if dynamic_speed_set.get():
        dynamicFanSpeedSet()  # Start function if enabled

def dynamicSpeedControlApply():
    save_settings()
    dynamicFanSpeedSet()

elevate.elevate(graphical=False)
check_root()

## Create the main window
root = tk.Tk()
_loadDriversOnStart = tk.BooleanVar()
root.title("Acer WMI Control")
root.geometry("1500x1000")

load_settings_values()

# Top Info 
topLabel = ttk.Label(root, text="Acer Linux Manager", font=("bold", 16))
topLabel.pack(pady=20)

infoFrame = tk.Frame(root)
cpuTempLabel = ttk.Label(infoFrame, text="CPU Temp")
gpuTempLabel = ttk.Label(infoFrame, text="GPU Temp")

# cpuFanSpeedPercentageLabel = ttk.Label(infoFrame, text="Configure and set the correct min and max fan speed range (Multiples of 128)")
# cpuFanSpeedPercentageLabel.grid(row=3)

# gpuFanSpeedPercentageLabel = ttk.Label(infoFrame, text="Incorrect values may set the fan speed to 0 and cause damage")
# gpuFanSpeedPercentageLabel.grid(row=4)


cpuTempLabel.grid(row=1)
gpuTempLabel.grid(row=2)
infoFrame.pack(pady=(0,20))

notebook = ttk.Notebook(root)
dynamicControlFrame = tk.Frame(notebook)
manualControlFrame = tk.Frame(notebook)
advancedControlFrame = tk.Frame(notebook)
notebook.add(dynamicControlFrame, text=" Dynamic Fan Control ")
# notebook.add(mixedControlFrame, text=" Mixed Fan Control ")
notebook.add(manualControlFrame, text=" Manual Fan Control ")
notebook.add(advancedControlFrame, text=" Advanced Controls ")
notebook.pack(expand=True, fill="both")

dynamic_speed_set = tk.BooleanVar(value=True)  # Default is False
dynamic_speed_checkbox = ttk.Checkbutton(dynamicControlFrame, text="Enable Dynamic Fan Speed", variable=dynamic_speed_set, command=toggleDynamicFanSpeed)
dynamic_speed_checkbox.pack(pady=10)

## Dynamic Control Tab

SlidersFrame = ttk.Frame(dynamicControlFrame)

# Step One Settings
frame1 = ttk.Frame(SlidersFrame)
label = ttk.Label(frame1, text="At Tempreature:")
label.pack()
stepOneTempInput = ttk.Entry(frame1, width=5)
stepOneTempInput.pack()
label = ttk.Label(frame1, text="Set Fan Speed:")
label.pack()
stepOneSlider = tk.Scale(frame1, resolution=128,from_=maxSpeedValue, to=minSpeedValue, length=200)
stepOneSlider.pack()
frame1.grid(column=0, row=0,padx=10)

# Step Two Settings
frame2 = ttk.Frame(SlidersFrame)
label = ttk.Label(frame2, text="At Tempreature:")
label.pack()
stepTwoTempInput = ttk.Entry(frame2, width=5)
stepTwoTempInput.pack()
label = ttk.Label(frame2, text="Set Fan Speed:")
label.pack()
stepTwoSlider = tk.Scale(frame2, resolution=128,from_=maxSpeedValue, to=minSpeedValue, length=200)
stepTwoSlider.pack()
frame2.grid(column=1, row=0,padx=10)

# Step Three Settings
frame3 = ttk.Frame(SlidersFrame)
label = ttk.Label(frame3, text="At Tempreature:")
label.pack()
stepThreeTempInput = ttk.Entry(frame3, width=5)
stepThreeTempInput.pack()
label = ttk.Label(frame3, text="Set Fan Speed:")
label.pack()
stepThreeSlider = tk.Scale(frame3, resolution=128,from_=maxSpeedValue, to=minSpeedValue, length=200)
stepThreeSlider.pack()
frame3.grid(column=2, row=0,padx=10)

# Step Four Settings
frame4 = ttk.Frame(SlidersFrame)
label = ttk.Label(frame4, text="At Tempreature:")
label.pack()
stepFourTempInput = ttk.Entry(frame4, width=5)
stepFourTempInput.pack()
label = ttk.Label(frame4, text="Set Fan Speed:")
label.pack()
stepFourSlider = tk.Scale(frame4, resolution=128,from_=maxSpeedValue, to=minSpeedValue, length=200)
stepFourSlider.pack()
frame4.grid(column=3, row=0,padx=10)

# Step Five Settings
frame5 = ttk.Frame(SlidersFrame)
label = ttk.Label(frame5, text="At Tempreature:")
label.pack()
stepFiveTempInput = ttk.Entry(frame5, width=5)
stepFiveTempInput.pack()
label = ttk.Label(frame5, text="Set Fan Speed:")
label.pack()
stepFiveSlider = tk.Scale(frame5, resolution=128,from_=maxSpeedValue, to=minSpeedValue, length=200)
stepFiveSlider.pack()
frame5.grid(column=4, row=0,padx=10)

frame6 = ttk.Frame(SlidersFrame)
label = ttk.Label(frame6, text="At Tempreature:")
label.pack()
stepSixTempInput = ttk.Entry(frame6, width=5)
stepSixTempInput.pack()
label = ttk.Label(frame6, text="Set Fan Speed:")
label.pack()
stepSixSlider = tk.Scale(frame6, resolution=128,from_=maxSpeedValue, to=minSpeedValue, length=200)
stepSixSlider.pack()
frame6.grid(column=5, row=0,padx=10)

SlidersFrame.pack(pady=40)

applyAutoButton = ttk.Button(dynamicControlFrame, text="Apply", command=dynamicSpeedControlApply)
applyAutoButton.pack(pady=20)

## Manual Control Tab

#Mixed Control
mixedControlFrame = tk.Frame(manualControlFrame)
allFanLabel = ttk.Label(mixedControlFrame, text="All Fans Speed: ")
allFanLabel.pack(pady=(50,0))

mixedFanSlider = tk.Scale(mixedControlFrame, from_=minSpeedValue, to=maxSpeedValue, orient="horizontal",
    length=400, width=40, command=SetTempMixedValue, resolution=128)
mixedFanSlider.pack()

mixedControlFrame.pack()

#Seperate Controls
seperateControlSliderFrame = ttk.Frame(manualControlFrame, borderwidth=3, relief="groove")

cpuFanLabel = ttk.Label(seperateControlSliderFrame, text="CPU Fan Speed: ")
cpuFanLabel.grid(column=0, row=0, padx= 20, pady=(40,0))

cpuFanSlider = tk.Scale(seperateControlSliderFrame, from_=minSpeedValue, to=maxSpeedValue, orient="horizontal",
    length=400, width=40, command=SetTempCPUValue, resolution=128)
cpuFanSlider.grid(column=0, row=1, padx=20, pady=(0, 40))

gpuFanLabel = ttk.Label(seperateControlSliderFrame, text="GPU Fan Speed: ")
gpuFanLabel.grid(column=1, row=0, padx=20, pady=(40, 0))

gpuFanSlider = tk.Scale(seperateControlSliderFrame, from_=minSpeedValue, to=maxSpeedValue, orient="horizontal",
    length=400, width=40, command=SetTempGPUValue, resolution=128)
gpuFanSlider.grid(column=1, row=1, padx=20, pady=(0, 40))

seperateControlSliderFrame.pack(pady=50)

applyMixedButton = ttk.Button(manualControlFrame, text="Apply Changes", command=ApplyMixedChanges, width=25)
applyMixedButton.pack()

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

dynamicFanSpeedSet()
update_info()
root.mainloop()