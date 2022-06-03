from datetime import timedelta

  
class WorkingDay:
    """Define working day structure."""
    def __init__(self, day, day_start_time=(8, 00), day_end_time=(18, 00), lunch_start_time=(12, 00), lunch_end_time=(13, 00), block_size=30):
        self.day = day
        # time of the working day starting, default 8:00
        self.day_start = self.day.replace(hour=day_start_time[0], minute=day_start_time[1])
        # time of the working day ending, default 18:00
        self.day_end = self.day.replace(hour=day_end_time[0], minute=day_end_time[1])
        # time of the lunch break starting, default 12:00
        self.lunch_start = self.day.replace(hour=lunch_start_time[0], minute=lunch_start_time[1])
        # time of the lunch break ending, default 13:00
        self.lunch_end = self.day.replace(hour=lunch_end_time[0], minute=lunch_end_time[1])
        # block_size of the appointment, default 30 minutes
        self.block_size = block_size
        # Number of appointments in the morning when having self.block_size
        slots_morning =  ((lunch_start_time[0] - day_start_time[0]) * 60 + (lunch_start_time[1] - day_start_time[1])) // self.block_size + 1
        # Number of appointments in the lunch break when having self.block_size
        slots_lunch =  ((lunch_end_time[0] - lunch_start_time[0]) * 60 + (lunch_end_time[1] - lunch_start_time[1])) // self.block_size + 1
        # Number of appointments in the afternoon when having self.block_size
        slots_afternoon = ((day_end_time[0] - lunch_end_time[0]) * 60 + (day_end_time[1]-lunch_end_time[1])) // self.block_size + 1
        # Number of slots outside working hours
        slots_outside = (((24 - day_end_time[0]) + day_start_time[0]) * 60 + (day_end_time[1] + day_start_time[1])) // self.block_size + 1
        # All possible appointments with instance attributes defined above
        # Morning list:
        morning_slots = [{"booked": False, "closed": False, "from":self.day_start + timedelta(minutes=self.block_size * (x - 1)), "to":self.day_start + timedelta(minutes=self.block_size * x)} for x in range(1, slots_morning)]
        # Slots closed, in case booked slot outside working hours
        slots_closed = [{"booked": False, "closed": True, "from":self.day_end + timedelta(minutes=self.block_size * (x - 1)), "to":self.day_end + timedelta(minutes=self.block_size * x)} for x in range(1, slots_outside)]
        # Lunch break list:
        lunch_slots = [{"booked": False, "closed": True, "from":self.lunch_start + timedelta(minutes=self.block_size * (x - 1)), "to":self.lunch_start + timedelta(minutes=self.block_size * x)} for x in range(1, slots_lunch)]
        # Afternoon list:
        afternoon_slots = [{"booked": False, "closed": False, "from":self.lunch_end + timedelta(minutes=self.block_size * (x - 1)), "to":self.lunch_end + timedelta(minutes=self.block_size * x)} for x in range(1, slots_afternoon)]
        self.all_slots = morning_slots + lunch_slots + afternoon_slots + slots_closed
        # Set the working_day to True from Monday to Friday
        if self.day.weekday() > 4:
            self.working_day = False
        else:
            self.working_day = True

