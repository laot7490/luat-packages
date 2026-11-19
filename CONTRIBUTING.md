# Contributing packages

Thanks for contributing to the LuaT package registry. A package can include LuaT or Lua modules and optional `.d.luat` declarations. Package metadata lives in `luat-package.toml`.

## Create and check a package

From the repository root, create a package under `packages/`:

```sh
luat package init --project packages
```

The command asks for the package name, author, description, version, and license, then creates `packages/<name>/` with a manifest and starter `init.luat`. Version defaults to `1.0.0`; license defaults to `MIT`.

Edit the manifest to:

- List runtime files and `.d.luat` files under `shared`, `client`, or `server`.
- Add published package dependencies under `[dependencies]` when needed.

Runtime modules should return a value so other modules can import them. The manifest lists determine declaration visibility. Shared declarations are available on both sides. Client and server declarations are available on their own side. See the [example package manifest](packages/example/luat-package.toml) for the three lists in use.

If the package has dependencies, install them first. Then check the package:

```sh
luat install --project packages/<name>
luat package check --project packages/<name>
```

`package check` checks the package and does not publish it.

## Submit a package

Open a pull request with the new or updated package in `packages/<name>/`. Published versions are immutable, so increase `version` in `luat-package.toml` whenever you change an already published package.

The registry checks package files and dependencies before publishing. Once a change is merged, the registry workflow publishes the package metadata automatically.
