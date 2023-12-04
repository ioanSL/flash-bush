import json
import matplotlib.pyplot as plt


if __name__ == "__main__":
    with open("scripts/assets/data_sample1.json", "r") as data_file:
        data = json.load(data_file)
    x_axis = []
    reserve_error_sushi = []
    reserve_error_quick = []
    sushiReserveUSD = []
    sushiReserveETH = []
    quickReserveUSD = []
    quickReserveETH = []
    for index, sample in data.items():
        x_axis.append(index)
        reserve_error_sushi.append(sample["SushiSwap"]["pair"]["token0PoolRR"])
        reserve_error_quick.append(sample["QuickSwap"]["pair"]["token0PoolRR"])
        sushiReserveUSD.append(float(sample["SushiSwap"]["pair"]["reserve0"]))
        sushiReserveETH.append(
            float(sample["SushiSwap"]["pair"]["reserveUSD"])
            - float(sample["SushiSwap"]["pair"]["reserve0"])
        )

        quickReserveUSD.append(float(sample["QuickSwap"]["pair"]["reserve0"]))
        quickReserveETH.append(
            float(sample["QuickSwap"]["pair"]["reserveUSD"])
            - float(sample["QuickSwap"]["pair"]["reserve0"])
        )

    fig, ax = plt.subplots()
    ax.plot(x_axis, reserve_error_sushi, label="SushiSwap")
    ax.plot(x_axis, reserve_error_quick, label="QuickSwap")
    ax.legend()
    plt.show()

    fig, ax = plt.subplots()
    ax.plot(x_axis, sushiReserveETH, label="SushiETH")
    ax.plot(x_axis, sushiReserveUSD, label="SushiUSD")
    ax.plot(x_axis, quickReserveETH, label="QuickETH")
    ax.plot(x_axis, quickReserveUSD, label="QuickUSD")
    ax.legend()
    plt.show()
