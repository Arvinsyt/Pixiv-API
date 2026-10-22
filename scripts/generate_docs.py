#!/usr/bin/env python3
"""将 apis/ 下的 OpenAPI 3.0.3 规范转换为 docs/ 下的 Markdown API 文档。

- apis/<name>.yaml -> docs/<name>.md（_shared.yaml 生成 docs/_shared.md）

用法：
    python scripts/generate_docs.py
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
APIS_DIR = ROOT / "apis"
DOCS_DIR = ROOT / "docs"
SHARED = "_shared.yaml"
# 源文件链接指向 GitHub 仓库:apis/ 在 srcDir 之外不会随站点发布,站内相对路径必然 404
REPO_BLOB = "https://github.com/Arvinsyt/Pixiv-API/blob/main"

SCHEMA_REF = re.compile(r"^(?:_shared\.yaml)?#/components/schemas/([^/]+)$")
METHODS = ("get", "put", "post", "delete", "patch", "options", "head", "trace")


# ---------------------------------------------------------------- 基础工具

_R_COMBINING = re.compile(r"[\u0300-\u036f]")
_R_CONTROL = re.compile(r"[\u0000-\u001f]")
# 连续特殊字符(空格、/、_、标点等)折叠为单个 -,与 VitePress slugify 的 rSpecial 一致
_R_SPECIAL = re.compile(r"[\s~`!@#$%^&*()\-_+=[\]{}|\\;:\"'“”‘’<>,.?/]+")


def slug(text: str) -> str:
    """VitePress 风格的标题锚点,必须与 vitepress 的 slugify 行为一致,否则链接命不中标题 id。"""
    s = unicodedata.normalize("NFKD", str(text))
    s = _R_COMBINING.sub("", s)
    s = _R_CONTROL.sub("", s)
    s = _R_SPECIAL.sub("-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    if s[:1].isdigit():
        s = "_" + s
    return s.lower()


def fmt_val(value) -> str:
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)


def fenced_json(value) -> str:
    return "```json\n" + json.dumps(value, ensure_ascii=False, indent=2) + "\n```"


def md_text(text) -> str:
    """描述文本：去除首尾空白，并把对其他 yaml 文件的提及转为文档链接。"""
    if not text:
        return ""
    s = str(text).strip()

    def to_link(m: re.Match) -> str:
        stem = m.group(1)
        return f"[{stem}.yaml]({stem}.md)" if (APIS_DIR / f"{stem}.yaml").is_file() else m.group(0)

    s = re.sub(r"`(\w+)\.yaml`", to_link, s)
    s = re.sub(r"(?<!\[)(\w+)\.yaml\b(?!#)", to_link, s)
    return s


def cell(text) -> str:
    """表格单元格：单行化并转义竖线。"""
    return str(text).replace("\n", "<br>").replace("|", "\\|") if text is not None else ""


def table(header: list[str], rows: list[tuple]) -> str:
    out = ["| " + " | ".join(header) + " |", "| " + " | ".join(["---"] * len(header)) + " |"]
    out += ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join(out)


# ---------------------------------------------------------------- $ref 解析

class Resolver:
    """解析 $ref：#/... 指向当前文件，_shared.yaml#/... 指向共享组件。"""

    def __init__(self, local: dict, shared: dict):
        self.local, self.shared = local, shared

    def resolve(self, ref: str):
        doc, pointer = self.local, ref
        if ref.startswith(SHARED):
            doc, pointer = self.shared, ref[len(SHARED):]
        if not pointer.startswith("#/"):
            raise ValueError(f"不支持的 $ref：{ref}")
        node = doc
        try:
            for key in pointer[2:].split("/"):
                node = node[key]
        except (KeyError, TypeError):
            raise KeyError(f"无法解析 $ref：{ref}") from None
        return node

    def deref(self, node):
        while isinstance(node, dict) and "$ref" in node:
            node = self.resolve(node["$ref"])
        return node


# ---------------------------------------------------------------- schema 展示

def schema_ref(schema) -> str | None:
    """schema 为纯 $ref（或 allOf 包单个 $ref）时返回该 $ref 字符串。"""
    if not isinstance(schema, dict):
        return None
    ref = schema.get("$ref")
    if ref is None:
        all_of = schema.get("allOf")
        if isinstance(all_of, list) and len(all_of) == 1 and isinstance(all_of[0], dict):
            ref = all_of[0].get("$ref")
    return ref if isinstance(ref, str) and SCHEMA_REF.match(ref) else None


