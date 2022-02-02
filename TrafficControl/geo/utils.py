from geopy.distance import distance
from math import radians, cos, sin, asin, sqrt
from shapely.geometry import Point,LineString
from copy import deepcopy
from django.db.models import QuerySet


def position_converter(positions):
    """
    converts string numbers to float
    """
    for e in positions:
        if isinstance(e,tuple):
            new_tuple = tuple()
            t_index = positions.index(e)
            for t in e :
                if isinstance(t,str):
                    t = float(t)
                new_tuple += (t,)

            positions[t_index] = new_tuple
        elif isinstance(e,str):
            index = positions.index(e)
            positions[index] = float(e)
        
        elif hasattr(e,'__iter__'):
            if isinstance(e,QuerySet):
                index = positions.index(e)
                new_item = list(e)
                positions[index] = new_item
                position_converter(new_item)
            else:
                position_converter(e)
    return positions
                


def haversine(center_long, center_lat, point_long, point_lat):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    #convert position valuse to float
    center_long, center_lat, point_long, point_lat = position_converter(
        [center_long, 
        center_lat, 
        point_long, 
        point_lat]
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
        [center_lat,
        center_long,
        point_lat,
        point_long,
        radius_in_km]
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
        [lat1,
        long1,
        lat2,
        long2]
    )
    dist = distance((lat1,long1),(lat2,long2))
    return {
        'km' : dist.km,
        'm' : dist.m
    }

def make_line(points):
    """
    givs points as tuple and make linestrings
    and return shapely module LineString
    """
    
    points = position_converter(points)
    
    line_points = []
    for lat,lng in points:
        line_points.append(Point(lat,lng))
    base_line=LineString(line_points)
    
    return base_line

def in_line(lat,lng,line:LineString):
    """
    returns true if given point is in
    the given line.
    """
    lat,lng = position_converter([lat,lng])
    point = Point(lat,lng)
    return line.contains(point) or line.covers(point)

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
    return line

def is_sub_path_of(super_path:list,sub_path:list):
    """
    returns true if super_path line covers
    sub_path line.
    """
    super_path = position_converter(super_path)
    sub_path = position_converter(sub_path)
    line1 = make_line(super_path)
    line2 = make_line(sub_path)
    return line1.covers(line2)




    



     