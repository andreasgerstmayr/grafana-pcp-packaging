Name:           grafana-pcp
Version:        1.0.0
Release:        1%{?dist}
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
Requires:       grafana >= 6.2.2
Suggests:       pcp >= 5.0.0
Suggests:       redis >= 5.0.0
Suggests:       bpftrace >= 0.9.2

# Obsolete old webapps
Obsoletes:	pcp-webjs
Obsoletes:	pcp-webapp-blinkenlights
Obsoletes:	pcp-webapp-grafana
Obsoletes:	pcp-webapp-graphite
Obsoletes:	pcp-webapp-vector

# Bundled npm packages
Provides: bundled(nodejs-@babel/cli) = 7.5.5
Provides: bundled(nodejs-@babel/core) = 7.5.5
Provides: bundled(nodejs-@babel/preset-env) = 7.5.5
Provides: bundled(nodejs-@babel/preset-react) = 7.0.0
Provides: bundled(nodejs-@babel/preset-typescript) = 7.3.3
Provides: bundled(nodejs-@grafana/data) = 6.4.0
Provides: bundled(nodejs-@grafana/ui) = 6.4.0
Provides: bundled(nodejs-@types/benchmark) = 1.0.31
Provides: bundled(nodejs-@types/d3) = 5.7.2
Provides: bundled(nodejs-@types/grafana) = 4.6.3
Provides: bundled(nodejs-@types/jest) = 24.0.17
Provides: bundled(nodejs-@types/lodash) = 4.14.136
Provides: bundled(nodejs-babel-jest) = 24.8.0
Provides: bundled(nodejs-babel-loader) = 8.0.6
Provides: bundled(nodejs-babel-plugin-angularjs-annotate) = 0.10.0
Provides: bundled(nodejs-benchmark) = 2.1.4
Provides: bundled(nodejs-clean-webpack-plugin) = 0.1.19
Provides: bundled(nodejs-copy-webpack-plugin) = 4.6.0
Provides: bundled(nodejs-core-js) = 3.1.4
Provides: bundled(nodejs-css-loader) = 1.0.1
Provides: bundled(nodejs-d3-flame-graph) = 2.1.2
Provides: bundled(nodejs-d3-selection) = 1.4.0
Provides: bundled(nodejs-expr-eval) = 1.2.3
Provides: bundled(nodejs-jest) = 24.8.0
Provides: bundled(nodejs-jest-date-mock) = 1.0.7
Provides: bundled(nodejs-jsdom) = 9.12.0
Provides: bundled(nodejs-lodash) = 4.17.15
Provides: bundled(nodejs-memoize-one) = 5.1.1
Provides: bundled(nodejs-mocha) = 6.2.0
Provides: bundled(nodejs-prunk) = 1.3.1
Provides: bundled(nodejs-q) = 1.5.1
Provides: bundled(nodejs-regenerator-runtime) = 0.12.1
Provides: bundled(nodejs-request) = 2.88.0
Provides: bundled(nodejs-style-loader) = 0.22.1
Provides: bundled(nodejs-ts-jest) = 24.0.2
Provides: bundled(nodejs-ts-loader) = 4.5.0
Provides: bundled(nodejs-tslint) = 5.18.0
Provides: bundled(nodejs-tslint-config-airbnb) = 5.11.1
Provides: bundled(nodejs-typescript) = 3.5.3
Provides: bundled(nodejs-uglifyjs-webpack-plugin) = 2.2.0
Provides: bundled(nodejs-weak) = 1.0.1
Provides: bundled(nodejs-webpack) = 4.39.1
Provides: bundled(nodejs-webpack-cli) = 3.3.6


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