def ref_link(ref: str, shared_base: str) -> str:
    name = SCHEMA_REF.match(ref).group(1)
    base = shared_base if ref.startswith(SHARED) else ""
    return f"[{name}]({base}#{slug(name)})"


def type_label(schema, shared_base: str) -> str:
    ref = schema_ref(schema)
    if ref:
        return ref_link(ref, shared_base)
    t = schema.get("type")
    if t == "array":
        return f"{type_label(schema.get('items') or {}, shared_base)}[]"
    if t:
        return t
    return "object" if schema.get("properties") is not None else "any"


def constraint_parts(schema: dict, include_description=True):
    parts = []
    if include_description and schema.get("description"):
        parts.append(md_text(schema["description"]))
    if schema.get("deprecated"):
        parts.append("**已废弃**")
    if "default" in schema:
        parts.append(f"默认 `{fmt_val(schema['default'])}`")
    if "enum" in schema:
        parts.append("可选值 " + " / ".join(f"`{fmt_val(v)}`" for v in schema["enum"]))
    if schema.get("format"):
        parts.append(f"格式 `{schema['format']}`")
    if "minimum" in schema:
        parts.append(f"最小值 {schema['minimum']}")
    if schema.get("example") is not None:
        parts.append(f"示例 `{fmt_val(schema['example'])}`")
    if schema.get("nullable"):
        parts.append("可为 null")
    return parts


def emit_properties(props, required, prefix, rows, shared_base, resolver):
    for name, sub in (props or {}).items():
        emit_property(name, sub or {}, prefix, required, rows, shared_base, resolver)


def emit_property(name, schema, prefix, required, rows, shared_base, resolver):
    path = prefix + str(name)
    req = "✓" if name in required else ""
    notes = cell("；".join(constraint_parts(schema)))

    ref = schema_ref(schema)
    if ref:
        rows.append((f"`{path}`", ref_link(ref, shared_base), req, notes))
        return

    t = schema.get("type")
    props = schema.get("properties")
    if t == "object" or props is not None:
        rows.append((f"`{path}`", "object", req, notes))
        emit_properties(props, schema.get("required") or [], f"{path}.", rows, shared_base, resolver)
    elif t == "array":
        items = schema.get("items") or {}
        if items.get("properties") is not None:
            rows.append((f"`{path}`", "object[]", req, notes))
            emit_properties(items["properties"], items.get("required") or [],
                            f"{path}[].", rows, shared_base, resolver)
        else:
            rows.append((f"`{path}`", type_label(schema, shared_base), req, notes))
    else:
        rows.append((f"`{path}`", type_label(schema, shared_base), req, notes))


def flatten_root(schema, shared_base, resolver):
    """把响应/请求体的根 schema 展开成字段行；无法展开（非对象/无字段）时返回 None。"""
    if not isinstance(schema, dict):
        return None
    if schema_ref(schema):
        schema = resolver.deref(schema)
    members = schema["allOf"] if isinstance(schema.get("allOf"), list) else [schema]
    members = [resolver.deref(m) for m in members if isinstance(m, dict)]
    required = set()
    for m in members:
        required |= set(m.get("required") or [])
    rows = []
    for m in members:
        emit_properties(m.get("properties"), required, "", rows, shared_base, resolver)
    return rows or None


# ---------------------------------------------------------------- 片段渲染

def param_row(param: dict, shared_base: str, resolver: Resolver):
    p = resolver.deref(param)
    sch = p.get("schema") or {}
    parts = []
    if p.get("deprecated"):
        parts.append("**已废弃**")
    desc = p.get("description") or sch.get("description")
    if desc:
        parts.append(md_text(desc))
    parts += constraint_parts(sch, include_description=False)
    return (f"`{p['name']}`", p.get("in", "query"), type_label(sch, shared_base),
            "✓" if p.get("required") else "", cell("；".join(parts)))


def media_examples(media: dict) -> list[str]:
    out = []
    examples = media.get("examples")
    if isinstance(examples, dict) and examples:
        for name, ex in examples.items():
            ex = ex or {}
            label = ex.get("summary") or name
            out.append(f"**{label}**\n\n{fenced_json(ex.get('value'))}")
    elif media.get("example") is not None:
        out.append(fenced_json(media["example"]))
    return out


