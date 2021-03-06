#!/usr/bin/env python
# Copyright 2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from tests import BaseSessionTest

import six


class TestCloudsearchOperations(BaseSessionTest):

    def test_streaming_json_upload(self):
        stream = six.BytesIO(b'{"fakejson": true}')
        service = self.session.get_service('cloudsearchdomain')
        operation = service.get_operation('UploadDocuments')
        built = operation.build_parameters(
            contentType='application/json', documents=stream)
        endpoint = service.get_endpoint(region_name='us-east-1',
                                        endpoint_url='http://example.com')
        request = endpoint.create_request(built, signer=None)
        self.assertEqual(request.body, stream)

    def test_region_not_required(self):
        stream = six.StringIO('{"fakejson": true}')
        service = self.session.get_service('cloudsearchdomain')
        service.signature_version = None
        operation = service.get_operation('UploadDocuments')
        built = operation.build_parameters(
            contentType='application/json', documents=stream)
        # Note we're not giving a region name.
        endpoint = service.get_endpoint(endpoint_url='http://example.com')
        request = endpoint.create_request(built, signer=None)
        self.assertEqual(request.body, stream)
