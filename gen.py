# coding=utf-8
import yaml

with open("mkdocs_template.yml", "r") as f:
    raw_data = yaml.load(f)
    data = raw_data["pages"]


def one(item, depth=0, result=""):
    for k, v in item.iteritems():
        if isinstance(v, basestring):
            if v.endswith("index.md"):
                v = v[:-8]
            if v.endswith(".md"):
                v = v[:-3]
            result += " ".join([" " * depth, "-", "[" + k + "](/" + v + ")\n"])
            print v, result
        elif isinstance(v, list):
            result += " ".join([" " * depth, "-", k, "\n"])
            for v_item in v:
                result += one(v_item, depth + 4)
    return result


def get_all(l):
    result = ""
    for _ in l:
        result += one(_)
    return result

new_data = []
for _ in data:
    name = list(_.iteritems())[0][0]
    if name == "Home":
        new_data.append(_)
        content = get_all(data)
        with open("src/index_template.md", "r") as f:
            old = f.read()
            old = old.replace("<!--TOC-->", content.encode("utf-8"))
        with open("src/index.md", "w") as f:
            f.write(old)
    else:
        content = one(_)
        path = name + "/index.md"
        with open("src/" + path, "w") as f:
            f.write("# Table of contents\n" + content.encode("utf-8"))
        tmp = [{"index": path}]
        tmp.extend(_[name])
        new_data.append({name: tmp})

raw_data["pages"] = new_data

with open("mkdocs.yml", "w") as f:
    yaml.dump(raw_data, f, default_flow_style=False)
