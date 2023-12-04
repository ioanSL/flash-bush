import pytest
import yaml
from scripts.price_query import PriceQuery


@pytest.mark.parametrize(
    ["amountIn", "reserveIn", "reserveOut", "expected_result"],
    [
        # Test 1
        (1, 7103.86, 21600857, 3025)
    ],
)
def test_price_query_get_amount_out(amountIn, reserveIn, reserveOut, expected_result):
    with open("../scripts/assets/dex_data.yaml") as dex_metadata:
        pairs = yaml.safe_load(dex_metadata)
        Q = PriceQuery(pairs)
    assert expected_result == pytest.approx(
        Q.getAmountOut(amountIn, reserveIn, reserveOut), 0.1
    )
