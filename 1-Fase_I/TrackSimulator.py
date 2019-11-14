# -*- coding: utf-8 -*-
"""
@author: tonibous
"""
import pandas as pd
import matplotlib as plt
import matplotlib.cm as cm
from geopy.distance import distance, VincentyDistance
import TrackPlot as tp
import geopy.distance
import numpy as np
from geopy import Point
import geopy
import random
import math
import gpxpy
import gpxpy.gpx
import TrackAnalyzer as ta
import networkx as nx

PROB_RETURN = 0.4
NUMBER_SIMULATIONS = 5
EARTH_RADIUM = 6378.1  # Radius of the Earth


def get_random_value(data):
    data.sort()
    cd_dx = np.linspace(0., 1., len(data))
    ser_dx = pd.Series(cd_dx, index=data)
    rnd = np.random.random()
    return np.argmax(np.array(ser_dx > rnd))


def calculate_initial_compass_bearing(point_a, point_b):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(point_a) != tuple) or (type(point_b) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(point_a[0])
    lat2 = math.radians(point_b[0])

    diff_long = math.radians(point_b[1] - point_a[1])

    x = math.sin(diff_long) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                                           * math.cos(lat2) * math.cos(diff_long))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360
    return compass_bearing


def getPoint(point, bearing, distance):
    bearing_radians = math.radians(bearing)

    lat_point = math.radians(point[0])  # Current lat point converted to radians
    lon_point = math.radians(point[1])  # Current long point converted to radians

    lat_result = math.asin(math.sin(lat_point) * math.cos(distance / EARTH_RADIUM) +
                           math.cos(lat_point) * math.sin(distance / EARTH_RADIUM) * math.cos(bearing_radians))

    lon_result = lon_point + math.atan2(math.sin(bearing_radians) * math.sin(distance / EARTH_RADIUM) *
                                        math.cos(lat_point), math.cos(distance / EARTH_RADIUM) - math.sin(lat_point) *
                                        math.sin(lat_result))

    lat_result = math.degrees(lat_result)
    lon_result = math.degrees(lon_result)

    return lat_result, lon_result


def simulate_segment(track_analyze, segment):
    """
    Simulates creation of points in the segment delimited by two nodes of the graph
    :param track_analyze: TrackAnalysis of the project with all the information for recreating the segment
    :param segment: Segment to simulate (Origin node, Target node)
    :return: Array of points (lat,lon) of the simulation
    """
    if track_analyze.trackpoint_number:
        gen_points_number = get_random_value(track_analyze.trackpoint_number)
    else:
        gen_points_number = 12

    aux = 0
    origin_node = segment[0]
    target_node = segment[1]
    segment = []
    origin_point = Point(track_analyze.graph.nodes[origin_node]['y'], track_analyze.graph.nodes[origin_node]['x'])
    target_point = Point(track_analyze.graph.nodes[target_node]['y'], track_analyze.graph.nodes[target_node]['x'])
    d = geopy.distance.distance(origin_point, target_point).m
    # print("Origen segmento: " + str(origin_node))
    # print("Punto origen segmento: " + str(origin_point))
    # print("Objetivo segmento: " + str(target_node))
    # print("Punto objetivo segmento: " + str(target_point))
    try:
        dest, aux = calculate_point(track_analyze, segment, origin_node, target_node, origin_point, target_point)
        next = dest
        # print("Dis. Inicio : " + str(aux))
        while aux > 24 and len(segment) < 30:
            dest, aux = calculate_point(track_analyze, segment, origin_node, target_node, next, target_point)
            # print(aux)
            next = dest
    except KeyError:
        pass
    # print("Dis Final : " + str(aux))

    return np.array(segment)


