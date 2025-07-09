using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace BuenosAires.BodegaBA
{
    public partial class VentanaBuscarID : Form
    {
        public VentanaBuscarID()
        {
            InitializeComponent();
            StartPosition = FormStartPosition.CenterScreen;
        }

        public int MostrarVentanaModal()
        {
            // Muestra la ventana modal y devuelve el número ingresado
            if (ShowDialog() == DialogResult.OK)
            {
                return int.Parse(TxtID.Text);
            }
            else
            {
                return -1;
            }
        }

        private void BtnBuscar_Click(object sender, EventArgs e)
        {
            // Verifica si el número ingresado es válido
            if (int.TryParse(TxtID.Text, out int IdNumerico))
            {
                // Cierra la ventana modal y devuelve el número
                DialogResult = DialogResult.OK;
                Close();
            }
            else
            {
                // Muestra un mensaje de error si el número es inválido
                MessageBox.Show("Ingrese un número válido.", 
                    "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void BtnCancelar_Click(object sender, EventArgs e)
        {
            DialogResult = DialogResult.Cancel;
            Close();
        }
    }
}