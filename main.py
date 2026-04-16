from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout

import requests
from concurrent.futures import ThreadPoolExecutor

from kivy.config import Config
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu

import re

Config.set('kivy', 'keyboard_mode', 'systemanddock')


def gatherData(i):
    s = requests.Session()
    try:
        data = s.get(url=f'https://api.exchangerate-api.com/v4/latest/{i}').json()
        currency_dict = data['rates']
        return currency_dict
    except:
        pass


def no_internet():
    Htext = MDDialog(
        title="No internet",
        text="Please, check your internet connection. The app will be closed.",
        buttons=[
            MDFlatButton(
                text="Exit",
                on_release=lambda _: exit()
            )],
    )
    Htext.open()


class Container(BoxLayout):

    currency_validator = {'pln': 0, 'byn': 0, 'uah': 0, 'usd': 0, 'eur': 0, 'gbp': 0, 'cad': 0}

    pool = ThreadPoolExecutor()

    futures = {}
    for code in currency_validator.keys():
        futures[code] = pool.submit(gatherData, code)


    def calculate(self, text, hint_text):
        input_list = {self.pln: 'Pln', self.byn: 'Byn', self.uah: 'Uah', self.usd: 'Usd', self.eur: 'Eur', self.gbp: 'Gbp', self.cad: 'Cad'}

        for i in input_list:
            if hint_text == input_list[i] and i.focus and i.text != '':
                text = re.sub(r'[^0-9.,]', '', text).replace(',', '.')
                if text.count('.') > 1:
                    first_dot = text.find('.')
                    text = text.replace('.','')
                    text = text[:first_dot]+'.'+text[first_dot:]
                if re.fullmatch(r'\d+(\.\d{0,3})?', text) or re.fullmatch(r'\d+\.', text):
                    return self.get_values(text, i)
                else:
                    for j in input_list.keys():
                        j.text = ''


    def get_values(self, text, start_currency):
        try:
            results = {}
            for code, future in Container.futures.items():
                results[f'{code}_task'] = future.result()

            calculated_data = {
                self.pln: results['pln_task'], self.byn: results['byn_task'], self.uah: results['uah_task'],
                self.usd: results['usd_task'], self.eur: results['eur_task'], self.cad: results['cad_task'],
                self.gbp: results['gbp_task'],
            }

            for cur in Container.currency_validator.keys():
                Container.currency_validator[cur.lower()] = \
                    round((float(text) * calculated_data[start_currency][cur.upper()]), 3)

            self.pln.text = str(Container.currency_validator['pln'])
            self.byn.text = str(Container.currency_validator['byn'])
            self.usd.text = str(Container.currency_validator['usd'])
            self.uah.text = str(Container.currency_validator['uah'])
            self.eur.text = str(Container.currency_validator['eur'])
            self.gbp.text = str(Container.currency_validator['gbp'])
            self.cad.text = str(Container.currency_validator['cad'])
        except:
            no_internet()


class CalcApp(MDApp):
    dialog = None

    def build(self):
        self.icon = "images/YourConverter.png"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.primary_hue = "500"

        menu_items = [
            {
                "text": f"Dark/Light theme",
                "leading_icon": "theme-light-dark",
                "height": dp(50),
                "on_release": lambda x=f"Dark/Light theme": self.dark_light(),
            },
            {
                "text": f"About",
                "leading_icon": "charity",
                "height": dp(50),
                "on_release": lambda x=f"About": self.about_n_charity(),
            },
            {
                "text": f"Exit",
                "leading_icon": "logout",
                "height": dp(50),
                "on_release": lambda x=f"Quit": exit(),
            }
        ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )
        return Container()


    def callback(self, button):
        self.menu.caller = button
        self.menu.open()


    def dark_light(self):
        if self.theme_cls.theme_style == 'Light':
            self.theme_cls.primary_palette = "BlueGray"
            self.theme_cls.theme_style = 'Dark'
            self.theme_cls.primary_hue = "600"
        else:
            self.theme_cls.primary_palette = "Teal"
            self.theme_cls.theme_style = 'Light'
            self.theme_cls.primary_hue = "500"


    def clear_content(self, pln, byn, uah, usd, eur, gbp, cad):
        pln.text = byn.text = uah.text = usd.text = eur.text = gbp.text = cad.text = ''


    def about_n_charity(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Hi, dear user!",
                text="My name is Kate Buko, " \
                     "I developed this app for most convenient " \
                     "conversion of major currencies (in my opinion) within the current " \
                     "situation in the world. The application will be developed and " \
                     "supplemented with new features." \
                    # "\n\nYou can support the project: just click on the \"See ads\" button." \
                     "\n\nThanks for choosing \"YourConverter\"!",
                buttons=[
                    # MDRaisedButton(
                    #    text="See ads",
                    #    theme_text_color="Custom",
                    #    on_release=lambda a: self.ads.show_rewarded_ad()
                    # ),
                    MDFlatButton(
                        text="close it",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_press=lambda _: self.dialog.dismiss()
                    ),
                ],
            )
        self.dialog.open()


if __name__ == "__main__":
    CalcApp().run()
