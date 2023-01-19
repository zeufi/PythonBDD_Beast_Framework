"""
- does not have the charts

"""
import shutil

import requests
from requests.auth import HTTPBasicAuth
import json
import argparse
from datetime import datetime
import os
import smtplib
from email.message import EmailMessage

myDate = datetime.now().strftime("%d-%m-%Y at %H-%M-%S")
myDate1 = "chr_result_{}".format(datetime.now().strftime("%Y%m%d"))
myDate2 = "ff_result_{}".format(datetime.now().strftime("%Y%m%d"))
auth_token = "Te68m0cO7rDdhfPfa4Cy1CF5"
basic_auth = HTTPBasicAuth('jojosongoas@gmail.com', auth_token)
# Set the title and content of the page to create
page_title = 'My New Page'
page_html = '<p>This page was created with Python!</p>'
parent_page_id = 16711845
space_key = 'QT'
url = 'https://nkuan.atlassian.net/wiki/rest/api/content/'
headers = {
    "Accept": "application/json",
    'Content-Type': 'application/json'
}


parser = argparse.ArgumentParser()
parser.add_argument('--input_json_file',
                    required=True,
                    help="Path of input json file. JSON file is output of Behave test run")
parser.add_argument('--output_html_file',
                    required=True,
                    help="Path of the output html file to be generated")

args = parser.parse_args()

input_file = args.input_json_file
output_html_path = args.output_html_file

file_path = os.getcwd()
files = os.path.join(os.getcwd())
if output_html_path == 'chrome_report_generator/chrome_report.html':
    src = os.path.join(files, myDate1, 'json_report_out.json')
    dst = os.path.join(files, 'report_generation')
    copy_out_dir = os.path.join(shutil.copy2(src, dst))
elif output_html_path == 'firefox_report_generator/firefox_report.html':
    src = os.path.join(files, myDate2, 'json_report_out.json')
    dst = os.path.join(files, 'report_generation')
    copy_out_dir = os.path.join(shutil.copy2(src, dst))

feature_count = 0
feature_failed_count = 0
feature_passed_count = 0
scenario_count = 0
scenario_failed_count = 0
scenario_passed_count = 0

report_styles = """
    <style>
        tr.feature {
            background: rgb(255,227,225);
        }
        td.scenario_td {
            width:50%;
        }

        td.status {
            width: 10%;
            }

        td.err_sc_name {
            max-width: 100%;
        }
        td.feature_td {
            min-width:50;
        }
        table, th, td {
            border: 1px solid rgb(26,122,222);
        }

    </style>

"""

report_javascript = """
    <script>
        function justalert(sc_name){
            var locator = 'tr.error_row[scenario_name="' + sc_name + '"]'
            var errRow = document.querySelector(locator)

            if ( errRow.style.display == "block") {
                errRow.style.display = "none";
            } else {
                errRow.style.display = "block";
            }
        }
    </script>
"""

all_rows1 = ""
feature_row_template1 = """<tr class="feature">
                            <td class="feature_td">
                            <strong>{fe_name}</strong>
                            </td>
                            <td class="status">
                            <span style="color: {feature_status_background};">{fe_status}</span>
                            </td>
                        </tr>"""

scenario_row_template1 = """<tr class="scenario" scenario_name="{sce_name}" onClick="{on_click}">    
                                <td class="scenario_td">{sce_name}</td>
                                <td class="status">
                                <span style="color: {sc_status_color}">{sce_status}</span>
                                </td>
                            </tr>"""

error_row_template1 = """<tr class="error_row" scenario_name="{sce_name}">
                            <td class="err_sc_name scenario_td">
                            <span style="color: rgb(255,170,170)">
                                {step_name}
                            </span>
                            </td>
                            <td>
                                {err}
                            </td>
                        </tr>"""

