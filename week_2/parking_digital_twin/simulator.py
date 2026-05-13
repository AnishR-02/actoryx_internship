from parking_spot import ParkingSpot


def test_parking_spot():
    spot = ParkingSpot(1)

    scenarios = {
        "Empty": {
            "FL": 0,
            "FR": 0,
            "RL": 0,
            "RR": 0
        },
        "Shopping Cart": {
            "FL": 20,
            "FR": 15,
            "RL": 10,
            "RR": 5
        },
        "Partial Car": {
            "FL": 250,
            "FR": 200,
            "RL": 0,
            "RR": 0
        },
        "Full Car": {
            "FL": 300,
            "FR": 320,
            "RL": 310,
            "RR": 290
        },
    }

    for name, sensor_data in scenarios.items():
        spot.sensors = sensor_data
        state = spot.evaluate_state()
        print(f"{name}: {sensor_data} -> {state}")  