import datetime
import os
#create_fn("path","enseignant")

def create_fname(path,source):
    path=str(path)
    source=str(source)
    if not os.path.exists(os.path.join(os.getcwd(),path)) :
        os.mkdir(os.path.join(os.getcwd(),path))
        
    if not os.path.exists(os.path.join(os.getcwd(),path,source)):
        os.mkdir(os.path.join(os.getcwd(),path,source))
    now=datetime.datetime.now()
    print(type(str(now)))
    current_time=now.strftime("%H%M%S")
    # print(type(current_time))
    # print(current_time)

    current_date=now.strftime("%Y%m%d")
    # print(type(current_date))
    # print(current_date)

    # print(current_date+"_"+current_time+"_"+source)
    return(os.path.join(os.getcwd(),path,source,str(current_date+"_"+current_time+"_"+source))), current_date, current_time, str(current_date+"_"+current_time+"_"+source), source


#print(create_fname("test","enseignant"))