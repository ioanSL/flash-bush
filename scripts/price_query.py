import re
from time import sleep
import yaml
from http import client
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

AMOUNTINUSD = 3000
AMOUNTINETH = 1


class PriceQuery:
    def __init__(self, dex_metadata={}):

        self.clients = {}
        for _, dex in dex_metadata.items():
            sample_transport = RequestsHTTPTransport(
                url=dex["endpoint"],
                verify=True,
                retries=5,
            )
            self.clients[dex["DEX Name"]] = {
                "client": Client(transport=sample_transport),
                "pairs": dex["pairs"],
            }

    def do_pairs_query(self):
        client_response = {}
        for dexName, dex in self.clients.items():
            for pair in dex["pairs"]:
                query = gql(
                    'query { pair(id: "%s") { reserveETH reserveUSD reserve0 reserve1 }}'
                    % pair
                )
                client_response[dexName] = dex["client"].execute(query)
        return client_response

    @staticmethod
    def getAmountOut(amountIn, reserveIn, reserveOut):
        if amountIn > 0 and reserveIn > 0 and reserveOut > 0:
            amountInWithFee = amountIn * 995
            numerator = amountInWithFee * reserveOut
            denominator = (reserveIn * 1000) + amountInWithFee
            return numerator / denominator

    def calculate_reserves(self, query={}):

        for _, pair in query.items():
            reserve0 = float(pair["pair"]["reserve0"])
            reserve1 = float(pair["pair"]["reserve1"])

            reserve0inToken1 = float(pair["pair"]["reserveETH"]) - reserve1
            reserve1inToken0 = float(pair["pair"]["reserveUSD"]) - reserve0

            pair["pair"]["token0PoolRR"] = reserve0 / reserve1inToken0
            pair["pair"]["token1PoolRR"] = reserve1 / reserve0inToken1

        return query

    def flag_for_arbitrage(self, query={}):
        arbitrage_flag = True
        sushiPoolRR = query["SushiSwap"]["pair"]["token0PoolRR"]
        quickPoolRR = query["QuickSwap"]["pair"]["token0PoolRR"]

        if sushiPoolRR > 1 and quickPoolRR > 1:
            arbitrage_flag = False
        elif sushiPoolRR < 1 and quickPoolRR < 1:
            arbitrage_flag = False

        sushi = query["SushiSwap"]
        quick = query["QuickSwap"]

        if arbitrage_flag:
            arbitrage_flag = self.calculate_roi(sushi, quick)

        return arbitrage_flag

    def calculate_roi(self, sushi, quick):
        sushi_absolute_error = abs(1 - sushi["pair"]["token0PoolRR"])
        quick_absolute_error = abs(1 - quick["pair"]["token0PoolRR"])
        roi = False
        if sushi_absolute_error > quick_absolute_error:
            # Start trade on Sushi
            if sushi["pair"]["token0PoolRR"] > 1:
                # ETH Flash loan
                sushiAmountOut = self.getAmountOut(
                    amountIn=AMOUNTINETH,
                    reserveIn=float(sushi["pair"]["reserve1"]),
                    reserveOut=float(sushi["pair"]["reserve0"]),
                )
                quickAmountOut = self.getAmountOut(
                    amountIn=sushiAmountOut,
                    reserveIn=float(quick["pair"]["reserve0"]),
                    reserveOut=float(quick["pair"]["reserve1"]),
                )
                flashReturn = AMOUNTINETH + AMOUNTINETH * 0.0009
                if quickAmountOut > flashReturn:
                    roi = True

            else:
                # USD Flash loan
                sushiAmountOut = self.getAmountOut(
                    amountIn=AMOUNTINUSD,
                    reserveIn=float(sushi["pair"]["reserve0"]),
                    reserveOut=float(sushi["pair"]["reserve1"]),
                )
                quickAmountOut = self.getAmountOut(
                    amountIn=sushiAmountOut,
                    reserveIn=float(quick["pair"]["reserve1"]),
                    reserveOut=float(quick["pair"]["reserve0"]),
                )
                if quickAmountOut > (AMOUNTINUSD + AMOUNTINUSD * 0.0009):
                    roi = True
        else:
            # Start trade on Quick
            if quick["pair"]["token0PoolRR"] > 1:
                # ETH Flash loan
                quickAmountOut = self.getAmountOut(
                    amountIn=AMOUNTINETH,
                    reserveIn=float(quick["pair"]["reserve1"]),
                    reserveOut=float(quick["pair"]["reserve0"]),
                )
                sushiAmountOut = self.getAmountOut(
                    amountIn=quickAmountOut,
                    reserveIn=float(sushi["pair"]["reserve0"]),
                    reserveOut=float(sushi["pair"]["reserve1"]),
                )
                flashReturn = AMOUNTINETH + AMOUNTINETH * 0.0009
                if sushiAmountOut > flashReturn:
                    roi = True
            else:
                # USD Flash loan
                quickAmountOut = self.getAmountOut(
                    amountIn=AMOUNTINUSD,
                    reserveIn=float(quick["pair"]["reserve0"]),
                    reserveOut=float(quick["pair"]["reserve1"]),
                )
                sushiAmountOut = self.getAmountOut(
                    amountIn=quickAmountOut,
                    reserveIn=float(sushi["pair"]["reserve1"]),
                    reserveOut=float(sushi["pair"]["reserve0"]),
                )
                if sushiAmountOut > (AMOUNTINUSD + AMOUNTINUSD * 0.0009):
                    roi = True
        return roi

    def setup_trade(self):
        # Query Pair data
        query = self.do_pairs_query()
        # Calculate Swap Price
        pass

    def trigger_trade(self):
        # Perform trade. Smart contract interface
        pass


if __name__ == "__main__":
    with open("scripts/assets/dex_data.yaml") as dex_metadata:
        pairs = yaml.safe_load(dex_metadata)
    Q = PriceQuery(pairs)
    querry_count = 0
    count = 0
    while True:
        query = Q.do_pairs_query()
        query = Q.calculate_reserves(query)
        print(querry_count, query)
        querry_count += 1
        if Q.flag_for_arbitrage(query):
            count += 1
            print("{} TRADE MOTHERFUCKER!!!!!".format(count))
            print("--------------------------------------")
            break
        sleep(1)
