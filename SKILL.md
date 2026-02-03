---
name: terra-pkg-creator
description: "Create and maintain packages for the Terra package repository (Fedora-based). Use when: creating new packages, writing RPM spec files, creating AndaX update scripts, packaging applications, or setting up auto-updates"
---

# Terra Package Creator

Create packages for the Terra package repository, a rolling-release Fedora-based distribution.

## Quick Start

1. Fork the [terrapkg/packages](https://github.com/terrapkg/packages) repository
2. Create a folder in the appropriate category under `anda/`
3. Add `anda.hcl` and `.spec` files (see templates below)
4. Build with: `anda build -c terra-rawhide-x86_64 anda/path/to/pkg`
5. Submit PR to the `frawhide` branch

## Package Structure

```
anda/
  <category>/
    <pkgname>/
      anda.hcl              # Anda manifest
      pkgname.spec           # RPM spec file
      pkgname.desktop        # Required for GUI apps
      update.rhai           # Auto-update script (recommended)
```

### Package Categories

Choose the correct category for your package (priority order):

1. **fonts/** - Font packages (MUST suffix with `-fonts`)
2. **system/** - Bootloaders, kernels, drivers
3. **tools/buildsys/** - Software used to build other software
4. **devs/** - Tools for software development
5. **games/** - Games
6. **themes/** - Themes
7. **docker/** - Container-related software
8. **desktops/** - DE-specific applications
9. **apps/** - GUI applications
10. **langs/** - Language-specific packages

## Essential Files

### 1. anda.hcl (Manifest)

Basic template:
```hcl
project pkg {
  rpm {
    spec = "pkgname.spec"
  }
}
```

Nightly packages:
```hcl
project pkg {
  rpm {
    spec = "pkgname.spec"
  }
  labels {
    nightly = 1
  }
}
```

With custom update script:
```hcl
project pkg {
  rpm {
    spec = "pkgname.spec"
    update = "custom-update.rhai"
  }
}
```

### 2. Spec File (.spec)

See `assets/templates/spec.template` for a complete template.

**Critical Requirements:**
- `Packager:` field is REQUIRED with your name and email
- `Release:` MUST be `1%?dist` or `1%{?dist}` (only one number)
- Add `%changelog` entry for new packages (e.g., "Initial package")
- No period at end of `Summary:`, but add period at end of `%description`

### 3. Auto-Update Script (update.rhai)

See `assets/templates/update.rhai.template` for examples.

**Basic pattern:**
```rhai
let ver = gh("owner/repo");  // Get latest version from GitHub
rpm.version(ver);            // Update version in spec file
```

IMPORTANT: You MUST use semicolons (;) in Rhai scripts!

**Update frequencies:**
- Standard: Every 10 minutes via `anda update`
- Nightly: Every 24 hours (add `nightly = 1` label)
- Weekly: Every 7 days (add `weekly = <0-6>` label)
- Per-branch: Every 30 minutes (add `updbranch = 1` label)

### 4. Desktop File (.desktop) - For GUI Apps

See `assets/templates/desktop-entry.template` for template.

**Required fields:**
- Name, Exec, Icon, Type=Application
- Icon should be filename without extension

## Language-Specific Guidelines

See `references/language-guidelines.md` for complete details.

### Rust
- Use `rust2rpm` to generate spec
- Replace `%cargo_prep` with `%cargo_prep_online`
- Remove `%generate_buildrequires`
- Use `%cargo_license_online` and `%cargo_license_summary_online`

**Example:**
```spec
%prep
%autosetup -n %{crate}-%{version} -p1
%cargo_prep_online

%build
%{cargo_license_online} > LICENSE.dependencies

%install
%cargo_install
```

### Go
- Use `go2rpm` (rename to sensible package name)
- Remove `%generate_buildrequires`
- Use `%goprep_online` instead of `%goprep` OR set `%global gomodulesmode GO111MODULE=on`
- Add `BuildRequires: anda-srpm-macros`

### Zig
- BuildRequires: zig, zig-rpm-macros, zig-srpm-macros
- Prefer `%zig_build` (uses Fedora defaults)
- For custom flags: use `%zig_build_target` (requires `anda-srpm-macros`)
- Example: `%zig_build_target -r fast -cx86_64_v2`

### Nim
- BuildRequires: nim, anda-srpm-macros
- Use `%nim_prep` and `%nim_c`
- Example: `%nim_c src/binary-name`

### Node.js
- BuildRequires: nodejs, nodejs-npm, nodejs-packaging
- MUST set `%global npm_name pkgname` or use `%npm_prep -n pkgname`
- Use `%npm_license` for bundled dependencies
- Bundle dependencies (Terra allows this unlike Fedora)

### Electron Apps
- Add `%electronmeta` macro (MUST be after `Name:` and before first `%description`)
- Use `%electron_install` for installation
- Exclude private libraries from requirements/provides

### Tauri Apps
- BuildRequires: `%{tauri_buildrequires}`
- Use `%tauri_prep` in `%prep`
- Use webapp build macros or `%tauri_build`
- Use `%{tauri_cargo_license}` for dependency licenses

## Building Packages

### Setup

**Fedora/Ultramarine:**
```bash
sudo dnf install terra-mock-configs via Terra
```

**Dev Container (Cross-platform):**
- Fork packages repo and clone
- Open in VS Code
- Reopen in Dev Container

### Build Command

```bash
anda build -c terra-rawhide-x86_64 anda/path/to/pkg
```

- Change architecture as needed (x86_64, i386, aarch64)
- For rpmbuild mode: add `--rpm-builder=rpmbuild`
- Install build deps first: `sudo dnf builddep path/to/pkgname.spec`

### Troubleshooting

- Built RPMs are in `anda-build/`
- Mock will show unpackaged files as errors - fix in `%files` section
- Useful error message is before Python traceback

## Policies and Guidelines

See `references/` for complete documentation:

- **policies.md** - Submission, versioning, naming, quality standards
- **guidelines.md** - Detailed packaging guidelines and macros
- **auto-update.md** - AndaX scripting reference

**Key Policies:**
- Only submit legally distributable software
- Try not to duplicate Fedora or Flathub packages
- GUI apps MUST include AppStream metadata and .desktop file
- Follow upstream versioning for stable releases
- Use `%{unreleased_version}~%{commit_date}git.%{shortcommit}` for unreleased

**Tagging System:**
Packages can have tags like `stable`, `preview`, `nightly`, `tip`
- Format: `%{rawname}.%{tag}` (e.g., `zed.preview`, `ghostty.tip`)
- Nightly packages require `labels { nightly = 1 }` in anda.hcl
- May add `Provides: %{rawname}-%{tag}` for UX

## Versioning Formats

**Stable (release tag tracking):**
```
Version: %{latest_stable_version}
```

**Nightly off stable (commit tracking):**
```
Version: %{latest_stable_version}^%{commit_date}git.%{shortcommit}
```

**No stable version (commit tracking):**
```
Version: %{unreleased_version}~%{commit_date}git.%{shortcommit}
```

Replace `git` with correct VCS identifier: svn, cvs, bzr, hg, p4, pjl, tfs, drc, fsl

For commit tracking, you MUST add `labels { nightly = 1 }` in anda.hcl unless there's no update.rhai.

## Naming Conventions

**Suffixes (in order):**
1. Fonts MUST use `-fonts` suffix
2. Shared libraries SHOULD use `-libs` suffix
3. Development libraries MUST use `-devel` suffix
4. Shell completions: `-bash-completion`, `-zsh-completion`, etc.
5. Documentation: `-doc`
6. Tags: `.nightly`, `.preview`, `.tip`, etc.

## Common Macros

**File locations:**
- `%{_bindir}` → `/usr/bin`
- `%{_libdir}` → `/usr/lib64`
- `%{_includedir}` → `/usr/include`
- `%{_datadir}` → `/usr/share`
- `%{_appsdir}` → Application desktop files (preferred)

**Shell completions:**
- Use `%pkg_completion` macro
- See `references/macros.md` for details

**Library subpackages:**
- `%pkg_libs_files` - shared library files
- `%pkg_devel_files` - development files
- `%pkg_static_files` - static library files

**Desktop files:**
- `%desktop_file_install` - install desktop file
- `%desktop_file_validate` - validate desktop file

## Testing Your Package

1. **Build locally:**
   ```bash
   anda build -c terra-rawhide-x86_64 anda/path/to/pkg
   ```

2. **Validate desktop file (if GUI app):**
   ```bash
   %check
   %desktop_file_validate %{buildroot}%{_appsdir}/pkgname.desktop
   ```

3. **Check for unpackaged files:**
   - Mock will report errors for files installed but not listed in `%files`

4. **Review against policies and guidelines:**
   - Check `references/policies.md`
   - Check `references/guidelines.md`

## Submitting to Terra

1. Commit your changes (commits MUST be signed)
2. Push to your fork
3. Create PR merging to `frawhide` branch
4. The CI will build and test your package

## Templates and Examples

See `assets/templates/` for:
- `anda.hcl.template` - Anda manifest template
- `spec.template` - RPM spec file template
- `update.rhai.template` - Auto-update script template
- `desktop-entry.template` - Desktop file template

See `assets/examples/` for:
- `simple-package/` - Complete simple package example

## Advanced Topics

### Subrepos

For packages that may introduce breaking changes, use `subrepo` label in anda.hcl:
```hcl
project pkg {
  rpm {
    spec = "pkgname.spec"
  }
  labels {
    subrepo = "extras"  // or "nvidia", "mesa", "multimedia"
  }
}
```

Valid subrepos: extras, nvidia, mesa, multimedia (43+)

### Custom AndaX Functions

See `references/auto-update.md` for:
- Available functions beyond `gh()`
- GitLab, crates.io, PyPI support
- Advanced update patterns

### Patches

Prefer applying patches in `%autosetup` with `-p#` flag:
```spec
%autosetup -p1
```

If not possible, use `%autopatch`.

## When to Use This Skill

Use this skill when you need to:
- Create a new package for Terra
- Write or modify RPM spec files
- Create auto-update scripts for packages
- Package applications following Terra's standards
- Understand Terra's packaging policies and guidelines
- Set up packages for specific languages (Rust, Go, Zig, Nim, etc.)
- Create desktop files and AppStream metadata
- Troubleshoot package builds

## References

For detailed information, see:
- `references/policies.md` - Terra packaging policies
- `references/guidelines.md` - Complete packaging guidelines
- `references/language-guidelines.md` - Language-specific instructions
- `references/auto-update.md` - AndaX scripting reference
- `assets/templates/` - File templates
- `assets/examples/` - Working examples
