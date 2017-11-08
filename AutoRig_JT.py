## Python Auto Rig Version 0.0

## Written by Jeremy Taylor nightsymbol@gmail.com

## Version 0.0 is a basic Bipedal Auto Rig for humans with the following features:
##                                                             IK/FK Arms and Legs
##                                                             SDK for fingers and feet
##                                                             Ribbion Spine With IK and FK
##                                                             VectorTracking for blendShape Targets
'''

NOTE : The refernce skeleton for this auto rig uses just the world space positions and auto orients the joints to face the correct direction


'''

## Import Python Libraries

import maya.cmds as cmds
from functools import partial

# define class for bones
class bone :
    
    def __init__(self, name, position):
        self.boneName = name
        self.bonePosition = position
        self.rotationAxis = '-y'
            
    def create(self):
        cmds.joint(name=(self.boneName),position=(self.bonePosition) )
        
    def parent(self, name):
        cmds.parent(self.boneName, name)
    
    def alignToChild(self,child):
         
         cmds.delete(cmds.aimConstraint( child, self.boneName, aim = (1,0,0), mo=False, n="alignToParentConstraint01"))
         cmds.makeIdentity(a=True,r=True)

    def queryLength(self):
        
        length = cmds.getAttr(self.boneName+".tx")
        return length
        
    type = 'joint'

AttrType = {'vector':'double3','float':'double','interger':'long','boolean':'bool','enum':'enum'}

heirachyNaming = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

heirarchyGroups = 'CharacterNode01', 'Model01', 'Skeleton01', 'Controls01', 'Ik01', 'ExtraNodes01', 'BlendShapes01'

nullRotation = 0.0,0.0,0.0

nullPos = 0,0,0

offsetFalse = False

offsetTrue = True

arm = 'shoulder', 'elbow','wrist'
leg = 'hip', 'shin','ankle'
mirrorAXIS = '_l_','_r_'
limbs = '_leftARM_','_rightARM_','_leftLEG_','_rightLEG_'

#  possible ik Chain class set up for the future
class IK_chain : 
    def __init__(self, name,joint1,joint2,joint3,ikHandle):
        self.name = name
        self.firstJoint = joint1
        self.secondJoint = joint2
        self.thirdJoint = joint3
        self.ikHandleName = ikHandle
    

# class definition for Controls 
class control :
    # class initilization
    def __init__(self, name, position,rotation,type):
        self.ctrlName = name.replace('jBn','ctrl');name.replace('jDrv_IK','ctrl');name.replace('jDrv_FK','ctrl')
        self.ctrlPosition = position
        self.ctrlRotation = rotation
        self.rotationAxis = 'xyz'
        self.ctrlShape = type
    type = 'control'
	# class function for creating the control, control shape is determined by the class attribute ctrlShape 
    def create(self):
        if self.ctrlShape == 'circle':
            cmds.circle(name=(self.ctrlName),nr=(1,0,0),r=10)
        if self.ctrlShape == 'box':
            cmds.curve(n=(self.ctrlName), d=1, p=[(-0.5, 0.5, -0.5) , (-0.5, 0.5, 0.5) , (0.5, 0.5, 0.5) , (0.5, 0.5, -0.5) , (-0.5, 0.5, -0.5) ,( -0.5, -0.5, -0.5) , (0.5, -0.5, -0.5) , (0.5, -0.5, 0.5) , (-0.5, -0.5, 0.5) , (-0.5, -0.5, -0.5) , (0.5, -0.5, -0.5) , (0.5, 0.5, -0.5) , (0.5, 0.5, 0.5) , (0.5, -0.5, 0.5) , (-0.5, -0.5, 0.5) , (-0.5, 0.5, 0.5)] ,k=[0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 ])
            cmds.scale(5,5,5)
            cmds.makeIdentity(a=True,s=True)
        if self.ctrlShape == 'square':
            cmds.curve( n=(self.ctrlName),d=1, p=[(1, 0, 1) , (1, 0, -1), (-1, 0, -1), (-1, 0, 1) , (1, 0, 1) ] , k=[0, 1 , 2 , 3 , 4 ])
            cmds.scale(5,5,5)
            cmds.rotate(0,0,90)
            cmds.makeIdentity(a=True,r=True,s=True)
        if self.ctrlShape == 'triangle':
            cmds.curve(n=(self.ctrlName), d=1, p=[(0, 0, 0) , (1, 0, 1), (-1, 0, 1), (0, 0, 0)] , k=[0, 1 , 2 , 3 ])
            cmds.scale(5,5,5)
            cmds.makeIdentity(a=True,s=True)
        if self.ctrlShape == 'pin':
            cmds.curve(n=(self.ctrlName), d=1, p=[(0, 0, 0) , (0, 0, -0.4), (0, 0, -0.8), (-0.1, 0, -0.8) , (-0.1, 0, -1) , (0.1, 0, -1) ,  (0.1, 0, -0.8),  (0, 0, -0.8)] , k=[0, 1 , 2 , 3 , 4 , 5 , 6 , 7])
            cmds.rotate(90,0,0)
            cmds.makeIdentity(a=True,r=True)
            cmds.move(0,-2.5,0)
            cmds.scale(5,5,5)
            cmds.makeIdentity(a=True,s=True)

        # groups the control to act as an offset for orientating the control later
        cmds.group(name=('grp'+self.ctrlName))
        cmds.setAttr((self.ctrlName+'.tx'),self.ctrlPosition[0])
        cmds.setAttr((self.ctrlName+'.ty'),self.ctrlPosition[1])
        cmds.setAttr((self.ctrlName+'.tz'),self.ctrlPosition[2])
        cmds.setAttr((self.ctrlName+'.rx'),self.ctrlRotation[0])
        cmds.setAttr((self.ctrlName+'.ry'),self.ctrlRotation[1])
        cmds.setAttr((self.ctrlName+'.rz'),self.ctrlRotation[2])
        cmds.select(self.ctrlName,r=True)
        cmds.makeIdentity(a=True,t=True,r=True)
        cmds.setAttr((self.ctrlName+'.ty'),0)
		# class function to parent control group to an object
    def parent(self, name):
        cmds.parent(('grp'+self.ctrlName), name)
    def offSetGrp(self):
        cmds.group(em=True,n=('grpOfs_'+self.ctrlName))
        cmds.delete(cmds.parentConstraint( self.ctrlName, ('grpOfs_'+self.ctrlName), mo=False, n="alignToJointConstraint01"))
        cmds.parent(('grpOfs_'+self.ctrlName),('grp'+self.ctrlName))
        cmds.parent((self.ctrlName),('grpOfs_'+self.ctrlName))
    # class function to align the control group to an object
    def alignToJoint(self,joint):
         
         cmds.delete(cmds.parentConstraint( joint, ('grp'+self.ctrlName), mo=False, n="alignToJointConstraint01"))
         pos = cmds.xform(joint,q=True,ws=True,rp=True)
         cmds.move(pos[0],pos[1],pos[2],(self.ctrlName+'.rotatePivot'),(self.ctrlName+'.scalePivot'),rpr=True)
         
	# class function to constrain an object to the controller, based on the input
    def constrainTo(self,joint,type,offset):
        
        if type == 'parent' :
            cmds.parentConstraint(self.ctrlName,joint,mo=offset)
        elif type == 'point' :
            cmds.pointConstraint(self.ctrlName,joint,mo=offset)
        elif type == 'orient' :
            cmds.orientConstraint(self.ctrlName,joint,mo=offset)
        elif type == 'aim' :
            cmds.aimConstraint(self.ctrlName,joint,mo=offset)
        else:
            cmds.warning('Incorrect Type')
	# class function to add attributes to the control
    def addAttributes(self,attr,type,amin,amax,display):
        
        if type == 'float':
            cmds.addAttr(self.ctrlName,ln=(attr),min=(amin),max=(amax),k=True,h=False)
            if display == 'Keyable':
                cmds.setAttr((self.ctrlName+'.'+attr),e=True,channelBox=True,keyable=True)
            elif display == 'Displayable':
                cmds.setAttr((self.ctrlName+'.'+attr),e=True,keyable=True)
            elif display == 'Hidden':
                cmds.setAttr((self.ctrlName+'.'+attr),e=True,h=True)
        elif type == 'enum':
            cmds.addAttr(at='enum',ln=(attr),enumName='green:blue',k=True)
            if attr == 'localSpace':
                cmds.addAttr((self.ctrlName+'.'+attr),e=True,enumName='World:COG:Chest:Pelvis:Head:Loc')
                
                
            if display == 'Keyable':
                cmds.setAttr((self.ctrlName+'.'+attr),e=True,channelBox=True,keyable=True)
            elif display == 'Displayable':
                cmds.setAttr((self.ctrlName+'.'+attr),e=True,keyable=True)
            elif display == 'Hidden':
                cmds.setAttr((self.ctrlName+'.'+attr),e=True,h=True)





# defines a function for aligning joints to their children with the Z axis facing the correct direction
def alignJoints(parent,joint,child,axis,mirrorFunction) :
    
    getPosParent = cmds.xform(parent,q=True, ws=True, rp=True)
    getPosChild = cmds.xform(child,q=True, ws=True, rp=True)
    getPosJoint = cmds.xform(joint,q=True, ws=True, rp=True)
	# locators used to calculate the 'Behind' axis of the joint
    cmds.spaceLocator(n='parentLoc',p=getPosParent)
    cmds.CenterPivot()
    cmds.spaceLocator(n='childLoc',p=getPosChild)
    cmds.CenterPivot()
    cmds.spaceLocator(n='jointLoc',p=getPosJoint)
    cmds.CenterPivot()
    cmds.spaceLocator(n='behindLoc')
    cmds.pointConstraint('parentLoc','childLoc','behindLoc')
	
    # a dictionary that takes the provided aim axis and defines the up vector 
	
    aim = {'x':(1, 0, 0),'y':(0, 1, 0),'z':(0, 0, 1),'-x':(-1, 0, 0),'-y':(0, -1, 0),'-z':(0, 0, -1), 'obj_arm':(0,0,1),'-obj_hip':(0,1,0)}
    
	# a dictionary that changes the aim vector based on if the joint is mirrored or normal
	
    mirror = {'mirror':(-1, 0, 0),'normal':(1, 0, 0)}
	
    Loc =  joint.replace('jBn','loc')
    LocName = Loc+'Z'
    # if the object is a hip or shoulder its up vector will aim towards a locator object
    if axis == 'obj_hip' :
        if mirrorFunction == 'normal':  
            cmds.aimConstraint('childLoc', 'jointLoc', offset=(0, 0, 0), weight=1, aimVector=(mirror[mirrorFunction]), upVector=(0,0,1), worldUpType="object", worldUpObject=LocName)
        else:
            cmds.aimConstraint('childLoc', 'jointLoc', offset=(0, 0, 0), weight=1, aimVector=(mirror[mirrorFunction]), upVector=(0,0,-1), worldUpType="object", worldUpObject=LocName)

    elif axis == 'obj_arm' :
        if mirrorFunction == 'normal':  
            cmds.aimConstraint('childLoc', 'jointLoc', offset=(0, 0, 0), weight=1, aimVector=(mirror[mirrorFunction]), upVector=(0,0,1), worldUpType="object", worldUpObject=LocName)
        else:
            cmds.aimConstraint('childLoc', 'jointLoc', offset=(0, 0, 0), weight=1, aimVector=(mirror[mirrorFunction]), upVector=(0,0,-1), worldUpType="object", worldUpObject=LocName)
    else:    
        cmds.aimConstraint('childLoc', 'jointLoc', offset=(0, 0, 0), weight=1, aimVector=(mirror[mirrorFunction]), upVector=(aim[axis]), worldUpType="object", worldUpObject='behindLoc')
    
	# variabless get the rotation form the created locator 
    Rotx = cmds.getAttr('jointLoc.rx')
    Roty = cmds.getAttr('jointLoc.ry')
    Rotz = cmds.getAttr('jointLoc.rz')
    # zeros out the joints orientation to orient it to the world 
    cmds.setAttr ((joint+".jointOrientX"), 0)
    cmds.setAttr ((joint+".jointOrientY"), 0)
    cmds.setAttr ((joint+".jointOrientZ"), 0)
	# sets the rotation of the joint to the same as the locator
    cmds.setAttr((joint+'.rx'),Rotx)
    cmds.setAttr((joint+'.ry'),Roty)
    cmds.setAttr((joint+'.rz'),Rotz)
	# freezes transforms which in maya 2016 and UP aligns the joint orientation to the joint rotation and then zeros the rotation values
    cmds.select(joint, r=True)
    cmds.makeIdentity(a=True,r=True)
    # deletes the locators 
    cmds.delete('parentLoc','childLoc','jointLoc','behindLoc')
