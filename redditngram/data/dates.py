import datetime
import logging

from dateutil.relativedelta import relativedelta


_DATA_START_DATE = datetime.date(2005, 12, 1)
_XZ_START_DATE = datetime.date(2017, 12, 1)


def validate_reddit_comments_date(date):
  """Check if queried date has reddit data."""
  start_date = _DATA_START_DATE
  end_date = datetime.date.today() + relativedelta(months=-1)
  if (date > end_date or date < start_date):
    logging.warning("date must be between {} and {}: given {}".format(
        start_date.strftime("%Y-%m"), end_date.strftime("%Y-%m"),
        date.strftime("%Y-%m")))
    return False
  return True