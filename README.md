# Fast Multithreaded Port Scanner

A lightweight, efficient, and fast port scanner written in Python. It uses multithreading to scan thousands of ports in seconds and includes service detection and result logging.

## Features
- **Multithreading**: Choose the number of threads for lightning-fast scans.
- **Port Ranges**: Scan specific ports, ranges (e.g., 1-1024), or all ports (1-65535).
- **Service Detection**: Automatically identifies common services running on open ports.
- **Result Logging**: Saves all discovered open ports to detailed text files.
- **Bulk Scanning**: Supports scanning multiple IP addresses from a file.
- **Easy to Use**: Simple command-line interface with clear output.

## Installation
No external libraries are strictly required as it uses Python standard `socket` and `concurrent.futures`. However, `pyfiglet` is used for the header banner.

1.  **Install dependencies**:
    ```bash
    pip install pyfiglet
    ```

## Usage

### Basic Scan
Scan common ports (1-1024) for a single IP:
```powershell
python port_Scan.py -i 127.0.0.1
```

### Advanced Usage
- **Custom Port Range**:
    ```powershell
    python port_Scan.py -i 192.168.1.1 -p 1-1000
    ```
- **Specific Ports**:
    ```powershell
    python port_Scan.py -i 127.0.0.1 -p 80,443,3306,8080
    ```
- **Increase Speed (More Threads)**:
    ```powershell
    python port_Scan.py -i 127.0.0.1 -p 1-10000 -t 500
    ```
- **Scan from a File**:
    Create a file called `targets.txt` with one IP per line, then run:
    ```powershell
    python port_Scan.py -f targets.txt -o ./results
    ```

## Arguments
| Argument | Flag | Description | Default |
| :--- | :--- | :--- | :--- |
| **IP** | `-i` / `--ip` | Target IP address(es). | Required (if no -f) |
| **File** | `-f` / `--file` | File containing target IPs. | Optional |
| **Ports** | `-p` / `--ports` | Range (1-100) or list (80,443). | `1-1024` |
| **Threads** | `-t` / `--threads` | Number of concurrent threads. | `100` |
| **Timeout** | `--timeout` | Socket timeout in seconds. | `1.0` |
| **Output** | `-o` / `--output-dir` | Directory to save results. | Current directory |

## Disclaimer
This tool is for educational and authorized testing purposes only. Do not scan any networks or targets that you do not have explicitly permission to test. The authors are not responsible for any misuse of this tool.

## Example Output

When running a scan, you will see a detailed output like this:

```text
    ____  ____  ____  ______   _____ _________    _   ___   ____________ 
   / __ \/ __ \/ __ \/_  __/  / ___// ____/   |  / | / / | / / ____/ __ \
  / /_/ / / / / /_/ / / /     \__ \/ /   / /| | /  |/ /  |/ / __/ / /_/ /
 / ____/ /_/ / _, _/ / /     ___/ / /___/ ___ |/ /|  / /|  / /___/ _, _/ 
/_/    \____/_/ |_| /_/     /____/\____/_/  |_/_/ |_/_/ |_/_____/_/ |_|  

Scanning 1 targets with 500 threads...
Port range: 1-10000 | Timeout: 1.0s
Started at: 2026-03-28 19:13:12

********************************
Scanning Target (1/1): 127.0.0.1
********************************
[+] Port 135   | OPEN (epmap)
[+] Port 445   | OPEN (microsoft-ds)
[+] Port 2869  | OPEN (icslap)
[+] Port 5040  | OPEN (Unknown)
[+] Port 5432  | OPEN (Unknown)

=====================================================================
[v] Results saved to '.\open_ports_127-0-0-1_2026-03-28_19-13-32.txt'
=====================================================================
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


