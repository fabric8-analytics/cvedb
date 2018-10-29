import os
from victimsdb_lib.model import Record


def iter_records():
    for yaml_path, ecosystem in iter_yaml_paths():

        with open(yaml_path, 'r') as f:
            record = Record.from_file(yaml_path, ecosystem=ecosystem)
            yield yaml_path, record, ecosystem


def iter_yaml_paths():
    for dirpath, dirnames, filenames in os.walk('../database/', followlinks=False):
        for filename in filenames:
            if filename.endswith('.yaml'):
                ecosystem = os.path.split(os.path.split(dirpath)[0])[1]
                yaml_path = os.path.join(dirpath, filename)
                yield yaml_path, ecosystem


def test_has_required():
    """Test that all required fields are present."""

    for path, record, ecosystem in iter_records():
        assert record.cve_id, 'missing "cve" field in {f}'.format(f=path)
        assert record.title, 'missing "title" field in {f}'.format(f=path)
        assert record.description, 'missing "description" field in {f}'.format(f=path)
        assert record.cvss_v2, 'missing "cvss_v2" field in {f}'.format(f=path)
        assert record.references, 'missing "references" field in {f}'.format(f=path)
        assert record.affected, 'missing "affected" field in {f}'.format(f=path)

        for affected in record.affected:
            assert affected.version, 'missing "affected.version" field in {f}'.format(f=path)
            assert affected.name, 'missing "affected.name" field in {f}'.format(f=path)
