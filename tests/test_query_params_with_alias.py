from typing import Literal
from fastapi import FastAPI, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

app = FastAPI()

class FilterParams(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal['created_at', 'updated_at'] = 'created_at'
    tags: list[str] = []

@app.get('/items/')
async def read_items(filter_query: FilterParams = Query()):
    return filter_query

client = TestClient(app)

def test_query_params_with_alias():
    # Test with camelCase query parameters
    response = client.get('/items/?offset=1&orderBy=updated_at')
    assert response.status_code == 200
    data = response.json()
    assert data["limit"] == 100
    assert data["offset"] == 1
    assert data["orderBy"] == "updated_at"  # This should now work with the fix
    assert data["tags"] == []

    # Test with snake_case query parameters (should not work)
    response = client.get('/items/?offset=1&order_by=updated_at')
    assert response.status_code == 200
    data = response.json()
    assert data["limit"] == 100
    assert data["offset"] == 1
    assert data["orderBy"] == "created_at"  # Should still be default value
    assert data["tags"] == []

if __name__ == "__main__":
    test_query_params_with_alias()
    print("All tests passed!")