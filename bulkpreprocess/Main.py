import preprocess_main as prep
import os
import sys


def main():
    unpacked_products_path = '/home/elebouder/Data/landsat/Unpacked Downloaded Products'
    intermediary_scene_dataset = '/home/elebouder/Data/landsat/RGB Scenes Ready for Site-Lifting'
    bands = [4, 3, 2, 8]

    ### EITHER
    ### 1) use the temporal type 'months' (specifying a distinct list of months
    #######and years to pick run through), or
    ### 2) pick a beginning and end date and have everthing on file within that interval
    ####### as data ('period')

    months = [[6, 2017]]

    start_month = []
    end_month = []

    temporal_type = 'months'

    if temporal_type == 'months':
        print 'number of months is: ', len(months)
        for month in months:
            filename = '%s_%s' % (month[0], month[1])
            filepath1 = unpacked_products_path + '/' + filename
            for scene in os.listdir(filepath1):
                print 'working on scene' + scene
                filepath2 = filepath1 + '/' + scene
                finishedScene = prep.preprocess(bands, filepath2, scene, intermediary_scene_dataset)
                
    elif temporal_type == 'period':
        print 'searching by period'
        mlist = []
        for dct in os.listdir(unpacked_products_path):
            splt = dct.split('_')
            m = splt[0]
            yr = splt[-1]
            if (start_month[1] <= yr <= end_month[1] and
                start_month[0] <= m <= end_month[0]):
                mlist.append([dct, m, yr])
        print 'number of months is: ', len(mlist)
        for l in mlist:
            m = l[0]
            filename = m
            filepath1 = unpacked_products_path + '/' + filename
            for scene in os.listdir(filepath1):
                print 'working on scene' + scene
                filepath2 = filepath1 + '/' + scene
                finishedScene = prep.preprocess(bands, filepath2, scene, intermediary_scene_dataset)
                
    else:
        print 'enter one of "months" or "period" for temporal_type'
        sys.exit(1)




if __name__ == '__main__':
    main()