def calculate_point(track_analysis, segment, origin_node, target_node, origin_point, target_point):
    """
    Calculates the point for the simulated segment.
    This point is calculated by a distance and a bearing.
    While the distance from the generated point to the closest point of the segment is not sustainable we recalculate
    the point.

    :param track_analysis: Object of TrackAnalyzer class
    :param segment: Segment related to the generated point
    :param origin_node: Origin node of the segment
    :param target_node: Target node of the segment
    :param origin_point: Origin GPS point of the segment
    :param target_point: Target point of the segment
    :return:
    """
    if track_analysis.trackpoint_route_distance:
        rnd_distance = random.choice(track_analysis.trackpoint_route_distance) / 1000
    else:
        rnd_distance = 0.04
    rnd_distance = 0.04
    # Cargar la estructura de lista del segmento
    coords = track_analysis.graph.edges[(origin_node, target_node, 0)]['geometry'].coords[:]
    coord_list = [list(reversed(item)) for item in coords]

    # Calcular el indice del punto GPS más cercano del segmento
    idx = get_closest_segment_point(track_analysis, coord_list, origin_node, target_node, origin_point)
    # print("indice del punto más cercano: " + str(idx))

    # Calculamos la dirección entre el punto que origen y el siguiente punto encontrado
    try:
        destPoint = (coord_list[idx + 1][0], coord_list[idx + 1][1])

    except IndexError:
        print("Error de indice")
        destPoint = (target_point[0], target_point[1])
        # Si nos hemos pasado con el indice apuntaremos directamente al final.

    bearing = calculate_initial_compass_bearing((origin_point[0], origin_point[1]), (destPoint[0], destPoint[1]))

    # Calculamos una desviación
    rndbear = np.random.uniform(bearing - 20, bearing + 20)

    # Calculamos distacia al punto que queremos crear
    # point_distance = get_random_value(ta.trackpoint_distance)/8000
    point_distance = rnd_distance

    # Generamos el punto
    dest = getPoint((origin_point[0], origin_point[1]), rndbear, point_distance)

    dist_gen_point = geopy.distance.distance(dest, (destPoint[0], destPoint[1])).m
    # print("Distancia al punto idx: " + str(dist_gen_point))
    i = 0
    while dist_gen_point > 70 and i < 30:
        i = i + 1
        rndbear = np.random.uniform(bearing - 20, bearing + 20)
        # print("random: " + str(rndbear))
        # print("bearing: " + str(bearing))
        dest = getPoint((origin_point[0], origin_point[1]), rndbear, point_distance)
        dist_gen_point = geopy.distance.distance(dest, (destPoint[0], destPoint[1])).m
        # print("Distancia al punto idx: " + str(dist_gen_point))

    # Calculamos la distancia entre este punto y el final
    aux = geopy.distance.distance(dest, target_point).m

    # Meter el punto en el segmento resultante
    segment.append(Point(dest[0], dest[1]))

    # Devolvemos el punto y la distancia de este al final
    return dest, aux


def get_closest_segment_point(track_analysis, coord_list, origin_node, target_node, point):
    """
    Gets the closest point's index given a segment and a point.

    :param track_analysis: Object of TrackAnalyzer class
    :param coord_list: List of GPS points of the segment
    :param origin_node: Origin node of the segment
    :param target_node: Target node of the segment
    :param point: GPS point to identify
    :return: Index of the list of closest point of the coordinates' list
    """
    # Buscamos los puntos candidatos más cercanos.
    a, b = track_analysis.get_closest_nodes([[point[0], point[1]]], 15)
    aux = []
    # Filtramos aquellos que pertenecen a la ruta en cuestión
    for idx in range(0, len(a)):
        aux.append([a[idx][0], a[idx][1], b[0][idx]])

    # Ordenamos por distancia
    aux = sorted(aux, key=lambda x: x[2])
    correct_aux = [a for a in aux if a[1] == (origin_node, target_node)]

    # Sacamos el índice del punto más cercano (primero de la lista) dentro de la lista de puntos del segmento
    try:
        idx = coord_list.index([correct_aux[0][0][0], correct_aux[0][0][1]])
    except (ValueError, IndexError):
        # Si falla devolvemos directamente el final
        idx = len(coord_list)
    return idx


