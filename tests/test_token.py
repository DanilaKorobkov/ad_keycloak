from ad_keycloak import TokenSchema


def test__schema__aud_is_always_list():
    builder = TokenSchema()
    expected = {
        "aud": ["a"],
    }

    assert expected == builder.aud_is_list_always({
        "aud": "a",
    })
    assert expected == builder.aud_is_list_always(expected)
