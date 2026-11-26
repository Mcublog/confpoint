import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import markdown

from confpoint.publisher.mermaid import MermaidExtension, MermaidRenderer


class MermaidTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.renderer = MermaidRenderer(self.temp.name, 'overview.md')

    def convert(self, text):
        return markdown.markdown(text, extensions=['fenced_code',
                                                  MermaidExtension(self.renderer)])

    def fake_render(self, command, **kwargs):
        Path(command[command.index('-o') + 1]).write_bytes(b'PNG')

    @patch('confpoint.publisher.mermaid.subprocess.run')
    def test_multiple_diagrams(self, run):
        run.side_effect = self.fake_render
        html = self.convert('```mermaid\ngraph TD; A-->B\n```\n\n'
                            '~~~mermaid\ngraph TD; B-->C\n~~~\n\n![photo](photo.png)')
        self.assertEqual(2, run.call_count)
        self.assertEqual(2, len(self.renderer.tags))
        self.assertIn('<ac:image>', html)
        self.assertIn('src="photo.png"', html)
        self.assertNotIn('language-mermaid', html)
        self.assertTrue(all(t.file.exists() for t in self.renderer.tags))

    @patch('confpoint.publisher.mermaid.subprocess.run')
    def test_code_examples_and_plain_document(self, run):
        html = self.convert('````markdown\n```mermaid\ngraph TD; A-->B\n```\n````')
        self.assertIn('language-markdown', html)
        self.assertIn('```mermaid', html)
        self.assertIn('<h1>Hello</h1>', self.convert('# Hello'))
        run.assert_not_called()

    @patch('confpoint.publisher.mermaid.subprocess.run', side_effect=FileNotFoundError)
    def test_missing_cli(self, run):
        with self.assertRaisesRegex(RuntimeError, 'CLI not found'):
            self.convert('```mermaid\ngraph TD; A-->B\n```')

    @patch('confpoint.publisher.mermaid.subprocess.run')
    def test_timeout_and_invalid_diagram(self, run):
        for error, message in [(subprocess.TimeoutExpired('mmdc', 1), 'timed out'),
                               (subprocess.CalledProcessError(1, 'mmdc', stderr='syntax'), 'syntax')]:
            run.side_effect = error
            with self.assertRaisesRegex(RuntimeError, message):
                self.renderer.render('invalid')

    @patch('confpoint.publisher.mermaid.subprocess.run')
    def test_stable_names_and_sandbox(self, run):
        run.side_effect = self.fake_render
        self.renderer.render('graph TD; A-->B')
        other = MermaidRenderer(self.temp.name, '/another/overview.md', no_sandbox=True)
        other.render('graph TD; B-->C')
        self.assertEqual(self.renderer.tags[0].file.name, other.tags[0].file.name)
        self.assertIn('--puppeteerConfigFile', run.call_args[0][0])


if __name__ == '__main__':
    unittest.main()
