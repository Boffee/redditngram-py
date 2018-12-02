import re

DEFAULT_TOKEN_MAX_CHARS = 25


def extract_filtered_ngram_strs(text, n, tok_max_chars=DEFAULT_TOKEN_MAX_CHARS):
  """Extract n-grams split on whitespace and filtered by max length."""
  text_cleaned = re.sub(r'\s+', ' ', text)
  token_match_str = r'[^ ]{1,%d}' % tok_max_chars
  ngram_match_str = r'(?=[\^ ](%s)[\$ ])' % ' '.join([token_match_str] * n)
  return re.findall(ngram_match_str, text_cleaned)


def extract_filtered_ngram_strs_slow(text,
                                     n,
                                     tok_max_chars=DEFAULT_TOKEN_MAX_CHARS):
  """Extract filtered ngram strings using tokens."""
  ngrams = extract_ngrams(text, n)
  filtered_ngrams = filter(
      lambda ngram: not has_long_token(ngram, tok_max_chars=tok_max_chars),
      ngrams)
  filtered_ngram_strs = map(lambda ngram: ' '.join(ngram), filtered_ngrams)
  return filtered_ngram_strs


def extract_ngrams(text, n):
  """Extract n-gram token sequences from text."""
  tokens = text.split()
  return zip(*[tokens[i:] for i in range(n)])


def has_long_token(tokens, tok_max_chars=DEFAULT_TOKEN_MAX_CHARS):
  """Check if any token has more than `tok_max_chars`."""
  for tok in tokens:
    if len(tok) > tok_max_chars:
      return True
  return False