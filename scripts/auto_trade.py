import token


def flag_operation(return_target, token_price0, token_price1, fee=0.0009):
    borrow = 10000  # €

    if token_price0 < token_price1:
        relation = token_price0 / token_price1
    else:
        relation = token_price1 / token_price0

    while True:
        if borrow >= 3000000:
            return False
        return_current = borrow - (borrow * relation) - (borrow * fee)
        if return_target <= return_current:
            return (borrow, return_current)
        borrow += 10000


if __name__ == "__main__":
    token0 = [2939]
    token1 = [2952]
    rois = 3500
    for i in range(len(token0)):
        res = flag_operation(rois, token0[i], token1[i])
        if res:
            print("token0:{}".format(token0[i]))
            print("token1:{}".format(token1[i]))
            print("Optimal borrow amount: {}".format(res[0]))
            print("Fee to pay: {}".format(res[0] * 0.0009))
            print("ROI: {}".format(res[1]))
            print("****************************")
        else:
            print("token0:{}".format(token0[i]))
            print("token1:{}".format(token1[i]))
            print("Transaction reverted!!!")
            print("****************************")
