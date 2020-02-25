import unittest
from repository.trackinformation_repository_impl import TrackInformationRepositoryImpl as TrackInformationRepository
from entities.TrackPoint_impl import TrackPoint as Point
import pandas as pd


class MyTestCase(unittest.TestCase):
    def test_reading(self):
        mongodbConnection = TrackInformationRepository('localhost', 27017)
        id_track = "activity_3905397717"
        data = mongodbConnection.get_trackinformation_dataframe(id_track)
        print(data)
        self.assertEqual(True, True)

    def test_writting(self):
        mongodbConnection = TrackInformationRepository('localhost', 27017)
        data = pd.DataFrame([[1, 2, 1, 2, 1248507104, 317813195],
                             [3, 4, 1, 2, 1248507104, 317813195],
                             [5, 6, 1, 2, 1248507105, 317813195],
                             [7, 8, 1, 2, 1248507104, 317813195],
                             [1, 2, 1, 2, 1248507106, 317813195],
                             [1, 2, 1, 2, 1248507104, 317813195]],
                            columns=['Point_X', 'Point_Y', 'Projection_X', 'Projection_Y', 'Origin', 'Target'])

        data = mongodbConnection.write_trackinformation_dataframe(data)
        print(data)
        self.assertEqual(True, False)

    def test_writting(self):
        mongodbConnection = TrackInformationRepository('localhost', 27017)
        data = pd.DataFrame([[1, 2, 1, 2, 1248507104, 317813195],
                             [3, 4, 1, 2, 1248507104, 317813195],
                             [5, 6, 1, 2, 1248507105, 317813195],
                             [7, 8, 1, 2, 1248507104, 317813195],
                             [1, 2, 1, 2, 1248507106, 317813195],
                             [1, 2, 1, 2, 1248507104, 317813195]],
                            columns=['Point_X', 'Point_Y', 'Projection_X', 'Projection_Y', 'Origin', 'Target'])
        data['id'] = 1
        cols = data.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        data = data[cols]
        data = mongodbConnection.write_trackinformation_dataframe(data)
        print(data)
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()