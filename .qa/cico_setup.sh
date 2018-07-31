#!/bin/bash -ex

load_jenkins_vars() {
    if [ -e "jenkins-env.json" ]; then
        eval "$(./env-toolkit load -f jenkins-env.json \
                JENKINS_URL \
                GIT_BRANCH \
                GIT_COMMIT \
                BUILD_NUMBER \
                ghprbSourceBranch \
                ghprbActualCommit \
                BUILD_URL \
                ghprbPullId)"
    fi
}

prep() {
    yum -y update
    yum -y install epel-release
    yum -y install git python34-pip

    pip3 install -r requirements.txt
}

load_jenkins_vars
prep
