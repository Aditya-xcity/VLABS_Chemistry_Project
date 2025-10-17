# quick_test_fixed.py
import requests
import time

def test_reaction(el1, el2):
    url = f"http://127.0.0.1:5000/get_reaction?el1={el1}&el2={el2}"
    
    print(f"\n🧪 Testing: {el1} + {el2}")
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        print(f"   Status: {data['type']}")
        print(f"   Products: {data['products']}")
        return data['type'] != 'no_reaction'
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    print("🔬 VLABS Reaction Tester - FIXED VERSION")
    print("=" * 50)
    
    # Wait a bit for server to start
    time.sleep(2)
    
    # Test reactions that should work
    test_cases = [
        ("H", "O"),
        ("O", "H"),  # Reverse order
        ("Na", "Cl"),
        ("Cl", "Na"),  # Reverse order
        ("C", "O"),   # This might not be in your test data
        ("Zn", "O")   # This might not be in your test data
    ]
    
    success_count = 0
    for el1, el2 in test_cases:
        if test_reaction(el1, el2):
            success_count += 1
    
    print(f"\n📊 Test Results: {success_count}/{len(test_cases)} reactions successful")
    
    # Test debug endpoint
    print(f"\n🔍 Checking debug endpoint...")
    try:
        response = requests.get("http://127.0.0.1:5000/debug", timeout=10)
        debug_data = response.json()
        print(f"   Elements loaded: {debug_data['elements_count']}")
        print(f"   Reactions loaded: {debug_data['reactions_count']}")
        print(f"   Available reactions: {debug_data['reactions']}")
    except Exception as e:
        print(f"   ❌ Debug endpoint error: {e}")

if __name__ == "__main__":
    main()