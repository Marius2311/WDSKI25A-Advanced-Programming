"""Motorcycle class definition with a runnable consistency check.

``Motorcycle`` inherits the shared state and behaviour from
:class:`Vehicle` and adds helmet handling and a wheelie.

Run directly to execute the consistency checks:
    python motorcycle.py
"""

from __future__ import annotations

from vehicle import Vehicle


class Motorcycle(Vehicle):
    """A motorcycle.

    Adds to :class:`Vehicle`:
        has_sidecar: Whether the motorcycle is fitted with a sidecar.
        has_helmet: Whether a helmet is currently stowed/available.
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
        super().__init__(license_plate, horse_power, max_speed, price,
                         tank_capacity)
        self.has_sidecar = has_sidecar
        self.has_helmet: bool = False

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
        return "Wheelie! 🏍️"

    # --- Implementation of the Vehicle contract --------------------------

    def _specific_status_lines(self) -> list[str]:
        return [
            f"  Sidecar: {'yes' if self.has_sidecar else 'no'}, "
            f"Helmet ready: {'yes' if self.has_helmet else 'no'}"
        ]


def _consistency_check() -> None:
    """Create instances and verify attributes behave correctly."""
    print("=== Motorcycle consistency check ===\n")

    ducati = Motorcycle("M-XY 42", horse_power=140, max_speed=270,
                        price=19_990.0)
    bmw = Motorcycle("S-GS 12", horse_power=40, max_speed=160,
                     price=8_500.0, has_sidecar=True)

    print(ducati, "\n")

    # Inherited behaviour: odometer accumulates across multiple calls.
    ducati.track_km_driven(50)
    ducati.track_km_driven(25.5)
    assert ducati.km_driven == 75.5, ducati.km_driven

    # Inherited behaviour: refuelling is capped at tank capacity.
    ducati.fuel_vehicle(10)
    ducati.fuel_vehicle(20)  # would be 30, but tank holds only 18
    assert ducati.fuel_count == ducati.tank_capacity == 18.0, ducati.fuel_count

    # Motorcycle-specific: helmet toggling and ride eligibility.
    assert ducati.can_ride() is False  # no helmet yet
    ducati.add_helmet()
    assert ducati.has_helmet is True
    assert ducati.can_ride() is True   # helmet + fuel
    assert ducati.do_wheelie() == "Wheelie! 🏍️"

    # Underpowered bike cannot wheelie even with a helmet.
    bmw.add_helmet()
    assert bmw.do_wheelie() == "Not enough power for a wheelie."

    # Wheelie without helmet raises, and instances are independent.
    ducati.remove_helmet()
    assert ducati.has_helmet is False
    assert bmw.has_helmet is True
    try:
        ducati.do_wheelie()
    except RuntimeError:
        pass
    else:
        raise AssertionError("expected RuntimeError without helmet")

    # It really is a Vehicle.
    assert isinstance(ducati, Vehicle)

    print(bmw, "\n")
    print("All Motorcycle checks passed.")


if __name__ == "__main__":
    _consistency_check()