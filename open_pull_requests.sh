#!/usr/bin/env bash

set -e
set -x

pwd
ls -la


files=$(git status -s | awk '{ print $2 }')


branches=
for f in ${files}; do
    git checkout master

    number_yaml=$(basename "$f")
    number=${number_yaml%.yaml}
    year=$(basename `dirname "$f"`)
    cve_id="CVE-${year}-${number}"
    branch=${cve_id}-001
    git checkout -b ${branch}
    git add "$f"
    git commit -m "Add $cve_id"
    branches="$branches $branch"
    git push -u origin ${branch}

    curl -X POST -H 'Content-Type: application/json' -H "Authorization: token $GITHUB_TOKEN" -d "\
    { \
        \"title\": \"[${CVEJOB_ECOSYSTEM:-javascript}] Add $cve_id\", \
        \"body\": \"\", \
        \"head\": \"${branch}\", \
        \"base\": \"master\" \
    } \
" https://api.github.com/repos/fabric8-analytics/cvedb/pulls

done
