Name:           grafana-pcp
Version:        2.0.2
Release:        2%{?dist}
Summary:        Performance Co-Pilot Grafana Plugin

%global         github https://github.com/performancecopilot/grafana-pcp
%global         install_dir %{_sharedstatedir}/grafana/plugins/grafana-pcp

BuildArch:      noarch
ExclusiveArch:  %{nodejs_arches}

License:        ASL 2.0
URL:            %{github}

Source0:        %{github}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        grafana-pcp-deps-%{version}.tar.xz
Source2:        create_dependency_bundle.sh

BuildRequires:  nodejs
Requires:       grafana >= 6.6.0
Suggests:       pcp >= 5.0.0
Suggests:       redis >= 5.0.0
Suggests:       bpftrace >= 0.9.2

# Obsolete old webapps
Obsoletes: pcp-webjs <= 4.3.4
Obsoletes: pcp-webapp-blinkenlights <= 4.3.4
Obsoletes: pcp-webapp-grafana <= 4.3.4
Obsoletes: pcp-webapp-graphite <= 4.3.4
Obsoletes: pcp-webapp-vector <= 4.3.4

# Bundled npm packages
Provides: bundled(nodejs-@babel/cli) = 7.8.4
Provides: bundled(nodejs-@babel/core) = 7.8.4
Provides: bundled(nodejs-@babel/preset-env) = 7.8.4
Provides: bundled(nodejs-@babel/preset-react) = 7.8.3
Provides: bundled(nodejs-@babel/preset-typescript) = 7.8.3
Provides: bundled(nodejs-@grafana/data) = 6.6.0
Provides: bundled(nodejs-@grafana/ui) = 6.6.0
Provides: bundled(nodejs-@types/benchmark) = 1.0.31
Provides: bundled(nodejs-@types/d3) = 5.7.2
Provides: bundled(nodejs-@types/grafana) = 4.6.3
Provides: bundled(nodejs-@types/jest) = 24.9.1
Provides: bundled(nodejs-@types/lodash) = 4.14.149
Provides: bundled(nodejs-babel-jest) = 24.9.0
Provides: bundled(nodejs-babel-loader) = 8.0.6
Provides: bundled(nodejs-babel-plugin-angularjs-annotate) = 0.10.0
Provides: bundled(nodejs-benchmark) = 2.1.4
Provides: bundled(nodejs-clean-webpack-plugin) = 0.1.19
Provides: bundled(nodejs-copy-webpack-plugin) = 5.1.1
Provides: bundled(nodejs-core-js) = 3.6.4
Provides: bundled(nodejs-css-loader) = 1.0.1
Provides: bundled(nodejs-d3-flame-graph) = 2.1.9
Provides: bundled(nodejs-d3-selection) = 1.4.1
Provides: bundled(nodejs-expr-eval) = 1.2.3
Provides: bundled(nodejs-jest) = 24.9.0
Provides: bundled(nodejs-jest-date-mock) = 1.0.8
Provides: bundled(nodejs-jsdom) = 9.12.0
Provides: bundled(nodejs-lodash) = 4.17.15
Provides: bundled(nodejs-memoize-one) = 5.1.1
Provides: bundled(nodejs-mocha) = 6.2.2
Provides: bundled(nodejs-prunk) = 1.3.1
Provides: bundled(nodejs-q) = 1.5.1
Provides: bundled(nodejs-regenerator-runtime) = 0.12.1
Provides: bundled(nodejs-request) = 2.88.0
Provides: bundled(nodejs-style-loader) = 0.22.1
Provides: bundled(nodejs-ts-jest) = 24.3.0
Provides: bundled(nodejs-ts-loader) = 4.5.0
Provides: bundled(nodejs-tslint) = 5.20.1
Provides: bundled(nodejs-tslint-config-airbnb) = 5.11.2
Provides: bundled(nodejs-typescript) = 3.7.5
Provides: bundled(nodejs-webpack) = 4.41.5
Provides: bundled(nodejs-webpack-cli) = 3.3.10


%description
This Grafana plugin for Performance Co-Pilot includes datasources for
scalable time series from pmseries(1) and Redis, live PCP metrics and
bpftrace scripts from pmdabpftrace(1), as well as several dashboards.

%prep
%setup -q
%setup -q -a 1

%build
rm -rf dist
./node_modules/webpack/bin/webpack.js --config webpack.config.prod.js

# webpack/copy-webpack-plugin sometimes outputs files with mode = 666 due to reasons unknown (race condition/umask issue afaics)
chmod -Rf a+rX,u+w,g-w,o-w dist

%check
./node_modules/jest/bin/jest.js --silent