all_rows = ""
feature_row_template = """<tr class="feature">
                            <td class="feature_td">{fe_name}</td>
                            <td class="status" style="background: {feature_status_background};">{fe_status}</td>
                        </tr>"""

scenario_row_template = """<tr class="scenario" scenario_name="{sce_name}" onClick="{on_click}">    
                                <td class="scenario_td">{sce_name}</td>
                                <td class="status" style="color: {sc_status_color}; font-weight: 
                                {sc_status_font_weight}">{sce_status}</td>
                            </tr>"""

error_row_template = """<tr class="error_row" scenario_name="{sce_name}" style="background: #ffaaaa; display: none;">
                            <td class="err_sc_name scenario_td">{step_name}</td>
                            <td>{err}</td>
                        </tr>"""


def calculate_percent_passed():
    global scenario_failed_count
    global scenario_passed_count
    global scenario_count

    total_scenarios = scenario_failed_count + scenario_passed_count
    if total_scenarios != scenario_count:
        raise Exception("Number of total scenario count and failed + passed does not match.")
    try:
        pct_pass = round((scenario_passed_count / total_scenarios) * 100, 2)
    except ZeroDivisionError:
        pct_pass = 100

    return pct_pass


# read the report json file
with open(input_file) as f:
    reports = json.load(f)

for report in reports:
    # verify each dictionary in the list is a feature
    _type = report['keyword']
    if _type == 'Feature':
        feature = report
    else:
        raise Exception("Unexpected top level keyword '{}'. Only expected 'Feature'".format(_type))

    # update the count of features passed/failed
    if feature['status'] == 'passed':
        feature_passed_count += 1
        feature_status_background = 'rgb(165,241,165)'
    elif feature['status'] == 'failed':
        feature_failed_count += 1
        feature_status_background = 'rgb(255,170,170)'

    else:
        raise Exception(
            "Unexpected status for feature. Expected 'passed' or 'failed' but found '{}'".format(feature['status']))

    # add the feature as one row in the html table
    all_rows1 = all_rows1 + feature_row_template1.format(fe_name=feature['name'], fe_status=feature['status'],
                                                         feature_status_background=feature_status_background)
    feature_count += 1

    scenarios = feature['elements']
    for s in scenarios:
        s_type = s['type']
        if s_type == 'scenario':
            scenario = s
        else:
            raise Exception(
                "Unexpected 'type' in list of elements for feature. Expected 'scenario' but found '{}'".format(s_type))

        scenario_name = scenario['name'].strip()
        if scenario['status'] == 'passed':
            scenario_passed_count += 1
            scenario_count += 1
            on_click = 'na'
            sc_status_color = 'rgb(28,136,28)'
            sc_status_font_weight = 'none'
        elif scenario['status'] == 'failed':
            scenario_failed_count += 1
            scenario_count += 1
            on_click = "justalert('{}')".format(scenario_name)
            sc_status_color = 'rgb(255,0,0)'
            sc_status_font_weight = 'bold'
            # add the scenario row
            all_rows1 = all_rows1 + scenario_row_template1.format(on_click=on_click, sce_name=scenario_name,
                                                                  sce_status=scenario['status'].upper(),
                                                                  sc_status_color=sc_status_color,
                                                                  sc_status_font_weight=sc_status_font_weight)
        else:
            raise Exception(
                "Unexpected 'status' for scenario. Expected 'passed' or 'failed'. Actual: {}. Scenario name: {}".format(
                    scenario['status'], scenario_name))

# for the failed scenario the error needs to be added to the report so identify the step that failed and add the error
        if scenario['status'] == 'failed':
            steps = scenario['steps']

            for step in steps:
                try:
                    if step['result']['status'] == 'failed':
                        failed_step = step
                        break
                except:
                    pass
            else:
                raise Exception(
                    "There should be a failed step but none found in list of steps for scenario."
                    "Scenario name: {}".format(scenario_name))

            # add the error detail row
            all_rows1 = all_rows1 + error_row_template1.format(sce_name=scenario_name,
                                                               step_name=failed_step['keyword'] + ":" + failed_step[
                                                                   'name'],
                                                               err='<br />'.join(
                                                                   failed_step['result']['error_message']))

