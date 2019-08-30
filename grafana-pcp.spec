Name:           grafana-pcp
Version:        0.0.7
Release:        1%{?dist}
Summary:        Performance Co-Pilot App for Grafana

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
Requires:       pcp >= 4.3.4
Requires:       grafana >= 6.2.2
Suggests:       redis >= 5.0.4

# Bundled npm packages
Provides: bundled(nodejs-@babel/cli) = 7.5.5
Provides: bundled(nodejs-@babel/core) = 7.5.5
Provides: bundled(nodejs-@babel/preset-env) = 7.5.5
Provides: bundled(nodejs-@babel/preset-typescript) = 7.3.3
Provides: bundled(nodejs-@types/benchmark) = 1.0.31
Provides: bundled(nodejs-@types/grafana) = 4.6.3
Provides: bundled(nodejs-@types/jest) = 23.3.14
Provides: bundled(nodejs-@types/lodash) = 4.14.136
Provides: bundled(nodejs-babel-jest) = 24.8.0
Provides: bundled(nodejs-babel-loader) = 8.0.6
Provides: bundled(nodejs-benchmark) = 2.1.4
Provides: bundled(nodejs-clean-webpack-plugin) = 0.1.19
Provides: bundled(nodejs-copy-webpack-plugin) = 4.6.0
Provides: bundled(nodejs-core-js) = 3.1.4
Provides: bundled(nodejs-css-loader) = 1.0.1
Provides: bundled(nodejs-expr-eval) = 1.2.3
Provides: bundled(nodejs-jest) = 24.8.0
Provides: bundled(nodejs-jest-date-mock) = 1.0.7
Provides: bundled(nodejs-jsdom) = 9.12.0
Provides: bundled(nodejs-lodash) = 4.17.15
Provides: bundled(nodejs-mocha) = 6.2.0
Provides: bundled(nodejs-ng-annotate-webpack-plugin) = 0.3.0
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
pmseries, live metrics and the bpftrace PMDA, and several example dashboards.

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
