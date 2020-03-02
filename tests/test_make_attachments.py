
from scrapper.email import generate_attachments, send_mailjet_email
import pandas as pd
def test_generate_plots():
  jobs_df = pd.read_csv('tests/sample_jobs.csv')
  sample_obj = generate_attachments(jobs_df)
  assert len(sample_obj) > 1
  # no errors here