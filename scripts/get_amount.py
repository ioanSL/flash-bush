import web3
import json
import yaml
from price_query import PriceQuery

"""
# Address to Uniswap V2 Router02
address = "0x93bcDc45f7e62f89a8e901DC4A0E2c6C427D9F25"

w3 = web3.Web3(web3.HTTPProvider("https://polygon-rpc.com"))
# Open router and put content into abi
with open("assets/UniswapV2Router02.json") as uniswap_router_abi:
    abi = json.load(uniswap_router_abi)

contract_interface = w3.eth.contract(address=address, abi=abi)

contract_interface.functions.getAmountOut(
    w3.toWei(10, "ether"),  # Flash loan value
    w3.toWei(
        50208558.97727772097779903338050385, "ether"
    ),  # Actually this is dollars so not sure if toWei is the best conversion
    w3.toWei(16625.77024240269462154040618608404, "ether"),  # ETH Reserve
).call()
"""

if __name__ == "__main__":
    with open("assets/dex_data.yaml") as dex_metadata:
        pairs = yaml.safe_load(dex_metadata)
    Q = PriceQuery(pairs)
    print(Q.do_pairs_query())
