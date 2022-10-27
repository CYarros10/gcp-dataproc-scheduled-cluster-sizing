#!/usr/bin/env python3
# encoding: utf-8

#    Copyright 2022 Google LLC
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
"""
Script that runs in Cloud Functions to describe all dataproc clusters and
generate spark property recommendations for these clusters.
"""

import os
import functions_framework
from google.cloud import dataproc_v1
from oauth2client.client import GoogleCredentials

_PROJECT_ID = os.environ.get('PROJECT_ID', 'Environment variable is not set.')
_REGION = os.environ.get('REGION', 'Environment variable is not set.')
_CLUSTER_NAME = os.environ.get('CLUSTER_NAME', 'Environment variable is not set.')
_INSTANCE_COUNT = str(os.environ.get('MIN_INSTANCE_COUNT', 'Environment variable is not set.'))


def sample_update_cluster():
    """This sample walks a user through updating a Cloud Dataproc cluster
    using the Python client library.
    Args:
        project_id (str): Project to use for creating resources.
        region (str): Region where the resources should live.
        cluster_name (str): Name to use for creating a cluster.
    """

    print(f"Beginning cluster update: {_CLUSTER_NAME}")

    # Create a client with the endpoint set to the desired cluster region.
    client = dataproc_v1.ClusterControllerClient(
        client_options={"api_endpoint": f"{_REGION}-dataproc.googleapis.com:443"}
    )

    # Get cluster you wish to update.
    cluster = client.get_cluster(
        project_id=_PROJECT_ID, region=_REGION, cluster_name=_CLUSTER_NAME
    )

    mask = {"paths": {"config.worker_config.num_instances": _MIN_INSTANCE_COUNT}}

    # Update cluster config
    cluster.config.worker_config.num_instances = int(_MIN_INSTANCE_COUNT)

    # Update cluster
    operation = client.update_cluster(
        project_id=_PROJECT_ID,
        region=_REGION,
        cluster=cluster,
        cluster_name=_CLUSTER_NAME,
        update_mask=mask,
    )

    # Output a success message.
    updated_cluster = operation.result()
    print(f"Cluster was updated successfully: {updated_cluster.cluster_name}")


@functions_framework.cloud_event
def execute(trigger):
    """
    Cloud Function entry point.
    """
    sample_update_cluster()