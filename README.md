# Terra Package Creator Skill for Clawdbot

A specialized skill for creating and maintaining packages in the [Terra package repository](https://terra.fyralabs.com) - a rolling-release Fedora-based distribution.

## What is Terra?

Terra is a package repository for Fedora and its derivatives that provides high-quality software built using the [Andaman](https://github.com/FyraLabs/anda) toolchain instead of traditional Koji.

## What This Skill Does

This skill provides comprehensive guidance for:

- Creating new packages for Terra
- Writing RPM spec files
- Creating AndaX (Rhai) auto-update scripts
- Packaging applications following Terra's policies and guidelines
- Setting up auto-updates for packages
- Language-specific packaging (Rust, Go, Zig, Nim, Node.js, Electron, Tauri)

## Quick Start

1. Fork the [terrapkg/packages](https://github.com/terrapkg/packages) repository
2. Create a folder in the appropriate category under `anda/`
3. Add `anda.hcl` and `.spec` files (see templates below)
4. Build with: `anda build -c terra-rawhide-x86_64 anda/path/to/pkg`
5. Submit PR to the `frawhide` branch

## Templates Included

- **anda.hcl** - Anda manifest for package configuration
- **spec.template** - Complete RPM spec file template
- **update.rhai.template** - Auto-update script with examples
- **desktop-entry.template** - Desktop file for GUI applications

## Documentation

- **policies.md** - Terra packaging policies (condensed)
- **guidelines.md** - Detailed packaging guidelines
- **language-guidelines.md** - Language-specific instructions
- **auto-update.md** - Complete AndaX scripting reference

## Example Package

A complete working example is provided in `assets/examples/simple-package/` showing a basic "hello" package.

## Installation

This skill is designed to be installed in Clawdbot's skills directory. To install:

```bash
# Copy the .skill file to your Clawdbot skills directory
cp terra-pkg-creator.skill /path/to/clawdbot/skills/
```

## Key Resources

- **Main Repo:** https://github.com/terrapkg/packages
- **Andaman Tool:** https://github.com/FyraLabs/anda
- **Devdocs:** https://developer.fyralabs.com/terra/
- **Discord:** https://fyralabs.com/discord

## License

This skill is part of the Clawdbot ecosystem.

## Author

Created by neuro-puppy 🐕 for Clawdbot
