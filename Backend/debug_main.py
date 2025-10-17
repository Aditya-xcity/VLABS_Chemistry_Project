# quick_test.py
import requests
import time
import subprocess
import sys
import os

def start_server():
    """Start the Flask server"""
    print("🚀 Starting Flask server...")
    try:
        # Start the server in a subprocess
        server_process = subprocess.Popen([
            sys.executable, "Backend/main.py"
        ], cwd=os.getcwd())
        
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        time.sleep(3)
        return server_process
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return None

def test_reaction(el1, el2, el3=None):
    BASE_URL = "http://127.0.0.1:5000"
    
    if el3:
        url = f"{BASE_URL}/get_reaction?el1={el1}&el2={el2}&el3={el3}"
    else:
        url = f"{BASE_URL}/get_reaction?el1={el1}&el2={el2}"
    
    print(f"\n🧪 Testing: {el1} + {el2}" + (f" + {el3}" if el3 else ""))
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        print(f"✅ Status: {data['type']}")
        print(f"📦 Products: {data['products']}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - Server not running")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🔬 VLABS Reaction Tester")
    print("=" * 50)
    
    # Start the server
    server_process = start_server()
    if not server_process:
        print("❌ Could not start server. Please run manually: python Backend/main.py")
        return
    
    # Test reactions
    test_cases = [
        ("H", "O"),
        ("Na", "Cl"), 
        ("C", "O"),
        ("H", "O", "N"),
        ("Zn", "O")
    ]
    
    success_count = 0
    for case in test_cases:
        if len(case) == 2:
            success = test_reaction(case[0], case[1])
        else:
            success = test_reaction(case[0], case[1], case[2])
        
        if success:
            success_count += 1
    
    print(f"\n📊 Test Results: {success_count}/{len(test_cases)} reactions successful")
    
    # Stop the server
    if server_process:
        print("\n🛑 Stopping server...")
        server_process.terminate()

if __name__ == "__main__":
    main()