import datetime as dt
import pytz

def format_current_datetime():
    tz = pytz.timezone('America/Los_Angeles')
    time = dt.datetime.now(tz)
    today_date = time.date().strftime('%A %B %d, %Y')
    h, m = str(time).split(':')[:2]
    h = h.split()[1]
    h = int(h)
    if 0 <= h <= 11:
        p = 'AM'
    else:
        p = 'PM'
    h2 = h % 12
    if h2 == 0:
        h2 = 12
    h2 = str(h2)
    if len(m) == 1:
        m = '0' + m
    if len(h2) == 1:
        h2 + '0' + h2
    return today_date + ', ' + h2 + ':' + m + p