def render_security(op: dict, spec: dict, shared: dict) -> str:
    schemes = {**(shared.get("components", {}).get("securitySchemes") or {}),
               **(spec.get("components", {}).get("securitySchemes") or {})}
    sec = op.get("security")
    if not sec:
        return "无需认证"
    items = []
    for req in sec:
        for name in req or {}:
            desc = (schemes.get(name) or {}).get("description", "")
            items.append(f"`{name}` — {md_text(desc)}" if desc else f"`{name}`")
    if len(items) == 1:
        return items[0]
    return "\n\n" + "\n".join(f"- {i}" for i in items) + "\n"


def render_endpoint(L: list, method: str, path: str, op: dict, base_params: list,
                    spec: dict, shared: dict, resolver: Resolver):
    shared_base = "_shared.md"
    heading = f"{method.upper()} {path}"
    if "{" in path:
        # 路径参数形如 {id} 恰在标题行尾时,会被 VitePress 的标题属性语法
        # ({#id}) 误解析为用户自定义锚点;追加显式锚点覆盖之,与目录链接同源。
        L.append(f"### {heading} {{#{slug(heading)}}}")
    else:
        L.append(f"### {heading}")
    L.append("")
    if op.get("summary"):
        L.append(f"**{op['summary']}**")
        L.append("")
    if op.get("description"):
        L.append(md_text(op["description"]))
        L.append("")
    meta = [f"operationId `{op.get('operationId', '')}`"]
    if op.get("tags"):
        meta.append("标签 " + "、".join(f"`{t}`" for t in op["tags"]))
    if op.get("deprecated"):
        meta.append("**已废弃**")
    L.append("*" + " · ".join(meta) + "*")
    L.append("")
    L.append(f"**认证**：{render_security(op, spec, shared)}")
    L.append("")

    params = list(base_params) + list(op.get("parameters") or [])
    if params:
        rows = [param_row(p, shared_base, resolver) for p in params]
        L.append("#### 请求参数")
        L.append("")
        L.append(table(["参数", "位置", "类型", "必填", "说明"], rows))
        L.append("")

    body = op.get("requestBody")
    if body:
        body = resolver.deref(body)
        for media_type, media in (body.get("content") or {}).items():
            need = "必填" if body.get("required") else "可选"
            L.append(f"#### 请求体（`{media_type}`，{need}）")
            L.append("")
            rows = flatten_root(media.get("schema"), shared_base, resolver)
            if rows:
                L.append(table(["字段", "类型", "必填", "说明"], rows))
                L.append("")
            for ex in media_examples(media):
                L.append(ex)
                L.append("")

    responses = op.get("responses") or {}
    if responses:
        L.append("#### 响应")
        L.append("")
        status_rows, field_blocks, example_blocks = [], [], []
        for status, resp in responses.items():
            resp = resolver.deref(resp)
            content = resp.get("content") or {}
            media_type, media = next(iter(content.items()), (None, None))
            struct = ""
            if media is not None:
                sch = media.get("schema") or {}
                plain = resolver.deref(sch)
                if plain.get("type") == "object" and not plain.get("properties"):
                    struct = "`{}`"
                elif schema_ref(sch):
                    struct = ref_link(schema_ref(sch), shared_base)
                elif plain.get("type"):
                    struct = f"`{plain['type']}`"
                else:
                    struct = "`object`"
            status_rows.append((f"`{status}`", cell(md_text(resp.get("description", ""))), struct))
            if media is None:
                continue
            if status.startswith("2"):
                rows = flatten_root(media.get("schema"), shared_base, resolver)
                if rows:
                    field_blocks.append((status, media_type, rows))
            if media.get("example") is not None or media.get("examples"):
                example_blocks.append((status, media_examples(media)))
        L.append(table(["状态码", "说明", "结构"], status_rows))
        L.append("")
        for status, media_type, rows in field_blocks:
            L.append(f"**{status} 响应字段**（`{media_type}`）")
            L.append("")
            L.append(table(["字段", "类型", "必填", "说明"], rows))
            L.append("")
        for status, exs in example_blocks:
            L.append(f"**{status} 响应示例**")
            L.append("")
            for ex in exs:
                L.append(ex)
                L.append("")


