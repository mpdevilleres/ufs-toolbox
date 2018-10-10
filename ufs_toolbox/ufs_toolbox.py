# -*- coding: utf-8 -*-
from io import StringIO
from urllib.parse import urlparse

import pandas as pd
import boto3

"""Main module."""


def save_to_s3(df, url, **kwargs):
    if df is None:
        raise ValueError('Dataframe is Required')
    if not isinstance(df, pd.DataFrame):
        raise TypeError('df must be a Dataframe')

    url = urlparse(url)
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, **kwargs)
    s3_resource = boto3.resource('s3')
    # s3_resource.Object(<bucket>, <key>).put(Body=csv_buffer.getvalue())
    # url.path[1:] to remove the starting '/'
    s3_resource.Object(url.netloc, url.path[1:]).put(Body=csv_buffer.getvalue())
