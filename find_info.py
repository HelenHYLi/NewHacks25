#import files
import requests
import json

#API keys
SERPAPI_KEY = "dc8dab92c68bd5f634e2ad1581f6a818296207ed0ac7c6f7efe41184d0778996"

def get_one_way_prices(origin_code, dest_code, day, month, year):
    """
    Ask SerpAPI (google_flights engine) for flight options on a single date.
    origin_code: "YYZ"
    dest_code: "JFK"
    date_str: "2025-12-03"  (YYYY-MM-DD)
    Returns: list of {price, airline, depart_time, arrival_time} dicts
    """
    url = "https://serpapi.com/search?engine=google_flights"

    #Add '0' to days for it be able to work
    day_str = ""
    if day < 10:
        day_str = "0"+str(day)
    else:
        day_str = str(day)
    
    #Set date to format (YYYY-MM-DD)
    date_str = str(year) + "-" + str(month) + "-" + day_str

    #Parameters of SerpApi
    params = {
        "engine": "google_flights",
        "departure_id": origin_code,
        "arrival_id": dest_code,
        "outbound_date": date_str,
        "type" : 2, #Single trip only
        "currency": "CAD",
        "api_key": SERPAPI_KEY,
    }

    #Request access
    res = requests.get(url, params=params)
    data = res.json()

    #Variables
    layover = 0 
    NOLAYOVER = 0
    info = {}
    flights_out = {}
    cheapest_flight = 0

    #If no information is recieves, return
    if data.get("best_flights") == None:
        return {"Price" : 1000000}

    cheapest_flight = data['price_insights']['lowest_price'] #Find lowest price

    # Try to read best_flights first, if found, add it to the variable
    for f in data["best_flights"]:
        if f["price"] == cheapest_flight:
            flights_out = f

    #If best_flights is not found, check other_flights
    if flights_out == {}:
        for f in data["other_flights"]:
            if f["price"] == cheapest_flight:
                flights_out = f

    #Different format for layover
    if "layovers" in flights_out:
        layover = len(flights_out["layovers"]) #Check amoung of layover

    if layover == NOLAYOVER:
        #Return this format if there's no layover
        info = {'Departure airport': flights_out.get("flights")[0].get('departure_airport').get("name"), 
                'Departure Airport ID':flights_out.get("flights")[0].get("departure_airport").get("id"), 
                'Departure Time': flights_out.get("flights")[0].get("departure_airport").get("time"), 
                'Arrival Aiport': flights_out.get("flights")[0].get("arrival_airport").get("name"), 
                'Arrival Airport ID': flights_out.get("flights")[0].get("arrival_airport").get("id"), 
                'Airline': flights_out.get("flights")[0].get("airline"),'Price': flights_out.get("price")}
        
    else:
        #Return this format if there's layovers
        info = {"Number of flights": layover+1}
        for i in range(layover+1):

            #Fix the description
            a = "Departure airport of Flight " + str(i+1)
            b = "Departure Airport ID of Flight " +str(i+1)
            c = "Departure Time of Flight " + str(i+1)
            d = "Arrival Aiport of Flight " + str(i+1)
            e = "Arrival Airport ID of Flight " +str(i+1)
            f = "Airline of Flight " + str(i+1)

            info.update({a: flights_out.get("flights")[i].get("departure_airport").get("name"), 
                b: flights_out.get("flights")[i].get("departure_airport").get("id"), 
                c: flights_out.get("flights")[i].get("departure_airport").get("time"), 
                d: flights_out.get("flights")[i].get("arrival_airport").get("name"), 
                e: flights_out.get("flights")[i].get("arrival_airport").get("id"), 
                f: flights_out.get("flights")[i].get("airline")})
            
        info.update({"Price": flights_out.get("price")})

    #Return cheapest flight option
    return info