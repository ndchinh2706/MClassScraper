import re
import json
import sys
import requests
import unicodedata
token = ""
sys.stdout = open("out.txt", 'w',encoding="utf8")
def parse_xclass_script(html_content):
    # Regex pattern to find the XCLASS object in the script
    xclass_match = re.search(r"var\s+XCLASS\s*=\s*({.*?});", html_content, re.DOTALL)
    
    if xclass_match:
        # Extract the XCLASS object as a string
        xclass_str = xclass_match.group(1)
        return xclass_str
    else:
        return ""
    
def multiline_to_singleline(json_str):
    try:
        json_obj = json.loads(json_str)  # Parse the JSON string
        single_line_json = json.dumps(json_obj, separators=(',', ':'))  # Convert back to string with no extra spaces
        return single_line_json
    except json.JSONDecodeError as e:
        return f"Invalid JSON: {e}"


url = "https://mclass.vn/course/T2K6C001/lesson/bai-toan-1-luy-thua-va-cac-cong-thuc-2"

payload = '_token={token}&play=1'
headers = {
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'accept-language': 'en-US,en;q=0.9',
  'cookie': '_ga=GA1.1.382263707.1724683831; cf_clearance=hm2g5ejFtmAkeQVdDjbZwPIKLxqGxmbcSqYos7espL0-1727163416-1.2.1.1-cCCF_qMwmRCJTySLLte_RUWsiN8_GWoa1GwBFAFq9Thb4aqzME12_CNN8UgiIVO9vPtmPSsmTYYhQK6V8hVVEJsw0zg4qQ2aErolMSJDnBmnxTL_wzcsFa7op0WmmF2Gr0IMxJEPugmJZkab2xah4Xxx7pAl9ERAJaKrgKWoxLOTX04X9xbKSVvmvSaLpsXQiOomR1H_41An3flIQ3BC3PZMqjR3efOSzfm1M7PUIICrBn1w21hKlieXM.r_navvmhchRYGlndRM6mkJxIZUnYWh5Zszg1FsG7zqFIG8w37NEgGjMPWAB_1aj1TnS5h_BmXuodlAkqX67IjowjFfkX8JDlmf5G4iBiAq3X8c0LDMsPl6ZW3PQ3dfdGu6MtGQZi9JVGrwDfwq39ygVJH_Kg; XSRF-TOKEN=eyJpdiI6Ik53UVpHRG5ua0FxalltOEs3UWdoN1E9PSIsInZhbHVlIjoiL3A4bEswSTlYTTNhT0tyTDRjZWFteElpdzVrcWhKUDkrc0tDKzNsS0xOMFhJWG5UcEdIM3RoWGxmVkNDbnh3NVFodUY4QVdYbWMxSFY5MlVpTXltL0FROFk3b3pnR21rRHBST3dYY1IvNnlaVUMwcmRuYVNRdnRwb0JuY0c3ZjAiLCJtYWMiOiI5NjNlMTQxN2E3ZWY2OTZkZDJiNzQ1Y2ZlNWMwYjg4MjhhZmI4YjUzYTFlYTAwMWI3NmE3ZDNkNmYwOTI3ZDNhIiwidGFnIjoiIn0%3D; mclass_session=eyJpdiI6ImFNdU1CK3p6MUh2bDg2dG1GcS8zbWc9PSIsInZhbHVlIjoiYzV2OFdCT0tTTnd2cEQ4K2NaQTkvT1NmSnlHS2ZtcGdtSllQOWRlTmRXcVJHRnpKQmZiLy9VdGRKdXN2Qjk2Q1NHdDQrbVVOTzlDZXJVTVMwR010MExHNkg2U2M2T0UxTzYrZ1ptMFpaNWVTWGlGYXBBNXZxb3E5cytKQlhTSVEiLCJtYWMiOiI5M2IzZWRjNTM2ODEyN2I3YjEyN2E5ZGM0ZWYzNjYwYzg2MTYwNzEwMzc1OWQwYzg4OGJhNTU5ODRlZDhlZWUyIiwidGFnIjoiIn0%3D; _ga_TB3KEYP7N7=GS1.1.1727163415.14.1.1727163514.57.0.0; XSRF-TOKEN=eyJpdiI6IjY3UmZpSk1ZNlYzOC9ZdmRHVkJDT1E9PSIsInZhbHVlIjoiR2hxTWNoNmJ4bXhYZkNiYlVEaVg0Sy9malRCMVduckdaVTFLTnR5cWYxS2U5VzBRK3NiNGJmajlUd3orUjJwa0JoZlp1Mi9pT3orY1VQTGtEWEtiRDhVRE1wM09TWVRXb0hrWVBWT3FyMWY0UzRMZnJ4ZG8wa05HY3RGQXNWZm8iLCJtYWMiOiIxNjJhYjMxYjNhNDYwZDdiZDZjZDkyOGE1YWZlODBkZmFlOTk5NGZmY2JiODBjYWQzNDc5MmJhZjllYTQ1ZGNlIiwidGFnIjoiIn0%3D; mclass_session=eyJpdiI6IlMrREtIYjBvbDZTSnByOXd5VFQ2V0E9PSIsInZhbHVlIjoidnFFa2s1Qk1Wd3BKa3drbzhLTEpIK3BFQnFyZlBMam5QQko5bk1valR1NlNqR1Z0VXM1WWNFaFRyRXdKTWp3ckRtV2xUK3FISjRXVk5tdjhPTFp2d2NBbm0vbnBjbmVaNjFiVnlGUjhTZXZWdWhmMTRuRkV5S3lCRTZLVWkrbzIiLCJtYWMiOiI4YzE2YmU4NmIyZmJlN2E2MzdhNmFlYjRjNzZiYjBlMDIzMjdmNTAyOGJmZjEyYWI1YTYyZGNmY2VmZGFhZGZiIiwidGFnIjoiIn0%3D',
  'priority': 'u=0, i',
  'referer': 'https://mclass.vn/course/T2K6C001/lesson/bai-toan-1-ki-thuat-xet-tinh-don-dieu-cua-ham-so-5',
  'sec-ch-ua': '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
  'Content-Type': 'application/x-www-form-urlencoded'
}


