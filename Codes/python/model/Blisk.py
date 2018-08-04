import numpy as np

class BliskBase:
    def __init__(self):
        self.SecNum = 0
        self.SecDof = 0

class Blisk(BliskBase):
    pass

class LmpBliskParams(BliskBase):
    def __init__(self):
        super().__init__()
        self.BladMassCoef = 0.0114
        self.BladStifCoef = 430000
        self.BladDampCoef = 1.443
        self.DiskMassCoef = 0.0114
        self.DiskStifCoef = 430000
        self.DiskDampCoef = 1.443
        self.CoupStifCoef = 45430

class LpmBlisk(Blisk):
    def __CreateMassMatrix(self, lpmBliskParams):
        return np.diag(
            np.tile(
                np.append(np.full(lpmBliskParams.SecDof-1,lpmBliskParams.BladMassCoef),
                    lpmBliskParams.DiskMassCoef),
                lpmBliskParams.SecNum))
    
    def __CreateStifMatrix(self, lmpBliskParams):
        sectorStif = np.diag(
            np.append(
                np.insert(
                    np.full(lmpBliskParams.SecDof-2, 2*lmpBliskParams.BladStifCoef),
                    0, lmpBliskParams.BladStifCoef),
                lmpBliskParams.BladStifCoef+lmpBliskParams.DiskStifCoef+2*lmpBliskParams.CoupStifCoef)) + \
            np.diag(np.full(lmpBliskParams.SecDof-1, -lmpBliskParams.BladStifCoef), 1) + \
            np.diag(np.full(lmpBliskParams.SecDof-1, -lmpBliskParams.BladStifCoef), -1)
        wholeStif = np.kron(np.identity(lmpBliskParams.SecNum), sectorStif)
        for i in range(lmpBliskParams.SecNum):
                wholeStif[(i+1)*lmpBliskParams.SecDof-1,((i+1)%lmpBliskParams.SecNum+1)*lmpBliskParams.SecDof-1] = -lmpBliskParams.CoupStifCoef
                wholeStif[(i+1)*lmpBliskParams.SecDof-1,((i-1)%lmpBliskParams.SecNum+1)*lmpBliskParams.SecDof-1] = -lmpBliskParams.CoupStifCoef
        return wholeStif

    def __CreateDampMatrix(self, lpmBliskParams):
        return np.diag(
            np.tile(
                np.append(np.full(lpmBliskParams.SecDof-1,lpmBliskParams.BladDampCoef),
                    lpmBliskParams.DiskDampCoef),
                lpmBliskParams.SecNum))

    def __init__(self, lpmBliskParams):
        self.Mass = self.__CreateMassMatrix(lpmBliskParams)
        self.Stif = self.__CreateStifMatrix(lpmBliskParams)
        self.Damp = self.__CreateDampMatrix(lpmBliskParams)

print(-1%3)
params = LmpBliskParams()
params.SecNum = 3
params.SecDof = 2
params.BladMassCoef = 0.0114
params.BladStifCoef = 430000
params.BladDampCoef = 1.443
params.DiskMassCoef = 0.0128
params.DiskStifCoef = 560000
params.DiskDampCoef = 1.780
params.CoupStifCoef = 45430
blisk = LpmBlisk(params)
print(blisk.Mass)
print(blisk.Stif)
print(blisk.Damp)
