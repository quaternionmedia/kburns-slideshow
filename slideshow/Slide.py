import pkgutil
import random
import os

class Slide:

    def __init__(self, file, output_width, output_height, duration, fade_duration = 1, fps = 60, title = None, overlay_text = None, transition = "random"):
        self.file = file
        self.has_audio = False
        self.output_width = output_width
        self.output_height = output_height
        self.duration = duration
        # fade-out duration (= fade-in duration of next slide)
        self.fade_duration = fade_duration
        self.title = title
        self.overlay_text = overlay_text
        self.output_ratio = self.output_width / self.output_height
        self.fps = fps
        
        if transition == "random":
            self.transition = random.choice(self.getEffects())
        else:
            self.transition = transition if transition in self.getEffects() else None
        
        self.splits = []
        self.tempfile = None
        
        # fix the duration
        # round down to last full frame
        self.frames = 0
        self.setDuration(duration)
        
    def getDuration(self): 
        return round(self.frames/self.fps, 3)
        
    def setDuration(self, duration):
        # for each frame (in one second) calculate the expected duration (i/fps)
        # if this value has more than 2 decimal places (*100 has no decimal places (is_integer))
        # it is a possible frame for a duration with less than 2 decimal places
        possibleFrames = [i for i in range(self.fps) if float(i/self.fps*100).is_integer()]
        
        total_frames = round(duration * self.fps)
        total_frames_seconds = int(duration) * self.fps
        
        remaining_frames = total_frames - total_frames_seconds
        
        frameCount = 0
        for i in possibleFrames:
            if i <= remaining_frames:
                frameCount = i
            else:
                break
        
        self.frames = total_frames_seconds + frameCount
        self.duration = self.frames/self.fps
        
    def getFrames(self):
        return self.frames
        
    def getFilter(self):
        return
        
    def getObject(self, config):
        object = {
            "file": self.file
        }
        
        if self.getDuration() != config["slide_duration"]:
            object["slide_duration"] = self.getDuration()
            
        if self.fade_duration != config["fade_duration"]:
            object["fade_duration"] = self.fade_duration
            
        if self.title is not None:
            object["title"] = self.title
            
        if self.overlay_text is not None:
            object["overlay"] = self.overlay_text
            
        if self.transition != config["transition"]:
            object["transition"] = self.transition
            
        return object
        
    def getEffects(self):
        return [package_name for importer, package_name, _ in pkgutil.iter_modules([os.path.dirname(os.path.realpath(__file__))+"/effects"])]