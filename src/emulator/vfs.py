import base64
import os
import xml.etree.ElementTree as ET


class VFSError(Exception):
    """Virtual file system error."""


class VirtualFileSystem:
    def __init__(self):
        self.root = {"type": "dir", "children": {}}

    def load(self, path):
        if not os.path.exists(path):
            raise VFSError(f"VFS file not found: {path}")
        try:
            tree = ET.parse(path)
        except ET.ParseError as exc:
            raise VFSError(f"invalid VFS XML: {exc}") from exc
        root_el = tree.getroot()
        if root_el.tag != "vfs":
            raise VFSError("root element must be <vfs>")
        self.root = {"type": "dir", "children": {}}
        self._load_children(root_el, self.root)

    def _load_children(self, parent_el, parent_node):
        for child in parent_el:
            name = child.attrib.get("name")
            if not name:
                raise VFSError("VFS item without name")
            if child.tag == "dir":
                node = {"type": "dir", "children": {}}
                parent_node["children"][name] = node
                self._load_children(child, node)
            elif child.tag == "file":
                encoding = child.attrib.get("encoding", "utf-8")
                text = child.text or ""
                if encoding == "base64":
                    try:
                        content = base64.b64decode(text.encode("ascii"))
                    except Exception as exc:
                        raise VFSError(f"invalid base64 in {name}") from exc
                    binary = True
                else:
                    content = text
                    binary = False
                parent_node["children"][name] = {
                    "type": "file",
                    "content": content,
                    "binary": binary,
                }
            else:
                raise VFSError(f"unsupported element: {child.tag}")

    def save(self, path):
        root_el = ET.Element("vfs", {"name": "saved"})
        self._save_children(root_el, self.root)
        tree = ET.ElementTree(root_el)
        ET.indent(tree, space="  ")
        tree.write(path, encoding="utf-8", xml_declaration=True)

    def _save_children(self, parent_el, parent_node):
        for name, node in parent_node["children"].items():
            if node["type"] == "dir":
                child = ET.SubElement(parent_el, "dir", {"name": name})
                self._save_children(child, node)
            else:
                if node["binary"]:
                    value = base64.b64encode(node["content"]).decode("ascii")
                    attrs = {"name": name, "encoding": "base64"}
                else:
                    value = node["content"]
                    attrs = {"name": name, "encoding": "utf-8"}
                child = ET.SubElement(parent_el, "file", attrs)
                child.text = value

    @staticmethod
    def split_path(path):
        return [part for part in path.replace("\\", "/").split("/") if part]

    def normalize(self, path, cwd="/"):
        if not path:
            path = cwd
        parts = [] if path.startswith("/") else self.split_path(cwd)
        for part in self.split_path(path):
            if part == ".":
                continue
            if part == "..":
                if parts:
                    parts.pop()
            else:
                parts.append(part)
        return "/" + "/".join(parts)

    def get_node(self, path, cwd="/"):
        normalized = self.normalize(path, cwd)
        node = self.root
        for part in self.split_path(normalized):
            if node["type"] != "dir":
                raise VFSError(f"not a directory: {path}")
            if part not in node["children"]:
                raise VFSError(f"path not found: {path}")
            node = node["children"][part]
        return node

    def get_parent(self, path, cwd="/"):
        normalized = self.normalize(path, cwd)
        parts = self.split_path(normalized)
        if not parts:
            raise VFSError("cannot use root here")
        name = parts[-1]
        parent_path = "/" + "/".join(parts[:-1])
        parent = self.get_node(parent_path or "/")
        if parent["type"] != "dir":
            raise VFSError(f"not a directory: {parent_path}")
        return parent, name

    def move(self, source, destination, cwd="/"):
        src_parent, src_name = self.get_parent(source, cwd)
        if src_name not in src_parent["children"]:
            raise VFSError(f"path not found: {source}")
        src_node = src_parent["children"][src_name]
        dest_norm = self.normalize(destination, cwd)
        try:
            dest_node = self.get_node(dest_norm)
        except VFSError:
            dest_node = None
        if dest_node and dest_node["type"] == "dir":
            dest_parent = dest_node
            dest_name = src_name
        else:
            dest_parent, dest_name = self.get_parent(dest_norm)
        dest_parent["children"][dest_name] = src_node
        del src_parent["children"][src_name]
