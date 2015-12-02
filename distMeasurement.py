import socket
import select
import struct
import time

MILLISECONDS = 1000
TIMEOUT = 1.5
RETRIES = 7

def main(destination):
    print "Destination: " + destination
    print "Attempting to reach host........."
    for _ in range(RETRIES):
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

        recv_socket.settimeout(TIMEOUT)
        send_socket.settimeout(TIMEOUT)

        # bind the address to recv_socket. empty string because we are accepting
        # packets from any host on port 33434 (unlikely port)
        recv_socket.bind(("", port))

        # Send no data (empty string) to the destination host
        # on an unlikely port
        send_time = time.time()
        send_socket.sendto("", (destination, port))
        ready = select.select([recv_socket], [], [], TIMEOUT)

        rcvd_packet = current_address = None
        try:
            rcv_time = time.time()
            # get data from the recv_socket,
            # recvfrom() returns the packet data and adress
            rcvd_packet, current_address = recv_socket.recvfrom(1500)
            # get the IP address
            current_address = current_address[0]

            icmp_header = rcvd_packet[20:28]
            ip_header = rcvd_packet[36:40]
            original_ip_header = rcvd_packet[28:48]

            icmp_type, code, checksum, pid, seq = struct.unpack_from("bbHHh", icmp_header)
            remaining_ttl, protocol, chk_sum = struct.unpack_from("bbH", ip_header)
            original_ip_header_data = struct.unpack_from("!BBHHHBBHII", original_ip_header)

            dest_port = struct.unpack("!H", rcvd_packet[50:52])[0]
            org_dest_ip = original_ip_header_data[9]

            original_destination_ip = socket.inet_ntoa(struct.pack("!L", org_dest_ip))
            # print "Original destination IP: " +  original_destination_ip
            # print "Original destination port:", dest_port

            if dest_address == original_destination_ip and port == dest_port :
                print "Packet varified! This is the original packet."
            else :
                print "Packet not varified."

            num_hops = ttl - remaining_ttl + 1
            RTT = (rcv_time - send_time) * MILLISECONDS
            print "Number of Hops: ", num_hops
            print "Round Trip Time: ", RTT
            break

        except (socket.error, socket.timeout) as e:
            pass
        finally:
            send_socket.close()
            recv_socket.close()
    else :
        print "Timed Out."

if __name__ == '__main__':
    with open('hosts.txt', 'r') as hosts:
        for line in hosts:
            site = line.replace('\n', "")
            main(site)
