# **Acer Nitro & Predator Fan Control (Linux)**

A GUI-based front end for managing fan speeds on Acer Nitro and Predator laptops running Linux. This tool simplifies driver handling and fan speed control, improving usability over the original drivers.

## **About This Project**
This project is a fork of [AcerNitroLinuxGamingDriver](https://github.com/DetuxTR/AcerNitroLinuxGamingDriver) and introduces a GUI frontend along with several new features. The GUI is very basic but functional, ensuring ease of use.

## **Features**
✅ Change fan speeds easily  
✅ Automatically compile and load drivers  
✅ Unload and clean drivers when needed  
✅ Auto-load drivers on frontend startup (optional)  
✅ Save and restore settings for convenience  

## **Installation & Setup**

### **1. Download & Extract**
- Go to the [Releases](#) section and download the latest release.
- Extract the archive.

### **2. Run the Frontend**
- **GUI method:** Right-click → *Run*  
- **Terminal method:** Run with:
  ```bash
  sudo ./frontend
  ```
  
## **Usage Guide**

### **1. Configure Drivers**
- Open the *Advanced Panel* and click **Configure Drivers** to compile and load them.
- Ensure you have the correct **kernel headers** installed.

### **2. Set Fan Speed Ranges**
- Some models use **512-2560**, while others use **128-512**.
- Always set values as multiples of **128**.

### **3. Control Fan Speeds**
- Use the **Mixed Fan** or **Separate Fan** tabs to adjust speeds.
- Enable **Auto-Load Drivers** to load pre-compiled drivers on frontend startup.

### **4. Troubleshooting**
- If the `make` command fails, manually navigate to the `NitroDrivers` directory, open a terminal, and run:
  ```bash
  make
  ```
- If you encounter errors, try restarting your system and ensure the correct Linux headers are installed.
- For any `make` errors, search online for a solution relevant to your kernel version.

### **5. Persistence & Boot Behavior**
- Settings are saved automatically.
- Drivers must be **manually loaded** after every system reboot by launching the frontend.
  - (*Auto-boot functionality may be added later.*)

## **Compatibility**
This driver will only work on Acer laptops that use **WMI-based protocols** for fan control.

## **Upcoming Features**
🔹 **Keyboard lighting control** (future update)

## **Contributing**
Pull requests and contributions are welcome! Please ensure your code follows best practices.

