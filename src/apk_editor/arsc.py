import json
from dataclasses import dataclass
from pathlib import Path


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
class ArscEntryValue:
    value_type: str
    data: int | str
    name: int | None

    def dict(self):
        data = {"value_type": self.value_type, "data": self.data}
        if self.name:
            data["name"] = self.name
        return data


@dataclass
class ARSCEntry:
    name: str
    value: ArscEntryValue
    id: int

    def dict(self):
        return {
            "entry_name": self.name,
            "value": self.value.dict(),
            "id": self.id,
        }


@dataclass
class ComplexARSCEntry:
    name: str
    is_complex: bool
    is_weak: bool
    values: list[ArscEntryValue]
    id: int
    parent_id: int | None

    def dict(self):
        data = {
            "entry_name": self.name,
            "values": [value.dict() for value in self.values],
            "id": self.id,
        }
        if self.is_complex:
            data["is_complex"] = self.is_complex
        if self.is_weak:
            data["is_weak"] = self.is_weak
        if self.parent_id:
            data["parent_id"] = self.parent_id
        return data


Entry = ARSCEntry | ComplexARSCEntry


@dataclass
class ARSCType:
    name: str
    id: int
    config: dict
    entries: dict[str, Entry]

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "config": self.config,
            "entries": [entry.dict() for entry in self.entries.values()],
        }


@dataclass
class ARSCSpec:
    name: str
    id: int
    spec_flags: list | None
    types: dict[tuple, ARSCType]

    def get_type(self, config: dict) -> ARSCType:
        return self.types[tuple(sorted(config.items()))]

    @property
    def default(self) -> ARSCType:
        return self.get_type({})

    def dict(self):
        data = {
            "spec": {"id": self.id},
            "types": [type_.dict() for type_ in self.types.values()],
        }
        if self.spec_flags:
            data["spec"]["spec_flags"] = self.spec_flags
        return data


class ARSC:
    def __init__(self, arsc_file: Path) -> None:
        self.path = arsc_file
        self.specs: dict[str, ARSCSpec] = {}
        self.empty_specs: list[dict | None] = []
        with self.path.open("rb") as f:
            self.arsc_data = json.load(f)
        self.package_name = self.arsc_data["packages"][0]["package_name"]
        self.package_id = self.arsc_data["packages"][0]["package_id"]
        self.arsc_lib_version = self.arsc_data["arsc_lib_version"]

        specs: list[dict] = self.arsc_data["packages"][0]["specs"]

        for spec in specs:
            if not spec["types"]:
                self.empty_specs.append(spec)
                continue  # apkanalyzer told me its 'attr'. But apkeditor gives me no info, so I skip it.
                # empty anyway so should be fine
            spec_name = spec["types"][0]["name"]
            spec_flags = spec["spec"].get("spec_flags")

            types = {}
            for type_ in spec["types"]:
                type_config = tuple(sorted(type_["config"].items()))
                entries: dict[str, Entry] = {}

                for entry in type_["entries"]:
                    if entry.get("is_complex"):
                        entry_name = entry["entry_name"]
                        is_complex = entry["is_complex"]
                        is_weak = entry.get("is_weak")
                        values = [ArscEntryValue(**value) for value in entry["values"]]
                        id = entry["id"]
                        parent_id = entry.get("parent_id")
                        entries[entry_name] = ComplexARSCEntry(
                            entry_name, is_complex, is_weak, values, id, parent_id
                        )
                    else:
                        entry_name = entry["entry_name"]
                        value_type = entry["value"]["value_type"]
                        data = entry["value"]["data"]
                        value = ArscEntryValue(value_type, data, None)
                        id = entry["id"]
                        entries[entry_name] = ARSCEntry(entry_name, value, id)

                types[type_config] = ARSCType(
                    type_["name"],
                    type_["id"],
                    type_["config"],
                    entries,
                )
            self.specs[spec_name] = ARSCSpec(
                spec_name, spec["spec"]["id"], spec_flags, types
            )

    def save(self):
        arsc = {
            "arsc_lib_version": self.arsc_lib_version,
            "packages": [
                {
                    "arsc_lib_version": self.arsc_lib_version,
                    "package_id": self.package_id,
                    "package_name": self.package_name,
                    "specs": [spec for spec in self.empty_specs]
                    + [spec.dict() for spec in self.specs.values()],
                }
            ],
        }
        with self.path.open("w") as f:
            json.dump(arsc, f)
