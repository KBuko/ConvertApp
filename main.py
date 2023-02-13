from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout

import asyncio
import aiohttp

from kivy.config import Config
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog

Config.set('kivy', 'keyboard_mode', 'systemanddock')

async def GatherData(i):
    try:
        session = aiohttp.ClientSession()
        async with session.get(url=f'https://api.exchangerate-api.com/v4/latest/{i}') as r:
            currency_dict = (await r.json())['rates']
            r.close()
        return currency_dict
    except:
        pass


def call_gathering():
    pln_task = asyncio.ensure_future(GatherData('pln'))
    byn_task = asyncio.ensure_future(GatherData('byn'))
    uah_task = asyncio.ensure_future(GatherData('uah'))
    usd_task = asyncio.ensure_future(GatherData('usd'))
    eur_task = asyncio.ensure_future(GatherData('eur'))
    cad_task = asyncio.ensure_future(GatherData('cad'))
    return asyncio.gather(pln_task, byn_task, uah_task, usd_task, eur_task, cad_task)


def no_internet():
    Htext = MDDialog(
        title="No internet",
        text="Please check your Internet connection. The application will be closed.",
        buttons=[
            MDFlatButton(
                text="Exit",
                on_release=lambda _: exit()
            )],
    )
    Htext.open()


class Container(BoxLayout):
    loop = asyncio.get_event_loop()
    pln_task, byn_task, uah_task, usd_task, eur_task, cad_task = loop.run_until_complete(call_gathering())
    loop.close()

    currency_validator = {'pln': 0.00, 'byn': 0.00, 'uah': 0.00, 'usd': 0.00, 'eur': 0.00, 'cad': 0.00}

    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)

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
        calculated_data = {
            self.pln: Container.pln_task, self.byn: Container.byn_task, self.uah: Container.uah_task,
            self.usd: Container.usd_task, self.eur: Container.eur_task, self.cad: Container.cad_task
        }
        try:
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
                     "\n\nYou can support the project: just click on the \"See ads\" button." \
                     "\n\nThanks for choosing \"YourConverter\"!",
                buttons=[
                    MDRaisedButton(
                        text="See ads",
                        theme_text_color="Custom",
                        on_release=lambda _: self.dialog.dismiss()

                    ),
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
