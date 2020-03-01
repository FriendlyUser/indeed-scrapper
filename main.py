import scrapper
import argparse
from scrapper import get_num_jobs, get_jobs_data, send_mailjet_email
from scrapper.util import get_indeed_url
from scrapper import process_jobs
def main(args):
  url_indeed = get_indeed_url(args)
  # Get number of jobs from indeed
  num_jobs = get_num_jobs(url_indeed)
  job_df = get_jobs_data(url_indeed, num_jobs, 'Victoria, BC')
  finalized_df = process_jobs(job_df)
  metadata = {
    "url_indeed": url_indeed,
    "num_total_indeed": num_jobs
  }
  send_mailjet_email(finalized_df, metadata)

if __name__ == '__main__':
    
  # Instantiate the parser
  parser = argparse.ArgumentParser(description='Indeed Job Scrapper')

  ### Indeed Search Parameters
  parser.add_argument('--input_job', default="Developer",
                      help='String containing the kind of job, for example: Developer')
  parser.add_argument('--input_quote', default=False, action='store_false',
                      help='add quotation marks("") to your input_job')
  parser.add_argument('--input_city', default="Victoria",
                      help='city to search for postings in (Victoria, Vancouver, etc ...)')    
  parser.add_argument('--input_state', default="BC",
                      help='state to search for postings in (BC,Alberta)')
  
  args = parser.parse_args()
  main(args)
