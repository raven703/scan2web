from datetime import *

timestamp = datetime(2021, 11, 17, 14, 50, 12, 458529)
datenow = datetime.today()
d2 = timedelta(days=5, minutes=0)

if datenow - timestamp > d2:
    print('time to backup')
else:
    print('its ok')
