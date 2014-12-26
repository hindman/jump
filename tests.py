import unittest
import imp
import os

nameit        = imp.load_source('nameit', 'nameit')
process_paths = nameit.process_paths
parse_options = nameit.parse_options
os.remove('nameitc')

class Nameit_TC(unittest.TestCase):

    def setUp(self):
        pass

    def test_named_paths_file(self):
        '''
        named_paths_file(): can exercise
        '''
        npf = nameit.named_paths_file()
        self.assertIsInstance(npf, str)

    def test_abspath(self):
        '''
        abspath(): can exercise
        '''
        tests = [
            '.',
            '../../blort',
            '~/foo/bar',
        ]
        for p in tests:
            ap = nameit.abspath(p)
            self.assertIsInstance(ap, str)

    def test_json_functions(self):
        '''
        JSON functions
        '''
        # Setup some named path info.
        f = 'tmp/nameit_test.json'
        d1 = dict(
            foo = '/foo/bar/blah',
            blort = '/tmp/blort',
        )
        # Remove temp file if it exists.
        OP = os.path
        if OP.isfile(f):
            os.remove(f)
        self.assertFalse(OP.isfile(f))
        # Save the named paths.
        nameit.save_named_paths(f, d1)
        self.assertTrue(OP.isfile(f))
        # Load them and make sure they equal the original.
        d2 = nameit.load_named_paths(f)
        self.assertEqual(d1, d2)
        # Clean up.
        os.remove(f)
        self.assertFalse(OP.isfile(f))

    def test_parse_options(self):
        '''
        parse_options()
        '''
        # Invalid options.
        args = '--hello --add x y'.split()
        opts, code, msg = parse_options(args)
        self.assertTrue(code)
        self.assertIn('Unrecognized arguments', msg)

        # Help.
        args = '--help --add a b'.split()
        opts, code, msg = parse_options(args)
        self.assertFalse(code)
        self.assertEqual(msg, nameit.usage())

        # Version.
        args = '--version --add q r'.split()
        opts, code, msg = parse_options(args)
        self.assertFalse(code)
        self.assertIn(nameit.__version__, msg)

        # Conflicting options.
        tests = [
            '--add a b -rm x',
            '--mv a b foo',
        ]
        for t in tests:
            args = t.split()
            opts, code, msg = parse_options(args)
            self.assertTrue(code)
            self.assertIn('Conflicting arguments', msg)

        # Regular usages.
        tests = [
            '--add a b',
            '--rm a',
            '--mv a b',
            'foo',
            '',
        ]
        for t in tests:
            args = t.split()
            opts, code, msg = parse_options(args)
            self.assertFalse(code)
            self.assertFalse(msg)

    def test_process_paths_add(self):
        '''
        process_paths(add)
        '''
        # Basic add.
        args = '--add a /foo/bar'.split()
        _, k, v = args
        opts = parse_options(args)[0]
        paths1 = {}
        paths2, save, code, msg = process_paths(opts, paths1)
        self.assertTrue(save)
        self.assertFalse(code)
        self.assertFalse(msg)
        self.assertEqual(paths2[k], v)
        self.assertNotEqual(paths1, paths2)

        # With --literal.
        args = '--add a ../foo/bar --literal'.split()
        _, k, v, _ = args
        opts = parse_options(args)[0]
        paths1 = {}
        paths2, save, code, msg = process_paths(opts, paths1)
        self.assertTrue(save)
        self.assertFalse(code)
        self.assertFalse(msg)
        self.assertEqual(paths2[k], v)
        self.assertNotEqual(paths1, paths2)

    def test_process_paths_rm(self):
        '''
        process_paths(rm)
        '''
        # Successful.
        args = '--rm a'.split()
        _, k = args
        opts = parse_options(args)[0]
        paths1 = dict(a = 'hi')
        paths2, save, code, msg = process_paths(opts, paths1)
        self.assertTrue(save)
        self.assertFalse(code)
        self.assertFalse(msg)
        self.assertEqual(paths2, {})
        self.assertNotEqual(paths1, paths2)

        # Bad key.
        args = '--rm a'.split()
        _, k = args
        opts = parse_options(args)[0]
        paths1 = {}
        paths2, save, code, msg = process_paths(opts, paths1)
        self.assertFalse(save)
        self.assertTrue(code)
        self.assertTrue(msg)
        self.assertIn('Name not found', msg)
        self.assertEqual(paths2, {})

    def test_process_paths_mv(self):
        '''
        process_paths(mv)
        '''
        # Successful.
        args = '--mv a b'.split()
        _, k1, k2 = args
        opts = parse_options(args)[0]
        v = 'hi'
        paths1 = dict(a = v)
        paths2, save, code, msg = process_paths(opts, paths1)
        self.assertTrue(save)
        self.assertFalse(code)
        self.assertFalse(msg)
        self.assertEqual(paths2[k2], v)
        self.assertEqual(paths1[k1], paths2[k2])
        self.assertNotIn(k1, paths2)
        self.assertNotEqual(paths1, paths2)

        # Bad key.
        args = '--mv a b'.split()
        _, k1, k2 = args
        opts = parse_options(args)[0]
        paths1 = {}
        paths2, save, code, msg = process_paths(opts, paths1)
        self.assertFalse(save)
        self.assertTrue(code)
        self.assertTrue(msg)
        self.assertIn('Name not found', msg)
        self.assertEqual(paths1, paths2)

    def test_process_paths_name(self):
        '''
        process_paths(name)
        '''
        # Successful.
        k, v = 'a b'.split()
        opts = parse_options([k])[0]
        paths1 = {k : v}
        paths2, save, code, msg = process_paths(opts, paths1)
        self.assertFalse(save)
        self.assertFalse(code)
        self.assertEqual(msg, v)

        # Bad key.
        k = 'a'
        opts = parse_options([k])[0]
        paths1 = {}
        paths2, save, code, msg = process_paths(opts, paths1)
        self.assertFalse(save)
        self.assertTrue(code)
        self.assertTrue(msg)
        self.assertIn('Name not found', msg)

    def test_process_paths_all_names(self):
        '''
        process_paths(all_names)
        '''
        # Successful.
        opts = parse_options([])[0]
        paths1 = dict(a = 'hi', b = 'bye')
        paths2, save, code, msg = process_paths(opts, paths1)
        self.assertFalse(save)
        self.assertFalse(code)
        for k, v in paths2.items():
            self.assertIn(k, msg)
            self.assertIn(v, msg)

        # No names.
        opts = parse_options([])[0]
        paths1 = {}
        paths2, save, code, msg = process_paths(opts, paths1)
        self.assertFalse(save)
        self.assertFalse(code)
        self.assertIn('No names', msg)

