#!/usr/bin/python

# Copyright: (c) 2023, Naing Ye Minn <naingyeminn@gmail.com>
# MIT License (see README.md or https://opensource.org/license/mit/)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: log_grep

short_description: This module can extract the lines by keyword

version_added: "1.0.0"

description: This module can be used to extract the lines from the files in a directory by a keyword.

options:
    path:
        description: directory to search
        required: true
        type: str
    output:
        description: output file path
        required: true
        type: str
    keyword:
        description: keyword to search
        required: true
        type: str
    file_extension:
        description: extension of the files to search through
        required: false
        type: str

author:
    - Naing Ye Minn (@naingyeminn)
'''

EXAMPLES = r'''
- name: grep logs to file
  log_grep:
    path: /var/log/app1
    output: /tmp/output.log
    keyword: Error
    file_extension: .log
'''

RETURN = r'''
output:
    description: output file path
    type: str
    returned: always
    sample: '/tmp/output.log'
'''

from ansible.module_utils.basic import AnsibleModule
import os
import re

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        path=dict(type='str', required=True),
        output=dict(type='str', required=True),
        keyword=dict(type='str', required=True),
        file_extension=dict(type='str', required=False, default='.log')
    )

    result = dict(
        changed=False,
        output=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    try:
        with open(module.params['output'], "w") as outfile:
            for dirpath, dirnames, filenames in os.walk(module.params['path']):
                for filename in filenames:
                    if filename.endswith(module.params['file_extension']):
                        file_path = os.path.join(dirpath, filename)
                        with open(file_path, "r") as infile:
                            for line in infile:
                                if re.search(module.params['keyword'], line):
                                    outfile.write(f"{line}")
    except IOError:
        module.fail_json(msg='File could not be created', **result)

    if os.path.exists(module.params['output']):
        result['output'] = module.params['output']
        result['changed'] = True

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