# this function creates locators specifically for referencing the bipedal skeleton
def jointLocators(name, X, Y, Z,axis):
    
    locator = cmds.spaceLocator(n=name) 
    firstCircle = cmds.circle( nr= (1, 0, 0), n=(name), ch=False)
    cmds.pickWalk(d='down')
    cmds.select(locator,add = True)
    cmds.parent(r=True, s=True)
    secondCircle = cmds.circle( nr= (0, 1, 0), n=name, ch=False)
    cmds.pickWalk(d='down')
    cmds.select(locator,add = True)
    cmds.parent(r=True, s=True)
    thirdCircle = cmds.circle( nr= (0, 0, 1), n=name, ch=False)
    cmds.pickWalk(d='down')
    cmds.select(locator,add = True)
    cmds.parent(r=True, s=True)
    cmds.delete(firstCircle, secondCircle, thirdCircle)

    cmds.setAttr((name+'.translateX'), X)
    cmds.setAttr((name+'.translateY'), Y)
    cmds.setAttr((name+'.translateZ'), Z)
    
    cmds.addAttr(name, ln="axis",at="enum",en="UP:LEFT:RIGHT:DOWN:OBJ_HIP:OBJ_ARM")
    
    sideAxis = {'UP':0,'LEFT':1,'RIGHT':2,'DOWN':3,'OBJ_HIP':4,'OBJ_ARM':5}
    cmds.setAttr((name+'.axis'), sideAxis[axis])

# this function mimics mayas replace name function 
def replaceNames(find,replaceWith, object_list):

    #for loop to look at each name and replace string
    for obj in object_list :
        name = obj
        newName = name.replace(find,replaceWith)
        newName = newName.replace('05','01')
        newName = newName.replace('02','01')
        cmds.select(obj,r=True)
        cmds.rename(newName)
# this function finds the polevector of IK chains 
def PoleVector(joint,ikhandle) :
        
        
    child = cmds.listRelatives(joint,children=True)
    parent = cmds.listRelatives(joint, parent=True)

    getPosParent = cmds.xform(parent[0],q=True, ws=True, rp=True)
    getPosChild = cmds.xform(child[0],q=True, ws=True, rp=True)
    getPosJoint = cmds.xform(joint,q=True, ws=True, rp=True)

    cmds.spaceLocator(n='parentLoc',p=getPosParent)
    cmds.CenterPivot()
    cmds.spaceLocator(n='childLoc',p=getPosChild)
    cmds.CenterPivot()
    cmds.spaceLocator(n='jointLoc',p=getPosJoint)
    cmds.CenterPivot()
    cmds.spaceLocator(n='behindLoc')
    cmds.group(n='ofs_behindLoc')
    cmds.pointConstraint('parentLoc','childLoc','ofs_behindLoc')
    cmds.aimConstraint('jointLoc', 'ofs_behindLoc', offset=(0, 0, 0), weight=1, aimVector=(1,0,0), upVector=(0,1,0), worldUpType="object",worldUpObject=parent[0])
    cmds.setAttr('behindLoc.tx', 15)
    cmds.setAttr('behindLoc.ty', 5)
    
    getPosPV = cmds.xform('behindLoc',q=True, ws=True, rp=True)
    
    controlName = joint.replace('jDrv','Ctrl')
    
    cmds.circle(nr=(0,0,1),n=controlName,r=5)
    
    cmds.delete(cmds.pointConstraint('behindLoc',controlName))
    
    cmds.makeIdentity(a=True,t=True)
    
    cmds.poleVectorConstraint(controlName,ikhandle,w=1)
    
    cmds.delete('parentLoc','childLoc','jointLoc','ofs_behindLoc')
    
# function defines all locators for the refernce skeleton with their positions and parent to each other
def referenceSkeleton():
    
    # default positions
        
    jointLocators('locRefSkl_pelvis01', 0.0 , 91.135, 1.44,'UP')

    jointLocators('locRefSkl_chest01', 0.0, 123.936, 3.322,'UP')

    jointLocators('locRefSkl_neck01', 0.0, 153.374, -2.236,'DOWN')
    
    cmds.parent('locRefSkl_neck01','locRefSkl_chest01')

    jointLocators('locRefSkl_head01',  0.0, 163.675, 1.423,'UP')
    
    cmds.parent('locRefSkl_head01','locRefSkl_neck01')

    jointLocators('locRefSkl_headTop01', 0.0, 181.474, 1.423,'UP')
    
    cmds.parent('locRefSkl_headTop01','locRefSkl_head01')

    # left Leg positions

    jointLocators('locRefSkl_l_hip01', 9.361 , 91.135, 1.44,'OBJ_HIP')
    
    cmds.parent('locRefSkl_l_hip01','locRefSkl_pelvis01')
    
    cmds.spaceLocator(n='loc_l_hip01Z', p= ( 0.0 , 91.135, 1.44))
    cmds.CenterPivot()
    cmds.parent('loc_l_hip01Z','locRefSkl_l_hip01')

    jointLocators('locRefSkl_l_shin01', 12.783, 49.559, 0.655,'DOWN')
    
    cmds.parent('locRefSkl_l_shin01','locRefSkl_l_hip01')

    jointLocators('locRefSkl_l_ankle01', 15.26, 9.256, -2.966,'UP')
    
    cmds.parent('locRefSkl_l_ankle01','locRefSkl_l_shin01')

    jointLocators('locRefSkl_l_ball01', 16.161, 0.912, 7.473,'UP')

    cmds.parent('locRefSkl_l_ball01','locRefSkl_l_ankle01')

    jointLocators('locRefSkl_l_toe01', 16.161, 0.229, 16.185,'UP')

    cmds.parent('locRefSkl_l_toe01','locRefSkl_l_ball01')

    # left arm positions

    jointLocators('locRefSkl_l_clavicle01', 2.527, 149.462, 4.152,'LEFT')
    
    cmds.parent('locRefSkl_l_clavicle01','locRefSkl_chest01')
    
    

    jointLocators('locRefSkl_l_shoulder01', 17.528, 144.535, -1.288,'OBJ_ARM')
    
    cmds.parent('locRefSkl_l_shoulder01','locRefSkl_l_clavicle01')
    
    cmds.spaceLocator(n='loc_l_shoulder01Z', p= (17.528 , 144.535, 5.383))
    cmds.CenterPivot()
    cmds.parent('loc_l_shoulder01Z','locRefSkl_l_shoulder01')

    jointLocators('locRefSkl_l_elbow01', 31.767, 116.753, -3.795,'LEFT')
    
    cmds.parent('locRefSkl_l_elbow01','locRefSkl_l_shoulder01')

    jointLocators('locRefSkl_l_wrist01', 42.811 , 94.241, 3.524,'LEFT')
    
    cmds.parent('locRefSkl_l_wrist01','locRefSkl_l_elbow01')

    # left fingers positions
    
    # metacarpal bone positions

    jointLocators('locRefSkl_l_thumb_metacarpal01', 42.447,91.97,5.692,'DOWN')
    
    cmds.parent('locRefSkl_l_thumb_metacarpal01','locRefSkl_l_wrist01')

    jointLocators('locRefSkl_l_index_metacarpal01', 46.132,87.872,7.244,'DOWN')
    
    cmds.parent('locRefSkl_l_index_metacarpal01','locRefSkl_l_wrist01')

    jointLocators('locRefSkl_l_middle_metacarpal01', 46.328,87.196,5.056,'DOWN')
    
    cmds.parent('locRefSkl_l_middle_metacarpal01','locRefSkl_l_wrist01')

    jointLocators('locRefSkl_l_ring_metacarpal01', 46.328,86.56,2.987,'DOWN')
    
    cmds.parent('locRefSkl_l_ring_metacarpal01','locRefSkl_l_wrist01')

    jointLocators('locRefSkl_l_pinkie_metacarpal01', 45.096,86.758,0.799,'DOWN')
    
    cmds.parent('locRefSkl_l_pinkie_metacarpal01','locRefSkl_l_wrist01')
    
    
    # thumb position

    jointLocators('locRefSkl_l_thumb_a01', 40.994, 88.867, 9.352,'DOWN')
    
    cmds.parent('locRefSkl_l_thumb_a01','locRefSkl_l_thumb_metacarpal01')

    jointLocators('locRefSkl_l_thumb_b01', 40.556, 85.406, 10.824,'DOWN')
    
    cmds.parent('locRefSkl_l_thumb_b01','locRefSkl_l_thumb_a01')

    jointLocators('locRefSkl_l_thumb_cEnd01', 39.819, 82.86, 12.257,'DOWN')
    
    cmds.parent('locRefSkl_l_thumb_cEnd01','locRefSkl_l_thumb_b01')
    
    # index position

    jointLocators('locRefSkl_l_index_a01', 45.95, 83.258, 9.034,'DOWN')
    
    cmds.parent('locRefSkl_l_index_a01','locRefSkl_l_index_metacarpal01')

    jointLocators('locRefSkl_l_index_b01', 45.686, 80.155, 10.029,'DOWN')
    
    cmds.parent('locRefSkl_l_index_b01','locRefSkl_l_index_a01')

    jointLocators('locRefSkl_l_index_c01', 45.114, 78.444, 10.785,'DOWN')
    
    cmds.parent('locRefSkl_l_index_c01','locRefSkl_l_index_b01')

    jointLocators('locRefSkl_l_index_dEnd01', 44.27,76.455,11.302,'DOWN')
    
    cmds.parent('locRefSkl_l_index_dEnd01','locRefSkl_l_index_c01')


    # middle finger position

    jointLocators('locRefSkl_l_middle_a01', 46.438, 82.223, 6.13,'DOWN')
    
    cmds.parent('locRefSkl_l_middle_a01','locRefSkl_l_middle_metacarpal01')

    jointLocators('locRefSkl_l_middle_b01',  46.124, 78.961, 6.886,'DOWN')
    
    cmds.parent('locRefSkl_l_middle_b01','locRefSkl_l_middle_a01')

    jointLocators('locRefSkl_l_middle_c01', 45.524, 76.415, 7.562,'DOWN')
    
    cmds.parent('locRefSkl_l_middle_c01','locRefSkl_l_middle_b01')

    jointLocators('locRefSkl_l_middle_dEnd01', 44.756, 74.148, 8.517,'DOWN')
    
    cmds.parent('locRefSkl_l_middle_dEnd01','locRefSkl_l_middle_c01')
    
    # ring finger position


    jointLocators('locRefSkl_l_ring_a01', 45.848, 81.905, 3.465,'DOWN')
    
    cmds.parent('locRefSkl_l_ring_a01','locRefSkl_l_ring_metacarpal01')

    jointLocators('locRefSkl_l_ring_b01', 45.388, 78.444, 4.3,'DOWN')
    
    cmds.parent('locRefSkl_l_ring_b01','locRefSkl_l_ring_a01')

    jointLocators('locRefSkl_l_ring_c01', 44.904, 76.176, 4.857,'DOWN')
    
    cmds.parent('locRefSkl_l_ring_c01','locRefSkl_l_ring_b01')

    jointLocators('locRefSkl_l_ring_dEnd01', 43.79, 73.949, 5.732,'DOWN')
    
    cmds.parent('locRefSkl_l_ring_dEnd01','locRefSkl_l_ring_c01')


    # pinkie positions

    jointLocators('locRefSkl_l_pinkie_a01', 44.215, 82.502, 0.72,'DOWN')
    
    cmds.parent('locRefSkl_l_pinkie_a01','locRefSkl_l_pinkie_metacarpal01')


    jointLocators('locRefSkl_l_pinkie_b01',  43.753, 80.393, 0.879,'DOWN')
    
    cmds.parent('locRefSkl_l_pinkie_b01','locRefSkl_l_pinkie_a01')


    jointLocators('locRefSkl_l_pinkie_c01', 43.008, 77.728, 1.555,'DOWN')
    
    cmds.parent('locRefSkl_l_pinkie_c01','locRefSkl_l_pinkie_b01')


    jointLocators('locRefSkl_l_pinkie_dEnd01', 42.014, 75.739, 2.072,'DOWN')
    
    cmds.parent('locRefSkl_l_pinkie_dEnd01','locRefSkl_l_pinkie_c01')
    
    # right Leg positions


    jointLocators('locRefSkl_r_hip01', -9.361 , 91.135, 1.44,'OBJ_HIP')
    
    cmds.parent('locRefSkl_r_hip01','locRefSkl_pelvis01')
    
    cmds.spaceLocator(n='loc_r_hip01Z', p= ( 0.0 , 91.135, 1.44))
    cmds.CenterPivot()
    cmds.parent('loc_r_hip01Z','locRefSkl_r_hip01')


    jointLocators('locRefSkl_r_shin01', -12.783, 49.559, 0.655,'UP')
    
    cmds.parent('locRefSkl_r_shin01','locRefSkl_r_hip01')


    jointLocators('locRefSkl_r_ankle01', -15.26, 9.256, -2.966,'DOWN')
    
    cmds.parent('locRefSkl_r_ankle01','locRefSkl_r_shin01')


    jointLocators('locRefSkl_r_ball01', -16.161, 0.912, 7.473,'DOWN')

    cmds.parent('locRefSkl_r_ball01','locRefSkl_r_ankle01')


    jointLocators('locRefSkl_r_toe01', -16.161, 0.229, 16.185,'DOWN')

    cmds.parent('locRefSkl_r_toe01','locRefSkl_r_ball01')

    # right arm positions


    jointLocators('locRefSkl_r_clavicle01', -2.527, 149.462, 4.152,'RIGHT')
    
    cmds.parent('locRefSkl_r_clavicle01','locRefSkl_chest01')


    jointLocators('locRefSkl_r_shoulder01', -17.528, 144.535, -1.288,'OBJ_ARM')
    
    cmds.parent('locRefSkl_r_shoulder01','locRefSkl_r_clavicle01')
    
    cmds.spaceLocator(n='loc_r_shoulder01Z', p= (-17.528 , 144.535, 5.383))
    cmds.CenterPivot()
    cmds.parent('loc_r_shoulder01Z','locRefSkl_r_shoulder01')


    jointLocators('locRefSkl_r_elbow01', -31.767, 116.753, -3.795,'RIGHT')
    
    cmds.parent('locRefSkl_r_elbow01','locRefSkl_r_shoulder01')
	
    jointLocators('locRefSkl_r_wrist01', -42.811 , 94.241, 3.524,'RIGHT')
    
    cmds.parent('locRefSkl_r_wrist01','locRefSkl_r_elbow01')

    # right fingers positions
    
    # metacarpal bone positions

    jointLocators('locRefSkl_r_thumb_metacarpal01', -42.447,91.97,5.692,'DOWN')
    
    cmds.parent('locRefSkl_r_thumb_metacarpal01','locRefSkl_r_wrist01')

    jointLocators('locRefSkl_r_index_metacarpal01', -46.132,87.872,7.244,'DOWN')
    
    cmds.parent('locRefSkl_r_index_metacarpal01','locRefSkl_r_wrist01')

    jointLocators('locRefSkl_r_middle_metacarpal01', -46.328,87.196,5.056,'DOWN')
    
    cmds.parent('locRefSkl_r_middle_metacarpal01','locRefSkl_r_wrist01')

    jointLocators('locRefSkl_r_ring_metacarpal01', -46.328,86.56,2.987,'DOWN')
    
    cmds.parent('locRefSkl_r_ring_metacarpal01','locRefSkl_r_wrist01')

    jointLocators('locRefSkl_r_pinkie_metacarpal01', -45.096,86.758,0.799,'DOWN')
    
    cmds.parent('locRefSkl_r_pinkie_metacarpal01','locRefSkl_r_wrist01')
    
    
    # thumb position

    jointLocators('locRefSkl_r_thumb_a01', -40.994, 88.867, 9.352,'DOWN')
    
    cmds.parent('locRefSkl_r_thumb_a01','locRefSkl_r_thumb_metacarpal01')

    jointLocators('locRefSkl_r_thumb_b01', -40.556, 85.406, 10.824,'DOWN')
    
    cmds.parent('locRefSkl_r_thumb_b01','locRefSkl_r_thumb_a01')

    jointLocators('locRefSkl_r_thumb_cEnd01', -39.819, 82.86, 12.257,'DOWN')
    
    cmds.parent('locRefSkl_r_thumb_cEnd01','locRefSkl_r_thumb_b01')

    jointLocators('locRefSkl_r_index_a01', -45.95, 83.258, 9.034,'DOWN')
    
    cmds.parent('locRefSkl_r_index_a01','locRefSkl_r_index_metacarpal01')

    jointLocators('locRefSkl_r_index_b01', -45.686, 80.155, 10.029,'DOWN')
    
    cmds.parent('locRefSkl_r_index_b01','locRefSkl_r_index_a01')

    jointLocators('locRefSkl_r_index_c01', -45.114, 78.444, 10.785,'DOWN')
    
    cmds.parent('locRefSkl_r_index_c01','locRefSkl_r_index_b01')

    jointLocators('locRefSkl_r_index_dEnd01', -44.27,76.455,11.302,'DOWN')
    
    cmds.parent('locRefSkl_r_index_dEnd01','locRefSkl_r_index_c01')


    # middle finger position
    jointLocators('locRefSkl_r_middle_a01', -46.438, 82.223, 6.13,'DOWN')
    
    cmds.parent('locRefSkl_r_middle_a01','locRefSkl_r_middle_metacarpal01')

    jointLocators('locRefSkl_r_middle_b01', -46.124, 78.961, 6.886,'DOWN')
    
    cmds.parent('locRefSkl_r_middle_b01','locRefSkl_r_middle_a01')

    jointLocators('locRefSkl_r_middle_c01', -45.524, 76.415, 7.562,'DOWN')
    
    cmds.parent('locRefSkl_r_middle_c01','locRefSkl_r_middle_b01')

    jointLocators('locRefSkl_r_middle_dEnd01', -44.756, 74.148, 8.517,'DOWN')
    
    cmds.parent('locRefSkl_r_middle_dEnd01','locRefSkl_r_middle_c01')
    
    # ring finger position

    jointLocators('locRefSkl_r_ring_a01', -45.848, 81.905, 3.465,'DOWN')
    
    cmds.parent('locRefSkl_r_ring_a01','locRefSkl_r_ring_metacarpal01')

    jointLocators('locRefSkl_r_ring_b01', -45.388, 78.444, 4.3,'DOWN')
    
    cmds.parent('locRefSkl_r_ring_b01','locRefSkl_r_ring_a01')

    jointLocators('locRefSkl_r_ring_c01', -44.904, 76.176, 4.857,'DOWN')
    
    cmds.parent('locRefSkl_r_ring_c01','locRefSkl_r_ring_b01')

    jointLocators('locRefSkl_r_ring_dEnd01', -43.79, 73.949, 5.732,'DOWN')
    
    cmds.parent('locRefSkl_r_ring_dEnd01','locRefSkl_r_ring_c01')

    # pinkie positions

    jointLocators('locRefSkl_r_pinkie_a01', -44.215, 82.502, 0.72,'DOWN')
    
    cmds.parent('locRefSkl_r_pinkie_a01','locRefSkl_r_pinkie_metacarpal01')

    jointLocators('locRefSkl_r_pinkie_b01', -43.753, 80.393, 0.879,'DOWN')
    
    cmds.parent('locRefSkl_r_pinkie_b01','locRefSkl_r_pinkie_a01')

    jointLocators('locRefSkl_r_pinkie_c01', -43.008, 77.728, 1.555,'DOWN')
    
    cmds.parent('locRefSkl_r_pinkie_c01','locRefSkl_r_pinkie_b01')

    jointLocators('locRefSkl_r_pinkie_dEnd01', -42.014, 75.739, 2.072,'DOWN')
    
    cmds.parent('locRefSkl_r_pinkie_dEnd01','locRefSkl_r_pinkie_c01') 
    
    # Foot control positions
    
    jointLocators('locRefCtrl_l_Heel01', 16.0,0.0, -6.072,'DOWN')
    
    cmds.parent('locRefCtrl_l_Heel01','locRefSkl_l_ankle01')
    
    jointLocators('locRefCtrl_l_tiltLeft01',18.0,0.0, 0.0,'DOWN')
    
    cmds.parent('locRefCtrl_l_tiltLeft01','locRefSkl_l_ankle01')
    
    jointLocators('locRefCtrl_l_tiltRight01', 14.0,0.0, 0.0,'DOWN')
    
    cmds.parent('locRefCtrl_l_tiltRight01','locRefSkl_l_ankle01')
    
    
    
    
    jointLocators('locRefCtrl_r_Heel01', -16.0,0.0, -6.072,'DOWN')
    
    cmds.parent('locRefCtrl_r_Heel01','locRefSkl_r_ankle01')
    
    jointLocators('locRefCtrl_r_tiltLeft01',-18.0,0.0, 0.0,'DOWN')
    
    cmds.parent('locRefCtrl_r_tiltLeft01','locRefSkl_r_ankle01')
    
    jointLocators('locRefCtrl_r_tiltRight01', -14.0,0.0, 0.0,'DOWN')
    
    cmds.parent('locRefCtrl_r_tiltRight01','locRefSkl_r_ankle01')
       
       
