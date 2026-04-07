import sys
from datetime import datetime, timedelta
from fast_flights import FlightData, get_flights, Passengers

def test_raw_api():
    print("=== DEBUGGING FAST_FLIGHTS API ===")
    
    # 1. Khởi tạo dữ liệu
    target_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    from_code = "HAN"
    to_code = "SGN"
    
    print(f"Testing: {from_code} -> {to_code} on {target_date}")
    
    try:
        passengers = Passengers(adults=1, children=0, infants_in_seat=0, infants_on_lap=0)
        fd = FlightData(date=target_date, from_airport=from_code, to_airport=to_code)
        
        print("Calling get_flights...")
        result = get_flights(
            flight_data=[fd], 
            trip='one-way', 
            passengers=passengers, 
            seat='economy',
            fetch_mode='common'
        )
        
        print("API Call finished.")
        if result and result.flights:
            print(f"Success! Found {len(result.flights)} flights.")
            for f in result.flights[:2]:
                print(f" - {f.name}: {f.departure} -> {f.arrival} | {f.price} VND")
        else:
            print("No flights found in result.")
            
    except Exception as e:
        print("\n!!! ERROR DETECTED !!!")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_raw_api()