def render_schema_section(L: list, name: str, schema: dict, shared_base: str, resolver: Resolver):
    schema = resolver.deref(schema)
    L.append(f"### {name}")
    L.append("")
    desc_parts = []
    if schema.get("description"):
        desc_parts.append(md_text(schema["description"]))
    if schema.get("additionalProperties"):
        desc_parts.append("允许出现未列出的额外字段。")
    if desc_parts:
        L.append("\n\n".join(desc_parts))
        L.append("")
    rows = flatten_root(schema, shared_base, resolver)
    if rows:
        L.append(table(["字段", "类型", "必填", "说明"], rows))
        L.append("")
    if schema.get("example") is not None:
        L.append("示例：")
        L.append("")
        L.append(fenced_json(schema["example"]))
        L.append("")


def absolutize_refs(node):
    """将 _shared.yaml 内部的 '#/' 相对 $ref 改写为 '_shared.yaml#/' 绝对引用。

    功能文件通过 _shared.yaml#/... 引用共享组件时，组件内部再出现的 '#/'
    引用属于 _shared.yaml 的上下文，需统一前缀后才能被 Resolver 正确解析。
    """
    if isinstance(node, dict):
        ref = node.get("$ref")
        if isinstance(ref, str) and ref.startswith("#/"):
            node["$ref"] = SHARED + ref
        for value in node.values():
            absolutize_refs(value)
    elif isinstance(node, list):
        for value in node:
            absolutize_refs(value)


# ---------------------------------------------------------------- 文档生成

def first_comment(path: Path) -> str:
    with path.open(encoding="utf-8") as f:
        line = f.readline()
    return line.lstrip("#").strip() if line.startswith("#") else ""


def strip_md(text: str) -> str:
    """去掉 markdown 记法（链接、加粗、行内代码），供 meta description 使用。"""
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    s = s.replace("**", "").replace("`", "")
    # 中文之间的空白（段内硬换行折叠而来）不保留
    s = re.sub(r"(?<=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])\s+(?=[\u4e00-\u9fff])", "", s)
    return re.sub(r"\s+", " ", s).strip()


def page_title(spec: dict, spec_path: Path) -> str:
    """从 yaml 首行注释「<中文名>（<服务器>）」推导页面标题，按服务器附加 API 分组后缀。"""
    fallback = (spec.get("info") or {}).get("title", spec_path.stem)
    base = re.split(r"[（(]", first_comment(spec_path) or fallback)[0].strip()
    base = base.replace(" · Web", "")
    servers = spec.get("servers") or []
    url = (servers[0] or {}).get("url", "") if servers else ""
    if "app-api" in url:
        return f"{base} · App API"
    if "www.pixiv.net" in url:
        return f"{base} · Web API"
    return base


def page_description(spec: dict) -> str:
    """info.description 首段去掉 markdown 后作为 meta description，超长截断。"""
    text = ((spec.get("info") or {}).get("description") or "").strip()
    if not text:
        return ""
    s = strip_md(text.split("\n\n")[0]).rstrip("，,；; ")
    if len(s) > 120:
        s = s[:120].rstrip("、，,；;：:．.。 ") + "……"
    return s


def frontmatter(title: str, description: str) -> list[str]:
    """VitePress 页面 frontmatter：title 用于 <title>/og:title，description 用于 meta description。"""
    out = ["---", f"title: {json.dumps(title, ensure_ascii=False)}"]
    if description:
        out.append(f"description: {json.dumps(description, ensure_ascii=False)}")
    out += ["---", ""]
    return out


def generate_api_doc(spec_path: Path, shared: dict) -> dict:
    spec = yaml.safe_load(spec_path.read_text(encoding="utf-8")) or {}
    resolver = Resolver(spec, shared)
    info = spec.get("info") or {}
    L = frontmatter(page_title(spec, spec_path), page_description(spec))
    L.append(f"# {info.get('title', spec_path.stem)}")
    L.append("")

    meta = [f"[源文件 `apis/{spec_path.name}`]({REPO_BLOB}/apis/{spec_path.name})"]
    servers = spec.get("servers") or []
    if servers:
        meta.append("Base URL " + " / ".join(f"`{s.get('url')}`" for s in servers))
    L.append("> " + " · ".join(meta))
    L.append("")
    if info.get("description"):
        L.append(md_text(info["description"]))
        L.append("")

    ops, sections = [], []
    for path, item in (spec.get("paths") or {}).items():
        item = item or {}
        base_params = item.get("parameters") or []
        for method in METHODS:
            op = item.get(method)
            if not op:
                continue
            heading = f"{method.upper()} {path}"
            label = op.get("summary") or op.get("operationId") or heading
            ops.append((heading, label))
            sec: list = []
            render_endpoint(sec, method, path, op, base_params, spec, shared, resolver)
            sections.append("\n".join(sec))

    if ops:
        L.append("## 接口目录")
        L.append("")
        for heading, label in ops:
            L.append(f"- [{heading}](#{slug(heading)}) — {label}")
        L.append("")
        L.append("## 接口")
        L.append("")
        for s in sections:
            L.append(s)
            L.append("")

    local_schemas = (spec.get("components") or {}).get("schemas") or {}
    if local_schemas:
        L.append("## 数据模型")
        L.append("")
        for name, sch in local_schemas.items():
            render_schema_section(L, name, sch, "", resolver)

    content = "\n".join(L).rstrip() + "\n"
    (DOCS_DIR / f"{spec_path.stem}.md").write_text(content, encoding="utf-8", newline="\n")
    return {"stem": spec_path.stem, "title": info.get("title", ""), "servers": servers,
            "ops": ops, "first_comment": first_comment(spec_path)}