def get_most_frequent_node(track_analysis, node, path):
    """
    Every segment have a frequency. It returns choose one of the options according the frequencies.
    :param path:
    :param track_analysis: Object od TrackAnalyzer class
    :param node: Node of the selection
    :return: selected target node
    """
    target_list = []
    roll = random.random()
    for i in track_analysis.graph.edges(node, data=True):
        target_list.append([i[1], i[2]['frequency']])
    target_list.sort(key=lambda x: x[1])
    aux = 0
    selected_target = 67
    idx_target = 0
    for target in target_list:

        aux = aux + target[1]
        if roll < aux:
            selected_target = target[0]
            if track_analysis.graph.degree(selected_target) > 1 and len(path) > 2 and path[-2] == selected_target:
                retro_roll = random.random()
                if retro_roll < PROB_RETURN:
                    selected_target = target[0]
                else:
                    selected_target = target_list[idx_target - 1][0]
            break
        idx_target = idx_target + 1
    return selected_target


def create_path(track_analysis, origin, dist):
    """
    Create the most frequent path given frequencies stored at track_analysis object.
    Given an origin node and a maximum distance it creates the most frequent path.
    Once the track_analysis is updated the path may change.
    It does not recognise returns of route.
    :param track_analysis:  Object of TrackAnalyzer class
    :param origin: Origin node of the simulated route
    :param dist: Distance of the route.
    :return: created path, distance of this path.
    """
    path = []
    distance_created = 0
    prev_node = origin
    path.append(origin)
    while distance_created < dist:
        next_node = get_most_frequent_node(track_analysis, prev_node, path)
        # print("next_node: ",next_node)
        distance_aux = distance_created + track_analysis.graph.edges[(prev_node, next_node, 0)]['length']
        if distance_aux < dist:
            distance_created = distance_aux
            path.append(next_node)
            prev_node = next_node
            # print("distance", distance_created)
        else:
            return path, distance_created
    return path, distance_created


def simulate_route(track_analysis, origin, end, distance, ax):
    """
    Simulates creation of route given an origin and target point.
    This simulation is made by searching Dijkstra's path and simulating points segment by segment.

    :param track_analysis: Object of TrackAnalyzer class
    :param origin: Origin node of the simulated route
    :param end: Target node of the simulated route
    :param ax: axes for plotting points
    :return: Numpy array of points of the simulated route
    """
    simulated_track = []
    # Simular creación de trayectoria completa

    # Encontrar el camino más probable.
    list_original = []
    list_distances = []
    list_reduced = []
    # Realizamos 5 y nos quedamos con el que tenga menos repeticiones.
    for i in range(0, NUMBER_SIMULATIONS):
        simulated_path_aux, distance_generated = create_path(track_analysis, origin, distance)
        list_original.append(simulated_path_aux)
        list_distances.append(distance_generated)
        res = []
        res = [l for l in simulated_path_aux if l not in res]
        list_reduced.append(res)

    idx_to_return = list_reduced.index(max(list_reduced, key=len))
    simulated_path = list_original[idx_to_return]
    distance_to_return = list_distances[idx_to_return]
    # Iterar para cada uno de los nodos del camino escogido
    path = []
    for d in range(0, len(simulated_path) - 1):
        path.append([simulated_path[d], simulated_path[d + 1]])

    # Lista de colores para los segmentos
    colors = ["green", "red", "blue", "purple", "pink", "orange", "yellow", "black"]
    # Indice para crear segmentos de colores distintos
    idx_color = 0
    for segment in path:
        seg = simulate_segment(track_analysis, segment)
        # print("Puntos: " + str(len(seg)))
        idx_color = idx_color + 1
        # tp.plot_points(ax, seg, colors[idx_color % len(colors)])
        for s in seg:
            simulated_track.append(s)

    return np.array(simulated_track), distance_to_return



def create_gpx_track(data, file_name):
    # Creating a new file:
    gpx = gpxpy.gpx.GPX()

    # Create first track in our GPX:
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    # Create first segment in our GPX track:
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    # Create points:
    for point in data:
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(point[0], point[1]))
        
    # print('Created GPX:', gpx.to_xml())
    with open(file_name, "w") as f:
        f.write(gpx.to_xml())
