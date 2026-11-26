"""Local Mermaid rendering for Markdown publication (no source files modified)."""

import hashlib
import json
import logging
import shlex
import subprocess
from pathlib import Path

from markdown.extensions import Extension
from markdown.extensions.fenced_code import FencedBlockPreprocessor
from markdown.preprocessors import Preprocessor

from confpoint.image_tag import ImageTag

log = logging.getLogger(__name__)


class MermaidRenderer:
    def __init__(self, directory, document, command='mmdc', image_format='png',
                 timeout=120, no_sandbox=False):
        if image_format not in ('png', 'svg'):
            raise ValueError('Mermaid format must be png or svg')
        if timeout <= 0:
            raise ValueError('Mermaid timeout must be positive')
        self.directory = Path(directory)
        self.command = shlex.split(command)
        self.image_format = image_format
        self.timeout = timeout
        self.no_sandbox = no_sandbox
        # Stable across checkout locations; diagram positions update existing attachments.
        self.document = hashlib.sha256(Path(document).name.encode('utf-8')).hexdigest()[:12]
        self.tags = []

    def render(self, source):
        number = len(self.tags) + 1
        name = 'confpoint-mermaid-{}-{}'.format(self.document, number)
        self.directory.mkdir(parents=True, exist_ok=True)
        source_file = self.directory / (name + '.mmd')
        image = self.directory / (name + '.' + self.image_format)
        source_file.write_text(source, encoding='utf-8')
        command = self.command + ['-i', str(source_file), '-o', str(image), '-b', 'white']
        if self.no_sandbox:
            config = self.directory / 'puppeteer.json'
            config.write_text(json.dumps({'args': ['--no-sandbox']}), encoding='utf-8')
            command += ['--puppeteerConfigFile', str(config)]
            log.warning('Chromium sandbox disabled: render trusted diagrams only')
        try:
            subprocess.run(command, check=True, capture_output=True, text=True,
                           timeout=self.timeout)
        except FileNotFoundError as exc:
            raise RuntimeError('Mermaid CLI not found; install @mermaid-js/mermaid-cli '
                               'or specify --mermaid-cli') from exc
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError('Mermaid diagram {} timed out after {} seconds'.format(
                number, self.timeout)) from exc
        except subprocess.CalledProcessError as exc:
            raise RuntimeError('Mermaid diagram {} failed: {}'.format(
                number, exc.stderr or exc.stdout)) from exc
        if not image.is_file():
            raise RuntimeError('Mermaid diagram {} produced no image'.format(number))
        tag = ImageTag('', image)
        self.tags.append(tag)
        log.info('Rendered Mermaid diagram %s', number)
        return tag.to_confluence()


class MermaidPreprocessor(Preprocessor):
    def __init__(self, md, renderer):
        super().__init__(md)
        self.renderer = renderer

    def run(self, lines):
        def replace(match):
            if match.group('lang') != 'mermaid':
                return match.group(0)
            html = self.renderer.render(match.group('code'))
            return '\n' + self.md.htmlStash.store(html) + '\n'

        # Match every complete fence, so mermaid examples inside a larger code
        # fence are not interpreted as diagrams.
        return FencedBlockPreprocessor.FENCED_BLOCK_RE.sub(
            replace, '\n'.join(lines)).split('\n')


class MermaidExtension(Extension):
    def __init__(self, renderer):
        self.renderer = renderer
        super().__init__()

    def extendMarkdown(self, md):
        md.preprocessors.register(MermaidPreprocessor(md, self.renderer), 'mermaid', 26)
