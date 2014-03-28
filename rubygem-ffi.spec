%{!?ruby_sitearch: %global ruby_sitearch %(ruby -rrbconfig -e "puts Config::CONFIG['sitearchdir']")}
%global gem_name ffi
%global libname %{gem_name}_c.so
%global githubhash b79eb61
%global githubbuild 0
%global tarballname ffi-ffi-%{version}-%{githubbuild}-g%{githubhash}
%global gitinternalname ffi-ffi-%{githubhash}

Name:           rubygem-%{gem_name}
Version:        1.0.9
Release:        9%{?dist}
Summary:        FFI Extensions for Ruby
Group:          Development/Languages

License:        LGPLv3
URL:            http://wiki.github.com/ffi/ffi
# The source file is hosted at github. You can access this tarball with
# the following link:
#          http://github.com/ffi/ffi/tarball/1.0.9
Source0:        %{tarballname}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ruby-devel rubygems-devel rubygem(rake) rubygem(rake-compiler) libffi-devel rubygem(rspec-core)
BuildRequires:  pkgconfig
Requires:       libffi
Requires: ruby(rubygems)
Requires:       ruby(abi) = 1.8
Provides:       rubygem(%{gem_name}) = %{version}

%description
Ruby-FFI is a ruby extension for programmatically loading dynamic
libraries, binding functions within them, and calling those functions
from Ruby code. Moreover, a Ruby-FFI extension works without changes
on Ruby and JRuby. Discover why should you write your next extension
using Ruby-FFI here[http://wiki.github.com/ffi/ffi/why-use-ffi].

%prep
%setup -q -n %{gitinternalname}

%build
export CFLAGS="%{optflags}"
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
rake gem
gem install -V -d --local --no-ri -i ./geminst --force pkg/%{gem_name}-%{version}.gem

%install
rm -rf %{buildroot}
mkdir %{buildroot}
install -d -m0755 %{buildroot}%{gem_dir}
install -d -m0755  %{buildroot}%{ruby_sitearch}
cp -R %{_builddir}/%{gitinternalname}/geminst/* %{buildroot}%{gem_dir}
mv %{buildroot}%{gem_libdir}/%{libname} %{buildroot}%{ruby_sitearch}/%{libname}
rm -rf %{buildroot}%{gem_instdir}/ext

%check
# https://github.com/ffi/ffi/issues/189
sed -i -e 's| -mimpure-text||' libtest/GNUmakefile
rake -v test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/History.txt
%doc %{gem_instdir}/LICENSE
%doc %{gem_docdir}
%dir %{gem_instdir}
# This file does not exist in 15
%if 0%{?fedora} <= 14
    %{gem_instdir}/.require_paths
%endif
%{gem_instdir}/Rakefile
%{gem_instdir}/gen
%{gem_libdir}
%{gem_instdir}/spec
%{gem_instdir}/tasks
%{ruby_sitearch}/%{libname}
%{gem_cache}
%{gem_spec}


%changelog
* Wed Mar 26 2014 Dominic Cleal <dcleal@redhat.com> - 1.0.9-9
- Fix install location of built library and gemspec (RHBZ#975332)

* Thu Jan 07 2013 Bryan Kearney <bkearney@redhat.com> - 1.0.9-8
- Change the ruby version back to 1.8

* Thu Jan 03 2013 Bryan Kearney <bkearney@redhat.com> - 1.0.9-7
- Add the gem macros which rubygems-devel would have provided

* Wed Jan 01 2013 Bryan Kearney <bkearney@redhat.com> - 1.0.9-6
- Change dependency to rubygems instead of rubgems-devel

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

* Tue Feb 22 2010 Bryan Kearney <bkearney@redhat.com> - 0.6.2-1
- Pull in 0.6.2 from upstream

* Tue Feb 22 2010 Bryan Kearney <bkearney@redhat.com> - 0.5.4-3
- Final updates based on package review

* Tue Feb 16 2010 Bryan Kearney <bkearney@redhat.com> - 0.5.4-2
- Updates Based on code review comments

* Mon Feb 15 2010 Bryan Kearney <bkearney@redhat.com> - 0.5.4-1
- Initial specfile
