#Requests with this part in name will not be converted to script
IGNORE_EXT = [".gif",".js",".css",".png","/imagem/","/sockjs/"]
#When this option is true, the delays between requests is converted to `think` operations for artillery, adding delays between requests.
CONVERT_THINK=True