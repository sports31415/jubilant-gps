import serial, pynmea2
from math import radians, cos, sin, asin, sqrt


def haversine(ln1, lt1, ln2, lt2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    ln1, lt1, ln2, lt2 = map(radians, [ln1, lt1, ln2, lt2])
    # haversine formula
    dlon = ln2 - ln1
    dlat = lt2 - lt1
    a = sin(dlat/2)**2 + cos(lt1) * cos(lt2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c # this is in KM, use 3959 for miles
    return km

if __name__ == '__main__':

    # set up serial connection - define the COM port to use here
    ser = serial.Serial('COM3', 9600)

    streamreader = pynmea2.NMEAStreamReader()

    lat1 = None
    lat2 = None
    lon1 = None
    lon2 = None

    while True:
        gpsdata = ser.readline().decode('utf-8')

        for msg in streamreader.next(gpsdata):
            if msg.sentence_type == 'GGA':
                print('~~~~~~~~~~~~~~~')
                # if this is the first reading then define lat2 and lon2
                if lat2 is None:
                    lat2 = msg.latitude
                    lon2 = msg.longitude
                else:
                    lat1 = lat2
                    lon1 = lon2
                    lat2 = msg.latitude
                    lon2 = msg.longitude
                    print('Distance travelled: ' + haversine(lon1, lat1, lon2, lat2).__str__())

                print('Timestamp: ' + str(msg.timestamp))
                print('Latitude: ' + msg.latitude.__str__())
                print('Longitude: ' + msg.longitude.__str__())
                # print('GPS quality: ' + msg.gps_qual.__str__())
                print('Number of satellites: ' + msg.num_sats.__str__())
                # print('Altitude: ' + msg.altitude.__str__() + msg.altitude_units.__str__())
