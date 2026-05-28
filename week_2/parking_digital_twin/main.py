from simulator import test_parking_spot
from parking_lot import ParkingLot


def main():
    # Run basic parking spot test scenarios
    test_parking_spot()

    print("\n==============================")
    print("DIGITAL TWIN: PARKING LOT SIMULATION")
    print("==============================")

    # Create parking lot with 20 spots
    parking_lot = ParkingLot(total_spots=20)

    # Generate simulated sensor states
    parking_lot.simulate_random_state()

    # Display parking lot state
    parking_lot.display_parking_lot()


if __name__ == "__main__":
    main()