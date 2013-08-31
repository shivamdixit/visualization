"""
Key commands:
4: Zoom in to model
5: Zoom out from model
Navigate using mouse + WASD keys
"""

import viz
import steve
import vizact
import vizcam
import vizshape
import _winreg
import viztip
import viztask

viz.setMultiSample(8)
viz.fov(50)
viz.go(viz.FULLSCREEN)
#viz.collision(viz.ON)

# Simulate head tracker using keyboard/mouse navigator
head_tracker = vizcam.addWalkNavigate()
head_tracker.setPosition([0,1.5,0])

viz.mouse.setVisible(False)

# Add pit model
model = viz.add('pit.osgb')
model.hint(viz.OPTIMIZE_INTERSECT_HINT)

for x in [-4,-2,2,4]:
	male = viz.addAvatar('vcc_male2.cfg',pos=(x,0.05,0),euler=(0,0,0))
	male.state(6)
	Chair=viz.addChild('chair.ive')
	Chair.setScale([.01,.01,.01])
	Chair.setEuler([180,0,0])
	Chair.setPosition([x,0.05,-.1])
for i in range(-4,5):
	Table=viz.addChild('table.wrl')
	Table.setPosition([i,0.3,1])
	
for i in range(-4,5,3):
	phone=viz.addChild('phone.ive')
	phone.setPosition([i,1,1])
	cup=viz.addChild('F:\cup.obj')
	cup.setScale([.05,.05,.05])
	cup.setPosition([i+1,1,1+.25])
Chair=viz.addChild('chair.ive')
Chair.setScale([.01,.01,.01])
Chair.setEuler([180,0,0])

Laptop=viz.addChild('F:\laptop.ive')
Laptop.setPosition([-3.5,.9,1])
Laptop.setScale([.03,.03,.03])
Laptop.setEuler([15,0,0])

Laptop=viz.addChild('F:\laptop.ive')
Laptop.setPosition([-1.8,.9,1])
Laptop.setScale([.03,.03,.03])
Laptop.setEuler([10,0,0])

Laptop=viz.addChild('F:\laptop.ive')
Laptop.setPosition([1.8,.9,1])
Laptop.setScale([.03,.03,.03])
Laptop.setEuler([-10,0,0])

avatar = viz.addAvatar('vcc_male2.cfg',pos=[-5.7,-5.2,0])
avatar.state(1)
sofa=viz.addChild('F:\Objects\max\obj2.ive')
sofa.setScale([.030,.030,.030])
sofa.setPosition([-9.2,0.15,-0])
sofa.setEuler([-90,0,0])

#stand=viz.addChild('F:\Objects\max\obj1.ive')
#stand.setScale([.00030,.00030,.00030])
#stand.setPosition([-0,0.15,-0])
#stand.setEuler([0,0,0])

shadow_texture = viz.addTexture('shadow.png')
shadow = vizshape.addQuad(parent=avatar,axis=vizshape.AXIS_Y)
shadow.texture(shadow_texture)
shadow.zoffset()
avatarMove = [[-5.7,-5.2,300],[-5.7,6.5,270],[0,8,0],[5.7,6.5,70],[5.7,2.6,70],[5.7,1,130]]
actions = []
RandomWait = vizact.waittime(vizact.randfloat(0,0))

for loc in avatarMove:
	
	if loc == avatarMove[2]:
		RandomWait = vizact.waittime(vizact.randfloat(5,10))
	else:
		RandomWait = vizact.waittime(vizact.randfloat(0,0))
	
	actions.append(vizact.method.playsound('footsteps.wav',viz.LOOP))
	actions.append(vizact.walkTo([loc[0],0,loc[1]],turnSpeed=250.0))
	actions.append(vizact.method.playsound('footsteps.wav',viz.STOP))
	
	actions.append(vizact.turn(loc[2],250.0))
	actions.append(RandomWait)
avatar.addAction(vizact.sequence(actions,viz.FOREVER))

avatar = viz.addAvatar('vcc_male.cfg',pos=[-5.7,-5.2,0.1])
avatar.state(1)


#Create static drop shadow to avatar
shadow_texture = viz.addTexture('shadow.png')
shadow = vizshape.addQuad(parent=avatar,axis=vizshape.AXIS_Y)
shadow.texture(shadow_texture)
shadow.zoffset()
avatarMove = [[5.7,-6.2,300],[5.7,6.5,270],[0,7,0],[-5.7,6.5,70],[-5.7,2.6,70],[-5.7,0,130]]
actions = []
RandomWait = vizact.waittime(vizact.randfloat(0,0))