for report in reports:
    # verify each dictionary in the list is a feature
    _type = report['keyword']
    if _type == 'Feature':
        feature = report
    else:
        raise Exception("Unexpected top level keyword '{}'. Only expected 'Feature'".format(_type))

    # update the count of features passed/failed
    if feature['status'] == 'passed':
        feature_status_background = '#a5f1a5'
    elif feature['status'] == 'failed':
        feature_status_background = '#ffaaaa'

    else:
        raise Exception(
            "Unexpected status for feature. Expected 'passed' or 'failed' but found '{}'".format(feature['status']))

    # add the feature as one row in the html table
    all_rows = all_rows + feature_row_template.format(fe_name=feature['name'], fe_status=feature['status'],
                                                      feature_status_background=feature_status_background)

    scenarios = feature['elements']
    for s in scenarios:
        s_type = s['type']
        if s_type == 'scenario':
            scenario = s
        else:
            raise Exception(
                "Unexpected 'type' in list of elements for feature. Expected 'scenario' but found '{}'".format(s_type))

        scenario_name = scenario['name'].strip()
        if scenario['status'] == 'passed':
            on_click = 'na'
            sc_status_color = '#1c881c'
            sc_status_font_weight = 'none'
        elif scenario['status'] == 'failed':
            on_click = "justalert('{}')".format(scenario_name)
            sc_status_color = 'red'
            sc_status_font_weight = 'bold'

        else:
            raise Exception(
                "Unexpected 'status' for scenario. Expected 'passed' or 'failed'. Actual: {}. Scenario name: {}".format(
                    scenario['status'], scenario_name))

        # add the scenario row
        all_rows = all_rows + scenario_row_template.format(on_click=on_click, sce_name=scenario_name,
                                                           sce_status=scenario['status'].upper(),
                                                           sc_status_color=sc_status_color,
                                                           sc_status_font_weight=sc_status_font_weight)

# for the failed scenario the error needs to be added to the report so identify the step that failed and add the error
        if scenario['status'] == 'failed':
            steps = scenario['steps']

            for step in steps:
                try:
                    if step['result']['status'] == 'failed':
                        failed_step = step
                        break
                except:
                    pass
            else:
                raise Exception(
                    "There should be a failed step but none found in list of steps for scenario. "
                    "Scenario name: {}".format(
                        scenario_name))

            # add the error detail row
            all_rows = all_rows + error_row_template.format(sce_name=scenario_name,
                                                            step_name=failed_step['keyword'] + ":" + failed_step[
                                                                'name'],
                                                            err='<br>'.join(failed_step['result']['error_message']))

# Build the report summary
percent_passed = calculate_percent_passed()

# parser = argparse.ArgumentParser()
# parser.add_argument("--output_html_file", help="Name of the user")
# args = parser.parse_args()
# # file = os.path.join(os.path.join(os.getcwd()), 'chrome_report_generator', 'out.html'
#
# def title():
#
#     global set_title
#     if args.output_html_file == 'chrome_report_generator/chrome_report.html':
#         set_title = "Chrome ATR generated the{}".format(myDate)
#     elif args.output_html_file == 'chrome_report_generator/chrome_report.html':
#         set_title = "Firefox ATR generated the{}".format(myDate)
#     else:
#         print("Name not passed through parser. Please check if the name is correct")
#     return set_title

