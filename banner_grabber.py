import socket


def grab_banner(host, port):
    """Connects to the target host and retrieves the banner."""

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(5)

    try:
        print("\nConnecting...\n")
        client_socket.connect((host, port))
        print(f"[+] Successfully connected to {host}:{port}")

        if port in [80, 8080]:
            http_request = (
                f"GET / HTTP/1.1\r\n"
                f"Host: {host}\r\n"
                "Connection: close\r\n\r\n"
            )
            client_socket.sendall(http_request.encode())
            response = client_socket.recv(4096)
            print("\nHTTP Response:\n")
            print(response.decode(errors="ignore"))
        else:
            banner = client_socket.recv(1024)
            print("\nBanner:\n")
            print(banner.decode(errors="ignore"))

    except socket.timeout:
        print("[-] Connection timed out.")
    except ConnectionRefusedError:
        print("[-] Connection refused.")
    except socket.gaierror:
        print("[-] Invalid hostname.")
    except Exception as error:
        print(f"[-] Error: {error}")
    finally:
        client_socket.close()
        print("\nConnection closed.")


def main():
    print("=" * 40)
    print("       Banner Grabber")
    print("=" * 40)

    host = input("Enter target host: ").strip()

    try:
        port = int(input("Enter target port: "))
    except ValueError:
        print("[-] Invalid port number.")
        return

    if not (1 <= port <= 65535):
        print("[-] Port must be between 1 and 65535.")
        return

    grab_banner(host, port)


if __name__ == "__main__":
    main()
