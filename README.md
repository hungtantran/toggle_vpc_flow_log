This repository contains code for GCP Cloud Function to enable/disable VPC Flow Log for a given project, region and subnet.

To deploy the Cloud Function

```bash
> gcloud functions deploy toggle_vpc_flow_log --runtime python37 --trigger-http
```

To trigger the Cloud Function

```bash
> gcloud functions call toggle_vpc_flow_log --data '{"enable":true/false, "subnet":<subnet name>, "project":<project name>, "region":<region name>}'
```
