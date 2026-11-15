import argparse
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tomllib

MANIFEST = 'luat-package.toml'
SKIP = {'.git', '.luat', 'target', 'node_modules', 'dist', 'build'}

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])

def sources(root, folder=None, rules=()):
    folder = folder or root
    rules = list(rules)
    ignore = folder / '.gitignore'
    if ignore.is_file():
        for line in ignore.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith('#'):
                rules.append((folder, line))
    for item in sorted(folder.iterdir()):
        if item.name in SKIP:
            continue
        ignored = False
        for base, rule in rules:
            relative = item.relative_to(base).as_posix()
            negative = rule.startswith('!')
            pattern = rule.lstrip('!').strip('/')
            if fnmatch.fnmatchcase(relative, pattern) or ('/' not in pattern and fnmatch.fnmatchcase(item.name, pattern)):
                ignored = not negative
        if ignored:
            continue
        if item.is_symlink():
            raise ValueError(f'symlink rejected: {item}')
        if item.is_dir():
            yield from sources(root, item, rules)
        elif item.suffix in {'.lua', '.luat'}:
            yield item

def hashes(root):
    files = [root / MANIFEST, *sources(root)]
    if len(files) > 256:
        raise ValueError('package exceeds 256 files')
    result = {}
    total = 0
    names = set()
    for file in files:
        if file.is_symlink() or not file.is_file():
            raise ValueError(f'expected regular file: {file}')
        name = file.relative_to(root).as_posix()
        if name.lower() in names or any(part in {'.', '..'} for part in name.split('/')):
            raise ValueError(f'unsafe or colliding path: {name}')
        names.add(name.lower())
        data = file.read_bytes()
        data.decode('utf-8')
        total += len(data)
        if len(data) > 4 * 1024 * 1024 or total > 32 * 1024 * 1024:
            raise ValueError(f'package size limit exceeded: {file}')
        result[name] = hashlib.sha256(data).hexdigest()
    return result

def indexes(root, base=None):
    if base:
        paths = git(root, 'ls-tree', '-r', '--name-only', base, '--', 'index').decode().splitlines()
        return {Path(p).stem: tomllib.loads(git(root, 'show', f'{base}:{p}').decode()) for p in paths}
    return {p.stem: tomllib.loads(p.read_text()) for p in (root / 'index').glob('*.toml')}

def serialize(index):
    quote = json.dumps
    lines = ['schema = 2', f'name = {quote(index["name"])}']
    for version, release in sorted(index['versions'].items()):
        key = f'versions.{quote(version)}'
        lines += ['', f'[{key}]', f'commit = {quote(release["commit"])}', f'[{key}.dependencies]']
        lines += [f'{quote(k)} = {quote(v)}' for k, v in sorted(release['dependencies'].items())]
        lines += [f'[{key}.files]']
        lines += [f'{quote(k)} = {quote(v)}' for k, v in sorted(release['files'].items())]
    return '\n'.join(lines) + '\n'

def run(root, cli, publish=False, base=None):
    current = indexes(root)
    previous = indexes(root, base) if base else current
    if base and current != previous:
        raise ValueError('index/ is generated; source contributions must not edit it')
    packages = sorted((root / 'packages').iterdir())
    if not packages:
        raise ValueError('packages/ contains no packages')
    commit = git(root, 'rev-parse', 'HEAD^{commit}').decode().strip()
    pending = {}
    for package in packages:
        if package.is_symlink() or not package.is_dir():
            raise ValueError(f'expected package directory: {package}')
        manifest = tomllib.loads((package / MANIFEST).read_text())
        name, version = manifest['name'], manifest['version']
        if name != package.name:
            raise ValueError('package name must match its directory')
        dependencies = manifest.get('dependencies', {})
        if dependencies:
            subprocess.run([cli, 'install', '--project', str(package), '--pretty', 'false'], check=True)
        subprocess.run([cli, 'package', 'check', '--project', str(package), '--pretty', 'false'], check=True)
        files = hashes(package)
        index = current.get(name, {'schema': 2, 'name': name, 'versions': {}})
        if index['schema'] != 2 or index['name'] != name:
            raise ValueError(f'invalid catalog: {name}')
        old = index['versions'].get(version)
        if old and (old['files'] != files or old.get('dependencies', {}) != dependencies):
            raise ValueError(f'{name}@{version} is already published; increase the manifest version')
        if publish and old is None:
            for relative, digest in files.items():
                committed = git(root, 'show', f'{commit}:packages/{name}/{relative}')
                if hashlib.sha256(committed).hexdigest() != digest:
                    raise ValueError(f'uncommitted publication input: {name}/{relative}')
            index['versions'][version] = {'commit': commit, 'dependencies': dependencies, 'files': files}
            pending[name] = serialize(index)
    for name in previous:
        if not (root / 'packages' / name / MANIFEST).is_file():
            raise ValueError(f'published package source removed: {name}')
    if pending:
        (root / 'index').mkdir(exist_ok=True)
        for name, text in pending.items():
            path = root / 'index' / f'{name}.toml'
            temporary = path.with_suffix('.toml.tmp')
            temporary.write_text(text, encoding='utf-8')
            temporary.replace(path)
    print(f'Checked {len(packages)} packages; generated {len(pending)} catalogs')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Validate and publish the LuaT registry')
    parser.add_argument('--luat', required=True)
    parser.add_argument('--publish', action='store_true')
    parser.add_argument('--base')
    args = parser.parse_args()
    try:
        base = args.base if args.base and set(args.base) != {'0'} else None
        run(Path.cwd(), str(Path(args.luat).resolve()), args.publish, base)
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as error:
        print(f'error: {error}', file=sys.stderr)
        sys.exit(2)
