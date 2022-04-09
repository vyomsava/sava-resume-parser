import nltk
nltk.download('stopwords')

from pyresparser import ResumeParser
import os
from pyairtable import Table
from pyairtable import Table
from pyairtable.formulas import match
import os
import wget
r = os.path.abspath(os.curdir)

table = Table("keyskn6UOjaF2EoBS", "appLJ6TtlvQ20lBlj", "MASTER")
formula = match({"parse_resume": "true"})
result = table.all(formula=formula)

if not result:
  exit()
else:
  list = []
  for i in result:
    list.append({"id": i['fields']['ID'], "resume": i['fields']['Resume'][0]['url']})

  for i in list:
    filepath = wget.download(i["resume"], out = r)
    data = ResumeParser(filepath).get_extracted_data()
    name = data['name'].lower()
    email = data['email'] 
    phone_un = data['mobile_number'].replace(" ", "")
    if len(phone_un) <= 10:
      phone = "+91" + phone_un
    else: phone = phone_un
    table.update(i["id"], {"Email": email, "Name": name, "Phone": phone, "parse_resume": "false"})
    os.remove(filepath)
    exit()