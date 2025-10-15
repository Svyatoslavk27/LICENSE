#!/usr/bin/env python3
import re
import sys

def migrate_unittest_to_pytest(source):
    result = []
    inside_class = False
    current_indent = ""

    for line in source.splitlines():
        #Знайти клас із unittest.TestCase (навіть з множинним успадкуванням)
        class_match = re.match(r'^(\s*)class\s+(\w+)\s*\((.*?)\):', line)
        if class_match:
            indent, name, bases = class_match.groups()
            bases_list = [b.strip() for b in bases.split(',')]
            # Прибираємо unittest.TestCase
            new_bases = [b for b in bases_list if b != "unittest.TestCase" and b != "TestCase"]
            if new_bases:
                new_line = f"{indent}class {name}({', '.join(new_bases)}):"
            else:
                # Якщо TestCase був єдиною базою — перетворюємо на коментар
                new_line = f"{indent}# Converted from unittest.TestCase: class {name}"
            result.append(new_line)
            inside_class = True
            current_indent = indent
            continue

        #Знайти метод test_*
        method_match = re.match(r'^(\s*)def\s+test_(\w+)\s*\(self[\,\)]', line)
        if method_match:
            indent, name = method_match.groups()
            # У pytest не треба self і test_-префікс необов’язковий — зробимо camelCase
            new_name = name[0].upper() + name[1:]
            new_line = re.sub(r'def\s+test_\w+\(self[\,\)]', f"def test{new_name}():", line)
            result.append(new_line)
            continue

        #Кінець класу
        if inside_class and (not line.startswith(current_indent + " ") and line.strip()):
            inside_class = False
            current_indent = ""

        #Прибираємо import unittest
        if re.match(r'\s*import\s+unittest', line):
            continue
        if re.match(r'\s*from\s+unittest\s+import', line):
            continue

        result.append(line)

    return "\n".join(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Використання: python migrate_tests.py <файл.py>")
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename, "r", encoding="utf-8") as f:
        source = f.read()

    migrated = migrate_unittest_to_pytest(source)

    backup_name = filename + ".bak"
    with open(backup_name, "w", encoding="utf-8") as f:
        f.write(source)
    print(f"Резервна копія створена: {backup_name}")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(migrated)
    print(f"Файл оновлено для pytest: {filename}")
