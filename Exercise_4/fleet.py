"""Sample fleet factory.

Centralises creation of the example vehicles so the GUI stays free of
hard-coded data. Each vehicle is built with a different number of
constructor arguments to showcase the optional parameters.
"""

from car import Car
from motorcycle import Motorcycle
from truck import Truck

Vehicle = Car | Motorcycle | Truck


def build_fleet() -> dict[str, Vehicle]:
    """Return a fresh fleet keyed by a human-readable label.

    A dict keeps lookup simple for the GUI's selectbox and guarantees
    stable, unique display names.
    """
    vehicles: list[Vehicle] = [
        # Cars — minimal vs. fully specified.
        Car("M-AB 1234", horse_power=110, max_speed=200,
            price=28_500.0, passenger_capacity=4),
        Car("B-EV 9000", horse_power=480, max_speed=261,
            price=54_990.0, passenger_capacity=4, tank_capacity=65.0),

        # Motorcycles — plain vs. with sidecar and custom tank.
        Motorcycle("M-XY 42", horse_power=140, max_speed=270, price=19_990.0),
        Motorcycle("S-GS 12", horse_power=40, max_speed=160, price=8_500.0,
                   has_sidecar=True, tank_capacity=24.0),

        # Trucks — standard vs. heavy-duty 4-axle.
        Truck("HH-TR 770", horse_power=460, max_speed=90, price=120_000.0,
              cargo_capacity=18_000, axle_count=3),
        Truck("K-LV 11", horse_power=540, max_speed=100, price=145_000.0,
              cargo_capacity=25_000, axle_count=4, tank_capacity=600.0),
    ]
    return {_label(v): v for v in vehicles}


def _label(vehicle: Vehicle) -> str:
    """Build a unique, type-prefixed label for the selectbox."""
    return f"{type(vehicle).__name__} · {vehicle.license_plate}"