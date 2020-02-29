import bs4
import pandas as pd
import math
from datetime import datetime
from scrapper.fetch_data import get_xml
from scrapper.util import largest_number
def get_num_jobs(url_indeed)-> int:
  indeed_data = get_xml(url_indeed)
  job_string  = indeed_data.find("div", {"id": "searchCount"})
  job_count_indeed = job_string.contents[0:3]
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
  # 
  total_jobs = float(num_total_indeed)
  return int(math.ceil(total_jobs / 10.0))

# TODO Get a config file
def get_jobs_data(url_indeed, num_pages, default_location='Victoria, BC'):
  BASE_URL_indeed = 'https://ca.indeed.com'
  # create an empty dataframe
  job_df_indeed = pd.DataFrame()
  # the date for today
  now = datetime.now()
  now_str = now.strftime("%m/%d/%Y")
  # now_str_name=now.strftime('%m%d%Y')
  # now_str_api=now.strftime('%Y-%d-%m')
  ########################################
  ##### Loop for all the total pages #####
  ########################################
  for i in range(1, num_pages+1):
    # generate the URL
    url = ''.join([url_indeed, '&start=', str(i*10)])
    print(url)

    # get the HTML code from the URL
    soup = get_xml(url)
    # pick out all the "div" with "class="job-row"
    divs = soup.findAll("div")
    job_divs = [jp for jp in divs if not jp.get('class') is None
                    and 'row' in jp.get('class')]

    # loop for each div chunk
    for job in job_divs:
      try:
        # job id
        id = job.get('data-jk', None)
        # job link related to job id
        link = BASE_URL_indeed + '/rc/clk?jk=' + id
        # job title
        title = job.find('a', attrs={'data-tn-element': 'jobTitle'}).attrs['title']
        # job company
        company = job.find('span', {'class': 'company'})
        if company is not None:
          company = company.text.strip()
        else:
          print('Company is missing')
        # job location
        location = job.find('span', {'class': 'location'})
        if location is not None:
          location = location.text.strip()
        else:
          location = default_location
          print('Location is missing')
      except Exception as e:
        print(e)
        exit()
        continue

      job_df_indeed = job_df_indeed.append({
        'job_title': title,
        'job_company': company,
        'job_location':location,
        'job_link':link},
      ignore_index=True)
  cols=['job_title','job_company','job_location','job_link']
  job_df_indeed = job_df_indeed[cols]
  # delete the duplicated jobs using job link
  job_df_indeed = job_df_indeed.drop_duplicates(['job_link'], keep='first')
  return job_df_indeed
