from datetime import date, datetime, time, timedelta

from pydantic import BaseModel


class Model(BaseModel):
    date_field: date = None
    datetime_field: datetime = None
    time_field: time = None
    timedelta_field: timedelta = None


m = Model(
    date_field=1966280412345.6789,
    datetime_field="2032-04-23T10:20:30.400+02:30",
    time_field=time(4, 8, 16),
    timedelta_field="P3DT12H30M5S",
)
print(m.dict())
