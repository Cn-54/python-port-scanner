import socket
import sys


def getService(port):
    try:
        return socket.getservbyport(port, "tcp")
    except:
        return "unknown"

def scanMulti(target, minPort, maxPort,showServices=False):
    socket.setdefaulttimeout(0.5)
    print(f"Scanning {target}...\n")
    for port in range(minPort, maxPort + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((target, port))
        if result == 0:
            if showServices:
                service = getService(port)
                print(f"[OPEN] Port {port} ({service})")
            else:
                print(f"[OPEN] Port {port}")
        else:
            print(f"[CLOSED] Port {port}")
        s.close()
    print("\nDone.")


def scanSingle(target, port,showServices=False):
    socket.setdefaulttimeout(0.5)
    print(f"Scanning {target}:{port}\n")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = s.connect_ex((target, port))
    if result == 0:
        if showServices:
            service = getService(port)
            print(f"[OPEN] Port {port} ({service})")
        else:
            print(f"[OPEN] Port {port}")
    else:
        print(f"[CLOSED] Port {port}")
    s.close()

    print("\nDone.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("python scanner.py <target> <port>")
        print("python scanner.py <target> <start:end>")
        sys.exit(1)

    target = sys.argv[1]
    portArg = sys.argv[2]

    ports = portArg.split(":")

    showServices = "-s" in sys.argv

    if len(ports) == 1:
        port = int(ports[0])
        scanSingle(target, port,showServices)
    elif len(ports) == 2:
        minPort = int(ports[0])
        maxPort = int(ports[1])
        scanMulti(target, minPort, maxPort,showServices)