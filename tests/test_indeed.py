from scrapper.indeed import get_num_jobs
from scrapper.util import get_indeed_url
import argparse
fake_args = argparse.Namespace()
fake_args.input_city = 'Victoria'
fake_args.input_state = 'BC'
fake_args.input_quote = False
def test_get_num_jobs():
    indeed_url = get_indeed_url(fake_args)
    num_jobs = get_num_jobs(indeed_url)
    print(num_jobs)
    assert num_jobs > 0
