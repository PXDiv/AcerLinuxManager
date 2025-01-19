# AcerNitroLinuxGamingDriver
An experimental driver to control fan speeds\ and the rgb of keyboard on Acer Nitro/Predator.

Thanks to https://github.com/tuxedocomputers/tuxedo-drivers for a starting point to new device based wmi drivers on linux kernel and https://github.com/JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module for setting 4zone keyboard rgb.

<p>Usage:<br>
Setting fan speeds<br>
*Cpu fan(left) echo {fanspeed} /dev/fan1<br>
*Gpu fan(right) echo {fanspeed} /dev/fan2<br>
Note: the fan speed should be multiples of 128. eg. 128 256 512 768<br>


Some things can be bugprone, feel free to report issues from here.

<p>To-do: Implementing the turbo mode in NitroSense<br>
Making turbo button usable <br>
Making nitrosense button usable <br>
Making a dkms module <br>
Adding it to aur <br>
Writing a daemon and writing services for both systemctl and openrc service to set and remember the settings every boot. </p>

NOTE: This driver is experimental and it can be dangereous, i am taking no responsibility.
  
