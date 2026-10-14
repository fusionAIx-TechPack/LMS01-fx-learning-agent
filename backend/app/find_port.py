"""Port resolution utility.
Finds an available local port starting from a desired port.
Safe for invocation from Windows batch scripts and Unix shell scripts without syntax escaping issues.
"""
import socket
import sys

def get_free_port(start_port: int = 8088, scan_count: int = 25) -> int:
    for port in range(start_port, start_port + scan_count):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    return start_port

if __name__ == "__main__":
    start = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 8088
    print(get_free_port(start))
