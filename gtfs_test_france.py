import zipfile
import csv

# Décompresser le fichier ZIP
file_path = 'C:\\Users\\alima\\OneDrive\\Desktop\\Moi\\Code\\GTFS\\sample_gtfs.zip'
with zipfile.ZipFile(file_path, 'r') as gtfs_zip:
    gtfs_zip.extractall('gtfs_data')  

# Charger les données des fichiers `stops.txt` et `stop_times.txt`
stops = {}
with open('gtfs_data/stops.txt', mode='r', encoding='utf-8') as stops_file:
    reader = csv.DictReader(stops_file)
    for row in reader:
        stops[row['stop_id']] = row['stop_name']

stop_times = []
with open('gtfs_data/stop_times.txt', mode='r', encoding='utf-8') as stop_times_file:
    reader = csv.DictReader(stop_times_file)
    for row in reader:
        stop_times.append(row)

# Rechercher les arrêts desservis par un trip donné
def get_stops_for_trip(trip_id):
    # Filtrer les lignes de stop_times correspondant au trip_id
    stops_for_trip = [row for row in stop_times if row['trip_id'] == trip_id]
    # Trier par ordre de passage
    stops_for_trip.sort(key=lambda x: int(x['stop_sequence']))
    return [stops[stop['stop_id']] for stop in stops_for_trip]


trip_id = 'OCESN003116F3903918858' # Exemple de trip_id --Gare de Le Havre--, --Gare de Rouen-Rive-Droite--, --Gare de Paris-St-Lazare--
try:
    stops_names = get_stops_for_trip(trip_id)
    print(f"Les arrêts desservis pour le trip {trip_id} sont :")
    for stop_name in stops_names:
        print(f"- {stop_name}") # Afficher les arrêts desservis
except KeyError:
    print(f"Erreur : trip_id '{trip_id}' ou stop_id correspondant introuvable.")
