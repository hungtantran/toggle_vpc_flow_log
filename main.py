# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import googleapiclient.discovery

from flask import abort

def _validate_request(request_json):
    """Validate the given request json."""
    if not request_json:
        return False

    if (('enable' not in request_json) or
        (type(request_json['enable']) is not bool)):
        print('request must contain `enable` field of type boolean')
        return False

    if (('project' not in request_json) or
        (type(request_json['project']) is not str) or
        not request_json['project']):
        print('request must contain `project` field of type string')
        return False

    if (('region' not in request_json) or
        (type(request_json['region']) is not str) or
        not request_json['region']):
        print('request must contain `region` field of type string')
        return False

    if (('subnet' not in request_json) or
        (type(request_json['subnet']) is not str) or
        not request_json['subnet']):
        print('request must contain `subnet` field of type string')
        return False

    return True

def toggle_vpc_flow_log(request):
    """Enable/Disable VPC Flow Log for a given subnet.
    Args:
        request (flask.Request): contain json with 4 fields
        * enable: boolean whether to enable or disable vpc flow log
        * project: project id whose vpc flow log to be toggled
        * region: region of the subnet whose vpc flow log to be toggled
        * subnet: name of the subnet whose vpc flow log to be toggled
    Returns:
        True if the request
    """
    request_json = request.get_json(silent=True)

    if not _validate_request(request_json):
        return abort(500)

    enable = request_json['enable']
    project = request_json['project']
    region = request_json['region']
    subnet = request_json['subnet']

    compute = googleapiclient.discovery.build('compute', 'v1')

    subnetwork = compute.subnetworks().get(
        project=project, region=region, subnetwork=subnet).execute()

    body = {
        'enableFlowLogs': enable,
        'fingerprint': subnetwork['fingerprint']
    }
    compute.subnetworks().patch(
        project=project, region=region, subnetwork=subnet,
        body=body).execute()

    return "success"
