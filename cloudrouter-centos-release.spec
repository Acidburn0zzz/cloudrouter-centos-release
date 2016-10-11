%define cr_display_name CloudRouter
%define cr_name cloudrouter
%define cr_version 4
%define cr_readme README.%{cr_display_name}-Release-Notes
# Set this to 'Beta' or 'Release' depending on what type of release is pending.
%define release_tag Release

%define base_display_name CentOS
%define base_name centos
%define base_version 7.2

%define project_url http://cloudrouter.org
%define bug_url https://cloudrouter.atlassian.net/secure/Dashboard.jspa

Summary:	%{cr_display_name} release files
Name:		%{cr_name}-%{base_name}-release
Version:	%{cr_version}
Release:	1
License:	AGPLv3
Source0:    GNU-AGPL-3.0.txt
Source1:    %{cr_readme}
Source2:    %{cr_readme}

Group:		System Environment/Base
Obsoletes:	redhat-release
Obsoletes:	%{cr_name}-release
Provides:	redhat-release
Provides:	system-release
Provides:	system-release(release)
Provides:   cloudrouter-release
BuildArch:	noarch
Conflicts:	%{base_name}-release
Requires:   cloudrouter-repo
Requires:   cloudrouter-test-repo
Requires:   centos-repo
Requires:   epel-release


%description
%{cr_display_name} release files such as the /etc/ files that
define the release.

%package notes
Summary:	Release Notes
License:	Open Publication
Group:		System Environment/Base
Provides:	system-release-notes = %{version}-%{release}
Provides:   cloudrouter-release-notes
Conflicts:	%{base_name}-release-notes

%description notes
CloudRouter release notes package. 

%prep
#%setup -q


%build
echo OK


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc
echo "%{cr_display_name} release %{version} (%{release_tag})" > $RPM_BUILD_ROOT/etc/%{cr_name}-release
echo "cpe:/o:%{cr_name}:%{cr_name}:%{version}" > $RPM_BUILD_ROOT/etc/system-release-cpe
cp -p $RPM_BUILD_ROOT/etc/cloudrouter-release $RPM_BUILD_ROOT/etc/issue
echo "Kernel \r on an \m (\l)" >> $RPM_BUILD_ROOT/etc/issue
echo >> $RPM_BUILD_ROOT/etc/issue
cp -p $RPM_BUILD_ROOT/etc/issue $RPM_BUILD_ROOT/etc/issue.net
ln -s cloudrouter-release $RPM_BUILD_ROOT/etc/redhat-release
ln -s cloudrouter-release $RPM_BUILD_ROOT/etc/system-release

cat << EOF >>$RPM_BUILD_ROOT/etc/os-release
NAME=%{cr_display_name}
VERSION="%{version} (%{release_tag})"
ID=%{cr_name}
VERSION_ID=%{version}
PRETTY_NAME="%{cr_display_name} %{version} (%{release_tag})"
ANSI_COLOR="0;34"
CPE_NAME="cpe:/o:%{cr_name}:%{cr_name}:%{version}"
HOME_URL="%{project_url}"
BUG_REPORT_URL="%{bug_url}"
EOF

# Set up the dist tag macros
install -d -m 755 $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d
cat >> $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.dist << EOF
# dist macros.

%%cloudrouter		%{cr_version}
%%dist		.cr%{cr_version}
%%cr%{cr_version}		%{cr_version}
EOF

# copy Release Notes
DOCS=( %{SOURCE0} %{SOURCE1} )
install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/CloudRouter
for file in "${DOCS[@]}"; do 
	install -m 644 $file %{buildroot}/%{_docdir}/CloudRouter
done



%clean
rm -rf $RPM_BUILD_ROOT


%post
# fix yum.conf
sed -i s-"^bugtracker_url=.*$"-"bugtracker_url=%{bug_url}"- /etc/yum.conf
sed -i s/"^distroverpkg=.*$"/"distroverpkg=%{name}"/ /etc/yum.conf


%files
%defattr(-,root,root,-)
%doc %{_docdir}/CloudRouter/*
%config %attr(0644,root,root) /etc/os-release
%config %attr(0644,root,root) /etc/%{cr_name}-release
/etc/redhat-release
/etc/system-release
%config %attr(0644,root,root) /etc/system-release-cpe
%config(noreplace) %attr(0644,root,root) /etc/issue
%config(noreplace) %attr(0644,root,root) /etc/issue.net
%attr(0644,root,root) %{_rpmconfigdir}/macros.d/macros.dist


%files notes
%defattr(-,root,root,-)
%doc %{_docdir}/CloudRouter/%{cr_readme}


%changelog
* Mon Oct 10 2016 John Siegrist <john@complects.com> - 4-1
- Updated version for CRv4

* Wed Dec 30 2015 John Siegrist <john@complects.com> - 3-1
- Updated version for CRv3
- Separated out the CentOS and CloudRouter RPM repository info.

* Tue Sep 01 2015 John Siegrist <john@complects.com> - 2-4
- Added dependency on epel-release so the CloudRouter dependencies in EPEL7 are accessible.

* Thu Aug 27 2015 John Siegrist <john@complects.com> - 2-3
- Added support for virtual package "cloudrouter-release".

* Fri Aug 14 2015 John Siegrist <john@complects.com> - 2-2
- Fixed GPG key verification for RPMs downloaded from the CloudRouter repository.

* Mon Aug 10 2015 John Siegrist <john@complects.com> - 2-1
- Initial commit of the Fedora-specific CloudRouter-release project after splitting it into separate ones for Fedora and CentOS.
