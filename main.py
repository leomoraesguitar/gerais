import os
import re
import json
import flet as ft
import yt_dlp


class SaveSelectFile2(ft.Row):
    def __init__(self, tipo, nome = None, json = None):
        '''
        tipo  == path: seleciona uma pasta (retorna o caminho completo da pasta selecionada)
        tipo  == file: seleciona um arquivo (retorna o caminho completo do arquivo selecionado)
        tipo  == save: sala um arquivo (retorna o caminho completo do arquivo, junto com seu nome)
        
        '''
        super().__init__()
        self.nome = nome
        self.arquiv = self.ler_json(json, default={
                    "pasta_donwloads": r'C:'
                })        
        self._diretorio = self.arquiv["pasta_donwloads"]        
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.tamanho_texto = 500
        self.selected_files = ft.Text(width=self.tamanho_texto, selectable=True, max_lines = 1)
        self._value = self.selected_files.value
        self.tipo = tipo

        def Selecionar_arquivo(_):
            self.pick_files_dialog.pick_files(allow_multiple=True)

        def Selecionar_pasta(_):
            self.pick_files_dialog.get_directory_path(dialog_title = 'askdjahs', initial_directory = self._diretorio)

        def Save1(_):
            self.pick_files_dialog.save_file()            



        if tipo == 'file':
            if self.nome == None:
                self.nome = 'Selecione o arquivo'            
            self.controls = [
                ft.ElevatedButton(
                    self.nome,
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=Selecionar_arquivo,
                ),
                self.selected_files,
            ]
        elif tipo == 'path':
            if self.nome == None:
                self.nome = 'Selecione a pasta'
            self.controls = [
                ft.ElevatedButton(
                    self.nome,
                    icon=ft.icons.FOLDER,
                    on_click=Selecionar_pasta,
                ),
                self.selected_files,
            ]   
        elif tipo == 'save':
            if self.nome == None:
                self.nome = 'Digite o nome do arquivo'            
            self.controls = [
                ft.ElevatedButton(
                    self.nome,
                    icon=ft.icons.SAVE,
                    on_click=Save1,
                ),
                self.selected_files,

            ]                      

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        if self.tipo == 'file':
            self.selected_files.value = (
                ",".join(map(lambda f: f.path, e.files)) if e.files else "Cancelled!"
            )
        elif self.tipo == 'path':
            self.selected_files.value = e.path if e.path else "Cancelled!"

        elif self.tipo == 'save':
            self.selected_files.value = e.path if e.path else "Cancelled!"            
            

        self.selected_files.update()
        self._value = self.selected_files.value


    # happens when example is added to the page (when user chooses the FilePicker control from the grid)
    def did_mount(self):
        self.page.overlay.append(self.pick_files_dialog)
        self.page.update()

    # happens when example is removed from the page (when user chooses different control group on the navigation rail)
    def will_unmount(self):
        self.page.overlay.remove(self.pick_files_dialog)
        self.page.update()

    def escrever_json(self, data, filename):
        if not filename.endswith('.json'):
            filename += '.json'
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def ler_json(self, filename, default=None):
        if not filename.endswith('.json'):
            filename += '.json'
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            try:
                self.escrever_json(default, filename)
            except:
                pass
            return default or {}



    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, valor):
        self._value = valor
        self.selected_files.value = valor
        # self.selected_files.update()

class BaixarDoYoutube:
    def __init__(self,output):
        self.converter_para_mp3 = False
        self.output = output
        self.arquiv = self.ler_json('config_baixar_youtube', default={
                    "pasta_donwloads": r'D:\baixados\tjse\mandados\2014'
                })        
        self._diretorio = self.arquiv["pasta_donwloads"]
        self.nomes = []
        self.bitrate = '320'
        self.ffmpeg_path = r'D:\baixados\programas_python\ffmpeg-2024-07-10-git-1a86a7a48d-essentials_build\ffmpeg-2024-07-10-git-1a86a7a48d-essentials_build\bin'  # Altere para o caminho correto do seu ffmpeg
         # Opções de download
        self.ydl_opts = {
            'format': 'bestaudio/best',  # Seleciona o melhor formato de áudio
            'outtmpl': os.path.join(self._diretorio, '%(title)s.%(ext)s'),  # Nome do arquivo de saída

            'ffmpeg_location': self.ffmpeg_path,  # Especifica o caminho para o ffmpeg
        }



    def remove_invalid_characters(self, filename):
        forbidden_characters = ['\\', '/', ':', '*', '?', '¿','[', ']', '{', '}' '"', '<', '>', '|', ')', '(','|' ]
        clean_filenames = []
        for character in forbidden_characters:
            filename = filename.replace(character, '')
        return filename


    # def Convert_to_mp32(self, stem):
    #     if stem.mime_type in ["audio/mp4"]:
    #         nome = stem.title +'.mp4'
    #         audio = AudioSegment.from_file(nome, format="mp4")


    #     elif stem.mime_type in ["audio/webm"]:
    #         nome = stem.title +'.webm'
    #         audio = AudioSegment.from_file(nome, format="webm")

    #     saida = stem.title +'.mp3'
    #     audio.export(saida, format="mp3")
    #     self.output(f"'{saida}' convertido com sucesso")


    # def Convert_to_mp3(self):
    #     self.output(f"convertendo para mp3....")

    #     audio = AudioSegment.from_file(self.nome_save, format= self.extencao[1:])
    #     saida = self.nome +'.mp3'
    #     saida = os.path.join(self._diretorio, saida)

    #     audio.export(saida, format="mp3", bitrate = self.bitrate)
    #     self.output(f"'{saida}' convertido para mp3 com sucesso\n")
    #     os.remove(self.nome_save) #deletar o arquivo não convertido
                

    def Download(self, url):
        if self.converter_para_mp3:
            self.ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',  # Formato de saída (por exemplo, mp3)
                'preferredquality': self.bitrate,  # Qualidade do áudio
            }]
        else:
            self.ydl_opts['postprocessors'] = []

        def progress_hook(d):
            if d['status'] == 'finished':
                self.title = d['info_dict']['title']

        self.ydl_opts['progress_hooks'] = [progress_hook]

        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([url])

        self.output(f' "{self.title}" foi baixado com sucesso para a pasta {self._diretorio} ')
        
                


    def BaixarAudio(self, url):
        self.Download(url)
    

    def Baixar(self, link):
        self.output(f"Iniciando donwload dos arquivos...")

        self.BaixarAudio(link)

    def escrever_json(self, data, filename):
        if not filename.endswith('.json'):
            filename += '.json'
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def ler_json(self, filename, default=None):
        if not filename.endswith('.json'):
            filename += '.json'
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            try:
                self.escrever_json(default, filename)
            except:
                pass
            return default or {}

    @property
    def diretorio(self):
        return self._diretorio
    @diretorio.setter
    def diretorio(self,valor):
        if valor not in ['', None]:
            self._diretorio = valor
            self.arquiv["pasta_donwloads"] = valor
            self.escrever_json(self.arquiv, 'config_baixar_youtube')


