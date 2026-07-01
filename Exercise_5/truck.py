"""Truck class definition with a runnable consistency check.

``Truck`` inherits the shared state and behaviour from :class:`Vehicle`
and adds cargo handling.

Run directly to execute the consistency checks:
    python truck.py
"""

from __future__ import annotations

from vehicle import Vehicle


class Truck(Vehicle):
    """A cargo truck.

    Adds to :class:`Vehicle`:
        cargo_capacity: Maximum payload in kilograms.
        axle_count: Number of axles.
        cargo_load: Current load in kilograms.
    """

    def __init__(
        self,
        license_plate: str,
        horse_power: int,
        max_speed: int,
        price: float,
        cargo_capacity: float,
        axle_count: int = 2,
        tank_capacity: float = 400.0,
    ) -> None:
        super().__init__(license_plate, horse_power, max_speed, price,
                         tank_capacity)
        if cargo_capacity <= 0:
            raise ValueError("cargo_capacity must be positive")
        if axle_count < 2:
            raise ValueError("axle_count must be at least 2")
        self.cargo_capacity = cargo_capacity
        self.axle_count = axle_count
        self.cargo_load: float = 0.0

    # --- Truck-specific methods ------------------------------------------

    def load_truck(self, kg: float) -> float:
        """Load cargo without exceeding the cargo capacity.

        Returns the new cargo load in kilograms.
        """
        if kg <= 0:
            raise ValueError("kg must be positive")
        if self.cargo_load + kg > self.cargo_capacity:
            raise ValueError(
                f"Cannot load {kg} kg: capacity is {self.cargo_capacity} kg, "
                f"currently loaded {self.cargo_load} kg."
            )
        self.cargo_load += kg
        return self.cargo_load

    def unload_truck(self, kg: float | None = None) -> float:
        """Unload cargo. With no argument the truck is fully unloaded.

        Returns the new cargo load in kilograms.
        """
        if kg is None:
            self.cargo_load = 0.0
            return self.cargo_load
        if kg <= 0:
            raise ValueError("kg must be positive")
        if kg > self.cargo_load:
            raise ValueError(
                f"Cannot unload {kg} kg: only {self.cargo_load} kg loaded."
            )
        self.cargo_load -= kg
        return self.cargo_load

    def remaining_capacity(self) -> float:
        """Return how much more cargo can be loaded, in kilograms."""
        return self.cargo_capacity - self.cargo_load

    # --- Implementation of the Vehicle contract --------------------------

    def _specific_status_lines(self) -> list[str]:
        return [
            f"  Axles: {self.axle_count}",
            f"  Cargo: {self.cargo_load:.1f}/{self.cargo_capacity:.1f} kg",
        ]


def _consistency_check() -> None:
    """Create instances and verify attributes behave correctly."""
    print("=== Truck consistency check ===\n")

    man = Truck("HH-TR 770", horse_power=460, max_speed=90,
                price=120_000.0, cargo_capacity=18_000, axle_count=3)
    volvo = Truck("K-LV 11", horse_power=540, max_speed=100,
                  price=145_000.0, cargo_capacity=25_000, axle_count=4)

    print(man, "\n")

    # Inherited behaviour: odometer accumulates across multiple calls.
    man.track_km_driven(300)
    man.track_km_driven(150.25)
    assert man.km_driven == 450.25, man.km_driven

    # Inherited behaviour: refuelling is capped at tank capacity.
    man.fuel_vehicle(250)
    man.fuel_vehicle(250)  # would be 500, but tank holds only 400
    assert man.fuel_count == man.tank_capacity == 400.0, man.fuel_count

    # Truck-specific: loading respects capacity; remaining stays consistent.
    man.load_truck(10_000)
    man.load_truck(5_000)
    assert man.cargo_load == 15_000, man.cargo_load
    assert man.remaining_capacity() == 3_000, man.remaining_capacity()

    # Over-loading raises and leaves the load unchanged.
    try:
        man.load_truck(5_000)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for over-loading")
    assert man.cargo_load == 15_000, man.cargo_load

    # Partial and full unloading.
    man.unload_truck(5_000)
    assert man.cargo_load == 10_000, man.cargo_load
    man.unload_truck()  # full unload
    assert man.cargo_load == 0.0, man.cargo_load

    # Instances are independent.
    volvo.load_truck(20_000)
    assert man.cargo_load == 0.0 and volvo.cargo_load == 20_000

    # It really is a Vehicle.
    assert isinstance(man, Vehicle)

    print(volvo, "\n")
    print("All Truck checks passed.")


if __name__ == "__main__":
    _consistency_check()