%install
install -d -m 755 %{buildroot}/%{install_dir}
cp -a dist/* %{buildroot}/%{install_dir}

%files
%{install_dir}

%license LICENSE NOTICE
%doc README.md

%changelog
* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Feb 25 2020 Andreas Gerstmayr <agerstmayr@redhat.com> 2.0.2-1
- vector, redis: remove autocompletion cache (PCP metrics can be added and removed dynamically)

* Thu Feb 20 2020 Andreas Gerstmayr <agerstmayr@redhat.com> 2.0.1-1
- support for Grafana 6.6+, drop support for Grafana < 6.6
- vector, bpftrace: fix version checks on dashboard load (prevent multiple pmcd.version checks on dashboard load)
- vector, bpftrace: change datasource check box to red if URL is inaccessible
- redis: add tests
- flame graphs: support multidimensional eBPF maps (required to display e.g. the process name)
- dashboards: remove BCC metrics from Vector host overview (because the BCC PMDA is not installed by default)
- misc: update dependencies
- build: fix production build (implement workaround for https://github.com/systemjs/systemjs/issues/2117, https://github.com/grafana/grafana/issues/21785)

* Wed Jan 29 2020 Andreas Gerstmayr <agerstmayr@redhat.com> 1.0.7-1
- redis: fix timespec (fixes empty graphs for large time ranges)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 07 2020 Andreas Gerstmayr <agerstmayr@redhat.com> 1.0.6-1
- redis: support wildcards in metric names
- redis: fix label support
- redis: fix legends
- redis: set default sample interval to 60s (fixes empty graph borders)
- build: upgrade copy-webpack-plugin to mitigate XSS vulnerability in the serialize-javascript transitive dependency
- build: remove deprecated uglify-webpack-plugin

* Thu Dec 12 2019 Andreas Gerstmayr <agerstmayr@redhat.com> 1.0.4-2
- remove node_modules/node-notifier directory from webpack (due to licensing issues)

* Wed Dec 11 2019 Andreas Gerstmayr <agerstmayr@redhat.com> 1.0.4-1
- flame graphs: clean flame graph stacks every 5s (reduces CPU load)
- general: implement PCP version checks
- build: remove weak dependency (doesn't work with Node.js 12)
- build: upgrade terser-webpack-plugin to mitigate XSS vulnerability in the serialize-javascript transitive dependency

* Tue Nov 26 2019 Nathan Scott <nathans@redhat.com> 1.0.3-1
- fix flame graph dependency (flamegraph.destroy error in javascript console)

* Tue Nov 12 2019 Andreas Gerstmayr <agerstmayr@redhat.com> 1.0.2-1
- handle counter wraps (overflows)
- convert time based counters to time utilization
- flame graphs: aggregate stack counts by selected time range in the Grafana UI
- flame graphs: add option to hide idle stacks
- vector: fix container dropdown in query editor
- vector: remove container setting from datasource settings page
- redis: fix value transformations (e.g. rate conversation of counters)
- request more datapoints from the datasource to fill the borders of the graph panel

* Fri Oct 11 2019 Andreas Gerstmayr <agerstmayr@redhat.com> 1.0.0-1
- bpftrace: support for Flame Graphs
- bpftrace: context-sensitive auto completion for bpftrace probes, builtin variables and functions incl. help texts
- bpftrace: parse output of bpftrace scripts (e.g. using `printf()`) as CSV and display it in the Grafana table panel
- bpftrace: sample dashboards (BPFtrace System Analysis, BPFtrace Flame Graphs)
- vector: table output: show instance name in left column
- vector: table output: support non-matching instance names (cells of metrics which don't have the specific instance will be blank)
- vector & bpftrace: if the metric/script gets changed in the query editor, immeditately stop polling the old metric/deregister the old script
- vector & bpftrace: improve pmwebd compatibility
- misc: help texts for all datasources (visible with the **[ ? ]** button in the query editor)
- misc: renamed PCP Live to PCP Vector
- misc: logos for all datasources
- misc: improved error handling

* Fri Aug 16 2019 Andreas Gerstmayr <agerstmayr@redhat.com> 0.0.7-1
- converted into a Grafana app plugin, renamed to grafana-pcp
- redis: support for instance domains, labels, autocompletion, automatic rate conversation
- live and bpftrace: initial commit of datasources

* Tue Jun 11 2019 Mark Goodwin <mgoodwin@redhat.com> 0.0.6-1
- renamed package to grafana-pcp-redis, updated README, etc

* Wed Jun 05 2019 Mark Goodwin <mgoodwin@redhat.com> 0.0.5-1
- renamed package to grafana-pcp-datasource, README, etc

* Fri May 17 2019 Mark Goodwin <mgoodwin@redhat.com> 0.0.4-1
- add suggested pmproxy URL in config html
- updated instructions and README.md now that grafana is in Fedora

* Fri Apr 12 2019 Mark Goodwin <mgoodwin@redhat.com> 0.0.3-1
- require grafana v6.1.3 or later
- install directory is now below /var/lib/grafana/plugins

* Wed Mar 20 2019 Mark Goodwin <mgoodwin@redhat.com> 0.0.2-1
- initial version
