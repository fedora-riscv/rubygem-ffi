%global gem_name ffi

Name: rubygem-%{gem_name}
Version: 1.9.18
Release: 1%{?dist}
Summary: FFI Extensions for Ruby
Group: Development/Languages

License: BSD
URL: http://wiki.github.com/ffi/ffi
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby-devel
BuildRequires: libffi-devel
BuildRequires: rubygem(rspec2)

%description
Ruby-FFI is a ruby extension for programmatically loading dynamic
libraries, binding functions within them, and calling those functions
from Ruby code. Moreover, a Ruby-FFI extension works without changes
on Ruby and JRuby. Discover why should you write your next extension
using Ruby-FFI here[http://wiki.github.com/ffi/ffi/why-use-ffi].

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/{gem.build_complete,*.so} %{buildroot}%{gem_extdir_mri}/

# Prevent dangling symlink in -debuginfo (rhbz#878863).
rm -rf %{buildroot}%{gem_instdir}/ext/


# Fix the permissions.
# https://github.com/ffi/ffi/pull/545
chmod a-x %{buildroot}%{gem_libdir}/ffi/platform/i386-cygwin/types.conf
chmod a-x %{buildroot}%{gem_libdir}/ffi/platform/x86_64-cygwin/types.conf


%check
pushd .%{gem_instdir}
# Build the test library with Fedora build options.
pushd spec/ffi/fixtures
make JFLAGS="%{optflags}"
popd

rspec2 -I$(dirs +1)%{gem_extdir_mri} spec
popd

%files
%dir %{gem_instdir}
%{gem_extdir_mri}
%license %{gem_instdir}/COPYING
%license %{gem_instdir}/LICENSE
%exclude %{gem_instdir}/ffi.gemspec
%exclude %{gem_instdir}/gen
%{gem_libdir}
%exclude %{gem_instdir}/libtest
%exclude %{gem_instdir}/spec
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile

%changelog
* Fri Mar 31 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.18-1
- 1.9.18

* Fri Feb 10 2017 Jun Aruga <jaruga@redhat.com> - 1.9.14-3
- Suppress deprecated Fixnum warnings on Ruby 2.4.0.

* Tue Jan 10 2017 Vít Ondruch <vondruch@redhat.com> - 1.9.14-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.4

* Tue Jan 03 2017 Vít Ondruch <vondruch@redhat.com> - 1.9.14-1
- Update to FFI 1.9.14.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 08 2016 Vít Ondruch <vondruch@redhat.com> - 1.9.10-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.3

* Sat Oct  3 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.10-1
- 1.9.10

* Mon Jul 20 2015 Vít Ondruch <vondruch@redhat.com> - 1.9.3-7
- Fix dangling symlinks in -debuginfo package.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 23 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 1.9.3-5
- fixed to build on aarch64

* Fri Jan 16 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.3-4
- Rebuild for ruby 2.2 again

* Thu Jan 15 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.3-3
- Rebuild for ruby 2.2
- Use rspec2 for now

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 05 2014 Dominic Cleal <dcleal@redhat.com> - 1.9.3-1
- Update to FFI 1.9.3

* Sat May  3 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.0-4
- F-21: rebuild for ruby 2.1 / rubygems 2.2

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Vít Ondruch <vondruch@redhat.com> - 1.4.0-2
- Use %%{gem_extdir_mri} instead of %%{gem_extdir}.

* Wed Feb 20 2013 Vít Ondruch <vondruch@redhat.com> - 1.4.0-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to FFI 1.4.0.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 1.0.9-4
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 14 2011 Bryan Kearney <bkearney@redhat.com> - 1.0.9-2
- Fixed the License, it is actually LGPL

* Mon Jun 13 2011 Bryan Kearney <bkearney@redhat.com> - 1.0.9-1
- Bring in 1.0.9 from upstream.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Mar 10 2010 Bryan Kearney <bkearney@redhat.com> - 0.6.2-1
- Power PC fixes from upstream which were found testing 0.6.2

* Mon Feb 22 2010 Bryan Kearney <bkearney@redhat.com> - 0.6.2-1
- Pull in 0.6.2 from upstream

* Mon Feb 22 2010 Bryan Kearney <bkearney@redhat.com> - 0.5.4-3
- Final updates based on package review

* Tue Feb 16 2010 Bryan Kearney <bkearney@redhat.com> - 0.5.4-2
- Updates Based on code review comments

* Mon Feb 15 2010 Bryan Kearney <bkearney@redhat.com> - 0.5.4-1
- Initial specfile
