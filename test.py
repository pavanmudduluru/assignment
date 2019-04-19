import template, unittest
from troposphere import Template


environment = 'Development'

class BasicTests(unittest.TestCase):
    def setUp(self):
        self.t = template.generate_template(environment)

    def test_description(self):
        '''
        Checking the description of the generated template
        '''
        value = 'Service VPC'
        self.assertEqual(value, self.t.description)

    def test_metadata(self):
        '''
        Checking the metadata of the generated template
        '''
        metadata = {
            "DependsOn": [],
            "Environment": 'Development',
            "StackName": 'Development-VPC'
        }
        self.assertEqual(metadata, self.t.metadata)

    def test_outputs(self):
        '''
        Checking if we have required outputs in the generated template
        '''
        self.assertIn('InternetGateway', self.t.outputs)
        self.assertIn('VPCID', self.t.outputs)

    def test_resources(self):
        '''
        Checking if we have required resources in the generated template
        '''
        self.assertIn('InternetGateway', self.t.resources)
        self.assertIn('VPC', self.t.resources)
        self.assertIn('VpcGatewayAttachment', self.t.resources)
        self.assertIn('VpcNetworkAcl', self.t.resources)
        self.assertIn('VpcNetworkAclInboundRule', self.t.resources)
        self.assertIn('VpcNetworkAclOutboundRule', self.t.resources)

    def test_tags(self):
        '''
        Checking if we the resources have the required tags and correct values in the generated template
        '''
        environment_tag = {}
        name_tag = {}
        resources_with_tags = ['InternetGateway', 'VPC', 'VpcNetworkAcl']
        for resource in resources_with_tags:
            for tag in self.t.resources[resource].Tags.tags:
                if tag['Key'] == 'Environment':
                    environment_tag = tag
                if tag['Key'] == 'Name':
                    name_tag = tag
            self.assertIsNotNone(environment_tag)
            self.assertIsNotNone(name_tag)
            self.assertEqual(environment_tag['Value'], environment)
            self.assertTrue(name_tag['Value'].startswith(environment))


if __name__ == '__main__':
    unittest.main()

