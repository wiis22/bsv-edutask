import pytest
from pymongo import errors

def test_create_video_valid(sut):
    video_data_valid = {
        "url": "https://youtube.com/watch?v=qwerty12345"
        }
    result = sut.create(video_data_valid)
    assert "_id" in result

    # fetched = sut.collection.find_one({"_id": result.inserted_id})
    # assert fetched["url"] == valid_video_data["url"]

def test_create_video_missing_url(sut):
    video_data_missing_url = {}
    with pytest.raises(errors.WriteError):
        sut.create(video_data_missing_url)

def test_create_video_extra_property(sut):
    vide_data_extra_property = {
        "url": "https://youtube.com/watch?v=qwerty12345",
        "extra_property": "extra_value"
        }
    result = sut.create(vide_data_extra_property)
    assert "_id" in result

def test_create_video_wrong_data_type(sut):
    video_data_wrong_type = {
        "url": 123
        }
    with pytest.raises(errors.WriteError):
        sut.create(video_data_wrong_type)

def test_create_video_none_value(sut):
    video_data_none_value = {
        "url": None
        }
    with pytest.raises(errors.WriteError):
        sut.create(video_data_none_value)
