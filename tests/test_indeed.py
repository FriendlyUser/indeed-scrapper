from scrapper.indeed import get_num_jobs, get_jobs_data
from scrapper.util import get_indeed_url
import argparse
import pytest
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

def test_get_num_df():
  indeed_url = get_indeed_url(make_namespace('Software Developer'))
  num_jobs = get_num_jobs(indeed_url)
  job_df = get_jobs_data(indeed_url, num_jobs)
  assert job_df.count > 0

def test_get_num_jobs_fail():
  indeed_url = get_indeed_url(make_namespace('adsadsadsa Sofware developer king god monkey master  asdadsadsadsadasdasdsadsad'))
  with pytest.raises(Exception) as e:
    assert get_num_jobs(indeed_url)

job_info = "https://ca.indeed.com/job/senior-java-developer-6d6b91c475780e06"