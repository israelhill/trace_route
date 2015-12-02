import urllib2
from xml.dom.minidom import parseString

def main():
    get_location()

def get_location():
    ip = urllib2.urlopen('http://ip.42.pl/raw').read()
    print "IP: " + ip

    xml = urllib2.urlopen('http://freegeoip.net/xml/{}'.format(ip))
    for line in xml:
        if "<Longitude>" in line:
            longitude = float(line.replace("<Longitude>", "").replace("</Longitude>", ""))
        elif "<Latitude>" in line:
            latitude = float(line.replace("<Latitude>", "").replace("</Latitude>", ""))

    print latitude
    print longitude

    return latitude, longitude


if __name__ == '__main__':
    main()
