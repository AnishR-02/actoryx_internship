import random
from parking_spot import ParkingSpot


class ParkingLot:
    def __init__(self, total_spots=20):
        self.spots = [ParkingSpot(i + 1) for i in range(total_spots)]

    def simulate_random_state(self):
        for spot in self.spots:
            scenario = random.choice([
                "EMPTY",
                "SHOPPING_CART",
                "PARTIAL_PARKING",
                "OCCUPIED"
            ])

            # Empty
            if scenario == "EMPTY":
                spot.sensors = {
                    "FL": 0,
                    "FR": 0,
                    "RL": 0,
                    "RR": 0
                }

            # Shopping cart / light obstruction
            elif scenario == "SHOPPING_CART":
                spot.sensors = {
                    "FL": random.randint(10, 60),
                    "FR": random.randint(5, 40),
                    "RL": random.randint(0, 20),
                    "RR": random.randint(0, 20)
                }

            # Partial parking
            elif scenario == "PARTIAL_PARKING":
                partial_type = random.choice([
                    "FRONT_ONLY",
                    "REAR_ONLY",
                    "LEFT_SIDE",
                    "RIGHT_SIDE"
                ])

                if partial_type == "FRONT_ONLY":
                    spot.sensors = {
                        "FL": random.randint(180, 350),
                        "FR": random.randint(180, 350),
                        "RL": random.randint(0, 40),
                        "RR": random.randint(0, 40)
                    }

                elif partial_type == "REAR_ONLY":
                    spot.sensors = {
                        "FL": random.randint(0, 40),
                        "FR": random.randint(0, 40),
                        "RL": random.randint(180, 350),
                        "RR": random.randint(180, 350)
                    }

                elif partial_type == "LEFT_SIDE":
                    spot.sensors = {
                        "FL": random.randint(180, 350),
                        "FR": random.randint(0, 40),
                        "RL": random.randint(180, 350),
                        "RR": random.randint(0, 40)
                    }

                elif partial_type == "RIGHT_SIDE":
                    spot.sensors = {
                        "FL": random.randint(0, 40),
                        "FR": random.randint(180, 350),
                        "RL": random.randint(0, 40),
                        "RR": random.randint(180, 350)
                    }

            # Fully occupied
            elif scenario == "OCCUPIED":
                spot.sensors = {
                    "FL": random.randint(250, 400),
                    "FR": random.randint(250, 400),
                    "RL": random.randint(250, 400),
                    "RR": random.randint(250, 400)
                }

            spot.evaluate_state()

        self.detect_double_parking()

    def display_parking_lot(self):
        state_counts = {
            "EMPTY": 0,
            "SHOPPING_CART": 0,
            "PARTIAL_PARKING": 0,
            "OCCUPIED": 0,
            "DOUBLE_PARKED": 0
        }

        print("\n--- PARKING LOT STATUS ---")

        for spot in self.spots:
            print(
                f"Spot {spot.spot_id}: "
                f"{spot.state} | Sensors: {spot.sensors}"
            )

            if spot.state in state_counts:
                state_counts[spot.state] += 1

        print("\n--- SUMMARY ---")
        print(f"Total Spots: {len(self.spots)}")
        print(f"Empty: {state_counts['EMPTY']}")
        print(f"Shopping Cart: {state_counts['SHOPPING_CART']}")
        print(f"Partial Parking: {state_counts['PARTIAL_PARKING']}")
        print(f"Occupied: {state_counts['OCCUPIED']}")
        print(f"Double Parked: {state_counts['DOUBLE_PARKED']}")

    def detect_double_parking(self):
        for i in range(len(self.spots) - 1):
            current_spot = self.spots[i]
            next_spot = self.spots[i + 1]

            if (
                current_spot.state == "PARTIAL_PARKING"
                and next_spot.state == "PARTIAL_PARKING"
            ):
                current_distribution = current_spot.get_weight_distribution()
                next_distribution = next_spot.get_weight_distribution()

                if (
                    current_distribution == "RIGHT_HEAVY"
                    and next_distribution == "LEFT_HEAVY"
                ):
                    current_spot.state = "DOUBLE_PARKED"
                    next_spot.state = "DOUBLE_PARKED"   