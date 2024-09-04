%define nijigenerate_ver 0.7.1
%define nijigenerate_dist 1073
%define nijigenerate_short 0f6d1ff

%define nijigenerate_suffix ^%{nijigenerate_dist}.git%{nijigenerate_short}

Name:           nijigenerate-nightly
Version:        %{nijigenerate_ver}%{?nijigenerate_suffix:}
Release:        %autorelease
Summary:        Tool to create and edit nijilive puppets

# Bundled lib licenses
##   bcaa licenses: BSL-1.0
##   bindbc-loader licenses: BSL-1.0
##   bindbc-sdl licenses: BSL-1.0
##   dcv licenses: BSL-1.0
##   ddbus licenses: MIT
##   dportals licenses: BSD-2-Clause
##   dunit licenses: MIT
##   dxml licenses: BSL-1.0
##   fghj licenses: BSL-1.0
##   i18n-d licenses: BSD-2-Clause
##   i2d-imgui licenses: BSL-1.0 and MIT
##   i2d-opengl licenses: BSL-1.0
##   imagefmt licenses: BSD-2-Clause
##   inmath licenses: BSD-2-Clause
##   kra-d licenses: BSD-2-Clause
##   mir-algorithm licenses: Apache-2.0
##   mir-core licenses: Apache-2.0
##   mir-linux-kernel licenses: BSL-1.0
##   mir-random licenses: Apache-2.0
##   nijilive licenses: BSD-2-Clause
##   psd-d licenses: BSD-2-Clause
##   silly licenses: ISC
##   tinyfiledialogs licenses: Zlib
License:        BSD-2-Clause and Apache-2.0 and BSL-1.0 and ISC and MIT and Zlib

URL:            https://github.com/grillo-delmal/nijigenerate-nightly

Source0:        https://github.com/grillo-delmal/nijigenerate-nightly/releases/download/nightly/nijigenerate-source.zip
Source1:        nijigenerate-nightly.desktop
Source2:        nijigenerate-nightly.appdata.xml
Source3:        dub.selections.json

# dlang
BuildRequires:  ldc
BuildRequires:  dub
BuildRequires:  jq

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  git

#dportals reqs
BuildRequires:       dbus-devel

#i2d-imgui reqs
BuildRequires:       cmake
BuildRequires:       gcc
BuildRequires:       gcc-c++
BuildRequires:       freetype-devel
BuildRequires:       SDL2-devel

Requires:       hicolor-icon-theme

#dportals deps
Requires:       dbus

#i2d-imgui deps
Requires:       libstdc++
Requires:       freetype
Requires:       SDL2


%description
nijilive is a framework for realtime 2D puppet animation which can be used for VTubing, 
game development and digital animation. 
nijigenerate is a tool that lets you create and edit nijilive puppets.
This is a nightly build of nijigenerate!
nijigenerate may crash unexpectedly and you will likely encounter bugs.
Make sure to save and back up your work often!

%prep
%setup -c

jq "map(.path = ([\"$(pwd)\"] + (.path | split(\"/\"))[-4:] | join(\"/\")) )" <<<$(<.dub/packages/local-packages.json) > .dub/packages/local-packages.linux.json
rm .dub/packages/local-packages.json
mv .dub/packages/local-packages.linux.json .dub/packages/local-packages.json
dub add-local .flatpak-dub/semver/*/semver
dub add-local .flatpak-dub/gitver/*/gitver

%build
export DFLAGS="%{_d_optflags}"

# Build metadata
dub build --skip-registry=all --compiler=ldc2 --config=meta

# Build the project, with its main file included, without unittests
dub build --skip-registry=all --compiler=ldc2 --config=linux-nightly --build=debug


%install
install -d ${RPM_BUILD_ROOT}%{_bindir}
install -p ./out/nijigenerate ${RPM_BUILD_ROOT}%{_bindir}/nijigenerate-nightly

install -d ${RPM_BUILD_ROOT}%{_datadir}/applications/
install -p -m 644 %SOURCE1 ${RPM_BUILD_ROOT}%{_datadir}/applications/nijigenerate-nightly.desktop
desktop-file-validate \
    ${RPM_BUILD_ROOT}%{_datadir}/applications/nijigenerate-nightly.desktop

install -d ${RPM_BUILD_ROOT}%{_metainfodir}/
install -p -m 644 %SOURCE2 ${RPM_BUILD_ROOT}%{_metainfodir}/nijigenerate-nightly.appdata.xml
appstream-util validate-relax --nonet \
    ${RPM_BUILD_ROOT}%{_metainfodir}/nijigenerate-nightly.appdata.xml

install -d $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/256x256/apps/
install -p -m 644 ./res/logo_256.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/256x256/apps/nijigenerate-nightly.png

install -d ${RPM_BUILD_ROOT}%{_datadir}/nijigenerate-nightly/
install -p -m 644 %SOURCE3 ${RPM_BUILD_ROOT}%{_datadir}/nijigenerate-nightly/dub.selections.json


%files
%license LICENSE
%{_bindir}/nijigenerate-nightly
%{_metainfodir}/nijigenerate-nightly.appdata.xml
%{_datadir}/applications/nijigenerate-nightly.desktop
%{_datadir}/icons/hicolor/256x256/apps/nijigenerate-nightly.png
%{_datadir}/nijigenerate-nightly/dub.selections.json


%changelog
%autochangelog
