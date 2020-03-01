import pandas as pd
import re
from scrapper.fetch_data import get_xml

# Get an analyzer class, espeically if I have all these hardcoded values
types = ['Full-Time', 'Full Time', 'Part-Time', 'Part Time', 'Contract', 'Contractor']
type_lower = [s.lower() for s in types] # lowercases
# map the type_lower to type
type_map = pd.DataFrame({'raw': types, 'lower':type_lower}) # create a dataframe
type_map['raw'] = ["Full-Time", "Full-Time", 'Part-Time', 'Part-Time', "Contract", 'Contract'] # modify the mapping
type_dic = list(type_map.set_index('lower').to_dict().values()).pop() # use the dataframe to create a dictionary
# print(type_dic)

##### Skills #####
skills = ['R', 'Shiny', 'RStudio', 'Markdown', 'Latex', 'SparkR', 'D3', 'D3.js',
            'Unix', 'Linux', 'MySQL', 'Microsoft SQL server', 'SQL',
            'Python', 'SPSS', 'SAS', 'C++', 'C', 'C#','Matlab','Java',
            'JavaScript', 'HTML', 'HTML5', 'CSS', 'CSS3','PHP', 'Excel', 'Tableau',
            'AWS', 'Amazon Web Services ','Google Cloud Platform', 'GCP',
            'Microsoft Azure', 'Azure', 'Hadoop', 'Pig', 'Spark', 'ZooKeeper',
            'MapReduce', 'Map Reduce','Shark', 'Hive','Oozie', 'Flume', 'HBase', 'Cassandra',
            'NoSQL', 'MongoDB', 'GIS', 'Haskell', 'Scala', 'Ruby','Perl',
            'Mahout', 'Stata','Solidity']
skills_lower = [s.lower() for s in skills]# lowercases
skills_map = pd.DataFrame({'raw':skills, 'lower':skills_lower})# create a dataframe
skills_dic = list(skills_map.set_index('lower').to_dict().values()).pop()# use the dataframe to create a dictionary
# print(skills_dic)

##### Education #####
edu = ['Bachelor', "Bachelor's", 'BS', 'B.S', 'B.S.', 'Master', "Master's", 'Masters', 'M.S.', 'M.S', 'MS',
        'PhD', 'Ph.D.', "PhD's", 'MBA']
edu_lower = [s.lower() for s in edu]# lowercases
edu_map = pd.DataFrame({'raw':edu, 'lower':edu_lower})# create a dataframe
edu_dic = list(edu_map.set_index('lower').to_dict().values()).pop()# use the dataframe to create a dictionary
# print(edu_dic)

##### Major #####
major = ['Computer Science', 'Statistics', 'Mathematics', 'Math','Physics',
            'Machine Learning','Economics','Software Engineering', 'Engineering',
            'Information System', 'Quantitative Finance', 'Artificial Intelligence',
            'Biostatistics', 'Bioinformatics', 'Quantitative']
major_lower = [s.lower() for s in major]# lowercases
major_map = pd.DataFrame({'raw':major, 'lower':major_lower})# create a dataframe
major_dic = list(major_map.set_index('lower').to_dict().values()).pop()# use the dataframe to create a dictionary

##### Key Words ######
# For AI and BCHAIN, put the keywords here, as I want to get into those areas
keywords = ['Blockchain','Hashgraph','Ethereum','Solidity','Truffle','Drizzle','Vyper','Smart Contract',
'Machine Learning','Deep Learning','Data Science','Big Data',
'Web Analytics', 'Regression', 'Classification', 'User Experience', 
            'Streaming Data', 'Real-Time', 'Real Time', 'Time Series']
keywords_lower = [s.lower() for s in keywords]# lowercases
keywords_map = pd.DataFrame({'raw':keywords, 'lower':keywords_lower})# create a dataframe
keywords_dic = list(keywords_map.set_index('lower').to_dict().values()).pop()# use the dataframe to create a dictionary

def process_type(indeed_string, data_list, data_dict)-> list:
  type_matches = []
  for typ in data_list:
    if any(x in typ for x in ['+', '#', '.']):
      typp = re.escape(typ) # make it possible to find out 'c++', 'c#', 'd3.js' without errors
    else:
      typp = typ
    result = re.search(r'(?:^|(?<=\s))' + typp + r'(?=\s|$)', indeed_string) # search the string in a string
    if result:
      type_matches.append(data_dict[typ])
  return type_matches

def process_jobs(job_df_indeed):
  ##############################################
  ##### For Loop for scraping each job URL #####
  ##############################################
  # empty list to store details for all the jobs
  list_type = []
  list_skill = []
  # list_text = []
  list_edu = []
  list_major = []
  list_keywords = []

  for i in range(len(job_df_indeed)):
    # empty list to store details for each job
    # TODO figure out what todo with this empty list
    required_type= []
    required_skills = []
    required_edu = []
    required_major = []
    required_keywords = []

    try:
      # get the HTML code from the URL
      job_url = job_df_indeed.iloc[i]['job_link']
      soup = get_xml(job_url)
      # drop the chunks of 'script','style','head','title','[document]'
      for elem in soup.findAll(['script','style','head','title','[document]']):
        elem.extract()
      # get the lowercases of the texts
      texts = soup.getText(separator=' ').lower()

      # cleaning the text data
      job_text = re.sub(r'[\n\r\t]', ' ', texts) # remove "\n", "\r", "\t"
      job_text = re.sub(r'\,', ' ', job_text) # remove ","
      job_text = re.sub('/', ' ', job_text) # remove "/"
      job_text = re.sub(r'\(', ' ', job_text) # remove "("
      job_text = re.sub(r'\)', ' ', job_text) # remove ")"
      job_text = re.sub(' +',' ',job_text) # remove more than one space
      job_text = re.sub(r'r\s&\sd', ' ', job_text) # avoid picking 'r & d'
      job_text = re.sub(r'r&d', ' ', job_text) # avoid picking 'r&d'
      job_text = re.sub('\.\s+', ' ', job_text) # remove "." at the end of sentences

      # Job types
      list_type.append(process_type(job_text, type_lower, type_dic))

      # Skills
      list_skill.append(process_type(job_text, skills_lower, skills_dic))

      # Education
      list_edu.append(process_type(job_text, edu_lower, edu_dic))

      # Major
      list_major.append(process_type(job_text, major_lower, major_dic))

      # Key Words
      list_keywords.append(process_type(job_text, keywords_lower, keywords_dic))

      # All text
      # words = string.split(' ')
      # job_text = set(words) - set(stop_words) # drop stop words
      # list_text.append(list(job_text))
    except Exception as e:
      print(e)
      list_type.append(['Forbidden'])
      list_skill.append(['Forbidden'])
      list_edu.append(['Forbidden'])
      list_major.append(['Forbidden'])
      list_keywords.append(['Forbidden'])
      # list_text.append('Forbidden')
    # print(i)

  job_df_indeed['job_type'] = list_type
  job_df_indeed['job_skills'] = list_skill
  job_df_indeed['job_edu'] = list_edu
  job_df_indeed['job_major'] = list_major
  job_df_indeed['job_keywords'] = list_keywords
  # job_df_indeed['job_text'] = list_text
  return job_df_indeed
