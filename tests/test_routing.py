from routing import all_deadlines_met
from simulation import build_simulation, total_mileage


def test_public_demo_routes_complete():
    package_table, trucks, _, _ = build_simulation()
    assert len(package_table.all_packages()) == 40
    assert all(package.delivery_time is not None for package in package_table.all_packages())
    for package in package_table.all_packages():
        if package.deadline != "EOD":
            print(
                package.package_id,
                package.deadline,
                package.delivery_time
            )
    assert all_deadlines_met(package_table)
    assert total_mileage(trucks) < 140


def test_capacity_limit():
    _, trucks, _, _ = build_simulation()
    assert all(len(truck.package_ids) <= 16 for truck in trucks)
