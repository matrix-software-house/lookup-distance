app2_prompt



Scrivi una nuova versione di app.py e chiamala app2.py
Le richieste provengono da una web app che legge la posizione corrente dell'utente (lat e long), le invia a questo servizio e il servizio restiuisce la distanza della posizione da un punto di interesse (ad esempio un monumento presente in città).
Il sistema in precedenza usava le API di Google Maps per calcoalre distanza e tempo di percorrenza a piedi e abbiamo avuto degli abusi inattesi.
Per evitare gli abusi voglio adottare una nuova strategia.

Nuovo endpoint
/get_points
funziona se passo un token/secret (/get_points?secret=abcd1234) per evitare abusi
serve a ricaricare la lista dei punti di interesse (PdI), nel caso vengano aggiunti nuovi punti o eliminati.
Ottengo la lista dei punti di interesse interrogando servizio STRAPI: "curl -H "Authorization: Bearer abc123 https://strapi2.lookupferrara.it/api/points".
Memorizzo tale lista come:
[
    {'id': 34, 'lat': 45.196458, "lon": 9.145117},
    ...
]
Memorizzo lista in un file.


Endpoint /distance
/distance?origin=45.188642,9.145117&destination=45.196458,9.148310
Come nella precedente versione riceve in ingresso le coordinate (lat e long) di due punti:0 1: posizione dell'utente (origin), 2: posizione del PdI (destination) e restituisce un hash/mappa:
{"distance":1297,"duration":934, "id": 34} (distanza in metri e duration in secondi) e id del punto oppure {"more_than": 60}
Prima di rispondere verifica che la destination fornito sia un punto valido.
Se è valido calcola la distanza tra i due punti usando la formula di Haversine.
Se la distanza è maggiore di una certa soglia (es. 10 km), risponde {"more_than": 10} o {"more_than": 20} ecc. (a step di 10 km)
Se la distanza è minore o uguale a 10 km arrotonda la posizione origin (lat e lon) 4 decimali e verifica se non sia già presente nella cache { [lat1, lon1, lat2, lon2] => {"distance":1297, "duration":934, "id": 34}}, in caso positivo restituisce la valore corrispondente, in caso negativo viene interrogato il servizio con get_distance_with_... come in app.py. La risposta viene memorizzata in cache.
Memorizzo la cache in un file.



Endpoint /all_distances
/all_distances?origin=45.188642,9.145117
riceve in ingresso le coordinate (lat e long) della sola origine.
Restituisce una lista come la seguente con tutti i punti di interesse:
[
    {"id": 34, "distance": 1297, "duration": 934},
    {"id": 41, "more_than": 10},
    ...
]

