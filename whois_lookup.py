#!/usr/bin/python3

import requests
import json
import yaml
import smtplib
import ssl


# SETTINGS
key = 'UPDATE ME'
email = 'UPDATE ME'
password = 'UPDATE ME'
path = '/usr/src/app/'


# SEND EMAIL VIA GMAIL
# GMAIL SECURITY SETTING NEEDS TO BE ENABLED
def send_mail(message):
    context = ssl.create_default_context()  # CREATE SECURE CONTEXT (CERTIFICATES)
    port = 465  # FOR SSL
    smtp_server = 'smtp.gmail.com'

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(email, password)
        try:
            server.sendmail(email, email,
                            message)  # SEND EMAIL FROM MYSELF TO MYSELF
        except:
            print('Unable to send')
            server.close()


# DOMAIN LIST READER
def domain_reader():
    full_path = path + "domains.yml"
    with open(full_path, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


# QUERY API DATA
def api_query(name):
    base_url = 'https://www.whoisxmlapi.com/whoisserver/WhoisService?'
    apiKey = 'apiKey=' + key
    domain = f'&domainName={name}'
    format = '&outputFormat=JSON'
    full_url = base_url + apiKey + domain + format
    response = requests.get(full_url)
    return response.text


# FOR TESTING PURPOSES, READ DATA FROM FILE RATHER THAN API
# def file_reader(file):
#     with open(file, 'r') as h:
#         return h.read()


# SEARCH JSON DATA FOR DESIRED VALUE VIA json.loads object_hook
def find_values(id, json_repr):
    results = []

    def _decode_dict(a_dict):
        try:
            results.append(a_dict[id])
        except KeyError:
            pass
        return a_dict

    json.loads(json_repr, object_hook=_decode_dict)  # RETURN VALUE IGNORED
    return results


# GATHERING/SORTING API DATA INTO DICTIONARY
def organize_api_data(response):
    api_dict = {}

    for value in ['createdDate', 'updatedDate', 'expiresDate', 'registrarName', 'contactEmail', 'domainName']:
        try:
            api_dict[value] = find_values(value, response)[0]
        except:
            api_dict[value] = 'NOT FOUND'
    api_domain = api_dict['domainName']
    return api_dict, api_domain


# COMPARE STORED DATA WITH NEW DATA
# IF STORED DATA DOES NOT EXISTS, CREATE NEW FILE
# SEND EMAIL IF NEW DATA IS PRESENT
def compare_data(data, name):
    new_data = json.dumps(data, indent=2)
    file_name = f"{name.split('.')[0]}_data"
    full_path = path + file_name
    try:
        with open(full_path, 'r') as h:  # READ OLD DATA
            old_data = h.read()
        if old_data != new_data:  # COMPARE DATA
            with open(full_path, 'w') as h:  # UPDATE DATA
                h.write(new_data)
            send_mail(new_data)
        else:
            print(f'{file_name} was not updated')  # NOT UPDATED
    except:
        with open(full_path, 'w') as h:  # WRITE IF OLD DATA NOT FOUND
            h.write(new_data)
        send_mail(new_data)


if __name__ == '__main__':
    domain_list = domain_reader()  # GATHER DOMAINS

    for domain in domain_list['domains']:
        query_data = api_query(domain)  # QUERY API
        new_api_dict, new_api_domain = organize_api_data(query_data)  # BUILD JSON OF RESULTS

        # COMPARE OLD DATE WITH NEW AND UPDATE IF NEEDED
        # SEND EMAIL IF NEEDED
        compare_data(new_api_dict, new_api_domain)
