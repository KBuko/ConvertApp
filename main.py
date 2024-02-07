from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout

import requests
from concurrent.futures import ThreadPoolExecutor

from kivy.config import Config
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog

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
        text="Please, check your Internet connection. The application will be closed.",
        buttons=[
            MDFlatButton(
                text="Exit",
                on_release=lambda _: exit()
            )],
    )
    Htext.open()


class Container(BoxLayout):
    pool = ThreadPoolExecutor()

    pln = pool.submit(gatherData, 'pln')
    byn = pool.submit(gatherData, 'byn')
    uah = pool.submit(gatherData, 'uah')
    usd = pool.submit(gatherData, 'usd')
    eur = pool.submit(gatherData, 'eur')
    cad = pool.submit(gatherData, 'cad')

    pln_task = pln.result()
    byn_task = byn.result()
    uah_task = uah.result()
    usd_task = usd.result()
    eur_task = eur.result()
    cad_task = cad.result()

    currency_validator = {'pln': 0.00, 'byn': 0.00, 'uah': 0.00, 'usd': 0.00, 'eur': 0.00, 'cad': 0.00}

    def calculate(self, text, hint_text):
        input_list = {self.pln: 'Pln', self.byn: 'Byn', self.uah: 'Uah', self.usd: 'Usd', self.eur: 'Eur',
                      self.cad: 'Cad'}
        for i in input_list:
            if hint_text == input_list[i] and i.focus and i.text != '' \
                    and float(i.text) != Container.currency_validator[input_list[i].lower()]:
                return self.get_values(text, i)
            elif hint_text == input_list[i] and i.focus and i.text == '':
                for j in input_list.keys():
                    j.text = ''

    def get_values(self, text, start_currency):
        try:
            calculated_data = {
                self.pln: Container.pln_task, self.byn: Container.byn_task, self.uah: Container.uah_task,
                self.usd: Container.usd_task, self.eur: Container.eur_task, self.cad: Container.cad_task
            }
            for cur in Container.currency_validator.keys():
                Container.currency_validator[cur.lower()] = \
                    round((float(text) * calculated_data[start_currency][cur.upper()]), 2)

            self.pln.text = str(Container.currency_validator['pln'])
            self.byn.text = str(Container.currency_validator['byn'])
            self.usd.text = str(Container.currency_validator['usd'])
            self.uah.text = str(Container.currency_validator['uah'])
            self.eur.text = str(Container.currency_validator['eur'])
            self.cad.text = str(Container.currency_validator['cad'])
        except:
            no_internet()


class CalcApp(MDApp):
    dialog = None

    def build(self):
        self.icon = "images/YourConverter.png"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.primary_hue = "500"
        return Container()

    def dark_light(self):
        if self.theme_cls.theme_style == 'Light':
            self.theme_cls.theme_style = 'Dark'
            self.theme_cls.primary_palette = "BlueGray"
            self.theme_cls.primary_hue = "600"
        else:
            self.theme_cls.theme_style = 'Light'
            self.theme_cls.primary_hue = "500"
            self.theme_cls.primary_palette = "Teal"

    def clear_content(self, pln, byn, uah, usd, eur, cad):
        pln.text = byn.text = uah.text = usd.text = eur.text = cad.text = ''

    def about_n_charity(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Hi, dear user!",
                text="My name is Kate Buko, " \
                     "I developed this app for most convenient " \
                     "conversion of major currencies (in my opinion) within the current " \
                     "situation in the world. The application will be developed and " \
                     "supplemented with new features." \
                     "\n\nThanks for choosing \"YourConverter\"!",
                buttons=[
                    MDFlatButton(
                        text="Later",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda _: self.dialog.dismiss()
                    ),
                ],
            )
        self.dialog.open()

if __name__ == "__main__":
    CalcApp().run()
