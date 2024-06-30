# Open-Source GUDP Attack

This Python script demonstrates a simple Generic UDP (GUDP) attack by sending a specified number of UDP packets to a target IP address and port. It is designed for educational purposes and should only be used with explicit permission on authorized networks.

## Features

- Sends a specified number of UDP packets to a target IP and port.
- Uses Python's `socket` library for network communication.
- Uses `argparse` for command-line argument handling.
- Includes confirmation prompt before initiating the attack.

## Requirements

- Python 3.x (with standard library modules: `socket`, `argparse`, `random`, `time`)

## Usage

1. **Clone the repository**:
   ```bash
   git clone https://github.com/IlumCI/os-gudp.git
   cd os-gudp
   python osgudp.py <target_ip> <target_port> <num_packets>

   
2. **Usage**

   Replace `<target_ip>`, `<target_port>`, and `<num_packets>` with your desired target IP address, port number, and number of packets to send.

3. **Follow the on-screen prompts**:
   - Confirm whether to proceed with the attack (`y` or `n`).

## Example

Send 1000 UDP packets to `192.168.1.100` on port `12345`:
```bash
python osgudp.py 192.168.1.100 12345 1000
```

## Legal Disclaimer

- This script is for educational purposes only.
- Use this script responsibly and with explicit permission from the target network owner.
- Do not use this script for any malicious purposes.

## Contributing

Contributions are welcome! Feel free to fork the repository, make improvements, and submit pull requests.

## Contact

- For questions or feedback, please create an issue or contact @Ilum_. on Discord.
