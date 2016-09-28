# Project: Toontown Two
# MakeAToon.py
# Created by: Factobot (Storm)

from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from panda3d.core import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.toon import ToonDNA
from direct.fsm.FSM import *

HeadTypes = ['ls',
 'ss',
 'sl',
 'll']

class MakeAToonSpaceGUI(FSM):
    maxHeadIndex = 3
    maxSpeciesIndex = len(ToonDNA.toonSpeciesTypes)
    maxBodyIndex = len(ToonDNA.toonTorsoTypes)
    maxLegIndex = len(ToonDNA.toonLegTypes)
    def __init__(self, mat):
        FSM.__init__(self, "MakeAToonSpaceGUI")
        self.makeAToon = mat
        self.headIndex = -1
        self.speciesIndex = -1
        self.bodyIndex = -1
        self.legIndex = -1
    
    def load(self, target):
        self.target = target
        self.guiNode = render.attachNewNode("MATSpaceGUI")
        self.__loadVirtualTexture()
        self.__loadGui()
        
    def unload(self):
        self.vt__cam.removeNode()
        self.vt__render.removeNode()
        self.paper.removeNode()
        self.guiNode.removeNode()
        self.rightNode.removeNode()
        self.leftNode.removeNode()
        self.paperNode.removeNode()
        self.nextButton.removeNode()
        self.backButton.removeNode()
        
    def prepareToon(self):
        self.toon = self.makeAToon.toon
        self.species = s = self.toon.style.head[0]
        self.speciesIndex = ToonDNA.toonSpeciesTypes.index(s)
        self.headIndex = ToonDNA.toonHeadTypes.index(self.toon.style.head) - ToonDNA.getHeadStartIndex(s)
        self.bodyIndex = ToonDNA.toonTorsoTypes.index(self.toon.style.torso) % 3
        self.legIndex = ToonDNA.toonLegTypes.index(self.toon.style.legs)
        self.colorList = self.getGenderColorList(self.toon.style.gender)
        self.tops = ToonDNA.getRandomizedTops(self.toon.style.gender,
                                              tailorId=ToonDNA.MAKE_A_TOON)
        self.bottoms = ToonDNA.getRandomizedBottoms(
               self.toon.style.gender, tailorId=ToonDNA.MAKE_A_TOON)
        self.topChoice = self.tops.index(
            (self.toon.style.topTex, self.toon.style.topTexColor,
             self.toon.style.sleeveTex, self.toon.style.sleeveTexColor))
        self.bottomChoice = self.bottoms.index(
            (self.toon.style.botTex, self.toon.style.botTexColor))
        try:
            self.headColorIndex = self.colorList.index(self.toon.style.headColor)
            self.armColorIndex = self.colorList.index(self.toon.style.armColor)
            self.legColorIndex = self.colorList.index(self.toon.style.legColor)
        except:
            self.headColorIndex = 1
            self.armColorIndex = 1
            self.legColorIndex = 1
        self.__loadToon()
        
    def enterClean(self):
        self.__resetArrows()
        self.rightNode.hide()
        self.leftNode.hide()
        self.backButton.hide()
        self.nextButton.hide()
        
    def enterBodyGUI(self):
        self.rightNode.show()
        self.leftNode.show()
        self.backButton.show()
        self.nextButton.show()
        self.__resetArrows()
        self.topRightArrow['text'] = TTLocalizer.Species
        self.topRightArrow['command'] = self.__swapSpecies
        self.topRightArrow['extraArgs'] = [1]
        self.topLeftArrow['command'] = self.__swapSpecies
        self.topLeftArrow['extraArgs'] = [-1]
        self.topMidRightArrow['text'] = TTLocalizer.Head
        self.topMidRightArrow['command'] = self.__swapHead
        self.topMidRightArrow['extraArgs'] = [1]
        self.topMidLeftArrow['command'] = self.__swapHead
        self.topMidLeftArrow['extraArgs'] = [-1]
        self.bottomMidRightArrow['text'] = TTLocalizer.Body
        self.bottomMidRightArrow['command'] = self.__swapBody
        self.bottomMidRightArrow['extraArgs'] = [1]
        self.bottomMidLeftArrow['command'] = self.__swapBody
        self.bottomMidLeftArrow['extraArgs'] = [-1]
        self.bottomRightArrow['text'] = TTLocalizer.Legs
        self.bottomRightArrow['command'] = self.__swapLegs
        self.bottomRightArrow['extraArgs'] = [1]
        self.bottomLeftArrow['command'] = self.__swapLegs
        self.bottomLeftArrow['extraArgs'] = [-1]
        
    def exitBodyGUI(self):
        self.__resetArrows()
        self.nextButton.hide()
        self.backButton.hide()
        self.rightNode.hide()
        self.leftNode.hide()
        
    def __resetArrows(self):
        self.topRightArrow['state'] = DGG.NORMAL
        self.topMidRightArrow['state'] = DGG.NORMAL
        self.bottomRightArrow['state'] = DGG.NORMAL
        self.bottomMidRightArrow['state'] = DGG.NORMAL
        self.topLeftArrow['state'] = DGG.NORMAL
        self.topMidLeftArrow['state'] = DGG.NORMAL
        self.bottomLeftArrow['state'] = DGG.NORMAL
        self.bottomMidLeftArrow['state'] = DGG.NORMAL
        
    def __swapSpecies(self, offset):
        length = len(ToonDNA.toonSpeciesTypes)
        self.speciesIndex = (self.speciesIndex+offset) % length
        self.species = ToonDNA.toonSpeciesTypes[self.speciesIndex]
        headList = ToonDNA.getHeadList(self.species)
        maxHeadChoice = len(headList) - 1
        if self.speciesIndex == length - 1:
            self.topRightArrow['state'] = DGG.DISABLED
        else:
            self.topRightArrow['state'] = DGG.NORMAL
        if self.speciesIndex == 0:
            self.topLeftArrow['state'] = DGG.DISABLED
        else:
            self.topLeftArrow['state'] = DGG.NORMAL
        if self.headIndex > maxHeadChoice:
            self.headIndex = maxHeadChoice
        self.__updateHead()
        
    def __swapHead(self, offset):
        headList = ToonDNA.getHeadList(self.species)
        length = len(headList)
        self.headIndex = (self.headIndex+offset) % length
        if self.headIndex == length - 1:
            self.topMidRightArrow['state'] = DGG.DISABLED
        else:
            self.topMidRightArrow['state'] = DGG.NORMAL
        if self.headIndex == 0:
            self.topMidLeftArrow['state'] = DGG.DISABLED
        else:
            self.topMidLeftArrow['state'] = DGG.NORMAL
        self.__updateHead()
            
    def __updateHead(self):
        headIndex = ToonDNA.getHeadStartIndex(self.species) + self.headIndex
        newHead = ToonDNA.toonHeadTypes[headIndex]
        self.toon.style.head = newHead
        self.toon.swapToonHead(newHead)
        self.toon.pose('neutral', 0)
        self.toon.swapToonColor(self.toon.style)
        self.toon.clearBin()
        self.toon.stopLookAroundNow()
        self.toon.stopBlink()
        
    def __swapBody(self, offset):
        torsoOffset = 0
        if self.toon.style.gender == 'm':
            length = len(ToonDNA.toonTorsoTypes[:3])
        else:
            length = len(ToonDNA.toonTorsoTypes[3:6])
            if self.toon.style.torso[1] == 'd':
                torsoOffset = 3
        self.bodyIndex = (self.bodyIndex+offset) % length
        if self.bodyIndex == length - 1:
            self.bottomMidRightArrow['state'] = DGG.DISABLED
        else:
            self.bottomMidRightArrow['state'] = DGG.NORMAL
        if self.bodyIndex == 0:
            self.bottomMidLeftArrow['state'] = DGG.DISABLED
        else:
            self.bottomMidLeftArrow['state'] = DGG.NORMAL
        torso = ToonDNA.toonTorsoTypes[torsoOffset+self.bodyIndex]
        self.toon.style.torso = torso
        self.toon.swapToonTorso(torso)
        self.toon.pose('neutral', 0)
        self.toon.swapToonColor(self.toon.style)
        self.toon.clearBin()
        self.toon.stopLookAroundNow()

    def __swapLegs(self, offset):
        length = len(ToonDNA.toonLegTypes)
        self.legIndex = (self.legIndex+offset) % length
        if self.legIndex == length - 1:
            self.bottomRightArrow['state'] = DGG.DISABLED
        else:
            self.bottomRightArrow['state'] = DGG.NORMAL
        if self.legIndex == 0:
            self.bottomLeftArrow['state'] = DGG.DISABLED
        else:
            self.bottomLeftArrow['state'] = DGG.NORMAL
        newLeg = ToonDNA.toonLegTypes[self.legIndex]
        self.toon.style.legs = newLeg
        self.toon.swapToonLegs(newLeg)
        self.toon.pose('neutral', 0)
        self.toon.swapToonColor(self.toon.style)
        
    def __loadGui(self):
        self.rightNode = base.a2dTopRight.attachNewNode("MATGUI_RN")
        self.rightNode.hide()
        self.leftNode = base.a2dTopLeft.attachNewNode("MATGUI_LN")
        self.leftNode.hide()
        self.paperNode = render.attachNewNode("MATGUI_PPN")
        self.paperNode.setPos(self.paper.getPos())
        self.paperNode.setHpr(self.paper.getHpr())
        self.paperNode.setY(-0.05)
        self.__loadArrows()
        self.__loadNavigators()
        
    def __loadNavigators(self):
        self.nextButton = DirectButton(
            image = loader.loadTexture("stage_3/maps/t2_gui_mat_pencil.png"),
            relief = None,
            parent = base.a2dBottomRight,
            pos = (-0.15,0,0.15),
            scale = 0.1,
            command = self.makeAToon.handleNext
        )
        self.nextButton.setTransparency(TransparencyAttrib.MAlpha)
        self.nextButton.hide()
        self.backButton = DirectButton(
            image = loader.loadTexture("stage_3/maps/t2_gui_mat_eraser.png"),
            relief = None,
            parent = base.a2dBottomRight,
            pos = (-0.4,0,0.15),
            scale = 0.1,
            command = self.makeAToon.handlePrev
        )
        self.backButton.setTransparency(TransparencyAttrib.MAlpha)
        self.backButton.hide()
        
    def makeFancyText(self, **kw):
        return OnscreenText(
            font=loader.loadFont('sebastiana.otf'),
            parent = self.paperNode,
            **kw
        )
    
    def getToonSpecies(self):
        return TTLocalizer.AnimalToSpecies[ToonDNA.getSpeciesName(self.makeAToon.toon.style.head)]
        
    def getToonBody(self):
        return  str(self.makeAToon.toon.style.torso)
        
    def __loadArrows(self):
        self.topRightArrow = self.makeArrow(text=TTLocalizer.Species, pos=(-0.3,0,-0.4), parent=self.rightNode)
        self.topMidRightArrow = self.makeArrow(text=TTLocalizer.Head, pos=(-0.3,0,-0.7), parent=self.rightNode)
        self.bottomRightArrow = self.makeArrow(text=TTLocalizer.Legs, pos=(-0.3,0,-1.3), parent=self.rightNode)
        self.bottomMidRightArrow = self.makeArrow(text=TTLocalizer.Body, pos=(-0.3,0,-1), parent=self.rightNode)
        self.topLeftArrow = self.makeArrow(1, pos=(0.3,0,-0.4), parent=self.leftNode)
        self.topMidLeftArrow = self.makeArrow(1, pos=(0.3,0,-0.7), parent=self.leftNode)
        self.bottomMidLeftArrow = self.makeArrow(1, pos=(0.3,0,-1), parent=self.leftNode)
        self.bottomLeftArrow = self.makeArrow(1, pos=(0.3,0,-1.3), parent=self.leftNode)
        
    def enterColorGUI(self):
        self.backButton.show()
        self.nextButton.show()
        self.rightNode.show()
        self.leftNode.show()
        self.topRightArrow['command'] = self.__swapAllColor
        self.topRightArrow['text'] = TTLocalizer.ColorAll
        self.topLeftArrow['command'] = self.__swapAllColor
        self.topMidRightArrow['command'] = self.__swapHeadColor
        self.topMidLeftArrow['command'] = self.__swapHeadColor
        self.bottomMidRightArrow['text'] = TTLocalizer.Arms
        self.bottomMidRightArrow['command'] = self.__swapArmColor
        self.bottomMidLeftArrow['command'] = self.__swapArmColor
        self.bottomRightArrow['command'] = self.__swapLegsColor
        self.bottomLeftArrow['command'] = self.__swapLegsColor
        
    def exitColorGUI(self):
        self.__resetArrows()
        self.backButton.hide()
        self.nextButton.hide()
        self.rightNode.hide()
        self.leftNode.hide()
        
    def getGenderColorList(self, gender):
        if gender == 'm':
            return ToonDNA.defaultBoyColorList
        else:
            return ToonDNA.defaultGirlColorList
        
    def __swapAllColor(self, offset):
        length = len(self.colorList)
        choice = (self.headColorIndex+offset) % length
        self.__swapHeadColor(offset)
        oldArmColorIndex = self.colorList.index(self.toon.style.armColor)
        oldLegColorIndex = self.colorList.index(self.toon.style.legColor)
        self.__swapArmColor(choice - oldArmColorIndex)
        self.__swapLegsColor(choice - oldLegColorIndex)
        if choice == length - 1:
            self.topRightArrow['state'] = DGG.DISABLED
            self.topMidRightArrow['state'] = DGG.DISABLED
            self.bottomRightArrow['state'] = DGG.DISABLED
            self.bottomMidRightArrow['state'] = DGG.DISABLED
        else:
            self.topRightArrow['state'] = DGG.NORMAL
            self.topMidRightArrow['state'] = DGG.NORMAL
            self.bottomRightArrow['state'] = DGG.NORMAL
            self.bottomMidRightArrow['state'] = DGG.NORMAL
        if choice == 0:
            self.topLeftArrow['state'] = DGG.DISABLED
            self.topMidLeftArrow['state'] = DGG.DISABLED
            self.bottomLeftArrow['state'] = DGG.DISABLED
            self.bottomMidLeftArrow['state'] = DGG.DISABLED
        else:
            self.topLeftArrow['state'] = DGG.NORMAL
            self.topMidLeftArrow['state'] = DGG.NORMAL
            self.bottomLeftArrow['state'] = DGG.NORMAL
            self.bottomMidLeftArrow['state'] = DGG.NORMAL
        
    def __swapHeadColor(self, offset):
        length = len(self.colorList)
        self.headColorIndex = (self.headColorIndex+offset) % length
        newColor = self.colorList[self.headColorIndex]
        self.toon.style.headColor = newColor
        self.toon.swapToonColor(self.toon.style)
        if self.headColorIndex == length - 1:
            self.topMidRightArrow['state'] = DGG.DISABLED
        else:
            self.topMidRightArrow['state'] = DGG.NORMAL
        if self.headColorIndex == 0:
            self.topMidLeftArrow['state'] = DGG.DISABLED
        else:
            self.topMidLeftArrow['state'] = DGG.NORMAL

    def __swapArmColor(self, offset):
        length = len(self.colorList)
        self.armColorIndex = (self.armColorIndex+offset) % length
        newColor = self.colorList[self.armColorIndex]
        self.toon.style.armColor = newColor
        self.toon.swapToonColor(self.toon.style)
        if self.armColorIndex == length - 1:
            self.bottomMidRightArrow['state'] = DGG.DISABLED
        else:
            self.bottomMidRightArrow['state'] = DGG.NORMAL
        if self.armColorIndex == 0:
            self.bottomMidLeftArrow['state'] = DGG.DISABLED
        else:
            self.bottomMidLeftArrow['state'] = DGG.NORMAL

    def __swapLegsColor(self, offset):
        length = len(self.colorList)
        self.legColorIndex = (self.legColorIndex+offset) % length
        newColor = self.colorList[self.legColorIndex]
        self.toon.style.legColor = newColor
        self.toon.swapToonColor(self.toon.style)
        if self.legColorIndex == length - 1:
            self.bottomRightArrow['state'] = DGG.DISABLED
        else:
            self.bottomRightArrow['state'] = DGG.NORMAL
        if self.armColorIndex == 0:
            self.bottomLeftArrow['state'] = DGG.DISABLED
        else:
            self.bottomLeftArrow['state'] = DGG.NORMAL
            
        
    def makeArrow(self, invert = 0, **kw):
        bt = DirectButton(
            image = (loader.loadTexture("stage_3/maps/arrow.png"), loader.loadTexture("stage_3/maps/arrow_hover.png")),
            scale=(0.24,1,0.15),
            relief=None,
            text_font=ToontownGlobals.getToonFont(),
            text_pos=(0,-0.2),
            text_scale=(0.3,0.4),
            text_mayChange = 1,
            **kw
        )
        bt.setTransparency(TransparencyAttrib.MAlpha)
        if invert: 
            bt.setP(180)
            bt.setR(180)
        return bt
        
    def __loadVirtualTexture(self):
        self.paper = self.guiNode.attachNewNode(CardMaker('background').generate())
        self.paper.setTexture(loader.loadTexture("stage_3/maps/paper.png"))
        self.paper.setTwoSided(1)
        self.paper.setPos(-8,45,-4)
        self.paper.setScale(15)
        self.vt__altBuffer = base.win.makeTextureBuffer("toonVirCam", 1024, 1024)
        self.vt__render = NodePath("toonVirRender")
        self.vt__cam = base.makeCamera(self.vt__altBuffer)
        self.vt__cam.reparentTo(render)
        self.vt__cam.setPos(0,25,3.4)
        self.target.setTexture(self.vt__altBuffer.getTexture(), 1)
        
    def __loadToon(self):
        if self.makeAToon.toon:
            toon = self.makeAToon.toon
            toon.reparentTo(self.guiNode)
            toon.pose("neutral", 0)
            toon.setPos(0,39,0)
            toon.setHpr(180,0,0)
            
    def enterClothes(self):
        self.rightNode.show()
        self.leftNode.show()
        self.topRightArrow.hide()
        self.topLeftArrow.hide()
        self.bottomRightArrow.hide()
        self.bottomLeftArrow.hide()
        self.topMidRightArrow['text'] = TTLocalizer.TShirt
        self.topMidRightArrow['command'] = self.swapTop
        self.topMidLeftArrow['command'] = self.swapTop
        self.bottomMidRightArrow['text'] = TTLocalizer.Shorts
        self.bottomMidRightArrow['command'] = self.swapBottom
        self.bottomMidLeftArrow['command'] = self.swapBottom
        self.backButton.hide()
        self.nextButton.show()
        
    def exitClothes(self):
        self.rightNode.hide()
        self.leftNode.hide()
        self.__resetArrows()
        
    def swapTop(self, offset):
        length = len(self.tops)
        self.topChoice += offset
        if self.topChoice <= 0:
            self.topChoice = 0
        if self.topChoice == 0:
            self.topMidLeftArrow['state'] = DGG.DISABLED
        else:
            self.topMidLeftArrow['state'] = DGG.NORMAL
        if self.topChoice == len(self.tops) - 1:
            self.topMidRightArrow['state'] = DGG.DISABLED
        else:
            self.topMidRightArrow['state'] = DGG.NORMAL
        if (self.topChoice >= len(self.tops)) or (
            len(self.tops[self.topChoice]) != 4):
            return
        self.toon.style.topTex = self.tops[self.topChoice][0]
        self.toon.style.topTexColor = self.tops[self.topChoice][1]
        self.toon.style.sleeveTex = self.tops[self.topChoice][2]
        self.toon.style.sleeveTexColor = self.tops[self.topChoice][3]
        if self.toon.generateToonClothes() == 1:
            self.toon.loop('neutral', 0)

    def swapBottom(self, offset):
        length = len(self.bottoms)
        self.bottomChoice += offset
        if self.bottomChoice <= 0:
            self.bottomChoice = 0
        if self.bottomChoice == 0:
            self.bottomMidLeftArrow['state'] = DGG.DISABLED
        else:
            self.bottomMidLeftArrow['state'] = DGG.NORMAL
        if self.bottomChoice == len(self.bottoms) - 1:
            self.bottomMidRightArrow['state'] = DGG.DISABLED
        else:
            self.bottomMidRightArrow['state'] = DGG.NORMAL
        if (self.bottomChoice >= len(self.bottoms)) or (
            len(self.bottoms[self.bottomChoice]) != 2):
            return
        self.toon.style.botTex = self.bottoms[self.bottomChoice][0]
        self.toon.style.botTexColor = self.bottoms[self.bottomChoice][1]
        if self.toon.generateToonClothes() == 1:
            self.toon.loop('neutral', 0)
