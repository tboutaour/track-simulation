import unittest
from track_analyzer.interactor.get_map_matching_impl import GetMapMatchingImpl
from track_analyzer.entities.hidden_markov_model_impl import HMM
from track_analyzer.repository.resource.gpx_resource_impl import GPXResourceImpl as LoaderSaver
from track_analyzer.entities.track_point import TrackPoint as Point
from track_analyzer.entities.graph_impl import Graph
from track_analyzer.repository.resource.mongo_resource_impl import MongoResourceImpl
from track_analyzer.repository.track_information_repository_impl import TrackInformationRepositoryImpl
import matplotlib.pyplot as plt
import osmnx
import seaborn as sns; sns.set()


class MyTestCase(unittest.TestCase):
    @unittest.skip
    def test_get_nearest_segment_points(self):
        test_file = LoaderSaver("../../../tracks/Ficheros/rutasMFlores/activity_3689734814.gpx")
        point = Point(39.5586107, 2.6227118)
        parsed_file = test_file.parseFile()
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)
        hidden_markov_model = HMM(graph=bellver_graph)
        fig, ax = osmnx.plot_graph(bellver_graph.graph, node_color='black', node_zorder=3, show=False, close=False)
        for p in parsed_file:
            list_of_points = hidden_markov_model.get_closest_nodes(p[2])
            plt.scatter(p[2].get_longitude(), p[2].get_latitude(), c="blue")
            plt.scatter(list_of_points[0][0].get_longitude(), list_of_points[0][0].get_latitude(), c="green")
            for res in range(2, len(list_of_points)):
                plt.scatter(list_of_points[res][0].get_longitude(), list_of_points[res][0].get_latitude(), c="red")

        plt.show()
        self.assertEqual(True, False)

    @unittest.skip
    def test_viterbi_algorithm(self):
        test_file = LoaderSaver("../../data/tracks_to_analysis/activity_3689734814.gpx")
        point = Point(2.6227118, 39.5586107)
        parsed_file = test_file.parseFile()
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)
        hidden_markov_model = HMM(graph=bellver_graph)
        fig, ax = osmnx.plot_graph(bellver_graph.graph, node_color='black', node_zorder=3, show=False, close=False)
        for p in parsed_file:
            plt.scatter(p[2].get_longitude(), p[2].get_latitude(), c="green")
        parsed_point_list = [x[2]for x in parsed_file]
        hmm = GetMapMatchingImpl(parsed_point_list, hidden_markov_model)
        result = hmm.match()
        for r in result:
            plt.scatter(r[0].get_longitude(), r[0].get_latitude(), c="red")
            print(r)
        plt.show()
        self.assertEqual(True, True)

    def test_read_from_data(self):
        bellver_graph = Graph(39.5713, 39.5573, 2.6257, 2.6023)
        mongo_resource = MongoResourceImpl()
        track_information = TrackInformationRepositoryImpl(mongo_resource)
        track = track_information.get_trackinformation_dataframe("activity_3783539967.gpx")
        _, _ = bellver_graph.plot_graph()
        for index, row in track.iterrows():
            try:
                plt.scatter(row['Point_lon'], row['Point_lat'], c="red")
                plt.scatter(row['Projection_lon'], row['Projection_lat'], c="green")
            except AttributeError:
                print("Point not found idx: " + str(index))
        plt.show()



if __name__ == '__main__':
    unittest.main()