def generate_shared_doc(shared: dict):
    resolver = Resolver(shared, shared)
    L = frontmatter("公共约定与数据模型", page_description(shared))
    L += ["# Pixiv API 共享组件", "", f"> [源文件 `apis/_shared.yaml`]({REPO_BLOB}/apis/_shared.yaml)", ""]
    info = shared.get("info") or {}
    if info.get("description"):
        L.append(md_text(info["description"]))
        L.append("")

    comp = shared.get("components") or {}
    schemes = comp.get("securitySchemes") or {}
    if schemes:
        L.append("## 认证方案")
        L.append("")
        rows = []
        for name, s in schemes.items():
            kind = f"`{s.get('type')}/{s.get('scheme')}`" if s.get("scheme") else f"`{s.get('type')}`"
            rows.append((f"`{name}`", kind, cell(md_text(s.get("description", "")))))
        L.append(table(["方案", "类型", "说明"], rows))
        L.append("")

    params = comp.get("parameters") or {}
    if params:
        L.append("## 公共参数")
        L.append("")
        L.append("各功能文件通过 $ref 引用的公共参数定义：")
        L.append("")
        rows = [param_row(p, "", resolver) for p in params.values()]
        L.append(table(["参数", "位置", "类型", "必填", "说明"], rows))
        L.append("")

    responses = comp.get("responses") or {}
    if responses:
        L.append("## 公共响应")
        L.append("")
        rows = []
        for name, resp in responses.items():
            media = next(iter((resp.get("content") or {}).values()), None)
            struct = ""
            if media is not None:
                sch = media.get("schema") or {}
                plain = resolver.deref(sch)
                if plain.get("type") == "object" and not plain.get("properties"):
                    struct = "`{}`"
                elif schema_ref(sch):
                    struct = ref_link(schema_ref(sch), "")
                else:
                    struct = f"`{plain.get('type', 'object')}`"
            rows.append((f"`{name}`", cell(resp.get("description", "")), struct))
        L.append(table(["名称", "说明", "响应结构"], rows))
        L.append("")

    schemas = comp.get("schemas") or {}
    if schemas:
        L.append("## 错误响应")
        L.append("")
        L.append("业务错误统一返回 ErrorMessage 结构（见 components/schemas/ErrorMessage）。")
        L.append("")
        L.append("## 数据模型")
        L.append("")
        for name, sch in schemas.items():
            render_schema_section(L, name, sch, "", resolver)

    content = "\n".join(L).rstrip() + "\n"
    (DOCS_DIR / "_shared.md").write_text(content, encoding="utf-8", newline="\n")


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    shared_path = APIS_DIR / SHARED
    if not shared_path.is_file():
        sys.exit(f"未找到 {shared_path}")
    shared = yaml.safe_load(shared_path.read_text(encoding="utf-8")) or {}
    absolutize_refs(shared)

    DOCS_DIR.mkdir(exist_ok=True)
    docs_meta = []
    for f in sorted(APIS_DIR.glob("*.yaml")):
        if f.name == SHARED:
            continue
        m = generate_api_doc(f, shared)
        docs_meta.append(m)
        print(f"生成 docs/{f.stem}.md（{len(m['ops'])} 个接口）")
    generate_shared_doc(shared)
    print("生成 docs/_shared.md")
    total = sum(len(m["ops"]) for m in docs_meta)
    print(f"完成，共 {total} 个接口")


if __name__ == "__main__":
    main()
