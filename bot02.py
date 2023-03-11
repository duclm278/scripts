from datetime import date, timedelta

# Conf
y1 = 2022
y2 = 2022

# Main
d = date(y1, 1, 1)
while (True):
    # ISO Calendar
    y1_num = d.strftime("%G")
    if int(y1_num) > y2:
        break

    d1_num = d.strftime("%j")
    w1_num = d.strftime("%V")  # Monday as 1st day of week
    m1_num = d.strftime("%m")
    print(d, d1_num, w1_num, w2_num, m1_num, y1_num)

    # Non-ISO Calendar
    y1_num = d.strftime("%Y")
    if int(y1_num) > y2:
        break
    d1_num = d.strftime("%j")
    w1_num = d.strftime("%W")  # Monday as 1st day of week
    w2_num = d.strftime("%U")  # Sunday as 1st day of week
    m1_num = d.strftime("%m")
    print(d, d1_num, w1_num, w2_num, m1_num, y1_num)

    d += timedelta(days=1)
