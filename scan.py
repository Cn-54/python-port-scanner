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

    if len(ports) == 1:
        port = int(ports[0])
        scanSingle(target, port,showServices)
    elif len(ports) == 2:
        minPort = int(ports[0])
        maxPort = int(ports[1])
        scanMulti(target, minPort, maxPort,showServices,verbose)