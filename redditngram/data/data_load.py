import bz2
import datetime
import gzip
import json
import logging
import lzma as xz

from dateutil.relativedelta import relativedelta
from functools import partial

from redditngram.data import dates
from redditngram.data import paths
from redditngram.utils import op_utils

def populate_reddit_comments_json(dest=paths.DEFAULT_REDDIT_COMMENTS_DATA):
  """Download all reddit comments data not in the local cache."""
  curr_date = dates._DATA_START_DATE
  end_date = datetime.date.today() + relativedelta(months=-1)
  query_dates = []
  while curr_date <= end_date:
    query_dates.append(curr_date)
    curr_date += relativedelta(months=1)
  download_fn = partial(_download_reddit_comments_json, dest=dest)
  # Using too many processes causes "ERROR 429: Too Many Requests."
  list(
      op_utils.multiproc_imap(
          download_fn,
          query_dates,
          processes=4,
          thread_only=True,
          total=len(query_dates)))


def _download_reddit_comments_json(date,
                                   dest=paths.DEFAULT_REDDIT_COMMENTS_DATA):
  return download_reddit_comments_json(date.year, date.month, dest=dest)


def download_reddit_comments_json(year,
                                  month,
                                  dest=paths.DEFAULT_REDDIT_COMMENTS_DATA):
  """Download reddit comments data for month of year."""
  url = paths.get_reddit_comments_url(year, month)
  if not url:
    logging.warning(
        datetime.date(year, month, 1).strftime("No data exists for %Y-%m."))
    return False
  return op_utils.download(url, dest=dest)


def load_reddit_comments_json(year,
                              month,
                              root=paths.DEFAULT_REDDIT_COMMENTS_DATA):
  """Loads Reddit comment json dictionary generator for month of year from disk."""
  path = paths.get_reddit_comments_local(year, month, root=root)
  if not path:
    logging.warning(
        datetime.date(year, month, 1).strftime("No data exists for %Y-%m."))
    return None
  assert path.endswith('.bz2') or path.endswith('.xz'), (
      "Failed to load {}.Only bz2 and xz are supported.".format(path))
  reader = bz2.BZ2File if path.endswith('.bz2') else xz.LZMAFile
  with reader(path, 'r') as fh:
    for line in fh:
      yield json.loads(line.decode())


def load_reddit_ngrams(year,
                       month,
                       n,
                       root=paths.DEFAULT_REDDIT_NGRAMS_DATA):
  """Loads Reddit (ngram, count) generator for month of year from disk."""
  path = paths.get_reddit_ngrams_local(year, month, n, root=root)
  if not path:
    logging.warning(
        datetime.date(year, month, 1).strftime("No data exists for %Y-%m."))
    return None
  with gzip.GzipFile(path, 'r') as fh:
    for line in fh:
      try:
        ngram, count = line.decode('utf-8').split('\t')
        count = int(count)
        yield ngram, count
      except (ValueError, UnicodeDecodeError):
        continue
