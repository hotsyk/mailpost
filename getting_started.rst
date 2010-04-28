.. _getting_started:


***************
Getting started
***************

.. 

.. _install:

Install
-----------------


.. _settings:

Settings to be added to your Django settings::

    MAILPOST_CONFIG_FILE =  os.path.join(DIRNAME, 'config', 'mailpost.yaml')
     
     
Settings
---------------------

Example of config yaml file::
         
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

         