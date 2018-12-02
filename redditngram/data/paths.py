import datetime
import os

from redditngram.data import dates

_REDDIT_COMMENT_BASE_URL = "https://files.pushshift.io/reddit/comments/"
_BZ2_FILENAME_TEMPLATE = "RC_%Y-%m.bz2"
_XZ_FILENAME_TEMPLATE = "RC_%Y-%m.xz"
_NGRAM_FILENAME_TEMPLATE = "RC_%Y-%m_{n}gc.gz"

DEFAULT_REDDIT_DATA = (os.environ.get('REDDIT_DATA') or
                       os.path.expanduser("~/reddit"))
DEFAULT_REDDIT_COMMENTS_DATA = os.path.join(DEFAULT_REDDIT_DATA, "comments")
DEFAULT_REDDIT_NGRAMS_DATA = os.path.join(DEFAULT_REDDIT_DATA, "ngrams")


def get_reddit_comments_url(year, month):
  """Url for reddit comment data download."""
  target_date = datetime.date(year, month, 1)
  url = _get_reddit_comments_path(target_date, _REDDIT_COMMENT_BASE_URL)
  return url


def get_reddit_comments_local(year, month, root=DEFAULT_REDDIT_COMMENTS_DATA):
  """Local path of downloaded reddit comment data."""
  target_date = datetime.date(year, month, 1)
  path = _get_reddit_comments_path(target_date, root=root)
  return path


def get_reddit_ngrams_local(year, month, n, root=DEFAULT_REDDIT_NGRAMS_DATA):
  """Local path of generated reddit ngram data."""
  target_date = datetime.date(year, month, 1)
  path = _get_reddit_ngrams_path(target_date, n, root=root)
  return path


def _get_reddit_comments_path(date, root):
  if not dates.validate_reddit_comments_date(date):
    return None
  filename = _get_reddit_comments_filename(date)
  path = os.path.join(root, filename)
  return path


def _get_reddit_ngrams_path(date, n, root):
  if not dates.validate_reddit_comments_date(date):
    return None
  filename = _get_reddit_ngrams_filename(date, n)
  path = os.path.join(root, filename)
  return path


def _get_reddit_comments_filename(date):
  if date < dates._XZ_START_DATE:
    return date.strftime(_BZ2_FILENAME_TEMPLATE)
  else:
    return date.strftime(_XZ_FILENAME_TEMPLATE)


def _get_reddit_ngrams_filename(date, n):
  return date.strftime(_NGRAM_FILENAME_TEMPLATE.format(n=n))