# this function creates the reference skeleton and parents it to a scale controller, the scale of this controller will be stored and used throughout the script
def createReferenceSkeleton():
    if (cmds.objExists('Ctrl_scaleRig01')==False) :
        
        # Loop to create the group heirachy for the rig
        for x in range(7):
            
            name = heirarchyGroups[x]

            cmds.group(em=True, n=name)
            
            cmds.setAttr((name+".tx"), lock=True, keyable=False ,channelBox=False)
            cmds.setAttr((name+".ty"), lock=True, keyable=False ,channelBox=False)
            cmds.setAttr((name+".tz"), lock=True, keyable=False ,channelBox=False)
            cmds.setAttr((name+".rx"), lock=True, keyable=False ,channelBox=False)
            cmds.setAttr((name+".ry"), lock=True, keyable=False ,channelBox=False)
            cmds.setAttr((name+".rz"), lock=True, keyable=False ,channelBox=False)
            cmds.setAttr((name+".sx"), lock=True, keyable=False ,channelBox=False)
            cmds.setAttr((name+".sy"), lock=True, keyable=False ,channelBox=False)
            cmds.setAttr((name+".sz"), lock=True, keyable=False ,channelBox=False)
        
            if x > 0 :
                cmds.parent(name,heirarchyGroups[0])
            
        upRot = 0.0,0.0,90.0

        globalCtrl = control('ctrl_global01',nullPos,upRot,'circle')

        globalCtrl.create()
        globalCtrl.ctrlName
        cmds.scale(5,5,5,globalCtrl.ctrlName)

        cmds.makeIdentity(globalCtrl.ctrlName, a=True, s = True)

        globalCtrl.parent('CharacterNode01')

        cmds.parent('Controls01','Skeleton01','Ik01','ctrl_global01')
        
        referenceSkeleton()

        cmds.circle( nr= (0, 1, 0), n='Ctrl_scaleRig01', r=50, ch=False)

        cmds.parent('locRefSkl_chest01','locRefSkl_pelvis01','Ctrl_scaleRig01')

        cmds.select('Ctrl_scaleRig01')
        
    else:
        cmds.warning("Reference Skeleton Already exsists")
        
# runs the above function
# defines a function that runs through all the locators and creates joints at their locations, parenting them in the correct order based on the locators
#and aligning them to their children using the above 'align Joints' function

