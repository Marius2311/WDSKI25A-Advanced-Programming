"""Streamlit GUI for the vehicle fleet.

Run with:
    streamlit run app.py

The app lets you inspect each vehicle's live status and interact with it:
drive, refuel, wash, and type-specific actions (passengers, helmet, cargo).
Vehicle objects live in ``st.session_state`` so their state persists across
Streamlit reruns.
"""

import streamlit as st

from car import Car
from fleet import Vehicle, build_fleet
from motorcycle import Motorcycle
from truck import Truck

# --------------------------------------------------------------------------
# State management
# --------------------------------------------------------------------------


def init_state() -> None:
    """Create the fleet once per user session."""
    if "fleet" not in st.session_state:
        st.session_state.fleet = build_fleet()


def reset_fleet() -> None:
    """Rebuild the fleet from scratch (resets all interactions)."""
    st.session_state.fleet = build_fleet()


# --------------------------------------------------------------------------
# Rendering helpers
# --------------------------------------------------------------------------


def render_status(vehicle: Vehicle) -> None:
    """Show the common status metrics plus the raw __str__ output."""
    st.subheader(f"Status · {type(vehicle).__name__} {vehicle.license_plate}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Horsepower", f"{vehicle.horse_power} PS")
    col2.metric("Max speed", f"{vehicle.max_speed} km/h")
    col3.metric("Price", f"{vehicle.price:,.0f} €")

    col4, col5, col6 = st.columns(3)
    col4.metric("Odometer", f"{vehicle.km_driven:,.1f} km")
    col5.metric(
        "Fuel",
        f"{vehicle.fuel_count:.1f} / {vehicle.tank_capacity:.0f} L",
    )
    col6.metric("Clean", "Yes" if vehicle.is_clean else "No")

    # Fuel level as a progress bar for an intuitive overview.
    st.progress(
        min(vehicle.fuel_count / vehicle.tank_capacity, 1.0),
        text="Fuel level",
    )

    with st.expander("Full text representation (__str__)"):
        st.code(str(vehicle), language="text")


def render_common_controls(vehicle: Vehicle) -> None:
    """Actions every vehicle supports: drive, refuel, wash."""
    st.markdown("#### Common actions")
    col_drive, col_fuel, col_wash = st.columns(3)

    with col_drive:
        km = st.number_input("Kilometres to drive", min_value=0.0,
                             value=50.0, step=10.0, key="drive_km")
        if st.button("🚗 Drive", use_container_width=True):
            _run(lambda: vehicle.track_km_driven(km),
                 f"Drove {km:.0f} km.")

    with col_fuel:
        litres = st.number_input("Litres to refuel", min_value=0.0,
                                value=20.0, step=5.0, key="fuel_litres")
        if st.button("Refuel", use_container_width=True):
            _run(lambda: vehicle.fuel_vehicle(litres),
                 f"Added {litres:.0f} L.")

    with col_wash:
        st.write("")  # spacer to align the button
        st.write("")
        if st.button("Wash", use_container_width=True):
            _run(vehicle.wash, "Vehicle washed.")


def render_specific_controls(vehicle: Vehicle) -> None:
    """Dispatch to the type-specific control panel."""
    st.markdown("#### Specific actions")

    if isinstance(vehicle, Car):
        _render_car_controls(vehicle)
    elif isinstance(vehicle, Motorcycle):
        _render_motorcycle_controls(vehicle)
    elif isinstance(vehicle, Truck):
        _render_truck_controls(vehicle)


def _render_car_controls(car: Car) -> None:
    st.info(f"Passengers: {car.passengers} / {car.passenger_capacity}")
    count = st.number_input("Passengers", min_value=1, value=1, step=1,
                            key="passenger_count")
    col_add, col_remove = st.columns(2)
    if col_add.button("➕ Add passenger(s)", use_container_width=True):
        _run(lambda: car.add_passenger(int(count)),
             f"Added {int(count)} passenger(s).")
    if col_remove.button("➖ Remove passenger(s)", use_container_width=True):
        _run(lambda: car.remove_passenger(int(count)),
             f"Removed {int(count)} passenger(s).")


def _render_motorcycle_controls(bike: Motorcycle) -> None:
    st.info(
        f"Helmet ready: {'yes' if bike.has_helmet else 'no'} · "
        f"Sidecar: {'yes' if bike.has_sidecar else 'no'}"
    )
    col_add, col_remove, col_wheelie = st.columns(3)
    if col_add.button("Add helmet", use_container_width=True):
        _run(bike.add_helmet, "Helmet stowed.")
    if col_remove.button("Remove helmet", use_container_width=True):
        _run(bike.remove_helmet, "Helmet removed.")
    if col_wheelie.button("Wheelie", use_container_width=True):
        _run(lambda: st.toast(bike.do_wheelie()), None)


def _render_truck_controls(truck: Truck) -> None:
    st.info(
        f"Cargo: {truck.cargo_load:,.0f} / {truck.cargo_capacity:,.0f} kg "
        f"(free: {truck.remaining_capacity():,.0f} kg)"
    )
    st.progress(
        min(truck.cargo_load / truck.cargo_capacity, 1.0),
        text="Cargo load",
    )
    kg = st.number_input("Cargo (kg)", min_value=0.0, value=1_000.0,
                        step=500.0, key="cargo_kg")
    col_load, col_unload, col_empty = st.columns(3)
    if col_load.button("Load", use_container_width=True):
        _run(lambda: truck.load_truck(kg), f"Loaded {kg:,.0f} kg.")
    if col_unload.button("Unload", use_container_width=True):
        _run(lambda: truck.unload_truck(kg), f"Unloaded {kg:,.0f} kg.")
    if col_empty.button("Empty fully", use_container_width=True):
        _run(truck.unload_truck, "Truck fully unloaded.")


# --------------------------------------------------------------------------
# Action runner
# --------------------------------------------------------------------------


def _run(action, success_message: str | None) -> None:
    """Execute a mutating action, surface errors, and refresh the view.

    Domain errors (ValueError / RuntimeError) are shown to the user instead
    of crashing the app. On success we rerun so all widgets reflect the new
    state immediately.
    """
    try:
        action()
    except (ValueError, RuntimeError) as exc:
        st.error(str(exc))
        return
    if success_message:
        st.toast(success_message, icon="✅")
    st.rerun()


# --------------------------------------------------------------------------
# Main layout
# --------------------------------------------------------------------------


def main() -> None:
    st.set_page_config(page_title="Vehicle Fleet", page_icon="🚗",
                       layout="wide")
    init_state()

    st.title("🚗 Vehicle Fleet Dashboard")
    st.caption(
        "Inspect and interact with example cars, motorcycles and trucks."
    )

    with st.sidebar:
        st.header("Fleet")
        labels = list(st.session_state.fleet.keys())
        selected = st.selectbox("Choose a vehicle", labels)
        st.divider()
        if st.button("🔄 Reset fleet", use_container_width=True):
            reset_fleet()
            st.rerun()
        st.caption("Resetting restores all vehicles to their initial state.")

    vehicle = st.session_state.fleet[selected]

    render_status(vehicle)
    st.divider()
    render_common_controls(vehicle)
    st.divider()
    render_specific_controls(vehicle)


if __name__ == "__main__":
    main()