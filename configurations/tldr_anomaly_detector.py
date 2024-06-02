from tldr_fail_test import *

def tldr_dectector(host, addr = None, port = 443):

    BinaryEncoding = ""

    if addr is None:
        addr = (host, port)
    else:
        addr = (addr, port)

    client_hello = make_client_hello(host, kyber=True)

    print(f"About to send a large TLS ClientHello ({len(client_hello)} bytes) to {addr[0]}:{addr[1]}.")
    print()
    print("The server should respond with a TLS ServerHello, which will be some")
    print("byte string beginning with b'\\x16\\x03\\x03'. If it closes the")
    print("connection or sends something else, the server is misbehaving.")
    print()

    print("Sending the large ClientHello in a single write:")
    sock = socket.create_connection(addr)
    try:
        sock.send(client_hello)
        print(sock.recv(256) , "\n L1-Flag:1")
        BinaryEncoding += "1"
    except Exception as e:
        print(e , "\n L1-Flag:0")
        BinaryEncoding += "0"
    print()

    print("Sending the large ClientHello in two separate writes:")
    sock = socket.create_connection(addr)
    try:
        half = len(client_hello)//2
        sock.send(client_hello[:half])
        time.sleep(1)
        sock.send(client_hello[half:])
        print(sock.recv(256) , "\n L2-Flag:1")
        BinaryEncoding += "1"
    except Exception as e:
        print(e , "\n L2-Flag:0")
        BinaryEncoding += "0"
    print()

    client_hello = make_client_hello(host, kyber=False)

    print(f"Repeating the process with a smaller ClientHello ({len(client_hello)} bytes).")
    print("This ClientHello would usually be sent in a single packet, but it")
    print("demonstrates that the bug is not triggered by the size of the")
    print("ClientHello, but whether it comes in across multiple reads.")
    print("(Note this ClientHello is smaller than a ClientHello from browsers")
    print("today. This script does not reproduce some padding behavior.)")
    print()

    print("Sending the smaller ClientHello in a single write:")
    sock = socket.create_connection(addr)
    sock.send(client_hello)
    try:
        print(sock.recv(256) , "\n S1-Flag:1")
        BinaryEncoding += "1"
    except Exception as e:
        print(e , "\n S1-Flag:0")
        BinaryEncoding += "0"
    print()

    print("Sending the smaller ClientHello in two separate writes:")
    sock = socket.create_connection(addr)
    try:
        half = len(client_hello)//2
        sock.send(client_hello[:half])
        time.sleep(1)
        sock.send(client_hello[half:])
        print(sock.recv(256) , "\n S2-Flag:1")
        BinaryEncoding += "1"
    except Exception as e:
        print(e , "\n S2-Flag:0")
        BinaryEncoding += "0"
    
    return BinaryEncoding


print(tldr_dectector("8.8.8.8"))