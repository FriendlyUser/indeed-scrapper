import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import base64
from mailjet_rest import Client
from scrapper.util import get_config
from ast import literal_eval
# TODO move to another package later
def generate_attachments(jobs_df):
  list_type = jobs_df['job_type'].tolist()
  list_skill = jobs_df['job_skills'].tolist()
  list_edu = jobs_df['job_edu'].tolist()
  list_keywords = jobs_df['job_keywords'].tolist()
  # implement later
  unique_data_type = set(x for l in list_type for x in l)
  unique_data_skills = set(x for l in list_skill for x in l)
  unique_data_edu = set(x for l in list_edu for x in l)
  unique_data_keywords = set(x for l in list_keywords for x in l)

  skills_dict={}
  for words in list_skill:
      for word in words:
          if not word in skills_dict:
              skills_dict[word]=1
          else:
              skills_dict[word]+=1
  # Calculate the frequency of keywords using a dataframe, consider adding plot or other data, perhaps save a csv and load it using d3
  result = pd.DataFrame()
  result['Skill'] = skills_dict.keys()
  result['Count'] = skills_dict.values()
  result['Ranking'] = result['Count']/float(len(list_skill))

  # Make another function
  results_dict={}
  for words in list_type:
      for word in words:
          if not word in results_dict:
              results_dict[word]=1
          else:
              results_dict[word]+=1
  # Calculate the frequency of keywords using a dataframe, consider adding plot or other data, perhaps save a csv and load it using d3
  result_type = pd.DataFrame()
  result_type['Type'] = results_dict.keys()
  result_type['Count'] = results_dict.values()
  result_type.set_index('Type') 

  results_dict={}
  for words in list_keywords:
      for word in words:
          if not word in results_dict:
              results_dict[word]=1
          else:
              results_dict[word]+=1
  # Calculate the frequency of keywords using a dataframe, consider adding plot or other data, perhaps save a csv and load it using d3
  result_keywords = pd.DataFrame()
  result_keywords['Keywords'] = results_dict.keys()
  result_keywords['Count'] = results_dict.values()

  result_keywords_html = result_keywords.to_html()

  matplotlib.use('Agg')
  skill_rank_plotname = 'skill-ranking.png'
  pie_plotname = 'pie.png'
  attachments_objs = []
  try:
    fig = plt.figure() # Create matplotlib figure
    default_size = fig.get_size_inches()
    ax = fig.add_subplot(111) # Create matplotlib axes
    ax2 = ax.twinx() # Create another axes that shares the same x-axis as ax.

    width = 0.4
    result.plot(x='Skill', y='Count', kind='bar', table=False, yerr=None,ax=ax, width=width, position=1,legend=False)
    result.plot(x='Skill', y='Ranking', kind='bar',table=False, yerr=None,ax=ax2, width=width, position=0,legend=False)

    ax.set_ylabel('Count')
    ax2.set_ylabel('Ranking')
    fig.set_size_inches((default_size[0]*2, default_size[1]*2))
    fig.tight_layout()
    ### This should be 2 x 2 times bigger, one 2 for dpi and one 2 for default size
    plt.savefig(skill_rank_plotname, dpi = 200)
  except Exception as e:
    print(e)
    print('Failed to make image for skill_rank')

  # On gitlab if there is a space in the file name, it doesn't send properly
  try:
    result_type.plot.pie(y='Count', labels=result_type['Type'], autopct='%1.1f%%', figsize=(5, 5))
    plt.savefig(pie_plotname, dpi = 200)
  except:
    print('Failed to make pie chart for type')
  for index, plot_file in enumerate([pie_plotname, skill_rank_plotname]):
    print(index)
    with open(plot_file, "rb") as img_file:
      base64_image = base64.b64encode(img_file.read())
    attachments_objs.append(
      {
        "ContentType": "image/png",
        "Filename": f"{plot_file}",
        "ContentID": f"id{index}",
        "Base64Content": base64_image.decode('ascii')
      }
    )
  return attachments_objs

def send_mailjet_email(jobs_df, metadata):
  api_key = os.environ['MJ_APIKEY_PUBLIC']
  api_secret = os.environ['MJ_APIKEY_PRIVATE']
  mailjet = Client(auth=(api_key, api_secret), version='v3.1')
  cfg = get_config()
  get_attachments = generate_attachments(jobs_df)
  keywords_skills = """\
    <div>
      <h4>Graphs</h4>
        <img src="cid:id0" alt = "Plot not generated" style="width:100%"/>
        <img src="cid:id1" alt = "Plot not made" style="width:100%"/>
      <h5> Potential Jobs </h5>
      {jobsTable}
    </div>
  """.format(jobsTable=jobs_df.to_html())
  data = {
    'Messages': [
      {
        "From": {
          "Email": cfg['email']['from'],
          "Name": "Indeed Scrapper"
        },
        "To": [
          {
            "Email": cfg['email']['to'],
            "Name": "Reciever Email"
          }
        ],
        "Subject": "Job Report",
        "HTMLPart": keywords_skills,
        "InlinedAttachments": get_attachments
      }
    ]
  }
  result = mailjet.send.create(data=data)
  print(result.status_code)
  print(result.json())
