import email,imaplib,base64
SERVIDOR = "imap.gmail.com"
EMAIL = ""
PASSWORD = ""
def createXML(filename:str,payload:bin):
    file = open(filename,"wb")
    file.write(base64.b64decode(payload))
    file.close()

def main():
    mail = imaplib.IMAP4_SSL(SERVIDOR)
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')
    status, ids = mail.search(None, 'ALL')
    if(status!="OK"):
        return 0
    ids = ids[0].decode().split(" ")
    for id in ids:
        status, data = mail.fetch(id, '(RFC822)')
        if(status=="OK"):
            for response in data:
                if isinstance(response, tuple):
                    data = email.message_from_bytes(response[1])
                    subject = data['subject']
                    if data.is_multipart():
                        payload,filename = '',''
                        for part in data.get_payload():
                            if part.get_content_type() == 'application/xml':
                                payload += part.get_payload()
                                filename = part.get_filename()
                                createXML(filename,payload)

main()
