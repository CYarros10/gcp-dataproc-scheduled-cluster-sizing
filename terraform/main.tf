# Copyright 2022 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

provider "google" {
  project = var.project_id
  region  = var.region
}

module "scheduled-cluster-sizing" {
	source = "./modules/scheduled-cluster-sizing"
    project_id              = var.project_id
    app_id                  = var.app_id
    region                  = var.region
    cluster_name            = var.cluster_name
    instance_count          = var.instance_count
    service_account_email   = var.service_account_email
    schedule                = var.schedule
}