response = requests.request("GET", url, headers=headers, data=payload)
#datastring = open("C:\\Users\\Dinh\\Desktop\\response.html", 'r', encoding="utf8").read()
# Parse the XCLASS scriptc
parsed_data = parse_xclass_script(response.text)
parsed_data = parsed_data.replace("\"", "\'")
parsed_data = parsed_data.replace("csrf_token", "\"csrf_token\"")
parsed_data = parsed_data.replace("next", "\"next\"")
parsed_data = parsed_data.replace("\": '", "\": \"")
parsed_data = parsed_data.replace("',\n", "\",\n")
parsed_data = parsed_data.replace("    }", "}")
parsed_data = parsed_data.replace("]}\",", "]}\"")
json_string = multiline_to_singleline(parsed_data)
new_parse = json_string.split("\"next\":\"")
parse1 = new_parse[-1].split("\"}")[0]
next = multiline_to_singleline(parse1.replace("'", "\""))
#print(parse1)
#print(multiline_to_singleline(parse1))
# Load the JSON data
#json_string = json_string.replace("'", '"')
#print(json_string)
data = json.loads(json_string)
next_data = json.loads(next)
name = unicodedata.normalize('NFKC', next_data['name'])
alias = next_data['alias']
embed_video = next_data['embed_video']
document_files = next_data.get('document_files', [])
parsed_documents = [{'name': unicodedata.normalize('NFKC', doc['name']), 'url': doc['url']} for doc in document_files]
parsed_data = {
    'name': name,
    'alias': alias,
    'embed_video': embed_video,
    'document_files': parsed_documents
}
print(name, alias, embed_video, parsed_documents)

url_prefix = "https://mclass.vn/course/T2K6C001/lesson/"
while(alias != ""):
    try:
        url = url_prefix + alias
        response = requests.request("GET", url, headers=headers, data=payload)
        # Parse the XCLASS scriptc
        parsed_data = parse_xclass_script(response.text)
        parsed_data = parsed_data.replace("\"", "\'")
        parsed_data = parsed_data.replace("csrf_token", "\"csrf_token\"")
        parsed_data = parsed_data.replace("next", "\"next\"")
        parsed_data = parsed_data.replace("\": '", "\": \"")
        parsed_data = parsed_data.replace("',\n", "\",\n")
        parsed_data = parsed_data.replace("    }", "}")
        parsed_data = parsed_data.replace("]}\",", "]}\"")
        json_string = multiline_to_singleline(parsed_data)
        new_parse = json_string.split("\"next\":\"")
        parse1 = new_parse[-1].split("\"}")[0]
        next = multiline_to_singleline(parse1.replace("'", "\""))
        #print(parse1)
        #print(multiline_to_singleline(parse1))
        # Load the JSON data
        #json_string = json_string.replace("'", '"')
        #print(json_string)
        data = json.loads(json_string)
        next_data = json.loads(next)
        name = unicodedata.normalize('NFKC', next_data['name'])
        alias = next_data['alias']
        embed_video = next_data['embed_video']
        document_files = next_data.get('document_files', [])
        parsed_documents = [{'name': unicodedata.normalize('NFKC', doc['name']), 'url': doc['url']} for doc in document_files]
        parsed_data = {
            'name': name,
            'alias': alias,
            'embed_video': embed_video,
            'document_files': parsed_documents
        }
        print(name, alias, embed_video, parsed_documents)
    except:
        print(alias)
        break