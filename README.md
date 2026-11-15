# LuaT Packages

Community packages for [LuaT](https://github.com/laot7490/luat), a typed Lua compiler for FiveM resources.

Packages provide declarations/modules that help LuaT understand the libraries and resources used in a project. The registry currently accepts packages in the `@types` scope.

## Install a package

From a LuaT project directory, run:

```powershell
luat add @types/example
```

LuaT selects the latest stable version and records it in `luat.toml`. To install a specific version, include it in the package name:

```powershell
luat add @types/example@1.0.0
```

Use `luat install` to restore the versions recorded in `luat.toml`. Use `luat remove @types/example` to remove a package.

Installed declarations are stored under `.luat/` beside `luat.toml` and loaded by LuaT automatically.

## Packages in this registry

- [`@types/example`](types/example) — example declarations for shared, client, and server contexts.

## Contributing

Package contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on creating, checking, and submitting a package.
