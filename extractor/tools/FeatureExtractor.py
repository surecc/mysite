'''
Created on 2011/11/24

@author: Surecc
'''

import sys
sys.path.append(r"C:\Python27\Lib\site-packages")

import cv2.cv as cv

class FeatureExtractor:
    DEBUG = 0
    TRAINING_MODE = 0
    TESTING_MODE = 1
    def __init__(self):
        self.imgT = None   #training Image
        self.imgTt = None  #testing Image
        self.avgBGRT = None
        self.avgBGRTt = None
        self.avgHSVT = None
        self.avgHSVTt = None
        self.element = cv.CreateStructuringElementEx(3, 3, 0, 0, cv.CV_SHAPE_CROSS)
        self.new_mask_val = 255
        self.connectivity = 8
        self.normalizeSize = 145
        self.maskT = cv.CreateImage( (self.normalizeSize, self.normalizeSize), 8, 1 )
        self.maskTt = cv.CreateImage( (self.normalizeSize, self.normalizeSize), 8, 1 )
        self.hsvT = cv.CreateImage((self.normalizeSize, self.normalizeSize),8,3)
        self.hsvTt = cv.CreateImage((self.normalizeSize, self.normalizeSize),8,3)
        self.MorphBuf = cv.CreateImage( (self.normalizeSize, self.normalizeSize), 8, 1 )
        self.resizeImgT = cv.CreateImage((self.normalizeSize, self.normalizeSize),8,3)
        self.resizeImgTt = cv.CreateImage((self.normalizeSize, self.normalizeSize),8,3)
    
    # load image for FeatureExtractor
    # mode = 0 : training image
    # mode = 1 : testing image
    def loadImg(self,strFileName, mode):
        if mode == self.TRAINING_MODE:
            self.imgT = cv.LoadImage(strFileName)
            if self.imgT != None:
                cv.Zero(self.maskT)
                cv.Zero(self.MorphBuf)
                cv.Zero(self.hsvT)
                cv.Resize(self.imgT, self.resizeImgT)
                self.preprocessing(self.resizeImgT,self.TRAINING_MODE)
            else:
                return 'Load image Fail'
        elif mode == self.TESTING_MODE:
            self.imgTt = cv.LoadImage(strFileName)
            if self.imgTt != None:
                cv.Zero(self.maskTt)
                cv.Zero(self.MorphBuf)
                cv.Zero(self.hsvTt)
                cv.Resize(self.imgTt, self.resizeImgTt)
                self.preprocessing(self.resizeImgTt,self.TESTING_MODE)  
            else:
                return 'Load image Fail'          
        else:
            return 'Unsupported mode!'
    
    def loadMask(self,strFileName,mode):
        mask = cv.LoadImage(strFileName,cv.CV_LOAD_IMAGE_GRAYSCALE)
        cv.Resize(mask, self.MorphBuf)
        if mode == self.TRAINING_MODE:
            cv.Zero(self.maskT)
            cv.Threshold(self.MorphBuf, self.maskT, 250, 255, cv.CV_THRESH_BINARY);
            cv.MorphologyEx(self.maskT, self.maskT, self.MorphBuf,self.element , cv.CV_MOP_OPEN) 
            if self.DEBUG:
                cv.NamedWindow("train")
                cv.ShowImage("train", self.maskTt);
                cv.WaitKey(0)
        elif mode == self.TESTING_MODE:
            cv.Zero(self.maskTt)
            cv.Threshold(self.MorphBuf, self.maskTt, 250, 255, cv.CV_THRESH_BINARY);
            cv.MorphologyEx(self.maskT, self.maskT, self.MorphBuf,self.element , cv.CV_MOP_OPEN) 
            if self.DEBUG:
                cv.NamedWindow("test")
                cv.ShowImage("test", self.maskTt);
                cv.WaitKey(0)
            
    def showImg(self):
        if self.maskT:
            cv.NamedWindow("mask",cv.CV_WINDOW_AUTOSIZE)
            cv.ShowImage("mask", self.maskT)
            cv.WaitKey(0)    
        elif self.maskTt:
            cv.NamedWindow("mask2",cv.CV_WINDOW_AUTOSIZE)
            cv.ShowImage("mask2", self.maskTt)
            cv.WaitKey(0)    
             
    
    def preprocessing(self,img,mode):
        if img != None:
            imgBuf = cv.CreateImage(cv.GetSize(img), 8, 3)
            if mode == self.TRAINING_MODE:
                flags = self.connectivity + (self.new_mask_val << 8) + cv.CV_FLOODFILL_FIXED_RANGE
                cv.FloodFill(img,(0,0) ,cv.CV_RGB(255, 255, 255,),cv.CV_RGB(5,5,5),
                             cv.CV_RGB(5,5,5),flags,None)
                cv.Split(img,self.maskT,None,None,None)
                cv.Threshold(self.maskT,self.maskT,250,255,cv.CV_THRESH_BINARY_INV);
                cv.MorphologyEx(self.maskT, self.maskT, self.MorphBuf,self.element , cv.CV_MOP_OPEN)
                cv.WaitKey(0)
                if self.DEBUG:
                    cv.Threshold(img,imgBuf,250,255,cv.CV_THRESH_TOZERO_INV); 
                    cv.NamedWindow("name",cv.CV_WINDOW_AUTOSIZE)
                    cv.ShowImage("name", self.maskT)
                    cv.WaitKey(0)
            elif mode == self.TESTING_MODE:
                cv.Threshold(img,imgBuf,250,255,cv.CV_THRESH_BINARY)
                flags = self.connectivity + (self.new_mask_val << 8) + cv.CV_FLOODFILL_FIXED_RANGE
                cv.FloodFill(imgBuf,(0,0) ,cv.CV_RGB(255, 255, 255,),cv.CV_RGB(5,5,5),
                             cv.CV_RGB(5,5,5),flags,None)
                cv.Split(imgBuf,self.maskTt,None,None,None)
                cv.Not(self.maskTt, self.maskTt)
                cv.MorphologyEx(self.maskTt, self.maskTt, self.MorphBuf,self.element , cv.CV_MOP_OPEN) 
                if self.DEBUG:
                    cv.Copy(img, imgBuf,self.maskTt )
                    cv.NamedWindow("name",cv.CV_WINDOW_AUTOSIZE)
                    cv.ShowImage("name", self.maskTt)
                    cv.WaitKey(0)
        return None
    # return feature values [ R G B H S]
    # The value are normalize to the range 0~1
    def exportFeature(self,mode):
        if mode == self.TRAINING_MODE:
            if self.imgT != None:
                avgBGR = cv.Avg(self.resizeImgT,self.maskT)
                cv.CvtColor(self.resizeImgT, self.hsvT, cv.CV_BGR2HSV)
                avgHSV = cv.Avg(self.hsvT,self.maskT) 
                return [avgBGR[1]/255,avgBGR[2]/255,avgBGR[0]/255, avgHSV[0]/180,avgHSV[1]/255]
            else:
                return 'No Training image is loaded'
        elif mode == self.TESTING_MODE:
            if self.imgTt != None:
                avgBGR = cv.Avg(self.resizeImgTt,self.maskTt)
                cv.CvtColor(self.resizeImgTt, self.hsvTt, cv.CV_BGR2HSV)
                avgHSV = cv.Avg(self.hsvTt,self.maskTt) 
                return [avgBGR[1]/255,avgBGR[2]/255,avgBGR[0]/255, avgHSV[0]/180,avgHSV[1]/255]
            else:
                return 'No Testing image is Loaded'
        return [0,0,0,0,0]
    
    # this function returns likelihood of two image the value is form 0~1
    # (histogram likelihood, Shape coverage ratio)
    # 0: not matched  1:completely matched
    
    def getCompareResult(self):
        return self.compareImage2(self.resizeImgT,self.resizeImgTt,self.maskT,self.maskTt)
    
    def compareImage2(self,img1,img2,mask1,mask2):
        if img1!= None and img2 != None:
            hist1 = self.getHistogram(img1,mask1)
            hist2 = self.getHistogram(img2,mask2)  
            cv.Xor(mask1, mask2, self.MorphBuf);
            if self.DEBUG:
                cv.NamedWindow('buf')
                cv.ShowImage('buf', self.MorphBuf)
                cv.WaitKey(0)
            return cv.CompareHist(hist1, hist2, cv.CV_COMP_BHATTACHARYYA),cv.Sum(self.MorphBuf)[0]/255/(self.normalizeSize*self.normalizeSize)
        return 'Images are not loaded'
    
    def compareImage(self,strImgFile1, strImgFile2):
        img1 = cv.LoadImage(strImgFile1)
        img2 = cv.LoadImage(strImgFile2)
        img1R = cv.CreateImage((self.normalizeSize,self.normalizeSize),8,3)
        img2R = cv.CreateImage((self.normalizeSize,self.normalizeSize),8,3)
        mask1 = cv.CreateImage((self.normalizeSize,self.normalizeSize),8,1)
        mask2 = cv.CreateImage((self.normalizeSize,self.normalizeSize),8,1)
        cv.Resize(img1, img1R)
        cv.Resize(img2, img2R)
        cv.Threshold(img1R,img1R,250,255,cv.CV_THRESH_TOZERO_INV);
        cv.Threshold(img2R,img2R,250,255,cv.CV_THRESH_TOZERO_INV);
        cv.Split(img1R, mask1,None,None,None)
        cv.Split(img2R, mask2,None,None,None)    
        hist1 = self.getHistogram(img1R,mask1)
        hist2 = self.getHistogram(img2R,mask2)  
        return cv.CompareHist(hist1, hist2, cv.CV_COMP_BHATTACHARYYA)
    #return histogram in HS domain        
    def getHistogram(self, img , mask):
        hsv = cv.CreateImage(cv.GetSize(img), 8, 3)
        cv.CvtColor(img, hsv, cv.CV_BGR2HSV)
        h = cv.CreateImage(cv.GetSize(img),8,1)
        s = cv.CreateImage(cv.GetSize(img),8,1)
        v = cv.CreateImage(cv.GetSize(img),8,1)
        planes = [h,s]
        cv.CvtPixToPlane(hsv, h, s, v, None)
        h_range = [0,180]
        s_range = [0,255]
        size = [15,16]
        ranges = [h_range,s_range]
        hist = cv.CreateHist(size,cv.CV_HIST_ARRAY,ranges,1)
        cv.CalcHist(planes, hist,0,mask)
        cv.NormalizeHist(hist, 1.0)
        if self.DEBUG:
            scale = 10
            hist_img = cv.CreateImage((size[0]*scale,size[1]*scale),8,3)
            cv.Zero(hist_img)
            max1 = cv.GetMinMaxHistValue(hist)
            for i in range(size[0]):
                for j in range (size[1]):
                    bin_val = cv.QueryHistValue_2D(hist, i, j)
                    intesity = cv.Round(bin_val*255/max1[1])
                    cv.Rectangle(hist_img, (i*scale, j*scale),((i+1)*scale-1,(j+1)*scale-1),cv.RGB(intesity, intesity, intesity),cv.CV_FILLED)
                    
            cv.NamedWindow('name')
            cv.ShowImage('name', hist_img)
            cv.WaitKey(0)
            
        return hist
