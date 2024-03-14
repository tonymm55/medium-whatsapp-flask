from datetime import datetime

# Given date and time
current_datetime_str = "Friday, March 15, 2024 07:50 AM"
current_datetime = datetime.strptime(current_datetime_str, "%A, %B %d, %Y %I:%M %p")

# Opening hours
opening_hours = {
    "Monday": ("08:00 AM", "07:00 PM"),
    "Tuesday": ("08:00 AM", "07:00 PM"),
    "Wednesday": ("08:00 AM", "07:00 PM"),
    "Thursday": ("08:00 AM", "07:00 PM"),
    "Friday": ("08:00 AM", "07:00 PM"),
    "Saturday": ("09:00 AM", "04:00 PM"),
    "Sunday": ("10:00 AM", "04:00 PM"),
}

# Check if open or closed
day_of_week = current_datetime.strftime("%A")
open_time_str, close_time_str = opening_hours[day_of_week]
open_time = datetime.strptime(open_time_str, "%I:%M %p").time()
close_time = datetime.strptime(close_time_str, "%I:%M %p").time()

is_open = open_time <= current_datetime.time() <= close_time
print(is_open)
