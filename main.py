#WIP
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():   
    # Pridobi IP naslov obiskovalca 
    if request.headers.get('X-Forwarded-For'): 
        ip = request.headers.get('X-Forwarded-For').split(',')[0] 
    else:
        ip = request.remote_addr  
        
    print(f"Debug IP: {ip}")  # Za debugging 
    
    ip = "8.8.8.8" 

    try:
        geo_response = requests.get(f"https://freeipapi.com/api/json/{ip}")
        geo_response.raise_for_status() 
        
        geo_data = geo_response.json()
        city = geo_data.get('cityName', 'Neznano mesto')
        
        return f"Vaš IP je {ip} in prihajate iz mesta: {city}."
        
    except requests.RequestException as e:
        return f"Prišlo je do napake pri API klicu: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)