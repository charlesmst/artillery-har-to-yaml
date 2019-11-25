import json
import yaml
import sys
from urllib.parse import urlparse
from datetime import datetime
import config

def convert(input_har,output_yrml):
    with open(input_har,"r",encoding="utf8")  as har_file:
        json_text = har_file.read()
    root_url = None
    all_data = json.loads(json_text)
    entries = all_data["log"]["entries"]
    # print(entries[0])
    last_time = None
    cenario = []
    for entry in entries:
      
        request = entry["request"]
        method = request["method"]
        url = request["url"]
        if not root_url:
            parsed_uri = urlparse(url )
            root_url = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        url =  urlparse(url ).path
        if len([x for x in config.IGNORE_EXT if x in url]):
            continue
        #Add think between requests
        if config.CONVERT_THINK:
            time =  datetime.strptime(entry["startedDateTime"], "%Y-%m-%dT%H:%M:%S.%f%z")
            think =(time -  last_time).total_seconds() if last_time else 0
            last_time =  time

        if think > 0.5:
            cenario.append({"think":think})
        query_strings = request["queryString"]
        
        item_data = {"url":url}
        item = {}
        item[method.lower()] = item_data

        if "postData" in request and "json" in request["postData"]["mimeType"]:
            json_data = json.loads(request["postData"]["text"])
            item_data["json"] = json_data
        if "postData" in request and "x-www-form-urlencoded" in request["postData"]["mimeType"]:
            form_data_params = {}
            for param in request["postData"]["params"]:
                form_data_params[param["name"]] = param["value"]
            item_data["formData"] = form_data_params
        
            
        if query_strings:
            queries = {}
            for query_string in query_strings:
                queries[query_string["name"]] = query_string["value"]
            item_data["query"] = queries
        cenario.append(item) 

    with open(output_yrml, 'w') as file:
        documents = yaml.dump({
            "config":{
                "target":root_url,
                "phases":[{
                    "duration":10,
                    "arrivalRate":1
                }]
            },
            "scenarios":[{"flow":cenario}]
        }, file)

if __name__ == "__main__":
    convert(sys.argv[1],sys.argv[2])