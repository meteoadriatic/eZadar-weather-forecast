def get_dates():
    import datetime as dt
    from datetime import timedelta

    d0 = dt.datetime.today().strftime("%Y-%m-%d")
    d1 = (dt.datetime.strptime(d0, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    d2 = (dt.datetime.strptime(d0, "%Y-%m-%d") + timedelta(days=2)).strftime("%Y-%m-%d")

    return d0, d1, d2