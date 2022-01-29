from geopy.distance import distance
from math import radians, cos, sin, asin, sqrt
from shapely.geometry import Point,LineString
from copy import deepcopy

def position_converter(*positions):
    """
    converts string numbers to float
    """
    res = []
    for p in positions:
        if hasattr(p,'__iter__'):
            #inner tuples in the list
            for coord in p:
                res.append(
                    (
                        float(coord[0]),
                        float(coord[1])
                    )
                    )
        else :
            res.append(float(p))
    return res


def haversine(center_long, center_lat, point_long, point_lat):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    #convert position valuse to float
    center_long, center_lat, point_long, point_lat = position_converter(
        center_long, 
        center_lat, 
        point_long, 
        point_lat
        )

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
    center_lat,center_long,point_lat,point_long,radius_in_km = position_converter(
        center_lat,
        center_long,
        point_lat,
        point_long,
        radius_in_km
    )
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
    lat1,long1,lat2,long2 = position_converter(
        lat1,
        long1,
        lat2,
        long2
    )
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
    points = position_converter(points)
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
    lat,lng = position_converter(lat,lng)
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
        path = position_converter(path)
        for coordinate in path:
            coordinates.append(Point(coordinate))
        line = line.union(LineString(coordinates))
        print(line.length)
    return line

def is_sub_path_of(super_path:list,sub_path:list):
    """
    returns true if super_path line covers
    sub_path line.
    """
    super_path = position_converter(super_path)
    sub_path = position_converter(sub_path)
    line1 = make_line(*super_path)
    line2 = make_line(*sub_path)
    return line1.covers(line2)

if __name__ == '__main__':
    path_list = [
        [(0,0),(0,1)], 
        [(11,2),(12,9),(4,6)],
        [(3,6),(1,4)]
        
        ]
    depth = lambda L: isinstance(L, (list,tuple,set)) and max(map(depth, L))+1
    print(depth(path_list))
    # line = make_lines(path_list)
    # print(line.contains(Point(0,.5)))

    



     