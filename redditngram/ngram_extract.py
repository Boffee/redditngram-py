from redditngram.data import data_load
from redditngram.utils import ngram_utils

def extract_reddit_comments_upto_ngram_strs(year, month, n):
  """Extract 1- to n-gram simultaneously because file load is the bottleneck."""
  jsons = data_load.load_reddit_comments_json(year, month)
  texts = map(lambda d: d['body'], jsons)
  for text in texts:
    upto_ngram_strs = []
    for m in range(n):
      mgrams = ngram_utils.extract_filtered_ngram_strs(text, m)
      upto_ngram_strs.append(mgrams)
    yield upto_ngram_strs


def extract_reddit_comments_ngram_strs(year, month, n):
  """Extract n-grams from reddit comments from month of year."""
  jsons = data_load.load_reddit_comments_json(year, month)
  texts = map(lambda d: d['body'], jsons)
  ngram_strs = map(lambda s: ngram_utils.extract_filtered_ngram_strs(s, n),
                   texts)
  return ngram_strs
