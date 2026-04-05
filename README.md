# Port Scanner

Multithreaded TCP port scanner written in Python — no external dependencies except `tqdm`.

## Features
- Configurable port range and thread count
- Automatic service detection (SSH, HTTP, FTP...)
- Progress bar with real-time open port display

## Usage
```bash
pip3 install tqdm
python3 scanner.py <host> [-s start] [-e end] [-t threads]
```

## Examples
```bash
python3 scanner.py scanme.nmap.org
python3 scanner.py scanme.nmap.org -s 1 -e 65535 --threads 200
```

## What I learned
- TCP socket programming in Python
- Multithreading with ThreadPoolExecutor
- How TCP handshake works at the code level
