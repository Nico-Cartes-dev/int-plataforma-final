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
    public partial class VentanaPrincipal : Form
    {
        public VentanaPrincipal()
        {
            InitializeComponent();
        }

        // Add a constructor that accepts a string parameter to fix the error  
        public VentanaPrincipal(string userInfo) : this()
        {
            // Optionally, you can use the userInfo parameter to set a label or other UI element  
            this.Text = userInfo;
        }

        private void VentanaPrincipal_Load(object sender, EventArgs e)
        {

        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            new ConsultarBodega().Show();
            Hide();
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        // Cierra la aplicación
        private void btnSalir_Click(object sender, EventArgs e)
        {
            System.Windows.Forms.Application.Exit();
        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void button2_Click(object sender, EventArgs e)
        {
            new VentanaGuiasDespacho().Show();
            Hide();
        }

        private void btnReservarEquipos_Click(object sender, EventArgs e)
        {
            new VentanaReservarAnwo().Show();
            Hide();
        }
    }
}
