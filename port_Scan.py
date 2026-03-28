import pyfiglet
import sys
import socket
from datetime import datetime
import os
import argparse
from concurrent.futures import ThreadPoolExecutor

def print_banner(message):
    """Prints a banner with a message."""
    print("\n" + "=" * len(message))
    print(message)
    print("=" * len(message))

def print_section_header(message, char='-'):
    """Prints a section header with a specified character."""
    print("\n" + char * len(message))
    print(message)
    print(char * len(message))

def parse_ip_list(ip_list):
    """Parse IP addresses from input list or file."""
    ips = []
    for item in ip_list:
        if os.path.isfile(item):
            with open(item, 'r') as file:
                ips.extend([ip.strip() for ip in file.read().splitlines() if ip.strip()])
        else:
            # Handle comma-separated list
            ips.extend([ip.strip() for ip in item.split(',') if ip.strip()])
    return ips

def parse_ports(port_str):
    """Parse port range or comma-separated list."""
    ports = []
    try:
        if '-' in port_str:
            start, end = map(int, port_str.split('-'))
            ports = list(range(start, end + 1))
        else:
            ports = [int(p.strip()) for p in port_str.split(',') if p.strip()]
    except ValueError:
        print(f"[x] Invalid port specification: {port_str}")
        sys.exit(1)
    return ports

def scan_port(target, port, timeout):
    """Attempt to connect to a specific port."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "Unknown"
                return port, service
    except:
        pass
    return None

def main():
    parser = argparse.ArgumentParser(description='Fast Port Scanner - Scan for open ports on specified IP addresses.')
    parser.add_argument('-i', '--ip', metavar='IP', type=str, nargs='+', help='Target IP addresses (comma/space separated).')
    parser.add_argument('-f', '--file', metavar='FILE', type=str, help='Read target IP addresses from a file.')
    parser.add_argument('-p', '--ports', metavar='PORTS', type=str, default="1-1024", help='Port range (e.g., 1-100) or list (e.g., 80,443). Default: 1-1024.')
    parser.add_argument('-t', '--threads', metavar='THREADS', type=int, default=100, help='Number of concurrent threads. Default: 100.')
    parser.add_argument('--timeout', metavar='SECONDS', type=float, default=1.0, help='Socket timeout in seconds. Default: 1.0.')
    parser.add_argument('-o', '--output-dir', metavar='DIRECTORY', type=str, help='Directory to save output files.')
    
    args = parser.parse_args()

    if not (args.ip or args.file):
        parser.print_help()
        sys.exit(1)

    # Resolve targets
    targets = []
    if args.file:
        with open(args.file, 'r') as file:
            targets.extend([line.strip() for line in file.readlines() if line.strip()])
    if args.ip:
        targets.extend(parse_ip_list(args.ip))
    
    targets = list(set([ip for ip in targets if ip])) # Deduplicate and prune
    ports_to_scan = parse_ports(args.ports)

    # Banner
    ascii_banner = pyfiglet.figlet_format("PORT SCANNER", font="slant")
    print(ascii_banner)
    print(f"Scanning {len(targets)} targets with {args.threads} threads...")
    print(f"Port range: {args.ports} | Timeout: {args.timeout}s")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        for idx, target in enumerate(targets, 1):
            target = target.strip()
            print_section_header(f"Scanning Target ({idx}/{len(targets)}): {target}", char='*')
            
            # Fast check if host is up (optional, but good for UX)
            try:
                socket.gethostbyname(target)
            except socket.gaierror:
                print(f"[x] Could not resolve host: {target}")
                continue

            open_ports = []
            
            # Using ThreadPoolExecutor for concurrent scanning
            with ThreadPoolExecutor(max_workers=args.threads) as executor:
                futures = [executor.submit(scan_port, target, port, args.timeout) for port in ports_to_scan]
                
                for future in futures:
                    res = future.result()
                    if res:
                        port, service = res
                        open_ports.append((port, service))
                        print(f"[+] Port {port:<5} | OPEN ({service})")

            # Output results
            if open_ports:
                now = datetime.now()
                date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
                ip_filename = target.replace(".", "-").replace(":", "-") # handle ipv6 briefly
                
                output_dir = args.output_dir or "."
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                    
                file_path = os.path.join(output_dir, f"open_ports_{ip_filename}_{date_time}.txt")
                
                try:
                    with open(file_path, "w") as f:
                        f.write(f"Scan Results for {target}\n")
                        f.write(f"Time: {now}\n")
                        f.write("-" * 30 + "\n")
                        for port, service in sorted(open_ports):
                            f.write(f"{port}: {service}\n")
                    print_banner(f"[v] Results saved to '{file_path}'")
                except Exception as e:
                    print_banner(f"[x] Error saving results: {e}")
            else:
                print_section_header(f"[x] No open ports found for {target}", char='-')

    except KeyboardInterrupt:
        print("\n[x] Scan interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()