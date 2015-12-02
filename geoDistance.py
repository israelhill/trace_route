import urllib2
import socket
from math import sin, cos, asin, sqrt, radians
from xml.dom.minidom import parseString

#CONSTANTS
KM = 6367
distances = []



def main(destination):
    print "Destination: " + destination
    ip = get_ip()
    dest_ip = socket.gethostbyname(destination)

    # get coordinates for both IP addresses and compute the distane between them
    lat1, long1 = get_location(ip)
    lat2, long2 = get_location(dest_ip)
    distance = compute_haversine(lat1, long1, lat2, long2)
    distances.append(distance)
    print "Distance between hosts: ", distance, " KM"
    print "\n"



def get_ip():
    # lookup the users IP address
    ip = urllib2.urlopen('http://ip.42.pl/raw').read()
    return ip



def get_location(ip_address):
    print "IP: ", ip_address

    # get the IP's coordinates from the geoip website in xml format
    xml = urllib2.urlopen('http://freegeoip.net/xml/{}'.format(ip_address))

    # parse the xml and get the longitude and Latitude. Remove xml tags
    for line in xml:
        if "<Longitude>" in line:
            longitude = float(line.replace("<Longitude>", "").replace("</Longitude>", ""))
        elif "<Latitude>" in line:
            latitude = float(line.replace("<Latitude>", "").replace("</Latitude>", ""))

    print "Latitude: ", latitude
    print "Longitude: ", longitude

    return latitude, longitude


# The haversine function as seen at http://www.movable-type.co.uk/scripts/latlong.html
def compute_haversine(lat1, long1, lat2, long2):
    #convert the coordinates to radians
    latitude1 = radians(lat1)
    longitude1 = radians(long1)
    latitude2 = radians(lat2)
    longitude2 = radians(long2)

    latitude_dist = latitude2 - latitude1
    longitude_dist = longitude2 - longitude1

    a = sin(latitude_dist/2)**2 + cos(latitude1) * cos(latitude2) * sin(longitude_dist/2)**2
    c = 2 * asin(sqrt(a))

    # convert distance to Kilometers
    return c * KM




if __name__ == '__main__':
# def run():
    with open('targets.txt', 'r') as hosts:
        for line in hosts:
            site = line.replace('\n', "")
            main(site)

    # for d in distances:
    #     print d

    # return distances
