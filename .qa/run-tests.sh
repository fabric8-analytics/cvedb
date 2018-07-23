#!/bin/bash -ex

here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

py.test -vv ${here}/tests/
