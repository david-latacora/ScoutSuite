import os

from msgraphcore import GraphSession

from ScoutSuite.core.console import print_exception
from azure.identity import DeviceCodeCredential, DefaultAzureCredential, AzureCliCredential, ManagedIdentityCredential, \
    ClientSecretCredential


class AADFacade:

    def __init__(self, credentials):
        self.credentials = credentials


    async def _get_microsoft_graph_response(self, api_resource, api_version='v1.0'):
        scopes = ['https://graph.microsoft.com/.default']

        client = GraphSession(self.credentials.get_credentials(), scopes)
        endpoint = 'https://graph.microsoft.com/{}/{}'.format(api_version, api_resource)

        try:
            response = client.get(endpoint)
            if response.status_code == 200:
                return response.json()
            else:
                print_exception('Failed to query Microsoft Graph endpoint \"{}\": status code {}'.
                                format(api_resource, response.status_code))
                return {}
        except Exception as e:
            print_exception('Failed to query Microsoft Graph endpoint \"{}\": {}'.format(api_resource, e))
            return {}

    async def get_users(self):
        try:
            # test = await self._get_microsoft_graph_response('users') # missing some necessary information for rules
            users_response_beta = await self._get_microsoft_graph_response('users', 'beta')
            users = users_response_beta.get('value')
            users_filtered = [d for d in users if d['userType'] in 'Guest']
            return users_filtered
        except Exception as e:
            print_exception(f'Failed to retrieve users: {e}')
            return []

    async def get_user(self, user_id):
        try:
            # test = await self._get_microsoft_graph_response('users') # missing some necessary information for rules
            user_response_beta = await self._get_microsoft_graph_response('users', 'beta')
            users = user_response_beta.get('value')
            users_filtered = [d for d in users if d['id'] in user_id]
            return users_filtered[0]
        except Exception as e:
            print_exception(f'Failed to retrieve user {user_id}: {e}')
            return None

    async def get_groups(self):
        try:
            groups_response = await self._get_microsoft_graph_response('groups')
            groups = groups_response.get('value')
            return groups
        except Exception as e:
            print_exception(f'Failed to retrieve groups: {e}')
            return []

    async def get_user_groups(self, group_id):
        try:
            user_groups_response = await self._get_microsoft_graph_response('groups')
            groups = user_groups_response.get('value')
            filtered_group = [d for d in groups if d['id'] in group_id]
            return filtered_group
        except Exception as e:
            print_exception(f'Failed to retrieve user\'s groups: {e}')
            return []

    async def get_service_principals(self):
        try:
            # Need publisher name value for serviceprincipals.py. v1.0 does not have that value, thus we use beta
            service_principals_response_beta = await self._get_microsoft_graph_response('servicePrincipals', 'beta')
            service_principals = service_principals_response_beta.get('value')
            return service_principals
        except Exception as e:
            print_exception(f'Failed to retrieve service principals: {e}')
            return []

    async def get_applications(self):
        try:
            applications_response = await self._get_microsoft_graph_response('applications')
            applications = applications_response.get('value')
            return applications
        except Exception as e:
            print_exception(f'Failed to retrieve applications: {e}')
            return []

    async def get_security_defaults(self):
        try:
            security_default_response = await self._get_microsoft_graph_response(
                'identitySecurityDefaultsEnforcementPolicy')
            return security_default_response
        except Exception as e:
            print_exception(f'Failed to retrieve applications: {e}')
            return []
