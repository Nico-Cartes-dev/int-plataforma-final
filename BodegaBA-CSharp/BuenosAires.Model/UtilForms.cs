using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Windows.Forms;
using BuenosAires.Model.Utiles;

namespace BuenosAires.Model.Utiles
{
    public static class UtilForms
    {

        public static DataGridViewTextBoxColumn GetColumn(string nombreCampo, string titulo)
        {
            return new DataGridViewTextBoxColumn()
            {
                Name = nombreCampo,
                DataPropertyName = nombreCampo,
                HeaderText = titulo
            };
        }

        public static void ConfigurarDataGridView(this DataGridView dgv, string columnas)
        {
            dgv.AutoGenerateColumns = false;
            string[] keyValuePairs = columnas.Split(',');
            var dgcols = new DataGridViewColumn[keyValuePairs.Count()];
            int index = 0;
            foreach (string pair in keyValuePairs)
            {
                string[] parts = pair.Split(':');
                string fieldName = parts[0].Trim();
                string headerText = parts[1].Trim();
                dgcols[index] = GetColumn(fieldName, headerText);
                index++;
            }
            dgv.Columns.AddRange(dgcols);
            dgv.ReadOnly = true;
            dgv.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
            dgv.MultiSelect = false;
        }

        public static void RefrescarYajustar(this DataGridView dgv)
        {
            dgv.Refresh();
            dgv.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
            dgv.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
            dgv.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
        }

        public static string GetString(this DataGridViewRow fila, string nombreCampo)
        {
            if (fila.Cells[nombreCampo].Value == null) return "";
            return fila.Cells[nombreCampo].Value.ToString();
        }

        public static void SeleccionarId(this DataGridView dgv, string nombreCampoID, int id)
        {
            int indiceFilaSeleccionada = -1;
            foreach (DataGridViewRow fila in dgv.Rows)
            {
                if (fila.Cells[nombreCampoID].Value.ToString() == id.ToString())
                {
                    indiceFilaSeleccionada = fila.Index;
                    break;
                }
            }
            if (indiceFilaSeleccionada != -1)
            {
                dgv.Rows[indiceFilaSeleccionada].Selected = true;
            }
        }

        public static bool EsNumero(this TextBox textBox)
        {
            return int.TryParse(textBox.Text, out int result);
        }
        
        public static int ToInt(this TextBox textBox)
        {
            return int.Parse(textBox.Text);
        }

        public static void SetText(this TextBox textBox, object valor)
        {
            textBox.Text = valor.ToString();
        }

        public static int ToIntOrDefault(this TextBox textBox)
        {
            return textBox.Text == "" ? 0 : textBox.ToInt();
        }

        public static void FocusToEnd(this TextBox textBox)
        {
            textBox.Focus();
            textBox.Select(textBox.Text.Length, 0);
        }

        public static void Limpiar(this Form form, TextBox[] textBoxs)
        {
            foreach (var textBox in textBoxs)
            {
                textBox.Text = "";
            }
        }

        public static void CentrarVentana(this Form form)
        {
            form.StartPosition = FormStartPosition.CenterScreen;
        }

        public static bool ErrRequerido(this Form form, string nombreCampo)
        {
            MessageBox.Show($"{nombreCampo} es un campo requerido, por lo que debe tener un valor."
                , UtilValidaciones.NombreSistema, MessageBoxButtons.OK
                , MessageBoxIcon.Exclamation);
            return false;
        }

        public static bool ErrEntero(this Form form, string nombreCampo)
        {
            MessageBox.Show($"El campo {nombreCampo} debe ser un número entero."
                , UtilValidaciones.NombreSistema, MessageBoxButtons.OK
                , MessageBoxIcon.Exclamation);
            return false;
        }

        public static bool ErrAccionID(this Form form, string nombreCampo, string accion)
        {
            MessageBox.Show($"Para poder {accion} debe seleccionar un número entero con el {nombreCampo}."
                , UtilValidaciones.NombreSistema, MessageBoxButtons.OK
                , MessageBoxIcon.Exclamation);
            return false;
        }

