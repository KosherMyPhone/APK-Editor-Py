import json
from dataclasses import dataclass

from apk_editor.apk import DecompiledAPK


def arsc_id_to_hex(type_id, entry_id):
    """
    Convert a resource ID to a hex string.

    Args:
        type_id (int): The type ID. For example, if the type is drawable, find the type ID for drawable. For example: 8. It will vary per APK.
        entry_id (int): The entry ID. Within the drawable type, find the entry ID for the specific drawable. For example: 125.
    """
    hex_str = f"0x7f{type_id:02x}{entry_id:04x}"
    return hex_str.format(type_id, entry_id)


@dataclass
class ARSCType:
    name: str
    id: int
    config: dict
    entries: dict[str, dict]
    entries_list: list[dict]  # cuz what if we need to add new entries


@dataclass
class ARSCSpec:
    name: str
    id: int
    types: dict[tuple, ARSCType]

    def get_type(self, config: dict) -> ARSCType:
        return self.types[tuple(sorted(config.items()))]

    @property
    def default(self) -> ARSCType:
        return self.get_type({})


class ARSC:
    def __init__(self, apk: DecompiledAPK) -> None:
        self.decompiled_apk = apk
        self.arsc_path = self.decompiled_apk.resources_arsc
        self.specs: dict[str, ARSCSpec] = {}
        with self.arsc_path.open("rb") as f:
            self.arsc_data = json.load(f)

        specs = self.arsc_data["packages"][0]["specs"]

        for spec in specs:
            if not spec["types"]:
                continue  # apkanalyzer told me its 'attr'. But apkeditor gives me no info, so I skip it.
                # empty anyway so should be fine
            spec_name = spec["types"][0]["name"]
            types = {}
            for type_ in spec["types"]:
                type_config = tuple(sorted(type_["config"].items()))
                entries: dict[str, dict] = {}
                for entry in type_["entries"]:
                    entries[entry["entry_name"]] = entry
                types[type_config] = ARSCType(
                    type_["name"],
                    type_["id"],
                    type_["config"],
                    entries,
                    type_["entries"],
                )
            self.specs[spec_name] = ARSCSpec(spec_name, spec["spec"]["id"], types)

    def save(self):
        with self.arsc_path.open("w") as f:
            json.dump(self.arsc_data, f)
