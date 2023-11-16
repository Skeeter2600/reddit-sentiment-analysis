#!/bin/bash
terraform destroy -auto-approve
terraform apply -auto-approve
OUTPUT=$(terraform output triggerurl)
TRIGGERURL=$(echo "$(echo $OUTPUT | tr -d '"')&operation=startbuild")
curl -X POST -d {} "${TRIGGERURL}" -H "Content-Type:application/json" -s > /dev/null