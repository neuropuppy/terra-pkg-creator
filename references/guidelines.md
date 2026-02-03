# Terra Packaging Guidelines

Condensed reference for Terra-specific packaging guidelines. See https://developer.fyralabs.com/terra/guidelines for full details.

## Macro Syntax

**Flags requiring arguments:**
- `<...>` - MUST have space and argument: `%autosetup -n name`
- `[...]` - MAY have argument: `%ifarch x86_64`

**Number flags:**
- `<#>` or `[#]` - Take only numbers as arguments
- No space between flag and argument when no space is present

## Critical Rules

1. **Summary:** NO period at end
2. **Description:** Period at end
3. **Changelog:** Use for large changes only, NOT `%autochangelog`
4. **Patches:** Prefer `-p#` with `%autosetup` over `%autopatch`
5. **Arch-specific:** Use `%elifarch` instead of `%endif + %ifarch`

## File Installation

**Shell completions:**
- Create as subpackage
- Use `%pkg_completion` macro

**Shared libraries (-libs):**
```
%_libdir/*.so.*
%doc ... (if needed)
%license ... (if needed)
```

**Development libraries (-devel):**
```
%doc ... (if needed)
%license ... (if needed)
%_includedir/*
%_libdir/*.so
%_libdir/*.a
%_libdir/pkgconfig/%{name}.pc
%_libdir/*.vapi
%_libdir/*.gir
%_libdir/*.typelib
```

**Desktop files:**
- Install to `%{_appsdir}` instead of `%{_datadir}/applications/`
- Use `%desktop_file_install` and `%desktop_file_validate`
- Validate in `%check` section

**Documentation:**
- Use `%doc` for README, AUTHORS, etc.
- Use `%license` for license files

## Common Macros

**Build macros:**
- `%configure` - Autoconf configure script
- `%make_build` or `%make` - Make with build target
- `%make_install` - Make install
- `%cmake` - CMake configuration
- `%cmake_build` - CMake build
- `%meson` - Meson setup
- `%meson_compile` - Meson build

**Rust macros:**
- `%cargo_prep_online` - Replace `%cargo_prep`
- `%cargo_build` - Build with cargo
- `%cargo_install` - Install with cargo
- `%crate_install_bin` - Install binary from cargo install
- `%cargo_license_online` - Generate license file
- `%rustup_nightly` - Enable Rust nightly

**Go macros:**
- `%goprep` - Prepare Go sources
- `%goprep_online` - Online Go prep (recommended)
- `%gobuild` - Build Go binary
- `%goinstall` - Install Go binary

**Zig macros:**
- `%zig_build` - Build with Zig (uses Fedora defaults)
- `%zig_build_target` - Custom Zig build target

**Nim macros:**
- `%nim_prep` - Prepare Nim sources
- `%nim_c` - Build with Nim
- `%nimble` - Use nimble for deps

**Node.js macros:**
- `%npm_prep -n pkgname` - Prepare npm package
- `%npm_license` - Generate license file for bundled deps

**Electron macros:**
- `%electronmeta` - Metadata for Electron (required!)
- `%electron_install` - Install Electron app
- `%{electron_license}` - License for bundled deps

**Tauri macros:**
- `%tauri_prep` - Prepare Tauri sources
- `%tauri_build` - Build Tauri app
- `%{tauri_cargo_license}` - License for Rust deps
- `%tauri_cargo_license_summary` - License summary
- `%tauri_cargo_vendor_manifest` - Vendor manifest

**File macros:**
- `%pkg_completion` - Shell completions
- `%pkg_libs_files` - Shared library files
- `%pkg_devel_files` - Development files
- `%pkg_static_files` - Static library files
- `%desktop_file_install` - Install desktop file
- `%desktop_file_validate` - Validate desktop file

**Path macros:**
- `%{_bindir}` - /usr/bin
- `%{_libdir}` - /usr/lib64
- `%{_includedir}` - /usr/include
- `%{_datadir}` - /usr/share
- `%{_appsdir}` - /usr/share/applications (preferred for desktop files)
- `%{_mandir}` - /usr/share/man
- `%{_docdir}` - /usr/share/doc
- `%{_licensedir}` - /usr/share/licenses

## Web Applications

**Electron Apps:**
1. Add `%electronmeta` (after `Name:`, before first `%description`)
2. Use `%electron_install` in `%install`
3. Exclude private libraries:
```spec
%global __requires_excludes %{__requires_excludes}|private_library\\.so
%global __provides_excludes %{__provides_excludes}|private_library\\.so
```

**Tauri Apps:**
1. Use `%{tauri_buildrequires}` with `%generate_buildrequires`
2. Use `%tauri_prep` in `%prep`
3. Use webapp macros or `%tauri_build`
4. Use `%{tauri_cargo_license}` for deps

## JavaScript/Node.js

- Bundle dependencies (Terra allows this unlike Fedora)
- Set `%global npm_name pkgname` OR use `%npm_prep -n pkgname`
- BuildRequires: nodejs, nodejs-npm, nodejs-packaging

## Security

**Build and Runtime Dependencies:**
- Runtime deps MUST be packaged separately
- Build deps can be bundled for statically compiled languages

**Macros for dependency handling:**
- `%{__requires_excludes}` - Exclude specific requires
- `%{__provides_excludes}` - Exclude specific provides

## Fixing Packages

**When to bump Release:**
- User-facing changes (file installs, deps, URL, License, Summary)
- Changes that affect the final package

**When NOT to bump:**
- Fixing build failures
- Changes that don't affect final package

**Changelog for fixes:**
- Add `%changelog` entry for large changes
- Small fixes (one-liners, build deps) MAY omit changelog

## Validating Desktop Files

```spec
BuildRequires: desktop-file-utils

%check
%desktop_file_validate %{buildroot}%{_appsdir}/pkgname.desktop

%files
%{_appsdir}/pkgname.desktop
```

## Best Practices

1. Check existing packages for similar patterns
2. Use Terra macros instead of raw commands
3. Keep specs simple and readable
4. Test builds locally before PR
5. Follow Fedora guidelines for unlisted languages
6. Use `rpm --eval %{MACRO}` to expand macros

## Example Spec File

See `assets/templates/spec.template` for complete template.
See `assets/examples/simple-package/` for working example.