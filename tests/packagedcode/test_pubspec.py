#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/scancode-toolkit for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import os.path

from packagedcode import pubspec
from packages_test_utils  import build_tests
from packages_test_utils import PackageTester
from scancode_config import REGEN_TEST_FIXTURES

test_data_dir = os.path.join(os.path.dirname(__file__), 'data')


class TestPubspecDatadriven(PackageTester):
    test_data_dir = test_data_dir

    def test_pubspec_lock_is_package_data_file(self):
        test_file = self.get_test_loc('pubspec/locks/dart-pubspec.lock')
        assert pubspec.DartPubspecLockHandler.is_datafile(test_file)

    def test_pubspec_yaml_is_package_data_file(self):
        test_file = self.get_test_loc('pubspec/specs/authors-pubspec.yaml')
        assert pubspec.DartPubspecYamlHandler.is_datafile(test_file)

    def test_parse_lock(self):
        test_loc = self.get_test_loc('pubspec/mini-pubspec.lock')
        expected_loc = self.get_test_loc('pubspec/mini-pubspec.lock-expected.json')
        package_data = pubspec.DartPubspecLockHandler.parse(test_loc)
        self.check_packages_data(package_data, expected_loc, regen=REGEN_TEST_FIXTURES)


def test_build_dep_with_mapping_dependencies():
    # a path dependency has no version and is not pinned
    dep = pubspec.build_dep(
        'my_local_lib', {'path': '../my_local_lib'}, scope='dependencies'
    )
    assert dep.purl == 'pkg:pubspec/my_local_lib'
    assert dep.extracted_requirement == 'path: ../my_local_lib'
    assert not dep.is_pinned

    # a git dependency has no version either
    dep = pubspec.build_dep(
        'some_git_pkg',
        {'git': {'url': 'https://github.com/example/some_git_pkg.git', 'ref': 'abc123'}},
        scope='dependencies',
    )
    assert dep.purl == 'pkg:pubspec/some_git_pkg'
    assert not dep.is_pinned

    # a hosted dependency uses its own "version" entry as the requirement
    dep = pubspec.build_dep(
        'hosted_pkg',
        {'hosted': {'name': 'hosted_pkg', 'url': 'https://my-pub-server.example.com'},
         'version': '2.0.0'},
        scope='dependencies',
    )
    assert dep.purl == 'pkg:pubspec/hosted_pkg@2.0.0'
    assert dep.is_pinned

    # an SDK dependency keeps its flattened mapping as the requirement
    dep = pubspec.build_dep('flutter', {'sdk': 'flutter'}, scope='dependencies')
    assert dep.purl == 'pkg:pubspec/flutter'
    assert dep.extracted_requirement == 'sdk: flutter'
    assert not dep.is_pinned


def pub_tester(location,):
    manifests = []
    for package_data in pubspec.DartPubspecYamlHandler.parse(location):
        manifests.append(package_data.to_dict())
    return manifests


def lock_tester(location,):
    manifests = []
    for package_data in pubspec.DartPubspecLockHandler.parse(location):
        manifests.append(package_data.to_dict())
    return manifests


build_tests(
    test_dir=os.path.join(test_data_dir, 'pubspec/specs'),
    clazz=TestPubspecDatadriven,
    test_method_prefix='test_pubspec_yaml',
    tested_function=pub_tester,
    test_file_suffix='pubspec.yaml',
    regen=REGEN_TEST_FIXTURES,
)

build_tests(
    test_dir=os.path.join(test_data_dir, 'pubspec/locks'),
    clazz=TestPubspecDatadriven,
    test_method_prefix='test_pubspec_lock',
    tested_function=lock_tester,
    test_file_suffix='pubspec.lock',
    regen=REGEN_TEST_FIXTURES,
)
