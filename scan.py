import socket
import sys


def formatResult(res):
    opn, port, service = res

    if opn:
        if service:
            return f"[OPEN] port {port} ({service})"
        return f"[OPEN] port {port}"
    return f"[CLOSED] port {port}"

def getService(port):
    try:
        return socket.getservbyport(port, "tcp")
    except:
        return "unknown"
    

def scanMulti(target, minPort, maxPort,showServices=False,verbose=False):
    for port in range(minPort, maxPort + 1):
        res = scan(target,port,showServices)
        if verbose:
            print(formatResult(res))
        else:
            if res[0]:
                print(formatResult(res))

def scanSingle(target, port,showServices=False):
    print(f"Scanning {target}:{port}\n")
    res = scan(target,port,showServices)
    print(formatResult(res))
    print("\nDone.")

def scan(target, port, showServices=False):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)

    try:
        result = s.connect_ex((target, port))

        if result == 0:
            if showServices:
                service = getService(port)
                return (True, port, service)
            else:
                return (True, port,None)
        else:
            return (False, port,None)

    finally:
        s.close()



def checkPort(port):
    return False if port > 65535 or port < 0 else True

def checkHostname(host):
    try:
        socket.gethostbyname(host)
        return True
    except socket.gaierror:
        return False

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
    verbose = "-v" in sys.argv
    if checkHostname(target):
        if len(ports) == 1:
            port = int(ports[0])
            if checkPort(port):
                scanSingle(target, port,showServices)
            else:
                print("invalid port entered")
        elif len(ports) == 2:
            minPort = int(ports[0])
            maxPort = int(ports[1])
            if checkPort(minPort) and checkPort(maxPort):
                scanMulti(target, minPort, maxPort,showServices,verbose)
            else:
                print("invalid port entered")
    else:
        print("invalid hostname or ip entered")


