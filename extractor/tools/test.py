import FeatureExtractor as ff

f =  ff.FeatureExtractor()
f.loadImg('imgdb/0002.jpg',0)
print f.exportFeature(0)
f.loadImg('imgdb/0001.jpg',1)
print f.exportFeature(1)
print 'match value =' , f.getCompareResult()

f.showImg()
