import math
from queue import Queue

class Points:
    class T:
        payer = None
        points = 0
        timestamp = None

        def __init__(self, payer, points, timestamp):
            self.payer = payer
            self.points = points
            self.timestamp = timestamp

    payerAccounts = None
    q = None
    total = None

    # Initializing the data.
    def __init__(self):
        self.total = 0
        self.payerAccounts = dict()
        self.q = Queue(1000)

    # Adding a given transation.
    def addTransaction(self, transaction):
        kvs = transaction.split(",")
        map = dict()
        for e in kvs:
            kv = e.split(":")
            map[kv[0].strip()] = kv[1].strip()
        payer = map["payer"]
        points = int(map["points"])
        if points == 0:
            return
        timestamp = map["timestamp"]
        self.q.put(Points.T(payer, points, timestamp))
        self.payerAccounts[payer] = points
        self.total += points

    # Spending the points while checking to see if no payerPoints are negative
    def spendPoints(self, points):
        if points <= 0:
            return
        if self.total < points:
            return
        out = dict()
        noTouch = []
        while not self.q.empty() and points > 0:
            t = self.q.get()
            remove = min(points, min(t.points, self.payerAccounts.get(t.payer)))
            if remove != t.points:
                t.points -= remove
                noTouch.append(t)
            self.payerAccounts[t.payer] = self.payerAccounts.get(t.payer) - remove
            self.total -= remove
            out[t.payer] = remove
            points -= remove
            if points == 0:
                break
            if self.q.empty():
                for no in noTouch:
                    self.q.put(no)
                noTouch = []
        for no in noTouch:
            self.q.put(no)
        for k, v in out.items():
            print("payer: " + k + ", points: -" + str(v))

    # Return all payer point balances.
    def allPayerBalances(self):
        for k, v in self.payerAccounts.items():
            print("payer: " + k + ", points: " + str(v))


def main():
    array =  ["payer: DANNON, points: 300, timestamp: 2020-10-31T10:00:00Z",
              "payer: UNILEVER, points: 200, timestamp: 2020-10-31T11:00:00Z",
              "payer: DANNON, points: -200, timestamp: 2020-10-31T15:00:00Z",
              "payer: MILLER COORS, points: 10000, timestamp: 2020-11-01T14:00:00Z",
              "payer: DANNON, points: 1000, timestamp: 2020-11-02T14:00:00Z"]
    t = Points()
    for transaction in array:
        t.addTransaction(transaction)
        t.spendPoints(5000)
        print("-------")
        t.allPayerBalances()

if __name__ == "__main__":
    main()