# if __name__ == '__main__':
#     link = 'https://www.youtube.com/watch?v=YyFd_dXy494&list=PLuo-Za1ITtoSDxMC0AQLfUDSztk06RsE6&ab_channel=AlineBarrosVEVO'
#     downloader = BaixarDoYoutube()
#     downloader.baixar(link)


def main(page: ft.Page):
    page.window_width = 300  # Define a largura da janela como 800 pixels
    page.window_height = 300  # 
    bgcolor = 'white'
    cor_texto = 'black'

    page.theme = ft.Theme(
        color_scheme_seed = 'white',
        color_scheme = ft.ColorScheme(background = 'white'),
        primary_color = 'red',
        primary_color_dark = 'red',
        primary_text_theme = ft.TextStyle(color = cor_texto),
        dialog_theme = ft.DialogTheme(
            bgcolor = bgcolor,
            title_text_style = ft.TextStyle(color = cor_texto),
            content_text_style = ft.TextStyle(color = cor_texto),
            alignment = ft.Alignment(0, 0),
            actions_padding = 2,
       )
        
    )

    COR1 = 'white,0.5'
    COR2 = 'black'
    COR3 = 'white'
    page.bgcolor = '#282a36'
    page.title = "Baixar vídeos do Youtube"
    # page.theme_mode = ft.ThemeMode.DARK
    # page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def escrever_json(data, filename):
        if not filename.endswith('.json'):
            filename += '.json'
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def ler_json( filename, default=None):
        if not filename.endswith('.json'):
            filename += '.json'
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            try:
                escrever_json(default, filename)
            except:
                pass
            return default or {}    

    def Get_links(e):
        url_pattern = r'https?://[^\s]+'
        url_field.value = re.findall(url_pattern, e.control.value)
        

    arquiv = ler_json('config_baixar_youtube', default={
                "pasta_donwloads": r'C:',
                "state_select":True
            })        
    state_select =  arquiv["state_select"]         
        
    def Chenge_select(e):
        arquiv["state_select"]  = e.control.value
        escrever_json(arquiv, 'config_baixar_youtube')

    url_field = ft.TextField(label = 'url',hint_text="Insira a URL do vídeo aqui", on_change=Get_links) #, border_color = 'white,0.8'
    download_button = ft.ElevatedButton("Baixar", on_click=lambda e: baixar_video(url_field.value))
    select_button = SaveSelectFile2('path', json='config_baixar_youtube')
    mp3 = ft.Checkbox(label = 'Converter para mp3?', value = state_select, on_change=Chenge_select, )
    output = ft.Text("")




    def Output(texto):
       output.value += f'{texto}\n'
       page.update()


    def baixar_video(url):
        # Aqui você pode chamar a função de download de vídeo
        downloader = BaixarDoYoutube(Output)
        downloader.diretorio = select_button.value
        downloader.converter_para_mp3 = mp3.value
        # print(downloader.diretorio)
        if isinstance(url, list):
            for i in url:
                if i not in ['', None]:
                    downloader.Baixar(i)


    page.add(
        ft.Column(
            [
                # ft.Text("Baixar vídeos do Youtube", style=ft.TextStyle(size=24)),
                url_field,
                select_button,                
                ft.Row([download_button]),
                ft.Container(ft.Column([output],auto_scroll = True, scroll=ft.ScrollMode.ADAPTIVE, height=90, width=page.window_height),bgcolor=f'red,0.1')
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

ft.app(main, 

# view=ft.AppView.WEB_BROWSER

)
