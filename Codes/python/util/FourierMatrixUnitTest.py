import unittest
from FourierMatrix import FourierMatrix

class FourierMatrixUnitTest(unittest.TestCase):
    dimension = 12

    def testDimension(self):
        fourierMatrix = FourierMatrix(self.dimension)
        self.assertEqual((self.dimension, self.dimension), fourierMatrix.shape)

    def testDifferentColumnsOrthogonality(self):
        fourierMatrix = FourierMatrix(self.dimension)
        for i in range(self.dimension):
            for j in range(self.dimension):
                if i!=j:
                    self.assertAlmostEqual(0, fourierMatrix[:,i].conj()@fourierMatrix[:,j])

    def testSameColumn(self):
        fourierMatrix = FourierMatrix(self.dimension)
        for i in range(self.dimension):
            self.assertAlmostEqual(self.dimension, fourierMatrix[:,i].conj()@fourierMatrix[:,i])

unittest.main(verbosity=2)

