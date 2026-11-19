# LuaT Packages

Community packages for [LuaT](https://github.com/laot7490/luat), a typed Lua compiler for FiveM resources.

Packages help LuaT understand the modules and declarations used by a resource. The `example` package includes a shared runtime module and declarations for shared, client, and server code.

## Install a package

From your LuaT project folder, add a package by name:

```sh
luat add example
```

LuaT records the package under `[dependencies]` in `luat.toml` and installs it for your project. To restore packages later, run `luat install`. Remove one with `luat remove example`.

## Use the example package

In a shared, client, or server LuaT script, import the package and call its function:

```lua
local example = import('example')
example.print('Ada')
-- Hello, Ada!
```

The shared aliases `ExampleId` and `ExampleName` are available on both sides. Client and server scripts can also use their own declaration types:

```lua
-- Client script
local player: ExampleClientPlayer = { id = 1, displayName = 'Ada' }
```

```lua
-- Server script
local player: ExampleServerPlayer = { id = 1, connected = true }
```

## Available packages

- See [packages](packages) for all packages.

## Contribute

New packages and improvements are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the short guide to creating and submitting a package.
