from pypylon import pylon
class MyVideoCapture:
	def __init__(self, video_source):
		# Open the video source
		self.vid = pylon.InstantCamera(video_source)
		self.vid.StartGrabbing(1)
		if not self.vid.IsOpen():
			raise ValueError("Unable to open video source", video_source)

						
	def get_frame(self):
		if not self.vid.IsOpen():
			self.vid.StartGrabbing()
		converter = pylon.ImageFormatConverter()
		# converting to opencv bgr format
		converter.OutputPixelFormat = pylon.PixelType_BGR8packed
		converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
		if self.vid.IsOpen():			
			grabResult = self.vid.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
			if grabResult.GrabSucceeded():
		        # Access the image data
				image = converter.Convert(grabResult)
				img = image.GetArray()
				return (grabResult.GrabSucceeded(),img)
			else:
				return(grabResult.GrabSucceeded(),None)
		else:
			return(self.vid.IsOpen(),None)

	def stop_get_frame(self):
		self.vid.StopGrabbing()