"""Abstract base class for all vehicles.

``Vehicle`` collects the state and behaviour every vehicle shares and
defines the contract that each concrete subclass must fulfil. It is an
Abstract Base Class (ABC): it cannot be instantiated directly, and any
subclass must implement the abstract method ``_specific_status_lines``.

Run directly to confirm the class cannot be instantiated:
    python vehicle.py
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Vehicle(ABC):
    """Common base for every vehicle.

    Attributes:
        license_plate: Official registration plate, e.g. "M-AB 1234".
        horse_power: Engine power in metric horsepower (PS).
        max_speed: Top speed in km/h.
        price: Purchase price in euro.
        tank_capacity: Maximum fuel the tank can hold in litres.
        fuel_count: Current fuel level in litres (managed by methods).
        km_driven: Total kilometres driven (odometer, managed by methods).
        is_clean: Whether the vehicle is currently clean.
    """

    def __init__(
        self,
        license_plate: str,
        horse_power: int,
        max_speed: int,
        price: float,
        tank_capacity: float,
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
        self.tank_capacity = tank_capacity

        # State managed by methods.
        self.fuel_count: float = 0.0
        self.km_driven: float = 0.0
        self.is_clean: bool = True

    # --- Behaviour shared by every vehicle -------------------------------

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
        """Clean the vehicle."""
        self.is_clean = True

    # --- Contract for subclasses -----------------------------------------

    @abstractmethod
    def _specific_status_lines(self) -> list[str]:
        """Return the subclass-specific status lines for ``__str__``.

        Each concrete vehicle reports its own unique state here (e.g. a
        truck's cargo, a car's passengers). This is the single piece every
        subclass *must* provide; the rest of the status is assembled by the
        base class below (template-method pattern).
        """
        raise NotImplementedError

    # --- Shared representation built on top of the contract --------------

    def __str__(self) -> str:
        lines = [
            f"{type(self).__name__} [{self.license_plate}] — "
            f"{self.horse_power} PS, max {self.max_speed} km/h, "
            f"{self.price:.2f} €",
            *self._specific_status_lines(),
            f"  Fuel: {self.fuel_count:.1f}/{self.tank_capacity:.1f} L",
            f"  Odometer: {self.km_driven:.1f} km",
            f"  Clean: {'yes' if self.is_clean else 'no'}",
        ]
        return "\n".join(lines)


if __name__ == "__main__":
    # Demonstrate that an ABC with an abstract method cannot be instantiated.
    try:
        Vehicle("X-00 0", 100, 200, 1.0, 50.0)  # type: ignore[abstract]
    except TypeError as exc:
        print("Vehicle is abstract and cannot be instantiated:")
        print(f"  {exc}")
    else:
        raise AssertionError("expected TypeError when instantiating Vehicle")