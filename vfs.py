"""Простая виртуальная файловая система из XML."""
import xml.etree.ElementTree as ET
import base64
import binascii


class VFS:
    def __init__(self, filename=None):
        self.root = ET.parse(filename).getroot() if filename else ET.Element('vfs')
        if self.root.tag != 'vfs':
            raise ValueError('root element must be vfs')
        for node in self.root.iter():
            if node is not self.root and (node.tag not in ('dir', 'file') or not node.get('name')):
                raise ValueError('invalid XML node')
            if node.tag == 'file' and node.get('encoding') == 'base64':
                try:
                    base64.b64decode((node.text or '').strip(), validate=True)
                except (binascii.Error, ValueError):
                    raise ValueError('invalid base64 file: ' + node.get('name', ''))
        self.cwd = '/'

    def parts(self, path):
        if path.startswith('/'):
            result = []
        else:
            result = [x for x in self.cwd.split('/') if x]
        for part in path.split('/'):
            if part == '..':
                if result:
                    result.pop()
            elif part not in ('', '.'):
                result.append(part)
        return result

    def find(self, path):
        node = self.root
        for part in self.parts(path):
            node = next((child for child in node if child.get('name') == part), None)
            if node is None:
                raise ValueError('path not found: ' + path)
        return node

    def ls(self, path='.'):
        node = self.find(path)
        if node.tag != 'dir' and node is not self.root:
            raise ValueError('not a directory: ' + path)
        return '\n'.join(child.get('name', '') + ('/' if child.tag == 'dir' else '') for child in node)

    def cd(self, path='/'):
        node = self.find(path)
        if node.tag != 'dir' and node is not self.root:
            raise ValueError('not a directory: ' + path)
        self.cwd = '/' + '/'.join(self.parts(path))

    def read(self, path):
        node = self.find(path)
        if node.tag != 'file':
            raise ValueError('not a file: ' + path)
        if node.get('encoding') == 'base64':
            raise ValueError('binary file: ' + path)
        return node.text or ''

    def mv(self, source, destination):
        srcparts = self.parts(source)
        if not srcparts:
            raise ValueError('cannot move root')
        parent = self.find('/' + '/'.join(srcparts[:-1]))
        node = self.find(source)
        destparts = self.parts(destination)
        try:
            target = self.find(destination)
            if target.tag != 'dir' and target is not self.root:
                raise ValueError('destination already exists: ' + destination)
            destparent, newname = target, node.get('name')
        except ValueError as error:
            if not str(error).startswith('path not found:'):
                raise
            if not destparts:
                raise ValueError('invalid destination')
            destparent = self.find('/' + '/'.join(destparts[:-1]))
            newname = destparts[-1]
        if destparent.tag != 'dir' and destparent is not self.root:
            raise ValueError('not a directory: ' + destination)
        # Нельзя переместить каталог внутрь самого себя.
        if node is destparent or any(destparent is x for x in node.iter()):
            raise ValueError('cannot move directory into itself')
        if any(x is not node and x.get('name') == newname for x in destparent):
            raise ValueError('destination already exists: ' + newname)
        parent.remove(node)
        node.set('name', newname)
        destparent.append(node)
        # После перемещения возвращаемся в корень: старый текущий путь мог исчезнуть.
        self.cwd = '/'

    def save(self, filename):
        ET.ElementTree(self.root).write(filename, encoding='utf-8', xml_declaration=True)
