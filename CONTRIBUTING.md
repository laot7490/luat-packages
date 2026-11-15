# Contributing packages

Packages contain LuaT modules, Lua modules, and optional `.d.luat` declarations in one versioned directory. Submit a pull request to this repository; dependencies must already be published.

## Create and check

```powershell
luat package init my-package
```

Fill in `author` in `luat-package.toml`, then list module paths under `shared`, `client`, or `server`, declaration paths under `declarations`, and published dependency ranges under `[dependencies]`. `import('my-package')` selects `init.luat` or `init.lua`; submodules can be imported by path. Every runtime module must end with a value-returning top-level `return`.

```powershell
luat package check
```

Edit `version` in `luat-package.toml` before changing published contents. Run `luat install` before checking packages with dependencies.

## Submit

Copy the current package directory to `packages/<name>/` and open a pull request. CI validates manifests, declarations, dependency versions, paths, hashes and import rules without executing package code. After review and merge, the registry publishes the new version automatically. Published versions cannot be changed; corrections require a higher version.
