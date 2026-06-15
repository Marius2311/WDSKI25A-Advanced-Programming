"""Truck class definition with a runnable consistency check.

Run directly to execute the consistency checks:
    python truck.py
"""


class Truck:
    """A cargo truck.

    Attributes:
        license_plate: Official registration plate, e.g. "HH-TR 770".
        horse_power: Engine power in metric horsepower (PS).
        max_speed: Top speed in km/h.
        price: Purchase price in euro.
        cargo_capacity: Maximum payload in kilograms. Class-specific.
        axle_count: Number of axles. Class-specific attribute.
        fuel_count: Current fuel level in litres (managed by methods).
        tank_capacity: Maximum fuel the tank can hold in litres.
        km_driven: Total kilometres driven (odometer, managed by methods).
        is_clean: Whether the truck is currently clean.
        cargo_load: Current load in kilograms. Class-specific.
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
        if horse_power <= 0:
            raise ValueError("horse_power must be positive")
        if max_speed <= 0:
            raise ValueError("max_speed must be positive")
        if price < 0:
            raise ValueError("price must not be negative")
        if cargo_capacity <= 0:
            raise ValueError("cargo_capacity must be positive")
        if axle_count < 2:
            raise ValueError("axle_count must be at least 2")
        if tank_capacity <= 0:
            raise ValueError("tank_capacity must be positive")

        self.license_plate = license_plate
        self.horse_power = horse_power
        self.max_speed = max_speed
        self.price = price
        self.cargo_capacity = cargo_capacity
        self.axle_count = axle_count
        self.tank_capacity = tank_capacity

        # State managed by methods.
        self.fuel_count: float = 0.0
        self.km_driven: float = 0.0
        self.is_clean: bool = True
        self.cargo_load: float = 0.0

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
        """Clean the truck."""
        self.is_clean = True

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

    def __str__(self) -> str:
        return (
            f"Truck [{self.license_plate}] — {self.horse_power} PS, "
            f"max {self.max_speed} km/h, {self.price:.2f} €\n"
            f"  Axles: {self.axle_count}\n"
            f"  Cargo: {self.cargo_load:.1f}/{self.cargo_capacity:.1f} kg\n"
            f"  Fuel: {self.fuel_count:.1f}/{self.tank_capacity:.1f} L\n"
            f"  Odometer: {self.km_driven:.1f} km\n"
            f"  Clean: {'yes' if self.is_clean else 'no'}"
        )


def _consistency_check() -> None:
    """Create instances and verify attributes behave correctly."""
    print("=== Truck consistency check ===\n")

    man = Truck("HH-TR 770", horse_power=460, max_speed=90,
                price=120000.0, cargo_capacity=18000, axle_count=3)
    volvo = Truck("K-LV 11", horse_power=540, max_speed=100,
                  price=145000.0, cargo_capacity=25000, axle_count=4)

    print(man, "\n")

    # Odometer accumulates across multiple calls.
    man.track_km_driven(300)
    man.track_km_driven(150.25)
    assert man.km_driven == 450.25, man.km_driven

    # Refuelling is capped at tank capacity.
    man.fuel_vehicle(250)
    man.fuel_vehicle(250)  # would be 500, but tank holds only 400
    assert man.fuel_count == man.tank_capacity == 400.0, man.fuel_count

    # Loading respects capacity; remaining capacity stays consistent.
    man.load_truck(10000)
    man.load_truck(5000)
    assert man.cargo_load == 15_000, man.cargo_load
    assert man.remaining_capacity() == 3000, man.remaining_capacity()

    # Over-loading raises and leaves the load unchanged.
    try:
        man.load_truck(5000)
    except ValueError as ve:
        print(ve)
        print("\n")
        pass
    else:
        raise AssertionError("expected ValueError for over-loading")
    assert man.cargo_load == 15000, man.cargo_load

    # Partial and full unloading.
    man.unload_truck(5000)
    assert man.cargo_load == 10000, man.cargo_load
    man.unload_truck()  # full unload
    assert man.cargo_load == 0.0, man.cargo_load

    # Instances are independent.
    volvo.load_truck(20000)
    assert man.cargo_load == 0.0 and volvo.cargo_load == 20000

    print(volvo, "\n")
    print("All Truck checks passed.")


if __name__ == "__main__":
    _consistency_check()