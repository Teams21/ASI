# src/my_kedro_project/datasets/auto_gluon_dataset.py
# src/my_kedro_project/datasets/auto_gluon_dataset.py
import os
from kedro.io import AbstractDataset
from autogluon.tabular import TabularPredictor
import boto3

class AutoGluonModelDataset(AbstractDataset):
    def __init__(self, filepath):
        self.filepath = filepath

    def _load(self) -> TabularPredictor:
        if self.filepath.startswith('s3://'):
            s3 = self._get_s3_obj('asi-s3-read')
            bucket, key = self._parse_s3_path(self.filepath)
            files = self._list_s3_objects(bucket, key, s3)
            for file in files:
                print(f'FILE: {file}')
                s3.download_file(Bucket=bucket, Key=file, Filename=file)
            return TabularPredictor.load(os.path.abspath(key))
        else:
            return TabularPredictor.load(self.filepath)

    def _save(self, model: TabularPredictor) -> None:
        if self.filepath.startswith('s3://'):
                s3 = self._get_s3_obj('asi-s3-write')
                bucket, key = self._parse_s3_path(self.filepath)
                for root, _, files in os.walk(key):
                    for file in files:
                        s3.upload_file(os.path.join(root, file).replace('\\', '/'), bucket, os.path.join(key, file).replace('\\', '/'))
        else:
            model.save()

    def _describe(self) -> dict:
        return {"filepath": self.filepath}
    
    @staticmethod
    def _parse_s3_path(s3_path):
        """Parse the S3 path into bucket and key."""
        path_parts = s3_path.replace("s3://", "").split("/", 1)
        bucket = path_parts[0]
        key = path_parts[1] if len(path_parts) > 1 else ""
        return bucket, key

    @staticmethod
    def _get_s3_obj(profile: str):
        my_session = boto3.session.Session(profile_name=profile)
        s3 = my_session.client('s3')

        return s3
    
    @staticmethod
    def _list_s3_objects(bucket_name, prefix, resource):

        # Initialize variables to keep track of the listed objects
        objects = []
        continuation_token = None

        # Loop through paginated results
        while True:
            if continuation_token:
                response = resource.list_objects_v2(
                    Bucket=bucket_name,
                    Prefix=prefix,
                    ContinuationToken=continuation_token
                )
            else:
                response = resource.list_objects_v2(
                    Bucket=bucket_name,
                    Prefix=prefix
                )

            # Add the current batch of objects to the list
            if 'Contents' in response:
                objects.extend(response['Contents'])

            # Check if there are more objects to retrieve
            if response.get('IsTruncated'):
                continuation_token = response.get('NextContinuationToken')
            else:
                break

        # Print out the objects
        for idx, obj in enumerate(objects):
            objects[idx] = obj['Key']

        return objects