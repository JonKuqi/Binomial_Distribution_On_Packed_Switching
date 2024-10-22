import math as math
from scipy.stats import poisson


class BinomialDistribution:

    @staticmethod
    def probability(n, k, p, mode):

        isPoisson = False
        if n > 20 and p < 0.05:
            isPoisson = True

        #mode -> = < > <= >=
        if mode == "=":
            return BinomialDistribution.calculateOneBinomialTerm(n, k, p)

        elif mode == "<" or mode == "<=":

            inverse = False
            if (n - k) < k: inverse = True

            if mode == "<":
                if inverse:
                    return 1 - BinomialDistribution.calculateMultipleTerms(n, p, k, n, isPoisson)
                else:
                    return BinomialDistribution.calculateMultipleTerms(n, p, 0, k - 1, isPoisson)

            if mode == "<=":
                if inverse:
                    return 1 - BinomialDistribution.calculateMultipleTerms(n, p, k + 1, 40, isPoisson)
                else:
                    return BinomialDistribution.calculateMultipleTerms(n, p, 0, k, isPoisson)

        else:
            inverse = False
            if (n - k) > k: inverse = True

            if mode == ">":
                if inverse:
                    return 1 - BinomialDistribution.calculateMultipleTerms(n, p, 0, k, isPoisson)
                else:
                    return BinomialDistribution.calculateMultipleTerms(n, p, k + 1, n, isPoisson)

            if mode == ">=":
                if inverse:
                    print("Here")
                    return 1 - BinomialDistribution.calculateMultipleTerms(n, p, 0, k - 1, isPoisson)
                else:
                    return BinomialDistribution.calculateMultipleTerms(n, p, k, n, isPoisson)



    @staticmethod
    def calculateMultipleTerms(n, p, start, finish, isPoisson):
        sumOfTerms = 0

        if isPoisson:
            for i in range(start, finish + 1):
                sumOfTerms += BinomialDistribution.calculateOnePoissonTerm(n, i, p)
            return sumOfTerms

        for i in range(start, finish + 1):
            sumOfTerms += BinomialDistribution.calculateOneBinomialTerm(n, i, p)

        return sumOfTerms


    @staticmethod
    def calculateOneBinomialTerm(n, k, p):

        #(n - k)
        binomialCoefficient = math.comb(n, k)

        # (n - k) * p^k * q^n-k
        return binomialCoefficient * pow(p, k) * pow(1-p, n-k)

    @staticmethod
    def calculateOnePoissonTerm(n, k, p):
        l = n * p
        return (l ** k) * math.exp(-l) / math.factorial(k)

    @staticmethod
    def calculateOnePoissonTermUsingSciPy(n, k, p):
        return poisson.pmf(k, n * p)



