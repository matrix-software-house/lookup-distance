

curl "https://distance.lookupferrara.it/distance?origin=45.188642,9.145117&destination=45.196458,9.148310"
curl "http://127.0.0.1:5001/distance?origin=45.188642,9.145117&destination=45.196458,9.148310"


9.145117,45.188642

Rispose
google maps
{"distance":1217,"duration":1027}

openroute
{"distance":1297.0,"duration":933.8}



## Nuovo app2.py

curl "http://localhost:5002/get_points?secret=nleFVkzP5RDYWodW3Bycu6cqRGddwKQV"


curl "http://127.0.0.1:5002/distance?origin=45.188642,9.145117&destination=45.196458,9.148310"
{
  "error": "Invalid destination point"
}

curl "http://localhost:5002/distance?origin=45.188642,9.145117&destination=44.8261762,11.6220539"
{
  "more_than": 200
}

curl "http://localhost:5002/distance?origin=44.8220125,11.6275&destination=44.8261762,11.6220539"
{
  "distance": 967,
  "duration": 782,
  "id": 94
}

curl "http://localhost:5002/all_distances?origin=44.8220125,11.6275"

[
  {
    "distance": 568,
    "duration": 470,
    "id": 86
  },
  {
    "distance": 1805,
    "duration": 1479,
    "id": 87
  },
  {
    "distance": 1746,
    "duration": 1431,
    "id": 92
  },
  {
    "distance": 967,
    "duration": 782,
    "id": 94
  },
  {
    "distance": 1505,
    "duration": 1229,
    "id": 97
  },


Gli stessi comandi eseguiti verso l'endopoint `https://distance2.lookupferrara.it/`


curl "https://distance2.lookupferrara.it/get_points?secret=nleFVkzP5RDYWodW3Bycu6cqRGddwKQV"
curl "https://distance2.lookupferrara.it/distance?origin=45.188642,9.145117&destination=45.196458,9.148310"
curl "https://distance2.lookupferrara.it/distance?origin=45.188642,9.145117&destination=44.8261762,11.6220539"
curl "https://distance2.lookupferrara.it/distance?origin=44.8220125,11.6275&destination=44.8261762,11.6220539"
curl "https://distance2.lookupferrara.it/all_distances?origin=44.8220125,11.6275"


