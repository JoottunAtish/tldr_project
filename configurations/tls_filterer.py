import socket
import ssl



def tls_version_check(ip_address, port):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    with socket.create_connection((ip_address, port)) as sock:
        sock.settimeout(30)
        with context.wrap_socket(sock, server_hostname=ip_address) as ssock:
            return ssock.version()
        

"""
json file:


tls_1-3:
[
ip:
netname:
cipher_suites:[]
]
"""