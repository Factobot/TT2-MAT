# Project: Toontown Two
# MakeAToon.py
# Created by: Factobot (Storm)

from direct.interval.IntervalGlobal import *
from direct.fsm.FSM import *
from panda3d.core import *

class MakeAToonCamera(FSM):
    def __init__(self, mat):
        FSM.__init__(self, "MakeAToonCamera")
        self.makeAToon = mat
        self.currentCam = None
        
    def enterChooseGenderCamera(self):
        self.currentCam = "choose_gender"
        self.cgIv = base.cam.posHprInterval(2, (-11.59, -19.19, 5.31), (329.74, 350.54, 0.00), blendType='easeOut')
        self.cgIv.start()
        
    def exitChooseGenderCamera(self):
        self.cgIv.finish()
        
    def enterBodyPickCamera(self):
        self.currentCam = "body_pick"
        self.bpIv = base.cam.posHprInterval(3, (-3.74, 3.96, 11.20), (383, 290.56, 0.00), blendType='easeOut')
        self.bpIv.start()
        
    def exitBodyPickCamera(self):
        self.bpIv.finish()
        
    def enterToonPopCamera(self):
        self.currentCam = "toon_pop"
        self.tpcIv = base.cam.posHprInterval(2, (0.42, -20.03, 5.17), (360.00, 360, 0.00), blendType='easeIn')
        self.tpcIv.start()
        
    def exitToonPopCamera(self):
        self.tpcIv.finish()
        
    def enterClothesCamera(self):
        self.currentCam = "cloth_cam"
        self.ccIv = Sequence(
            base.cam.posInterval(2, (3, -9, 3.5), blendType='easeOut'),
            Func(self.makeAToon.ccCamDone)
        )
        self.ccIv.start()
        
    def enterFadeOffCamera(self):
        self.foIv = Sequence(
            base.cam.posInterval(5, (3, -15, 3.5), blendType='easeOut'),
            Func(self.makeAToon.foCamDone)
        )
        self.foIv.start()
