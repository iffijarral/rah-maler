from bottle import Bottle, get, post, run, template, static_file
import x
import json
import os

app = Bottle()  

@get('/css/<file_name:path>')
def serve_css(file_name):
    return static_file(file_name, root='./css')

@get('/images/<file_name:path>')
def serve_images(file_name):
    return static_file(file_name, root='./images')

@get('/js/<file_name:path>')
def serve_js(file_name):
    return static_file(file_name, root='./js')

@get('/')
def _():    
    return "Hello World"
    # return template("index", extra_head="")

@get('/malearbejde')
def _():
    return template("malearbejde")

@get('/spartling')
def _():
    return template("spartling")

@get('/renovering')
def _():
    return template("renovering")

@get('/vinduer-dore')
def _():
    return template("vinduer-dore")

@get('/gallery')
def _():
    try:
        thumbnails = x.get_thumbnails()

        return template("gallery", extra_head="", thumbnails=thumbnails, thumbnails_json = json.dumps(thumbnails))
    
    except Exception as ex:
        print(ex)
    finally:
        pass

@get('/kontakt')
def _():
    return template("kontakt")

@get('/upload')
def _():
    return template("upload")
@post('/upload')
def _():
    try:        
        x.upload()
        return "image resized and saved successfully"
    except Exception as ex:
        print(ex)
    finally:
        pass
@post('/tilbud')
def tilbud():
    try:
        result = isInputValid()
        if result is True:
            print('no error')
            return "Success"  # Or redirect to a success page
        else:
            return result
    except Exception as ex:
        print(ex)
        return "An unexpected error occurred"
    finally:
        pass

def isInputValid():
    name = x.validate_name()
    email = x.validate_email()
    phone = x.validate_phone()
    postnr = x.validate_post_no()
    city = x.validate_city()
    message = x.validate_message()
    answer = x.validate_question()
    
    hasError = False
    html = ''
    
    if name:
        html += f"""    
            <template mix-target="#name-error" mix-replace>
                <span id="name-error" class="text-red-500 text-xs"> </span>
            </template>                
        """
    else:
        hasError = True
        html += f"""    
            <template mix-target="#name-error" mix-replace>
                <span id="name-error" class="text-red-500 text-xs"> Angiv venligst et gyldigt navn. </span>
            </template>                
        """
    
    if email:
        html += f"""    
            <template mix-target="#email-error" mix-replace>
                <span id="email-error" class="text-red-500 text-xs"> </span>
            </template>                             
        """
    else:
        hasError = True
        html += f"""    
            <template mix-target="#email-error" mix-replace>
                <span id="email-error" class="text-red-500 text-xs"> Angiv venligst en gyldig email. </span>
            </template>                             
        """
    
    if phone:
        html += f"""    
            <template mix-target="#phone-error" mix-replace>
                <span id="phone-error" class="text-red-500 text-xs"> </span>
            </template>                
        """
    else:
        hasError = True
        html += f"""    
            <template mix-target="#phone-error" mix-replace>
                <span id="phone-error" class="text-red-500 text-xs"> Angiv venligst et gyldigt telefon nr. </span>
            </template>                
        """
    
    if postnr:
        html += f"""    
            <template mix-target="#postno-error" mix-replace>
                <span id="postno-error" class="text-red-500 text-xs"> </span>
            </template>                             
        """
    else:
        hasError = True
        html += f"""    
            <template mix-target="#postno-error" mix-replace>
                <span id="postno-error" class="text-red-500 text-xs"> Angiv venligst gyldigt postnr. </span>
            </template>                             
        """
    
    if city:
        html += f"""    
            <template mix-target="#city-error" mix-replace>
                <span id="city-error" class="text-red-500 text-xs"> </span>
            </template>                             
        """
    else:
        hasError = True
        html += f"""    
            <template mix-target="#city-error" mix-replace>
                <span id="city-error" class="text-red-500 text-xs"> Angiv venligst en gyldig by. </span>
            </template>                             
        """
    
    if message:
        if len(message) < 500:
            html += f"""    
                <template mix-target="#message-error" mix-replace>
                    <span id="message-error" class="text-red-500 text-xs"> </span>                    
                </template>                             
            """
        else:
            hasError = True
            html += f"""    
                <template mix-target="#message-error" mix-replace>
                    <span id="message-error" class="text-red-500 text-xs"> Besked kan ikke være mere end 500 tegn. </span>
                </template>                             
            """        
    else:
        hasError = True
        html += f"""    
            <template mix-target="#message-error" mix-replace>
                <span id="message-error" class="text-red-500 text-xs"> Angiv venligst en besked. </span>
            </template>                             
        """ 
    
    if answer == 5:
        html += f"""    
            <template mix-target="#question-error" mix-replace>
                <span id="question-error" class="text-red-500 text-xs"> </span>
            </template>                             
        """
    else:
        hasError = True            
        html += f"""    
            <template mix-target="#question-error" mix-replace>
                <span id="question-error" class="text-red-500 text-xs"> Angiv venligst et korrekt svar. </span>
            </template>                             
        """
    
    if hasError:
        return html
    else:
        return True

# run(host='0.0.0.0', port=8080, debug=True, reloader=True)
# Handler for Vercel
if __name__ == "__main__":
    run(app, host='0.0.0.0', port=8080)
