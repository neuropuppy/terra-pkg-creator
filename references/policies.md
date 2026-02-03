# Terra Packaging Policies

This is a condensed reference of Terra packaging policies. For full details, see https://developer.fyralabs.com/terra/policies

## Quick Summary

**Package Submission:**
- Only submit legally distributable software
- Try not to duplicate Fedora or Flathub packages
- Avoid work-in-progress code or untested patches
- Submit to appropriate category under `anda/`

**Versioning:**
- Stable: `%{latest_stable_version}`
- Nightly off stable: `%{latest_stable_version}^%{commit_date}git.%{shortcommit}`
- No stable version: `%{unreleased_version}~%{commit_date}git.%{shortcommit}`
- Replace `git` with correct VCS: svn, cvs, bzr, hg, p4, pjl, tfs, drc, fsl

**Tags:**
- Format: `%{rawname}.%{tag}` (e.g., `zed.preview`, `ghostty.tip`)
- Common tags: stable, preview, nightly, tip
- Nightly packages require `labels { nightly = 1 }` in anda.hcl

**Release Field:**
- MUST be `1%?dist` or `1%{?dist}` (only one number)
- Increment when making user-facing changes
- No upstream version info in Release field

**Packager Field:**
- REQUIRED: `Packager: Your Name <email@example.com>`
- Must be included in all packages

**Naming Conventions:**
- Fonts: `-fonts` suffix (MUST)
- Shared libraries: `-libs` suffix (SHOULD)
- Dev libraries: `-devel` suffix (MUST)
- Completions: `-bash-completion`, etc. (SHOULD)
- Documentation: `-doc` suffix (SHOULD)
- Tags: `.nightly`, `.preview`, etc. (when needed)

**GUI Applications:**
- MUST provide .desktop file
- MUST provide AppStream metadata
- See desktop file template in `assets/templates/desktop-entry.template`

**Subrepos:**
For packages affecting existing installs, use `subrepo` label:
```hcl
labels {
  subrepo = "extras"  // or "nvidia", "mesa", "multimedia"
}
```

**Maintenance:**
- Packages must be maintained
- Unmaintained packages may be removed
- Anyone can make PR to existing packages
- Terra supports latest Fedora versions only

**Quality Standards:**
- Low-quality contributions will be declined
- Follow Fedora packaging guidelines as fallback
- Team may reject packages at their discretion

**GUI Apps Flatpak Exception:**
Generally don't submit apps that work as Flatpaks, UNLESS:
- Terminal emulators
- CLI/TUI applications
- Modded/multi-instance game launchers
- Apps requiring manual data file modification
- Apps with performance issues due to sandboxing (IDEs, DAWs)
- System components
- Libraries required for above

## Category Priority

Choose category in this order:
1. fonts/
2. system/ (bootloaders, kernels, drivers)
3. tools/buildsys/ (build tools)
4. devs/ (development tools)
5. games/
6. themes/
7. docker/ (container-related)
8. desktops/ (DE-specific)
9. apps/ (GUI apps)
10. langs/ (language-specific)

## Security & Conduct

- Security: See SECURITY.md in packages repo
- Code of conduct: See CODE_OF_CONDUCT.md in packages repo
- Lifecycle: See https://developer.fyralabs.com/terra/lifecycle

## When in Doubt

- Refer to Fedora packaging guidelines
- Check existing packages for examples
- Ask in Discord server: https://fyralabs.com/discord