        public static bool MensajeInfo(this Form form, string mensaje)
        {
            MessageBox.Show(mensaje
                , UtilValidaciones.NombreSistema, MessageBoxButtons.OK
                , MessageBoxIcon.Information);
            return false;
        }

        public static bool MensajeExclam(this Form form, string mensaje)
        {
            MessageBox.Show(mensaje
                , UtilValidaciones.NombreSistema, MessageBoxButtons.OK
                , MessageBoxIcon.Exclamation);
            return false;
        }

        public static bool MensajeError(this Form form, string mensaje)
        {
            MessageBox.Show(mensaje, UtilValidaciones.NombreSistema, MessageBoxButtons.OK
                , MessageBoxIcon.Error);
            return false;
        }

        public static bool ObtenerValorPropiedad(object origen, string nombrePropiedad, out object valorPropiedad)
        {
            // Obtener todas las propiedades del objeto
            var propiedades = origen.GetType().GetProperties();

            // Recorrer cada propiedad
            foreach (var propiedad in propiedades)
            {
                // Obtener el nombre de la propiedad en mayúsculas
                var nombrePropiedadMayusculas = propiedad.Name.ToUpper();

                // Verificar si el nombre de la propiedad en mayúsculas coincide con el parámetro en mayúsculas
                if (nombrePropiedadMayusculas == nombrePropiedad.ToUpper())
                {
                    // Obtener el valor de la propiedad
                    valorPropiedad = propiedad.GetValue(origen);

                    // Devolver el valor de la propiedad
                    return true;
                }
            }

            // Si no se encuentra ninguna propiedad coincidente, devolver nulo
            valorPropiedad = null;
            return false;
        }

        // Este método copiará las propiedades de un objeto de origen
        // a las cajas de texto del formulario.
        // El método usará como criterio que el nombre de la caja de texto
        // comience con "txt" y que el resto del nombre sea igual al nombre
        // de una de las propiedades del objeto de origen. Por ejemplo:
        // si el nombre de la caja de texto es "txtNomProducto", el método
        // asignará el valor de la propiedad "NomProducto" del objeto
        // "Producto" indicado en el parámetro origen, a la caja de texto
        // "txtNomProducto".
        public static void AsignarValoresTextBox(this Form form, object origen)
        {
            var controlsStack = new Stack<Control>();
            controlsStack.Push(form);

            while (controlsStack.Count > 0)
            {
                var control = controlsStack.Pop();

                if (control is TextBox textBox && control.Name.StartsWith("txt"))
                {
                    var nomProp = control.Name.Substring(3);

                    if (ObtenerValorPropiedad(origen, nomProp, out object valProp))
                    {
                        textBox.Text = valProp == null ? "" : valProp.ToString();
                    }
                }

                if (control.HasChildren)
                {
                    foreach (Control childControl in control.Controls)
                    {
                        controlsStack.Push(childControl);
                    }
                }
            }
        }

        public static void AsignarValoresTextBox(this Form form, DataGridViewRow row)
        {
            foreach (DataGridViewCell cell in row.Cells)
            {
                string cellValue = "";
                if (cell != null) cellValue = cell.Value?.ToString();
                string nomPropCelda = cell.OwningColumn.DataPropertyName;

                var controlsStack = new Stack<Control>();
                controlsStack.Push(form);

                while (controlsStack.Count > 0)
                {
                    var control = controlsStack.Pop();

                    if (control is TextBox textBox && control.Name.StartsWith("txt"))
                    {
                        var nomProp = control.Name.Substring(3);

                        if (nomProp.ToUpper() == nomPropCelda.ToUpper())
                        {
                            textBox.Text = cellValue;
                        }
                    }

                    if (control.HasChildren)
                    {
                        foreach (Control childControl in control.Controls)
                        {
                            controlsStack.Push(childControl);
                        }
                    }
                }
            }
        }
    }
}
