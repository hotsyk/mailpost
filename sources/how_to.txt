.. _how_to:


***************
How to
***************

.. 
.. _example:

Example
---------------------------------------

* Django form to receive email::

	class EmailForm(forms.Form):
	    sender = forms.CharField(required=False)
	    to = forms.CharField(required=False)
	    subject = forms.CharField(max_length=255)
	    body = forms.CharField(widget=forms.Textarea)
	    
* Job to handle mails::

	python manage.py fetchmail
	
* Mailpost config file example::

    backend: 'imap'
    host: 'imap.gmail.com'
    port: null #If none is specified, default IMAP port will be used
    ssl: 'true'
    username: 'change_this@gmail.com'
    password: 'ChangeThis'
    mailboxes: ['INBOX'] #default
    query: 'all' #Options are 'all', 'unseen', 'seen', 'deleted', 'nondeleted'  
    base_url: 'http://localhost:8000/' #Default: null
    
    #Note the difference between 'from'('to') and 'sender'('receiver') fields
    #The former contains full address, like 'Test Mname <test@gmail.com>'
    #The latter contains email only, like 'test@gmail.com'
    
    rules:
       -   url       : 'mail_test/' 
           method    : 'post' #default
           conditions: #Multiple conditions have effect of boolean 'and'
                   sender : ['*@gmail.com', '*@odesk.com'] #Multiple patterns have effect of boolean 'or'
                   subject: '*test*'
           syntax    : 'glob' # Patterns syntax for params. 
                              #Possible values are 'glob' and 'regexp'. Default: 'glob'
           raw       : false # Send unparsed message. Default: false
           msg_params: ['from', 'to', 'sender', 'receiver', 'subject', 'body'] 
                        # Which parsed parts of message to send in the request. 
                        #Has no effect if raw=true
           add_params: { message_type: 'test' }
                         #Additional params to send in request. 
                         #Will overwrite message params in case of identical keys.
                         # Default: {}
           send_files: true #Whether to send attachments. Default: true
           actions   : ['mark_as_read','delete'] 
                        # Additional processing actions. Default: []. 
                        #In future it may vary depending on backend		    