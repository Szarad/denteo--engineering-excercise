from datetime import datetime
from app.main import find_free_time_slots
from app.booked_slots import weeklyAppointments

def test_find_free_time_slots_one_day():
    weekly_appointments = [{'from': datetime(2021, 1, 4, 10, 5), 'to': datetime(2021, 1, 4, 10, 55)}]
    search_range = { "from":"2021-01-04", "to":"2021-01-04" }
    assert len(find_free_time_slots(search_range, weekly_appointments)) == 1
    assert len(find_free_time_slots(search_range, weekly_appointments)[datetime(2021, 1, 4).date()]) == 16

def test_find_free_time_slots_three_day():
    weekly_appointments = [{'from': datetime(2021, 1, 4, 10, 5), 'to': datetime(2021, 1, 4, 10, 55)}, {'from': datetime(2021, 1, 5, 10, 5), 'to': datetime(2021, 1, 5, 10, 55)}, {'from': datetime(2021, 1, 6, 10, 5), 'to': datetime(2021, 1, 6, 10, 55)}]
    search_range = { "from":"2021-01-04", "to":"2021-01-06"}
    assert len(find_free_time_slots(search_range, weekly_appointments)) == 3
    assert len(find_free_time_slots(search_range, weekly_appointments)[datetime(2021, 1, 6).date()]) == 16

def test_find_free_time_slots_is_weekend():
    weekly_appointments = [{'from': datetime(2022, 1, 2, 10, 5), 'to': datetime(2022, 1, 2, 10, 55)}]
    search_range = { "from":"2022-01-02", "to":"2022-01-02"}
    assert len(find_free_time_slots(search_range, weekly_appointments)) == 0

# Primary test cases:
def test_primary_test_cases():
    search_range = { "from":"2021-01-04", "to":"2021-01-07" }
    available_slots = find_free_time_slots(search_range, weeklyAppointments)
    assert len(available_slots) == 4
    assert len(available_slots[datetime(2021, 1, 4).date()]) == 17
    assert len(available_slots[datetime(2021, 1, 5).date()]) == 15
    assert len(available_slots[datetime(2021, 1, 6).date()]) == 14
    assert len(available_slots[datetime(2021, 1, 7).date()]) == 18

# Test a booked slot during lunch break
def test_slot_during_closed():
    search_range = { "from":"2021-01-04", "to":"2021-01-04" }
    weekly_appointments = [{'from': datetime(2021, 1, 4, 11, 0), 'to': datetime(2021, 1, 4, 12, 30)}]
    assert len(find_free_time_slots(search_range, weekly_appointments)) == 1
    assert len(find_free_time_slots(search_range, weekly_appointments)[datetime(2021, 1, 4).date()]) == 16
