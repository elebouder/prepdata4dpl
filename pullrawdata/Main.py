import prepMTD as mtd
import downloadUnpack as du
import os

def main(startdate, enddate):
    
    cloudcover = 25.00
    monthlist = list_months(startdate, enddate)
    for elem in monthlist:
        metafile, scenelist = decide(elem[0], elem[1], cloudcover)
        print metafile
        print scenelist


def list_months(start, end):
    monthlist = []
    current = start
    while True:
        monthlist.append(current)
        if current == end:
            break
        if can_grow(current):
            current = [current[0] + 1, current[1]]
        elif not can_grow(current):
            current = [1, current[1] + 1]
    return monthlist 

def can_grow(date):
    mth = date[0]
    if mth == 12:
        return False
    else:
        return True

def decide(month, year, cloudcover):
    account = 'Etienne Le Bouder'
    passwd = 'C130Hercules'
    data_base = '/home/elebouder/Data/landsat/'

    
    outputdir = data_base + 'Unpacked Downloaded Products/%s_%s' % (month, year)
    if os.path.exists(outputdir):
        return 1
    else:
        os.makedirs(outputdir)
    metafile_rough, scenereqlist_rough, roughdict, metafields = mtd.search_mtd(month, year, cloudcover, data_base)

    checkval, txt, mcsv = mtd.refine_mtd(roughdict, month, year, metafields, data_base)

    if checkval == 1:
        meta_csv = mcsv
        scenelist = txt
    elif checkval == 2:
        meta_csv = metafile_rough
        scenelist = scenereqlist_rough

    p, rlocation = du.download_list(scenelist, account, passwd, outputdir)
    print ('final data')
    print p, rlocation, meta_csv, scenelist

    return meta_csv, scenelist


if __name__ == '__main__':
    sdate = [6, 2017]
    edate = [1, 2018]
    main(sdate, edate)

##TODO: delete rough meta and list once you have the refined version
## TODO: take care of checking if the data already exists in file (smooth exit)
## TODO: handle multiple continuous months as well as one month
