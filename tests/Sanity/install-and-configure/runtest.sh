#!/bin/bash
# vim: dict+=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of /tools/grafana-pcp/Sanity/install-and-configure
#   Description: grafana testing via grafana testsuite
#   Author: Jan Kuřík <jkurik@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2019 Red Hat, Inc.
#
#   This program is free software: you can redistribute it and/or
#   modify it under the terms of the GNU General Public License as
#   published by the Free Software Foundation, either version 2 of
#   the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied
#   warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#   PURPOSE.  See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see http://www.gnu.org/licenses/.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Include Beaker environment
. /usr/share/beakerlib/beakerlib.sh || exit 1

PACKAGE="grafana-pcp"

rlJournalStart
  rlPhaseStartTest "Check if $PACKAGE is installed"
    rlAssertRpm $PACKAGE || \
        { rlFail "$PACKAGE is not installed"; rlDie "Giving up"; }
    rlRun "grafana-cli plugins ls | grep performancecopilot-pcp-app"
  rlPhaseEnd

  rlPhaseStartTest "Check if Grafana is aware of the $PACKAGE plugin"
    rlServiceStart grafana-server
    rlRun "curl -X GET -s http://admin:admin@localhost:3000//api/datasources |& \
        grep -q 'plugins/performancecopilot-pcp-app'" 0
    rlServiceRestore
  rlPhaseEnd
rlJournalPrintText
rlJournalEnd
