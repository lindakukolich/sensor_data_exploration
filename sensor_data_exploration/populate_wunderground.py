import os

def populate():
    wu_data_source = add_data_source(
        name = "Weather Underground Thompson Island",
        access_info = "",
        latitude = None,
        longitude = None,
        elevation = None)

def add_data_source(name, access_info,latitude,longitude,elevation):
        d = DataSource.objects.get_or_create(name=name, access_info=access_info, latitude=latitude, longitude=longitude, elevation=elevation)[0]
        return d

# Start execution here!
if __name__ == '__main__':
    print "Starting Weather Underground population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sensor_data_exploration.settings')
    from sensor_data_exploration.apps.explorer.models import DataSource
    populate()
