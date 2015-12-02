import urllib2
from math import sin, cos, asin, sqrt
from xml.dom.minidom import parseString

KM = 6367

def main():
    ip = get_ip()
    get_location(ip)

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
    latitude1 = math.radians(lat1)
    longitude1 = math.radians(long1)
    latitude2 = math.radians(lat2)
    longitude2 = math.radians(long2)

    latitude_dist = latitude2 - latitude1
    longitude_dist = longitude2 - longitude1

    a = math.sin(latitude_dist/2)**2 + math.cos(latitude1) * math.cos(latitude2) * math.sin(longitude/2)**2
    c = 2 * math.asin(sqrt(a))

    # convert to km and return
    return c * KM



if __name__ == '__main__':
    main()
