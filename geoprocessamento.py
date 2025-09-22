from geopy.distance import geodesic

def calcular_distancia(coord1, coord2):
    return geodesic(coord1, coord2).kilometers

def locais_proximos(coord, locais, raio):
    proximos = []
    for local in locais:
        distancia = calcular_distancia(coord, (local['coordenadas']['latitude'], local['coordenadas']['longitude']))
        if distancia <= raio:
            proximos.append(local)
    return proximos