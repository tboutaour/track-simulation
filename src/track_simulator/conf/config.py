import os

# MongoDB
MONGO_HOST = os.environ.get('MONGO_HOST')
MONGO_PORT = int(os.environ.get('MONGO_PORT'))
MONGO_DATABASE = os.environ.get('MONGO_DATABASE')
MONGO_GRAPH_INFORMATION_COLLECTION = os.environ.get('MONGO_GRAPH_INFORMATION_COLLECTION')
MONGO_TRACK_INFORMATION_COLLECTION = os.environ.get('MONGO_TRACK_INFORMATION_COLLECTION')
MONGO_TRACK_STATISTICS_COLLECTION = os.environ.get('MONGO_TRACK_STATISTICS_COLLECTION')
LAST_VERSION_GRAPH = os.environ.get('LAST_VERSION_GRAPH')

# Files directories
ROOT_DIRECTORY = os.environ.get('ROOT_DIRECTORY')
FILE_DIRECTORY = os.environ.get('FILE_DIRECTORY')
EXPORT_ANALYSIS_IMAGES_FOLDER = os.environ.get('EXPORT_ANALYSIS_IMAGES_FOLDER')
EXPORT_SIMULATIONS_GPX_FOLDER = os.environ.get('EXPORT_SIMULATIONS_GPX_FOLDER')
EXPORT_SIMULATIONS_IMAGES_FOLDER = os.environ.get('EXPORT_SIMULATIONS_IMAGES_FOLDER')

# Graph
NORTH_COMPONENT = float(os.environ.get('NORTH_COMPONENT'))
SOUTH_COMPONENT = float(os.environ.get('SOUTH_COMPONENT'))
EAST_COMPONENT = float(os.environ.get('EAST_COMPONENT'))
WEST_COMPONENT = float(os.environ.get('WEST_COMPONENT'))

# Static values
GENERATION_DISTANCE = float(os.environ.get('GENERATION_DISTANCE'))
DESTINATION_NODE_THRESHOLD = float(os.environ.get('DESTINATION_NODE_THRESHOLD'))
