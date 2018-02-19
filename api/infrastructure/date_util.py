from datetime import timedelta


def day_iterator_inclusive(start, end, jump=1):
    while end >= start:
        yield start
        start += timedelta(days=jump)
