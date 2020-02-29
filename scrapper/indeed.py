import bs4
from scrapper.fetch_data import get_xml
from scrapper.util import largest_number
def get_num_jobs(url_indeed):
  indeed_data = get_xml(url_indeed)
  num_total_indeed  = indeed_data.find("div", {"id": "searchCount"})
  job_count_indeed = num_total_indeed.contents[0:3]
  job_number_str = ''
  for item in job_count_indeed:
    if type(item) is bs4.element.Tag:
      job_number_str += item.get_text()
  if job_number_str.split()[-1] == 'jobs':
    print('Found jobs at the end')
    num_total_indeed = largest_number(job_number_str)
  else:
    print('Expected to find job number')
    assert(False)
  return float(num_total_indeed)