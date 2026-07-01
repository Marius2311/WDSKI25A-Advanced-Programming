"""Car class definition with a runnable consistency check.

``Car`` inherits the shared state and behaviour from :class:`Vehicle` and
adds passenger handling on top.

Run directly to execute the consistency checks:
    python car.py
"""

from __future__ import annotations

from vehicle import Vehicle


class Car(Vehicle):
    """A passenger car.

    Adds to :class:`Vehicle`:
        passenger_capacity: Number of seats for passengers (driver excluded).
        passengers: Current number of passengers on board.
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
        super().__init__(license_plate, horse_power, max_speed, price,
                         tank_capacity)
        if passenger_capacity < 0:
            raise ValueError("passenger_capacity must not be negative")
        self.passenger_capacity = passenger_capacity
        self.passengers: int = 0

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

    # --- Implementation of the Vehicle contract --------------------------

    def _specific_status_lines(self) -> list[str]:
        return [f"  Passengers: {self.passengers}/{self.passenger_capacity}"]


def _consistency_check() -> None:
    """Create instances and verify attributes behave correctly."""
    print("=== Car consistency check ===\n")

    golf = Car("M-AB 1234", horse_power=110, max_speed=200,
               price=28_500.0, passenger_capacity=4)
    tesla = Car("B-EV 9000", horse_power=480, max_speed=261,
                price=54_990.0, passenger_capacity=4, tank_capacity=65.0)

    print(golf, "\n")

    # Inherited behaviour: odometer accumulates across multiple calls.
    golf.track_km_driven(120)
    golf.track_km_driven(80.5)
    assert golf.km_driven == 200.5, golf.km_driven

    # Inherited behaviour: refuelling is capped at tank capacity.
    golf.fuel_vehicle(30)
    golf.fuel_vehicle(40)  # would be 70, but tank holds only 50
    assert golf.fuel_count == golf.tank_capacity == 50.0, golf.fuel_count

    # Car-specific: passengers respect capacity and never go negative.
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

    # Inherited washing toggles cleanliness independently per instance.
    golf.is_clean = False
    golf.wash()
    assert golf.is_clean is True
    assert tesla.is_clean is True  # instances are independent

    # It really is a Vehicle.
    assert isinstance(golf, Vehicle)

    print(golf, "\n")
    print("All Car checks passed.")


if __name__ == "__main__":
    _consistency_check()