import scrapper
import argparse
from scrapper import get_num_jobs, get_jobs_data, send_email
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
  send_email(args, finalized_df, metadata)

if __name__ == '__main__':
    
  # Instantiate the parser
  parser = argparse.ArgumentParser(description='Indeed Job Scrapper')

  ### Email login details
  # Required positional argument
  parser.add_argument('email_from', default="lidavid@uvic.ca",
                      help='Email address used to send csv to self')

  parser.add_argument('email_password', 
                      help="Email password for STMP (not secure)")

  parser.add_argument('email_to', default="studentdavidli@gmail.com",
                      help="Receiver of job posting report.")
                      
  ### Indeed Search Parameters
  # Optional argument
  parser.add_argument('--input_job', default="Developer",
                      help='String containing the kind of job, for example: Developer')

  # Optional positional argument
  parser.add_argument('--input_quote', default=False, action='store_false',
                      help='add quotation marks("") to your input_job')

  # Optional argument
  parser.add_argument('--input_city', default="Victoria",
                      help='city to search for postings in (Victoria, Vancouver, etc ...)')
                      
  parser.add_argument('--input_state', default="BC",
                      help='state to search for postings in (BC,Alberta)')

  parser.add_argument('--testing', default=False, type=lambda x: (str(x).lower() == 'true'))
  args = parser.parse_args()
  main(args)
