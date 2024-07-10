import datetime
from restaurant.models import TimeSlot

start_date = datetime.date(2024, 7, 1)
end_date = datetime.date(2024, 8, 31)
start_time = datetime.time(9, 0)
end_time = datetime.time(21, 0)
delta = datetime.timedelta(days=1)


while start_date <= end_date:
    for i in range(9, 22):
        start_time = datetime.time(i, 0)
        TimeSlot.objects.create(date=start_date, time=start_time, available=True)
    start_date += delta