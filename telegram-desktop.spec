# Telegram Desktop's constants...
%global qtversion 5.6.2
%global appname tdesktop

# Git revision of GYP...
%global commit3 a7055b3989c1074adca03b4b4829e7f0e57f6efd
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})

# Git revision of Breakpad...
%global commit4 2b7724245b7298df872983cdec941be877ea9b62
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})

# Git revision of Breakpad-lss...
%global commit5 5cedb6bf4e42ebb0a90603535321a265b72d3709
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})

# Git revision of GSL...
%global commit6 3819df6e378ffccf0e29465afe99c3b324c2aa70
%global shortcommit6 %(c=%{commit6}; echo ${c:0:7})

Summary: Telegram is a new era of messaging
Name: telegram-desktop
Version: 1.0.21
Release: 1%{?dist}

Group: Applications/Internet
License: GPLv3
URL: https://github.com/telegramdesktop/%{appname}

Source0: %{url}/archive/v%{version}.tar.gz#/%{appname}-%{version}.tar.gz
Source1: https://download.qt.io/official_releases/qt/5.6/%{qtversion}/submodules/qtbase-opensource-src-%{qtversion}.tar.xz
Source2: https://download.qt.io/official_releases/qt/5.6/%{qtversion}/submodules/qtimageformats-opensource-src-%{qtversion}.tar.xz
Source3: https://chromium.googlesource.com/external/gyp/+archive/%{commit3}.tar.gz#/gyp-%{shortcommit3}.tar.gz
Source4: https://chromium.googlesource.com/breakpad/breakpad/+archive/%{commit4}.tar.gz#/breakpad-%{shortcommit4}.tar.gz
Source5: https://chromium.googlesource.com/linux-syscall-support/+archive/%{commit5}.tar.gz#/breakpad-lss-%{shortcommit5}.tar.gz
Source6: https://github.com/Microsoft/GSL/archive/%{commit6}.tar.gz#/GSL-%{shortcommit6}.tar.gz

Source101: telegram.desktop
Source102: telegram-desktop.appdata.xml
Source103: tg.protocol

Patch0: fix_build_under_fedora.patch
Patch1: fix_cmake.patch
Patch2: qtbase-opensource-src-5.6.2-QTBUG-56514.patch

Requires: hicolor-icon-theme
BuildRequires: desktop-file-utils
BuildRequires: libappstream-glib
BuildRequires: ffmpeg-devel >= 3.1
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: chrpath
BuildRequires: cmake
BuildRequires: libwayland-client-devel
BuildRequires: libwayland-server-devel
BuildRequires: libwayland-cursor-devel
BuildRequires: libproxy-devel
BuildRequires: libxcb-devel
BuildRequires: libogg-devel
BuildRequires: xz-devel
BuildRequires: libappindicator-devel
BuildRequires: libunity-devel
BuildRequires: libstdc++-devel
BuildRequires: libwebp-devel
BuildRequires: libpng-devel
BuildRequires: xorg-x11-util-macros
BuildRequires: gettext-devel
BuildRequires: libICE-devel
BuildRequires: libSM-devel
BuildRequires: libXi-devel
BuildRequires: openjpeg-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: zlib-devel
BuildRequires: libexif-devel
BuildRequires: opus-devel
BuildRequires: portaudio-devel
BuildRequires: openal-soft-devel
BuildRequires: xcb-util-devel
BuildRequires: xcb-util-wm-devel
BuildRequires: xcb-util-xrm-devel
BuildRequires: xcb-util-image-devel
BuildRequires: xcb-util-cursor-devel
BuildRequires: xcb-util-keysyms-devel
BuildRequires: xcb-util-renderutil-devel
BuildRequires: libva-devel
BuildRequires: libvdpau-devel
BuildRequires: libxkbcommon-devel
BuildRequires: libxkbcommon-x11-devel
BuildRequires: harfbuzz-devel
BuildRequires: pcre-devel
%if 0%{?fedora} >= 26
BuildRequires: compat-openssl10-devel
%else
BuildRequires: openssl-devel
%endif

