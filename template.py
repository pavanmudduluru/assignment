from troposphere import Ref, Template, Output, Tags
from troposphere.ec2 import InternetGateway, VPC, VPCGatewayAttachment, NetworkAcl, NetworkAclEntry, PortRange
import argparse


def generate_template(environment):
    '''
    Generates the required template based on the given environment.
    Parameters: 
        environment: str
        The environment for which the template is to be generated.
        Ex: Experimental, Development, Production 
          
    Returns: 
        template: obj
        A Template(troposphere) object with all the requiured attributes.
    '''
    template = Template()

    template.set_description('Service VPC')

    template.set_metadata({
        "DependsOn": [],
        "Environment": environment,
        "StackName": f'{environment}-VPC'
    })

    internet_gateway = template.add_resource(InternetGateway(
        "InternetGateway",
        Tags=Tags(
            Environment=environment,
            Name=f'{environment}-InternetGateway'
        )
    ))

    vpc = template.add_resource(VPC(
        "VPC",
        CidrBlock="10.0.0.0/16",
        EnableDnsHostnames=True,
        EnableDnsSupport=True,
        InstanceTenancy="default",
        Tags=Tags(
            Environment=environment,
            Name=f'{environment}-ServiceVPC'
        )
    ))

    gateway_attachment = template.add_resource(VPCGatewayAttachment(
        "VpcGatewayAttachment",
        InternetGatewayId=Ref(internet_gateway),
        VpcId=Ref(vpc)
    ))

    network_acl = template.add_resource(NetworkAcl(
        "VpcNetworkAcl",
        VpcId=Ref(vpc),
        Tags=Tags(
            Environment=environment,
            Name=f'{environment}-NetworkAcl'
        ),
    ))

    network_acl_inbound_rule = template.add_resource(NetworkAclEntry(
        "VpcNetworkAclInboundRule",
        CidrBlock="0.0.0.0/0",
        Egress=False,
        NetworkAclId=Ref(network_acl),
        PortRange=PortRange(To='443', From='443'),
        Protocol=6,
        RuleAction="allow",
        RuleNumber=100
    ))

    network_acl_outbound_rule = template.add_resource(NetworkAclEntry(
        "VpcNetworkAclOutboundRule",
        CidrBlock="0.0.0.0/0",
        Egress=True,
        NetworkAclId=Ref(network_acl),
        Protocol=6,
        RuleAction="allow",
        RuleNumber=200
    ))

    template.add_output([
        Output(
            "InternetGateway",
            Value=Ref(internet_gateway)
        ),
        Output(
            "VPCID",
            Value=Ref(vpc)
        )
    ])
    return template


def write_to_file(template):
    '''
    Creates a json file based on the template
    Parameters: 
        template: obj
        A Troposphere Template object.
    '''
    f = open(f'template_{environment.lower()}.json', 'w+')
    f.write(template.to_json())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--env',
                        help="Environment to which the template is being created."
                        " Ex: Experimental, Development, Production")
    environment = parser.parse_args().env

    template = generate_template(environment)
    write_to_file(template)

