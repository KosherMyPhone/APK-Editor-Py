# APK-Editor-Py
A Python wrapper for [apkeditor.jar](https://github.com/reandroid/apkeditor) helping automate APK Editing.

## Getting Statrted
```
uv pip install git+https://github.com/KosherMyPhone/apk-editor-py
```

Download dependencies from [Google Drive](https://drive.google.com/file/d/1lYmf_OObQOMTWA-KnXkImS9QMtFPT1JR/view?usp=sharing). 
Place apkeditordeps.zip in the root of any drive (personally, I use a USB Flash Drive). Then run:
```
apkeditor-deps local
```

## Usage

```python
from apk_editor.apk import APK

apk = APK('path/to/apk.apk')
decompiled_apk = apk.decompile()
manifest = decompiled_apk.androidmanifest
manifest_content = manifest.read_text()

smali_utils = SmaliUtils(decompiled_apk)
main_activity_path = smali_utils.find_activity_or_class('com.package.MainActivity') # Whatever class you want to find
print(f"Found Activity at {main_activity_path}")
```

More to come later, stay tuned!