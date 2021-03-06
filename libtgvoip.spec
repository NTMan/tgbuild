Summary: VoIP library for Telegram clients
Name: libtgvoip
Version: 1.0.3
Release: 1%{?dist}

# Libtgvoip shared library - Public Domain.
# Bundled webrtc library - BSD with patented echo cancellation algorithms.
License: Public Domain and BSD
URL: https://github.com/grishka/%{name}

Source0: %{url}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0: %{name}-build-fixes.patch

Provides: bundled(webrtc-audio-processing) = 0.3
BuildRequires: pulseaudio-libs-devel
BuildRequires: alsa-lib-devel
BuildRequires: openssl-devel
BuildRequires: opus-devel
BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: gcc
BuildRequires: gyp

%description
Provides VoIP library for Telegram clients.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
%{summary}.

%prep
%autosetup -n %{name}-%{version} -p1

%build
export VOIPVER="%{version}"
gyp --format=cmake --depth=. --generator-output=. -Goutput_dir=out -Gconfig=Release %{name}.gyp

pushd out/Release
    %cmake .
    %make_build
popd

%install
# Installing shared library...
mkdir -p "%{buildroot}%{_libdir}"
install -m 0755 -p out/Release/lib.target/%{name}.so.%{version} "%{buildroot}%{_libdir}/%{name}.so.%{version}"
ln -s %{name}.so.%{version} "%{buildroot}%{_libdir}/%{name}.so.1.0"
ln -s %{name}.so.%{version} "%{buildroot}%{_libdir}/%{name}.so.1"
ln -s %{name}.so.%{version} "%{buildroot}%{_libdir}/%{name}.so"

# Installing additional development files...
mkdir -p "%{buildroot}%{_includedir}/%{name}/audio"
find . -maxdepth 1 -type f -name "*.h" -exec install -m 0644 -p '{}' %{buildroot}%{_includedir}/%{name} \;
find audio -maxdepth 1 -type f -name "*.h" -exec install -m 0644 -p '{}' %{buildroot}%{_includedir}/%{name}/audio \;

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license UNLICENSE
%{_libdir}/%{name}.so.*

%files devel
%{_includedir}/%{name}
%{_libdir}/%{name}.so

%changelog
* Fri Dec 29 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.3-1
- Updated to 1.0.3 (regular release).

* Sat Nov 18 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.1-2.20171111git6a0b3b2
- Provide compactibility with 1.0.

* Sat Nov 18 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.1-1.20171111git6a0b3b2
- Updated to 1.0.1-git.

* Fri Aug 04 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0-3.20170801gitbfd5cfe
- Fixed build on other architectures. Build against regular OpenSSL.

* Wed Aug 02 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0-2.20170801gitbfd5cfe
- Updated to latest snapshot. Small SPEC fixes. Added virtual provides.

* Tue Aug 01 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0-1.20170727git01f2701
- Initial release.
