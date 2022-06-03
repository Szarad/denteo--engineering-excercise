import bisect
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from datetime import datetime, timedelta
from collections import defaultdict
from app.working_day import WorkingDay
from app.settings import get_settings
from app.booked_slots import weeklyAppointments

settings = get_settings()

def get_weekly_appointments_by_day(weekly_appointments):
    """Structure the weekly appointments by the day."""
    weekly_appointments_by_day = defaultdict(list)
    for appointment in weekly_appointments:
        weekly_appointments_by_day[appointment["from"].date()].append(appointment)
    return weekly_appointments_by_day

def find_free_time_slots(search_range, weekly_appointments):
    """Find free slots without booked appointments in search_range."""
    weekly_appointments_by_day = get_weekly_appointments_by_day(weekly_appointments) 
    start = datetime.fromisoformat(search_range["from"])
    stop = datetime.fromisoformat(search_range["to"])
    available_slots = defaultdict(list)
    current_day = start
    # Check all days from search_range
    while current_day <= stop:
        working_day = WorkingDay(current_day)
        # Check if chose day is a working day
        if working_day.working_day == False:
            current_day += timedelta(days=1)
            continue
        all_slots = working_day.all_slots
        if current_day.date() in weekly_appointments_by_day:
            # take all booked slots for the current day
            booked_slots = weekly_appointments_by_day[current_day.date()]
            # separated booked_slots into two lists to use bisect
            all_slots_from = [s["from"] for s in all_slots]
            all_slots_to = [s["to"] for s in all_slots]
            for booked_slot in booked_slots:
                booked_from = booked_slot["from"]
                booked_to = booked_slot["to"]
                # Check position of a booked slot in all possible slots
                idx_from = bisect.bisect_right(all_slots_from, booked_from) - 1
                # If two values are the same, return position on the left
                idx_to =  bisect.bisect_left( all_slots_to, booked_to) + 1
                # Change available slots to 'booked' if overlapping with booked_slots
                for i in range(idx_from, idx_to):
                    all_slots[i]["booked"] = True
        # Display only free slots from all available slots
        available_slots[current_day.date()] = [slot for slot in all_slots if slot["booked"] == False and slot["closed"] == False]
        # Check the next day
        current_day += timedelta(days=1)
    return available_slots


app = FastAPI()
@app.get("/appointments")
async def get_all_appointments(from_date: str="2021-01-04", to_date: str="2021-01-07" ):
    """List all available appointments between two dates."""
    search_range = { "from": from_date, "to": to_date }
    return find_free_time_slots(search_range, weeklyAppointments)

@app.get("/")
def docs():
    """Redirect local environment to /docs."""
    url = settings.production_url
    status_code=301
    if settings.development_env == "local":
        url = "/docs"
        status_code = 302
    return RedirectResponse(url=url, status_code=status_code)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

