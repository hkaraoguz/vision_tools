import xml.etree.ElementTree as ET
import os
import argparse


def get_image_filepaths(path):
    
    '''
    Function that returns filepaths 
    and filenames of images
    '''

    filepaths = []
    filenames = []

    for file in os.listdir(path):
        if file.endswith(("jpg","png","PNG","JPG")):
            filepath = os.path.join(path, file)
            print(os.path.join(path, file))
            print(os.path.abspath(file))
            
            filepaths.append(filepath)
            filenames.append(file)
    
    return filepaths,filenames


def read_labels(path):
    labels = []

    with open(path,"r") as f:
        labels.append(str(f.readline()))
    
    return labels

def xml_to_csv(xml_path,image_filepath,image_filename,f,labels = None):
    '''
    Function that parses xml annotations and converts them to csv format
    '''
    
    xml_filename = image_filename[:-3]
    xml_filename +='xml'

    xml_file = os.path.join(xml_path,xml_filename)
    
    tree = ET.parse(xml_file)
    root = tree.getroot()

    #labels =[14,15,16,17,18,19,20,22,23,25,29,32,67]

    for obj in root.iter('object'):
        aline = {}
        for child in obj:
            if child.tag == "name":
                #print(child.text)
                if labels != None:
                    if(int(child.text)) in labels:
                        aline["class_name"] = child.text
                    else:
                        continue
                else:
                    aline["class_name"] = child.text
            elif child.tag == "bndbox":
                #xmin
                aline["x1"] = child[0].text
                aline["y1"] = child[1].text
                aline["x2"] = child[2].text
                aline["y2"] = child[3].text
        if(len(aline.keys())==5):
            f.write("%s,%d,%d,%d,%d,%s\n"%(image_filepath,int(aline["x1"]),int(aline["y1"]),int(aline["x2"]),int(aline["y2"]),aline["class_name"]))
    


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('image_dir',help='root image directory')
    parser.add_argument('xml_dir',help='root xml annotations directory')
    parser.add_argument('--csv_path',help='optional output path for csv',default='annotations.csv')
    parser.add_argument('--labels_path',help='optional labels list file',default=None)

    args = parser.parse_args()

    labels = None

    if args.labels_path is not None:
        labels = read_labels(args.labels_path)


    filepaths,filenames = get_image_filepaths(args.image_dir)

    image_data = zip(filepaths,filenames)
    
    csv_filepath = args.csv_path

    with open(csv_filepath,"w") as f:
        for filepath,filename in image_data:
            xml_to_csv(args.xml_dir,filepath,filename,f,labels)
