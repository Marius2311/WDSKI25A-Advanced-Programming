"""Motorcycle class definition with a runnable consistency check.

Run directly to execute the consistency checks:
    python motorcycle.py
"""


class Motorcycle:
    """A motorcycle.

    Attributes:
        license_plate: Official registration plate, e.g. "M-XY 42".
        horse_power: Engine power in metric horsepower (PS).
        max_speed: Top speed in km/h.
        price: Purchase price in euro.
        has_helmet: Whether a helmet is currently stowed/available.
            Class-specific attribute.
        has_sidecar: Whether the motorcycle is fitted with a sidecar.
            Class-specific attribute.
        fuel_count: Current fuel level in litres (managed by methods).
        tank_capacity: Maximum fuel the tank can hold in litres.
        km_driven: Total kilometres driven (odometer, managed by methods).
        is_clean: Whether the motorcycle is currently clean.
    """

    def __init__(
        self,
        license_plate: str,
        horse_power: int,
        max_speed: int,
        price: float,
        has_sidecar: bool = False,
        tank_capacity: float = 18.0,
    ) -> None:
        if horse_power <= 0:
            raise ValueError("horse_power must be positive")
        if max_speed <= 0:
            raise ValueError("max_speed must be positive")
        if price < 0:
            raise ValueError("price must not be negative")
        if tank_capacity <= 0:
            raise ValueError("tank_capacity must be positive")

        self.license_plate = license_plate
        self.horse_power = horse_power
        self.max_speed = max_speed
        self.price = price
        self.has_sidecar = has_sidecar
        self.tank_capacity = tank_capacity

        # State managed by methods.
        self.fuel_count: float = 0.0
        self.km_driven: float = 0.0
        self.is_clean: bool = True
        self.has_helmet: bool = False

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
        """Clean the motorcycle."""
        self.is_clean = True

    # --- Motorcycle-specific methods -------------------------------------

    def add_helmet(self) -> None:
        """Stow a helmet so the rider is allowed to ride."""
        self.has_helmet = True

    def remove_helmet(self) -> None:
        """Remove the stowed helmet."""
        self.has_helmet = False

    def can_ride(self) -> bool:
        """A ride is only legal/safe with a helmet and some fuel."""
        return self.has_helmet and self.fuel_count > 0

    def do_wheelie(self) -> str:
        """Attempt a wheelie — only possible with enough power and a helmet."""
        if not self.has_helmet:
            raise RuntimeError("Put on a helmet before attempting a wheelie!")
        if self.horse_power < 50:
            return "Not enough power for a wheelie."
        return "Wheelie done!"

    def __str__(self) -> str:
        return (
            f"Motorcycle [{self.license_plate}] — {self.horse_power} PS, "
            f"max {self.max_speed} km/h, {self.price:.2f} €\n"
            f"  Sidecar: {'yes' if self.has_sidecar else 'no'}, "
            f"Helmet ready: {'yes' if self.has_helmet else 'no'}\n"
            f"  Fuel: {self.fuel_count:.1f}/{self.tank_capacity:.1f} L\n"
            f"  Odometer: {self.km_driven:.1f} km\n"
            f"  Clean: {'yes' if self.is_clean else 'no'}"
        )


def _consistency_check() -> None:
    """Create instances and verify attributes behave correctly."""
    print("=== Motorcycle consistency check ===\n")

    ducati = Motorcycle("M-XY 42", horse_power=140, max_speed=270,
                        price=19_990.0)
    bmw = Motorcycle("S-GS 12", horse_power=40, max_speed=160,
                     price=8_500.0, has_sidecar=True)

    print(ducati, "\n")

    # Odometer accumulates across multiple calls.
    ducati.track_km_driven(50)
    ducati.track_km_driven(25.5)
    assert ducati.km_driven == 75.5, ducati.km_driven

    # Refuelling is capped at tank capacity.
    ducati.fuel_vehicle(10)
    ducati.fuel_vehicle(20)  # would be 30, but tank holds only 18
    assert ducati.fuel_count == ducati.tank_capacity == 18.0, ducati.fuel_count

    # Helmet toggling and ride eligibility.
    assert ducati.can_ride() is False  # no helmet yet
    ducati.add_helmet()
    assert ducati.has_helmet is True
    assert ducati.can_ride() is True   # helmet + fuel
    assert ducati.do_wheelie() == "Wheelie done!"

    # Underpowered bike cannot wheelie even with a helmet.
    bmw.add_helmet()
    assert bmw.do_wheelie() == "Not enough power for a wheelie."

    # Wheelie without helmet raises, and instances are independent.
    ducati.remove_helmet()
    assert ducati.has_helmet is False
    assert bmw.has_helmet is True
    try:
        ducati.do_wheelie()
    except RuntimeError as re:
        print(re)
        print("\n")
        pass
    else:
        raise AssertionError("expected RuntimeError without helmet")

    print(bmw, "\n")
    print("All Motorcycle checks passed.")


if __name__ == "__main__":
    _consistency_check()