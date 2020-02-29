from scrapper.indeed import get_num_jobs
from scrapper.util import get_indeed_url

fake_args = {'email_from': 'a', 'email_password': 'a', 'email_to': 'a', 'input_job': 'Developer', 'input_quote': False, 'input_city': 'Victoria', 'input_state': 'BC', 'testing': False}
def test_get_num_jobs():
    indeed_url = get_indeed_url(fake_args)
    num_jobs = get_num_jobs(indeed_url)
    print(num_jobs)
    assert num_jobs > 0
