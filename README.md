# IntuisNetatmo

A Python library for controlling Netatmo smart thermostats and water heaters through the Intuis API.

## Installation

```bash
pip install intuis-netatmo
```

## Usage

```python
from intuis_netatmo import IntuisNetatmo

# Initialize the client
client = IntuisNetatmo(client_id="your_client_id", client_secret="your_client_secret")

# Authenticate
client.authenticate()

# Get rooms and water heaters
rooms = client.get_rooms()
water_heaters = client.get_water_heaters()
```

## API Reference

### IntuisNetatmo Class


#### `do_init(username: Any, password: Any, client_id: Any, client_secret: Any, base_url: Any) -> None`


#### `get_home_measure(scale: str) -> None`

Get measurements for the home.


#### `get_homesdata() -> Dict`

Get data about all homes associated with the account.


#### `get_homestatus() -> Dict`

Get current status of the home including rooms and modules.


#### `get_room_id_by_name(room_name: str) -> str`

Look up a room's ID by its name.


#### `get_room_mode(room_id: str) -> Dict`

Get the current mode and settings for a room.


#### `get_room_setpoint(room_id: str) -> Dict`

Get the current temperature setpoint for a room.


#### `get_room_temperature(room_id: str) -> float`

Get the current measured temperature for a room.


#### `get_water_heater_mode(water_heater_id: str) -> str`

Get the current mode of a water heater.


#### `print_home_info() -> None`

Print information about the home including home name, ID and all rooms.


#### `pull_data() -> None`

Pull all initial data from the Intuis API, and setup internal structures


#### `set_room_hg(room_id: str) -> Dict`

Set a room to HG (Hors Gel/Frost Protection) mode with minimum temperature (7°C).


#### `set_room_mode(room_id: str, mode: str, temperature: float) -> Dict`

Set the mode for a room.


#### `set_room_off(room_id: str) -> Dict`

Set a room to off mode with minimum temperature (7°C frost protection).


#### `set_room_setpoint(room_id: str, temp: float, end_time: Optional) -> Dict`

Set a manual temperature setpoint for a specific room.


#### `set_water_heater_mode(water_heater_id: str, mode: str) -> Dict`

Set the mode of a water heater.


#### `write_debug_files() -> None`

Write homestatus and homesdata to debug JSON files.


#### `write_json_to_file(data: Dict, filename: str) -> None`

Write JSON data to a debug file.


### IntuisRoom Class


#### `add_module(module: dict) -> None`

Add an associated module to the room


#### `update_status(room_status: dict) -> None`

Update room status from API response


### IntuisWaterHeater Class


#### `update_status(heater_status: dict) -> None`

Update water heater status from API response

