#Import Files
import os
from google import genai
from google.genai import types
import find_info
import json
from datetime import datetime, timedelta

#API keys
os.environ["GEMINI_API_KEY"] = "AIzaSyBjQ3D6a7qbKopKrpwQKNSVFhdg11Ettnk"

#Upload GoogleGemini through Google Gemini Studio
client = genai.Client()


def gemini (user_request:str):
    '''
    This fuction take in user's description of their flight information and organize it
    so that the system can read and analyze the information
    '''

    #Variables
    noInfo = True   #If there's no flight at all
    cheapest_flight = {} 
    cheapest  = 1000000 #Set values to indicate possibility
    result = {} #Place holder variable

    #Train Google Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction="""
            You are a trip-planning extraction system. 
            Read the user's request and return ONLY raw JSON (no backticks, no code block, no commentary).

            Fields:
            - origin_city: string (city they are leaving from), else null
            - destination_city: string (city they want to go to)
            - origin_airport_code: 3-letter IATA airport code for origin (e.g. Toronto -> YYZ)
            - destination_airport_code: 3-letter IATA airport code for destination (e.g. New York -> JFK)
            - depart_window_start: earliest acceptable departure date, format "YYYY-MM-DD", else null
            - depart_window_end: latest acceptable departure date, format "YYYY-MM-DD", else null

            Rules:
            - If the user input have nothing to do with flight description, set destination_airport_code to null
            - otherwise ALWAYS include origin_airport_code and destination_airport_code using main international airports.
            - If the user sounds flexible like "anytime next weekend" or "sometime between Dec 2 and Dec 5", convert that to start/end dates.
            - Only output valid JSON. Do not wrap in ```json.
            """
        ),
            contents=user_request
    )

    #Clean Up Google Gemini Respond
    raw = response.text.strip()

    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw.split("```")[-2] if "```" in raw else raw
        raw = raw.replace("json", "", 1).strip()
    data = json.loads(raw)

    #Set location
    orgin = data.get("origin_airport_code")
    des = data.get("destination_airport_code")

    #Set if Statement incase prompt doesn't make sense
    if des == "null":
        return "Please input information about your flights"
    elif data.get("depart_window_start") == "null":
        return "Please input full information of your flight including your departure window"
    elif orgin == "null":
        return "Please input full information of your flight including your departure location"
    else:

        #Set and calculate how many days in departure window
        start_date = datetime(int(data.get("depart_window_start")[0:4]), int(data.get("depart_window_start")[5:7]),int(data.get("depart_window_start")[8:]))
        end_date = datetime(int(data.get("depart_window_end")[0:4]), int(data.get("depart_window_end")[5:7]),int(data.get("depart_window_end")[8:]))
        delta = end_date - start_date

        #Find cheapest flight per day within the departure window
        for i in range(delta.days+1):
            result = find_info.get_one_way_prices(orgin, des, int(start_date.day), int(start_date.month), int(start_date.year))
            
            #If no information is recieve
            if noInfo and result.get("Price") == 1000000:
                noInfo = True
            
            #Only note if the price is cheaper than previous
            elif int(result.get("Price")) < cheapest:
                noInfo = False #Information is recieve
                cheapest = int(result.get("Price"))
                cheapest_flight = result
            #Increase date
            start_date += timedelta(1)
        
        #Depends on the information, return accordingly
        if noInfo:
            return "There's no flight information for your requirement"
        else:
            #Call google Gemini to make writting more human
            ans = geminiFinal(str(cheapest_flight))
            return ans 

def geminiFinal (text):
    '''
    Make Writting more human
    '''
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction="""
            Take in information in JSON format of flights information and turn it into a more human output.
            Specifically put everything in a sentence
            """
        ),
            contents=text
    )
    final = response.text.strip()

    return final



#print(gemini("Flight ticket from toronto to regina, from october 30, 2025, to november 3, 2025"))