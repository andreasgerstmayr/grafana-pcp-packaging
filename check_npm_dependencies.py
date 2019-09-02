#!/usr/bin/env python3
import sys
import tarfile
import json

def read_spec_provides(spec_path):
    with open(spec_path) as f:
        for line in f:
            if line.startswith('Provides:'):
                yield line.strip()

def read_node_deps(source_archive_path):
    root_dir = source_archive_path[:-len('.tar.gz')]
    with tarfile.open(source_archive_path) as tar:
        f = tar.extractfile('{}/package.json'.format(root_dir))
        package_json = json.load(f)
        return list(package_json['devDependencies'].keys()) + list(package_json['dependencies'].keys())

def read_node_deps_versions(dep_bundle_path, dependencies):
    with tarfile.open(dep_bundle_path) as tar:
        for dependency in dependencies:
            f = tar.extractfile('node_modules/{}/package.json'.format(dependency))
            package_json = json.load(f)
            yield 'Provides: bundled(nodejs-{}) = {}'.format(package_json["name"], package_json["version"])

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('usage: {} specfile source-archive dependency-bundle'.format(sys.argv[0]))
        sys.exit(1)

    provides = list(read_spec_provides(sys.argv[1]))
    dependencies = sorted(read_node_deps(sys.argv[2]))
    actual_provides = list(read_node_deps_versions(sys.argv[3], dependencies))

    if provides == actual_provides:
        print("Dependencies are up-to-date with the specfile.")
        sys.exit(0)
    else:
        print("Dependencies don't match, please update the specfile:")
        print ('\n'.join(actual_provides))
        sys.exit(1)
