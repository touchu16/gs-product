# Google AutoML API

import os
import re
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
from werkzeug.utils import secure_filename
import argparse
import os
import sys


def predict(
    project_id, compute_region, model_id, file_path, score_threshold=""
):
    project_id = 'gga-product'
    compute_region = 'us-central1'
    model_id = 'ICN1745623247420128444'
    file_path = './static/images'
    score_threshold = "0.5"

    from google.cloud import automl_v1beta1 as automl

    automl_client = automl.AutoMlClient()

    model_full_id = automl_client.model_path(
        project_id, compute_region, model_id
    )

    prediction_client = automl.PredictionServiceClient()

    with open(file_path, "rb") as img_file:
        content = img_file.read()
    payload = {"image": {"image_bytes": content}}

    params = {}
    if score_threshold:
        params = {"score_threshold": score_threshold}

    response = prediction_client.predict(model_full_id, payload, params)
    print("Prediction results:")
    return render_template('result.html', )
    for result in response.payload:
        print("Predicted class name: {}".format(result.display_name))
        print("Predicted class score: {}".format(result.classification.score))

    if __name__ == "__main__":
        parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        subparsers = parser.add_subparsers(dest="command")

        predict_parser = subparsers.add_subparsers(
            "predict", help=predict.__doc__)
        predict_parser.add_argument("model_id")
        predict_parser.add_argument("file_path")
        predict_parser.add_argument("score_threshold", nargs="?", default="")

        project_id = os.environ["PROJECT_ID"]
        compute_region = os.environ["REGION_NAME"]

        args = parser.parse_args()

        if args.command == "predict":
            predict(
                project_id,
                compute_region,
                args.model_id,
                args.file_path,
                args.score_threshold,
            )

    # 【参考】以下、Google AutoML 記載のprecit.py codeを記載

    # import sys

    # from google.cloud import automl_v1beta1
    # from google.cloud.automl_v1beta1.proto import service_pb2

    # def get_prediction(content, project_id, model_id):
    #   prediction_client = automl_v1beta1.PredictionServiceClient()

    #   name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
    #   payload = {'image': {'image_bytes': content }}
    #   params = {}
    #   request = prediction_client.predict(name, payload, params)
    #   return request  # waits till request is returned

    # if __name__ == '__main__':
    #   file_path = sys.argv[1]
    #   project_id = sys.argv[2]
    #   model_id = sys.argv[3]

    #   with open(file_path, 'rb') as ff:
    #     content = ff.read()

    # print (get_prediction(content, project_id, model_id))
