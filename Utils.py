K = None

class Utils():
    @staticmethod
    def fetchDecryptedToken(k):
        global K
        K = k