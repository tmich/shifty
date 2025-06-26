def test_engine_is_sqlite():
    from shifty.infrastructure.db import engine
    assert "sqlite" in str(engine.url)
