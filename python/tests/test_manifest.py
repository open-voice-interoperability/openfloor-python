import pytest
from dataclasses import dataclass
from openfloor.manifest import Identification, Manifest, Capability, SupportedLayers
from openfloor.json_serializable import JsonSerializableDataclass
from openfloor.dialog_event import Span, Token, Feature, DialogEvent
from openfloor.envelope import (
    Schema, Conversant, Conversation, Sender, To, Event, Envelope, Payload,
)


def test_identification_from_dict_ignores_extra_keys():
    data = {
        "speakerUri": "foo",
        "serviceUrl": "bar",
        "organization": "org",
        "conversationalName": "name",
        "synopsis": "syn",
        "extra1": "ignored",
        "extra2": "ignored",
    }

    ident = Identification.from_dict(data)
    assert ident.department == None

    # the unknown keys should be preserved and re-emitted during serialization
    serialized = ident.__json__()
    assert serialized["extra1"] == "ignored"
    assert serialized["extra2"] == "ignored"

def test_manifest_from_dict_with_unknown_fields_and_capabilities():
    data = {
        "identification": {
            "speakerUri": "foo",
            "serviceUrl": "bar",
            "organization": "org",
            "conversationalName": "name",
            "synopsis": "syn",
            "department": "dept"
        },
        "capabilities": [
            {"keyphrases": ["a"], "descriptions": ["b"], "unknown": 123}
        ],
        "extra_root": True,
    }

    manifest = Manifest.from_dict(data)
    assert manifest.identification.department == "dept"
    # capability should be created and silently preserve its unknown key
    assert isinstance(manifest.capabilities[0], Capability)
    assert not hasattr(manifest.capabilities[0], "unknown")
    # unknown keys should be preserved and re-emitted during serialization
    serialized = manifest.__json__()
    assert serialized["extra_root"] is True
    cap_serialized = manifest.capabilities[0].__json__()
    assert cap_serialized["unknown"] == 123


def test_generic_dataclass_from_dict_ignores_extras():
    @dataclass
    class Dummy(JsonSerializableDataclass):
        x: int
        y: str

    payload = {"x": 1, "y": "hello", "z": 3.14}
    obj = Dummy.from_dict(payload)
    assert obj.x == 1
    assert obj.y == "hello"
    # ensure unknown field was not set as a regular attribute
    assert not hasattr(obj, "z")


# ---------------------------------------------------------------------------
# Minimal valid dicts for every JsonSerializableDataclass subclass, each with
# an extra key that must be silently preserved by from_dict.
# ---------------------------------------------------------------------------

_IDENTIFICATION_DICT = {
    "speakerUri": "uri",
    "serviceUrl": "url",
    "organization": "org",
    "conversationalName": "name",
    "synopsis": "syn",
}


@pytest.mark.parametrize("cls, data", [
    (Identification, {**_IDENTIFICATION_DICT, "_extra": True}),
    (SupportedLayers, {"input": ["text"], "output": ["text"], "_extra": True}),
    (Capability, {"keyphrases": ["k"], "descriptions": ["d"], "_extra": True}),
    (Manifest, {
        "identification": _IDENTIFICATION_DICT,
        "capabilities": [],
        "_extra": True,
    }),
    (Span, {"startOffset": "PT1S", "_extra": True}),
    (Token, {"value": "hello", "_extra": True}),
    (Feature, {"mimeType": "text/plain", "_extra": True}),
    (DialogEvent, {"speakerUri": "uri", "span": {"startOffset": "PT1S"}, "_extra": True}),
    (Schema, {"version": "1.1.0", "_extra": True}),
    (Conversant, {"identification": _IDENTIFICATION_DICT, "_extra": True}),
    (Conversation, {"id": "conv:1", "_extra": True}),
    (Sender, {"speakerUri": "uri", "_extra": True}),
    (To, {"speakerUri": "uri", "_extra": True}),
    (Event, {"eventType": "utterance", "_extra": True}),
    (Envelope, {
        "sender": {"speakerUri": "uri"},
        "conversation": {"id": "conv:1"},
        "_extra": True,
    }),
    (Payload, {
        "openFloor": {
            "sender": {"speakerUri": "uri"},
            "conversation": {"id": "conv:1"},
        },
        "_extra": True,
    }),
], ids=lambda v: v.__name__ if isinstance(v, type) else "")
def test_from_dict_ignores_extra_keys(cls, data):
    """Every JsonSerializableDataclass.from_dict must silently preserve unknown keys
    in _undefined_extras and re-emit them during serialization."""
    obj = cls.from_dict(data)
    # Extra key must not become a regular attribute
    assert not hasattr(obj, "_extra"), (
        f"{cls.__name__}.from_dict stored '_extra' as a regular attribute instead of in _undefined_extras"
    )
    # Extra key must be preserved in _undefined_extras
    assert hasattr(obj, "_undefined_extras"), (
        f"{cls.__name__}.from_dict did not set _undefined_extras"
    )
    assert obj._undefined_extras == {"_extra": True}, (
        f"{cls.__name__}._undefined_extras has wrong content: {obj._undefined_extras}"
    )
    # Extra key must appear in JSON serialization output
    serialized = obj.__json__()
    assert "_extra" in serialized, (
        f"{cls.__name__}.__json__() did not re-emit the '_extra' key"
    )
    assert serialized["_extra"] is True


def test_json_round_trip_preserves_complex_extras():
    """Verify that complex, nested undefined extras survive a full
    JSON serialization round-trip: dict -> from_dict -> to_json -> from_json."""
    import json
    import copy

    input_dict = {
        "identification": {
            "speakerUri": "urn:example:bot",
            "serviceUrl": "https://example.com/bot",
            "organization": "Acme Corp",
            "conversationalName": "Acme Bot",
            "synopsis": "A helpful bot",
            "x-vendor-meta": {
                "region": "us-east-1",
                "tags": ["production", "v2"],
                "limits": {"rps": 100, "burst": 200},
            },
        },
        "capabilities": [
            {
                "keyphrases": ["weather"],
                "descriptions": ["Get the weather"],
                "x-custom-scoring": [0.9, 0.1, {"nested": True}],
            }
        ],
        "x-deployment": {
            "cluster": "prod-3",
            "replicas": 5,
            "features": {"canary": True, "ab-test": [1, 2, 3]},
        },
    }

    # from_dict mutates data in-place, so keep a pristine copy for comparison
    expected = copy.deepcopy(input_dict)

    # from_dict -> to_json -> parse back to plain dict
    manifest = Manifest.from_dict(input_dict)
    json_str = manifest.to_json()
    output_dict = json.loads(json_str)

    # The top-level complex extra must survive intact
    assert output_dict["x-deployment"] == expected["x-deployment"]

    # The nested extra inside identification must survive
    assert output_dict["identification"]["x-vendor-meta"] == \
        expected["identification"]["x-vendor-meta"]

    # The nested extra inside the capability must survive
    assert output_dict["capabilities"][0]["x-custom-scoring"] == \
        expected["capabilities"][0]["x-custom-scoring"]

    # Defined fields must also be correct
    assert output_dict["identification"]["speakerUri"] == "urn:example:bot"
    assert output_dict["capabilities"][0]["keyphrases"] == ["weather"]
