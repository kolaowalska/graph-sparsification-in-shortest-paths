from ..main import main

def test_smoke():
    assert main(["--smoke"]) == 0
