import urllib2
import socket
from math import sin, cos, asin, sqrt, radians
from xml.dom.minidom import parseString

KM = 6367

def main():
    ip = get_ip()
    kfc = socket.gethostbyname("kfc.com")
    # ip2 = "184.51.126.194"
    lat1, long1 = get_location(ip)
    lat2, long2 = get_location(kfc)
    distance = compute_haversine(lat1, long1, lat2, long2)
    print "Distance is: ", distance

def get_ip():
    ip = urllib2.urlopen('http://ip.42.pl/raw').read()
    return ip

def get_location(ip_address):
    print "IP: ", ip_address

    xml = urllib2.urlopen('http://freegeoip.net/xml/{}'.format(ip_address))
    for line in xml:
        if "<Longitude>" in line:
            longitude = float(line.replace("<Longitude>", "").replace("</Longitude>", ""))
        elif "<Latitude>" in line:
            latitude = float(line.replace("<Latitude>", "").replace("</Latitude>", ""))

    print "Latitude: ", latitude
    print "Longitude: ", longitude

    return latitude, longitude

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
    main()
