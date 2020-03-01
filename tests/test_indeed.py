from scrapper.indeed import get_num_jobs, get_jobs_data
from scrapper.util import get_indeed_url
from scrapper.analyze import process_jobs
import argparse
import pytest
import os
def make_namespace(job):
  fake_args = argparse.Namespace()
  fake_args.input_city = 'Victoria'
  fake_args.input_state = 'BC'
  fake_args.input_quote = False
  fake_args.input_job = job
  fake_args.email_from = os.environ.get('INDEED_EMAIL')
  fake_args.email_password = os.environ.get('INDEED_PASSWORD')
  fake_args.email_to = os.environ.get('TEST_EMAIL', 'davidli012345@gmail.com')
  return fake_args

def test_get_num_jobs():
  indeed_url = get_indeed_url(make_namespace('Software Developer'))
  num_jobs = get_num_jobs(indeed_url)
  print(num_jobs)
  assert num_jobs > 0

def test_get_num_df():
  indeed_url = get_indeed_url(make_namespace('Software Developer'))
  num_jobs = get_num_jobs(indeed_url)
  job_data_df = get_jobs_data(indeed_url, num_jobs)
  assert job_data_df.shape[0] > 0

def test_get_num_jobs_fail():
  indeed_url = get_indeed_url(make_namespace('adsadsadsa Sofware developer king master  asdadsadsadsadasdasdsadsad'))
  with pytest.raises(Exception) as e:
    print(e)
    assert get_num_jobs(indeed_url)

def test_get_full_data():
  indeed_url = get_indeed_url(make_namespace('Senior Java Developer'))
  num_jobs = get_num_jobs(indeed_url)
  job_data_df = get_jobs_data(indeed_url, num_jobs)
  full_job_data_df = process_jobs(job_data_df)
  assert full_job_data_df.shape[0] > 5
