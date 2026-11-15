import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('registry', Path(__file__).with_name('registry.py'))
registry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(registry)

class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.package = self.root / 'packages' / 'example'
        self.package.mkdir(parents=True)
        (self.package / registry.MANIFEST).write_text("name='example'\nversion='1.0.0'\nauthor='Test'\nlicense='MIT'\nshared=['init.luat']\n")
        (self.package / 'init.luat').write_text('return {}\n')

    def git(self, root, *args):
        if args[0] == 'rev-parse':
            return b'a' * 40
        if args[0] == 'show':
            return (root / args[1].split(':', 1)[1]).read_bytes()
        raise AssertionError(args)

    def test_publish_writes_commit_paths_and_hashes(self):
        with patch.object(registry, 'git', side_effect=self.git), patch.object(registry.subprocess, 'run') as cli:
            registry.run(self.root, 'luat', True)
            self.assertEqual(cli.call_count, 1)
        index = registry.indexes(self.root)['example']
        self.assertEqual(index['versions']['1.0.0']['commit'], 'a' * 40)
        self.assertEqual(index['versions']['1.0.0']['files'], registry.hashes(self.package))
        self.assertEqual(registry.tomllib.loads(registry.serialize(index)), index)

    def test_published_contents_are_immutable(self):
        with patch.object(registry, 'git', side_effect=self.git), patch.object(registry.subprocess, 'run'):
            registry.run(self.root, 'luat', True)
            (self.package / 'init.luat').write_text('return 1\n')
            with self.assertRaisesRegex(ValueError, 'already published'):
                registry.run(self.root, 'luat', True)

    def test_check_does_not_write_index(self):
        with patch.object(registry, 'git', side_effect=self.git), patch.object(registry.subprocess, 'run'):
            registry.run(self.root, 'luat')
        self.assertFalse((self.root / 'index').exists())

    def test_uncommitted_inputs_are_rejected(self):
        with patch.object(registry, 'git', side_effect=lambda root, *args: b'a' * 40), patch.object(registry.subprocess, 'run'):
            with self.assertRaisesRegex(ValueError, 'uncommitted'):
                registry.run(self.root, 'luat', True)
        self.assertFalse((self.root / 'index').exists())

    def test_nested_ignore_and_generated_directories(self):
        (self.package / '.gitignore').write_text('ignored.lua\n')
        (self.package / 'ignored.lua').write_text('skip')
        (self.package / 'target').mkdir()
        (self.package / 'target' / 'generated.lua').write_text('skip')
        self.assertEqual(set(registry.hashes(self.package)), {registry.MANIFEST, 'init.luat'})

if __name__ == '__main__':
    unittest.main()
