# Port Scanner

a simple multithreaded tcp port scanner written in python

## Disclaimer
This tool is intended for educational and authorized security testing purposes only. 
Do not use it on any system without explicit permission. The author is not responsible for misuse or damage caused by this program.

## Usage

```bash
python scanner.py <target> <port>
python scanner.py <target> <start:end>
```

## Examples

```bash
python scanner.py localhost 80
python scanner.py 192.168.1.1 1:1024
python scanner.py scanme.nmap.org 1:1024 -s -v
```

## Flags

| Flag | Description |
|------|-------------|
| -s | Show service names for open ports |
| -v | Verbose mode, show closed ports too |
| -t | Set timeout in seconds (default 0.5) |

## How it works

Performs TCP connect scans by attempting a full connection to each port.
Uses threading with a semaphore to scan up to 100 ports concurrently.
Results are sorted by port number regardless of which threads finish first.
