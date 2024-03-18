import simconnect
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Initialize SimConnect
simconnect = simconnect.SimConnect()

# Define data structure for player position
class PlayerPositionDataStructure(simconnect.Structure):
    def __init__(self):
        self.latitude = None
        self.longitude = None

# Define callback function for receiving player position data
def player_position_callback(data, flags):
    player_position = PlayerPositionDataStructure.from_buffer(data)
    # Update player position on the map
    update_map(player_position.latitude, player_position.longitude)

# Create a Basemap instance
map = Basemap(projection='merc', lat_0=0, lon_0=0, resolution='l', llcrnrlon=-180, llcrnrlat=-90, urcrnrlon=180, urcrnrlat=90)

# Create a figure and axes
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111)

# Draw coastlines, countries, and states
map.drawcoastlines()
map.drawcountries()
map.drawstates()

# Initialize lists to store player positions
player_lats = []
player_lons = []

# Update map function
def update_map(latitude, longitude):
    player_lats.append(latitude)
    player_lons.append(longitude)
    x, y = map(player_lons, player_lats)
    ax.plot(x, y, 'ro', markersize=6)

# Register data definition for player position
simconnect.add_to_data_definition(PlayerPositionDataStructure, "PLANE LATITUDE", "degrees")
simconnect.add_to_data_definition(PlayerPositionDataStructure, "PLANE LONGITUDE", "degrees")

# Request data on player position
simconnect.request_data_on_sim_object(1, "PLANE LATITUDE", simconnect.SIMCONNECT_OBJECT_ID_USER, simconnect.SIMCONNECT_PERIOD_VISUAL_FRAME)

# Register event handler for player position update
simconnect.subscribe_to_system_event(1, "SimStart", player_position_callback)

# Show the map
plt.title("Online Players Map")
plt.show()
