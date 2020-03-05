import numpy as np
import cv2
import os
import pandas as pd
import argparse


def raw_object_count(object_width, object_height, no_pixels, results_path):
    '''
    Performs raw object count on nonzero pixels given object dimensions
    '''

    object_count = int((no_pixels / (object_height * object_width)))
    print('raw object count: %d' % (object_count))

    output_filename = os.path.join(results_path,'raw_object_count.txt')

    with open(output_filename, 'w') as f:
        f.write('raw object count: %d' % (object_count))
    


def count_pixels(root_path, results_path):
    '''
    Counts the nonzero pixels in an image
    '''

    df = pd.DataFrame(columns=['filename','Pixel Count','Nonzero Pixel Count','Ratio'])

    for _, _, files in os.walk(root_path):
        sum_nonzero = 0.0
        sum_total = 0.0
        count = 0
        for file in files:
            if file.endswith(('jpg', 'png', 'PNG', 'JPG')):
                
                image_total = 0.0
                image_nonzero = 0.0

                filepath = os.path.join(root_path, file)

                # Load an image
                img = cv2.imread(filepath, -1)

                #print(img.shape)

                channels = []
                
                channels = cv2.split(img)
                
                for channel in channels:
                    sum_nonzero += cv2.countNonZero(channel)
                    image_nonzero = cv2.countNonZero(channel)

                sum_total += img.shape[0]*img.shape[1]
                image_total = img.shape[0]*img.shape[1]
                ratio = image_nonzero / image_total
                

                df.loc[count] = [filepath, image_total, image_nonzero, ratio]
                count += 1
    
    ratio = sum_nonzero / sum_total

    df.loc[count + 1] = ['Total', sum_total, sum_nonzero, ratio]
    
    print('Total number of pixels in all images ', sum_total)
    print('Total number of nonzero pixels in all images', sum_nonzero)

    output_filename = os.path.join(results_path, 'pixel_count_results.csv')

    df.to_csv(output_filename, index=False)
    
    return sum_nonzero


if __name__ == "__main__":
    
    # Get the arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('image_dir', help='root image directory')
    parser.add_argument('--results_path', help='optional file path to save results', default='./')
    parser.add_argument('--object_height', help='optional object height of an object for statistical calculations', default=None, type=int)
    parser.add_argument('--object_width', help='optional object width of an object for statistical calculations', default=None, type=int)

    args=parser.parse_args()

    # Count pixels and save results
    sum_nonzero = count_pixels(args.image_dir,args.results_path)

    if args.object_height and args.object_width:
        assert args.object_height > 0, \
            'object height must be positive'
        assert args.object_width > 0, \
            'object width must be positive'

        raw_object_count(args.object_width, args.object_height, sum_nonzero, args.results_path)
