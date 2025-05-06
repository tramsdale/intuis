#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path
from intuis_netatmo import IntuisNetatmo
from typing import Optional, Dict

def get_credentials(secrets_file: str = "secrets.json") -> tuple[str, str, str, str]:
    """
    Get credentials from secrets file.
    
    Args:
        secrets_file (str): Path to the secrets file
        
    Returns:
        tuple: (username, password, client_id, client_secret)
        
    Raises:
        FileNotFoundError: If secrets file doesn't exist
        KeyError: If required fields are missing
    """
    secrets_path = Path(secrets_file)
    if not secrets_path.exists():
        raise FileNotFoundError(
            f"Secrets file not found at {secrets_path.absolute()}. "
            "Please create a secrets.json file with username and password."
        )
    
    with open(secrets_path) as f:
        secrets = json.load(f)
    
    if "username" not in secrets or "password" not in secrets or "client_id" not in secrets or "client_secret" not in secrets:
        raise KeyError("Secrets file must contain all required fields")
    
    return secrets["username"], secrets["password"], secrets["client_id"], secrets["client_secret"]


def get_homes_data(client: IntuisNetatmo) -> None:
    """
    Get and display homes data.
    """
    try:
        homes_data = client.get_homesdata()
        print("\nHomes Data:")
        print(f"  Home ID: {client.home_id}")
        print(f"  Home Name: {client.home_name}")
        print(f"Room data:")
        for room in homes_data["body"]["homes"][0]["rooms"]:
            print(f"  Room ID: {room['id']}")
            print(f"    Room Name: {room['name']}")
            print(f"    Room Type: {room['type']}")
        print(f"Module data:")
        for module in homes_data["body"]["homes"][0]["modules"]:
            print(f"    Module ID: {module['id']}")
            try:
                print(f"      Module Name: {module['name']}")
            except:
                pass
            print(f"      Module Type: {module['type']}")
            
    except Exception as e:
        print(f"Error getting homes data: {str(e)}")

def get_home_status_summary(client: IntuisNetatmo) -> None:
    """
    Display a summary of home status including room temperatures, modes, and energy consumption.
    """
    try:
        client.get_homesdata()
        home_status = client.get_homestatus()
        print("\nHome Status Summary:")
        print("=" * 80)
        
        # Get room information from homesdata
        rooms = {room['id']: room['name'] for room in client.homesdata["body"]["homes"][0]["rooms"]}
        
        # Process each room
        for room_id, room_name in rooms.items():
            print(f"\nRoom: {room_name}")
            print("-" * 40)
            
            # Find room status
            room_status = next((room for room in home_status["body"]["home"]["rooms"] if room["id"] == room_id), None)
            if room_status:
                print(f"  Current Temperature: {room_status.get('therm_measured_temperature', 'N/A')}°C")
                print(f"  Target Temperature: {room_status.get('therm_setpoint_temperature', 'N/A')}°C")
                print(f"  Mode: {room_status.get('therm_setpoint_mode', 'N/A')}")
                print(f"  Heating Status: {room_status.get('heating_power_request', 'N/A')}")
                
                # Calculate energy consumption if available
                if 'energy' in room_status:
                    print(f"  Energy Consumption: {room_status['energy']} kWh")
                else:
                    print("  Energy Consumption: N/A")
            
            # Find associated modules
            modules = [m for m in home_status["body"]["home"]["modules"] if m.get("room_id") == room_id]
            if modules:
                print("\n  Associated Modules:")
                for module in modules:
                    print(f"    - {module.get('name', 'Unknown')} ({module.get('type', 'Unknown')})")
                    if 'battery_percent' in module:
                        print(f"      Battery: {module['battery_percent']}%")
                    if 'rf_status' in module:
                        print(f"      RF Status: {module['rf_status']}")
            
            print("-" * 40)
            
    except Exception as e:
        print(f"Error getting home status summary: {str(e)}")

def get_homes_measure(client: IntuisNetatmo) -> None:
    """
    Get and display home measurements.
    """
    try:
        client.get_homesdata()
        measurements = client.get_home_measure()
        print("\nHome Measurements:")
        print("=" * 80)
        print(json.dumps(measurements, indent=2))
    except Exception as e:
        print(f"Error getting home measurements: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Intuis Netatmo CLI')
    parser.add_argument('--device', '-d', help='Device ID to get details for')
    parser.add_argument('--list', '-l', action='store_true', help='List all available devices')
    parser.add_argument('--homes', action='store_true', help='Get homes data')
    parser.add_argument('--status', action='store_true', help='Get home status summary')
    parser.add_argument('--measure', action='store_true', help='Get home measurements')
    parser.add_argument('--secrets', '-s', default='secrets.json', help='Path to secrets file (default: secrets.json)')
    
    args = parser.parse_args()
    
    if not args.list and not args.device and not args.homes and not args.status and not args.measure:
        parser.print_help()
        return
    
    try:
        username, password, client_id, client_secret = get_credentials(args.secrets)
        client = IntuisNetatmo(username=username, password=password, client_id=client_id, client_secret=client_secret)
        
        if args.homes:
            get_homes_data(client)
            
        if args.status:
            get_home_status_summary(client)
            
        if args.measure:
            get_homes_measure(client)
        
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        print("\nPlease create a secrets.json file with the following format:")
        print('''{
    "username": "your_username",
    "password": "your_password",
    "client_id": "your_client_id",
    "client_secret": "your_client_secret"
}''')
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main() 