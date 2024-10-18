import sys;
import os;

##sys.argv[0] --the first argument passed - in this case the search string
def GetTotalFilesInDirectory(directory, count):
    _count = count;
    for item in os.listdir(directory):
        _item = os.path.join(directory, item)
        # checking if it is a file
        if os.path.isfile(_item):
            _count += 1;
        else:
            _count = GetTotalFilesInDirectory(_item, _count);
    return _count;

def GetFilesContainsString(directory, checkStrings, files, currentFCount, totalFiles):
    count = currentFCount;

    for item in os.listdir(directory):
        _item = os.path.join(directory, item);
        if os.path.isfile(_item):
            count += 1;
            print('processing file ' + str(count) + ' | ' + str(count/totalFiles*100) + '%');
            [occurence, previews] = GetStringDetailsInFile(checkStrings, _item);
            if(occurence > 0):
                files.append('file:' + _item + ' occurs:' + str(occurence) + ' preview:' + ':::::'.join(previews));
        else:
            files,count = GetFilesContainsString(_item, checkStrings, files, count, totalFiles);

    return files,count;

def GetStringDetailsInFile(_strings, filename): ##details = occurance + previews [seperated by ::: ]
    f_open = open(filename, 'r');

    try:
        lines = f_open.readlines();
        f_open.close();
    except:
        lines = [];
    
    total_occurence = 0;
    total_previews = [];

    if(len(lines) > 0):
        string_occurence = [0] * len(_strings); ##[o1, o2, o3], n = total strings
        string_previews = [[]] * len(_strings); ##[p1, p2, p3], p = total strings
        # for _string in _strings:
        #     previews = [];
        #     occurence = 0;
        #     for line in lines:
        #         o_count = line.count(_string);
        #         occurence += o_count;
        #         if(o_count > 0):
        #             previews.append(line);
        #     string_occurence[string_count] = occurence;
        #     string_previews[string_count] = previews;
        #     string_count += 1;

        for line in lines:
            string_count = 0;
            for _string in _strings:
                o_count = line.count(_string);
                string_occurence[string_count] = string_occurence[string_count] + o_count;
                if(o_count > 0):
                    string_previews[string_count].append(line);
                string_count += 1;
            
        ### only all the search string presence then result is complete, else result will shows empty
        allStringsFound = True;
        for o in string_occurence:
            if(o == 0):
                allStringsFound = False;
        ### merge and returns the results
        if(allStringsFound):
            for o in string_occurence:
                total_occurence += o;
            for previews in string_previews:
                for _previews in previews:
                    total_previews.append(_previews);

        # for line in lines:
        #     o_count = line.count(_string);
        #     occurence += o_count;
        #     if(o_count > 0):
        #         previews.append(line);
    return total_occurence,total_previews;

##scan for total files for progress tracking
totalFiles = 0;
totalFiles = GetTotalFilesInDirectory('./', totalFiles);

##get file name & occurence contains string
if(len(sys.argv) > 1):
    fileDetails = []; ## filename: , occurence: 
    current_file_count = 0;
    fileDetails,count = GetFilesContainsString('./', (sys.argv[1].replace('[+]', ' ')).split('[;]'), fileDetails, current_file_count, totalFiles);
    print('\n\ndone processing\n\n');

    if(len(fileDetails) > 0):
        f = open('./FOS_Results.txt', 'w');
        count = 1;
        for detail in fileDetails:
            print('writing results ' + str(count) + ' | ' + str(count/len(fileDetails)*100) + '%');
            f.writelines(detail + '\n');
            count += 1;
        f.close();
        print('Results Output To : ./FOS(FilesOfString)_Results.txt');
    else:
        print('no results found!');
else:
    print('no search strings passed, please check!');

