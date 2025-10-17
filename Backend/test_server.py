# Backend/test_server.py
import requests
import time

def test_server():
    base_url = "http://127.0.0.1:5000"
    
    print("🔬 Testing VLABS Server...")
    print("=" * 50)
    
    # Test if server is running
    try:
        response = requests.get(f"{base_url}/debug", timeout=5)
        print("✅ Server is running!")
        debug_data = response.json()
        print(f"📊 Elements loaded: {debug_data['elements_loaded']}")
        print(f"📊 Reactions loaded: {debug_data['reactions_loaded']}")
        print(f"🔧 Available elements: {debug_data['available_elements']}")
        print(f"🔧 Available reactions: {debug_data['available_reactions']}")
    except Exception as e:
        print(f"❌ Server not running: {e}")
        print("💡 Please start the server first: python Backend/main.py")
        return
    
    # Test some reactions
    test_cases = [
        ("H", "O", "Should form Water"),
        ("Na", "Cl", "Should form Salt"),
        ("C", "O", "Should form CO₂ or CO"),
        ("N", "H", "Should form Ammonia"),
        ("X", "Y", "Should NOT form anything")
    ]
    
    print("\n Testing Reactions:")
    print("-" * 50)
    
    for el1, el2, description in test_cases:
        try:
            response = requests.get(f"{base_url}/get_reaction?el1={el1}&el2={el2}", timeout=5)
            data = response.json()
            
            print(f"\n{el1} + {el2}: {description}")
            if data["type"] == "no_reaction":
                print("   ❌ No reaction found")
            else:
                print(f"   ✅ REACTION FOUND!")
                print(f"   🧪 Formula: {data['products'][0]}")
                print(f"   📝 IUPAC: {data['products'][1]}")
                print(f"   🏷️ Common: {data['products'][2]}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_server()