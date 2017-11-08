### Auto Rig UI ###

import maya.cmds as cmds
import os
from functools import partial
import maya.mel as mel
import AutoRig_JT
import pymel.core as pm

def alignJointChain(List,translateVector,scale,direction):
        
    

    i = 0
    
    ChainParent = List[0].getParent()
    
    pm.parent(List,w=True)

    for Joint in List:
        
        if i < (len(List)-1):

            # create and position a locator in the Z facing direction
        
            locator = pm.spaceLocator()
            
            pm.delete(pm.parentConstraint(Joint,locator,mo=False))
            
            translateValue = pm.getAttr(locator+'.'+translateVector)

            forwardPosition = 5 * scale * direction

            pm.setAttr(locator+'.'+translateVector, (translateValue + forwardPosition))

            # aim constraint 

            pm.delete(pm.aimConstraint(List[i+1], Joint, offset=(0, 0, 0), weight=1, aimVector=(1, 0, 0), upVector=(0, 0, 1),
                             worldUpType="object", worldUpObject=locator))

            pm.makeIdentity(Joint,a=True,r=True)

            pm.parent(List[i+1],Joint)

            pm.delete(locator)
        
        
        i = i + 1


def AutoRig_UI():
    
    if pm.window("AutoRig_JT", q=True, exists = True):
            pm.deleteUI("AutoRig_JT")
    
    windowUI = pm.window("AutoRig_JT",titleBarMenu=True, menuBar=True, mxb = False, t="AutoRig_JT", w = 300, h = 500, sizeable = False, bgc=[0.15,0.15,0.15],maximizeButton=False)
	
    pm.menu( label='File', tearOff=True )
    pm.menuItem( label='Quit', c = partial(quit, "AutoRig_JT"))
    pm.menu( label='Help', helpMenu=True )
    pm.menuItem( 'Application..."', label='About Creator', c = about )
    pm.menuItem( 'Instructions', label='Instructions', c = instructions )
	
		
    mainLayout = pm.columnLayout(adj = True, w=300, h=700)

    # unique UI stuff

    imagePath = pm.internalVar(upd = True) + "icons/autoRig_banner.jpg"
    pm.image(w = 300, h = 100,image = imagePath, parent = mainLayout)
    pm.separator(style = 'none', h=20)

    pm.rowColumnLayout(nc = 2, cw = [(1,100),(2,200)],parent = mainLayout, columnOffset = ([(1,"left",10),(2,"left",0)]))

    pm.text(l='    Rig_Prefix : ')

    RigPrefix = pm.textFieldGrp("RigPrefix",tx='Character_',w=80) 

    pm.separator(style = 'none', h=20)
    pm.separator(style = 'none', h=20)
	
    
	
    pm.text(l='Spine Joints : ')
    spineNumberField = pm.intFieldGrp("spineNumberField",numberOfFields=1,v1=3,w=190)
	
    pm.setParent(u=True)
	
	
    pm.separator(style = 'none', h=20)
    pm.separator(style = 'none', h=20)

    pm.separator(style = 'none',h=20)
    pm.button(l='Create Reference Skeleton',c=referenceSkeleton, w=190,h=40,bgc=[0.2,0.2,0.2])

    pm.separator(style = 'none', h=20)

    pm.button(l='Mirror Locators (X+ to -X) (edit)', c=mirrorLocators, w=190, h=40, bgc=[0.2, 0.2, 0.2])

    pm.separator(style='none', h=20)
    
    pm.button(l='Create Joint Skeleton (edit)', c=jointSkeleton, w=190, h=40, bgc=[0.2, 0.2, 0.2])

    pm.separator(style='none', h=20)
    
    pm.radioButtonGrp('ZAxisOption', label='Z Align Axis', labelArray3=['X', 'Y', 'Z'], numberOfRadioButtons=3,cw=[(1,70),(2,35),(3,35)] )

    pm.radioButtonGrp('directionOption', label='+ or -', labelArray2=['+', '-'], numberOfRadioButtons=2,cw=[(1,70),(2,35)] )
    
    pm.button(l='Align Joints (select joints in chain you want to align)', c=alignChain, w=190, h=40, bgc=[0.2, 0.2, 0.2])

    pm.separator(style='none', h=20)

    pm.button(l='Finalize Rig',c=finalize, w=190,h=40,bgc=[0.2,0.2,0.2])

    pm.separator(style = 'none', h=20)


    pm.button(l='Exit',c=partial(quit,"AutoRig_JT"), w=190,h=40,bgc=[0.2,0.2,0.2])	

    print windowUI

    pm.showWindow(windowUI)
	
    pm.window("AutoRig_JT", e=True,w=300,h=600)

def referenceSkeleton(*args):
	AutoRig_JT.createReferenceSkeleton()

