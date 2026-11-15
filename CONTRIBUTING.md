# Contributing packages

Thank you for helping expand the LuaT type package registry. Contributions are submitted as pull requests to this repository.

## Create a package

Install a LuaT version that includes the package authoring commands, then run this command from the directory where you want to create the package:

```powershell
luat package init
```

Choose **Type** in the interactive prompt, then enter a package name, description, and license. The license defaults to MIT. For example, entering `my_resource` creates a `my_resource/` folder with `package.toml` and a `1.0.0/` directory containing shared, client, and server declaration templates.

Edit the declaration files to describe the library or resource. For example:

```lua
---@shared

typedef ResourceId = number
```

```lua
---@client

declare MyResource: { notify: (message: string) -> () }
```

```lua
---@server

declare MyResourceServer: { getName: (id: ResourceId) -> string }
```

## Check and build

Enter the package folder and run:

```powershell
luat package check
luat package build
```

`check` validates the package without changing its files. `build` checks it and records the declaration file names and hashes in `package.toml`. Resolve any errors and run the commands again before submitting.

## Submit a package

Copy the complete package folder into `types/<name>/` in your fork. Keep the package name in `package.toml` aligned with the folder name, and include the version directory. Review the changes, then open a pull request targeting `main`.

GitHub Actions checks the package metadata, files, hashes, and declarations. The registry also prevents changes to already published versions. Add corrections in a new version instead of editing a published release.

## Publish another version

From the package folder, create a version and prepare it:

```powershell
luat package version 1.1.0
luat package check
luat package build
```

Use a new valid Semantic Version. The new version starts with the latest existing declaration files; update them as needed before checking and building.
