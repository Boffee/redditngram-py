import gzip
import itertools
import logging
import os

from collections import Counter

from redditngram import ngram_extract
from redditngram.data import paths


def count_reddit_comments_ngram_strs(year, month, n):
  """Count n-grams in reddit comments for month of year."""
  ngram_strs = ngram_extract.extract_reddit_comments_ngram_strs(year, month, n)
  return Counter(itertools.chain.from_iterable(ngram_strs))


def generate_reddit_comments_ngram_counts(
    year, month, n, root=paths.DEFAULT_REDDIT_NGRAMS_DATA):
  """Count and write n-gram in reddit comments for month of year."""
  ngram_path = paths.get_reddit_ngrams_local(year, month, n, root=root)
  if os.path.isfile(ngram_path):
    logging.warning("Cache exists for all requested n-grams."
                    "Skipping %04d-%02d\n" % (year, month))
    return False

  counts = count_reddit_comments_ngram_strs(year, month, n)
  with gzip.GzipFile(ngram_path, 'wb') as fh:
    for k, v in counts.items():
      fh.write("{}\t{}\n".format(k, v).encode())
  return True