if output_html_path == 'chrome_report_generator/chrome_report.html':
    data = {
        "title": "Chrome ATR generated the{}".format(myDate),
        "type": "page",
        "space": {
            "key": space_key
        },
        "ancestors": [{
            "id": parent_page_id
        }],
        "status": "current",
        "body": {
            "storage": {
                "value": f"""
    <h1> Scenario Pass Rate: {percent_passed}% ({scenario_passed_count}/{(scenario_failed_count
                                                                          + scenario_passed_count)})
    <ac:layout>
      <ac:layout-section ac:type="two_equal">
        <ac:layout-cell>
          <ac:structured-macro ac:name="chart">
      <ac:parameter ac:name="title">Pie</ac:parameter>
      <ac:parameter ac:name="type">pie</ac:parameter>
      <ac:rich-text-body>
        <table>
          <tbody>
            <tr>
              <th>
                <p>Status Type</p>
              </th>
              <th>
                <p>Passed</p>
              </th>
              <th>
                <p>Failed</p>
              </th>
            </tr>
            <tr>
              <th>
                <p>Scenario Passed and Failed</p>
              </th>
              <td>
                <p>{scenario_passed_count}</p>
              </td>
              <td>
                <p>{scenario_failed_count}</p>
              </td>
            </tr>
          </tbody>
        </table>
      </ac:rich-text-body>
    </ac:structured-macro>
        </ac:layout-cell>
        <ac:layout-cell>
          <ac:macro ac:name="chart">
      <ac:parameter ac:name="title">Bar</ac:parameter>
      <ac:parameter ac:name="type">bar</ac:parameter>
      <ac:rich-text-body>
        <table>
          <tbody>
            <tr>
              <th>
                <p>Status Type</p>
              </th>
              <th>
                <p>2023</p>
              </th>
              <th>
                <p>2024</p>
              </th>
            </tr>
            <tr>
              <th>
                <p>Passed</p>
              </th>
              <td>
                <p>{scenario_passed_count}</p>
              </td>
              <td>
                <p>0</p>
              </td>
            </tr>
            <tr>
              <th>
                <p>Failed</p>
              </th>
              <td>
                <p>{scenario_failed_count}</p>
              </td>
              <td>
                <p>0</p>
              </td>
            </tr>

          </tbody>
        </table>
      </ac:rich-text-body>
    </ac:macro>
        </ac:layout-cell>
      </ac:layout-section>
    </ac:layout>

    </h1>
    <table class="table-summary">
        <tr><th></th><th style="text-align: center;">PASSED</th>
        <th style="text-align: center;">FAILED</th>
        <th style="text-align: center;">PASS RATE</th>
        </tr>
        <tbody>
            <tr class="Jojo">
                <th style="text-align: center;">Features</th>
                <td class="status" style="text-align: center;">
                <span style="color: rgb(0,102,51);">{feature_passed_count}</span>
                </td>
                <td style="text-align: center;">
                <span style="color: rgb(255,0,0);">{feature_failed_count}</span>
                </td>
                <td style="text-align: center;">{round(
                    feature_passed_count / (scenario_failed_count + feature_passed_count), 2) * 100} %</td>
            </tr>
            <tr>
                <th style="text-align: center;">Scenario</th>
                <td style="text-align: center;">
                <span style="color: rgb(0,102,51);">{scenario_passed_count}</span>
                </td>
                <td style="text-align: center;">
                <span style="color: rgb(255,0,0);">{scenario_failed_count}</span>
                </td>
                <td style="text-align: center;">{round(
                    scenario_passed_count / (scenario_failed_count + scenario_passed_count), 2) * 100} %</td>
            </tr>
        </tbody>
    </table>
    <h3>Test failed Details</h3> 
    {report_javascript}
    """,
                "representation": "storage"
            }
        },
        "version": {
            "number": 4
        },
        "metadata": {
            "properties": {
                "editor": {
                    "value": "v2"
                }
            }
        }
    }
