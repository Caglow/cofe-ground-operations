# chart.py
# wx widget for showing a chart of objects
#   (depends: python-opengl, pyftgl)

import FTGL
from OpenGL.GL import *
import sys
import wx
from wx import glcanvas

class Chart (glcanvas.GLCanvas):
    
    def __init__ (self, parent, fov_ctrl):
        glcanvas.GLCanvas.__init__(self, parent, -1)
        self.context = glcanvas.GLContext(self)
        self.SetCurrent(self.context)
        
        # field of view indicator widget
        self.fov_ctrl = fov_ctrl
        
        # drawing settings
        self.path = [] # list of points [x, y]
        self.center = [0, 0]
        self.h_fov = 90.0 # horizontal field of view
        
        # event handlers
        self.Bind(wx.EVT_SIZE, self.on_resize)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_MOUSEWHEEL, self.scroll_fov)
        
        self.initialized = False
        
    # initialize OpenGL
    def gl_init (self):
        self.initialized = True
        self.resize(self.width, self.height)
        
        glDisable(GL_DEPTH_TEST) # using 2D drawing, so no depth
        glClearColor(0, 0, 0, 1) # black background
        
        # enable antialiasing on lines
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    
    # event handlers
    def on_resize (self, event):
        self.SetCurrent(self.context)
        size = self.GetClientSize()
        self.resize(size.width, size.height)
        
        self.Refresh()
        event.Skip()
    
    def on_paint (self, event):
        wx.PaintDC(self)
        self.SetCurrent(self.context)
        self.draw()
        self.SwapBuffers()
        
        event.Skip()
    
    # scrolling to change field of view directly on the sky chart
    def scroll_fov (self, event):
        if self.h_fov < 100 or \
                int(self.h_fov) == 50 and event.GetWheelRotation() > 0:
            self.h_fov += -2 * float(event.GetWheelRotation()) / 120
        else:
            self.h_fov += -4 * float(event.GetWheelRotation()) / 120
        
        # constraint to range [1, 180]
        if self.h_fov > 180:
            self.h_fov = 180.0
        elif self.h_fov < 1:
            self.h_fov = 1.0
        
        # show new value on field of view indicator
        self.fov_ctrl.SetValue(self.h_fov)
        
        self.Refresh()
        event.Skip()
        
    # resize: update 2D OpenGL display with new size
    #   width, height: new chart size (pixels)
    def resize (self, width, height):
        self.width = width
        self.height = height
        glViewport(0, 0, width, height)
        
        # set up view so top-left is (0, 0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, height, 0, 0, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    
    # project: convert from sky coordinates to screen coordinates
    #          using equirectangular projection
    #   sky_coord -> [crd_a, crd_b]: position of object in the sky
    def project (self, sky_coord):
        
        # find displacement of sky coordinate from center of screen
        displace = [(sky_coord[0] - self.center[0]) % 360.0,
                     sky_coord[1] - self.center[1]]
        
        # transform [0, 360) -> (-180, 180]
        if displace[0] > 180:
            displace[0] -= 360
        
        # compute pixels per degree from horizontal field of view
        pix_per_deg = self.width / self.h_fov
        
        # convert displacement from center in sky coordinates into displacement
        # in screen coordinates and compute final screen position
        return 0.5 * self.width  + displace[0] * pix_per_deg, \
               0.5 * self.height - displace[1] * pix_per_deg
    
    # draw: draw all objects onto the screen
    def draw (self):
        if not self.initialized:
            self.gl_init()
        
        glClear(GL_COLOR_BUFFER_BIT) # clear previous drawing
        
        # draw grid
        glLineWidth(2.5)            # width of 2.5px
        glColor(0.5, 0.5, 0.5)    # gray
        glLineStipple(2, 0xAAAA)  # dashed lines
        glEnable(GL_LINE_STIPPLE)
        
        # mark frequency
        if self.h_fov >= 150:
            mark = 30
        elif self.h_fov >= 50:
            mark = 10
        elif self.h_fov >= 25:
            mark = 5
        elif self.h_fov >= 10:
            mark = 2
        else: # self.h_fov < 10
            mark = 1
        
        # vertical lines
        for azi in range(0, 360/mark):
            point = self.project([azi * mark, 0])
            if -1 < point[0] < self.width + 1:
                # draw line
                glBegin(GL_LINES)
                glVertex(point[0], 0)
                glVertex(point[0], self.height)
                glEnd()
                
                # draw label
                
        
        # horizontal lines
        for alt in range(-90/mark, 90/mark + 1):
            point = self.project([0, alt * mark])
            if -1 < point[1] < self.height + 1:
                # draw line
                glBegin(GL_LINES)
                glVertex(0, point[1])
                glVertex(self.width, point[1])
                glEnd()
                
                # draw label
        
        glDisable(GL_LINE_STIPPLE)
        
        # draw the path
        glLineWidth(3)         # width of 3px
        glColor(0.9, 0.9, 0.9) # light gray
        glBegin(GL_LINE_STRIP)
        
        for point in self.path:
            screen_x, screen_y = self.project(point)
            glVertex(screen_x, screen_y)
        
        glEnd()
        
        glFlush()
