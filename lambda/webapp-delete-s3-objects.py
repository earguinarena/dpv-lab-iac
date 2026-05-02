import boto3
import os

code_pipeline = boto3.client("codepipeline")
s3_resource = boto3.resource("s3")
s3_bucket = s3_resource.Bucket(os.environ["bucketName"])


def handler(event, context):
    job_id = event["CodePipeline.job"]["id"]
    try:
        # Deleting objects
        for s3_object in s3_bucket.objects.all():
            s3_object.delete()
        # Deleting objects versions if S3 versioning enabled
        for s3_object_ver in s3_bucket.object_versions.all():
            s3_object_ver.delete()
        print("S3 Bucket cleaned up")

    except Exception as e:
        print(str(e))
        code_pipeline.put_job_failure_result(
            jobId=job_id,
            failureDetails={
                "type": "JobFailed",
                "message": str(e),
            },
        )
    else:
        code_pipeline.put_job_success_result(jobId=job_id, )