def createJoints(Input_spineJoints):    
    cmds.select("Ctrl_scaleRig01")
    cmds.select(hi=True)
    cmds.select("Ctrl_scaleRig01", d=True)
    cmds.select('loc_l_shoulder01Z','loc_l_hip01Z','loc_r_shoulder01Z','loc_r_hip01Z','locRefCtrl_r_Heel01','locRefCtrl_r_tiltLeft01','locRefCtrl_r_tiltRight01','locRefCtrl_l_Heel01','locRefCtrl_l_tiltLeft01','locRefCtrl_l_tiltRight01',d=True)

    referenceLocators = cmds.ls(sl=True,tr=True)

    cmds.select("Ctrl_scaleRig01")
    world = cmds.ls(sl=True,tr=True)

    for locs in referenceLocators :
        
        
        name = locs
        newName = name.replace("locRefSkl","jBn")
        
        getPos = cmds.xform(locs,q=True, ws=True, rp=True)

        joint = bone(newName,getPos)

        # create joint
        cmds.select(cl=True)
        joint.create()
        
        # align joints and parent

    for locs in referenceLocators :

        parent = cmds.listRelatives(locs, parent=True)
        child = cmds.listRelatives(locs, children=True, type='transform')
        
        num = 0
        
        if (not child) == False :
            for x in child:
                if x == 'loc_l_shoulder01Z':
                    del child[num]
                elif x == 'loc_l_hip01Z' :
                    del child[num]
                elif x == 'loc_r_shoulder01Z' :
                    del child[num]
                elif x == 'loc_r_hip01Z' :
                    del child[num]
                num = num + 1
                
        
        name = locs
        newName = name.replace("locRefSkl","jBn")
        
        newParent = parent[0]
        newParentName = newParent.replace("locRefSkl","jBn")
        
        getAxis = cmds.getAttr(locs+'.axis')
        
        aimAxis = 'y','z','-z','-y','obj_hip','obj_arm'
        
        axis = aimAxis[getAxis]
               
        mirror = ''
        
        if newName.find('_r_')==-1 :
            mirror = 'normal'
        else:
            mirror = 'mirror'
        
        if (not child) == False :
            newChild = child[0]
            newChildName = newChild.replace("locRefSkl","jBn")
        #else:

        # align joint to child
        if (not child) == True :
            print 'no'
        elif len(child) > 1:
            print 'no'
        else:
            alignJoints(newParentName, newName, newChildName,axis, mirror)
            
        # parent joint
        if parent[0] == world[0]:
            print 'no'
        else:
            cmds.parent(newName,newParentName)
            if (not child) == True :
                cmds.setAttr ((newName+".jointOrientX"), 0)
                cmds.setAttr ((newName+".jointOrientY"), 0)
                cmds.setAttr ((newName+".jointOrientZ"), 0)

            elif len(child) > 1:
                cmds.setAttr ((newName+".jointOrientX"), 0)
                cmds.setAttr ((newName+".jointOrientY"), 0)
                cmds.setAttr ((newName+".jointOrientZ"), 0)
            
    # reorient fingers
    fingers = '*l_thumb*','*l_index*','*l_middle*','*l_ring*','*l_pinkie*','*r_thumb*','*r_index*','*r_middle*','*r_ring*','*r_pinkie*',
    for finger in fingers :
        cmds.select(finger,hi=True)
        L_index = cmds.ls(sl=True,type='joint')
        for bones in L_index : 
            #unparent child
            child = cmds.listRelatives(bones,children=True)
            if (not child) == True :
                print 'no'
            else:    
                cmds.parent(child, w=True)
            # zero Z jointOrient
            cmds.setAttr ((bones+".jointOrientX"), 0)
            if (not child) == False :
                cmds.parent(child, bones)
    # create spine
    
    def createSpine(inputX):
        
        getPosPelvis = cmds.xform('locRefSkl_pelvis01',q=True, ws=True, rp=True)
        getPosChest = cmds.xform('locRefSkl_chest01',q=True, ws=True, rp=True)
        
        numSkeletonjoints = range(inputX)
        
        spineStart = bone(('jBn_spine_'+heirachyNaming[0]+'01'),getPosPelvis)
        spineEnd = bone(('jBn_spine_'+heirachyNaming[numSkeletonjoints[(inputX-1)]]+'01'),getPosChest)
        
        spineStart.create()
        cmds.select(cl=True)
        spineEnd.create()
        spineStart.alignToChild(spineEnd.boneName)
        cmds.parent(spineEnd.boneName,spineStart.boneName)
        
        cmds.setAttr ((spineEnd.boneName+".jointOrientX"), 0)
        cmds.setAttr ((spineEnd.boneName+".jointOrientY"), 0)
        cmds.setAttr ((spineEnd.boneName+".jointOrientZ"), 0)
        
        boneLen = (cmds.getAttr((spineEnd.boneName+'.tx'))/(inputX-1))
        addBoneLen = boneLen
                
        cmds.select(cl=True)
        
        currentBoneNum = 1
        
        for x in range((inputX-2)):
            
            spineName = ('jBn_spine_'+heirachyNaming[currentBoneNum]+'01')
            
            spineMiddle = cmds.duplicate(spineEnd.boneName, n=spineName)
            
            cmds.setAttr((spineName+'.tx'),boneLen)
            if currentBoneNum > 1 :
                cmds.parent(spineName,('jBn_spine_'+heirachyNaming[(currentBoneNum-1)]+'01'))
            currentBoneNum =  currentBoneNum + 1
            
            boneLen = boneLen + addBoneLen
            
        cmds.parent(spineEnd.boneName,spineName)
        
    
    
    #spineJointsQuery = cmds.promptDialog(t='How Many Spine Joints?', tx='How Many Spine Joints?')

    #Input_spineJoints = cmds.promptDialog(q=True, tx=True)
    
    spineJointsNum = Input_spineJoints
    cmds.select(cl=True)
    
    createSpine(int(spineJointsNum))
    
    cmds.parent('jBn_spine_a01', 'jBn_pelvis01', 'jBn_chest01', 'Skeleton01')
    
    
    cmds.parent('locRefCtrl_r_Heel01','locRefCtrl_r_tiltLeft01','locRefCtrl_r_tiltRight01','locRefCtrl_l_Heel01','locRefCtrl_l_tiltLeft01','locRefCtrl_l_tiltRight01',w=True)        
    cmds.delete("Ctrl_scaleRig01")

# creates the IK handles and pole vectors for the arms and legs
def IK_System():
    
    # Duplicate and rename chains
    
    cmds.select('jBn_l_shoulder01','jBn_r_shoulder01','jBn_l_hip01','jBn_r_hip01',r=True)
    listB = cmds.ls(sl=True)
    cmds.duplicate(rc=True)
    
    
    list_IK = cmds.ls(sl=True)
    
     # delete unessesary joints
    
    for x in list_IK:
        cmds.select(x, r=True)
        cmds.pickWalk(d='down')
        thirdjoint = cmds.pickWalk(d='down')
        cmds.select(hi=True)
        cmds.select(thirdjoint, d=True)
        cmds.delete()
    
    for x in list_IK :
        cmds.select(x,r=True,hi=True)
        list_chain = cmds.ls(sl=True)
        replaceNames('jBn','jDrv_IK', list_chain)
    
    
    cmds.select('jBn_l_shoulder01','jBn_r_shoulder01','jBn_l_hip01','jBn_r_hip01',r=True)
    
    cmds.duplicate(rc=True)
    
    list_FK = cmds.ls(sl=True)
    
    # delete unessesary joints

    for x in list_FK:
        cmds.select(x, r=True)
        cmds.pickWalk(d='down')
        thirdjoint = cmds.pickWalk(d='down')
        cmds.select(hi=True)
        cmds.select(thirdjoint, d=True)
        cmds.delete()
    
    for x in list_FK :
        cmds.select(x,r=True,hi=True)
        list_chain = cmds.ls(sl=True)
        replaceNames('jBn','jDrv_FK', list_chain)
    
    # relist IK and FK

    cmds.select('jDrv_IK_l_shoulder01','jDrv_IK_r_shoulder01','jDrv_IK_l_hip01','jDrv_IK_r_hip01',r=True)
    list_IK = cmds.ls(sl=True)
    
    cmds.select('jDrv_FK_l_shoulder01','jDrv_FK_r_shoulder01','jDrv_FK_l_hip01','jDrv_FK_r_hip01',r=True)
    list_FK = cmds.ls(sl=True)
    
    # group chains
    
    # group  bind chains 
    
    
    grpNames = 'grp_l_ARM01','grp_r_ARM01','grp_l_LEG01','grp_r_LEG01'
    i = 0
    for x in listB :
        cmds.select(x, r=True)
        cmds.group(n=grpNames[i])
        i = i+1
    
    # group  IK chains 
    
    grpNames = 'grp_l_ARM_IK_01','grp_r_ARM_IK_01','grp_l_LEG_IK_01','grp_r_LEG_IK_01'
    i = 0
    for x in list_IK :
        cmds.select(x, r=True)
        cmds.group(n=grpNames[i])
        i = i+1
   
    
    grpNames = 'grp_l_ARM_FK_01','grp_r_ARM_FK_01','grp_l_LEG_FK_01','grp_r_LEG_FK_01'
    i = 0
    for x in list_FK :
        cmds.select(x, r=True)
        cmds.group(n=grpNames[i])
        i = i+1
    
    # IK handles
    
    ikNames = 'ikRp_l_arm01','ikRp_r_arm01','ikRp_l_leg01','ikRp_r_leg01'
    
    i=0
    
    for x in list_IK :
        cmds.select(x, r=True)
        cmds.pickWalk(d='down')
        elbowJoint = cmds.ls(sl=True) 
        cmds.pickWalk(d='down')        
        endJoint = cmds.ls(sl=True)      
        cmds.ikHandle(endJoint[0],sj=x,sol='ikRPsolver',n=ikNames[i])
        cmds.parent(ikNames[i],'Ik01')
        
        PoleVector(elbowJoint[0],ikNames[i])
        
        i= i+1
    
    cmds.parent('grp_l_ARM01','grp_l_ARM_IK_01','grp_l_ARM_FK_01','grp_r_ARM01','grp_r_ARM_IK_01','grp_r_ARM_FK_01','jBn_chest01')

# a function used in testing to run the code up till the reference skeleton and test moving the locators around before creating the joint skeleton to look for bugs
def continueCommand():
    createJoints()
    IK_System()
    cmds.deleteUI(ContinueWithSkeleton)
        
'''-    '''
# function creates the Ribbion IK spine of the character 
def spineRig():
	# selects the base of the skeleton, a joint that must always exsist and grabs its heirarchy
    cmds.select('jBn_spine_a01',hi=True)
    list = cmds.ls(sl=True)
    points = []
    knots = [2,2]
    i = 2

    length = len(list)

    spans = length -1

	# a loop that creates a CV curve based on the positions spine joints
    for x in range(len(list)) :
        Xp = cmds.xform(list[x],q=True,ws=True,rp=True) 
        
        points.append(Xp)

        if x == 0 :
            cmds.curve(n='crv_1',d=1,p=[Xp])
        else:
            cmds.curve('crv_1',a=True,p=[Xp])
        
        knots.append(i)
        
        i = i + 1 +1
        
	
	# duplicates the cv curve and moves it to the other side, then using the loft tool to create a nurbs surface  
    cmds.move(1,0,0)

    cmds.duplicate(n='crv_2')

    cmds.move(-1,0,0)

    cmds.loft('crv_1','crv_2',n='surf_spine01',ch=False)

    cmds.rebuildSurface( "surf_spine01",ch=False,rpo=1,rt=0,end=1,kr=0,kcp=0,kc=0,su=1,du=3,sv=spans,dv=3,tol=0.01,fr=0,dir=2)

    cmds.select('surf_spine01',r=True)

    cmds.pickWalk(d='down')

    lofted = cmds.ls(sl=True)



    indent = 1

    V_value = 0.0

    V_increment = 1.0/((length-1))
	
	# creates the follicles that attach themselves to the nurbs surface, then parenting the joints to the follicles 

    for x in range(len(list)) :

        cmds.createNode('follicle',n=('fol_spine_Shape0'+str(indent)))

        folShape = cmds.ls(sl=True)
        
        

        cmds.pickWalk(d='up')

        fol = cmds.ls(sl=True)
        
        

        cmds.connectAttr((lofted[0]+'.worldMatrix[0]'),(folShape[0]+'.inputWorldMatrix'),f=True)

        cmds.connectAttr((lofted[0]+'.local'),(folShape[0]+'.inputSurface'),f=True)

        cmds.connectAttr((folShape[0]+'.outRotate'),fol[0]+'.rotate')
        cmds.connectAttr((folShape[0]+'.outTranslate'),fol[0]+'.translate')
        cmds.setAttr(fol[0]+'.inheritsTransform',False)
        
        cmds.setAttr((folShape[0]+'.parameterU'),0.5)
        cmds.setAttr((folShape[0]+'.parameterV'),(V_value))
        
        V_value = V_value + V_increment
        
        cmds.parent(list[x],fol[0])
        
        cmds.setAttr((list[x]+'.tx'),0)
        cmds.setAttr((list[x]+'.ty'),0)
        cmds.setAttr((list[x]+'.tz'),0)
        
        cmds.setAttr((list[x]+'.rx'),0)
        cmds.setAttr((list[x]+'.ry'),0)
        cmds.setAttr((list[x]+'.rz'),0)
        
        cmds.scaleConstraint('ctrl_global01',fol[0])
        
        indent = indent + 1
    # groups the folicles    
    cmds.select('*fol_*')

    cmds.group(n='grpFlcs_spine01')

    cmds.delete('crv_2')

    cmds.select('crv_1')

    cmds.move(0,0,0)
	
	# renames the initial curve and rebuilds it into a more flexible curve

    cmds.rename('crv_wireSpine01')

    cmds.rebuildCurve("crv_wireSpine01",ch=False,rpo=1,rt=0,end=0,kr=0,kcp=0,kep=1,kt=0,s=spans,d=3,tol=0.01 )

	# creates a blendshpe for the nurb surface, and uses the curve as a wiredeformer to control the blendshape
    cmds.duplicate('surf_spine01',n='bShps_spine01')

    blendName = cmds.blendShape( 'bShps_spine01', 'surf_spine01',n='blend_spine01')
    cmds.setAttr((blendName[0]+".bShps_spine01") ,1)

    wireName = cmds.wire('bShps_spine01',w='crv_wireSpine01',gw=False,en=1.0,ce=0.0,li=0.0,n='def_wireSpine01')

    cmds.setAttr( (wireName[0]+".dropoffDistance[0]"), 20)

    firstJoint = points[0]

    lastJoint = points[(len(list)-1)]
    cmds.select(cl=True)
	# creates 3 joints to control the curve and in turn the Ribbon IK Spine
    cmds.joint(n='jDrv_spineBtm01',p=firstJoint)
    cmds.setAttr( "jDrv_spineBtm01.jointOrientX" ,90)
    cmds.setAttr( "jDrv_spineBtm01.jointOrientZ" ,90)
    cmds.select(cl=True)
    cmds.joint(n='jDrv_spineTop01',p=lastJoint)
    cmds.setAttr( "jDrv_spineTop01.jointOrientX" ,90)
    cmds.setAttr( "jDrv_spineTop01.jointOrientZ" ,90)
    cmds.select(cl=True)
    cmds.joint(n='jDrv_spineMiddle01')
    cmds.setAttr( "jDrv_spineMiddle01.jointOrientX" ,90)
    cmds.setAttr( "jDrv_spineMiddle01.jointOrientZ" ,90)
    cmds.delete(cmds.pointConstraint('jDrv_spineBtm01','jDrv_spineTop01','jDrv_spineMiddle01'))
    
    skinClusterName = cmds.skinCluster('crv_wireSpine01','jDrv_spineBtm01','jDrv_spineTop01','jDrv_spineMiddle01',n='def_skinSpineCrv01')

    cmds.select( 'jDrv_spineBtm01', 'jDrv_spineTop01', 'jDrv_spineMiddle01', r=True )
    cmds.group(n='grp_spineDrv_jnts01')
	# creates a twist deformer to get natural twistin up and down the spine
    twist = cmds.nonLinear('bShps_spine01',n='defssss', type='twist')
    name = cmds.rename(twist[1],'def_spineTwistHandle01')
    print twist[0]

    #name = cmds.rename(twist[0],'def_twistSpine01')
	# uses the arc length to correction scale the twist handle
    arcLengthName = cmds.arclen('crv_wireSpine01',ch=True,n='length_wireSpine01')
    arclength = cmds.getAttr((arcLengthName+'.arcLength'))
    curveLength = arclength/2
	# aligns the twist handle to face up and down the spine
    cmds.select('jDrv_spineTop01','def_spineTwistHandle01',r=True)
    cmds.delete(cmds.aimConstraint(aim=(0,-1,0)))

    cmds.setAttr("def_spineTwistHandle01.scaleZ", curveLength)
    cmds.setAttr("def_spineTwistHandle01.scaleX", curveLength)
    cmds.setAttr("def_spineTwistHandle01.scaleY", curveLength)

    cmds.connectAttr('jDrv_spineTop01.rx',(twist[0]+".startAngle"))
    cmds.connectAttr('jDrv_spineBtm01.rx',(twist[0]+".endAngle"))
	
	# reorders the deformers so the twist still works even then the spine is bent
	
    cmds.reorderDeformers(wireName[0], twist[0], 'bShps_spine01')
    
    cmds.group('crv_wireSpine01', 'surf_spine01', 'grpFlcs_spine01', 'bShps_spine01', 'crv_wireSpine01BaseWire', 'grp_spineDrv_jnts01', 'def_spineTwistHandle01',n='grp_spineSystem01')
    cmds.parent('grp_spineSystem01','ExtraNodes01')

    # creating all the controls for the rig using the controller class previously defined 