elif output_html_path == 'firefox_report_generator/firefox_report.html':
    data = {
        "title": "Firefox ATR generated the{}".format(myDate),
        "type": "page",
        "space": {
            "key": space_key
        },
        "ancestors": [{
            "id": parent_page_id
        }],
        "status": "current",
        "body": {
            "storage": {
                "value": f"""
        <h1> Scenario Pass Rate: {percent_passed}% ({scenario_passed_count}/{(scenario_failed_count
                                                                              + scenario_passed_count)})
        <ac:layout>
          <ac:layout-section ac:type="two_equal">
            <ac:layout-cell>
              <ac:structured-macro ac:name="chart">
          <ac:parameter ac:name="title">Pie</ac:parameter>
          <ac:parameter ac:name="type">pie</ac:parameter>
          <ac:rich-text-body>
            <table>
              <tbody>
                <tr>
                  <th>
                    <p>Status Type</p>
                  </th>
                  <th>
                    <p>Passed</p>
                  </th>
                  <th>
                    <p>Failed</p>
                  </th>
                </tr>
                <tr>
                  <th>
                    <p>Scenario Passed and Failed</p>
                  </th>
                  <td>
                    <p>{scenario_passed_count}</p>
                  </td>
                  <td>
                    <p>{scenario_failed_count}</p>
                  </td>
                </tr>
              </tbody>
            </table>
          </ac:rich-text-body>
        </ac:structured-macro>
            </ac:layout-cell>
            <ac:layout-cell>
              <ac:macro ac:name="chart">
          <ac:parameter ac:name="title">Bar</ac:parameter>
          <ac:parameter ac:name="type">bar</ac:parameter>
          <ac:rich-text-body>
            <table>
              <tbody>
                <tr>
                  <th>
                    <p>Status Type</p>
                  </th>
                  <th>
                    <p>2023</p>
                  </th>
                  <th>
                    <p>2024</p>
                  </th>
                </tr>
                <tr>
                  <th>
                    <p>Passed</p>
                  </th>
                  <td>
                    <p>{scenario_passed_count}</p>
                  </td>
                  <td>
                    <p>0</p>
                  </td>
                </tr>
                <tr>
                  <th>
                    <p>Failed</p>
                  </th>
                  <td>
                    <p>{scenario_failed_count}</p>
                  </td>
                  <td>
                    <p>0</p>
                  </td>
                </tr>

              </tbody>
            </table>
          </ac:rich-text-body>
        </ac:macro>
            </ac:layout-cell>
          </ac:layout-section>
        </ac:layout>

        </h1>
        <table class="table-summary">
            <tr><th></th><th style="text-align: center;">PASSED</th>
            <th style="text-align: center;">FAILED</th>
            <th style="text-align: center;">PASS RATE</th>
            </tr>
            <tbody>
                <tr class="Jojo">
                    <th style="text-align: center;">Features</th>
                    <td class="status" style="text-align: center;">
                    <span style="color: rgb(0,102,51);">{feature_passed_count}</span>
                    </td>
                    <td style="text-align: center;">
                    <span style="color: rgb(255,0,0);">{feature_failed_count}</span>
                    </td>
                    <td style="text-align: center;">{round(
                    feature_passed_count / (scenario_failed_count + feature_passed_count), 2) * 100} %</td>
                </tr>
                <tr>
                    <th style="text-align: center;">Scenario</th>
                    <td style="text-align: center;">
                    <span style="color: rgb(0,102,51);">{scenario_passed_count}</span>
                    </td>
                    <td style="text-align: center;">
                    <span style="color: rgb(255,0,0);">{scenario_failed_count}</span>
                    </td>
                    <td style="text-align: center;">{round(
                    scenario_passed_count / (scenario_failed_count + scenario_passed_count), 2) * 100} %</td>
                </tr>
            </tbody>
        </table>
        <h3>Test failed Details</h3> 
        {report_javascript}
        """,
                "representation": "storage"
            }
        },
        "version": {
            "number": 4
        },
        "metadata": {
            "properties": {
                "editor": {
                    "value": "v2"
                }
            }
        }
    }
else:
    print("Name not passed through parser.")

