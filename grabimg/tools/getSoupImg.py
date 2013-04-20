'''
Created on Jan 15, 2013

@author: surecc
'''

'''
# coding=utf-8 
from bs4 import BeautifulSoup, Tag, NavigableString 
#from SentenceSpliter import SentenceSpliter 
from os.path import basename,dirname,isdir,isfile 
from os import makedirs 
from shutil import copyfile 
import io 
import time 
import re 

class build_tpl: 
    def __init__(self,parse_file,build_tpl_name,cp_pic_dir,show_pic_dir,js_path,set_lang=2052): 
        #参数说明：解析文件名，模版名称，保存图片路径，图片显示路径，js路径，当前语言（分句使用）
        #取得解析文件目录路径 
        if len(dirname(parse_file))>1: 
            self.cur_dir = dirname(parse_file)+"/"; 
        else: 
            self.cur_dir ="./"; 
        #建立的模版文件文件名 
        self.build_tpl_name = build_tpl_name; 
        #图片cp到得目录 
        self.cp_pic_dir = cp_pic_dir; 
        #通过http展现图片的目录 
        self.show_pic_dir = show_pic_dir; 
        #加载js的路径 
        self.js_path = js_path; 
        
        #句段组 
        self.get_text_arr = []; 
        #当前图片名数组 
        self.cur_pic_arr = []; 
        
        #解析文件 取得soup 资源 
        self.soup = self.get_soup(parse_file); 
        #取得html文档中，段文档 
        self.get_text_arr = self.soup.body.findAll(text=lambda(x): len(x.strip()) > 0); 
        #取得句对 
        self.get_sentence_arr = self.parse_text(self.get_text_arr,set_lang); 
        #取得替换数组 
        self.replace_list = self.get_replace_list(self.get_text_arr,set_lang); 
        #取得图片数组 
        self.cur_pic_arr = self.soup.findAll('img'); 
        
        #self.write_file_by_list("no.txt",self.get_text_arr); 
        #self.write_file_by_list("yes.txt",self.get_sentence_arr); 

    #保存词组到文件 
    def save_data_file(self): 
        file_name = self.build_tpl_name+".data"; 
        self.write_file_by_list(file_name,self.get_data()); 
    #取得词组 
    def get_data(self): 
        return self.get_sentence_arr; 
    #数组写入到文档 
    def write_file_by_list(self,file_name,write_arr): 
        file=io.FileIO(file_name,"w"); 
        file.write(('\n'.join(write_arr)).encode('utf-8')); 
        file.close(); 
    #字符串写入到文档 
    def write_file(self,file_name,file_contents): 
        file=io.FileIO(file_name,"w"); 
        file.write(file_contents.encode('utf-8')); 
        file.close(); 
    #建立图片hash目录 
    def get_pic_hash(self): 
        return time.strftime("%Y/%m/%d/"); 
    #建立模版文件 
    def builder(self): 
        #没能发生替换的单词 
        bug_msg = []; 
        #进行内容模版替换 
        for i in range(len(self.get_text_arr)): 
            #替换 
            rep_str = "$rep_arr[{0}]".format(i); 
            try: 
                self.soup.body.find(text=self.get_text_arr[i]).replaceWith(self.replace_list[i]); 
            except AttributeError: 
                bug_msg.append(self.get_text_arr[i]); 
            
            #取得图片hash路径 
            hash_dir = self.get_pic_hash(); 
            #构造展示图片路径 
            show_pic_dir = self.show_pic_dir+hash_dir; 
            #构造图片保存路径 
            cp_pic_dir = self.cp_pic_dir+hash_dir; 
        
        #判断保存图片的目录是否存在 不存在建立 
        if not isdir(cp_pic_dir): 
            makedirs(cp_pic_dir); 
        
        for pic_name in self.cur_pic_arr: 
            #进行图片路径替换 
            old_pic_src = pic_name['src']; 
            pic_name['src'] = show_pic_dir+old_pic_src; 
            #进行图片拷贝 
            cp_src_file = self.cur_dir+old_pic_src; 
            cp_dis_file = cp_pic_dir+old_pic_src; 
            copyfile(cp_src_file,cp_dis_file); 
        
        #建立bug信息的文档 
        #self.write_file_by_list("bug.txt",bug_msg); 
        
        #添加js 
        tag = Tag(self.soup,"script"); 
        tag['type'] = "text/javascript"; 
        tag['src'] =self.js_path+"jquery.js"; 
        
        tag2 = Tag(self.soup,"script"); 
        tag2['type'] = "text/javascript"; 
        tag2['src'] =self.js_path+"init.js"; 
        
        self.soup.head.insert(2,tag2); 
        self.soup.head.insert(2,tag); 
        
        
        #建立模版 
        self.write_file(self.build_tpl_name,self.soup); 
        
    #取得替换的html文件 
    def get_replace_html(self,rep_id,rep_data=""): 
        ''' 
                            参数说明：替换id，替换内容（为空的采用模版模式替换） 
        ''' 
        if len(rep_data) > 0 : 
            rep_str = rep_data; 
        else: 
            rep_str = "$rep_arr[{0}]".format(rep_id); 
        return "<span sty=\"data\" id=\"rep_"+str(rep_id)+"\">"+rep_str+"</span>"; 
    #取得替换数组 
    def get_replace_list(self,text_arr,set_lang): 
        Sp = SentenceSpliter(); 
        Sp.SetLang(set_lang); 
        temp_sentence = []; 
        jump_i = 0; 
        for text in text_arr: 
            SList = Sp.Split(text); 
            replace_temp = ""; 
            if SList != None: 
                for item in SList: 
                    replace_temp = replace_temp+self.get_replace_html(jump_i,item); 
                    jump_i=jump_i+1; 
            else: 
                replace_temp = self.get_replace_html(jump_i,text); 
                jump_i=jump_i+1; 
                temp_sentence.append(replace_temp); 
        return temp_sentence; 
    
    #分句 
    def parse_text(self,text_arr,set_lang): 
        Sp = SentenceSpliter(); 
        Sp.SetLang(set_lang); 
        temp_sentence = []; 
        for text in text_arr: 
            SList = Sp.Split(text); 
            if SList != None: 
                for item in SList: 
                    temp_sentence.append(item); 
            else: 
                temp_sentence.append(text); 
        
        return temp_sentence; 
        
    #取得解析资源 
    def get_soup(self,parse_file): 
        try: 
            file=io.FileIO(parse_file,"r"); 
            doc = file.readall(); 
            file.close(); 
        except IOError: 
            print 'ERROR: %s file not found!' %parse_file; 
            return False; 
        #开始解析html文档 
        return BeautifulSoup(''.join(doc)); 
        
        if __name__ == "__main__": 
            from sys import argv, exit; 
        
            if len(argv) < 3: 
                print "USAGE: python %s <input-file> <output-file>" % argv[0] 
                exit(255); 
        
            if not isfile(argv[1]): 
                print "no such input file: %s" % argv[1] 
                exit(1) 
                
            paser_file = argv[1];#"html/testpic.html"; 
            tpl_file = argv[2]; 
            save_pic_path = argv[3]; 
            show_pic_path = argv[4]; 
            load_js_path = argv[5]; 
            #解析开始 设置解析文件，模版名，图片保存路径，图片显示路径 
            so = build_tpl(paser_file,tpl_file,save_pic_path,show_pic_path,load_js_path); 
            #建立模版 
            so.builder(); 
            #保存分句的句对 
            so.save_data_file();
'''