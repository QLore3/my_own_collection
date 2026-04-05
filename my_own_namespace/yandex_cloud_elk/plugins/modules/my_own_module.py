#!/usr/bin/python
from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module
short_description: Create text file with content
version_added: "1.0.0"

description:
  - Module creates a text file on remote host with provided content.

options:
  path:
    description: Path to the file
    required: true
    type: str
  content:
    description: Content of the file
    required: true
    type: str

author:
  - Ilya
'''

EXAMPLES = r'''
- name: Create file
  my_own_module:
    path: /tmp/test.txt
    content: "Hello from module"
'''

RETURN = r'''
changed:
  description: Was file changed
  type: bool
'''

from ansible.module_utils.basic import AnsibleModule
import os


def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True),
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']

    if module.check_mode:
        module.exit_json(**result)

    # Проверка существования файла и его содержимого (идемпотентность)
    if os.path.exists(path):
        with open(path, 'r') as f:
            current = f.read()
        if current == content:
            module.exit_json(**result)

    # Создание / изменение файла
    with open(path, 'w') as f:
        f.write(content)

    result['changed'] = True
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
