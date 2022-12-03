from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout

from bs4 import BeautifulSoup
from requests import get

from kivy.config import Config
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog

Config.set('kivy', 'keyboard_mode', 'systemanddock')

to_pln = 'https://currency.world/convert/PLN/USD/BYN/UAH'
to_byn = 'https://currency.world/convert/BYN/USD/PLN/UAH'
to_usd = 'https://currency.world/convert/USD/PLN/BYN/UAH'
to_uah = 'https://currency.world/convert/UAH/PLN/BYN/USD'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

def no_internet():
    Htext = MDDialog(
        title="No internet",
        text="Please, check your internet connection",
    )
    Htext.open()

def get_currency_price_pln():
    full_page_to_pln = get(to_pln, headers=headers)
    soup = BeautifulSoup(full_page_to_pln.content, 'html.parser')
    convert_pln_byn = soup.find('input', {"id": "amountv2"}).get('value')
    convert_pln_usd = soup.find('input', {"id": "amountv1"}).get('value')
    convert_pln_uah = soup.find('input', {"id": "amountv3"}).get('value')
    return float(convert_pln_byn), float(convert_pln_usd), float(convert_pln_uah)


def add_result_pln(pln):
    bynCourse, usdCourse, uahCourse = get_currency_price_pln()
    byn = str(round((pln * bynCourse), 2))
    usd = str(round((pln * usdCourse), 2))
    uah = str(round((pln * uahCourse), 2))
    return {'byn': byn, 'usd': usd, 'uah': uah}


def get_currency_price_byn():
    full_page_to_byn = get(to_byn, headers=headers)
    soup = BeautifulSoup(full_page_to_byn.content, 'html.parser')
    convert_byn_pln = soup.find('input', {"id": "amountv2"}).get('value')
    convert_byn_usd = soup.find('input', {"id": "amountv1"}).get('value')
    convert_byn_uah = soup.find('input', {"id": "amountv3"}).get('value')
    return float(convert_byn_pln), float(convert_byn_usd), float(convert_byn_uah)


def add_result_byn(byn):
    plnCourse, usdCourse, uahCourse = get_currency_price_byn()
    pln = str(round((byn * plnCourse), 2))
    usd = str(round((byn * usdCourse), 2))
    uah = str(round((byn * uahCourse), 2))
    return {'pln': pln, 'usd': usd, 'uah': uah}


def get_currency_price_uah():
    full_page_to_uah = get(to_uah, headers=headers)
    soup = BeautifulSoup(full_page_to_uah.content, 'html.parser')
    convert_uah_pln = soup.find('input', {"id": "amountv1"}).get('value')
    convert_uah_byn = soup.find('input', {"id": "amountv2"}).get('value')
    convert_uah_usd = soup.find('input', {"id": "amountv3"}).get('value')
    return float(convert_uah_pln), float(convert_uah_byn), float(convert_uah_usd)


def add_result_uah(uah):
    plnCourse, bynCourse, usdCourse = get_currency_price_uah()
    pln = str(round((uah * plnCourse), 2))
    byn = str(round((uah * bynCourse), 2))
    usd = str(round((uah * usdCourse), 2))
    return {'pln': pln, 'byn': byn, 'usd': usd}


def get_currency_price_usd():
    full_page_to_usd = get(to_usd, headers=headers)
    soup = BeautifulSoup(full_page_to_usd.content, 'html.parser')
    convert_usd_pln = soup.find('input', {"id": "amountv1"}).get('value')
    convert_usd_byn = soup.find('input', {"id": "amountv2"}).get('value')
    convert_usd_uah = soup.find('input', {"id": "amountv3"}).get('value')
    return float(convert_usd_pln), float(convert_usd_byn), float(convert_usd_uah)


def add_result_usd(usd):
    plnCourse, bynCourse, uahCourse = get_currency_price_usd()
    pln = str(round((usd * plnCourse), 2))
    byn = str(round((usd * bynCourse), 2))
    uah = str(round((usd * uahCourse), 2))
    return {'pln': pln, 'byn': byn, 'uah': uah}


class Container(BoxLayout):
    ArrCurency = {'pln': 0.00, 'byn': 0.00, 'uah': 0.00, 'usd': 0.00}
    Empty_text = None

    def Calculate(self):
        if self.pln.text != '' and float(self.pln.text) != Container.ArrCurency['pln']:
            try:
                myCalculation = add_result_pln(float(self.pln.text))
                self.byn.text = myCalculation.get('byn')
                self.usd.text = myCalculation.get('usd')
                self.uah.text = myCalculation.get('uah')
                self.Set_values()
            except:
                 no_internet()

        elif self.byn.text != '' and float(self.byn.text) != Container.ArrCurency['byn']:
            try:
                myCalculation = add_result_byn(float(self.byn.text))
                self.pln.text = myCalculation.get('pln')
                self.usd.text = myCalculation.get('usd')
                self.uah.text = myCalculation.get('uah')
                self.Set_values()
            except:
                no_internet()

        elif self.uah.text != '' and float(self.uah.text) != Container.ArrCurency['uah']:
            try:
                myCalculation = add_result_uah(float(self.uah.text))
                self.pln.text = myCalculation.get('pln')
                self.byn.text = myCalculation.get('byn')
                self.usd.text = myCalculation.get('usd')
                self.Set_values()
            except:
                no_internet()

        elif self.usd.text != '' and float(self.usd.text) != Container.ArrCurency['usd']:
            try:
                myCalculation = add_result_usd(float(self.usd.text))
                self.pln.text = myCalculation.get('pln')
                self.byn.text = myCalculation.get('byn')
                self.uah.text = myCalculation.get('uah')
                self.Set_values()
            except:
                no_internet()

        else:
            def Mbox():
                self.Empty_text = MDDialog(
                    title="No data",
                    text="Please, enter the data for the calculation",
                )
                self.Empty_text.open()

            Mbox()

    def Set_values(self):
        Container.ArrCurency['pln'] = float(self.pln.text)
        Container.ArrCurency['byn'] = float(self.byn.text)
        Container.ArrCurency['uah'] = float(self.uah.text)
        Container.ArrCurency['usd'] = float(self.usd.text)


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

    def clear_content(self, pln, byn, uah, usd):
        pln.text = byn.text = uah.text = usd.text = ''
        Container.ArrCurency['pln'] = 0.00
        Container.ArrCurency['byn'] = 0.00
        Container.ArrCurency['uah'] = 0.00
        Container.ArrCurency['usd'] = 0.00

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
