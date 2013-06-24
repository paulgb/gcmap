
import pandas as pd
from gcmap import GCMapper

ROUTE_COLS = ('airline_name', 'airline_id', 'source_code', 'source_id', 'dest_code', 'dest_id', 'codeshare', 'stops', 'equiptment')
AIRPORT_COLS = ('airport_id', 'airport_name', 'city', 'country', 'iata', 'icao', 'latitude', 'longitude', 'altitude', 'timezone', 'dst')
def parseint(x):
    try:
        return int(x)
    except ValueError:
        return None
routes = pd.read_csv('routes.dat', header=None, names=ROUTE_COLS, converters={'source_id': parseint, 'dest_id': parseint})
airports = pd.read_csv('airports.dat', header=None, names=AIRPORT_COLS)

airports_latlon = airports.ix[:,('airport_id','latitude','longitude')]
airport_pairs = routes.groupby(('source_id', 'dest_id')).size()
airport_pairs = airport_pairs.reset_index()
airport_pairs.columns = ('source_id', 'dest_id', 'cnt')
airport_pairs.head()

airport_pairs = airport_pairs.merge(airports_latlon, left_on='source_id', right_on='airport_id') \
                             .merge(airports_latlon, left_on='dest_id', right_on='airport_id', suffixes=('_source', '_dest'))

gcm = GCMapper(width=12000)
gcm.set_data(airport_pairs.longitude_source,
             airport_pairs.latitude_source,
             airport_pairs.longitude_dest,
             airport_pairs.latitude_dest,
             airport_pairs.cnt)
gcm.draw()

