import os
import yaml


def iter_records():
    for yaml_path in iter_yaml_paths():
        with open(yaml_path, 'r') as f:
            yaml_dict = yaml.safe_load(f)
            yield yaml_path, yaml_dict


def iter_yaml_paths():
    for dirpath, dirnames, filenames in os.walk('../database/', followlinks=False):
        for filename in filenames:
            if filename.endswith('.yaml'):
                yaml_path = os.path.join(dirpath, filename)
                yield yaml_path


def test_parse():
    """Test that all YAML files can be parsed."""
    for yaml_path in iter_yaml_paths():
        with open(yaml_path, 'r') as f:
            try:
                yaml.safe_load(f)
            except yaml.YAMLError as exc:
                assert False, 'Unable to parse {f} {e}'.format(f=yaml_path, e=str(exc))


def test_has_required():
    """Test that all required fields are present.

    TODO: we could use JSON schema to validate the YAML files.
    """
    for path, record in iter_records():
        assert record.get('cve'), 'missing "cve" field in {f}'.format(f=path)
        assert record.get('title'), 'missing "title" field in {f}'.format(f=path)
        assert record.get('description'), 'missing "description" field in {f}'.format(f=path)
        assert record.get('cvss_v2'), 'missing "cvss_v2" field in {f}'.format(f=path)
        assert record.get('references'), 'missing "references" field in {f}'.format(f=path)
        assert record.get('affected'), 'missing "affected" field in {f}'.format(f=path)

        for affected in record.get('affected'):
            assert affected.get('version'), 'missing "affected.version" field in {f}'.format(f=path)

            if '/java/' in path:
                assert affected.get('groupId'), 'missing "affected.groupId" field in {f}'.format(f=path)
                assert affected.get('artifactId'), 'missing "affected.artifactId" field in {f}'.format(f=path)
            else:
                assert affected.get('name'), 'missing "affected.name" field in {f}'.format(f=path)
