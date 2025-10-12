%define		crates_ver	0.5.18

Summary:	Tool to "cargo vendor" with filtering
Summary(pl.UTF-8):	Narzędzie do "cargo vendor" z filtrowaniem
Name:		cargo-vendor-filterer
Version:	0.5.18
Release:	1
License:	Apache v2.0
Group:		Applications
Source0:	https://github.com/coreos/cargo-vendor-filterer/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	fa5e8e4c56ba81b12adf70bcb984e855
Source1:	%{name}-crates-%{crates_ver}.tar.xz
# Source1-md5:	3a187bef2982d868e3afefe3ac895af1
Patch0:		tier2-platforms-without-host-tools.patch
URL:		https://github.com/coreos/cargo-vendor-filterer
BuildRequires:	cargo
BuildRequires:	openssl-devel
BuildRequires:	rpmbuild(macros) >= 2.050
BuildRequires:	rust
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%{?rust_req}
Requires:	cargo
Requires:	rust
ExclusiveArch:	%{rust_arches}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The core "cargo vendor" tool is useful to save all dependencies.
However, it doesn't offer any filtering; today cargo includes all
platforms, but some projects only care about Linux for example.

%description -l pl.UTF-8
Podstawowe narzędzie "cargo vendor" jest przydatne do zapisywania
wszystkich zależności. Jednak nie oferuje żadnego filtrowania;
obecnie cargo obejmuje wszystkie platformy, ale niektóre projekty
wymagają np. tylko linuksowych.

%prep
%setup -q -a1
%patch -P0 -p1

%{__mv} %{name}-%{crates_ver}/* .
sed -i -e 's/@@VERSION@@/%{version}/' Cargo.lock

# use our offline registry
export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config <<EOF
[source.crates-io]
registry = 'https://github.com/rust-lang/crates.io-index'
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"

%cargo_build --frozen

%install
rm -rf $RPM_BUILD_ROOT
export CARGO_HOME="$(pwd)/.cargo"

%cargo_install --frozen --root $RPM_BUILD_ROOT%{_prefix} --path $PWD

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/cargo-vendor-filterer
