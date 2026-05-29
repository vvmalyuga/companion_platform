from airflow.providers.amazon.aws.hooks.base_aws import AwsBaseHook
class MinioHook(AwsBaseHook):
    def __init__(self, *args, **kwargs):
        kwargs['client_type'] = 's3'
        super().__init__(*args, **kwargs)
    def get_conn(self):
        conn = super().get_conn()
        conn.meta.endpoint_url = "http://minio:9000"
        return conn