def createControls():

    nullRotation = 0.0,0.0,0.0

    nullPos = 0,0,0

    offsetFalse = False

    offsetTrue = True


    ### SPINE, PELVIS CONTROLS for both IK and FK 

    COGRot = 0.0,0.0,90.0

    ctrlCentreOfGravity = control('ctrl_COG01',nullPos,COGRot,'square')

    ctrlCentreOfGravity.create()

    cmds.scale(5,1,3,ctrlCentreOfGravity.ctrlName)

    cmds.makeIdentity(ctrlCentreOfGravity.ctrlName, a=True, s = True)

    ctrlCentreOfGravity.alignToJoint('jBn_pelvis01')

    ctrlCentreOfGravity.parent('Controls01')

    ctrlCentreOfGravity.constrainTo('grp_spineDrv_jnts01','parent',offsetTrue)
    cmds.scaleConstraint(ctrlCentreOfGravity.ctrlName,'grp_spineDrv_jnts01')




    ctrlSpineA_FK = control('ctrl_spineFK_a01',nullPos,nullRotation,'circle')

    ctrlSpineA_FK.create()

    cmds.scale(2,2,2,ctrlSpineA_FK.ctrlName)

    cmds.makeIdentity(ctrlSpineA_FK.ctrlName, a=True, s = True)



    ctrlSpineA_FK.alignToJoint('jDrv_spineBtm01')

    ctrlSpineA_FK.constrainTo('jDrv_spineBtm01','parent',offsetFalse)

    ctrlSpineA_FK.constrainTo('jBn_pelvis01','point',offsetFalse)


    ctrlSpineA_FK.parent('ctrl_COG01')


    ctrlSpineB_Fk = control('ctrl_spineFK_b01',nullPos,nullRotation,'circle')

    ctrlSpineB_Fk.create()

    cmds.scale(2,2,2,ctrlSpineB_Fk.ctrlName)

    cmds.makeIdentity(ctrlSpineB_Fk.ctrlName, a=True, s = True)


    ctrlSpineB_Fk.alignToJoint('jDrv_spineMiddle01')

    ctrlSpineB_Fk.constrainTo('jDrv_spineMiddle01','orient',offsetFalse)

    ctrlSpineB_Fk.parent('ctrl_spineFK_a01')


    ctrlSpineC_Fk = control('ctrl_spineFK_c01',nullPos,nullRotation,'circle')

    ctrlSpineC_Fk.create()

    cmds.scale(2,2,2,ctrlSpineC_Fk.ctrlName)

    cmds.makeIdentity(ctrlSpineC_Fk.ctrlName, a=True, s = True)


    ctrlSpineC_Fk.alignToJoint('jDrv_spineTop01')

    ctrlSpineC_Fk.constrainTo('jDrv_spineTop01','orient',offsetFalse)

    cmds.orientConstraint('ctrl_spineFK_c01','jBn_chest01',mo=True)

    ctrlSpineC_Fk.parent('ctrl_spineFK_b01')

    ctrlSpineB_IK = control('ctrl_spineIK_b01',nullPos,nullRotation,'square')

    ctrlSpineB_IK.create()

    cmds.scale(3,3,3,ctrlSpineB_IK.ctrlName)

    cmds.makeIdentity(ctrlSpineB_IK.ctrlName, a=True, s = True)

    ctrlSpineB_IK.alignToJoint('jDrv_spineMiddle01')

    ctrlSpineB_IK.constrainTo('jDrv_spineMiddle01','point',offsetFalse)

    ctrlSpineB_IK.parent('ctrl_spineFK_b01')


    ctrlSpineC_IK = control('ctrl_spineIK_c01',nullPos,nullRotation,'square')

    ctrlSpineC_IK.create()

    cmds.scale(3,3,3,ctrlSpineC_IK.ctrlName)

    cmds.makeIdentity(ctrlSpineC_IK.ctrlName, a=True, s = True)

    ctrlSpineC_IK.alignToJoint('jDrv_spineTop01')

    ctrlSpineC_IK.constrainTo('jDrv_spineTop01','point',offsetFalse)

    ctrlSpineC_IK.parent('ctrl_spineFK_c01')

    ctrlSpineC_IK.constrainTo('jBn_chest01','point',offsetFalse)

    footRotation = [0.0,0.0,90.0]

    pelvisRotation = [90.0,0.0,0.0]
    pelvisPos = [0.0,0.0,0.0]
    ctrlPelvis = control('ctrl_pelvis01',pelvisPos,pelvisRotation,'pin')

    ctrlPelvis.create()

    ctrlPelvis.alignToJoint('jBn_pelvis01')

    ctrlPelvis.constrainTo('jBn_pelvis01','orient',offsetFalse)

    cmds.scale(4,4,4,ctrlPelvis.ctrlName)

    cmds.makeIdentity(ctrlPelvis.ctrlName, a=True, s = True)

    ctrlPelvis.parent('ctrl_spineFK_a01')



    ### IK HANDS AND FEET CONTROLS

    L_ctrlWrist = control('ctrl_l_wrist01',nullPos,nullRotation,'circle')

    L_ctrlWrist.create()

    L_ctrlWrist.alignToJoint('jBn_l_wrist01')

    L_ctrlWrist.constrainTo('jBn_l_wrist01','orient',offsetFalse)

    L_ctrlWrist.constrainTo('ikRp_l_arm01','point',offsetFalse)

    L_ctrlWrist.addAttributes('ik_fk','float',0,1,'Keyable')

    L_ctrlWrist.addAttributes('thumbRoll','float',-10,10,'Keyable')

    L_ctrlWrist.addAttributes('indexRoll','float',-10,10,'Keyable')

    L_ctrlWrist.addAttributes('middleRoll','float',-10,10,'Keyable')

    L_ctrlWrist.addAttributes('ringRoll','float',-10,10,'Keyable')

    L_ctrlWrist.addAttributes('pinkieRoll','float',-10,10,'Keyable')

    L_ctrlWrist.addAttributes('localSpace','enum',-10,10,'Keyable')

    L_ctrlWrist.parent('Controls01')


    R_ctrlWrist = control('ctrl_r_wrist01',nullPos,nullRotation,'circle')

    R_ctrlWrist.create()

    R_ctrlWrist.alignToJoint('jBn_r_wrist01')

    R_ctrlWrist.constrainTo('jBn_r_wrist01','orient',offsetFalse)

    R_ctrlWrist.constrainTo('ikRp_r_arm01','point',offsetFalse)

    R_ctrlWrist.addAttributes('ik_fk','float',0,1,'Keyable')

    R_ctrlWrist.addAttributes('thumbRoll','float',-10,10,'Keyable')

    R_ctrlWrist.addAttributes('indexRoll','float',-10,10,'Keyable')

    R_ctrlWrist.addAttributes('middleRoll','float',-10,10,'Keyable')

    R_ctrlWrist.addAttributes('ringRoll','float',-10,10,'Keyable')

    R_ctrlWrist.addAttributes('pinkieRoll','float',-10,10,'Keyable')

    R_ctrlWrist.addAttributes('localSpace','enum',0,10,'Keyable')


    L_anklePos = cmds.xform('jBn_l_ankle01',q=True,ws=True,rp=True)

    L_anklePos[1] = 0

    cmds.spaceLocator(n='locVrt_l_foot01',p=(L_anklePos))

    cmds.CenterPivot()


    L_anklePos = 0.0,0.0,6.0

    R_ctrlWrist.parent('Controls01')

    L_ctrlFoot = control('ctrl_l_ankle01',L_anklePos,footRotation,'square')

    L_ctrlFoot.create()

    cmds.scale(1,1,3,L_ctrlFoot.ctrlName)

    cmds.makeIdentity(L_ctrlFoot.ctrlName, a=True, s = True)

    L_ctrlFoot.alignToJoint('locVrt_l_foot01')



    L_ctrlFoot.addAttributes('ik_fk','float',0,1,'Keyable')

    L_ctrlFoot.addAttributes('FootRoll','float',-30,30,'Keyable')

    #L_ctrlFoot.addAttributes('BallRoll','float',-10,10,'Keyable')

    #L_ctrlFoot.addAttributes('ToeRoll','float',-10,10,'Keyable')

    #L_ctrlFoot.addAttributes('HeelRoll','float',-10,10,'Keyable')

    #L_ctrlFoot.addAttributes('ToeFlop','float',-10,10,'Keyable')

    L_ctrlFoot.addAttributes('localSpace','enum',-10,10,'Keyable')


    L_ctrlFoot.parent('Controls01')


    R_anklePos = cmds.xform('jBn_r_ankle01',q=True,ws=True,rp=True)

    R_anklePos[1] = 0

    cmds.spaceLocator(n='locVrt_r_foot01',p=(R_anklePos))

    cmds.CenterPivot()

    R_anklePos = 0.0,0.0,6.0


    R_ctrlFoot = control('ctrl_r_ankle01',R_anklePos,footRotation,'square')

    R_ctrlFoot.create()


    cmds.scale(1,1,3,R_ctrlFoot.ctrlName)

    cmds.makeIdentity(R_ctrlFoot.ctrlName, a=True, s = True)

    R_ctrlFoot.alignToJoint('locVrt_r_foot01')


    cmds.delete('locVrt_r_foot01','locVrt_l_foot01')


    R_ctrlFoot.addAttributes('ik_fk','float',0,1,'Keyable')

    R_ctrlFoot.addAttributes('FootRoll','float',-30,30,'Keyable')

    #R_ctrlFoot.addAttributes('BallRoll','float',-10,10,'Keyable')

    #R_ctrlFoot.addAttributes('ToeRoll','float',-10,10,'Keyable')

    #R_ctrlFoot.addAttributes('HeelRoll','float',-10,10,'Keyable')

    #R_ctrlFoot.addAttributes('ToeFlop','float',-10,10,'Keyable')

    R_ctrlFoot.addAttributes('localSpace','enum',-10,10,'Keyable')


    R_ctrlFoot.parent('Controls01')

    ### CLAVICLES 

    L_ctrlClavicle = control('ctrl_l_clavicle01',nullPos,nullRotation,'pin')

    L_ctrlClavicle.create()

    L_ctrlClavicle.alignToJoint('jBn_l_clavicle01')

    L_ctrlClavicle.constrainTo('jBn_l_clavicle01','orient',offsetFalse)


    L_ctrlClavicle.constrainTo('grp_l_ARM01','parent',offsetTrue)
    L_ctrlClavicle.constrainTo('grp_l_ARM_IK_01','parent',offsetTrue)
    L_ctrlClavicle.constrainTo('grp_l_ARM_FK_01','parent',offsetTrue)

    cmds.scale(2,2,2,L_ctrlClavicle.ctrlName)

    cmds.makeIdentity(L_ctrlClavicle.ctrlName, a=True, s = True)

    L_ctrlClavicle.parent('ctrl_spineFK_c01')




    rClavRot = 180.0,0.0,0.0
    R_ctrlClavicle = control('ctrl_r_clavicle01',nullPos,rClavRot,'pin')

    R_ctrlClavicle.create()

    R_ctrlClavicle.alignToJoint('jBn_r_clavicle01')

    R_ctrlClavicle.constrainTo('jBn_r_clavicle01','orient',offsetFalse)

    cmds.scale(2,2,2,R_ctrlClavicle.ctrlName)

    cmds.makeIdentity(R_ctrlClavicle.ctrlName, a=True, s = True)


    R_ctrlClavicle.parent('ctrl_spineFK_c01')


    R_ctrlClavicle.constrainTo('grp_r_ARM01','parent',offsetTrue)
    R_ctrlClavicle.constrainTo('grp_r_ARM_IK_01','parent',offsetTrue)
    R_ctrlClavicle.constrainTo('grp_r_ARM_FK_01','parent',offsetTrue)

    ### FK ARMS AND LEGS CONTROLS



    L_ctrlShoulder = control('ctrl_l_shoulder01',nullPos,nullRotation,'circle')

    L_ctrlShoulder.create()

    L_ctrlShoulder.alignToJoint('jDrv_FK_l_shoulder01')

    L_ctrlShoulder.constrainTo('jDrv_FK_l_shoulder01','orient',offsetFalse)

    L_ctrlShoulder.parent('ctrl_l_clavicle01')


    L_ctrlElbow = control('ctrl_l_elbow01',nullPos,nullRotation,'circle')

    L_ctrlElbow.create()

    L_ctrlElbow.alignToJoint('jDrv_FK_l_elbow01')

    L_ctrlElbow.constrainTo('jDrv_FK_l_elbow01','orient',offsetFalse)

    L_ctrlElbow.parent('ctrl_l_shoulder01')



    R_ctrlShoulder = control('ctrl_r_shoulder01',nullPos,nullRotation,'circle')

    R_ctrlShoulder.create()

    R_ctrlShoulder.alignToJoint('jDrv_FK_r_shoulder01')

    R_ctrlShoulder.constrainTo('jDrv_FK_r_shoulder01','orient',offsetFalse)

    R_ctrlShoulder.parent('ctrl_r_clavicle01')


    R_ctrlElbow = control('ctrl_r_elbow01',nullPos,nullRotation,'circle')

    R_ctrlElbow.create()

    R_ctrlElbow.alignToJoint('jDrv_FK_r_elbow01')

    R_ctrlElbow.constrainTo('jDrv_FK_r_elbow01','orient',offsetFalse)

    R_ctrlElbow.parent('ctrl_r_shoulder01')


    L_ctrlHip = control('ctrl_l_hip01',nullPos,nullRotation,'circle')


    L_ctrlHip.create()

    L_ctrlHip.alignToJoint('jDrv_FK_l_hip01')

    L_ctrlHip.constrainTo('jDrv_FK_l_hip01','orient',offsetFalse)

    L_ctrlHip.parent('Controls01')


    L_ctrlElbow = control('ctrl_l_knee01',nullPos,nullRotation,'circle')

    L_ctrlElbow.create()

    L_ctrlElbow.alignToJoint('jDrv_FK_l_shin01')

    L_ctrlElbow.constrainTo('jDrv_FK_l_shin01','orient',offsetFalse)

    L_ctrlElbow.parent('ctrl_l_hip01')




    R_ctrlShoulder = control('ctrl_r_hip01',nullPos,nullRotation,'circle')

    R_ctrlShoulder.create()

    R_ctrlShoulder.alignToJoint('jDrv_FK_r_hip01')

    R_ctrlShoulder.constrainTo('jDrv_FK_r_hip01','orient',offsetFalse)

    R_ctrlShoulder.parent('Controls01')


    R_ctrlElbow = control('ctrl_r_knee01',nullPos,nullRotation,'circle')

    R_ctrlElbow.create()

    R_ctrlElbow.alignToJoint('jDrv_FK_r_shin01')

    R_ctrlElbow.constrainTo('jDrv_FK_r_shin01','orient',offsetFalse)

    R_ctrlElbow.parent('ctrl_r_hip01')


    cmds.group('ctrl_l_wrist01',n='grpOfs_IK_l_wrist01')
    cmds.parentConstraint('ctrl_l_elbow01', 'grpOfs_IK_l_wrist01',mo=True,w=0.0)


    cmds.group('ctrl_r_wrist01',n='grpOfs_IK_r_wrist01')
    cmds.parentConstraint('ctrl_r_elbow01', 'grpOfs_IK_r_wrist01',mo=True,w=0.0)


    cmds.group('ctrl_l_ankle01',n='grpOfs_IK_l_ankle01')
    cmds.parentConstraint('ctrl_l_knee01', 'grpOfs_IK_l_ankle01',mo=True,w=0.0)


    cmds.group('ctrl_r_ankle01',n='grpOfs_IK_r_ankle01')
    cmds.parentConstraint('ctrl_r_knee01', 'grpOfs_IK_r_ankle01',mo=True,w=0.0)
    ### NECK AND HEAD CONTROLS

    ctrlNeck = control('ctrl_neck01',nullPos,nullRotation,'circle')

    ctrlNeck.create()

    ctrlNeck.alignToJoint('jBn_neck01')

    ctrlNeck.constrainTo('jBn_neck01','orient',offsetFalse)

    ctrlNeck.parent('ctrl_spineFK_c01')



    ctrlHead = control('ctrl_head01',nullPos,nullRotation,'circle')

    ctrlHead.create()

    ctrlHead.alignToJoint('jBn_head01')

    ctrlHead.constrainTo('jBn_head01','orient',offsetFalse)

    ctrlHead.parent('ctrl_neck01')


    l_WristLoc = jointLocators('locVrt_l_wrist01', 0, 0, 0,'UP')

    cmds.parent('locVrt_l_wrist01','Controls01')

    cmds.parentConstraint('ctrl_COG01','grpctrl_l_wrist01',w=0,mo=True)
    cmds.parentConstraint('ctrl_spineFK_c01','grpctrl_l_wrist01',w=0,mo=True)
    cmds.parentConstraint('ctrl_spineFK_a01','grpctrl_l_wrist01',w=0,mo=True)
    cmds.parentConstraint('ctrl_head01','grpctrl_l_wrist01',w=0,mo=True)
    cmds.parentConstraint('locVrt_l_wrist01','grpctrl_l_wrist01',w=0,mo=True)

    r_WristLoc = jointLocators('locVrt_r_wrist01', 0, 0, 0,'UP')


    cmds.parent('locVrt_r_wrist01','Controls01')

    cmds.parentConstraint('ctrl_COG01','grpctrl_r_wrist01',w=0,mo=True)
    cmds.parentConstraint('ctrl_spineFK_c01','grpctrl_r_wrist01',w=0,mo=True)
    cmds.parentConstraint('ctrl_spineFK_a01','grpctrl_r_wrist01',w=0,mo=True)
    cmds.parentConstraint('ctrl_head01','grpctrl_r_wrist01',w=0,mo=True)
    cmds.parentConstraint('locVrt_r_wrist01','grpctrl_r_wrist01',w=0,mo=True)





    l_AnkleLoc = jointLocators('locVrt_l_ankle01', 0, 0, 0,'UP')

    cmds.parent('locVrt_l_ankle01','Controls01')

    cmds.parentConstraint('ctrl_COG01','grpctrl_l_ankle01',w=0,mo=True)
    cmds.parentConstraint('ctrl_spineFK_c01','grpctrl_l_ankle01',w=0,mo=True)
    cmds.parentConstraint('ctrl_spineFK_a01','grpctrl_l_ankle01',w=0,mo=True)
    cmds.parentConstraint('ctrl_head01','grpctrl_l_ankle01',w=0,mo=True)
    cmds.parentConstraint('locVrt_l_ankle01','grpctrl_l_ankle01',w=0,mo=True)

    r_AnkleLoc = jointLocators('locVrt_r_ankle01', 0, 0, 0,'UP')


    cmds.parent('locVrt_r_ankle01','Controls01')

    cmds.parentConstraint('ctrl_COG01','grpctrl_r_ankle01',w=0,mo=True)
    cmds.parentConstraint('ctrl_spineFK_c01','grpctrl_r_ankle01',w=0,mo=True)
    cmds.parentConstraint('ctrl_spineFK_a01','grpctrl_r_ankle01',w=0,mo=True)
    cmds.parentConstraint('ctrl_head01','grpctrl_r_ankle01',w=0,mo=True)
    cmds.parentConstraint('locVrt_r_ankle01','grpctrl_r_ankle01',w=0,mo=True)



    ### Reverse Foot Rig

    footReferenceLocs ='locRefCtrl_r_Heel01','locRefCtrl_r_tiltLeft01','locRefCtrl_r_tiltRight01','locRefCtrl_l_Heel01','locRefCtrl_l_tiltLeft01','locRefCtrl_l_tiltRight01','jBn_l_ball01','jBn_l_toe01','jBn_l_ankle01','jBn_r_ball01','jBn_r_toe01','jBn_r_ankle01'

    footRollDrivers = []

    for x in footReferenceLocs :
        locName = x.replace('locRefCtrl','locDrv')
        print locName
        locName = locName.replace('jBn','locDrv')
        print locName
        cmds.spaceLocator(n=locName)
        cmds.group(locName,n=('grp'+locName))
        cmds.delete(cmds.parentConstraint(x,('grp'+locName),mo=False))
        footRollDrivers.append(locName)
    cmds.select('*locRefCtrl*',r=True)
    cmds.delete()

    cmds.parent('grplocDrv_l_ankle01','locDrv_l_ball01')
    cmds.parent('grplocDrv_l_ball01','locDrv_l_toe01')
    cmds.parent('grplocDrv_l_toe01','locDrv_l_Heel01')
    cmds.parent('grplocDrv_l_Heel01','locDrv_l_tiltLeft01')
    cmds.parent('grplocDrv_l_tiltLeft01','locDrv_l_tiltRight01')
    cmds.parent('grplocDrv_l_tiltRight01','ctrl_l_ankle01')

    cmds.parent('grplocDrv_r_ankle01','locDrv_r_ball01')
    cmds.parent('grplocDrv_r_ball01','locDrv_r_toe01')
    cmds.parent('grplocDrv_r_toe01','locDrv_r_Heel01')
    cmds.parent('grplocDrv_r_Heel01','locDrv_r_tiltLeft01')
    cmds.parent('grplocDrv_r_tiltLeft01','locDrv_r_tiltRight01')
    cmds.parent('grplocDrv_r_tiltRight01','ctrl_r_ankle01')


    cmds.orientConstraint('locDrv_l_ball01','jBn_l_ankle01',mo=True)
    cmds.orientConstraint('locDrv_l_toe01','jBn_l_ball01',mo=True)

    cmds.orientConstraint('locDrv_r_ball01','jBn_r_ankle01',mo=True)
    cmds.orientConstraint('locDrv_r_toe01','jBn_r_ball01',mo=True)




    L_ctrlBall = control('ctrl_l_ball01',nullPos,nullRotation,'pin')

    L_ctrlBall.create()

    L_ctrlBall.offSetGrp()

    L_ctrlBall.alignToJoint('jBn_l_ball01')

    L_ctrlBall.constrainTo('locDrv_l_ball01','orient',offsetTrue)


    L_ctrlToe = control('ctrl_l_toe01',nullPos,nullRotation,'pin')

    L_ctrlToe.create()

    L_ctrlToe.offSetGrp()


    L_ctrlToe.alignToJoint('jBn_l_toe01')

    L_ctrlToe.constrainTo('locDrv_l_toe01','orient',offsetFalse)

    L_ctrlBall.parent('ctrl_l_toe01')

    footSquareRot = 0.0,0.0,90.0
    footSquarePos = 0.0,0.0,0.0


    L_ctrlHeel = control('ctrl_l_heel01',nullPos,footSquareRot,'square')

    L_ctrlHeel.create()

    L_ctrlHeel.offSetGrp()


    cmds.scale(0.5,0.5,0.5,L_ctrlHeel.ctrlName)

    cmds.makeIdentity(L_ctrlHeel.ctrlName, a=True, s = True)


    L_ctrlHeel.alignToJoint('locDrv_l_Heel01')

    L_ctrlHeel.constrainTo('locDrv_l_Heel01','orient',offsetFalse)

    L_ctrlToe.parent('ctrl_l_heel01')



    L_ctrlTiltLeft = control('ctrl_l_tiltLeft01',nullPos,footSquareRot,'square')

    L_ctrlTiltLeft.create()

    L_ctrlTiltLeft.offSetGrp()


    cmds.scale(0.5,0.5,0.5,L_ctrlTiltLeft.ctrlName)

    cmds.makeIdentity(L_ctrlTiltLeft.ctrlName, a=True, s = True)

    L_ctrlTiltLeft.alignToJoint('locDrv_l_tiltLeft01')

    L_ctrlTiltLeft.constrainTo('locDrv_l_tiltLeft01','orient',offsetFalse)

    L_ctrlHeel.parent('ctrl_l_tiltLeft01')



    L_ctrlTiltRight = control('ctrl_l_tiltRight01',nullPos,footSquareRot,'square')

    L_ctrlTiltRight.create()

    L_ctrlTiltRight.offSetGrp()


    cmds.scale(0.5,0.5,0.5,L_ctrlTiltRight.ctrlName)

    cmds.makeIdentity(L_ctrlTiltRight.ctrlName, a=True, s = True)

    L_ctrlTiltRight.alignToJoint('locDrv_l_tiltRight01')

    L_ctrlTiltRight.constrainTo('locDrv_l_tiltRight01','orient',offsetFalse)

    L_ctrlTiltLeft.parent('ctrl_l_tiltRight01')
    L_ctrlTiltRight.parent('ctrl_l_ankle01')

    r_rotation = 0.0,0.0,180.0

    R_ctrlBall = control('ctrl_r_ball01',nullPos,r_rotation,'pin')

    R_ctrlBall.create()

    R_ctrlBall.offSetGrp()


    R_ctrlBall.alignToJoint('jBn_r_ball01')

    R_ctrlBall.constrainTo('locDrv_r_ball01','orient',offsetFalse)


    R_ctrlToe = control('ctrl_r_toe01',nullPos,r_rotation,'pin')

    R_ctrlToe.create()

    R_ctrlToe.offSetGrp()


    R_ctrlToe.alignToJoint('jBn_r_toe01')

    R_ctrlToe.constrainTo('locDrv_r_toe01','orient',offsetFalse)

    R_ctrlBall.parent('ctrl_r_toe01')


    R_ctrlHeel = control('ctrl_r_heel01',nullPos,footSquareRot,'square')

    R_ctrlHeel.create()

    R_ctrlHeel.offSetGrp()


    cmds.scale(0.5,0.5,0.5,R_ctrlHeel.ctrlName)

    cmds.makeIdentity(R_ctrlHeel.ctrlName, a=True, s = True)

    R_ctrlHeel.alignToJoint('locDrv_r_Heel01')

    R_ctrlHeel.constrainTo('locDrv_r_Heel01','orient',offsetFalse)

    R_ctrlToe.parent('ctrl_r_heel01')



    R_ctrlTiltLeft = control('ctrl_r_tiltLeft01',nullPos,footSquareRot,'square')

    R_ctrlTiltLeft.create()

    R_ctrlTiltLeft.offSetGrp()


    cmds.scale(0.5,0.5,0.5,R_ctrlTiltLeft.ctrlName)

    cmds.makeIdentity(R_ctrlTiltLeft.ctrlName, a=True, s = True)

    R_ctrlTiltLeft.alignToJoint('locDrv_r_tiltLeft01')

    R_ctrlTiltLeft.constrainTo('locDrv_r_tiltLeft01','orient',offsetFalse)

    R_ctrlHeel.parent('ctrl_r_tiltLeft01')



    R_ctrlTiltRight = control('ctrl_r_tiltRight01',nullPos,footSquareRot,'square')

    R_ctrlTiltRight.create()

    R_ctrlTiltRight.offSetGrp()


    cmds.scale(0.5,0.5,0.5,R_ctrlTiltRight.ctrlName)

    cmds.makeIdentity(R_ctrlTiltRight.ctrlName, a=True, s = True)

    R_ctrlTiltRight.alignToJoint('locDrv_r_tiltRight01')

    R_ctrlTiltRight.constrainTo('locDrv_r_tiltRight01','orient',offsetFalse)

    R_ctrlTiltLeft.parent('ctrl_r_tiltRight01')


    R_ctrlTiltRight.parent('ctrl_r_ankle01')


    cmds.pointConstraint('locDrv_l_ankle01','ikRp_l_leg01')
    cmds.pointConstraint('locDrv_r_ankle01','ikRp_r_leg01')

    ### SDK ###

    influences = ['ctrl_COG01','ctrl_spineFK_c01','ctrl_spineFK_a01','ctrl_head01','locVrt_l_wrist01']
    IK_controls = ['ctrl_l_wrist01','ctrl_r_wrist01','ctrl_l_ankle01','ctrl_r_ankle01']

    v1 = 0,1,0,0,0,0
    v2 = 0,0,1,0,0,0
    v3 = 0,0,0,1,0,0
    v4 = 0,0,0,0,1,0
    v5 = 0,0,0,0,0,1
    LorR = '_l_','_r_'

    for y in range(4) :
        
        for x in range(6) :
            
            cmds.setDrivenKeyframe(('grp'+IK_controls[y]+'_parentConstraint1'),at ='.ctrl_COG01W0',v=(v1[x]) ,currentDriver= (IK_controls[y]+'.localSpace'),dv=x)
            cmds.setDrivenKeyframe(('grp'+IK_controls[y]+'_parentConstraint1'),at ='.ctrl_spineFK_c01W1',v=(v2[x]) ,currentDriver= (IK_controls[y]+'.localSpace'),dv=x)
            cmds.setDrivenKeyframe(('grp'+IK_controls[y]+'_parentConstraint1'),at ='.ctrl_spineFK_a01W2',v=(v3[x]) ,currentDriver= (IK_controls[y]+'.localSpace'),dv=x)
            cmds.setDrivenKeyframe(('grp'+IK_controls[y]+'_parentConstraint1'),at ='.ctrl_head01W3',v=(v4[x]) ,currentDriver= (IK_controls[y]+'.localSpace'),dv=x)

    for x in range(6):

        cmds.setDrivenKeyframe(('grpctrl_l_wrist01_parentConstraint1'),at ='.locVrt_l_wrist01W4',v=(v5[x]) ,currentDriver= ('ctrl_l_wrist01.localSpace'),dv=x)
        cmds.setDrivenKeyframe(('grpctrl_r_wrist01_parentConstraint1'),at ='.locVrt_r_wrist01W4',v=(v5[x]) ,currentDriver= ('ctrl_r_wrist01.localSpace'),dv=x)
        cmds.setDrivenKeyframe(('grpctrl_l_ankle01_parentConstraint1'),at ='.locVrt_l_ankle01W4',v=(v5[x]) ,currentDriver= ('ctrl_l_ankle01.localSpace'),dv=x)
        cmds.setDrivenKeyframe(('grpctrl_r_ankle01_parentConstraint1'),at ='.locVrt_r_ankle01W4',v=(v5[x]) ,currentDriver= ('ctrl_r_ankle01.localSpace'),dv=x)


    # foot Roll SDK

    for x in range(2):
        
        cmds.setDrivenKeyframe(('grpOfs_ctrl'+LorR[x]+'ball01'),at ='.rz',v=(0.0) ,currentDriver= ('ctrl'+LorR[x]+'ankle01.FootRoll'),dv=0.0)
        cmds.setDrivenKeyframe(('grpOfs_ctrl'+LorR[x]+'ball01'),at ='.rz',v=(-30.0) ,currentDriver= ('ctrl'+LorR[x]+'ankle01.FootRoll'),dv=15.0)
        cmds.setDrivenKeyframe(('grpOfs_ctrl'+LorR[x]+'ball01'),at ='.rz',v=(60.0) ,currentDriver= ('ctrl'+LorR[x]+'ankle01.FootRoll'),dv=30.0)


        cmds.setDrivenKeyframe(('grpOfs_ctrl'+LorR[x]+'toe01'),at ='.rz',v=(0.0) ,currentDriver= ('ctrl'+LorR[x]+'ankle01.FootRoll'),dv=0.0)
        cmds.setDrivenKeyframe(('grpOfs_ctrl'+LorR[x]+'toe01'),at ='.rz',v=(0.0) ,currentDriver= ('ctrl'+LorR[x]+'ankle01.FootRoll'),dv=15.0)
        cmds.setDrivenKeyframe(('grpOfs_ctrl'+LorR[x]+'toe01'),at ='.rz',v=(-60.0) ,currentDriver= ('ctrl'+LorR[x]+'ankle01.FootRoll'),dv=30.0)


        cmds.setDrivenKeyframe(('grpOfs_ctrl'+LorR[x]+'heel01'),at ='.rx',v=(0.0) ,currentDriver= ('ctrl'+LorR[x]+'ankle01.FootRoll'),dv=0.0)
        cmds.setDrivenKeyframe(('grpOfs_ctrl'+LorR[x]+'heel01'),at ='.rx',v=(-60.0) ,currentDriver= ('ctrl'+LorR[x]+'ankle01.FootRoll'),dv=-30.0)
        
        cmds.setDrivenKeyframe(('grpOfs_ctrl'+LorR[x]+'toe01'),at ='.rz',v=(0.0) ,currentDriver= ('ctrl'+LorR[x]+'ankle01.FootRoll'),dv=0.0)
        





    # Loop to create all the controls for the fingers and parent them appropriately 

    parentName = 'Controls01'

    count = 0

    fingers = '*l_thumb*','*l_index*','*l_middle*','*l_ring*','*l_pinkie*','*r_thumb*','*r_index*','*r_middle*','*r_ring*','*r_pinkie*'

    for finger in fingers :
        cmds.select(finger,hi=True)
        listDigits = cmds.ls(sl=True,type='joint')
        
        for digit in listDigits:
            ctrlName = digit.replace('jBn','ctrl')
            
            ctrlFinger = control(ctrlName,nullPos,nullRotation,'pin')
            ctrlFinger.create()
            ctrlFinger.offSetGrp()
            
            ctrlFinger.alignToJoint(digit)
            ctrlFinger.constrainTo(digit,'orient',offsetFalse)
            
            ctrlFinger.parent(parentName)
            parentName = ctrlName
            
            cmds.setAttr( (ctrlName+".tx"),lock=True,k=False,cb=False)
            cmds.setAttr( (ctrlName+".ty"),lock=True,k=False,cb=False)
            cmds.setAttr( (ctrlName+".tz"),lock=True,k=False,cb=False)
            
        
        parentName = 'Controls01'
        if count < 5 :
            cmds.parent(('grpctrl_'+finger+'_metacarpal01'),'ctrl_l_wrist01')
        else :
            cmds.parent(('grpctrl_'+finger+'_metacarpal01'),'ctrl_r_wrist01')
        cmds.parent(('grpctrl_'+finger+'_a01'),('ctrl_'+finger+'_metacarpal01'))
        
        
        cmds.setAttr( (ctrlName+".tx"),lock=True,k=False,cb=False)
        cmds.setAttr( (ctrlName+".ty"),lock=True,k=False,cb=False)
        cmds.setAttr( (ctrlName+".tz"),lock=True,k=False,cb=False)

        
        count = count + 1
        
    fingers ='thumb','index','middle','ring','pinkie'
    digits = '_a','_b','_c',
    thumbdigits = '_metacarpal','_a','_b'
    for i in range(2):
        for x in fingers:
            if x == 'thumb' :
                for y in thumbdigits:
                    cmds.setDrivenKeyframe(('grpOfs_ctrl'+LorR[i]+x+y+'01'),at ='.ry',v=(0.0) ,currentDriver= ('ctrl'+LorR[i]+'wrist01.'+x+'Roll'),dv=0.0)
                    cmds.setDrivenKeyframe(('grpOfs_ctrl'+LorR[i]+x+y+'01'),at ='.ry',v=(-60.0) ,currentDriver= ('ctrl'+LorR[i]+'wrist01.'+x+'Roll'),dv=10.0)
                    cmds.setDrivenKeyframe(('grpOfs_ctrl'+LorR[i]+x+y+'01'),at ='.ry',v=(60.0) ,currentDriver= ('ctrl'+LorR[i]+'wrist01.'+x+'Roll'),dv=-10.0)
            else:
                for y in digits:
                    cmds.setDrivenKeyframe(('grpOfs_ctrl'+LorR[i]+x+y+'01'),at ='.rz',v=(0.0) ,currentDriver= ('ctrl'+LorR[i]+'wrist01.'+x+'Roll'),dv=0.0)
                    cmds.setDrivenKeyframe(('grpOfs_ctrl'+LorR[i]+x+y+'01'),at ='.rz',v=(60.0) ,currentDriver= ('ctrl'+LorR[i]+'wrist01.'+x+'Roll'),dv=10.0)
                    cmds.setDrivenKeyframe(('grpOfs_ctrl'+LorR[i]+x+y+'01'),at ='.rz',v=(-60.0) ,currentDriver= ('ctrl'+LorR[i]+'wrist01.'+x+'Roll'),dv=-10.0)


        
    arm = 'shoulder', 'elbow','wrist'
    leg = 'hip', 'shin','ankle'
    mirrorAXIS = '_l_','_r_'
    limbs = '_leftARM_','_rightARM_','_leftLEG_','_rightLEG_'
    ## defines a function for creating the IK / FK system

