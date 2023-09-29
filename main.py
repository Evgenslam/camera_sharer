import time
import webbrowser
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from filesharer import Filesharer
from kivy.core.clipboard import Clipboard


Builder.load_file('frontend.kv')


class CameraScreen(Screen):
    def start(self):
        """Starts camera and changes button text"""
        self.ids.camera.play = True
        self.ids.toggle_button.text = 'Stop camera'
        self.ids.camera.texture = self.ids.camera._camera.texture

    def stop(self):
        """Stops camera and changes button text"""
        self.ids.camera.play = False
        self.ids.toggle_button.text = 'Start camera'
        self.ids.camera.texture = None

    def capture(self):
        """Saves screenshot of camera into a png file named with
        datetime when it is done. Changes the screen to display
        the screenshot and call to action"""
        current_time = time.strftime('%Y%m%d-%H%M%S')
        self.filepath = f'files/{current_time}.png'
        self.ids.camera.export_to_png(self.filepath)
        self.manager.current = 'image_screen'
        self.manager.current_screen.ids.screenshot.source = self.filepath


class ImageScreen(Screen):
    link_message = 'Please generate the link first'

    def generate_link(self):
        """Access the file saved locally, uploads it to web and
        inserts the file link to label widget"""
        filepath = App.get_running_app().root.ids.camera_screen.filepath
        filesharer = Filesharer(filepath=filepath)
        self.uploaded_filelink = filesharer.share()
        self.ids.link.text = self.uploaded_filelink

    def copy_link(self):
        """Copies link to the clipboard. Shows reminder when no
        has been generated"""
        try:
            Clipboard.copy(self.uploaded_filelink)
        except:
            self.ids.link.text = self.link_message

    def open_link(self):
        """Opens link in default webbrowser. Shows reminder when
         no has been generated"""
        try:
            webbrowser.open(self.uploaded_filelink)
        except:
            self.ids.link.text = self.link_message


class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


MainApp().run()
