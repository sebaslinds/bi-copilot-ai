import pytest
from fastapi.testclient import TestClient

import main
from errors import QueryExecutionError
from scripts.seed_db import seed
from services.query_service import run_query


@pytest.fixture(scope="module", autouse=True)
def seeded_database() -> None:
    seed()


def test_health() -> None:
    client = TestClient(main.app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ask_with_mocked_gemini(monkeypatch: pytest.MonkeyPatch) -> None:
    client = TestClient(main.app)

    monkeypatch.setattr(
        main,
        "generate_sql",
        lambda question: (
            "SELECT product, price * quantity AS revenue "
            "FROM sales ORDER BY revenue DESC LIMIT 3;"
        ),
    )
    monkeypatch.setattr(
        main,
        "generate_insight",
        lambda data: "Top revenue is concentrated in premium computer products.",
    )

    response = client.post("/ask", json={"question": "Top products by revenue"})

    assert response.status_code == 200
    payload = response.json()
    assert set(payload) == {"sql", "data", "insight", "chart"}
    assert payload["data"]
    assert payload["chart"] == {"type": "bar", "x": "product", "y": "revenue"}


def test_run_query_accepts_select() -> None:
    rows = run_query("SELECT product, price * quantity AS revenue FROM sales LIMIT 2;")

    assert len(rows) == 2
    assert {"product", "revenue"} <= set(rows[0])


@pytest.mark.parametrize(
    "sql",
    [
        "DROP TABLE sales;",
        "DELETE FROM sales;",
        "SELECT * FROM sales; DELETE FROM sales;",
        "SELECT * FROM sales -- comment",
    ],
)
def test_run_query_blocks_unsafe_sql(sql: str) -> None:
    with pytest.raises(QueryExecutionError):
        run_query(sql)
