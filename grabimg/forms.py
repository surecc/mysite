#coding=utf-8
'''
Created on Jan 15, 2013

@author: surecc
'''
from django import forms

class SoupForm(forms.Form):
    LIST_WEBSITE = (
                    ('360buy','360buy'),
                    ('taobao','taobao'),
                    ('others','others'),
                    )
    LIST_GENDER = (
		('female','女'),
		('male','男'),
		('other','其他')
	)
    url = forms.CharField(widget=forms.Textarea)
    cate = forms.ChoiceField(choices=LIST_WEBSITE, required=True)
    gender = forms.ChoiceField(choices=LIST_GENDER, required=True)
    
    # start as clean_ and end as the name of the words, it will valide in auto
    '''
    def clean_url(self):
        url = self.cleaned_data['url']
        num_words = len(url.split())
        if num_words < 10:
            raise forms.ValidationError(num_words)
        return url'''
    
