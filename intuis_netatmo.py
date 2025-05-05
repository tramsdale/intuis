import requests
import json
from typing import Dict, Optional, Union
from datetime import datetime

class IntuisNetatmo:
    def __init__(self, username: str, password: str, client_id: str, client_secret: str, base_url: str = "https://app.muller-intuitiv.net"):
        """
        Initialize the IntuisNetatmo client.
        
        Args:
            username (str): Your Intuis account username
            password (str): Your Intuis account password
            client_id (str): Your Intuis client ID
            client_secret (str): Your Intuis client secret
            base_url (str): Base URL for the Intuis API
        """
        self.base_url = base_url
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = requests.Session()
        self.token = None
        self.refresh_token = None
        self.token_expiry = None
        self.homesdata = None
        self.home_id = None
        self.home_name = None
        self.homestatus = None

    def _get_token(self) -> str:
        """
        Get or refresh the authentication token.
        
        Returns:
            str: Authentication token
        """
        if self.token and self.token_expiry and datetime.now().timestamp() < self.token_expiry:
            return self.token

        url = f"{self.base_url}/oauth2/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "password",
            "user_prefix": "muller",
            "scope": "read_muller write_muller",
            "username": self.username,
            "password": self.password
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = self.session.post(url, data=data, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        self.token = result.get("access_token")
        self.refresh_token = result.get("refresh_token")
        # Assuming token expires in 1 hour
        self.token_expiry = datetime.now().timestamp() + 3600
        
        return self.token

    def get_homesdata(self) -> Dict:
        """
        Get data about all homes associated with the account.
        
        Returns:
            Dict: Homes data and their information
        """
        token = self._get_token()
        url = f"{self.base_url}/api/homesdata"
        headers = {"Authorization": f"Bearer {token}"}
        
        response = self.session.get(url, headers=headers)
        response.raise_for_status()
        self.homesdata = response.json()
        self.home_id = self.homesdata["body"]["homes"][0]["id"]
        self.home_name = self.homesdata["body"]["homes"][0]["name"]
        
        return response.json()

    def get_homestatus(self) -> Dict:
        """
        Get current status of the home including rooms and modules.
        
        Returns:
            Dict: Home status information including rooms and modules
        """
        token = self._get_token()
        url2 = f"{self.base_url}/syncapi/v1/homestatus"
        url1 = f"{self.base_url}/syncapi/v1/getconfigs"
        headers = {"Authorization": f"Bearer {token}", 
                   "Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "home_id": self.home_id
        }
        print(headers)
        print(data)

        response = self.session.post(url1, headers=headers, data=data)
        response.raise_for_status()
        response = self.session.post(url2, headers=headers, data=data)
        response.raise_for_status()
        self.homestatus = response.json()
        
        return response.json()

    def get_home_measure(self, scale: str = "1hour", type: list[str] = ["sum_energy_elec$0","sum_energy_elec$1","sum_energy_elec$2"]) -> Dict:
        """
        Get measurements for the home.
        
        Args:
            scale (str): Time scale for measurements (e.g., "1hour", "1day", "1week")
            type (str): Types of measurements to retrieve, comma-separated
            
        Returns:
            Dict: Home measurements data
        """
        token = self._get_token()
        url = f"{self.base_url}/api/gethomemeasure"
        headers = {"Authorization": f"Bearer {token}", 
                   "Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "home_id": self.home_id,
            "scale": scale,
            "type": type
        }
        
        response = self.session.post(url, headers=headers, data=data)
        response.raise_for_status()
        
        return response.json()


    