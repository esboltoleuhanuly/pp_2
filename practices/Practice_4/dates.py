from datetime import datetime, timedelta

#1. Subtract five days
five_days_ago = datetime.now() - timedelta(days=5)
print(five_days_ago)

#2. Yesterday, Today, Tomorrow
today = datetime.now()
print(today - timedelta(days=1))
print(today)
print(today + timedelta(days=1))

#3. Drop microseconds
dt_no_ms = datetime.now().replace(microsecond=0)
print(dt_no_ms)

#4. Difference in seconds
date1 = datetime.now()
date2 = datetime(2026, 2, 20)
diff = date1 - date2
print(diff.total_seconds())