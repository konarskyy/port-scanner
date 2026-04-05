import socket
import argparse
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm  # <-- 1. import

KNOWN_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 3306: "MySQL", 5432: "PostgreSQL",
    6379: "Redis", 8080: "HTTP-alt", 27017: "MongoDB"
}

def get_service(port):
    try:
        return socket.getservbyport(port)
    except:
        return KNOWN_PORTS.get(port, "unknown")

def scan_port(host, port, timeout):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            return (port, get_service(port))
    except socket.error:
        pass
    return None

def main():
    parser = argparse.ArgumentParser(description="Port Scanner")
    parser.add_argument("host")
    parser.add_argument("-s", "--start", type=int, default=1)
    parser.add_argument("-e", "--end", type=int, default=1024)
    parser.add_argument("-t", "--threads", type=int, default=100)
    parser.add_argument("--timeout", type=float, default=1.0)
    args = parser.parse_args()

    try:
        ip = socket.gethostbyname(args.host)
    except socket.gaierror:
        print(f"Błąd: nie można rozwiązać adresu '{args.host}'")
        sys.exit(1)

    print(f"\n{'='*50}")
    print(f" Cel:   {args.host} ({ip})")
    print(f" Porty: {args.start}–{args.end}")
    print(f" Start: {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*50}\n")

    open_ports = []
    ports = list(range(args.start, args.end + 1))

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(scan_port, ip, p, args.timeout): p for p in ports}

        # 2. owijamy futures w tqdm — on liczy ile już gotowych
        with tqdm(total=len(ports), desc="Skanowanie", unit="port",
              bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]") as pbar:

            from concurrent.futures import as_completed
            for future in as_completed(futures):  # 3. as_completed zamiast listy
                result = future.result()
                if result:
                    open_ports.append(result)
                    # tqdm.write nie psuje paska — zwykły print by go rozjechał
                    tqdm.write(f"  [+] Port {result[0]:<6} {result[1]}")
                pbar.update(1)  # <-- przesuwa pasek o 1

    open_ports.sort()
    print(f"\n{'='*50}")
    print(f" Znaleziono {len(open_ports)} otwartych portów")
    print(f"{'='*50}")
    print(f"\n{'PORT':<10}{'USŁUGA'}")
    print(f"{'-'*25}")
    for port, service in open_ports:
        print(f"{port:<10}{service}")

if __name__ == "__main__":
    main()
