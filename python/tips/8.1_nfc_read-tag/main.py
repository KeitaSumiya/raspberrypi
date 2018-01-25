import nfc
import time

def connected (tag):
    #try:
    #    pass
    #except KeyboardInterrupt:
    #    pass
    pass
    #print(tag)
    #print(tag.type)
    #print( tag.idm )
    #print( str(tag.idm) )
    #print( str(tag.idm).encode("hex") )
    #print( tag.pmm )
    #print( str(tag.pmm) )
    #print( str(tag.pmm).encode("hex") )
    #print( tag.sys )
    #print( str(tag.sys) )
    #print( str(tag.sys).encode("hex") )
    #time.sleep(1)
    
clf = nfc.ContactlessFrontend("usb")

if __name__ == "__main__":
    try:
        while True:
            print("waiting...")
            result = clf.connect(rdwr={"on-connect":connected})
            #print('----------------------')
            print("scaned")
            print(result)
            print( str(result.idm).encode("hex"))
            print( str(result.pmm).encode("hex"))
            print( str(result.sys).encode("hex"))
            print("-----------------------")

    except KeyboardInterrupt:
        pass
