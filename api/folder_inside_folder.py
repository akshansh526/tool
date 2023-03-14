import os 

def create_folder(a):
    path1="E:/Projects_folder/ak1702202300"
    i=1
    while True:

        if (not os.path.isdir(path1)):
            os.mkdir(path1)
            # print(">>>>>>>",path1)
        if len(os.listdir(path1))>=10:
            path2=path1+str(i)
            print(">>>>>>",path2)
            if (not os.path.isdir(path2)):
                os.mkdir(path2)
                i+=1
                path1=path2
                print(">>>>>>",path1)


path1="E:/Projects_folder"
dir_list=os.listdir(path1)
print("dir_list",dir_list)
# create_folder()