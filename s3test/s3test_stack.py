from aws_cdk import (
    # Duration,
    Stack,
    aws_s3 as s3,
    aws_s3_notifications as s3n,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_iam as iam,
    aws_lambda as _lambda,
)
from constructs import Construct


class S3TestStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        permissions_boundary_policy_arn = self.node.try_get_context(
            "PermissionsBoundaryPolicyArn"
        )
        if permissions_boundary_policy_arn:
            policy = iam.ManagedPolicy.from_managed_policy_arn(
                self, "PermissionsBoundary", permissions_boundary_policy_arn
            )
            iam.PermissionsBoundary.of(self).apply(policy)

        bucket_name = self.node.try_get_context("BucketName")
        lambda_role_arn = self.node.try_get_context("LambdaRoleArn")

        # lambda_role = iam.Role.from_role_name(self, "DefaultLambdaRole", "TestLambdaRole")
        role = iam.Role.from_role_arn(
            self,
            "DefaultLambdaRole",
            lambda_role_arn,
            # "arn:aws:iam::458358814065:role/TestLambdaRole",
            # self.format_arn(service='iam', region='', account=self.account, resource='role', resource_name=lambda_role_name),
            mutable=False,
        )

        arn=self.format_arn(service="s3", resource=bucket_name)
        test_bucket = s3.Bucket.from_bucket_attributes(
            self,
            "TestBucket",
            # bucket_arn='arn:aws:s3:::pmr-cdk-testing-bucket'
            bucket_arn=arn,   #self.format_arn(service="s3", resource=bucket_name),
            # notifications_handler_role=lambda_role
        )
        print(self.resolve(arn))

        test_topic = sns.Topic(self, "TestTopic")
        test_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED, s3n.SnsDestination(test_topic)
        )

        handler = _lambda.Function(
            self,
            "Handler",
            code=_lambda.Code.from_asset("lambda"),
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="handler.lambda_handler",
            role=role,
        )

        test_topic.add_subscription(subscriptions.LambdaSubscription(handler))