Provides: bundled(qt5-qtbase) = %{qtversion}
Provides: bundled(qt5-qtimageformats) = %{qtversion}

%description
Telegram is a messaging app with a focus on speed and security, it’s super
fast, simple and free. You can use Telegram on all your devices at the same
time — your messages sync seamlessly across any of your phones, tablets or
computers.

With Telegram, you can send messages, photos, videos and files of any type
(doc, zip, mp3, etc), as well as create groups for up to 200 people. You can
write to your phone contacts and find people by their usernames. As a result,
Telegram is like SMS and email combined — and can take care of all your
personal or business messaging needs.

%prep
# Setting some constants...
qtv=%{qtversion}
qtdir="%_builddir/Libraries/qt${qtv//./_}"
qtpatch="%_builddir/%{appname}-%{version}/Telegram/Patches/qtbase_${qtv//./_}.diff"

# Creating directory for libraries...
mkdir -p "$qtdir"

# Unpacking Telegram Desktop source archive...
tar -xf %{SOURCE0}

# Patching Telegram Desktop...
cd "%_builddir/%{appname}-%{version}"
%patch0 -p1
%patch1 -p1

# Unpacking Qt...
cd "$qtdir"
tar -xf %{SOURCE1}
mv -f "qtbase-opensource-src-%{qtversion}" "qtbase"
tar -xf %{SOURCE2}
mv -f "qtimageformats-opensource-src-%{qtversion}" "qtimageformats"

# Applying Qt patch by Telegram Desktop team...
cd "$qtdir/qtbase"
patch -p1 -i "$qtpatch"

# Applying QTBUG-56514 patch for Fedora Rawhide (GCC 7.x)...
%if 0%{?fedora} >= 26
%patch2 -p1
%endif

# Unpacking GYP...
mkdir -p "%_builddir/Libraries/gyp"
cd "%_builddir/Libraries/gyp"
tar -xf %{SOURCE3}

# Applying GYP patch...
patch -p1 -i "%_builddir/%{appname}-%{version}/Telegram/Patches/gyp.diff"

# Unpacking breakpad with lss support...
mkdir -p "%_builddir/Libraries/breakpad"
cd "%_builddir/Libraries/breakpad"
tar -xf %{SOURCE4}
mkdir -p "%_builddir/Libraries/breakpad/src/third_party/lss"
cd "%_builddir/Libraries/breakpad/src/third_party/lss"
tar -xf %{SOURCE5}

# Unpacking GSL...
cd "%_builddir/Libraries"
tar -xf %{SOURCE6}
mv GSL-%{commit6} GSL

%build
# Setting some constants...
qtv=%{qtversion}
qtdir="%_builddir/Libraries/qt${qtv//./_}"

# Building breakpad...
cd "%_builddir/Libraries/breakpad"
%configure
%make_build

# Building patched Qt...
cd "$qtdir/qtbase"
./configure \
    -prefix "%_builddir/qt" \
    -release \
    -opensource \
    -confirm-license \
    -system-zlib \
    -system-libpng \
    -system-libjpeg \
    -system-freetype \
    -system-harfbuzz \
    -system-pcre \
    -system-xcb \
    -system-xkbcommon-x11 \
    -no-opengl \
    -no-gtkstyle \
    -static \
    -nomake examples \
    -nomake tests
%make_build
make install

# Exporting new PATH...
export PATH="%_builddir/qt/bin:$PATH"

# Building Qt image plugins...
cd "$qtdir/qtimageformats"
qmake .
%make_build
make install

# Building Telegram Desktop...
cd "%_builddir/%{appname}-%{version}/Telegram"
gyp/refresh.sh
cd "%_builddir/%{appname}-%{version}/out/Release"
%make_build

