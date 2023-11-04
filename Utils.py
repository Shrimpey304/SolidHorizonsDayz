T = None
K = None

class Utils():
    @staticmethod
    def fetchDecryptedToken(t):
        global T
        T = t

    @staticmethod
    def fetchKey(k):
        global K
        K = k