import zipfile
import csv
import os
import requests

"""
# Télécharger un fichier GTFS d'exemple
url = "https://github.com/google/transit/raw/master/gtfs/spec/en/examples/sample-feed-1.zip"
file_path = "sample_gtfs.zip"

print("Téléchargement du fichier GTFS d'exemple...")
response = requests.get(url)

if response.status_code == 200:
    with open(file_path, "wb") as f:
        f.write(response.content)
    print("Fichier GTFS téléchargé avec succès.")
else:
    print(f"Erreur lors du téléchargement : {response.status_code}")
    exit()

# Vérifiez si le fichier est un ZIP valide
if zipfile.is_zipfile(file_path):
    print("Le fichier est un fichier ZIP valide.")
    with zipfile.ZipFile(file_path, "r") as gtfs_zip:
        gtfs_zip.extractall('gtfs_data')
    print("Fichier GTFS décompressé avec succès.")
else:
    print("Erreur : le fichier téléchargé n'est pas un fichier ZIP valide.")
    exit()
"""

# Charger les données des fichiers `stops.txt` et `stop_times.txt`
stops = {}
with open(os.path.join("gtfs_data", "stops.txt"), mode="r", encoding="utf-8") as stops_file:
    reader = csv.DictReader(stops_file)
    for row in reader:
        stops[row["stop_id"]] = row["stop_name"]

stop_times = []
with open(os.path.join("gtfs_data", "stop_times.txt"), mode="r", encoding="utf-8") as stop_times_file:
    reader = csv.DictReader(stop_times_file)
    for row in reader:
        stop_times.append(row)

# Rechercher les arrêts desservis par un trip donné
def get_stops_for_trip(trip_id):
    # Filtrer les lignes de stop_times correspondant au trip_id
    stops_for_trip = [row for row in stop_times if row["trip_id"] == trip_id]
    # Trier par ordre de passage
    stops_for_trip.sort(key=lambda x: int(x["stop_sequence"]))
    return [stops[stop["stop_id"]] for stop in stops_for_trip]

# Exemple d'utilisation
trip_id = "AAMV3"
try:
    stops_names = get_stops_for_trip(trip_id)
    print(f"Les arrêts desservis pour le trip {trip_id} sont :")
    for stop_name in stops_names:
        print(f"- {stop_name}")
except KeyError:
    print(f"Erreur : trip_id '{trip_id}' ou stop_id correspondant introuvable.")
