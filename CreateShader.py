from maya.cmds import *
from pymel.core import *
import maya.mel as mel
from random import uniform as rnd

def createShader(shaderType,shaderColor,useTexture):
	#1. get selection
	target = ls(sl=True)
	#2. initialize shader
	shader=shadingNode(shaderType,asShader=True)
	#3. create a file texture node
	if(useTexture==True):
		file_node=shadingNode("file",asTexture=True)
	#4. create a shading group
	shading_group= sets(renderable=True,noSurfaceShader=True,empty=True)
	#5. set the color
	setRGBA(shader,shaderColor)
	#6. connect shader to sg surface shader
	connectAttr('%s.outColor' %shader ,'%s.surfaceShader' %shading_group)
	#7. connect file texture node to shader's color
	if(useTexture==True):
		connectAttr('%s.outColor' %file_node, '%s.color' %shader)
	#9. restore selection
	select(target)
	#10. return the completed shader
	return shader

def assignShader(shader):
	hyperShade(a=shader)

def getShader():
	# get shapes of selection:
	shapesInSel = ls(dag=1,o=1,s=1,sl=1)
	# get shading groups from shapes:
	shadingGrps = listConnections(shapesInSel,type='shadingEngine')
	# get the shaders:
	shader = ls(listConnections(shadingGrps),materials=1)
	return shader[0] 

def quickShader(shaderType,shaderColor,useTexture):
	shader = createShader(shaderType,shaderColor,useTexture)
	assignShader(shader)

def setRGBA(s,c):
	r = float(c[0]) / 255.0
	g = float(c[1]) / 255.0
	b = float(c[2]) / 255.0
	a = abs(1-(float(c[3]) / 255.0))
	setAttr(s + ".color", (r,g,b))
	setAttr(s + ".transparency", (a,a,a))

def setRGB(s,c):
	r = float(c[0]) / 255.0
	g = float(c[1]) / 255.0
	b = float(c[2]) / 255.0
	setAttr(s + ".color", (r,g,b))

def setAlpha(s,c):
	a = abs(1-(float(c) / 255.0))
	setAttr(s + ".transparency", (a,a,a))	

def keyAlpha(shader):
	mel.eval("setKeyframe { \"" + shader + ".it\" };")	

quickShader("blinn",[255,0,0,100],False)