from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from db_operations import DbOperations
from Trie import Trie
import pyttsx3 as sx3
# initializing the object
engine = sx3.init()


def text_to_speech(info):
    engine.say(info)
    engine.runAndWait()




searchedWord:str = ''

db = DbOperations()
dictionary = db.readJson()
keys = dictionary["allWords"]
trie = Trie()

for key in keys:
    trie.insert(key)



#functions searches for word
def searchWordFromDictionary(word):
    return dictionary.get(word, None)


#function to work on getting synonyms
def shouldFindSyn(word: str, synonymArr: list):
    for synonym in synonymArr:
        synonym = synonym.lower()
        data = {
            "meaning": f"Word Not Found, check out {word}",
            "synonym": [],
        }
        if(not synonym in dictionary):
            dictionary[synonym] = data
            dictionary['allWords'] = synonym

    db.writeToJson(dictionary)



class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        
        # Create a FloatLayout
        layout = FloatLayout()
        
        # Add a top app bar
        top_app_bar = MDTopAppBar(
            title="SHORTMAN DICTIONARY",
            md_bg_color=(0.2, 0.2, 0.2, 1),
            left_action_items=[["menu", lambda x: None]],
            size_hint=(1, None),
            height='56dp',
            pos_hint={'top': 1}  # Position at the top of the layout
        )
        layout.add_widget(top_app_bar)
        
        # Add an image
        image = Image(
            source="Images/open-book.png",  
            size_hint=(None, None),
            size=(300, 300),  
            pos_hint={'center_x': 0.5, 'center_y': 0.6}  
        )
        layout.add_widget(image)
        
        # Add a text input field
        self.text_input = MDTextField(
            hint_text="Enter a word",
            size_hint=(None, None), # Disable size_hint so you can specify exact size
            size=(250, 48),
            pos_hint={'center_x': 0.5, 'center_y': 0.3}
        )
        self.text_input.bind(on_text_validate=self.search_word) 
        layout.add_widget(self.text_input)
        
        # Add a label for displaying word not found message (initially hidden)
        self.error_label = Label(
            text= f"Word not found in dictionary",
            size_hint=(None, None),
            size=(250, 48),
            pos_hint={'center_x': 0.5, 'center_y': 0.25},
            color=(1, 0, 0, 1),  # Red color for error message
            opacity=0  # Initially hidden
        )
        layout.add_widget(self.error_label)
        
        self.text_input.bind(text=self.update_error_label) 
        
        # Add a search button
        search_button = MDIconButton(
            icon="magnify",
            pos_hint={'right': 0.7, 'center_y': 0.3}
        )

        search_button.bind(on_release=self.search_word)
        layout.add_widget(search_button)
        

        # Add a button to navigate to the AddWordScreen
       
        add_word_button = MDFlatButton(
            text="Add Word",
            pos_hint={'right': 0.55, 'center_y': 0.2}
        )

        add_word_button.bind(on_release=self.go_to_add_word_screen)
        layout.add_widget(add_word_button)
        
        # Centered layout for the image
        self.image_layout = FloatLayout(size_hint=(None, None), size=(300, 300), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(self.image_layout)
        
        # Add the layout to the screen
        self.add_widget(layout)

    def update_error_label(self, instance, value):
            searched_word = value.lower()
            similar_words = trie.get_similar_words(searched_word)
            if similar_words:
                self.error_label.text = f"Word not found in dictionary. Did you mean {similar_words[0]}"
            else:
                self.error_label.text = "Word not found in dictionary."
                
    def search_word(self, instance):
        # Get the entered word from the text input field
        word = self.text_input.text
        searchedWord = word.lower()
        print(searchedWord)
        
        result = searchWordFromDictionary(word.lower())
        
        # If the word is found, switch to the new screen and display the meaning and image
        if result:
            self.error_label.opacity = 0  # Hide error label
            self.manager.get_screen('meaning_screen').display_meaning(word.lower(), result["meaning"],result["synonym"], result.get("img", None))
            self.manager.current = 'meaning_screen'
        else:
            # Display word not found message
            
            self.error_label.opacity = 1  # Show error label

    def go_to_add_word_screen(self, instance):
        self.manager.current = 'add_word_screen'
    
    

class AddWordScreen(Screen):
    def __init__(self, **kwargs):
        super(AddWordScreen, self).__init__(**kwargs)

        # Create a FloatLayout
        layout = FloatLayout()

        # Add text input fields for word, meaning, and image
        self.word_input = MDTextField(
            hint_text="Enter the word",
            size_hint=(None, None),
            size=(250, 48),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        layout.add_widget(self.word_input)

        self.meaning_input = MDTextField(
            hint_text="Enter the meaning",
            size_hint=(None, None),
            size=(250, 48),
            pos_hint={'center_x': 0.5, 'center_y': 0.6}
        )
        layout.add_widget(self.meaning_input)

        self.synonym_input = MDTextField(
            hint_text="Synonyms seperated with spaces",
            size_hint=(None, None),
            size=(250, 48),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        layout.add_widget(self.synonym_input)

        # Add a button to submit the word, meaning, and image
        submit_button = MDFlatButton(
            text="Submit",
            pos_hint={'center_x': 0.5, 'center_y': 0.4}
        )
        submit_button.bind(on_release=self.submit_word)
        layout.add_widget(submit_button)

        # Add the layout to the screen
        self.add_widget(layout)

        # Add the back button
        back_button = Button(text='Back', size_hint=(None, None), size=('100dp', '48dp'), pos_hint={'center_x': 0.5, 'y': 0})
        back_button.bind(on_release=self.go_back)
        layout.add_widget(back_button)

    # Add word, meaning, and image to the hash table
    def submit_word(self, instance):
        word = self.word_input.text
        meaning = self.meaning_input.text
        synonym = self.synonym_input.text

        synonymArr = []
        value = ""

        # indexf for traversing through synonym
        i = 0
        while(i < len(synonym)):
            if not synonym[i] == " ":
                value += synonym[i]
            else:
                synonymArr.append(value)
                value = ""

            if not value in synonymArr and i == len(synonym) - 1:
                synonymArr.append(value)
            i += 1

        if word and meaning:
            #word in dictionary template
            data = {
                    "meaning": meaning,
                    "synonym": synonymArr,
            }

            # Add the word to the dictionary
            dictionary[word.lower()] = data
            dictionary['allWords'].append(word.lower())
            db.writeToJson(dictionary)

            shouldFindSyn(word.lower(), synonymArr)

            print("Word added successfully:", word, meaning)
            self.manager.current = 'main_screen'
        else:
            print("Please fill all fields.")

    def go_back(self, instance):
        self.manager.current = 'main_screen'

class MeaningScreen(Screen):
    def __init__(self, **kwargs):
        super(MeaningScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()

        # Add a 'Back' button
        back_button = Button(text='Back', size_hint=(None, None), size=('100dp', '48dp'), pos_hint={'center_x': 0.08, 'y': 0})
        back_button.bind(on_release=self.go_back)

        back_button.background_color = (0.2, 0.7, 0.3, 1)  

        self.layout.add_widget(back_button)

        # BoxLayout to contain the meaning with background color
        meaning_box = FloatLayout(size_hint=(None, None), size=('300dp', '200dp'), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Label to display the searched word
        self.word_label = Label(text='', color=(0, 0, 0, 1), font_size='24sp', size_hint=(None, None), size=('300dp', '50dp'), pos_hint={'center_x': 0.5, 'top': 1.5})
        meaning_box.add_widget(self.word_label)
        

        # Label to display the meaning
        self.meaning_label = Label(text='', color=(0, 0, 0, 1), font_size='18sp', size_hint=(None, None), size=(300, 200), pos_hint={'center_x': 0.5, 'center_y': 0.9}, text_size=(300, None), halign='center', valign='middle')
        meaning_box.add_widget(self.meaning_label)

        # Label to display the synonym
        self.synonym_label = Label(text='', color=(0, 0, 20, 1), font_size='18sp', size_hint=(None, None), size=(100, 100), pos_hint={'center_x': 0.5, 'center_y': 1.1}, text_size=(300, None), halign='center', valign='middle')
        meaning_box.add_widget(self.synonym_label)


        # Image widget to display the image
        self.image_widget = Image(source='', size_hint=(None, None), size=(200, 200), pos_hint={'center_x': 0.5, 'center_y': 0.1})
        self.image_widget.size = (250, 250)
        meaning_box.add_widget(self.image_widget)
        

        # Add the layout to the screen
        self.layout.add_widget(meaning_box)

        # Add a delete button
        delete_button = Button(text='Delete', size_hint=(None, None), size=('100dp', '48dp'), pos_hint={'right': 1, 'y': 0})
        delete_button.bind(on_release=self.delete_word)
        delete_button.background_color = (100, 0, 0, 1)

        self.layout.add_widget(delete_button)

        audio_button = Button(size_hint=(None, None), size=('24dp', '24dp'),
                              pos_hint={'right': 0.55, 'top': -0.65})
        
        audio_button.bind(on_release=self.play_audio)
        audio_button.background_normal = 'Images/audio.png'  
        meaning_box.add_widget(audio_button)

        # Add the layout to the screen
        self.add_widget(self.layout)


    def display_meaning(self, word, meaning:str,synonym:list, image_filename):
        # Update the labels with the searched word and its meaning
        self.word_label.text = word
        self.meaning_label.text = meaning

        words = ""
        for word in synonym:
            if not len(synonym) > 1 or word == synonym[len(synonym)-1]:
                seperator = ""
            else:
                seperator = ","
            
            words += word + seperator

        self.synonym_label.text= f"synonyms: {words}"

        # Update the image widget with the image filename
        if image_filename:
            self.image_widget.source = image_filename

    def go_back(self, instance):
        # Switch back to the main screen
        self.manager.current = 'main_screen'
    
    def play_audio(self, instance):
        text_to_speech(self.word_label.text)
    
    def delete_word(self, instance):
        word = self.word_label.text
        # Remove the word from the dictionary and image hash table
        if word in dictionary:

            all_synonyms = dictionary[word.lower()]["synonym"]
            for synonym in all_synonyms:
                if synonym in dictionary and not dictionary[synonym]["meaning"] == f"Word Not Found, check out "+word:
                    del dictionary[synonym]

            del dictionary[word]

            new_all_words:list = dictionary['allWords']
            new_all_words.remove(word)
            dictionary['allWords'] = new_all_words
            db.writeToJson(dictionary)

        print("Word deleted successfully:", word)
        # Go back to the main screen
        self.manager.current = 'main_screen'


        

class DictionaryApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main_screen'))
        sm.add_widget(MeaningScreen(name='meaning_screen'))
        sm.add_widget(AddWordScreen(name='add_word_screen'))
        return sm

if __name__ == '__main__':
    DictionaryApp().run()