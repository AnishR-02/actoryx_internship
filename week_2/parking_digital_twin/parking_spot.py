class ParkingSpot:
    def __init__(self, spot_id):
        self.spot_id = spot_id
        self.sensors = {
            "FL": 0,
            "FR": 0,
            "RL": 0,
            "RR": 0
        }
        self.state = "EMPTY"

    def total_weight(self):
        return sum(self.sensors.values())

    def evaluate_state(self):
        total = self.total_weight()

        active_sensors = sum(
            1 for weight in self.sensors.values() if weight > 50
        )

        # Empty spot
        if total < 50:
            self.state = "EMPTY"

        # Shopping cart / small object
        elif total < 300:
            self.state = "SHOPPING_CART"

        # Partial parking
        elif 300 <= total < 1000:
            self.state = "PARTIAL_PARKING"

        # Fully occupied
        elif total >= 1000:
            if active_sensors == 4:
                self.state = "OCCUPIED"
            else:
                self.state = "PARTIAL_PARKING"

        return self.state

    def get_weight_distribution(self):
        left_weight = self.sensors["FL"] + self.sensors["RL"]
        right_weight = self.sensors["FR"] + self.sensors["RR"]

        if left_weight > right_weight * 1.5:
            return "LEFT_HEAVY"
        elif right_weight > left_weight * 1.5:
            return "RIGHT_HEAVY"
        else:
            return "BALANCED"