def createIKFKSYSTEMS():

    def IKFKSystem(limb,axis,Chain,ik) :
        
        cmds.parentConstraint(('jDrv_IK'+axis+Chain[0]+'01'), ('jDrv_FK'+axis+Chain[0]+'01'), ('jBn'+axis+Chain[0]+'01'),skipTranslate=['x','y','z'],weight=1)
        cmds.parentConstraint(('jDrv_IK'+axis+Chain[1]+'01'), ('jDrv_FK'+axis+Chain[1]+'01'), ('jBn'+axis+Chain[1]+'01'))
        #cmds.parentConstraint(('jDrv_IK'+axis+Chain[2]+'01'), ('jDrv_FK'+axis+Chain[2]+'01'), ('jBn'+axis+Chain[2]+'01'))

        cmds.select(cl=True)
            
        cmds.shadingNode('condition', asUtility=True,n=('cond'+axis+limb+'ikFkSwap01'))
        # cmds.rename( ('cond'+axis+limb+'ikFkSwap01') )

        cmds.setAttr( ('cond'+axis+limb+'ikFkSwap01.operation'), 0)

        cmds.setAttr( ('cond'+axis+limb+'ikFkSwap01.firstTerm'), 0)
        cmds.setAttr( ('cond'+axis+limb+'ikFkSwap01.secondTerm'), 0)

        cmds.setAttr( ('cond'+axis+limb+'ikFkSwap01.colorIfTrueR'), 0)
        cmds.setAttr(('cond'+axis+limb+'ikFkSwap01.colorIfTrueG') ,1)

        cmds.setAttr( ('cond'+axis+limb+'ikFkSwap01.colorIfFalseR') ,1)
        cmds.setAttr( ('cond'+axis+limb+'ikFkSwap01.colorIfFalseG') ,0)

        cmds.connectAttr(  ('ctrl'+axis+Chain[2]+'01.ik_fk'), ('cond'+axis+limb+'ikFkSwap01.firstTerm'))

        cmds.connectAttr(  ('cond'+axis+limb+'ikFkSwap01.outColorR'), ('jBn'+axis+Chain[0]+'01_parentConstraint1.jDrv_IK'+axis+Chain[0]+'01W0'))
        cmds.connectAttr(  ('cond'+axis+limb+'ikFkSwap01.outColorG') ,('jBn'+axis+Chain[0]+'01_parentConstraint1.jDrv_FK'+axis+Chain[0]+'01W1'))

        cmds.connectAttr(  ('cond'+axis+limb+'ikFkSwap01.outColorR') ,('jBn'+axis+Chain[1]+'01_parentConstraint1.jDrv_IK'+axis+Chain[1]+'01W0'))
        cmds.connectAttr(  ('cond'+axis+limb+'ikFkSwap01.outColorG') ,('jBn'+axis+Chain[1]+'01_parentConstraint1.jDrv_FK'+axis+Chain[1]+'01W1'))


        cmds.connectAttr(  ('ctrl'+axis+Chain[2]+'01.ik_fk'), ('ikRp'+axis+ik+'01.ikBlend'))
        cmds.connectAttr(('cond'+axis+limb+'ikFkSwap01.outColorR') ,('jDrv_IK'+axis+Chain[0]+'01.v'))
        cmds.connectAttr(('cond'+axis+limb+'ikFkSwap01.outColorG') ,('jDrv_FK'+axis+Chain[0]+'01.v'))
        #cmds.connectAttr(  ('cond'+axis+limb+'ikFkSwap01.outColorR') ,('jBn'+axis+Chain[2]+'01_parentConstraint1.jDrv_IK'+axis+Chain[2]+'01W0'))
        #cmds.connectAttr(  ('cond'+axis+limb+'ikFkSwap01.outColorG') ,('jBn'+axis+Chain[2]+'01_parentConstraint1.jDrv_FK'+axis+Chain[2]+'01W1'))

    a = 0
    b = 2


    # runs the IK AND FK system function for each arm and leg
    for x in mirrorAXIS:
        
        IKFKSystem(limbs[a],x,arm,'arm')
        IKFKSystem(limbs[b],x,leg,'leg')
        a = a+1
        b = b+1

