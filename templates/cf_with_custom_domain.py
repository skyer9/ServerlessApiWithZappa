from troposphere import (
    Template,
    GetAtt,
    Join)

from troposphere.cloudfront import (
    Distribution,
    DistributionConfig,
    Origin,
    ViewerCertificate,
    DefaultCacheBehavior,
    ForwardedValues,
    CustomOriginConfig,
)
from troposphere.route53 import RecordSetGroup, RecordSet, AliasTarget

from configuration import (
    root_domain_name,
    api_url,
    acm_certificate_arn,
)

api_domain_name = "api." + root_domain_name
aliases = [api_domain_name]

template = Template()

distribution = template.add_resource(Distribution(
    "ApiDistribution",
    DistributionConfig=DistributionConfig(
        Aliases=aliases,
        Origins=[Origin(
            Id="ApiGatewayOrigin",
            DomainName=api_url,
            CustomOriginConfig=CustomOriginConfig(
                HTTPPort=80,
                HTTPSPort=443,
                # ApiGateway 는 https 만 허용한다.
                OriginProtocolPolicy="https-only"
            ),
        )],
        ViewerCertificate=ViewerCertificate(
            # 인증키는 미국동부(버지니아 북부) 리전에서 생성한 것만 사용가능하다.
            AcmCertificateArn=acm_certificate_arn,
            SslSupportMethod='sni-only'
        ),
        DefaultCacheBehavior=DefaultCacheBehavior(
            TargetOriginId="ApiGatewayOrigin",
            # ApiGateway 는 https 만 허용한다.
            ViewerProtocolPolicy="https-only",
            ForwardedValues=ForwardedValues(QueryString=True),
            # ApiGateway 의 TTL 을 최대 10분으로 설정한다.
            MaxTTL=600,
        ),
        DefaultRootObject="index.html",
        Enabled=True,
        PriceClass="PriceClass_All",
        HttpVersion="http2",
    ),
))

template.add_resource(RecordSetGroup(
    "AssetsDNSName",
    HostedZoneName=Join("", [root_domain_name, "."]),
    Comment="Zone apex alias.",
    RecordSets=[
        RecordSet(
            Name=api_domain_name,
            Type="A",
            AliasTarget=AliasTarget(
                # CloudFront 는 HostedZoneId 가 하나이다.
                HostedZoneId="Z2FDTNDATAQYW2",
                DNSName=GetAtt(distribution, "DomainName")
            ),
        ),
    ],
))


def get():
    return template.to_yaml()
