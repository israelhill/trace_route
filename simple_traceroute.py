import socket

def main(destination):
    # get the IP address of the destination adress
    dest_address = socket.gethostbyname(destination)
    port = 33434
    # gets a particular protocol by name... needed for RAW Sockets
    # it specifies what protocol I want to use
    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')
    # Start the time to live at 1
    ttl = 1

    while True:
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
        send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

        # bind the adress to recv_socket. empty string because we are accepting
        # packets from any host on port 33434 (unlikely port)
        recv_socket.bind(("", port))

        # Send no data (empty string) to the destination host
        # on an unlikely port
        send_socket.sendto("", (destination, port))

        current_adress = None
        try:
            # get data from the recv_socket,
            # recvfrom() returns the packet data and adress
            # we dont care about the packet data so we use _
            _, current_adress = recv_socket.recvfrom(512)

            # get the IP address
            current_adress = current_adress[0]
            try:
                # reverse DNS lookup
                current_name = socket.gethostbyaddr(current_adress)[0]
            except socket.error:
                current_name = current_adress
        except socket.error:
            pass
        finally:
            send_socket.close()
            recv_socket.close()

        # print the data
        if current_adress is not None:
                curr_host = "%s (%s)" % (current_name, current_adress)
        else:
            current_host = "*"
        print "%d\t%s" % (ttl, current_host)

        ttl += 1
        # break out the loop when the following are true:
        if current_adress == dest_address or ttl > max_hops:
            break

if __name__ == '__main__':
    main('google.com')