def polishRig(Input_RigPrefix):
    cmds.parent('Ctrl_IK_l_elbow01', 'Ctrl_IK_r_elbow01', 'Ctrl_IK_l_shin01', 'Ctrl_IK_r_shin01', 'Controls01')


    cmds.group('Ctrl_IK_l_elbow01',n='grpCtrl_IK_l_elbow01')
    cmds.group('Ctrl_IK_r_elbow01',n='grpCtrl_IK_r_elbow01')

    cmds.group('Ctrl_IK_l_shin01',n='grpCtrl_IK_l_shin01')
    cmds.group('Ctrl_IK_r_shin01',n='grpCtrl_IK_r_shin01')


    cmds.parentConstraint('ctrl_l_ankle01','grpCtrl_IK_l_shin01', mo=True)
    cmds.parentConstraint('ctrl_r_ankle01','grpCtrl_IK_r_shin01', mo=True)

    cmds.parentConstraint('ctrl_l_wrist01','grpCtrl_IK_l_elbow01', mo=True)

    cmds.parentConstraint('ctrl_r_wrist01','grpCtrl_IK_r_elbow01', mo=True)


    cmds.connectAttr('cond_l__leftARM_ikFkSwap01.outColorG','grpOfs_IK_l_wrist01_parentConstraint1.ctrl_l_elbow01W0')

    cmds.connectAttr('cond_r__rightARM_ikFkSwap01.outColorG','grpOfs_IK_r_wrist01_parentConstraint1.ctrl_r_elbow01W0')

    cmds.connectAttr('cond_l__leftLEG_ikFkSwap01.outColorG','grpOfs_IK_l_ankle01_parentConstraint1.ctrl_l_knee01W0')

    cmds.connectAttr('cond_r__rightLEG_ikFkSwap01.outColorG','grpOfs_IK_r_ankle01_parentConstraint1.ctrl_r_knee01W0')


    cmds.connectAttr('cond_l__leftARM_ikFkSwap01.outColorG','grpctrl_l_shoulder01.v')

    cmds.connectAttr('cond_r__rightARM_ikFkSwap01.outColorG','grpctrl_r_shoulder01.v')

    cmds.connectAttr('cond_l__leftLEG_ikFkSwap01.outColorG','grpctrl_l_hip01.v')

    cmds.connectAttr('cond_r__rightLEG_ikFkSwap01.outColorG','grpctrl_r_hip01.v')



    cmds.connectAttr('cond_l__leftARM_ikFkSwap01.outColorR','grpCtrl_IK_l_elbow01.v')

    cmds.connectAttr('cond_r__rightARM_ikFkSwap01.outColorR','grpCtrl_IK_r_elbow01.v')

    cmds.connectAttr('cond_l__leftLEG_ikFkSwap01.outColorR','grpCtrl_IK_l_shin01.v')

    cmds.connectAttr('cond_r__rightLEG_ikFkSwap01.outColorR','grpCtrl_IK_r_shin01.v')


    cmds.connectAttr('grpctrl_l_wrist01_parentConstraint1.locVrt_l_wrist01W4','locVrt_l_wrist01.v')
    cmds.connectAttr('grpctrl_r_wrist01_parentConstraint1.locVrt_r_wrist01W4','locVrt_r_wrist01.v')
    cmds.connectAttr('grpctrl_l_ankle01_parentConstraint1.locVrt_l_ankle01W4','locVrt_l_ankle01.v')
    cmds.connectAttr('grpctrl_r_ankle01_parentConstraint1.locVrt_r_ankle01W4','locVrt_r_ankle01.v')




    cmds.setAttr( "ctrl_l_ankle01.ik_fk", 1)
    cmds.setAttr( "ctrl_r_ankle01.ik_fk", 1)

    cmds.setAttr( "grp_r_LEG_FK_01.visibility", 0)
    cmds.setAttr( "grp_l_ARM_IK_01.visibility", 0)
    cmds.setAttr( "grp_l_ARM_FK_01.visibility", 0)
    cmds.setAttr( "grp_r_ARM_FK_01.visibility", 0)
    cmds.setAttr( "grp_r_ARM_IK_01.visibility", 0)
    cmds.setAttr( "grp_l_LEG_IK_01.visibility", 0)
    cmds.setAttr( "grp_r_LEG_IK_01.visibility", 0)
    cmds.setAttr( "grp_l_LEG_FK_01.visibility", 0)
    cmds.setAttr( "ExtraNodes01.visibility", 0)
    cmds.setAttr( "BlendShapes01.visibility", 0)
    cmds.setAttr( "Skeleton01.visibility", 0)

    cmds.setAttr( "Ik01.v", 0)

    cmds.setAttr( "locDrv_l_tiltRight01.v", 0)
    cmds.setAttr( "locDrv_r_tiltRight01.v", 0)

    cmds.select('ctrl*','Ctrl_IK_l_shin01','Ctrl_IK_r_shin01','Ctrl_IK_l_elbow01','Ctrl_IK_r_elbow01',r=True)
    sel_lock = cmds.ls(sl=True ,tr=True)

    for objs in sel_lock :
        if objs == 'ctrl_global01':
            cmds.setAttr( (objs+".v"),lock=True,k=False,cb=False)
        else:
            cmds.setAttr( (objs+".sx"),lock=True,k=False,cb=False)
            cmds.setAttr( (objs+".sy"),lock=True,k=False,cb=False)
            cmds.setAttr( (objs+".sz"),lock=True,k=False,cb=False)
            cmds.setAttr( (objs+".v"),lock=True,k=False,cb=False)

    FKCtrls = 'ctrl_pelvis01','ctrl_r_elbow01','ctrl_r_knee01','ctrl_r_shoulder01','ctrl_l_shoulder01','ctrl_l_clavicle01','ctrl_r_clavicle01','ctrl_neck01','ctrl_head01','ctrl_spineFK_c01','ctrl_spineFK_b01','ctrl_spineFK_a01','ctrl_l_tiltRight01','ctrl_l_heel01','ctrl_l_tiltLeft01','ctrl_l_ball01','ctrl_l_toe01','ctrl_r_toe01','ctrl_r_ball01','ctrl_r_tiltLeft01','ctrl_r_tiltRight01','ctrl_r_heel01','ctrl_l_hip01','ctrl_r_hip01','ctrl_l_knee01','ctrl_l_elbow01'

    for objs in FKCtrls :
        cmds.setAttr( (objs+".tx"),lock=True,k=False,cb=False)
        cmds.setAttr( (objs+".ty"),lock=True,k=False,cb=False)
        cmds.setAttr( (objs+".tz"),lock=True,k=False,cb=False)

    IKCtrls = 'Ctrl_IK_l_elbow01','Ctrl_IK_r_elbow01','Ctrl_IK_l_shin01','Ctrl_IK_r_shin01','ctrl_spineIK_b01','ctrl_spineIK_c01'

    for objs in IKCtrls :
        cmds.setAttr( (objs+".rx"),lock=True,k=False,cb=False)
        cmds.setAttr( (objs+".ry"),lock=True,k=False,cb=False)
        cmds.setAttr( (objs+".rz"),lock=True,k=False,cb=False)

    
                
    prefix = Input_RigPrefix
    cmds.select('CharacterNode01',hi=True)
    list = cmds.ls(sl=True,tr=True)
    for x in list :
        cmds.rename(x,(prefix+x))
    
    

def finaliseRig(Input_RigPrefix):
    IK_System()
    spineRig()
    createControls()
    createIKFKSYSTEMS()
    polishRig(Input_RigPrefix)