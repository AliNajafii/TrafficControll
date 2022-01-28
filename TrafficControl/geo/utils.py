from geopy.distance import distance
from math import radians, cos, sin, asin, sqrt
from shapely.geometry import Point,LineString
from copy import deepcopy

def haversine(center_long, center_lat, point_long, point_lat):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    center_long, center_lat, point_long, point_lat = map(radians, [center_long, center_lat, point_long, point_lat])

    # haversine formula 
    dlon = point_long - center_long 
    dlat = point_lat - center_lat 
    a = sin(dlat/2)**2 + cos(center_lat) * cos(point_lat) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def in_radius_range(center_lat,center_long,point_lat,point_long,radius_in_km):
    """
    uses haversine formula to calculate
    if a point coordinates is in radius range of the 
    center coordinates with the given radiuos
    it returns true.
    """
    dist = haversine(center_long,center_lat,point_long,point_lat)
    return dist <= radius_in_km

def get_distance(lat1,long1,lat2,long2,measure='km'):
    
    """
    calculates the distance between two points
    and returns a dictionary :
    {
        'km' : distance in km,
        'm' : distance in m
    }
    """

    dist = distance((lat1,long1),(lat2,long2))
    return {
        'km' : dist.km,
        'm' : dist.m
    }

def make_line(*points:tuple):
    """
    givs points as tuple and make linestrings
    and return shapely module LineString
    """
    base_line = LineString()
    points = []
    for lat,lng in points:
        points.append(Point(lat,lng))
    base_line.union(LineString(points))
    return base_line

def in_line(lat,lng,line:LineString):
    """
    returns true if given point is in
    the given line.
    """
    return line.contains(Point(lat,lng))

def make_lines(path_list:list):
    """
    creates LineString with list of pathes.
    for ex : path_list = [
        [(0,0),(0,1)], -->each inner list is a path
        [(11,2),(12,9),(4,6)],
        [(3,6),(1,4)]
        
        ]
    """
    line = LineString()
    for path in path_list :
        coordinates = []
        for coordinate in path:
            coordinates.append(Point(coordinate))
        line = line.union(LineString(coordinates))
        print(line.length)
    return line

# if __name__ == '__main__':
#     path_list = [
#         [(0,0),(0,1)], 
#         [(11,2),(12,9),(4,6)],
#         [(3,6),(1,4)]
        
#         ]
#     line = make_lines(path_list)
#     print(line.contains(Point(0,.5)))
    



     