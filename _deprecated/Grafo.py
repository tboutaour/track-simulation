# -*- coding: utf-8 -*-
"""
Created on Wed May  8 18:01:48 2019

@author: tonibous
"""

import osmnx as ox
from sklearn.neighbors import KDTree
import numpy as np


class Grafo:
        def __init__(self, north, south,east,west,p1):
            self.north = north
            self.south = south
            self.east = east
            self.west = west
            self.Grafo = ox.graph_from_bbox(self.north,self.south,self.east,self.west)
            self.p1 = p1

        def GenerarKDtreeSegmentos(self, data):
            self.nodes, _ = ox.graph_to_gdfs(self.Grafo)
            self.tree = KDTree(data[:,:2], metric='euclidean')
                    
        def getClosestNodes(self, data,puntos):
            dist_cerc, idx_cerc = self.tree.query(puntos, k = 1 , return_distance=True)
            return data[idx_cerc[:,0]][:,2], data[idx_cerc[:,0]][:,3], dist_cerc
            
        def GetNodePoints(self, t):
            ruta_simplificada = []
            for b in t:
                lon = self.Grafo.node[b]['x']
                lat = self.Grafo.node[b]['y']
                ruta_simplificada.append([lat,lon])
            return np.array(ruta_simplificada)
        
#        def GenerarRutaRandom(self):
#            route = nx.shortest_path(self.Grafo, np.random.choice(self.Grafo.nodes), 
#            np.random.choice(self.Grafo.nodes))
#            ox.plot_graph_route(self.Grafo, route, fig_height=10, fig_width=10)

#        def GenerarPuntoRandom(self):
#            aux = self.Grafo.nodes[np.random.choice(self.Grafo.nodes)]
#            fig, ax = ox.plot_graph(self.Grafo, fig_height=10, fig_width=10, 
#                        show=False, close=False, 
#                        edge_color='black')
#            ax.scatter(aux['x'], aux['y'], c='red', s=100)
            