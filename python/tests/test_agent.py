from openfloor import (
    BotAgent, Envelope, Conversation, Sender,
    GetManifestsEvent, Manifest, Identification,
)


def _make_manifest_with_extra_field() -> Manifest:
    return Manifest.from_dict({
        "identification": {
            "speakerUri": "tag:example.com,2024:test-bot",
            "serviceUrl": "https://example.com/bot",
            "organization": "Test Corp",
            "conversationalName": "TestBot",
            "synopsis": "A test bot",
        },
        "capabilities": [],
        "customVendorField": "custom-value-123",
    })


def test_get_manifests_returns_extra_field_in_manifest():
    """Extra non-standard fields on a manifest must survive a GetManifests round-trip."""
    manifest = _make_manifest_with_extra_field()
    agent = BotAgent(manifest)

    in_envelope = Envelope(
        conversation=Conversation(id="conv:test-123"),
        sender=Sender(speakerUri="tag:example.com,2024:user"),
        events=[GetManifestsEvent()],
    )

    out_envelope = agent.process_envelope(in_envelope)

    publish_events = [e for e in out_envelope.events if e.eventType == "publishManifests"]
    assert len(publish_events) == 1, "Expected exactly one publishManifests event"

    servicing_manifests = publish_events[0].parameters["servicingManifests"]
    assert len(servicing_manifests) == 1, "Expected exactly one servicing manifest"

    manifest_data = servicing_manifests[0].__json__()
    assert "customVendorField" in manifest_data, (
        "Extra field 'customVendorField' was not returned in the manifest response"
    )
    assert manifest_data["customVendorField"] == "custom-value-123"
