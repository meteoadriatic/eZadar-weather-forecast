import datetime as dt
from datetime import timedelta

def get_fdays(forecastt):
    import datetime as dt
    from datetime import timedelta

    if forecastt == 'morning':
        fday1 = dt.datetime.today().strftime("%Y-%m-%d")
        fday2 = (dt.datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        fday1 = (dt.datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        fday2 = (dt.datetime.today() + timedelta(days=2)).strftime("%Y-%m-%d")

    return fday1, fday2