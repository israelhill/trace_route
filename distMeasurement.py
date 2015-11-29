import socket
import select

def main(destination):
    # get the IP address of the destination adress
    dest_address = socket.gethostbyname(destination)
    port = 33434
    # gets a particular protocol by name... needed for RAW Sockets
    # it specifies what protocol I want to use
    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')
    # Start the time to live at 1
    ttl = 32
    max_hops = 128



    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
    send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

    # bind the adress to recv_socket. empty string because we are accepting
    # packets from any host on port 33434 (unlikely port)
    recv_socket.bind(("", port))

    # Send no data (empty string) to the destination host
    # on an unlikely port
    send_socket.sendto("", (destination, port))
    ready = select.select([recv_socket], [], [], 10.0)

    if ready:
        rcvd_packet = current_address = None
        try:
            # get data from the recv_socket,
            # recvfrom() returns the packet data and adress
            rcvd_packet, current_address = recv_socket.recvfrom(1500)

            # get the IP address
            current_address = current_address[0]

            print "Received Packet: " + rcvd_packet
        except socket.error:
            pass
        finally:
            send_socket.close()
            recv_socket.close()

if __name__ == '__main__':
    main('google.com')
