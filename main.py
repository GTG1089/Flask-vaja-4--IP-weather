#WIP
from flask import Flask, render_template, request
import requests
from tinydb import TinyDB, Query
app = Flask(__name__)
odb=TinyDB('obiskovalci.json')
@app.route('/')
def index():   
    # Pridobi IP naslov obiskovalca 
    if request.headers.get('X-Forwarded-For'): 
        ip = request.headers.get('X-Forwarded-For').split(',')[0] 
    else:
        ip = request.remote_addr  
        
    print(f"Debug IP: {ip}")  # Za debugging 
    #debugip
    ip="8.8.8.8"
    geo_response = requests.get(f"https://freeipapi.com/api/json/{ip}") 
    geo_data = geo_response.json()
    country=geo_data.get('countryName')
    city = geo_data.get('cityName')
    

    odb.insert({'ip':ip, 'country':country, 'city':city})
    return render_template(index.html, geo_response=geo_response, ip=ip, country=country, city=city)
    
    return f"Vaš IP je {ip} in prihajate iz mesta: {city}."
@app.route('/obiskovalci')
def obiski():
    vsi_obiskovalci = odb.all()
    return render_template(obiski.html, obiski=vsi_obiskovalci)
if __name__ == '__main__':
    app.run(debug=True)