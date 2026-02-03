# Language-Specific Packaging Guidelines

Complete guidelines for packaging software written in specific languages.

## Rust

**Build dependencies:**
```
BuildRequires: anda-srpm-macros
BuildRequires: cargo-rpm-macros
BuildRequires: rust-srpm-macros
```

**Recommended tools:**
- Use `rust2rpm` to generate initial spec

**Spec file sections:**

```spec
%prep
%autosetup -n %{crate}-%{version} -p1
%cargo_prep_online

%build
%{cargo_license_online} > LICENSE.dependencies
%cargo_build --locked  # Only if needed, else remove

%install
%cargo_install
```

**Or for binaries:**
```spec
%prep
%autosetup -n %{crate}-%{version}
%cargo_prep_online

%build
%{cargo_license_online} > LICENSE.dependencies
%cargo_build --locked

%install
%crate_install_bin
```

**Key points:**
- Use `%cargo_prep_online` NOT `%cargo_prep`
- Remove `%generate_buildrequires` section
- Use `%cargo_license_online` and `%cargo_license_summary_online`
- Don't use both `%cargo_build` and `%cargo_install` (cargo bug)
- For nightly Rust: add `%rustup_nightly` in `%prep`

## Go

**Build dependencies:**
```
BuildRequires: go-rpm-macros
BuildRequires: go-srpm-macros
BuildRequires: anda-srpm-macros  # if using %goprep_online
```

**Recommended tools:**
- Use `go2rpm` to generate initial spec

**Spec file sections:**

```spec
%prep
%goprep_online

%build
%gobuild -o %{buildroot}%{_bindir}/binary-name ./cmd/app

%install
%goinstall
```

**Or with GO111MODULE:**
```spec
%global gomodulesmode GO111MODULE=on

%prep
%autosetup -n %{name}-%{version}
%goprep

%build
%gobuild -o %{buildroot}%{_bindir}/binary-name ./cmd/app
```

**Key points:**
- Remove `%generate_buildrequires` section
- Rename go2rpm's auto-generated name to something sensible
- Put auto-generated name in `Provides:` if needed
- Use `%goprep_online` OR set `gomodulesmode GO111MODULE=on`

## Zig

**Build dependencies:**
```
BuildRequires: zig
BuildRequires: zig-rpm-macros
BuildRequires: zig-srpm-macros
BuildRequires: anda-srpm-macros  # for %zig_build_target
```

**Basic build:**
```spec
%build
%{zig_build} -Demit-docs
```

**Custom target (for ReleaseFast, microarchitectures):**
```spec
%build
%{zig_build_target -r fast -cx86_64_v2} -Demit-docs
```

**Key points:**
- Many Zig projects need ReleaseFast for optimization
- Some need x86_64_v2 instead of baseline (SIMD)
- If debug info is lost: `-Dstrip=false` or `%global debug_package %{nil}`
- For no deps or static linking only: use `-s` flag with `-fsys=pkgname`

## Nim

**Build dependencies:**
```
BuildRequires: nim
BuildRequires: anda-srpm-macros
```

**Using nimble:**
```spec
%prep
%autosetup
%nim_prep

%build
%nim_c src/dive

%install
install -Dm755 src/dive -t %{buildroot}%{_bindir}
```

**Using atlas:**
```spec
%prep
%autosetup -Sgit

%build
atlas init
atlas rep atlas.lock
%nim_c src/netto
```

**Key points:**
- Use `%nim_c` (same as `%nim_build`)
- Dependencies should be downloaded in `%prep`
- Atlas is for projects using nimble-like dependency management

## JavaScript / Node.js

**Build dependencies:**
```
BuildRequires: nodejs  # or specific version
BuildRequires: nodejs-npm
BuildRequires: nodejs-packaging
```

**Spec file:**
```spec
%global npm_name pkgname  # Canonical name from npm registry

%prep
%autosetup -n %{name}-%{version}
%npm_prep -n %{npm_name}

%build
# Node.js packages typically don't need build step

%install
%npm_install

%files
%{nodejs_sitelib}/lib/node_modules/%{npm_name}/bin/*  # executables
%{nodejs_sitelib}/lib/node_modules/%{npm_name}/lib/*  # library files
```

**Key points:**
- MUST set `%global npm_name pkgname` OR use `%npm_prep -n pkgname`
- Use `%npm_license` for bundled dependency licenses
- Bundle dependencies (Terra allows this unlike Fedora!)
- If using alternate Node.js version, may need to patch shebangs

## Electron

**Build dependencies:**
```
BuildRequires: desktop-file-utils
```

**Spec file:**
```spec
Name: electron-app
Version: 1.2.3

%electronmeta  # REQUIRED - after Name, before first %description

Source0: https://github.com/owner/repo/archive/v%{version}.tar.gz

%description
An Electron application.

%prep
%autosetup -n %{name}-%{version}

%build
# Electron apps typically build during install or prep

%install
%electron_install

%files
# Electron apps install to /usr/lib/%{name}
```

**Key points:**
- `%electronmeta` MUST be after `Name:` and before first `%description`
- Exclude private bundled libraries:
```spec
%global __requires_excludes %{__requires_excludes}|private_library\\.so
%global __provides_excludes %{__provides_excludes}|private_library\\.so
```
- Use `%{electron_license}` for bundled license
- Validate desktop file if providing one

## Tauri

**Build dependencies:**
```
BuildRequires: %{tauri_buildrequires}
```

**Spec file:**
```spec
%generate_buildrequires
%tauri_generate_buildrequires

%prep
%tauri_prep

%build
# Use webapp macros OR %tauri_build
# %tauri_build -f feature1,feature2

%install
# Tauri typically installs during build
```

**Key points:**
- Use `%tauri_prep` in `%prep`
- Most Rust macros have Tauri equivalents
- Tauri macros only support `-f` for features
- Use `%{tauri_cargo_license}` for deps
- See `references/guidelines.md` for Tauri macros

## C / C++

**Standard approach:**
```spec
%build
%configure
%make_build

%install
%make_install
```

**With mold linker (encouraged):**
```spec
CFLAGS="%{optflags} -fuse-ld=mold"
CXXFLAGS="%{optflags} -fuse-ld=mold"
```

**Key points:**
- Dependencies required for runtime MUST be separate packages
- Build-time deps can be bundled (Terra's mock has networking)
- Use mold linker for faster builds (enabled by default in anda-srpm-macros)

## Python

**Follow Fedora guidelines:**
- All dependencies must be packaged individually
- Python packages are considered runtime dependencies
- Use Python 3 as `python3`

## Ruby

**Follow Fedora guidelines:**
- Use `rubygem-foo` pattern for gems
- Dependencies must be packaged separately

## Vala

**Follow Fedora guidelines:**
- Use standard build system (meson, cmake, etc.)
- Runtime dependencies must be packaged

## General Notes

1. **Check existing packages** for similar software in the same category
2. **Terra's mock has networking** - can download deps during build
3. **Reproducibility requirements** are relaxed - vendoring is okay
4. **Use Terra macros** whenever possible
5. **Test builds locally** before submitting PR
6. **Refer to Fedora guidelines** for unlisted languages or scenarios