from docusign_esign import *
import webbrowser
import requests
import json
import base64

def configureApiClient():
    client_id = ''
    client_secret = ''
    scope = 'signature'

     # OAuth endpoints given in the DocuSign API documentation
    authorization_base_url = 'https://account-d.docusign.com/oauth/auth'
    token_url = 'https://account-d.docusign.com/oauth/token'
    redirect_uri = 'https://example.com/callback'
    scope = 'signature'

    from requests_oauthlib import OAuth2Session
    docusign = OAuth2Session(client_id,redirect_uri = redirect_uri,scope=scope)

     # Redirect user to DocuSign for authorization
    authorization_url, state = docusign.authorization_url(authorization_base_url)
    #print ('Please go here and authorize,' + authorization_url)
    print(authorization_url)
    webbrowser.open(authorization_url)

     # Get the authorization verifier code from the callback url
    redirect_response = input('Paste the full redirect URL here:')

     # Fetch the access token
    response = docusign.fetch_token(token_url, client_secret=client_secret,
            authorization_response=redirect_response)
    token = response.get("access_token")
    print(token)

    apiClient = ApiClient()
    apiClient.host = "https://demo.docusign.net/restapi"
    apiClient.set_default_header(header_name="Authorization", header_value=f"Bearer" + " " + token)
    #apiClient.set_base_path();
    return apiClient

def createEnvelope():
    apiClient = configureApiClient()
    envelopesApi = EnvelopesApi(apiClient)
    envelope = envelopesApi.get_envelope("000000", "00000-0000-0000-00000-0000000");

def createTemplate():
            with open("C:\\Users\\User.Name\\Downloads\\LeaseAgreement (1).pdf", "rb") as file:
                content_bytes = file.read()
                base64_file_content = base64.b64encode(content_bytes).decode("ascii")

        # Create the document model
            document = Document(  # create the DocuSign document object
                document_base64=base64_file_content,
                name="Lorem Ipsum",  # can be different from actual file name
                file_extension="pdf",  # many different document types are accepted
                document_id=1  # a label used to reference the doc
            )

            # Create the signer recipient model
            signer = Signer(role_name="signer", recipient_id="1", routing_order="1")
            # create a cc recipient to receive a copy of the envelope (transaction)
            cc = CarbonCopy(role_name="cc", recipient_id="2", routing_order="2")
            # Create fields using absolute positioning
            # Create a sign_here tab (field on the document)
            sign_here = SignHere(document_id="1", page_number="1", x_position="191", y_position="148")
            
            # Add the tabs model to the signer
            # The Tabs object wants arrays of the different field/tab types
            signer.tabs = Tabs(
                sign_here_tabs=[sign_here]
            )

            # Top object:
            template_request = EnvelopeTemplate(
                documents=[document], email_subject="Please sign this document",
                recipients=Recipients(signers=[signer], carbon_copies=[cc]),
                description="Example template created via the API",
                name="Api Template Test",
                shared="false",
                status="created"
            )

            apiClient = configureApiClient()
            templates_api = TemplatesApi(apiClient)
            res = templates_api.create_template('11254982',template_request)
            

            
            
            #return template_request
            

#Call Methods Below
########################

createTemplate()

























