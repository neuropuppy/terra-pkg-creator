Name:           hello
Version:        2.12.1
Release:        1%{?dist}
Summary:        A "Hello, World!" program

URL:            https://www.gnu.org/software/hello/
Source0:        https://ftp.gnu.org/pub/gnu/hello/hello-%{version}.tar.gz

License:        GPL-3.0-or-later
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  texinfo

%description
GNU Hello is a program that displays "Hello, World!" on the terminal.
It's a simple example of a well-documented, traditional program.

%prep
%autosetup

%build
%configure
%make_build

%install
%make_install

%files
%{_bindir}/hello
%{_mandir}/man1/hello.1*
%{_datadir}/info/hello.info*

%changelog
* Sat Feb 03 2024 Example Packager <packager@example.com> - 2.12.1-1
- Initial package for Terra