import flet as ft
from typing import Union


class Display(ft.Container):
    def __init__(self,
                 
            data = None,
            value = None,
            opitions = None, #lista
            height =40,
            width = 120, 
            bgcolor = 'black' ,
            tipos_dados: Union[float, int, str] = [int, float],
            borda_width = 4,
            text_size = 25,
            border_radius = 10,
            func = None,
            on_click = None,
            text_color = None,
            text_align = 'center', #Optional[TextAlign] = None,
            horizontal_alignment = 'center' #CrossAxisAlignment
        ): 
        super().__init__()
        self.opitions = opitions
        self.func = func
        self.on_click = on_click
        self.data = data
        if self.opitions is None:
            self.opitions = [ft.PopupMenuItem(i, data = self.data, on_click = self.Clicou, padding = ft.Padding(0,0,0,0)) for i in range(30,250,1)]
        else:
            self.opitions = [ft.PopupMenuItem(i, data = self.data, on_click = self.Clicou, padding = ft.Padding(0,0,0,0)) for i in opitions]

        self.border_radius =border_radius
        self.borda_width = borda_width
        self.text_size = text_size
        if borda_width > 0:
            self.border = ft.border.all(self.borda_width, ft.colors.with_opacity(0.6,'blue'))
        else:
            self.border = None
        self.data = data
        self._value = value
        self.bgcolor = bgcolor
        self.height =height
        self.width = width
        self.padding = ft.Padding(0,0,0,0)
        self._text_color = text_color
        self.tipos_dados = tipos_dados
        self.text_align = text_align
        self.horizontal_alignment = horizontal_alignment
        self._campotexto = ft.TextField(dense=True, on_submit=self.SetarValue)
        self.on_long_press = self.VirarCampoTexto

        self.content = ft.PopupMenuButton(
            content=ft.Column([ft.Text(self._value, color = self._text_color, weight='BOLD', size=self.text_size, no_wrap = False,text_align = self.text_align  )], alignment='center', horizontal_alignment= self.horizontal_alignment),
            items=self.opitions,
            menu_position=ft.PopupMenuPosition.UNDER,
        
        )

    def SetarValue(self,e):
        self._value = self._campotexto.value
        self.content = ft.PopupMenuButton(
            content=ft.Column([ft.Text(self._value, color = self._text_color, weight='BOLD', size=self.text_size, no_wrap = False,text_align = self.text_align  )], alignment='center', horizontal_alignment= self.horizontal_alignment),
            items=self.opitions,
            menu_position=ft.PopupMenuPosition.UNDER,
        
        )
        if not self.func is None:
            self.func(self._value)
        if not self.on_click is None:
            self.on_click(e)            
        self.Atualizar() 

    def VirarCampoTexto(self,e):
        content_antigo = self.content
        self.content = self._campotexto
        if not self.on_click is None:
            self.on_click(e)  
        self.Atualizar()


    def Clicou(self,e):
        if type(e.control.text) in [int, float]:
            valor = round(e.control.text,1)
        else:
           valor = e.control.text 
        self.content.content.controls[0].value = valor
        self._value = valor
        if not self.func is None:
            self.func(valor)
        if not self.on_click is None:
            self.on_click(e)            
        self.Atualizar()



    def Atualizar(self):
        try:
            self.update()
        except:
            pass

    @property
    def value(self):
        try:
            v = int(self._value)
        except:
            try:
                v = float(self._value)
            except:            
                v = self._value
        return v

    @value.setter
    def value(self, valor):
        if isinstance(self.content, ft.PopupMenuButton):
            if type(valor in self.tipos_dados):
                self._value = valor
                self.content.items.append(ft.PopupMenuItem(valor, on_click = self.Clicou))
                self.content.content.controls[0].value = valor
                self.Atualizar()
            else:
                print('número inválido')
        elif isinstance(self.content, ft.TextField):
            if type(valor in self.tipos_dados):
                self._value = valor
                self.content.value = valor
                self.Atualizar()
            else:
                print('número inválido')


    @property
    def text_color(self):
        return self._text_color

    @text_color.setter
    def text_color(self, cor):
        self._text_color = cor  
        colors = {
            '16': 'red',
            '15': '#ff9900',
            '14': '#ffd966',
            '13': '#93c47d',
            '12': '#ea9999',
            '11': '#ffff00',
            '10': '#d9ead3',
            '9': '#c9daf8',
            '8': '#d9d9d9',
        }        

        self.content = ft.PopupMenuButton(
            content=ft.Column([ft.Text(self._value, color = self._text_color, weight='BOLD', size=self.text_size, no_wrap = False,text_align = 'center' )], alignment='center', horizontal_alignment='center'),
            items=self.opitions,
            menu_position=ft.PopupMenuPosition.UNDER,        
        )
         
        self.Atualizar()


class My_tabelaC(ft.Column):
    def __init__(self, dic# dicionário
                    ):
        super().__init__()
        self.spacing = 0
        self.run_spacing = 0
        self._dic = dic          
        self.Linhas()




    def Colunas(self):
        self.chaves = list(self._dic.keys())
        self.larguras = {i:60 for i in self.chaves}
        self.opcoes = self._dic[self.chaves[0]]
        self.controls = [ft.Container(ft.Row([ft.Text(i, width=self.larguras[i], text_align='center') for i in self.chaves], tight=True),bgcolor='white,0.3')]

            
    def Linhas(self):
        self.Colunas()
        for i, k in enumerate(self._dic[self.chaves[0]]):     
            cor  = 'black' if i%2 == 0 else  'white,0.1'  
            self.controls.append(
                ft.Container(ft.Row([
                                Display(value = self._dic[self.chaves[0]][i],opitions=self.opcoes, width=self.larguras[self.chaves[0]],height=20,text_size = 12, 
                                        borda_width = 0,border_radius = 0, 
                                                text_align= ft.TextAlign.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, bgcolor = 'white,0')
                ]+[ft.Text(self._dic[j][i],width=self.larguras[j], text_align='center') for j in self.chaves[1:]], tight=True),bgcolor=cor)
                
                )
            
    @property
    def dic(self):
        return self._dic
    
    @dic.setter
    def dic(self, dic):
        if isinstance(dic, dict):
            self._dic = dic
            self.Linhas()
        self.update()




def main(page: ft.Page):
    # page.title = "Guerra de Clans"
    # page.window.width = 500  # Define a largura da janela como 800 pixels
    # page.window.height = 770  #    
    page.theme_mode = ft.ThemeMode.DARK


    dic = {'Jogador':list(range(15)), 'Vila':list(range(15)), 'Estrelas': list(range(15))}
    dic2 = {'Jogador':list(range(10)), 'Vila':list(range(10)), 'Estrelas': list(range(10))}
    def mudar(e):
        e.control.data = not e.control.data
        if e.control.data:
            tabela.dic = dic
        else:
            tabela.dic = dic2
    bt = ft.TextButton('mudar', on_click=mudar, data = True)

    tabela = My_tabelaC(dic)

    page.add(bt,tabela)


if __name__ == '__main__':  
    
    ft.app(main,
    #    view = ft.AppView.WEB_BROWSER
    # port = 8050
       )