for loc in avatarMove:
	
	if loc == avatarMove[2]:
		RandomWait = vizact.waittime(vizact.randfloat(5,10))
	else:
		RandomWait = vizact.waittime(vizact.randfloat(0,0))
	#Add an action to walk to the next painting, turn towards it, and wait a few seconds
	actions.append(vizact.method.playsound('footsteps.wav',viz.LOOP))
	actions.append(vizact.walkTo([loc[0],0,loc[1]],turnSpeed=250.0))
	actions.append(vizact.method.playsound('footsteps.wav',viz.STOP))
	
	actions.append(vizact.turn(loc[2],250.0))
	actions.append(RandomWait)
avatar.addAction(vizact.sequence(actions,viz.FOREVER))
music = viz.addAudio('bach_air.mid',loop=1)



# Add fall sound
fallSound = viz.addAudio('sounds/pit_fall.wav')

# Add blur effect for fall action
import vizfx.postprocess
from vizfx.postprocess.blur import DirectionalBlurEffect
blurEffect = DirectionalBlurEffect(samples=3,angle=90)
vizfx.postprocess.addEffect(blurEffect)

# Add red quad to flash screen after falling
flash_quad = viz.addTexQuad(parent=viz.ORTHO)
flash_quad.color(viz.RED)
flash_quad.alignment(viz.ALIGN_LEFT_BOTTOM)
flash_quad.blendFunc(viz.GL_ONE,viz.GL_ONE)
flash_quad.visible(False)
viz.link(viz.MainWindow.WindowSize,flash_quad,mask=viz.LINK_SCALE)

def FallAction():
	"""Flashes screen red and animates blur effect"""
	fallSound.stop()
	fallSound.play()
	flash_quad.visible(True)
	flash_quad.color(viz.RED)
	fade_out = vizact.fadeTo(viz.BLACK,time=2.5)
	flash_quad.runAction(vizact.sequence(fade_out,vizact.method.visible(False)))
	flash_quad.runAction(vizact.call(blurEffect.setDistance,vizact.mix(50,0,time=2.5)),pool=1)

class TrackedFaller(viz.VizNode):
	"""Class for simulating a head tracked user falling"""

	# Threshold to clamp height to ground level
	GROUND_CLAMP_THRESHOLD = 0.1

	# Distance from edge to allow before falling
	FALL_EDGE_BUFFER = 0.4

	# Maximum step height allowed
	STEP_HEIGHT = 0.3

	# Maximum fall velocity
	TERMINAL_VELOCITY = 60.0

	# Gravity acceleration
	GRAVITY = 9.8

	def __init__(self,tracker):

		# Initialize using group node
		group = viz.addGroup()
		viz.VizNode.__init__(self,group.id)

		self._offset = viz.Vector()
		self._tracker = tracker
		self._velocity = 0.0

		# Update tracker every frame
		self._updater = vizact.onupdate(0,self.update)

	def _onFinishedFalling(self):
		pass

	def _intersect(self,begin,end):
		return viz.intersect(begin,end)

	def _clearVelocity(self):
		if self._velocity > 0.0:
			self._onFinishedFalling()
			self._velocity = 0.0

	def reset(self):
		"""Reset faller to origin"""
		self.setOffset([0,0,0])
		self._velocity = 0.0

	def setOffset(self, offset):
		"""Set offset"""
		self._offset.set(offset)
		self.setPosition(self._offset+self._tracker.getPosition())

	def getOffset(self):
		"""Get offset"""
		return list(self._offset)

	def getVelocity(self):
		return self._velocity

	def update(self):

		# Get tracker position
		tracker_pos = self._tracker.getPosition()

		# Get current view position
		view_pos = self._offset + tracker_pos
		view_pos[1] =  self._offset[1] + self.STEP_HEIGHT

		# Perform intersection to determine height of view above ground
		line_end = view_pos - [0,500,0]
		isections = [self._intersect(view_pos,line_end)]

		# Check points around position to allow buffer around edges
		if self.FALL_EDGE_BUFFER > 0.0:
			buf = self.FALL_EDGE_BUFFER
			isections.append(self._intersect(view_pos+[buf,0,0],line_end+[buf,0,0]))
			isections.append(self._intersect(view_pos+[-buf,0,0],line_end+[-buf,0,0]))
			isections.append(self._intersect(view_pos+[0,0,buf],line_end+[0,0,buf]))
			isections.append(self._intersect(view_pos+[0,0,-buf],line_end+[0,0,-buf]))

		# Get intersection with largest height
		try:
			info = max((info for info in isections if info.valid),key=lambda info:info.point[1])
		except ValueError:
			info = isections[0]

		if info.valid:

			# Get height above ground
			ground_height = info.point[1]

			# If current offset is greater than ground height, then apply gravity
			if self._offset[1] > ground_height:
				dt = viz.getFrameElapsed()
				self._velocity = min(self._velocity + (self.GRAVITY * dt),self.TERMINAL_VELOCITY)
				self._offset[1] -= (self._velocity * dt)

			# Clamp to ground level if fallen below threshold
			if self._offset[1] - self.GROUND_CLAMP_THRESHOLD < ground_height:
				self._offset[1] = ground_height
				self._clearVelocity()

		# Update position/orientation
		self.setPosition(self._offset+tracker_pos)
		self.setQuat(self._tracker.getQuat())

