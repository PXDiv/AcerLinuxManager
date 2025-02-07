# Currently In Works, Not Imported in FrontEnd 

import time

# Define temperature thresholds and corresponding fan speeds
FAN_SPEED_MAP = {
    40: 640,
    50: 1024,
    60: 1536,
    70: 2048,
    80: 2560
}

# Add hysteresis to prevent rapid toggling
HYSTERESIS = 3  # Temperature buffer to prevent constant toggling

# Store the last applied speed to avoid unnecessary updates
last_applied_speed = None

def get_fan_speed_for_temp(temp):
    """Returns the fan speed based on the current temperature."""
    for threshold, speed in sorted(FAN_SPEED_MAP.items()):
        if temp < threshold:
            return speed
    return max(FAN_SPEED_MAP.values())  # Max speed if above highest threshold

def DynamicFanSpeed():
    global last_applied_speed

    currentCPUTemp = get_cpu_temp()  # Replace with your function to get CPU temp
    target_speed = get_fan_speed_for_temp(currentCPUTemp)

    # Apply new speed only if it's different from the last applied speed (reduces redundant updates)
    if last_applied_speed is None or abs(last_applied_speed - target_speed) > HYSTERESIS:
        SetFanSpeed(1, target_speed)
        last_applied_speed = target_speed

    # Run the function every second
    root.after(1000, DynamicFanSpeed)
