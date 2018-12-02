import logging
import os
import requests

from multiprocessing import Pool
from multiprocessing.dummy import Pool as dPool
from tqdm import tqdm


def download(url, dest='/tmp/'):
  """Download with caching and progress bar."""
  filename = os.path.basename(url)
  if dest[-1] == '/' or os.path.isdir(dest):
    if not os.path.isdir(dest):
      os.makedirs(dest)
    dest = os.path.join(dest, filename)
  if os.path.isfile(dest):
    logging.info("{} already exist in {}.".format(url, dest))
  else:
    logging.info("Downloading {} to {}...".format(url, dest))
    resp = requests.get(url, stream=True)
    if not resp.ok:
      logging.warning("{}: {}".format(resp.reason, url))
      return False
    total_size = int(resp.headers.get('content-length', 0))
    block_size = 2**20
    with open(dest, 'wb') as fh:
      for data in tqdm(
          resp.iter_content(block_size),
          unit="MB",
          total=total_size // block_size):
        fh.write(data)
  return True


def multiproc_imap(func,
                   iterable,
                   processes=None,
                   thread_only=False,
                   total=None,
                   chunksize=1):
  """multi-thread/proc with progress bar."""
  pool_fn = dPool if thread_only else Pool
  pool = pool_fn(processes=processes)
  return tqdm(pool.imap(func, iterable, chunksize=chunksize), total=total)
