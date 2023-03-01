from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from ingrediints import ing
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRaisedButton

KV = '''
<Content>
    id:content
    orientation: "horizontal"
    spacing: "15dp"
    size_hint_y: None
    height: self.minimum_height
    MDTextField:
        id: gramms
        line_color_focus: "white"
        line_color_normal: "#173B1E"
    MDLabel:
        id: texts
        text: ""
        theme_text_color: "Custom"
        text_color: [0, 0, 0, 0.5]

MDScreen:
    id: scr
    scr1: scr1
    MDBottomNavigation:
        text_color_normal: "#173B1E"
        panel_color: "#BCBCBC"
        selected_color_background: "#173B1E"
        text_color_active: "black"
        MDBottomNavigationItem:
            size_hint_x: .97
            pos_hint: {"center_x":.5}
            id: scr1
            name: 'screen 1'
            text: 'Ингредиенты'
            icon: 'fridge'
            badge_icon: "numeric-10"
            MDScrollView:
                bar_color: "#173B1E"
                pos_hint:{"center_x":.5,"center_y":.72}
                size_hint_y: .2
                MDList:
                    id: container

            MDScrollView:
                bar_color: "#173B1E"
                pos_hint:{"center_x":.5,"center_y":.25}
                size_hint_y: .5
                MDList:
                    id: list_products
            BoxLayout:
                size_hint_y: None
                height: self.minimum_height
                pos_hint: {"center_x": .5, "center_y": 0.9}
                MDTextField:
                    line_color_focus: "white"
                    line_color_normal: "#173B1E"
                    id:pole
                    helper_text_mode: "persistent"
                    helper_text: "Вводи ингредиенты, бездарь"
                    on_text: app.indigrid()
                MDIconButton:
                    icon: "close"
                    theme_icon_color: "Custom"
                    icon_color: "#173B1E"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    on_press: app.clear()


        MDBottomNavigationItem:
            name: 'screen 2'
            text: 'Рецепты'
            icon: 'silverware-variant'


            MDLabel:

                text: 'Рецепты'
                halign: 'center'

        MDBottomNavigationItem:
            name: 'screen 3'
            text: 'Любимое'
            icon: 'heart'
            MDLabel:
                text: 'Избранное'
                halign: 'center'

'''

products = {}
product = ''


class Content(BoxLayout):
    pass


class Test(MDApp):
    dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)

    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Light"
        return self.screen

    def indigrid(self):
        self.root.ids.container.clear_widgets()
        to_print = set()
        for i in ing.keys():
            if len(self.screen.ids.pole.text.lower()) != 0 and self.screen.ids.pole.text.lower() == i[
                                                                                                    :len(
                                                                                                        self.screen.ids.pole.text)].lower():
                to_print.add(i.capitalize())
        if len(to_print) == 0:
            pass
        for i in to_print:
            self.root.ids.container.add_widget(
                OneLineListItem(text=i, on_release=self.dobavka, theme_text_color="Custom", divider_color="green"))

    def dobavka(self, arg):
        global product
        product = arg.text
        if not self.dialog:
            self.dialog = MDDialog(
                title="Вводи количество штук-дрюк",
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDRaisedButton(
                        text="ОТМЕНА",
                        on_press=self.zakritie,
                        md_bg_color="#173B1E"
                    ),
                    MDRaisedButton(
                        text="ДОБАВИТЬ",
                        on_press=self.final,
                        md_bg_color="#173B1E"
                    ),
                ],
            )
        self.dialog.content_cls.ids.texts.text = ing[arg.text]
        self.dialog.content_cls.ids.gramms.text = ''
        self.dialog.open()

    def final(self, arg):
        self.dialog.dismiss(force=True)
        products[product] = self.dialog.content_cls.ids.gramms.text
        self.root.ids.list_products.clear_widgets()
        for i in products.keys():
            self.root.ids.list_products.add_widget(
                OneLineListItem(text=f'{i} - {products[i]} {ing[i]}', on_release=self.udalenie,
                                theme_text_color="Custom", divider_color="green"))

    def udalenie(self, arg):
        nazv = arg.text.split(' - ')
        del products[nazv[0]]
        self.root.ids.list_products.clear_widgets()
        for i in products.keys():
            self.root.ids.list_products.add_widget(
                OneLineListItem(text=f'{i} - {products[i]}', on_release=self.udalenie,
                                theme_text_color="Custom", divider_color="green"))

    def zakritie(self, arg):
        self.dialog.dismiss(force=True)

    def clear(self):
        self.screen.ids.pole.text = ''


Test().run()
