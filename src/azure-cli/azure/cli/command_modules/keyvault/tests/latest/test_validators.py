# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest

from knack.arguments import CLICommandArgument
from knack.util import CLIError

from azure.cli.command_modules.keyvault._validators import validate_vault_name_and_hsm_name


class _Command:
    def __init__(self, vault_name_options):
        self.arguments = {
            'vault_name': CLICommandArgument('vault_name', options_list=vault_name_options)
        }


class _Namespace:
    def __init__(self, vault_name_options=None, vault_name=None, hsm_name=None):
        if vault_name_options:
            self.cmd = _Command(vault_name_options)
        self.vault_name = vault_name
        self.hsm_name = hsm_name


class KeyVaultValidatorsTest(unittest.TestCase):
    def test_validate_vault_name_and_hsm_name(self):
        # the error message should match the option registered for the command
        with self.assertRaisesRegex(CLIError, r'Please specify --name/-n or --hsm-name\.'):
            validate_vault_name_and_hsm_name(_Namespace(vault_name_options=['--name', '-n']))

        with self.assertRaisesRegex(CLIError, r'--name/-n and --hsm-name are mutually exclusive\.'):
            validate_vault_name_and_hsm_name(
                _Namespace(vault_name_options=['--name', '-n'], vault_name='vault', hsm_name='hsm'))

        with self.assertRaisesRegex(CLIError, r'Please specify --vault-name or --hsm-name\.'):
            validate_vault_name_and_hsm_name(_Namespace(vault_name_options=['--vault-name']))

        # no exception when just one of them is specified
        validate_vault_name_and_hsm_name(_Namespace(vault_name_options=['--name', '-n'], vault_name='vault'))
        validate_vault_name_and_hsm_name(_Namespace(vault_name_options=['--name', '-n'], hsm_name='hsm'))


if __name__ == '__main__':
    unittest.main()
