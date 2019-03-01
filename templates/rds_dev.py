from troposphere import (
    Template,
    ec2,
    rds,
    Ref,
    AWS_STACK_NAME,
    AWS_REGION,
    Join,
    GetAtt,
    Output,
    Sub,
    Export)
from troposphere.ec2 import Subnet

from configuration import (
    vpc_id,
    container_a_subnet_cidr,
    container_b_subnet_cidr,
    db_allocated_storage,
    db_name,
    db_class,
    db_user,
    db_password,
)

template = Template()

db_security_group = template.add_resource(ec2.SecurityGroup(
    'DatabaseSecurityGroup',
    GroupDescription="Database security group.",
    VpcId=vpc_id,
    SecurityGroupIngress=[
        ec2.SecurityGroupRule(
            IpProtocol="tcp",
            FromPort="3306",
            ToPort="3306",
            CidrIp=container_a_subnet_cidr,
        ),
    ],
))

container_a_subnet = template.add_resource(Subnet(
    "ContainerASubnet",
    VpcId=vpc_id,
    CidrBlock=container_a_subnet_cidr,
    AvailabilityZone=Join("", [Ref(AWS_REGION), "a"]),
))

container_b_subnet = template.add_resource(Subnet(
    "ContainerBSubnet",
    VpcId=vpc_id,
    CidrBlock=container_b_subnet_cidr,
    AvailabilityZone=Join("", [Ref(AWS_REGION), "c"]),
))

db_subnet_group = template.add_resource(rds.DBSubnetGroup(
    "DatabaseSubnetGroup",
    DBSubnetGroupDescription="Subnets available for the RDS DB Instance",
    SubnetIds=[
        Ref(container_a_subnet),
        Ref(container_b_subnet),
    ],
))

db_instance = template.add_resource(rds.DBInstance(
    "MySQL",
    DBName=db_name,
    AllocatedStorage=db_allocated_storage,
    DBInstanceClass=db_class,
    DBInstanceIdentifier=Ref(AWS_STACK_NAME),
    Engine="MySQL",
    EngineVersion="5.6",
    MultiAZ=False,
    StorageType="gp2",
    MasterUsername=db_user,
    MasterUserPassword=db_password,
    DBSubnetGroupName=Ref(db_subnet_group),
    VPCSecurityGroups=[Ref(db_security_group)],
    BackupRetentionPeriod="0",
    DeletionProtection=False,
))

template.add_output(Output(
    "JDBCConnectionString",
    Description="JDBC connection string for database",
    Value=Join("", [
        "jdbc:mysql://",
        GetAtt("MySQL", "Endpoint.Address"),
        GetAtt("MySQL", "Endpoint.Port"),
        "/",
        db_name,
    ]),
    Export=Export(Sub("${AWS::StackName}-JDBCConnectionString")),
))

template.add_output(Output(
    "MySQLInstance",
    Description="MySQL Instance",
    Value=Ref(db_instance),
    Export=Export(Sub("${AWS::StackName}-MySQLInstance")),
))


def get():
    return template.to_yaml()
