import pytest
import script


@pytest.mark.asyncio
async def test_script_valid():
    assert await script.main(test="valid") == \
           [{'https://www.python.org/': {'Python': 21, 'and': 20, 'to': 16, 'the': 14, 'for': 13}}]


@pytest.mark.asyncio
async def test_script_invalid():
    assert await script.main(test="valid") == []
