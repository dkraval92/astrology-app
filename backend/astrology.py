import swisseph as swe
from geopy.geocoders import Nominatim
from datetime import datetime

geolocator = Nominatim(user_agent="astro_app_v1")

PLANETS = {
    0: "Sun", 1: "Moon", 2: "Mercury", 3: "Venus", 
    4: "Mars", 5: "Jupiter", 6: "Saturn", 11: "Rahu", 12: "Ketu"
}

ZODIAC = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

def get_lat_lon(city_name):
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    return 28.6139, 77.2090

def calculate_chart(dob_str, tob_str, lat, lon):
    dt = datetime.strptime(f"{dob_str} {tob_str}", "%Y-%m-%d %H:%M")
    year, month, day = dt.year, dt.month, dt.day
    hour = dt.hour + (dt.minute / 60.0) - 5.5 
    
    jd = swe.julday(year, month, day, hour)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    houses, ascmc = swe.houses_ex(jd, lat, lon, b'P', flags=swe.FLG_SIDEREAL)
    ascendant_degree = ascmc[0]
    ascendant_sign = int(ascendant_degree / 30)
    
    planets_data = []
    
    for swe_id, name in PLANETS.items():
        pos, ret = swe.calc_ut(jd, swe_id, swe.FLG_SIDEREAL)
        longitude = pos[0]
        sign_idx = int(longitude / 30)
        degree = longitude % 30
        is_retrograde = pos[3] < 0
        house_num = ((sign_idx - ascendant_sign) % 12) + 1
        
        planets_data.append({
            "name": name,
            "sign": ZODIAC[sign_idx],
            "sign_id": sign_idx + 1,
            "degree": round(degree, 2),
            "house": house_num,
            "is_retrograde": is_retrograde
        })
        
    return {
        "ascendant_sign": ascendant_sign + 1,
        "ascendant_name": ZODIAC[ascendant_sign],
        "planets": planets_data
    }