%install
# Installing executables...
cd "%_builddir/%{appname}-%{version}/out/Release"
mkdir -p "%{buildroot}%{_bindir}"
chrpath -d Telegram
strip Telegram
install -m 755 Telegram "%{buildroot}%{_bindir}/%{name}"

# Installing desktop shortcut...
desktop-file-install --dir="%{buildroot}%{_datadir}/applications" "%{SOURCE101}"

# Installing icons...
for size in 16 32 48 64 128 256 512; do
	dir="%{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps"
	install -d "$dir"
	install -m 644 "%_builddir/%{appname}-%{version}/Telegram/Resources/art/icon${size}.png" "$dir/%{name}.png"
done

# Installing tg protocol handler...
install -d "%{buildroot}%{_datadir}/kde4/services"
install -m 644 "%{SOURCE103}" "%{buildroot}%{_datadir}/kde4/services/tg.protocol"

# Installing appdata for Gnome Software...
install -d "%{buildroot}%{_datadir}/appdata"
install -m 644 "%{SOURCE102}" "%{buildroot}%{_datadir}/appdata/%{name}.appdata.xml"

%check
appstream-util validate-relax --nonet "%{buildroot}%{_datadir}/appdata/%{name}.appdata.xml"

%post
/bin/touch --no-create %{_datadir}/mime/packages &>/dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :

%posttrans
/usr/bin/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc %{appname}-%{version}/README.md %{appname}-%{version}/changelog.txt
%license %{appname}-%{version}/LICENSE
%{_bindir}/%{name}
%{_datadir}/applications/telegram.desktop
%{_datadir}/kde4/services/tg.protocol
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/appdata/%{name}.appdata.xml

%changelog
* Sat Mar 11 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.21-1
- Updated to 1.0.21 (alpha).

* Thu Mar 09 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.20-1
- Updated to 1.0.20 (alpha).

* Wed Mar 08 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.19-1
- Updated to 1.0.19 (alpha).

* Sat Mar 04 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.18-2
- Fixed build of latest commits. Added GSL support.

* Thu Mar 02 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.18-1
- Updated to 1.0.18 (alpha).

* Tue Feb 28 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.17-1
- Updated to 1.0.17 (alpha).

* Mon Feb 27 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.15-1
- Updated to 1.0.15 (alpha).

* Tue Feb 21 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.14-1
- Updated to 1.0.14.

* Mon Feb 20 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.13-1
- Updated to 1.0.13.
- Added changelog.txt to documents.

* Sun Feb 19 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.12-1
- Updated to 1.0.12.

* Fri Feb 17 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.11-1
- Updated to 1.0.11 (alpha).

* Sun Feb 12 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.9-1
- Updated to 1.0.9 (alpha).
- Updated GYP, Breakpad and LSS to latest commits.

* Thu Feb 02 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.6-2
- Backported QTBUG-56514 patch to fix building under GCC 7.0.

* Wed Feb 01 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.6-1
- Updated to 1.0.6.

* Fri Jan 27 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.3-1
- Updated to 1.0.3 (alpha).

* Thu Jan 19 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.2-1
- Updated to 1.0.2.

* Tue Jan 17 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.1-1
- Updated to 1.0.1.

* Thu Jan 12 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.0-1
- Updated to 1.0.0.

* Wed Jan 11 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.27-1
- Updated to 0.10.27 (alpha).

* Sat Jan 07 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.26-1
- Updated to 0.10.26 (alpha).

* Thu Jan 05 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.25-1
- Updated to 0.10.25 (alpha). Added patch to build with GCC 6.3.1.

* Mon Jan 02 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.23-1
- Updated to 0.10.23 (alpha). Updated externals to latest commits.

* Tue Dec 20 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.20-1
- Updated to 0.10.20.

* Sun Oct 30 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.19-2
- Fixed build under Fedora Rawhide (26).

* Tue Oct 25 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.19-1
- Updated to 0.10.19.

