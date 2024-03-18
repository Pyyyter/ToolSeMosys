from Scripts.Capacity_VIS import visualization_CAP
from Scripts.Emission_VIS import visualization_EMI
from Scripts.Energy_VIS import visualization_ENER
from Scripts.Landuse_VIS import visualization_LAND
from Scripts.Visualization_server import visualization_Server
from Scripts.Dashboard import dashboard

def visualization():

    visualization_CAP()
    visualization_EMI()
    visualization_ENER()
    visualization_LAND()
    dashboard()
    visualization_Server()