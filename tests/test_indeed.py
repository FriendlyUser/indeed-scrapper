from scrapper.indeed import get_num_jobs
from scrapper.util import get_indeed_url
import argparse

def make_namespace(job):
  fake_args = argparse.Namespace()
  fake_args.input_city = 'Victoria'
  fake_args.input_state = 'BC'
  fake_args.input_quote = False
  fake_args.input_job = job
  return fake_args

def test_get_num_jobs():
    indeed_url = get_indeed_url(make_namespace('Software Developer'))
    num_jobs = get_num_jobs(indeed_url)
    print(num_jobs)
    assert num_jobs > 0


def test_get_num_jobs_fail():
    indeed_url = get_indeed_url(make_namespace('Sofware developer king god monkey master'))
    try:
      num_jobs = get_num_jobs(indeed_url)
      assert False
    except Exception as e:
      assert True