def mirrorLocators(*args):
	# Mirror AutoRig locators from Left to Right

	pm.select('*locRefSkl_l*')
	LeftLocators = pm.ls(sl=True, tr=True)

	pm.select('*locRefSkl_r*')
	RightLocators = pm.ls(sl=True, tr=True)

	MirList = []

	for locator in LeftLocators:
		# create Locator, group and flip then snap the matching locators to them

		MirrorProx = pm.spaceLocator(n='MIRROR_' + locator)
		MirList.append(MirrorProx[0])

		pm.delete(pm.pointConstraint(locator, MirrorProx, mo=False))

	mirGRP = pm.group(em=True, n='GRP_MirGroup')

	pm.parent(MirList, mirGRP)

	pm.setAttr(mirGRP + '.sx', -1)

	i = 0
	listConstraints = []
	for locator in MirList:
		rightLoc = LeftLocators[i].replace('_l_', '_r_')
		print rightLoc

		constraint = pm.pointConstraint(locator, rightLoc, mo=False)
		listConstraints.append(constraint[0])

		i = i + 1

	pm.delete(listConstraints)

def alignChain(*args):
    selectionZ =  pm.radioButtonGrp('directionOption',q=True,sl=True)
    direction =  pm.radioButtonGrp('ZAxisOption',q=True,sl=True)
    
    alignJointChain(pm.ls(sl=True,type='joint'),selectionZ,1,direction)



    
def jointSkeleton(*args):
	Input_spineJoints = pm.intFieldGrp("spineNumberField", q=True, v1=True)
	AutoRig_JT.createJoints(Input_spineJoints)



def finalize(*args):


	Input_spineJoints = pm.intFieldGrp("spineNumberField", q=True, v1=True)
	Input_RigPrefix = pm.textFieldGrp("RigPrefix", q=True, tx=True)
	
	AutoRig_JT.finaliseRig(Input_spineJoints,Input_RigPrefix)

def quit(window, *args):
	pm.deleteUI(window)
def instructions(*args):

	if pm.window("InstructionsWindow", q=True, exists = True):
			pm.deleteUI("InstructionsWindow")
			
	InstructionsWindow = pm.window("InstructionsWindow",t="Instructions",w=200,h=300,bgc=[0.15,0.15,0.15], sizeable=False)
	pm.columnLayout(parent = "InstructionsWindow",adjustableColumn=True)
	
	pm.text(l='Instructions', fn='boldLabelFont', align='center' )
	pm.separator(h=10, style = 'none')
	pm.text(l='First define what the prefix of the character rig will be.', align='center' )
	pm.text(l='This is so when rigging multiple characters there are no overlapping names. ', align='center' )
	pm.separator(h=5, style = 'none')
	pm.text(l='Then input how many joints you want in the spine', align='center' )
	pm.text(l='the more joints the smoother the bend but the more weight painting required.', align='center' )
	pm.text(l='Judge based on the topology resolution of your model. ', align='center' )
	pm.separator(h=5, style = 'none')
	pm.text(l='When ready create the "Reference Skeleton" and scale the rig to match your character', align='center' )
	pm.text(l='before placing all the joints based on your model', align='center' )
	pm.separator(h=10, style = 'none')
	pm.text(l='When done press Finalize and your rig will be made! Happy animating!!!', align='center' )
	
	pm.separator(h=20,style='none')
	
	pm.button(l='Exit',c=partial(quit, "InstructionsWindow"),h=50,bgc=[0.2,0.2,0.2])
	
	pm.showWindow(InstructionsWindow)
	
	pm.window("InstructionsWindow", e=True,w=500,h=220)

	
def about(*args):
	
	if pm.window("AboutWindow", q=True, exists = True):
		pm.deleteUI("AboutWindow")
		pm.deleteUI("AboutWindow")
		
	aboutWindow = pm.window("AboutWindow",t="About",w=200,h=200,bgc=[0.15,0.15,0.15], sizeable=False)
	pm.columnLayout(parent = "AboutWindow",adj=True)
	
	pm.text(l='About AutoRig', fn='boldLabelFont', align='center' )
	pm.separator(h=10, style = 'none')
	pm.rowColumnLayout(nc=2, cw=[(1,100),(2,190)])
	pm.text(l='Created by:', align='center' )
	pm.text(l='Jeremy Taylor', align='left' )
	pm.separator(h=5, style = 'none')
	pm.separator(h=5, style = 'none')
	pm.text(l='Email:', align='center' )
	pm.text(l='nightsymbol@gmail.com', align='left' )
	pm.separator(h=5, style = 'none')
	pm.separator(h=5, style = 'none')
	pm.text(l='Vimeo Page :', align='center' )
	vimeoLink = pm.text(hl=True, l="https://vimeo.com/spiritforger101", align='left' )
	print vimeoLink
	pm.separator(h=10, style = 'none')
	pm.separator(h=10, style = 'none')
	pm.text(l='Report Bugs:', align='center' )
	pm.text(l='No Link', align='left' )
	
	pm.setParent(u=True)
	
	pm.separator(h=10,style='none')
	
	pm.button(l='Exit',c=partial(quit, "AboutWindow"),bgc=[0.2,0.2,0.2])
	
	pm.showWindow(aboutWindow)
	
	pm.window("AboutWindow", e=True,w=290,h=140)