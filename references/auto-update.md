# AndaX Auto-Update Script Reference

Complete reference for creating automatic update scripts using Rhai in Andaman.

## Overview

AndaX scripts (`.rhai` files) are used to automatically update package versions in Terra. Place the script as `update.rhai` next to your `anda.hcl` file.

**IMPORTANT:** All statements MUST end with semicolons (`;`)

## Basic Syntax

```rhai
let ver = gh("owner/repo");
rpm.version(ver);
```

## Version Fetching Functions

### GitHub Releases

```rhai
// Get latest release tag
let ver = gh("owner/repo");
rpm.version(ver);

// Get version with custom format
let ver = gh("owner/repo");
rpm.version("v" + ver);
```

### GitHub Commits

```rhai
// Get latest commit hash
let commit = gh_commit("owner/repo", "main");
rpm.version(commit);

// Get commit date
let commit = gh_commit("owner/repo", "main");
let date = gh_commit_date("owner/repo", commit);
rpm.version(date);
```

### GitLab

```rhai
// Get latest release from GitLab
let ver = gl("owner/project");
rpm.version(ver);
```

### PyPI

```rhai
// Get latest version from Python Package Index
let ver = pypi("package-name");
rpm.version(ver);
```

### Crates.io

```rhai
// Get latest version from Rust crates registry
let ver = crate("crate-name");
rpm.version(ver);
```

## Update Functions

### rpm.version()

Updates the `Version:` field in the spec file:

```rhai
let ver = gh("owner/repo");
rpm.version(ver);

// Or with custom version
rpm.version("v" + ver);
```

### rpm.release()

Updates the `Release:` field (rarely needed):

```rhai
rpm.release("2%{?dist}");
```

## Labels and Filters

### Check Labels

```rhai
// Check if nightly label is present
if filters.contains("nightly") {
  // nightly-specific update logic
}

// Check for weekly label (0-6)
if filters.contains("weekly") {
  // weekly update logic
}
```

### Access Labels

```rhai
// Get branch name for per-branch updates
let branch = labels.branch;

if branch == "f41" {
  let ver = gh("owner/repo", "v1");
  rpm.version(ver);
} else if branch == "f42" {
  let ver = gh("owner/repo", "v2");
  rpm.version(ver);
}
```

## Common Patterns

### Pattern 1: Simple GitHub Release

```rhai
let ver = gh("owner/repo");
rpm.version(ver);
```

### Pattern 2: Version with Prefix

```rhai
let ver = gh("owner/repo");
rpm.version("v" + ver);
```

### Pattern 3: Nightly from Git Commit

```rhai
let commit = gh_commit("owner/repo", "main");
let date = gh_commit_date("owner/repo", commit);
rpm.version("0~" + date + "git." + commit);
```

### Pattern 4: Conditional Based on Labels

```rhai
if filters.contains("nightly") {
  let commit = gh_commit("owner/repo", "main");
  let date = gh_commit_date("owner/repo", commit);
  rpm.version("2.0.0~" + date + "git." + commit);
} else {
  let ver = gh("owner/repo");
  rpm.version(ver);
}
```

### Pattern 5: Per-Branch Updates

```rhai
if labels.branch == "f41" {
  let ver = gh("owner/repo", "v1");
  rpm.version(ver);
} else if labels.branch == "f42" {
  let ver = gh("owner/repo", "v2");
  rpm.version(ver);
} else {
  let ver = gh("owner/repo");
  rpm.version(ver);
}
```

### Pattern 6: Version Transformation

```rhai
let ver = gh("owner/repo");
// Extract major.minor from "v1.2.3"
let parts = ver.split(".");
let transformed = parts[0] + "." + parts[1] + ".0";
rpm.version(transformed);
```

### Pattern 7: Multiple Sources

```rhai
// Try crates.io first, fall back to GitHub
let ver = crate("crate-name");
if ver == "" {
  ver = gh("owner/repo");
}
rpm.version(ver);
```

## Update Frequencies

### Standard Packages

- Runs every 10 minutes
- Command: `anda update -vv --excludes nightly=1 --excludes updbranch=1`
- No special labels needed

### Nightly Packages

- Runs every 24 hours
- In anda.hcl:
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

### Weekly Packages

- Runs every 7 days (random day)
- In anda.hcl:
```hcl
project pkg {
  rpm {
    spec = "pkgname.spec"
  }
  labels {
    weekly = 0  # Random 0-6
  }
}
```

### Per-Branch Packages

- Runs every 30 minutes
- In anda.hcl:
```hcl
project pkg {
  rpm {
    spec = "pkgname.spec"
  }
  labels {
    updbranch = 1
  }
}
```

**IMPORTANT:** Don't use per-branch updates if the script bumps versions across all branches simultaneously. Only use when versions differ per branch.

## Best Practices

1. **Avoid GitHub API when possible** - Rate limits apply
   - Prefer: GitLab, crates.io, PyPI
   - Fall back to GitHub if no alternatives

2. **Keep scripts simple** - One-liners are best:
   ```rhai
   rpm.version(gh("owner/repo"));
   ```

3. **Always use semicolons** - Statements MUST end with `;`

4. **Don't run unrelated code** - Only update version logic

5. **Test before deploying** - Run:
   ```bash
   anda update -vv --path anda/path/to/pkg
   ```

6. **Version format matters** - Match your versioning scheme:
   - Stable: Just the version number
   - Nightly: Version with commit date/hash

## Error Handling

AndaX functions fail gracefully:
- API rate limits: Skip update, try later
- Repository not found: Skip update
- Network errors: Skip update

No explicit error handling needed in most cases.

## Available Functions Summary

| Function | Purpose | Example |
|----------|---------|---------|
| `gh(owner/repo)` | GitHub release | `let ver = gh("owner/repo");` |
| `gh_commit(owner/repo, branch)` | GitHub commit | `let c = gh_commit("owner/repo", "main");` |
| `gh_commit_date(owner/repo, commit)` | Commit date | `let d = gh_commit_date("owner/repo", c);` |
| `gl(owner/project)` | GitLab release | `let ver = gl("owner/project");` |
| `pypi(package)` | PyPI version | `let ver = pypi("requests");` |
| `crate(name)` | Crates.io version | `let ver = crate("serde");` |
| `rpm.version(ver)` | Update Version field | `rpm.version(ver);` |
| `rpm.release(rel)` | Update Release field | `rpm.release("2%{?dist}");` |
| `filters.contains(label)` | Check filter | `if filters.contains("nightly") {...}` |
| `labels.branch` | Get branch name | `let b = labels.branch;` |

## Troubleshooting

**Version not updating:**
- Check that script has semicolons
- Verify API function syntax
- Check Anda logs for errors

**GitHub rate limit:**
- Switch to GitLab, PyPI, or crates.io
- Wait for rate limit reset

**Invalid version format:**
- Ensure version matches your versioning scheme
- Add prefix/suffix if needed (e.g., `v` prefix)

## Examples

See `assets/templates/update.rhai.template` for template with all examples.

See `assets/examples/` for complete package examples with working update scripts.