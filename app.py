from bottle import Bottle, get, post, run, template, static_file
import x
import json
import os

app = Bottle()

@app.get('/css/<file_name:path>')
def serve_css(file_name):
    return static_file(file_name, root='./css')

@app.get('/images/<file_name:path>')
def serve_images(file_name):
    return static_file(file_name, root='./images')

@app.get('/js/<file_name:path>')
def serve_js(file_name):
    return static_file(file_name, root='./js')

@app.route('/')
def _():        
    return template("index", extra_head="")

@app.route('/malearbejde')
def _():
    return template("malearbejde")

@app.route('/spartling')
def _():
    return template("spartling")

@app.route('/renovering')
def _():
    return template("renovering")

@app.route('/vinduer-dore')
def _():
    return template("vinduer-dore")

@app.route('/gallery')
def _():
    try:
        thumbnails = x.get_thumbnails()

        return template("gallery", extra_head="", thumbnails=thumbnails, thumbnails_json = json.dumps(thumbnails))
    
    except Exception as ex:
        print(ex)
    finally:
        pass

@app.route('/kontakt')
def _():
    return template("kontakt")

@app.route('/upload')
def _():
    return template("upload")
@app.post('/upload')
def _():
    try:        
        x.upload()
        return "image resized and saved successfully"
    except Exception as ex:
        print(ex)
    finally:
        pass
@app.post('/tilbud')
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
# port = int(os.environ.get("PORT", 8000))

# run(host='0.0.0.0', port=port, debug=True, reloader=True)
if __name__ == "__main__":
    # Development-only configurations
    port = int(os.environ.get("PORT", 8000))
    run(app, host='0.0.0.0', port=port, debug=True, reloader=True)
