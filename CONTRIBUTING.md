# Contributing packages

Thanks for contributing to the LuaT package registry. A package can include LuaT or Lua modules and optional `.d.luat` declarations. Package metadata lives in `luat-package.toml`.

## Create and check a package

From the repository root, create a package under `packages/`:

```sh
luat package init my-package --project packages
```

Edit `packages/my-package/luat-package.toml`:

- Fill in `author` and a short `description`.
- List runtime files under `shared`, `client`, or `server`.
- List declaration files under `declarations`.
- Add published package dependencies under `[dependencies]` when needed.

The starter package includes `init.luat`. Runtime modules should return a value so other modules can import them. Declarations can describe shared, client, or server APIs; see [`packages/example`](packages/example) for an example.

If the package has dependencies, install them first. Then check the package:

```sh
luat install --project packages/my-package
luat package check --project packages/my-package
```

`package check` checks the package and does not publish it.

## Submit a package

Open a pull request with the new or updated package in `packages/<name>/`. Published versions are immutable, so increase `version` in `luat-package.toml` whenever you change an already published package.

The registry checks package files and dependencies before publishing. Once a change is merged, the registry workflow publishes the package metadata automatically.
