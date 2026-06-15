"""Car class definition with a runnable consistency check.

Run directly to execute the consistency checks:
    python car.py
"""


class Car:
    """A passenger car.

    Attributes:
        license_plate: Official registration plate, e.g. "M-AB 1234".
        horse_power: Engine power in metric horsepower (PS).
        max_speed: Top speed in km/h.
        price: Purchase price in euro.
        passenger_capacity: Number of seats available for passengers
            (driver excluded). Class-specific attribute.
        fuel_count: Current fuel level in litres (managed by methods).
        tank_capacity: Maximum fuel the tank can hold in litres.
        km_driven: Total kilometres driven (odometer, managed by methods).
        is_clean: Whether the car is currently clean.
        passengers: Current number of passengers on board. Class-specific.
    """

    def __init__(
        self,
        license_plate: str,
        horse_power: int,
        max_speed: int,
        price: float,
        passenger_capacity: int,
        tank_capacity: float = 50.0,
    ) -> None:
        if horse_power <= 0:
            raise ValueError("horse_power must be positive")
        if max_speed <= 0:
            raise ValueError("max_speed must be positive")
        if price < 0:
            raise ValueError("price must not be negative")
        if passenger_capacity < 0:
            raise ValueError("passenger_capacity must not be negative")
        if tank_capacity <= 0:
            raise ValueError("tank_capacity must be positive")

        self.license_plate = license_plate
        self.horse_power = horse_power
        self.max_speed = max_speed
        self.price = price
        self.passenger_capacity = passenger_capacity
        self.tank_capacity = tank_capacity

        # State managed by methods.
        self.fuel_count: float = 0.0
        self.km_driven: float = 0.0
        self.is_clean: bool = True
        self.passengers: int = 0

    # --- Methods every vehicle needs -------------------------------------

    def track_km_driven(self, km: float) -> float:
        """Add driven kilometres to the odometer and return the new total."""
        if km < 0:
            raise ValueError("km must not be negative")
        self.km_driven += km
        return self.km_driven

    def fuel_vehicle(self, litres: float) -> float:
        """Add fuel without exceeding the tank capacity.

        Returns the new fuel level in litres.
        """
        if litres < 0:
            raise ValueError("litres must not be negative")
        self.fuel_count = min(self.fuel_count + litres, self.tank_capacity)
        return self.fuel_count

    def wash(self) -> None:
        """Clean the car."""
        self.is_clean = True

    # --- Car-specific methods --------------------------------------------

    def add_passenger(self, count: int = 1) -> int:
        """Add passengers without exceeding the passenger capacity.

        Returns the new passenger count.
        """
        if count <= 0:
            raise ValueError("count must be positive")
        if self.passengers + count > self.passenger_capacity:
            raise ValueError(
                f"Cannot add {count} passenger(s): capacity is "
                f"{self.passenger_capacity}, currently {self.passengers}."
            )
        self.passengers += count
        return self.passengers

    def remove_passenger(self, count: int = 1) -> int:
        """Remove passengers without dropping below zero.

        Returns the new passenger count.
        """
        if count <= 0:
            raise ValueError("count must be positive")
        if count > self.passengers:
            raise ValueError(
                f"Cannot remove {count} passenger(s): only "
                f"{self.passengers} on board."
            )
        self.passengers -= count
        return self.passengers

    def __str__(self) -> str:
        return (
            f"Car [{self.license_plate}] — {self.horse_power} PS, "
            f"max {self.max_speed} km/h, {self.price:.2f} €\n"
            f"  Passengers: {self.passengers}/{self.passenger_capacity}\n"
            f"  Fuel: {self.fuel_count:.1f}/{self.tank_capacity:.1f} L\n"
            f"  Odometer: {self.km_driven:.1f} km\n"
            f"  Clean: {'yes' if self.is_clean else 'no'}"
        )


def _consistency_check() -> None:
    """Create instances and verify attributes behave correctly."""
    print("=== Car consistency check ===\n")

    golf = Car("M-AB 1234", horse_power=110, max_speed=200,
               price=28_500.0, passenger_capacity=4)
    tesla = Car("B-EV 9000", horse_power=480, max_speed=261,
                price=54_990.0, passenger_capacity=4, tank_capacity=0.001)

    print(golf, "\n")

    # Odometer accumulates across multiple calls.
    golf.track_km_driven(120)
    golf.track_km_driven(80.5)
    assert golf.km_driven == 200.5, golf.km_driven

    # Refuelling is capped at tank capacity.
    golf.fuel_vehicle(30)
    golf.fuel_vehicle(40)  # would be 70, but tank holds only 50
    assert golf.fuel_count == golf.tank_capacity == 50.0, golf.fuel_count

    # Passengers respect capacity and never go negative.
    golf.add_passenger(2)
    golf.add_passenger()
    assert golf.passengers == 3, golf.passengers
    golf.remove_passenger(3)
    assert golf.passengers == 0, golf.passengers

    # Capacity violations raise.
    try:
        golf.add_passenger(99)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for over-capacity")

    # Washing toggles cleanliness independently per instance.
    golf.is_clean = False
    golf.wash()
    assert golf.is_clean is True
    assert tesla.is_clean is True  # instances are independent

    print(golf, "\n")
    print("All Car checks passed.")


if __name__ == "__main__":
    _consistency_check()