try:
    r = requests.post(url=url, data=json.dumps(data), headers=headers, auth=basic_auth)
    # Consider any status other than 2xx an error
    if not r.status_code // 100 == 2:
        print("Error: Unexpected response {}".format(r))
    else:
        print('Confluence Page Created!')
except requests.exceptions.RequestException as e:
    # A serious problem happened, like an SSLError or InvalidURL
    print("Error: {}".format(e))

report_html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    {report_styles}
    <title>My Test Report</title>
</head>
<body>
<div id="test_summary">
         <h1> Scenario Pass Rate: {percent_passed}% ({scenario_passed_count}/{(
        scenario_failed_count + scenario_passed_count)})</h1>
<table class="table-summary">
    <thead><th></th><th>PASSED</th><th>FAILED</th><th>PASS RATE</th></thead>
    <tbody>
        <tr>
            <th>Features</th><td style="color:green"><center>{feature_passed_count}</center></td>
            <td style="color:red"><center>{feature_failed_count}</center></td>
            <td><center>{round(feature_passed_count / (scenario_failed_count +
                                                       feature_passed_count), 2) * 100} %</center></td>
        </tr>
        <tr>
            <th>Scenario</th><td style="color:green"><center>{scenario_passed_count}</center></td>
            <td style="color:red"><center>{scenario_failed_count}</center></td>
            <td><center>{round(scenario_passed_count / (scenario_failed_count +
                                                        scenario_passed_count), 2) * 100} %</center></td>
        </tr>
    </tbody>
</table>
</div>
<br>
<table>
    <thead></thead>
    <tbody>
    {all_rows}
    </tbody>

</table>
{report_javascript}
    <table>
        <thead></thead>
        <tbody>
        {all_rows1}
        </tbody>
    </table>
</body>
</html>"""

# # reate the final report html
with open(output_html_path, 'w') as f:
    f.write(report_html_template)

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

contacts = ['zeufackjojo@yahoo.fr', 'jojo.zeufacksongoa@postecert.it', 'jojosongoas@gmail.com']
msg = EmailMessage()
msg['Subject'] = 'Check out attached as a followUp!'
msg['From'] = EMAIL_ADDRESS
msg['To'] = contacts
msg.set_content('This is a test text email .....')
msg.add_alternative("""\
<!DOCTYPE html>
<html>
    <body>
        <h1 style="color:SlateGray;">This is an HTML Email!</h1>
    </body>
</html>
""", subtype='html')
# files = ['C:\\Users\\agsuser\\Desktop\\New folder\\1.PNG', 'C:\\Users\\agsuser\\Desktop\\New folder\\2.PNG',
#         'C:\\Users\\agsuser\\Desktop\\New folder\\3.PNG', 'C:\\Users\\agsuser\\Desktop\\New folder\\4.PNG',
#         'C:\\Users\\agsuser\\Desktop\\New folder\\5.PNG']

# To send a single file present in a folder with other files
files = os.path.join(os.getcwd())
file = os.path.join(files, 'chrome_report_generator', 'chrome_report.html')
with open(file, 'rb') as f:
    file_data = f.read()
    file_name = f.name
msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

"""
# To send all files present in a folder
files = [my_file for my_file in os.listdir() if os.path.isfile(my_file)]
for file in files:
    with open(file, 'rb') as f:
        file_data = f.read()
        file_name = f.name
        #file_type = imghdr.what(f.name)
    #msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)
    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
"""
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)

print("***************************")
print("Feature count: {}".format(feature_count))
print("feature_failed_count: {}".format(feature_failed_count))
print("feature_passed_count: {}".format(feature_passed_count))
print("scenario_count: {}".format(scenario_count))
print("scenario_failed_count: {}".format(scenario_failed_count))
print("scenario_passed_count: {}".format(scenario_passed_count))
print("Output html: {}".format(output_html_path))
print("***************************")
