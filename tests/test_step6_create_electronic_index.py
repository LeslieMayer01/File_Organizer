import unittest
from unittest.mock import MagicMock, patch

from organizer import step6_create_electronic_index as sei


class TestElectronicIndex(unittest.TestCase):

    @patch("os.listdir")
    def test_get_empty_folders(self, mock_listdir):
        mock_listdir.return_value = []
        result = sei.get_empty_folders("dummy/path")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Causa del problema"], "Carpeta vacía")

    @patch("os.listdir")
    @patch("os.path.getsize")
    @patch("os.path.isfile")
    def test_get_empty_files(self, mock_isfile, mock_getsize, mock_listdir):
        mock_listdir.return_value = ["file1.txt", "file2.txt"]
        mock_isfile.return_value = True
        mock_getsize.return_value = 0
        result = sei.get_empty_files("dummy/path")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["Causa del problema"], "Archivo vacío")

    def test_format_file_size(self):
        with patch("os.path.getsize", return_value=500):
            self.assertEqual(sei.format_file_size("dummy.txt"), "500 B")
        with patch("os.path.getsize", return_value=2048):
            self.assertIn("KB", sei.format_file_size("dummy.txt"))
        with patch("os.path.getsize", return_value=1048576):
            self.assertIn("MB", sei.format_file_size("dummy.txt"))

    def test_add_datetime(self):
        filename = "report.xlsx"
        result = sei.add_datetime(filename)
        self.assertTrue(result.endswith("-report.xlsx"))

    def test_valid_document(self):
        self.assertTrue(sei.valid_document("10_doc.pdf"))
        self.assertFalse(sei.valid_document(".hidden"))
        self.assertFalse(sei.valid_document("desktop.ini"))
        self.assertFalse(sei.valid_document("00IndiceElectronicoX.xlsm"))

    def test_filter_target_folders(self):
        dirs = ["01PrimeraInstancia", "temp", "02SegundaInstancia"]
        filtered = sei.filter_target_folders(dirs)
        self.assertEqual(
            filtered,
            ["01PrimeraInstancia", "02SegundaInstancia"],
        )

    def test_get_file_info_pdf(self):
        mock_path = "document.pdf"
        with patch("os.path.getctime", return_value=0), patch(
            "os.path.getsize", return_value=1024
        ), patch("fitz.open", MagicMock(return_value=MagicMock(page_count=3))):
            info = sei.get_file_info(mock_path)
            self.assertEqual(info["file_extension"], "PDF")
            self.assertEqual(info["page_count"], 3)

    def test_validate_files_with_numeric_prefix(self):
        with patch("os.listdir", return_value=["01doc.pdf", "Zcontrol.xlsx"]):
            self.assertIsNone(sei.validate_files_with_numeric_prefix("dummy"))
        with patch("os.listdir", return_value=["doc.pdf"]):
            result = sei.validate_files_with_numeric_prefix("dummy")
            self.assertEqual(
                result[0]["Causa del problema"],
                "Sin prefijo numérico de 2 dígitos",
            )

    @patch("pandas.read_excel")
    def test_buscar_radicado_en_base_de_datos_found(self, mock_read_excel):
        mock_df = MagicMock()
        mock_df.iloc.__getitem__.return_value.str.contains.return_value = [
            True,
        ]
        mock_df.__getitem__.return_value = mock_df
        mock_df.empty = False
        mock_df.iloc[:, [4, 5]].to_dict.return_value = [
            {"col1": "val1", "col2": "val2"}
        ]

        mock_read_excel.return_value = mock_df

        result = sei.buscar_radicado_en_base_de_datos("radicado")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["col1"], "val1")

    @patch("pandas.read_excel")
    def test_buscar_radicado_en_base_de_datos_not_found(self, mock_read_excel):
        mock_df = MagicMock()
        mock_df.iloc.__getitem__.return_value.str.contains.return_value = []
        mock_df.__getitem__.return_value = mock_df
        mock_df.empty = True

        mock_read_excel.return_value = mock_df

        result = sei.buscar_radicado_en_base_de_datos("no_existe")
        self.assertIsInstance(result, list)
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
