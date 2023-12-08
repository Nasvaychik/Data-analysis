import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import pandas as pd
import matplotlib.pyplot as plt


class App:
    def __init__(self, page: ft.Page):
        self.chart_generated = False

        self.page = page

        self.page.title = 'Аналитика данных'
        self.page.theme_mode = 'dark'
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.file = None
        self.file_picker = ft.FilePicker(on_result=self.__open_file_result)

        self.page.overlay.append(self.file_picker)

        self.page.add(
            ft.Row(
                [

                    ft.ElevatedButton(text='Открыть файл', icon=ft.icons.UPLOAD_FILE, on_click=self.open_file),
                    ft.OutlinedButton(text='Данные для построения графика', icon=ft.icons.SAVE,
                                      on_click=self.plot_data),
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

    def __open_file_result(self, e, *args, **kwargs):
        self.file = pd.read_csv(e.files[0].path)

        if self.chart_generated:
            self.page.remove_at(-1)

        self.show_dialog('Файл успешно загружен!')

    def open_file(self, *args, **kwargs):
        self.file_picker.pick_files(
            dialog_title='Выберите файл',
            allowed_extensions=['csv'],
            allow_multiple=False
        )

    def validate_file(self):
        if self.file is None:
            return True, 'Сначала выберите файл.'

        if self.file.empty:
            return True, 'Открытый Вами файл пуст.'

        return False, None

    def plot_data(self, *args, **kwargs):
        has_error, message = self.validate_file()

        if has_error:
            return self.show_dialog(message)

        df = self.file

        try:
            fig, ax = plt.subplots()
            values = df._mgr.items.values
            ax.plot(*[df[key] for key in values[0:2]])
        except TypeError:
            return self.show_dialog('Неверный формат координат для графика.'
                                    'Координаты должны быть вещественным числом')

        self.page.add(MatplotlibChart(fig, expand=True))
        self.chart_generated = True

    def show_dialog(self, message: str = None):
        dialog = ft.AlertDialog(
            title=ft.Text(message)
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()


if __name__ == '__main__':
    ft.app(target=App)