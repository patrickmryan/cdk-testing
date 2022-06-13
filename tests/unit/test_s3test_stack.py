import aws_cdk as core
import aws_cdk.assertions as assertions

from s3test.s3test_stack import S3TestStack

# example tests. To run these tests, uncomment this file along with the example
# resource in s3test/s3test_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = S3TestStack(app, "s3test")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
