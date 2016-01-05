

BaudRate = 115200		# Baud rate used to communicate with the Arduino
#UpdateRate = 60			# Seconds between web updates
UpdateRate = 600			# Seconds between web updates
#UpdateRate = 3600			# Seconds between web updates
NodeIdToWebIdMap = {'0':'0', '1':'1', '2':'2', '3':'3', '4':'4'} 	# Map between node id and web id
												# Node Id (Host): Web Id (not applicable)
												# Node Id (1): Web Id (1 - Small)
												# Node Id (2): Web Id (2 - Barn)
												# Node Id (3): Web Id (3 - Main)
												# Node Id (4): Web Id (4 - Cement)
LogAddr = "http://your.website.address/postlogmsg.php"
PostAddr = "http://your.website.address/post2.php"