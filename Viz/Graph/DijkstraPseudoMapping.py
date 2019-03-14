from Viz.utils.AnimationUpdate import AnimationUpdate


class DijkstraPseudoMapping:
    def __init__(self):
        self.mapping = AnimationUpdate("Dijkstra.txt")
        self.distanceId = "distID"
        self.prevId = "prevID"
        self.QId = "qID"
        self.minUID = "minUID"
        self.neighbourID = "neighbourID"
        self.altAdditionID = "altAdditionID"
        self.cmpCostID = "cmpCostID"
        self.returnDataID = "returnDataID"

    def initDistAndPrev(self, dist, prev):
        self.mapping.addToUpdateQueue(6)
        self.mapping.addToUpdateQueue(7, data={"lineData": [self.distanceId, "distance: {}".format(dist)]})
        self.mapping.addToUpdateQueue(8, data={"lineData": [self.prevId, "previous: {}".format(prev)]})

    def updateDist(self, dist: dict, source: int):
        self.mapping.addToUpdateQueue(11, data={"lineData": [self.distanceId, "distance: {}".format(dist)]})

    def initQ(self, q):
        self.mapping.addToUpdateQueue(12, data={"lineData": [self.QId, "Q: {}".format(q)]})

    def setMinU(self, minVertex):
        self.mapping.addToUpdateQueue(15, data={"lineData": [self.minUID, "Min U: {}".format(minVertex)]})

    def removeU(self, q, neighbour):
        self.mapping.addToUpdateQueue(16, data={"lineData": [self.QId, "Q: {}".format(q)]})
        self.mapping.addToUpdateQueue(17, data={"lineData": [self.neighbourID, "neighbour: {}".format(neighbour)]})

    def findAltAndCmp(self, uDistance, vDistance, cost):
        self.mapping.addToUpdateQueue(18, data={"lineData": [self.altAdditionID, "{} + {}".format(uDistance, cost)]})
        self.mapping.addToUpdateQueue(19, data={"lineData": [self.cmpCostID, "{} < {}".format(uDistance + cost, vDistance)]})  # Alt = uDist+cost

    def setDistAndPrevToAlt(self, distance, prev):
        self.mapping.addToUpdateQueue(20, data={"lineData": [self.distanceId, "distance: {}".format(distance)]})
        self.mapping.addToUpdateQueue(21, data={"lineData": [self.prevId, "previous: {}".format(prev)]})
        self.mapping.addToUpdateQueue(22)

    def ret(self, dist, prev):
        self.mapping.addToUpdateQueue(23)
        self.mapping.addToUpdateQueue(24)
        self.mapping.addToUpdateQueue(25, data={"lineData": [self.returnDataID, "Distance: {}, Previous: {}".format(dist, prev)]})

    def getUpdates(self):
        return dict(**self.mapping.getUpdates())
