from MainShortcuts2 import ms
from xml.etree import ElementTree
KEY_NAME = "{http://schemas.android.com/apk/res/android}name"
MANIFEST_PATH = ms.MAIN_DIR + "/app/src/main/AndroidManifest.xml"
exist_perms: set[str] = set()
main_et = ElementTree.parse(MANIFEST_PATH)
new_perms: set[str] = set(ms.json.read(ms.MAIN_DIR + "/android-perms.json"))
ElementTree.register_namespace("android", "http://schemas.android.com/apk/res/android")


def import_from_xml(path: ElementTree.ElementTree | str):
  if isinstance(path, ElementTree.ElementTree):
    et = path.getroot()
  else:
    et = ElementTree.parse(path).getroot()
  for perm in et.findall("uses-permission"):
    name: str = perm.get(KEY_NAME)
    if name:
      if name.startswith("android.permission."):
        yield name


for name in import_from_xml(main_et):
  exist_perms.add(name)
main_root = main_et.getroot()
edited = False
for name in new_perms:
  if name not in exist_perms:
    print("Новое разрешение:", name)
    el = ElementTree.Element("uses-permission", {KEY_NAME: name, "android:required": "false"})
    main_root.append(el)
    edited = True
if edited:
  main_et.write(MANIFEST_PATH, "utf-8", True)
