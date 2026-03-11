#WIP
from flask import Flask, render_template, request
import requests
from tinydb import TinyDB, Query
app = Flask(__name__)
odb=TinyDB('obiskovalci.json')
WMO_CODE = {
    0: "Jasno",
    1: "Pretežno jasno", 2: "Delno oblačno", 3: "Oblačno",
    45: "Megla", 48: "Megla s slano",
    51: "Rahlo pršenje", 53: "Zmerno pršenje", 55: "Gosto pršenje",
    61: "Rahel dež", 63: "Zmeren dež", 65: "Močan dež",
    71: "Rahel sneg", 73: "Zmeren sneg", 75: "Močan sneg",
    95: "Nevihta", 96: "Nevihta s točo", 99: "Močna nevihta s točo"
}
@app.route('/')
def index():   
    # Pridobi IP naslov obiskovalca 
    if request.headers.get('X-Forwarded-For'): 
        ip = request.headers.get('X-Forwarded-For').split(',')[0] 
    else:
        ip = request.remote_addr     
    print(f"Debug IP: {ip}")  # Za debugging 
    #debugip
    geo_response = requests.get(f"https://freeipapi.com/api/json/{ip}") 
    geo_data = geo_response.json()
    country=geo_data.get('countryName')
    city = geo_data.get('cityName')
    lon=geo_data.get('longitude')
    lat=geo_data.get('latitude')
    api_key='61ea5bdda483dd02d99dfd5308d8264f'
    temp = None
    weatherdesc = None
    wind = None
    humidity = None
    precipitation = None
    if lat and lon:
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,precipitation,weather_code,wind_speed_10m,relative_humidity_2m"
        weather_res = requests.get(weather_url)
        
        if weather_res.status_code == 200:
            weather_data = weather_res.json()
            current = weather_data.get('current', {})
            
            temp = current.get('temperature_2m', temp)
            wind = current.get('wind_speed_10m', wind)
            humidity = current.get('relative_humidity_2m', humidity)
            precipitation = current.get('precipitation', precipitation)
            code = current.get('weather_code')
            if code is not None:
                weatherdesc = WMO_CODE.get(code, f"Neznana koda ({code})")
    odb.insert({
        'ip': ip, 'country': country, 'city': city, 'lon': lon, 'lat': lat, 
        'temp': temp, 'weatherdesc': weatherdesc
    })
    return render_template('index.html', ip=ip, country=country, city=city, temp=temp, weatherdesc=weatherdesc, wind=wind, humidity=humidity, precipitation=precipitation)
@app.route('/obiskovalci')
def obiski():
    vsi_obiskovalci = odb.all()
    return render_template('obiski.html', obiski=vsi_obiskovalci)
if __name__ == '__main__':
    app.run(debug=True)