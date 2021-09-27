#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = r"""
---
module: power_panel
short_description: Create, update or delete power panels within Nautobot
description:
  - Creates, updates or removes power panels from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Tobias Groß (@toerb)
requirements:
  - pynautobot
version_added: "1.0.0"
options:
  url:
    description:
      - URL of the Nautobot instance resolvable by Ansible control host
    required: true
    type: str
  token:
    description:
      - The token created within Nautobot to authorize API access
    required: true
    type: str
  data:
    type: dict
    required: true
    description:
      - (deprecated) In the next version of the modules the `data` option will be removed. All sub options will now be an option of the module.
      - Defines the power panel configuration
    suboptions:
      site:
        description:
          - The site the power panel is located in
        required: true
        type: raw
      rack_group:
        description:
          - The rack group the power panel is assigned to
        required: false
        type: raw
      name:
        description:
          - The name of the power panel
        required: true
        type: str
  state:
    description:
      - Use C(present) or C(absent) for adding or removing.
    choices: [ absent, present ]
    default: present
    type: str
  query_params:
    description:
      - This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined
      - in plugins/module_utils/utils.py and provides control to users on what may make
      - an object unique in their environment.
    required: false
    type: list
    elements: str
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.
    default: true
    type: raw
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create power panel within Nautobot with only required information
      networktocode.nautobot.power_panel:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          name: Test Power Panel
          site: Test Site
        state: present

    - name: Update power panel with other fields
      networktocode.nautobot.power_panel:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          name: Test Power Panel
          site: Test Site
          rack_group: Test Rack Group
        state: present

    - name: Delete power panel within nautobot
      networktocode.nautobot.power_panel:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          name: Test Power Panel
          site: Test Site
        state: absent
"""

RETURN = r"""
power_panel:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    NautobotAnsibleModule,
    NAUTOBOT_ARG_SPEC,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotDcimModule,
    NB_POWER_PANELS,
)
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(
        dict(
            data=dict(
                type="dict",
                required=True,
                options=dict(
                    site=dict(required=True, type="raw"),
                    rack_group=dict(required=False, type="raw"),
                    name=dict(required=True, type="str"),
                ),
            ),
        )
    )

    required_if = [
        ("state", "present", ["site", "name"]),
        ("state", "absent", ["site", "name"]),
    ]

    module = NautobotAnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True, required_if=required_if
    )

    power_panel = NautobotDcimModule(module, NB_POWER_PANELS)
    power_panel.run()


if __name__ == "__main__":  # pragma: no cover
    main()
