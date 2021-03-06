#!/usr/bin/env python
#tlsrpt_processor
#Copyright 2018 Comcast Cable Communications Management, LLC
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
#See the License for the specific language governing permissions and
#limitations under the License
#
#This product includes software developed at Comcast ( http://www.comcast.com/)
#
#
# Author: Alex Brotman (alex_brotman@comcast.com)
#
# Purpose: Parse a TLSRPT report, and output as specified
#
# Notes: RFC-TBD
#
# URL: https://github.com/Comcast/tlsrpt_processor/
#

import json,sys,getopt,time

def show_help():
  print("")
  print("This script should process a TLSRPT JSON file pass as an argument")
  print("Options are as follows:")
  print("-h\t\t\t\tShow this help message")
  print("-i/-input\t\t\tInput file")
  print("-o/-output-style\t\tOutput Style (values: kv,csv)")
  print("")

def main(argv):
  try:
    opts, args = getopt.getopt(argv, "i:o:h",["input=","output-style=","help"])
  except getopt.GetoptError as err:
    print str(err)
    print show_help()
    sys.exit(2)
  input_file = None
  output_style = None
  for o,a in opts:
    if o in ("-h","-help"):
      show_help()
      sys.exit()
    elif o in ("-i","-input"):
      input_file = a
    elif o in ("-o","-output-style"):
      output_style = a
      if a not in ("kv","csv"):
        show_help()
        sys.exit(1)
    else:
      assert False, "Unrecognized option"
  
  if input_file is None:
    print("\nERROR: Input file is required")
    show_help()
    sys.exit(1)
  
  
  try:
    open(input_file,"r")
  except IOError:
    print("Input File does not exist or does not have the proper permissions")
    sys.exit(1)
  
  process_time = "%15.0f" % time.time()
  process_time = process_time.strip()
  csv_separator = "|"
  
  with open(input_file) as json_file:
    try:
      data = json.load(json_file)
    except ValueError as e:
      print("Invalid JSON file: %s" % e)
      sys.exit(1)
  
  
    organization_name = data.get("organization-name", "")
    start_date_time = data.get("date-range", {}).get("start-datetime", "")
    end_date_time = data.get("date-range", {}).get("end-datetime", "")
    contact_info = data.get("contact-info", "")
    email_address = data.get("email-address", "")
    report_id = data.get("report-id", "")
  
    for policy_set in data.get("policies", []):
      policy_type = policy_set.get("policy", {}).get("policy-type", "")
      policy_string = policy_set.get("policy", {}).get("policy-string", "")
      policy_domain = policy_set.get("policy", {}).get("policy-domain", "")
      policy_mx_host = policy_set.get("policy", {}).get("policy-mx-host", "")
      policy_success_count = policy_set.get("summary", {}).get("total-successful-session-count", 0)
      policy_failure_count = policy_set.get("summary", {}).get("total-failure-session-count", 0)
  
      for failure_details_set in policy_set.get("failure-details", []):
        result_type = failure_details_set.get("result-type", "")
        sending_ip = failure_details_set.get("sending-mta-ip", "")
        receiving_mx_hostname = failure_details_set.get("receiving-mx-hostname", "")
        receiving_mx_helo = failure_details_set.get("receiving-mx-helo", "")
        receiving_ip = failure_details_set.get("receiving-ip", "")
        failed_session_count = failure_details_set.get("failed-session-count", 0)
        additional_info = failure_details_set.get("additional-information", "")
        failure_error_code = failure_details_set.get("failure-error-code", "")
  
        if output_style in ('kv'):
  
          sys.stdout.write('process-time="' + process_time + '"')
          sys.stdout.write(' report-id="' + report_id + '"')
          sys.stdout.write(' organization-name="' + organization_name + '"')
          sys.stdout.write(' start-date-time="' + start_date_time + '"')
          sys.stdout.write(' end-date-time="' + end_date_time + '"')
          sys.stdout.write(' contact-info="' + contact_info + '"')
          sys.stdout.write(' email-address="' + email_address + '"')
          sys.stdout.write(' policy-type="' + policy_type + '"')
          sys.stdout.write(' policy-string="' + ",".join(policy_string) + '"')
          sys.stdout.write(' policy-domain="' + policy_domain + '"')
          sys.stdout.write(' policy-mx-host="' + policy_mx_host + '"')
          sys.stdout.write(' policy-success-count="' + str(policy_success_count) + '"')
          sys.stdout.write(' policy-failure-count="' + str(policy_failure_count) + '"')
          sys.stdout.write(' result-type="' + result_type + '"')
          sys.stdout.write(' sending-ip="' + sending_ip + '"')
          sys.stdout.write(' receiving-mx-hostname="' + receiving_mx_hostname + '"')
          sys.stdout.write(' receiving-mx-helo="' + receiving_mx_helo + '"')
          sys.stdout.write(' receiving-ip="' + receiving_ip + '"')
          sys.stdout.write(' failed-count="' + str(failed_session_count) + '"')
          sys.stdout.write(' additional-info="' + additional_info + '"')
          sys.stdout.write(' failure-error-code="' + failure_error_code + '"')
  
        elif output_style in ('csv'):
  
          sys.stdout.write(process_time + csv_separator)
          sys.stdout.write(report_id + csv_separator)
          sys.stdout.write('"' + organization_name + '"' + csv_separator)
          sys.stdout.write(start_date_time + csv_separator)
          sys.stdout.write(end_date_time + csv_separator)
          sys.stdout.write(contact_info + csv_separator)
          sys.stdout.write(email_address + csv_separator)
          sys.stdout.write(policy_type + csv_separator)
          sys.stdout.write('"' + csv_separator.join(policy_string) + '"' + csv_separator)
          sys.stdout.write(policy_domain + csv_separator)
          sys.stdout.write('"' + policy_mx_host + '"' + csv_separator)
          sys.stdout.write(str(policy_success_count) + csv_separator)
          sys.stdout.write(str(policy_failure_count) + csv_separator)
          sys.stdout.write(result_type + csv_separator)
          sys.stdout.write(sending_ip + csv_separator)
          sys.stdout.write(receiving_mx_hostname + csv_separator)
          sys.stdout.write(receiving_mx_helo + csv_separator)
          sys.stdout.write(receiving_ip + csv_separator)
          sys.stdout.write(str(failed_session_count) + csv_separator)
          sys.stdout.write('"' + additional_info + '"' + csv_separator)
          sys.stdout.write(failure_error_code)
  
        else:
          print "Unrecognized output style"
        sys.stdout.write('\n')

if __name__ == "__main__":
    main(sys.argv[1:])
