from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

from routing import all_deadlines_met
from simulation import build_simulation, total_mileage


st.set_page_config(
    page_title="Delivery Route Optimizer",
    page_icon="🚚",
    layout="wide",
)


def format_time(value):
    if value is None:
        return "--"
    total_seconds = int(round(value.total_seconds()))
    hours = (total_seconds // 3600) % 24
    minutes = (total_seconds % 3600) // 60
    suffix = "AM" if hours < 12 else "PM"
    display_hour = hours % 12 or 12
    return f"{display_hour}:{minutes:02d} {suffix}"


@st.cache_resource
def simulation():
    return build_simulation()


package_table, trucks, _, _ = simulation()
packages = sorted(package_table.all_packages(), key=lambda package: package.package_id)

st.title("Delivery Route Optimizer")
st.caption("Python routing simulator using a custom chained hash table and a deadline-aware nearest-neighbor heuristic.")

col1, col2, col3 = st.columns(3)
col1.metric("Packages", len(packages))
col2.metric("Total mileage", f"{total_mileage(trucks):.1f} mi")
col3.metric("Deadlines met", "Yes" if all_deadlines_met(package_table) else "No")

st.subheader("Truck summary")
truck_rows = []
for truck in trucks:
    truck_rows.append(
        {
            "Truck": truck.truck_id,
            "Packages": len(truck.package_ids),
            "Departure": format_time(truck.departure_time),
            "Return": format_time(truck.return_time),
            "Mileage": round(truck.mileage, 1),
            "Stops": len(truck.route) - 2,
        }
    )
st.dataframe(pd.DataFrame(truck_rows), use_container_width=True, hide_index=True)

st.subheader("Package status lookup")
selected_time = st.time_input("View package status at", value=datetime.strptime("10:15 AM", "%I:%M %p").time())
query_time = timedelta(hours=selected_time.hour, minutes=selected_time.minute)

package_rows = []
for package in packages:
    status = package.status_at(query_time)
    package_rows.append(
        {
            "ID": package.package_id,
            "Truck": package.truck_id,
            "Address": package.address,
            "Deadline": package.deadline,
            "Weight": package.weight,
            "Status": status,
            "Delivery time": format_time(package.delivery_time) if status == "Delivered" else "--",
            "Notes": package.notes,
        }
    )

status_filter = st.multiselect(
    "Filter by status",
    options=["Delayed", "At the hub", "En route", "Delivered"],
    default=["Delayed", "At the hub", "En route", "Delivered"],
)
status_df = pd.DataFrame(package_rows)
st.dataframe(status_df[status_df["Status"].isin(status_filter)], use_container_width=True, hide_index=True)

st.subheader("Route order")
selected_truck = st.selectbox("Select truck", options=[truck.truck_id for truck in trucks])
truck = next(item for item in trucks if item.truck_id == selected_truck)
route_df = pd.DataFrame({"Stop": range(len(truck.route)), "Address": truck.route})
st.dataframe(route_df, use_container_width=True, hide_index=True)

with st.expander("How the project works"):
    st.markdown(
        """
        - Package records are stored in a **custom hash table** using package ID as the key.
        - Hash collisions are resolved with **separate chaining**.
        - Each truck uses a **deadline-aware nearest-neighbor heuristic**: earlier deadlines are prioritized, and the closest package is chosen among packages sharing the same deadline.
        - Travel time is calculated using an average truck speed of **18 mph**.
        - Departure and delivery timestamps make it possible to reconstruct package status at any point in the simulated day.
        """
    )
