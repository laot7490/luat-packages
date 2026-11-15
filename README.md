# LuaT Packages

Community packages for [LuaT](https://github.com/laot7490/luat), a typed Lua compiler for FiveM resources.

Packages help LuaT understand the modules and declarations used by a resource. This registry currently includes the `example` package, which demonstrates shared, client, and server declarations.

## Install a package

From your LuaT project folder, add a package by name:

```sh
luat add example
```

LuaT records the package in `luat.toml` and installs it for your project. To restore packages later, run `luat install`. Remove one with `luat remove example`.

## Available packages

- See [PACKAGES.md](PACKAGES.md) for all available packages.

## Contribute

New packages and improvements are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the short guide to creating and submitting a package.
