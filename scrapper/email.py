import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def send_email(args, jobs_df, metadata):
  # Try to login with gmail
  s = smtplib.SMTP(host='smtp.gmail.com', port=587)
  s.starttls()
  s.login(args.email_from, args.email_password)
  msg = MIMEMultipart()       # create a message
  # setup the parameters of the message
  msg['From']=args.email_from
  msg['To']=args.email_to
  msg['Subject']="Job Hunt Postings Indeed (Script)"
  # Add the list of search times and the url searched
  num_jobs = metadata.get("url_indeed", '')
  num_total_indeed = metadata.get("num_total_indeed",'')
  search_info = 'Searched at: %s \n Jobs: %f' % (num_jobs, num_total_indeed)
  search_info = MIMEText(search_info) # convert the body to a MIME compatible string
  msg.attach(search_info)

  # Add logic later if it seems important
  #if indeed_flag_jobs:
  ### Add list of skills and keywords 
  keywords_skills = """\
  <html>
    <head></head>
    <body>
      <h5> Potential Jobs </h5>
      {jobsTable}
    </body> 
  </html>
  """.format(jobsTable=jobs_df.to_html())
  keywords_skills = MIMEText(keywords_skills,'html')
  msg.attach(keywords_skills)
  s.send_message(msg)