class PitTrackedFaller(TrackedFaller):
	"""Derived tracked faller class for performing action when finished falling"""
	def _onFinishedFalling(self):
		if self.getVelocity() > 6.0:
			FallAction()

# Create tracked faller and link to main view
faller = PitTrackedFaller(head_tracker)
viz.link(faller,viz.MainView)

def Reset():
	"""Reset platforms and place faller back at origin"""

	# Reset platform
	platform.clearActions(viz.ALL_POOLS)
	platform.raised = False
	platform.setPosition([0,0,0])
	platform.audio_running.pause()

	# Reset pit
	pit.clearActions(viz.ALL_POOLS)
	pit.lowered = False
	pit.setPosition([0,0,0])
	pit.color(viz.WHITE)
	pit.audio_running.pause()

	# Reset faller
	faller.reset()
def MyTask():
	yield viztask.waitTime(.5)
	viz.window.displayHTML('F:\Lab 2\index.html',size=[1200,600],pos=[30,30,-30])
	head_tracker.setEuler([0,0,0])
def d(a):
	if a==1:
		move=vizact.moveTo([-0.4,6,6],speed=12)
		head_tracker.addAction(move)
		head_tracker.runAction(move)
#		viz.window.displayHTML('F:\Lab 2\index.html',size=[1200,600],pos=[30,30,-30])
#		head_tracker.setEuler([0,0,0])
		viztask.schedule(MyTask())
	if a==2:
		
		viz.window.hideHTML()
		move=vizact.moveTo([0,1.5,0],speed=15)
		head_tracker.addAction(move)
		head_tracker.runAction(move)
		head_tracker.setEuler([0,0,0])
	
vizact.onkeydown('4',d,1)
vizact.onkeydown('5',d,2)

reg = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Internet Explorer\Main\FeatureControl\FEATURE_BROWSER_EMULATION',0,_winreg.KEY_ALL_ACCESS)
_winreg.SetValueEx(reg,'VizHTMLViewer.exe',0,_winreg.REG_DWORD,9999)


	# Load texture
pic = viz.addTexture('F:\project\wall1.jpg')

	# Create surface to wrap the texture on
quad = viz.addTexQuad(scale=[24.2,12,8])
quad.setPosition([-11,5,2.5]) #put quad in view
	
	# Wrap texture on quad
quad.setEuler([90,0,0])
quad.texture(pic)
pic = viz.addTexture('F:\project\wall2.jpg')

# Create surface to wrap the texture on
quad = viz.addTexQuad(scale=[24.2,12,8])
quad.setPosition([7.7,5,2.5]) #put quad in view
	# Wrap texture on quad
quad.setEuler([90,0,0])
quad.texture(pic)

pic1 = viz.addTexture('F:\project\wall4.jpg')

# Create surface to wrap the texture on
quad = viz.addTexQuad(scale=[24.2,25,8])
quad.setPosition([0,.05,02]) #put quad in view
quad.setEuler([0,90,0])
quad.texture(pic1)
pic2 = viz.addTexture('F:\pro.jpg')
quad = viz.addTexQuad(scale=[24.2,25,8])
quad.setPosition([0,8.5,02]) #put quad in view
quad.setEuler([0,90,0])
quad.texture(pic2)
for i in [[0,05,-8],[0,05,12]]:
	pic2 = viz.addTexture('F:\pro.jpg')
	quad = viz.addTexQuad(scale=[24.2,15,8])
	quad.setPosition(i) #put quad in view
	quad.setEuler([0,0,0])
	quad.texture(pic2)
pic1=viz.addTexture('F:\screen.jpg')
quad = viz.addTexQuad(scale=[7,5,4])
quad.setPosition([-0.8,8,11]) #put quad in view
quad.setEuler([0,-9.5,0])
quad.texture(pic1)

pic3=viz.addTexture('F:\Parallel.png')
quad = viz.addTexQuad(scale=[5,2.5,4])
quad.setPosition([-8.5,7,9.5]) #put quad in view
quad.setEuler([-40,-9.5,0])
quad.texture(pic3)

pic4=viz.addTexture('F:\Scatter.png')
quad = viz.addTexQuad(scale=[5.5,2.5,4])
quad.setPosition([5.8,7,9.5]) #put quad in view
quad.setEuler([55,-9.5,0])
quad.texture(pic4)


