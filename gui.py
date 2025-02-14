import tkinter as tk
from tkinter import messagebox, ttk
import json
import socket

SOCKET_FILE = "/tmp/fancontrol.sock"  # IPC socket path

# Function to communicate with the daemon
def send_command(command):
    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(SOCKET_FILE)
        client.send(json.dumps(command).encode())
        response = client.recv(1024).decode()
        client.close()
        return json.loads(response) if response else None
    except Exception as e:
        print("Failed to connect to daemon:", e)
        return None

# Apply Mixed Fan Speed
def apply_mixed_changes():
    send_command({"action": "set_fan", "fan": 1, "speed": mixedFanSlider.get()})
    send_command({"action": "set_fan", "fan": 2, "speed": mixedFanSlider.get()})

# Enable/Disable Dynamic Mode
def toggle_dynamic_mode():
    value = dynamicModeVar.get()
    send_command({"action": "enable_dynamic", "value": value})

# Update Temperature & Fan Speed
def update_info():
    data = send_command({"action": "get_status"})
    if data:
        cpuTempLabel.config(text=f"CPU Temp: {data['cpu_temp']}°C | Fan: {data['cpu_fan_speed']} RPM")
        gpuTempLabel.config(text=f"GPU Temp: {data['gpu_temp']}°C | Fan: {data['gpu_fan_speed']} RPM")
    root.after(1000, update_info)

# GUI Setup
root = tk.Tk()
root.title("Acer WMI Control")
root.geometry("800x600")

cpuTempLabel = ttk.Label(root, text="Loading CPU Temp...")
cpuTempLabel.pack()

gpuTempLabel = ttk.Label(root, text="Loading GPU Temp...")
gpuTempLabel.pack()

mixedFanSlider = tk.Scale(root, from_=640, to=2560, orient="horizontal")
mixedFanSlider.pack()

applyButton = ttk.Button(root, text="Apply Mixed Speed", command=apply_mixed_changes)
applyButton.pack()

dynamicModeVar = tk.BooleanVar()
dynamicModeCheck = tk.Checkbutton(root, text="Enable Dynamic Mode", variable=dynamicModeVar, command=toggle_dynamic_mode)
dynamicModeCheck.pack()

update_info()
root.mainloop()
