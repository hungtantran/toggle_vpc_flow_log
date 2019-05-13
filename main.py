import sys
import googleapiclient.discovery

def toggle_vpc_flow_log(data, context):
    """Enable/Disable VPC Flow Log for a given subnet.
    Args:
        data: contain json with 4 fields
        * enable: boolean whether to enable or disable vpc flow log
        * project: project id whose vpc flow log to be toggled
        * region: region of the subnet whose vpc flow log to be toggled
        * subnet: name of the subnet whose vpc flow log to be toggled
    Returns:
        True if the request
    """
    enable = data.get('enable')
    project = data.get('project')
    region = data.get('region')
    subnet = data.get('subnet')

    compute = googleapiclient.discovery.build('compute', 'v1')

    subnetwork = compute.subnetworks().get(
        project=project, region=region, subnetwork=subnet).execute()

    body = {
        'enableFlowLogs': enable,
        'fingerprint': subnetwork['fingerprint']
    }
    return compute.subnetworks().patch(
        project=project, region=region, subnetwork=subnet,
        body=body).execute()

