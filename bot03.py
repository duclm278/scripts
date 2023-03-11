import csv
from datetime import date, timedelta
from pprint import pprint

# Conf
y1 = 1
y2 = 9999

# Main
dw = {}  # Day -> Week
dm = {}  # Day -> Month
d = date(y1, 1, 1)
while (True):
    # Year with century as a decimal number.
    # E.g 0001, 0002, …, 2013, 2014, …, 9998, 9999
    y1_num = d.strftime("%Y")
    if int(y1_num) > y2:
        break

    # Day of the year as a zero-padded decimal number.
    # E.g. 001, 002, …, 366
    d_num = d.strftime("%j")

    # Week number of the year (Sunday as the first day of the week) as a
    # zero-padded decimal number. All days in a new year preceding the first
    # Sunday are considered to be in week 0.
    # E.g. 00, 01, …, 53
    # w_num = d.strftime("%U")

    # Week number of the year (Monday as the first day of the week) as a
    # zero-padded decimal number. All days in a new year preceding the first
    # Monday are considered to be in week 0.
    # E.g. 00, 01, …, 53
    # w_num = d.strftime("%W")

    # ISO 8601 week as a decimal number with Monday as the first day of the
    # week. Week 01 is the week containing Jan 4.
    # E.g. 01, …, 53
    w_num = d.strftime("%V")

    # Month as locale’s abbreviated name.
    # E.g. Jan, Feb, …, Dec (en_US)
    m_num = d.strftime("%b")

    try:
        dw[d_num].add(w_num)
        dm[d_num].add(m_num)
    except KeyError:
        dw[d_num] = {w_num}
        dm[d_num] = {m_num}

    try:
        d += timedelta(days=1)
    except OverflowError:
        break

# pprint(dw)
# pprint(dm)
with open("test.tsv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter="\t")
    for d in dw:
        writer.writerow(
            [d, ", ".join(sorted(dm[d])), ", ".join(sorted(dw[d]))]
        )