* Fri Oct 21 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.16-2
- Use specified revisions of 3rd-party libraries.

* Thu Oct 20 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.16-1
- Updated to 0.10.16.

* Wed Oct 19 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.15-1
- Updated to 0.10.15.

* Tue Oct 18 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.14-1
- Updated to 0.10.14.

* Sat Oct 08 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.11-3
- GYP will now export correct build flags for project.

* Sat Oct 08 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.11-2
- Will use configure macro to export correct build flags.

* Mon Oct 03 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.11-1
- Updated to 0.10.11.

* Wed Sep 21 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.7-1
- Updated to 0.10.7.

* Tue Sep 20 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.6-3
- Added new patch to build project using systemwide cmake.

* Sat Sep 17 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.6-2
- Created new SPEC.
- Added installation of tg protocol and mime-handler.

* Wed Sep 14 2016 Arkady L. Shane <ashejn@russianfedora.pro> 0.10.6-1
- update to 0.10.6

* Mon Aug  8 2016 Arkady L. Shane <ashejn@russianfedora.pro> 0.10.1-2
- added appdata file

* Mon Aug  8 2016 Arkady L. Shane <ashejn@russianfedora.pro> 0.10.1-1
- update to 0.10.1

* Thu Aug  4 2016 Arkady L. Shane <ashejn@russianfedora.pro> 0.10.0-1
- update to 0.10.0

* Mon Jun 27 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.56-1.R
- update to 0.9.56

* Thu Jun 16 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.51-1.R
- update to 0.9.51

* Wed May 25 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.49-1.R
- update to 0.9.49

* Wed May 11 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.48-1.R
- update to 0.9.48

* Thu Apr 14 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.42-1.R
- update to 0.9.42

* Wed Apr 13 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.41-1.R
- update to 0.9.41

* Tue Apr  5 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.40-1.R
- update to 0.9.40

* Wed Mar 16 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.33-1.R
- update to 0.9.33

* Tue Mar 15 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.32-1.R
- update to 0.9.32

* Mon Feb 29 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.28-1.R
- update to 0.9.28

* Tue Feb 23 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.26-1.R
- update to 0.9.26

* Wed Feb 17 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.24-1.R
- update to 0.9.18

* Sun Jan 10 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.18-1.R
- update to 0.9.18

* Thu Dec 10 2015 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.15-1.R
- update to 0.9.15

* Thu Nov 26 2015 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.13-1.R
- update to 0.9.13

* Fri Nov 13 2015 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.10-1.R
- update to 0.9.10

* Tue Oct 27 2015 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.6-1.R
- clean up spec
- update to 0.9.6

* Mon Aug 03 2015 rommon <rommon@t-online.de> - 0.8.45-1
- update to new version

* Sat Jul 18 2015 rommon <rommon@t-online.de> - 0.8.38-1
- update to new version

* Fri Jun 26 2015 rommon <rommon@t-online.de> - 0.8.32-1
- update to new version
- rename from telegram to telegram-desktop

* Tue Jun 9 2015 rommon <rommon@t-online.de> - 0.8.24-1
- update to new version

* Fri May 1 2015 rommon <rommon@t-online.de> - 0.8.11-1
- update to new version

* Mon Apr 27 2015 rommon <rommon@t-online.de> - 0.8.7-1
- update to new version

* Mon Apr 27 2015 rommon <rommon@t-online.de> - 0.8.4-5
- fix icon permissions

* Fri Apr 24 2015 rommon <rommon@t-online.de> - 0.8.4-4
- fix desktop file

* Tue Apr 21 2015 rommon <rommon@t-online.de> - 0.8.4-3
- changed desktop file

* Tue Apr 21 2015 rommon <rommon@t-online.de> - 0.8.4-2
- adaption for 32/64 bit builds

* Tue Apr 21 2015 rommon <rommon@t-online.de> - 0.8.4-1
- initial package
